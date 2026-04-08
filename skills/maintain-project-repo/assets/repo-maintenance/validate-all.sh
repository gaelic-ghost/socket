#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$SELF_DIR/lib/common.sh"

load_profile_env
load_env_file "$SELF_DIR/config/validation.env"
ensure_git_repo
log "Running repo-maintenance validation from $REPO_ROOT with the $REPO_MAINTENANCE_PROFILE profile."
run_dispatch_dir "$SELF_DIR/validations" "validation"
log "Repo-maintenance validation completed successfully."
