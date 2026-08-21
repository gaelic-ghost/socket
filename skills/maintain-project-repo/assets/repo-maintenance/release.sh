#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export REPO_MAINTENANCE_COMMON_DIR="$SELF_DIR/lib"
. "$SELF_DIR/lib/common.sh"

load_profile_env
load_env_file "$SELF_DIR/config/release.env"

mode="${REPO_MAINTENANCE_DEFAULT_RELEASE_MODE:-standard}"
release_tag=""
skip_validate="false"
skip_gh_release="false"
skip_version_bump="false"
base_branch="${REPO_MAINTENANCE_RELEASE_BRANCH:-main}"
review_comments_addressed="false"
skip_branch_cleanup="false"
dry_run="false"
operation="${REPO_MAINTENANCE_RELEASE_OPERATION:-prepare}"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --mode)
      mode="${2:-}"
      shift 2
      ;;
    --version)
      release_tag="${2:-}"
      shift 2
      ;;
    --skip-validate)
      skip_validate="true"
      shift
      ;;
    --skip-gh-release)
      skip_gh_release="true"
      shift
      ;;
    --skip-version-bump)
      skip_version_bump="true"
      shift
      ;;
    --base-branch)
      base_branch="${2:-}"
      shift 2
      ;;
    --review-comments-addressed)
      review_comments_addressed="true"
      shift
      ;;
    --operation)
      operation="${2:-}"
      shift 2
      ;;
    --skip-branch-cleanup)
      skip_branch_cleanup="true"
      shift
      ;;
    --dry-run)
      dry_run="true"
      shift
      ;;
    -h|--help)
      cat <<'USAGE'
Usage:
  release.sh --mode standard --version <vX.Y.Z> --operation prepare|inspect|advance [--base-branch main] [--skip-validate] [--skip-version-bump] [--skip-gh-release] [--review-comments-addressed] [--skip-branch-cleanup] [--dry-run]
  release.sh --mode submodule --version <vX.Y.Z> [--skip-validate] [--skip-gh-release] [--dry-run]
USAGE
      exit 0
      ;;
    *)
      die "Unknown release argument: $1"
      ;;
  esac
done

[ -n "$release_tag" ] || die "Pass --version vX.Y.Z when running the release workflow."

export REPO_MAINTENANCE_RELEASE_MODE="$mode"
export RELEASE_TAG="$release_tag"
export REPO_MAINTENANCE_SKIP_GH_RELEASE="$skip_gh_release"
export REPO_MAINTENANCE_DRY_RUN="$dry_run"
export REPO_MAINTENANCE_RELEASE_OPERATION="$operation"

ensure_clean_worktree() {
  status_output="$(git -C "$REPO_ROOT" status --porcelain)"
  [ -z "$status_output" ] || die "Release workflow requires committed changes and a clean worktree before it can continue."
}

ensure_gh_cli() {
  command -v gh >/dev/null 2>&1 || die "Standard release mode requires the GitHub CLI gh so it can inspect and advance the pull request, merge, and publish the release."
}

ensure_semver_tag() {
  case "$RELEASE_TAG" in
    v[0-9]*.[0-9]*.[0-9]*|v[0-9]*.[0-9]*.[0-9]*-*)
      ;;
    *)
      die "Release tag must use vX.Y.Z SemVer syntax."
      ;;
  esac
}

ensure_operation() {
  case "$REPO_MAINTENANCE_RELEASE_OPERATION" in
    prepare|inspect|advance)
      ;;
    *)
      die "Release operation must be prepare, inspect, or advance. Long-running remote checks must be resumed by a host-native scheduled continuation, never watched from this script."
      ;;
  esac
}

current_branch() {
  git -C "$REPO_ROOT" symbolic-ref --quiet --short HEAD || true
}

ensure_branch_release_context() {
  branch_name="$(current_branch)"
  [ -n "$branch_name" ] || die "Standard release mode requires a named feature branch or worktree instead of detached HEAD."
  [ "$branch_name" != "$base_branch" ] || die "Standard release mode must run from a release branch or worktree, not protected $base_branch."
  printf '%s\n' "$branch_name"
}

run_version_bump() {
  release_version="${RELEASE_TAG#v}"
  version_bump_script="$SELF_DIR/version-bump.sh"
  head_subject="$(git -C "$REPO_ROOT" log -1 --format=%s 2>/dev/null || true)"

  if [ "$skip_version_bump" = "true" ]; then
    log "Skipping repo version bump because --skip-version-bump was requested."
    return 0
  fi

  if [ "$head_subject" = "release: bump versions for $RELEASE_TAG" ]; then
    log "Version bump commit for $RELEASE_TAG is already at HEAD; continuing the release resume path."
    return 0
  fi

  [ -x "$version_bump_script" ] || die "Standard release mode expected an executable repo-specific version bump hook at $version_bump_script. Add that hook so the repo's version surfaces move together, or rerun with --skip-version-bump when this release intentionally has no version-bearing files."

  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would run $version_bump_script $release_version with RELEASE_TAG=$RELEASE_TAG."
    return 0
  fi

  RELEASE_VERSION="$release_version" "$version_bump_script" "$release_version"

  if [ -z "$(git -C "$REPO_ROOT" status --porcelain)" ]; then
    die "Version bump hook completed without changing files. Update $version_bump_script to edit the repo's version surfaces, or rerun with --skip-version-bump if this release intentionally has no version bump."
  fi

  git -C "$REPO_ROOT" add -A
  git -C "$REPO_ROOT" commit -m "release: bump versions for $RELEASE_TAG"
  log "Committed version bump for $RELEASE_TAG."
}

create_release_tag() {
  head_sha="$(git -C "$REPO_ROOT" rev-parse HEAD)"
  tag_sha="$(git -C "$REPO_ROOT" rev-parse -q --verify "refs/tags/$RELEASE_TAG" 2>/dev/null || true)"

  if [ -n "$tag_sha" ]; then
    tag_commit_sha="$(git -C "$REPO_ROOT" rev-list -n 1 "$RELEASE_TAG")"
    [ "$tag_commit_sha" = "$head_sha" ] || die "Tag $RELEASE_TAG already exists and does not point at HEAD."
    log "Tag $RELEASE_TAG already points at HEAD."
    return 0
  fi

  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would create annotated tag $RELEASE_TAG at HEAD."
    return 0
  fi

  git -C "$REPO_ROOT" tag -a "$RELEASE_TAG" -m "Release $RELEASE_TAG"
  log "Created annotated tag $RELEASE_TAG."
}

push_release_branch() {
  branch_name="$1"

  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would push branch $branch_name to origin."
    return 0
  fi

  git -C "$REPO_ROOT" push -u origin "$branch_name"
  log "Pushed branch $branch_name."
  remote_branch_is_visible "$branch_name" || return 1
}

push_release_tag() {
  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would push tag $RELEASE_TAG to origin."
    return 0
  fi

  git -C "$REPO_ROOT" push origin "$RELEASE_TAG"
  log "Pushed tag $RELEASE_TAG."
  remote_tag_is_visible "$RELEASE_TAG" || return 1
}

create_or_update_pr() {
  branch_name="$1"
  PR_NUMBER=""

  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would create or update a release PR from $branch_name into $base_branch."
    PR_NUMBER="DRY-RUN"
    return 0
  fi

  body_file="$(mktemp "${TMPDIR:-/tmp}/repo-maintenance-release-pr.XXXXXX")"
  trap 'rm -f "$body_file"' EXIT INT TERM

  cat >"$body_file" <<EOF
## Release

- prepares $RELEASE_TAG from branch \`$branch_name\`
- keeps protected \`$base_branch\` updates behind pull request review and CI
- release tag \`$RELEASE_TAG\` will be created after CI and the review-comment gate pass, so failed or still-discussed release candidates do not get tagged

## Continuation Gate

Before merge and tagging, use \`release.sh --operation inspect\` after CI and review contexts have had time to settle. Agents schedule a host-native continuation at least five minutes later; this script never watches or polls remote state.
EOF

  pr_number="$(gh pr list --head "$branch_name" --base "$base_branch" --json number --jq '.[0].number // empty' --limit 1)"
  if [ -n "$pr_number" ]; then
    pr_url="$(gh pr view "$pr_number" --json url --jq '.url')"
    gh pr edit "$pr_number" --title "release: prepare $RELEASE_TAG" --body-file "$body_file" >/dev/null
    log "Updated existing release PR #$pr_number at $pr_url."
  else
    gh pr create --base "$base_branch" --head "$branch_name" --title "release: prepare $RELEASE_TAG" --body-file "$body_file" >/dev/null
    pr_number="$(gh pr list --head "$branch_name" --base "$base_branch" --json number --jq '.[0].number // empty' --limit 1)"
    [ -n "$pr_number" ] || die "GitHub CLI did not return a release PR number after creating the pull request."
    pr_url="$(gh pr view "$pr_number" --json url --jq '.url')"
    log "Created release PR #$pr_number at $pr_url."
    PR_NUMBER="$pr_number"
    return 0
  fi

  PR_NUMBER="$pr_number"
}

inspect_pr_gate() {
  pr_number="$1"
  minimum_check_count="${REPO_MAINTENANCE_MIN_REQUIRED_CHECKS:-1}"
  case "$minimum_check_count" in
    ''|*[!0-9]*) die "REPO_MAINTENANCE_MIN_REQUIRED_CHECKS must be a non-negative integer; received $minimum_check_count." ;;
  esac
  if CHECK_STATE="$(gh pr checks "$pr_number" --json name,bucket --jq 'map(.name + ":" + .bucket) | join(",")' 2>/dev/null)"; then
    check_readable="true"
  elif [ -n "${CHECK_STATE:-}" ]; then
    # gh pr checks exits 8 while pending even when it returned valid JSON output.
    check_readable="true"
  else
    CHECK_STATE="unreadable"
    check_readable="false"
  fi
  if CHECK_BUCKETS="$(gh pr checks "$pr_number" --json bucket --jq 'map(.bucket) | join(",")' 2>/dev/null)"; then
    :
  elif [ -z "${CHECK_BUCKETS:-}" ]; then
    check_readable="false"
  fi
  if check_count="$(gh pr checks "$pr_number" --json bucket --jq 'length' 2>/dev/null)"; then
    :
  elif [ -z "${check_count:-}" ]; then
    check_readable="false"
  fi
  REVIEW_DECISION="$(gh pr view "$pr_number" --json reviewDecision --jq '.reviewDecision // ""' 2>/dev/null || printf 'UNREADABLE')"
  COMMENT_COUNT="$(gh pr view "$pr_number" --json comments,reviews --jq '([.comments[]?, (.reviews[]? | select(.state == "COMMENTED"))] | length)' 2>/dev/null || printf '1')"
  if [ "$check_readable" != "true" ] || [ "$REVIEW_DECISION" = "UNREADABLE" ]; then
    GATE_PHASE="awaiting-github-state"
  elif [ "$check_count" -lt "$minimum_check_count" ]; then
    GATE_PHASE="awaiting-github-state"
  elif case ",$CHECK_BUCKETS," in *,fail,*|*,cancel,*) true ;; *) false ;; esac; then
    GATE_PHASE="failed-checks"
  elif case ",$CHECK_BUCKETS," in *,pending,*) true ;; *) false ;; esac; then
    GATE_PHASE="awaiting-pr-checks"
  elif [ "$REVIEW_DECISION" = "CHANGES_REQUESTED" ]; then
    GATE_PHASE="changes-requested"
  else
    GATE_PHASE="ready-to-advance"
  fi
  log "PR #$pr_number snapshot: phase=$GATE_PHASE; checks=${CHECK_STATE:-none}; review=${REVIEW_DECISION:-none}; comments=$COMMENT_COUNT."
}

emit_continuation_packet() {
  pr_number="$1"
  branch_name="$2"
  phase="$3"
  resume_operation="inspect"
  case "$phase" in
    not-started|awaiting-branch-visibility)
      resume_operation="prepare"
      ;;
  esac
  repo_name="$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null || printf 'unknown')"
  head_sha="$(git -C "$REPO_ROOT" rev-parse HEAD)"
  printf '%s\n' "{\"schema\":\"repo-maintenance-continuation/v1\",\"operation\":\"standard-release\",\"repository\":\"$repo_name\",\"release_tag\":\"$RELEASE_TAG\",\"branch\":\"$branch_name\",\"head_commit\":\"$head_sha\",\"pr_number\":\"$pr_number\",\"phase\":\"$phase\",\"minimum_delay_minutes\":5,\"resume_command\":\"scripts/repo-maintenance/release.sh --mode standard --version $RELEASE_TAG --operation $resume_operation\",\"advance_command\":\"scripts/repo-maintenance/release.sh --mode standard --version $RELEASE_TAG --operation advance\"}"
  log "Before scheduling, reuse a live matching host-native continuation while this gate is pending and healthy; do not delete/recreate it after an unchanged snapshot. Create or update one only after it fires or becomes stale, no sooner than five minutes. On wakeup run inspect first; run advance only if this branch, commit, PR, and tag still match."
}

check_pr_comments() {
  pr_number="$1"

  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would check PR #$pr_number for comments and requested changes."
    return 0
  fi

  review_decision="$REVIEW_DECISION"
  comment_count="$COMMENT_COUNT"

  if [ "$review_decision" = "CHANGES_REQUESTED" ]; then
    gh pr view "$pr_number" --comments
    die "PR #$pr_number has requested changes. Address valid concerns in code, or add out-of-scope concerns to ROADMAP.md, resolve the threads, push, and rerun release.sh."
  fi

  if [ "$comment_count" != "0" ] && [ "$review_comments_addressed" != "true" ]; then
    gh pr view "$pr_number" --comments
    die "PR #$pr_number has review or discussion comments. Address and resolve valid concerns, add out-of-scope concerns to ROADMAP.md, then rerun release.sh with --review-comments-addressed once the comment pass is intentionally complete."
  fi

  log "PR #$pr_number has no blocking review state."
}

merge_pr() {
  pr_number="$1"

  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would merge PR #$pr_number into $base_branch with a merge commit and delete the remote branch."
    return 0
  fi

  gh pr merge "$pr_number" --merge --delete-branch
  log "Merged PR #$pr_number into $base_branch."
}

fast_forward_base_branch() {
  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would fast-forward local $base_branch from origin/$base_branch."
    return 0
  fi

  git -C "$REPO_ROOT" fetch origin "$base_branch"
  if git -C "$REPO_ROOT" switch "$base_branch" 2>/dev/null || git -C "$REPO_ROOT" checkout "$base_branch" 2>/dev/null; then
    git -C "$REPO_ROOT" pull --ff-only origin "$base_branch"
    log "Fast-forwarded local $base_branch."
  else
    die "Could not check out local $base_branch, likely because another worktree owns it. Fast-forward $base_branch from origin/$base_branch in that checkout, then rerun release.sh so the release tag is created from the reviewed base branch."
  fi
}

create_github_release() {
  if [ "$REPO_MAINTENANCE_SKIP_GH_RELEASE" = "true" ]; then
    log "Skipping GitHub release creation because --skip-gh-release was requested."
    return 0
  fi

  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    prerelease_flag="$(github_release_create_prerelease_flag "$RELEASE_TAG")"
    log "Would create a GitHub release for $RELEASE_TAG with gh release create --verify-tag${prerelease_flag:+ $prerelease_flag}."
    return 0
  fi

  if gh release view "$RELEASE_TAG" >/dev/null 2>&1; then
    verify_github_release_prerelease_metadata "$RELEASE_TAG"
    log "GitHub release $RELEASE_TAG already exists."
    return 0
  fi

  prerelease_flag="$(github_release_create_prerelease_flag "$RELEASE_TAG")"
  create_github_release_from_notes_or_generated "$RELEASE_TAG" "$prerelease_flag"
  log "Created GitHub release $RELEASE_TAG."
  if ! github_release_is_visible "$RELEASE_TAG"; then
    warn "GitHub release $RELEASE_TAG is not readable in this immediate re-read. Schedule a continuation for at least five minutes rather than polling."
    return 1
  fi
  verify_github_release_prerelease_metadata "$RELEASE_TAG"
}

cleanup_merged_branches() {
  release_branch_name="$1"

  if [ "$skip_branch_cleanup" = "true" ]; then
    log "Skipping local merged-branch cleanup because --skip-branch-cleanup was requested."
    return 0
  fi

  if [ "$REPO_MAINTENANCE_DRY_RUN" = "true" ]; then
    log "Would prune origin and delete local branches already merged into $base_branch, including $release_branch_name when safe."
    return 0
  fi

  git -C "$REPO_ROOT" remote prune origin
  for merged_branch in $(git -C "$REPO_ROOT" for-each-ref --format='%(refname:short)' --merged "$base_branch" refs/heads); do
    case "$merged_branch" in
      "$base_branch")
        ;;
      *)
        git -C "$REPO_ROOT" branch -d "$merged_branch" >/dev/null 2>&1 || warn "Could not delete local merged branch $merged_branch; it may be checked out in another worktree."
        ;;
    esac
  done
  log "Cleaned up local branches already merged into $base_branch where safe."
}

run_standard_release() {
  ensure_git_repo
  ensure_gh_cli
  ensure_semver_tag
  ensure_operation

  if [ "$REPO_MAINTENANCE_RELEASE_OPERATION" = "inspect" ]; then
    branch_name="$(current_branch)"
    if [ -z "$branch_name" ]; then
      log "Release inspection state: not-started; no named branch is checked out."
      return 0
    fi
    pr_number="$(gh pr list --head "$branch_name" --base "$base_branch" --json number --jq '.[0].number // empty' --limit 1)"
    if [ -z "$pr_number" ]; then
      emit_continuation_packet "pending" "$branch_name" "not-started"
      log "Release inspection state: not-started; no release PR exists for branch $branch_name."
      return 0
    fi
    inspect_pr_gate "$pr_number"
    emit_continuation_packet "$pr_number" "$branch_name" "$GATE_PHASE"
    return 0
  fi

  branch_name="$(ensure_branch_release_context)"
  ensure_clean_worktree

  if [ "$REPO_MAINTENANCE_RELEASE_OPERATION" = "prepare" ] && [ "$skip_validate" != "true" ]; then
    sh "$SELF_DIR/validate-all.sh"
  fi

  if [ "$REPO_MAINTENANCE_RELEASE_OPERATION" = "prepare" ]; then
    run_version_bump
    ensure_clean_worktree
    if ! push_release_branch "$branch_name"; then
      emit_continuation_packet "pending" "$branch_name" "awaiting-branch-visibility"
      return 0
    fi
    create_or_update_pr "$branch_name"
    pr_number="$PR_NUMBER"
    inspect_pr_gate "$pr_number"
    emit_continuation_packet "$pr_number" "$branch_name" "$GATE_PHASE"
    log "Standard release preparation completed for $RELEASE_TAG."
    return 0
  fi

  pr_number="$(gh pr list --head "$branch_name" --base "$base_branch" --json number --jq '.[0].number // empty' --limit 1)"
  [ -n "$pr_number" ] || die "No release PR exists for branch $branch_name into $base_branch. Run --operation prepare first."
  inspect_pr_gate "$pr_number"
  case "$GATE_PHASE" in
    awaiting-github-state|awaiting-pr-checks)
      emit_continuation_packet "$pr_number" "$branch_name" "$GATE_PHASE"
      return 0
      ;;
    failed-checks|changes-requested)
      die "Release PR #$pr_number is in $GATE_PHASE. Resolve the remote gate, push any correction, then use --operation inspect after a scheduled continuation."
      ;;
  esac
  check_pr_comments "$pr_number"
  merge_pr "$pr_number"
  fast_forward_base_branch
  create_release_tag
  if ! push_release_tag; then
    emit_continuation_packet "$pr_number" "$branch_name" "awaiting-tag-visibility"
    return 0
  fi
  if ! create_github_release; then
    emit_continuation_packet "$pr_number" "$branch_name" "awaiting-github-release-visibility"
    return 0
  fi
  cleanup_merged_branches "$branch_name"
  log "Standard release flow completed successfully for $RELEASE_TAG."
}

if [ "$mode" = "standard" ]; then
  run_standard_release
  exit 0
fi

if [ "$skip_validate" != "true" ]; then
  sh "$SELF_DIR/validate-all.sh"
fi

log "Running repo-maintenance release flow in $REPO_MAINTENANCE_RELEASE_MODE mode for $RELEASE_TAG with the $REPO_MAINTENANCE_PROFILE profile."
run_dispatch_dir "$SELF_DIR/release" "release"

if [ "$REPO_MAINTENANCE_RELEASE_MODE" = "submodule" ]; then
  log "Submodule release finished. Update the parent repository's submodule pointer in a separate follow-up commit."
fi

log "Repo-maintenance release flow completed successfully."
