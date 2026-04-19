#!/usr/bin/env sh
set -eu

COMMON_CONTEXT_DIR=${SELF_DIR:-}
[ -n "$COMMON_CONTEXT_DIR" ] || COMMON_CONTEXT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ -f "$COMMON_CONTEXT_DIR/lib/common.sh" ]; then
  REPO_MAINTENANCE_ROOT="$COMMON_CONTEXT_DIR"
else
  REPO_MAINTENANCE_ROOT=$(CDPATH= cd -- "$COMMON_CONTEXT_DIR/.." && pwd)
fi
REPO_ROOT=$(CDPATH= cd -- "$REPO_MAINTENANCE_ROOT/../.." && pwd)
REPO_MAINTENANCE_PROFILE="generic"
REPO_MAINTENANCE_PROFILE_DESCRIPTION="Generic repo-maintenance baseline with no Swift or Xcode specialization."

log() {
  printf '%s\n' "$*"
}

warn() {
  printf 'WARN: %s\n' "$*" >&2
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

load_env_file() {
  env_file="$1"
  [ -f "$env_file" ] || return 0
  set -a
  # shellcheck disable=SC1090
  . "$env_file"
  set +a
}

load_profile_env() {
  load_env_file "$REPO_MAINTENANCE_ROOT/config/profile.env"
}

ensure_git_repo() {
  git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "The repo-maintenance toolkit must run inside a git worktree rooted at $REPO_ROOT."
}

run_dispatch_dir() {
  dir="$1"
  label="$2"
  ran_any="false"

  for script in "$dir"/*.sh; do
    [ -e "$script" ] || continue
    ran_any="true"
    log "Running $label step $(basename "$script")"
    sh "$script"
  done

  if [ "$ran_any" = "false" ]; then
    log "No $label steps are currently defined under $dir."
  fi
}
