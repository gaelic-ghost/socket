#!/usr/bin/env sh
set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

exec uv run python "$SELF_DIR/release_version.py" "$@"
