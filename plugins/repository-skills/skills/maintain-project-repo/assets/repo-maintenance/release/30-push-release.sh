#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export REPO_MAINTENANCE_COMMON_DIR="$SELF_DIR/../lib"
. "$SELF_DIR/../lib/common.sh"

branch_name="$(git -C "$REPO_ROOT" symbolic-ref --quiet --short HEAD)"

if [ "${REPO_MAINTENANCE_DRY_RUN:-false}" = "true" ]; then
  log "Would push branch $branch_name and tag $RELEASE_TAG to origin."
  exit 0
fi

git -C "$REPO_ROOT" push -u origin "$branch_name"
remote_branch_is_visible "$branch_name" || die "Remote branch origin/$branch_name is not visible in this immediate re-read. Do not poll; schedule a host-native continuation for at least five minutes, then re-run the release step."
git -C "$REPO_ROOT" push origin "$RELEASE_TAG"
remote_tag_is_visible "$RELEASE_TAG" || die "Remote tag $RELEASE_TAG is not visible in this immediate re-read. Do not poll; schedule a host-native continuation for at least five minutes, then re-run the release step."
log "Pushed branch $branch_name and tag $RELEASE_TAG."
