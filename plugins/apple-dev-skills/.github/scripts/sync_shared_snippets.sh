#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODE="${1:-sync}"

if [[ "$MODE" != "sync" && "$MODE" != "--check" && "$MODE" != "check" ]]; then
  echo "Usage: $0 [--check|check]" >&2
  exit 2
fi

check_mode=false
if [[ "$MODE" == "--check" || "$MODE" == "check" ]]; then
  check_mode=true
fi

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
    if "$check_mode"; then
      [[ -f "$target" ]] || {
        echo "Missing target snippet: $target" >&2
        exit 1
      }
      cmp -s "$source" "$target" || {
        echo "Snippet drift detected between $source and $target" >&2
        exit 1
      }
    else
      cp "$source" "$target"
    fi
  done
}

sync_one \
  "$ROOT_DIR/shared/agents-snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/apple-ui-accessibility-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/xcode-build-run-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/xcode-testing-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/xcode-app-project-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/bootstrap-xcode-app-project/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/format-swift-sources/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/explore-apple-swift-docs/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/safari-extension-control-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/devicecheck-app-attest-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/swiftui-app-architecture-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/appkit-app-architecture-workflow/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/sync-xcode-project-guidance/references/snippets/apple-xcode-project-core.md" \
  "$ROOT_DIR/skills/xcode-coding-intelligence-workflow/references/snippets/apple-xcode-project-core.md"

sync_one \
  "$ROOT_DIR/shared/agents-snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/swift-package-build-run-workflow/references/snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/swift-package-testing-workflow/references/snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/swift-package-workflow/references/snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/bootstrap-swift-package/references/snippets/apple-swift-package-core.md" \
  "$ROOT_DIR/skills/sync-swift-package-guidance/references/snippets/apple-swift-package-core.md"

if "$check_mode"; then
  echo "Shared snippet skill-local copies are in sync."
else
  echo "Synchronized shared snippet set to skill-local copies."
fi
