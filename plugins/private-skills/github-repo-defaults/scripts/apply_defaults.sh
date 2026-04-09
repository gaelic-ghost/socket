#!/bin/sh

set -eu

usage() {
  cat <<'EOF'
Usage: apply_defaults.sh [options]

Applies GitHub repository defaults for the current local repository.

Options:
  --repo OWNER/NAME       Target repository (default: inferred from owner + local dir)
  --owner OWNER           GitHub owner when --repo is not set
  --remote NAME           Remote name to use/create (default: origin)
  --visibility VALUE      private|public|internal (default: private)
  --description TEXT      Override generated description
  --topics CSV            Comma-separated topics to merge with inferred topics
  --dry-run               Print actions without making API changes
  -h, --help              Show this help
EOF
}

err() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || err "Required command not found: $1"
}

trim() {
  printf '%s' "$1" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//'
}

sanitize_topic() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g; s/--*/-/g; s/^-//; s/-$//'
}

append_topic() {
  candidate="$(sanitize_topic "$1")"
  [ -n "$candidate" ] || return 0
  case ",$TOPICS_CSV," in
    *,"$candidate",*) return 0 ;;
    *)
      if [ -n "$TOPICS_CSV" ]; then
        TOPICS_CSV="$TOPICS_CSV,$candidate"
      else
        TOPICS_CSV="$candidate"
      fi
      ;;
  esac
}

infer_owner() {
  if gh auth status >/dev/null 2>&1; then
    owner="$(gh api user -q .login 2>/dev/null || true)"
    [ -n "$owner" ] && {
      printf '%s' "$owner"
      return 0
    }
  fi
  printf '%s' "${GITHUB_OWNER:-}"
}

readme_description() {
  [ -f README.md ] || return 1
  heading="$(sed -n 's/^#\{1,\}[[:space:]]*//p' README.md | sed -n '1p')"
  paragraph="$(
    awk '
      BEGIN { started=0; seen_heading=0 }
      /^#/ { if (!seen_heading) { seen_heading=1; next } else if (started) { exit } else { next } }
      /^[[:space:]]*$/ { if (started) exit; next }
      {
        started=1
        if (out == "") out=$0
        else out=out " " $0
      }
      END { print out }
    ' README.md
  )"
  heading="$(trim "$heading")"
  paragraph="$(trim "$paragraph")"
  if [ -n "$heading" ] && [ -n "$paragraph" ]; then
    printf '%s' "$heading: $paragraph"
    return 0
  fi
  if [ -n "$heading" ]; then
    printf '%s' "$heading"
    return 0
  fi
  return 1
}

package_json_description() {
  [ -f package.json ] || return 1
  if command -v jq >/dev/null 2>&1; then
    desc="$(jq -r '.description // empty' package.json 2>/dev/null || true)"
    desc="$(trim "$desc")"
    [ -n "$desc" ] || return 1
    printf '%s' "$desc"
    return 0
  fi
  return 1
}

pyproject_description() {
  [ -f pyproject.toml ] || return 1
  desc="$(
    awk '
      /^\[project\]/ { in_project=1; next }
      /^\[/ && in_project { in_project=0 }
      in_project && /^[[:space:]]*description[[:space:]]*=/ {
        line=$0
        sub(/^[^=]*=[[:space:]]*/, "", line)
        gsub(/^"/, "", line)
        gsub(/"$/, "", line)
        print line
        exit
      }
    ' pyproject.toml
  )"
  desc="$(trim "$desc")"
  [ -n "$desc" ] || return 1
  printf '%s' "$desc"
}

build_description() {
  if [ -n "$DESCRIPTION" ]; then
    printf '%s' "$DESCRIPTION"
    return 0
  fi
  if desc="$(readme_description)"; then
    printf '%.140s' "$desc"
    return 0
  fi
  if desc="$(package_json_description)"; then
    printf '%.140s' "$desc"
    return 0
  fi
  if desc="$(pyproject_description)"; then
    printf '%.140s' "$desc"
    return 0
  fi
  printf '%s: development project' "$REPO_NAME"
}

seed_topics() {
  append_topic "$REPO_NAME"
  OLDIFS="$IFS"
  IFS='-_'
  set -- $REPO_NAME
  IFS="$OLDIFS"
  for token in "$@"; do
    [ "${#token}" -ge 3 ] && append_topic "$token"
  done
  [ -f Package.swift ] && { append_topic "swift"; append_topic "swiftpm"; }
  [ -f pyproject.toml ] && append_topic "python"
  if [ -f package.json ]; then
    if [ -f tsconfig.json ]; then
      append_topic "typescript"
    else
      append_topic "javascript"
    fi
  fi
  [ -f Cargo.toml ] && append_topic "rust"
  [ -f Dockerfile ] && append_topic "docker"
  if [ -d .github/workflows ] && find .github/workflows -maxdepth 1 -type f \( -name '*.yml' -o -name '*.yaml' \) | grep -q .; then
    append_topic "github-actions"
  fi
}

merge_user_topics() {
  [ -n "$USER_TOPICS" ] || return 0
  OLDIFS="$IFS"
  IFS=','
  set -- $USER_TOPICS
  IFS="$OLDIFS"
  for topic in "$@"; do
    append_topic "$topic"
  done
}

limit_topics() {
  limited=""
  count=0
  OLDIFS="$IFS"
  IFS=','
  set -- $TOPICS_CSV
  IFS="$OLDIFS"
  for topic in "$@"; do
    [ -n "$topic" ] || continue
    count=$((count + 1))
    [ "$count" -le 8 ] || break
    if [ -n "$limited" ]; then
      limited="$limited,$topic"
    else
      limited="$topic"
    fi
  done
  TOPICS_CSV="$limited"
}

is_git_repo() {
  git rev-parse --is-inside-work-tree >/dev/null 2>&1
}

has_commits() {
  git rev-parse --verify HEAD >/dev/null 2>&1
}

repo_exists_remote() {
  gh repo view "$REPO_FULL" >/dev/null 2>&1
}

create_repo_if_needed() {
  if repo_exists_remote; then
    return 0
  fi

  if [ "$DRY_RUN" -eq 1 ]; then
    printf 'DRY RUN: gh repo create %s --%s --source . --remote %s%s\n' \
      "$REPO_FULL" "$VISIBILITY" "$REMOTE_NAME" "$PUSH_SUFFIX"
    return 0
  fi

  set -- gh repo create "$REPO_FULL" "--$VISIBILITY" --source . --remote "$REMOTE_NAME"
  if has_commits; then
    set -- "$@" --push
  fi
  "$@"
}

ensure_remote() {
  if git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
    return 0
  fi
  repo_url="$(gh repo view "$REPO_FULL" --json url -q .url)"
  [ -n "$repo_url" ] || err "Could not resolve repository URL for $REPO_FULL"
  if [ "$DRY_RUN" -eq 1 ]; then
    printf 'DRY RUN: git remote add %s %s\n' "$REMOTE_NAME" "$repo_url"
    return 0
  fi
  git remote add "$REMOTE_NAME" "$repo_url"
}

apply_settings() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf 'DRY RUN: gh api --method PATCH /repos/%s <settings-payload>\n' "$REPO_FULL"
    return 0
  fi
  gh api --method PATCH "/repos/$REPO_FULL" \
    -f description="$FINAL_DESCRIPTION" \
    -F has_issues=true \
    -F has_wiki=false \
    -F has_projects=false \
    -F has_discussions=false \
    -F delete_branch_on_merge=true \
    -F allow_update_branch=true \
    -F auto_close_issues=true \
    -F allow_squash_merge=true \
    -F allow_merge_commit=false \
    -F allow_rebase_merge=false >/dev/null
}

apply_topics() {
  [ -n "$TOPICS_CSV" ] || return 0
  if [ "$DRY_RUN" -eq 1 ]; then
    printf 'DRY RUN: gh api --method PUT /repos/%s/topics with topics: %s\n' "$REPO_FULL" "$TOPICS_CSV"
    return 0
  fi

  set -- gh api --method PUT "/repos/$REPO_FULL/topics"
  OLDIFS="$IFS"
  IFS=','
  for topic in $TOPICS_CSV; do
    set -- "$@" -f "names[]=$topic"
  done
  IFS="$OLDIFS"
  "$@" >/dev/null
}

show_summary() {
  printf 'Repository: %s\n' "$REPO_FULL"
  printf 'Remote: %s\n' "$REMOTE_NAME"
  printf 'Description: %s\n' "$FINAL_DESCRIPTION"
  printf 'Topics: %s\n' "$TOPICS_CSV"
  if [ "$DRY_RUN" -eq 1 ]; then
    printf 'Mode: dry-run\n'
    return 0
  fi
  gh repo view "$REPO_FULL" --json visibility,description -q '"visibility=\(.visibility) description=\(.description)"'
}

REPO_FULL=""
OWNER=""
REMOTE_NAME="origin"
VISIBILITY="private"
DESCRIPTION=""
USER_TOPICS=""
TOPICS_CSV=""
DRY_RUN=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo)
      [ "$#" -ge 2 ] || err "--repo requires a value"
      REPO_FULL="$2"
      shift 2
      ;;
    --owner)
      [ "$#" -ge 2 ] || err "--owner requires a value"
      OWNER="$2"
      shift 2
      ;;
    --remote)
      [ "$#" -ge 2 ] || err "--remote requires a value"
      REMOTE_NAME="$2"
      shift 2
      ;;
    --visibility)
      [ "$#" -ge 2 ] || err "--visibility requires a value"
      VISIBILITY="$2"
      shift 2
      ;;
    --description)
      [ "$#" -ge 2 ] || err "--description requires a value"
      DESCRIPTION="$2"
      shift 2
      ;;
    --topics)
      [ "$#" -ge 2 ] || err "--topics requires a value"
      USER_TOPICS="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      err "Unknown argument: $1"
      ;;
  esac
done

case "$VISIBILITY" in
  private|public|internal) ;;
  *) err "--visibility must be one of: private, public, internal" ;;
esac

require_cmd git
require_cmd gh
require_cmd sed
require_cmd awk
require_cmd tr
require_cmd grep

is_git_repo || err "Current directory is not a git repository"

REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"

if [ -z "$REPO_FULL" ]; then
  [ -n "$OWNER" ] || OWNER="$(infer_owner)"
  [ -n "$OWNER" ] || err "Could not infer owner. Set --owner or GITHUB_OWNER."
  REPO_FULL="$OWNER/$REPO_NAME"
fi

case "$REPO_FULL" in
  */*) ;;
  *) err "--repo must be in OWNER/NAME format" ;;
esac

PUSH_SUFFIX=""
has_commits && PUSH_SUFFIX=" --push"

FINAL_DESCRIPTION="$(build_description)"
seed_topics
merge_user_topics
limit_topics

create_repo_if_needed
ensure_remote
apply_settings
apply_topics
show_summary
