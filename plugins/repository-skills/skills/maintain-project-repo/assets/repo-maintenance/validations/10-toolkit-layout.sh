#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export REPO_MAINTENANCE_COMMON_DIR="$SELF_DIR/../lib"
. "$SELF_DIR/../lib/common.sh"

for required in \
  "$REPO_MAINTENANCE_ROOT/validate-all.sh" \
  "$REPO_MAINTENANCE_ROOT/sync-shared.sh" \
  "$REPO_MAINTENANCE_ROOT/release.sh" \
  "$REPO_MAINTENANCE_ROOT/lib/common.sh" \
  "$REPO_MAINTENANCE_ROOT/config/profile.env"
do
  [ -f "$required" ] || die "maintain-project-repo is missing the required file $required."
done
