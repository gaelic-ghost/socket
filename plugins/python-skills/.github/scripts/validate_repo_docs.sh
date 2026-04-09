#!/usr/bin/env zsh
set -euo pipefail

cd "$(dirname "$0")/../.."
uv run scripts/validate_repo_metadata.py
