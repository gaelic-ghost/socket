#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="$ROOT_DIR/shared/agents-snippets/apple-swift-core.md"

TARGETS=(
  "$ROOT_DIR/skills/apple-dash-docsets/references/snippets/apple-swift-core.md"
  "$ROOT_DIR/skills/apple-swift-package-bootstrap/references/snippets/apple-swift-core.md"
  "$ROOT_DIR/skills/apple-xcode-workflow/references/snippets/apple-swift-core.md"
)

[[ -f "$SOURCE" ]] || {
  echo "Missing source snippet: $SOURCE" >&2
  exit 1
}

for target in "${TARGETS[@]}"; do
  target_dir="$(dirname "$target")"
  [[ -d "$target_dir" ]] || {
    echo "Missing target directory: $target_dir" >&2
    exit 1
  }

  cp "$SOURCE" "$target"
done

echo "Synchronized apple-swift-core snippet to ${#TARGETS[@]} skill-local copies."
