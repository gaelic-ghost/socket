#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)

# Prefer repo-local uv cache for reproducible, writable Codex sessions.
if [ -z "${UV_CACHE_DIR:-}" ]; then
  UV_CACHE_DIR="$REPO_ROOT/.codex/.cache/uv"
fi
mkdir -p "$UV_CACHE_DIR"
export UV_CACHE_DIR

echo "Configured UV_CACHE_DIR=$UV_CACHE_DIR"
