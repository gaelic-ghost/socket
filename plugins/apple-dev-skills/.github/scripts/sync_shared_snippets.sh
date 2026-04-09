#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

sync_one() {
  local source="$1"
  shift
  local targets=("$@")

  [[ -f "$source" ]] || {
    echo "Missing source snippet: $source" >&2
    exit 1
  }

  for target in "${targets[@]}"; do
    local target_dir
    target_dir="$(dirname "$target")"
    [[ -d "$target_dir" ]] || {
      echo "Missing target directory: $target_dir" >&2
      exit 1
    }
    cp "$source" "$target"
  done
}

sync_one \
  "$ROOT_DIR/shared/agents-snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/xcode-build-run-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/xcode-testing-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/xcode-app-project-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/bootstrap-xcode-app-project/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/explore-apple-swift-docs/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/sync-xcode-project-guidance/references/snippets/apple-xcode-project-core.md"

sync_one \
  "$ROOT_DIR/shared/agents-snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/swift-package-build-run-workflow/references/snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/swift-package-testing-workflow/references/snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/bootstrap-swift-package/references/snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/sync-swift-package-guidance/references/snippets/apple-swift-package-core.md"

echo "Synchronized shared snippet set to skill-local copies."
