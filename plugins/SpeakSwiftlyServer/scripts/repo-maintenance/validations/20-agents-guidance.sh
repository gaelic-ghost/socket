#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export REPO_MAINTENANCE_COMMON_DIR="$SELF_DIR/../lib"
. "$SELF_DIR/../lib/common.sh"

if [ "${REPO_MAINTENANCE_REQUIRE_AGENTS:-true}" != "true" ]; then
  log "Skipping AGENTS.md validation because REPO_MAINTENANCE_REQUIRE_AGENTS is disabled."
  exit 0
fi

agents_path="$REPO_ROOT/AGENTS.md"
[ -f "$agents_path" ] || die "Expected $agents_path to exist so maintain-project-repo has repo guidance to complement."
[ -s "$agents_path" ] || die "Expected $agents_path to be non-empty."

for needle in \
  "scripts/repo-maintenance/validate-all.sh" \
  "scripts/repo-maintenance/sync-shared.sh" \
  "scripts/repo-maintenance/release.sh"
do
  grep -F "$needle" "$agents_path" >/dev/null 2>&1 || die "Expected $agents_path to mention $needle so the maintainer validation, sync, and release entrypoints stay discoverable."
done
