#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export REPO_MAINTENANCE_COMMON_DIR="$SELF_DIR/../lib"
. "$SELF_DIR/../lib/common.sh"

if [ "${REPO_MAINTENANCE_SKIP_GH_RELEASE:-false}" = "true" ]; then
  log "Skipping GitHub release creation because --skip-gh-release was requested."
  exit 0
fi

if ! command -v gh >/dev/null 2>&1; then
  warn "gh is unavailable, so the release tag was pushed without creating a GitHub release object."
  exit 0
fi

if [ "${REPO_MAINTENANCE_DRY_RUN:-false}" = "true" ]; then
  prerelease_flag="$(github_release_create_prerelease_flag "$RELEASE_TAG")"
  log "Would create a GitHub release for $RELEASE_TAG with gh release create --verify-tag${prerelease_flag:+ $prerelease_flag}."
  exit 0
fi

if gh release view "$RELEASE_TAG" >/dev/null 2>&1; then
  verify_github_release_prerelease_metadata "$RELEASE_TAG"
  log "GitHub release $RELEASE_TAG already exists."
  exit 0
fi

prerelease_flag="$(github_release_create_prerelease_flag "$RELEASE_TAG")"
create_github_release_from_notes_or_generated "$RELEASE_TAG" "$prerelease_flag"
log "Created GitHub release $RELEASE_TAG."
github_release_is_visible "$RELEASE_TAG" || die "GitHub release $RELEASE_TAG is not readable in this immediate re-read. Do not poll; schedule a host-native continuation for at least five minutes, then re-run the release step."
verify_github_release_prerelease_metadata "$RELEASE_TAG"
