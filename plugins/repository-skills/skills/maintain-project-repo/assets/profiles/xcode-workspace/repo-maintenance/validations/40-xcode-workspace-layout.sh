#!/usr/bin/env sh

set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export REPO_MAINTENANCE_COMMON_DIR="$SELF_DIR/../lib"
. "$SELF_DIR/../lib/common.sh"

require_exactly_one_workspace() {
  workspace_count=$(find "$REPO_ROOT" -maxdepth 1 -type d -name '*.xcworkspace' -print | wc -l | tr -d ' ')
  [ "$workspace_count" -eq 1 ] || die "The xcode-workspace profile requires exactly one root .xcworkspace; found $workspace_count."
}

require_component_roots() {
  [ -d "$REPO_ROOT/Apps" ] || die "The xcode-workspace profile requires Apps/ at the repository root."
  [ -d "$REPO_ROOT/Packages" ] || die "The xcode-workspace profile requires Packages/ at the repository root."
  [ -d "$REPO_ROOT/Services" ] || die "The xcode-workspace profile requires Services/ at the repository root."

  [ -f "$REPO_ROOT/project.yml" ] || die "The xcode-workspace profile requires root project.yml."
  project_count=$(find "$REPO_ROOT" -maxdepth 1 -type d -name '*.xcodeproj' -print | wc -l | tr -d ' ')
  [ "$project_count" -eq 1 ] || die "The xcode-workspace profile requires exactly one generated root .xcodeproj; found $project_count."

  component_count=$(find "$REPO_ROOT/Apps" -type f \( -name 'target.yml' -o -name 'target.yaml' \) -print; find "$REPO_ROOT/Packages" "$REPO_ROOT/Services" -type f -name 'Package.swift' -print)
  [ -n "$component_count" ] || die "The xcode-workspace profile requires at least one component under Apps/, Packages/, or Services/."
}

require_exactly_one_workspace
require_component_roots
log "Validated xcode-workspace composition: one root workspace and project with Apps/, Packages/, and Services/ component roots."
