#!/usr/bin/env sh

set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export REPO_MAINTENANCE_COMMON_DIR="$SELF_DIR/../lib"
. "$REPO_MAINTENANCE_COMMON_DIR/common.sh"

run_component_validation() {
  component_root=$1
  component_kind=$2
  candidate="$component_root/scripts/repo-maintenance/validate-all.sh"
  if [ -f "$candidate" ]; then
    log "Validating $component_kind component at $component_root with ${candidate#"$component_root/"}."
    sh "$candidate"
    return 0
  fi
  log "No component-owned repo-maintenance validation found for $component_kind at $component_root; skipping."
}

find "$REPO_ROOT/Apps" -type f \( -name 'target.yml' -o -name 'target.yaml' \) -print | sort | while IFS= read -r spec; do
  run_component_validation "$(dirname -- "$spec")" "app-target"
done

find "$REPO_ROOT/Packages" -type f -name 'Package.swift' -print | sort | while IFS= read -r manifest; do
  run_component_validation "$(dirname -- "$manifest")" "package"
done

if [ -d "$REPO_ROOT/Services" ]; then
  find "$REPO_ROOT/Services" -mindepth 1 -maxdepth 1 -type d -print | sort | while IFS= read -r service; do
    run_component_validation "$service" "service"
  done
fi
