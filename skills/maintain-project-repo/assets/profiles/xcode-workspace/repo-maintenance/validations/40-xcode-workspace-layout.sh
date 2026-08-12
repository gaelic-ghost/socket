#!/usr/bin/env sh

set -eu

SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export REPO_MAINTENANCE_COMMON_DIR="$SELF_DIR/../lib"
. "$SELF_DIR/../lib/common.sh"

require_exactly_one_workspace() {
  workspace_count=$(find "$REPO_ROOT" -maxdepth 1 -type d -name '*.xcworkspace' -print | wc -l | tr -d ' ')
  [ "$workspace_count" -eq 1 ] || die "The xcode-workspace profile requires exactly one root .xcworkspace; found $workspace_count."
}

require_apps_and_packages() {
  [ -d "$REPO_ROOT/Apps" ] || die "The xcode-workspace profile requires Apps/ at the repository root."
  [ -d "$REPO_ROOT/Packages" ] || die "The xcode-workspace profile requires Packages/ at the repository root."

  app_count=$(find "$REPO_ROOT/Apps" -type d -name '*.xcodeproj' -print | wc -l | tr -d ' ')
  [ "$app_count" -gt 0 ] || die "The xcode-workspace profile requires at least one .xcodeproj under Apps/."

  package_count=$(find "$REPO_ROOT/Packages" -type f -name 'Package.swift' -print | wc -l | tr -d ' ')
  [ "$package_count" -gt 0 ] || die "The xcode-workspace profile requires at least one Package.swift under Packages/."
}

require_exactly_one_workspace
require_apps_and_packages
log "Validated xcode-workspace composition: one root workspace, Apps/, and Packages/."
