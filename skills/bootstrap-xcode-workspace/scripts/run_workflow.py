#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Create one Apple product workspace with a root XcodeGen project."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SUPPORTED_PLATFORMS = {
    "ios": "iOS",
    "macos": "macOS",
    "tvos": "tvOS",
    "watchos": "watchOS",
    "visionos": "visionOS",
}
CONFIGURATIONS = ("Debug", "Staging", "Release", "AppStore", "DirectDistribution", "AltStore")
XCODE_PRODUCT_TYPES = {
    "com.apple.product-type.application": "app",
    "com.apple.product-type.app-extension": "extension",
    "com.apple.product-type.extensionkit-extension": "extension",
    "com.apple.product-type.bundle.unit-test": "test",
    "com.apple.product-type.bundle.ui-testing": "ui-test",
}


@dataclass
class Component:
    """One concrete repository component; never a whole-repository classification."""

    name: str
    kind: str
    current_owner: str
    proposed_destination: str
    evidence: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    host_target: str | None = None
    platform: str | None = None
    product_type: str | None = None
    extension_point_identifier: str | None = None
    owned_paths: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)


def write(path: Path, content: str, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)


def version_sort_key(path: Path) -> tuple[int, ...]:
    return tuple(int(part) if part.isdigit() else -1 for part in path.name.split("."))


def maintain_project_repo_runner() -> Path:
    candidates: list[Path] = []
    seen: set[Path] = set()
    for root in Path(__file__).resolve().parents:
        paths = [root / "repository-skills" / "skills" / "maintain-project-repo" / "scripts" / "run_workflow.py"]
        version_root = root / "repository-skills"
        if version_root.is_dir():
            paths.extend(
                version / "skills" / "maintain-project-repo" / "scripts" / "run_workflow.py"
                for version in sorted(version_root.iterdir(), key=version_sort_key, reverse=True)
            )
        for path in paths:
            resolved = path.resolve()
            if resolved not in seen:
                candidates.append(resolved)
                seen.add(resolved)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = "\n".join(f"- {candidate}" for candidate in candidates)
    raise RuntimeError(
        "bootstrap-xcode-workspace needs repository-skills/maintain-project-repo to install "
        f"workspace maintenance files. Searched:\n{searched}"
    )


def server_component_runner() -> Path:
    candidates: list[Path] = []
    for parent in Path(__file__).resolve().parents:
        plugin_root = parent / "server-side-swift"
        candidates.append(plugin_root / "skills" / "workspace-service-component" / "scripts" / "run_workflow.py")
        if plugin_root.is_dir():
            candidates.extend(
                version / "skills" / "workspace-service-component" / "scripts" / "run_workflow.py"
                for version in sorted(plugin_root.iterdir(), key=version_sort_key, reverse=True)
                if version.is_dir()
            )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = "\n".join(f"- {candidate}" for candidate in candidates)
    raise RuntimeError(f"Adding a service requires the server-side-swift workspace-service-component adapter from the Socket marketplace. Searched:\n{searched}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--name")
    result.add_argument("--file-prefix", default="APP")
    result.add_argument("--destination", default=".")
    result.add_argument("--platforms", default="ios,macos")
    result.add_argument("--org-identifier", default="com.galewilliams")
    result.add_argument("--development-team", default="BC73766F69")
    result.add_argument("--dry-run", action="store_true")
    result.add_argument("--skip-validation", action="store_true")
    result.add_argument("--repo-root", help="Adopt, add to, or align an existing Swift repository.")
    result.add_argument("--operation", choices=("create", "adopt", "add-component", "align"), default="create")
    result.add_argument("--component-kind", choices=("app", "extension", "library", "service"))
    result.add_argument("--component-name")
    result.add_argument("--platform", choices=tuple(SUPPORTED_PLATFORMS))
    result.add_argument("--framework", choices=("hummingbird", "vapor"))
    result.add_argument("--host-target", help="Containing application target for an extension component.")
    result.add_argument("--extension-product-type", choices=("app-extension", "extensionkit-extension"))
    result.add_argument("--extension-point-identifier", help="Documented NSExtensionPointIdentifier for an extension component.")
    result.add_argument("--adoption-map", help="Reviewed adoption-map JSON to apply after the read-only adopt inventory.")
    result.add_argument("--apply", action="store_true", help="Apply --adoption-map. Adopt is read-only without this flag.")
    return result


def blocked(message: str, inputs: dict[str, object]) -> int:
    print(json.dumps({"status": "blocked", "path_type": "primary", "normalized_inputs": inputs, "stderr": message}, indent=2, sort_keys=True))
    return 1


MANAGED_BEGIN = "<!-- socket-managed:begin"
MANAGED_END = "<!-- socket-managed:end"
JUST_BEGIN = "# socket-managed:begin just-recipes"
JUST_END = "# socket-managed:end just-recipes"


def marker_state(content: str, begin: str = MANAGED_BEGIN, end: str = MANAGED_END) -> str:
    begins, ends = content.count(begin), content.count(end)
    if begins == 0 and ends == 0:
        return "absent"
    if begins == 1 and ends == 1 and content.index(begin) < content.index(end):
        return "valid"
    return "invalid"


def workspace_findings(root: Path, allow_missing_services: bool = False) -> list[str]:
    findings: list[str] = []
    if len(list(root.glob("*.xcworkspace"))) != 1:
        findings.append("Expected exactly one root .xcworkspace.")
    if len(list(root.glob("*.xcodeproj"))) != 1:
        findings.append("Expected exactly one generated root .xcodeproj.")
    required = ["project.yml", "Apps/apps-shared.yml", "Apps/Apps-shared.xcconfig", "Packages/packages-shared.yml"]
    if not allow_missing_services:
        required.append("Services/services-shared.yml")
    findings.extend(f"Expected {path}." for path in required if not (root / path).is_file())
    components = list((root / "Apps").glob("**/target.y*ml")) + list((root / "Packages").glob("**/Package.swift")) + list((root / "Services").glob("**/Package.swift"))
    if not components:
        findings.append("Expected at least one component under Apps/, Packages/, or Services/.")
    return findings


def managed_recipe_block() -> str:
    return "\n".join((
        "# socket-managed:begin just-recipes",
        "# Socket owns this bounded setup/alignment contract. Add project recipes outside it.",
        "setup:", "  sh .socket/managed/setup.sh", "align:", "  sh .socket/managed/align.sh",
        "# socket-managed:end just-recipes", "",
    ))


def setup_script() -> str:
    return "\n".join((
        "#!/usr/bin/env sh", "set -eu",
        'for tool in git just swift xcodegen xcodebuild; do command -v "$tool" >/dev/null 2>&1 || { echo "Missing required tool: $tool" >&2; exit 1; }; done',
        "git config core.hooksPath .githooks", "",
    ))


def align_script() -> str:
    return "\n".join((
        "#!/usr/bin/env sh", "set -eu",
        "base=${SOCKET_TEMPLATE_BASE_URL:-https://raw.githubusercontent.com/gaelic-ghost/socket/main/plugins/apple-dev-skills/skills/bootstrap-xcode-workspace/assets/managed-guidance}",
        "tmp=$(mktemp -d)", "trap 'rm -r \"$tmp\"' EXIT HUP INT TERM",
        "for file in AGENTS-root.md AGENTS-apps.md AGENTS-packages.md AGENTS-services.md CONTRIBUTING.md pre-commit; do curl --fail --silent --show-error \"$base/$file\" -o \"$tmp/$file\"; done",
        "for file in AGENTS-root.md AGENTS-apps.md AGENTS-packages.md AGENTS-services.md CONTRIBUTING.md; do [ \"$(grep -c 'socket-managed:begin' \"$tmp/$file\")\" -eq 1 ] && [ \"$(grep -c 'socket-managed:end' \"$tmp/$file\")\" -eq 1 ] || { echo \"just align: remote $file has invalid managed markers; no files were changed.\" >&2; exit 1; }; done",
        "[ -s \"$tmp/pre-commit\" ] || { echo \"just align: remote pre-commit hook is empty; no files were changed.\" >&2; exit 1; }",
        "for file in AGENTS.md Apps/AGENTS.md Packages/AGENTS.md Services/AGENTS.md CONTRIBUTING.md; do [ \"$(grep -c 'socket-managed:begin' \"$file\")\" -eq 1 ] && [ \"$(grep -c 'socket-managed:end' \"$file\")\" -eq 1 ] || { echo \"just align: $file has invalid managed markers; no files were changed.\" >&2; exit 1; }; done",
        "replace() { source=$1; destination=$2; awk -v replacement=\"$source\" '/<!-- socket-managed:begin/ { while ((getline line < replacement) > 0) { print line; if (line ~ /<!-- socket-managed:end/) break }; in_managed=1; next } in_managed { if (/<!-- socket-managed:end/) in_managed=0; next } { print }' \"$destination\" > \"$tmp/out\"; mv \"$tmp/out\" \"$destination\"; }",
        "replace \"$tmp/AGENTS-root.md\" AGENTS.md", "replace \"$tmp/AGENTS-apps.md\" Apps/AGENTS.md", "replace \"$tmp/AGENTS-packages.md\" Packages/AGENTS.md", "replace \"$tmp/AGENTS-services.md\" Services/AGENTS.md", "replace \"$tmp/CONTRIBUTING.md\" CONTRIBUTING.md",
        "cp \"$tmp/pre-commit\" .githooks/pre-commit", "chmod +x .githooks/pre-commit", "git config core.hooksPath .githooks", "xcodegen generate --spec project.yml", "",
    ))


def managed_document(source: Path, existing: str | None) -> str:
    template = source.read_text(encoding="utf-8")
    if existing is None:
        return template
    state = marker_state(existing)
    if state == "invalid":
        raise RuntimeError(f"{source.name} has malformed Socket managed markers.")
    return existing + ("" if existing.endswith("\n") else "\n") + "\n" + template if state == "absent" else existing


def install_alignment_runtime(root: Path, dry_run: bool = False) -> list[str]:
    assets = Path(__file__).resolve().parents[1] / "assets" / "managed-guidance"
    docs = (("AGENTS-root.md", root / "AGENTS.md"), ("AGENTS-apps.md", root / "Apps/AGENTS.md"), ("AGENTS-packages.md", root / "Packages/AGENTS.md"), ("AGENTS-services.md", root / "Services/AGENTS.md"), ("CONTRIBUTING.md", root / "CONTRIBUTING.md"))
    planned: dict[Path, tuple[str, bool]] = {}
    for source_name, destination in docs:
        if destination.exists() and not destination.is_file():
            raise RuntimeError(f"{destination.relative_to(root)} exists but is not a regular file.")
        existing = destination.read_text(encoding="utf-8") if destination.exists() else None
        planned[destination] = (managed_document(assets / source_name, existing), False)
    justfile = root / "Justfile"
    if justfile.exists() and not justfile.is_file():
        raise RuntimeError("Justfile exists but is not a regular file.")
    existing = justfile.read_text(encoding="utf-8") if justfile.exists() else 'set shell := ["sh", "-eu", "-c"]\n'
    state = marker_state(existing, JUST_BEGIN, JUST_END)
    if state == "invalid":
        raise RuntimeError("Justfile has malformed Socket managed recipe markers.")
    planned[justfile] = ((existing.rstrip() + "\n\n" + managed_recipe_block()) if state == "absent" else existing, False)
    for path, content in ((root / ".socket/managed/setup.sh", setup_script()), (root / ".socket/managed/align.sh", align_script())):
        if path.exists() and path.read_text(encoding="utf-8") != content:
            raise RuntimeError(f"{path.relative_to(root)} conflicts with the Socket-managed alignment helper.")
        planned[path] = (content, True)
    hook = root / ".githooks/pre-commit"
    if hook.exists() and not hook.is_file():
        raise RuntimeError(".githooks/pre-commit exists but is not a regular file.")
    planned[hook] = ((assets / "pre-commit").read_text(encoding="utf-8"), True)
    if not dry_run:
        for destination, (content, executable) in planned.items():
            write(destination, content, executable)
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=root, check=False)
    return [f"install Socket-managed alignment surface at {path.relative_to(root)}" for path in planned]


def root_spec(name: str, platforms: list[str]) -> str:
    includes = ["  - path: Apps/apps-shared.yml\n    relativePaths: false", "  - path: Packages/packages-shared.yml\n    relativePaths: false", "  - path: Services/services-shared.yml\n    relativePaths: false"]
    includes.extend(f"  - path: Apps/{name}{SUPPORTED_PLATFORMS[platform]}/target.yml\n    relativePaths: false" for platform in platforms)
    return "\n".join([
        f"name: {name}", "include:", *includes, "options:",
        "  minimumXcodeGenVersion: 2.46.0", "  projectFormat: xcode16_3", "  defaultConfig: Debug",
        "  defaultSourceDirectoryType: syncedFolder", "  schemePathPrefix: ../", "  localPackagesGroup: Packages",
        "  deploymentTarget:", "    iOS: \"26.1\"", "    macOS: \"26.1\"", "    tvOS: \"26.1\"", "    watchOS: \"26.1\"", "    visionOS: \"26.1\"",
        "configs:", *(f"  {config}: {'debug' if config == 'Debug' else 'release'}" for config in CONFIGURATIONS), "configFiles:",
        *(f"  {config}: Configurations/{config}.xcconfig" for config in CONFIGURATIONS),
        "fileGroups:", "  - Apps", "  - Packages", "  - Services", "  - Configurations", "  - Scripts", "  - docs", "",
    ])


def app_shared_spec() -> str:
    return """targetTemplates:
  SwiftUIApp:
    type: application
    settings:
      base:
        GENERATE_INFOPLIST_FILE: NO
        ASSETCATALOG_COMPILER_APPICON_NAME: AppIcon
    preBuildScripts:
      - name: SwiftFormat and SwiftLint
        script: |
          if command -v swiftformat >/dev/null 2>&1; then
            swiftformat --lint --config "${SRCROOT}/.swiftformat" "${SRCROOT}/Apps/${TARGET_NAME}"
          else
            echo "warning: SwiftFormat is not installed; skipping lint."
          fi
          if command -v swiftlint >/dev/null 2>&1; then
            swiftlint lint --config "${SRCROOT}/.swiftlint.yml" --force-exclude "${SRCROOT}/Apps/${TARGET_NAME}"
          else
            echo "warning: SwiftLint is not installed; skipping lint."
          fi
  SwiftTesting:
    type: bundle.unit-test
    settings:
      base:
        GENERATE_INFOPLIST_FILE: YES
    preBuildScripts:
      - name: SwiftFormat and SwiftLint
        script: |
          if command -v swiftformat >/dev/null 2>&1; then swiftformat --lint --config "${SRCROOT}/.swiftformat" "${SRCROOT}/Apps/${TARGET_NAME}"; else echo "warning: SwiftFormat is not installed; skipping lint."; fi
          if command -v swiftlint >/dev/null 2>&1; then swiftlint lint --config "${SRCROOT}/.swiftlint.yml" --force-exclude "${SRCROOT}/Apps/${TARGET_NAME}"; else echo "warning: SwiftLint is not installed; skipping lint."; fi
  SwiftUIAutomation:
    type: bundle.ui-testing
    settings:
      base:
        GENERATE_INFOPLIST_FILE: YES
    preBuildScripts:
      - name: SwiftFormat and SwiftLint
        script: |
          if command -v swiftformat >/dev/null 2>&1; then swiftformat --lint --config "${SRCROOT}/.swiftformat" "${SRCROOT}/Apps/${TARGET_NAME}"; else echo "warning: SwiftFormat is not installed; skipping lint."; fi
          if command -v swiftlint >/dev/null 2>&1; then swiftlint lint --config "${SRCROOT}/.swiftlint.yml" --force-exclude "${SRCROOT}/Apps/${TARGET_NAME}"; else echo "warning: SwiftLint is not installed; skipping lint."; fi
schemeTemplates:
  AppScheme:
    run: { config: Debug }
    test:
      config: Debug
      gatherCoverageData: true
    archive: { config: Staging }
    management: { shared: true }
"""


def package_spec(name: str) -> str:
    return f"""packages:
  {name}Core:
    path: Packages/{name}Core
"""


def target_spec(name: str, platform: str, prefix: str, org: str, team: str, core_package: str | None = None) -> str:
    display = SUPPORTED_PLATFORMS[platform]
    target = f"{name}{display}"
    suffix = {"ios": "ios", "macos": "mac", "tvos": "tv", "watchos": "watch", "visionos": "vision"}[platform]
    spec = f"""targets:
  {target}:
    templates: [SwiftUIApp]
    platform: {display}
    sources:
      - path: Apps/{target}/Sources
        type: syncedFolder
      - path: Apps/{target}/Resources
        type: syncedFolder
    info:
      path: Apps/{target}/Resources/Info.plist
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: {org}.{name.lower()}.{suffix}
        DEVELOPMENT_TEAM: {team}
        CODE_SIGN_STYLE: Automatic
        CODE_SIGN_ENTITLEMENTS: Apps/{target}/Resources/{target}.entitlements
        SWIFT_DEFAULT_ACTOR_ISOLATION: MainActor
    configFiles:
      Debug: Apps/{target}/Configurations/Debug.xcconfig
      Staging: Apps/{target}/Configurations/Staging.xcconfig
      Release: Apps/{target}/Configurations/Release.xcconfig
      AppStore: Apps/{target}/Configurations/AppStore.xcconfig
      DirectDistribution: Apps/{target}/Configurations/DirectDistribution.xcconfig
      AltStore: Apps/{target}/Configurations/AltStore.xcconfig
    dependencies:
      - package: {core_package or name + 'Core'}
  {target}Tests:
    templates: [SwiftTesting]
    platform: {display}
    sources:
      - path: Apps/{target}Tests/Sources
        type: syncedFolder
    dependencies:
      - target: {target}
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: {org}.{name.lower()}.{suffix}.tests
        DEVELOPMENT_TEAM: {team}
        SWIFT_DEFAULT_ACTOR_ISOLATION: MainActor
schemes:
  {target}:
    templates: [AppScheme]
    preActions:
      - name: Increment build number
        script: 'sh "${{SRCROOT}}/Scripts/increment-build-version.sh" "${{TARGET_NAME}}" "${{CONFIGURATION}}"'
        settingsTarget: {target}
    build:
      targets:
        {target}: all
    test:
      targets:
        - name: {target}Tests
          parallelizable: true
"""
    if platform != "watchos":
        spec = spec.replace("schemes:\n", f"""  {target}UITests:
    templates: [SwiftUIAutomation]
    platform: {display}
    sources:
      - path: Apps/{target}UITests/Sources
        type: syncedFolder
    dependencies:
      - target: {target}
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: {org}.{name.lower()}.{suffix}.uitests
        DEVELOPMENT_TEAM: {team}
        SWIFT_DEFAULT_ACTOR_ISOLATION: MainActor
schemes:
  {target} UI Tests:
    preActions:
      - name: Increment build number
        script: 'sh "${{SRCROOT}}/Scripts/increment-build-version.sh" "${{TARGET_NAME}}" "${{CONFIGURATION}}"'
        settingsTarget: {target}
    build:
      targets: {{ {target}: all }}
    test:
      config: Debug
      targets:
        - name: {target}UITests
          parallelizable: true
""")
    channels = [("Staging", "Staging"), ("App Store", "AppStore")]
    if platform in {"ios", "visionos"}:
        channels.append(("AltStore", "AltStore"))
    if platform == "macos":
        channels.append(("Direct Distribution", "DirectDistribution"))
    for title, config in channels:
        spec += f"""  {target} {title}:
    preActions:
      - name: Increment build number
        script: 'sh "${{SRCROOT}}/Scripts/increment-build-version.sh" "${{TARGET_NAME}}" "${{CONFIGURATION}}"'
        settingsTarget: {target}
    build:
      targets: {{ {target}: all }}
    archive: {{ config: {config} }}
"""
    spec += f"""  {target} Unit Tests:
    preActions:
      - name: Increment build number
        script: 'sh "${{SRCROOT}}/Scripts/increment-build-version.sh" "${{TARGET_NAME}}" "${{CONFIGURATION}}"'
        settingsTarget: {target}
    build:
      targets: {{ {target}: all }}
    test:
      config: Debug
      targets:
        - name: {target}Tests
          parallelizable: true
  {target} All Tests:
    preActions:
      - name: Increment build number
        script: 'sh "${{SRCROOT}}/Scripts/increment-build-version.sh" "${{TARGET_NAME}}" "${{CONFIGURATION}}"'
        settingsTarget: {target}
    build:
      targets: {{ {target}: all }}
    test:
      config: Debug
      targets:
        - name: {target}Tests
          parallelizable: true
"""
    if platform != "watchos":
        spec += f"""        - name: {target}UITests
          parallelizable: true
"""
    return spec


def workspace_name(root: Path) -> str:
    match = re.search(r"^name:\s*([A-Za-z][A-Za-z0-9]*)\s*$", (root / "project.yml").read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise RuntimeError("project.yml does not declare a canonical alphanumeric workspace name.")
    return match.group(1)


def add_root_include(root: Path, relative_path: str) -> None:
    project = root / "project.yml"
    content = project.read_text(encoding="utf-8")
    if f"path: {relative_path}" in content:
        return
    anchor = "options:\n"
    if anchor not in content:
        raise RuntimeError("project.yml is missing the options section used as the managed include boundary.")
    include = f"  - path: {relative_path}\n    relativePaths: false\n"
    write(project, content.replace(anchor, include + anchor, 1))


def ensure_services_surface(root: Path, dry_run: bool = False) -> list[str]:
    actions: list[str] = []
    shared = root / "Services/services-shared.yml"
    if not shared.is_file():
        actions.append("create Services/services-shared.yml")
        if not dry_run:
            write(shared, "packages: {}\n")
    project = (root / "project.yml").read_text(encoding="utf-8")
    if "path: Services/services-shared.yml" not in project:
        actions.append("register Services/services-shared.yml in project.yml")
        if not dry_run:
            add_root_include(root, "Services/services-shared.yml")
    return actions


def add_package_mapping(root: Path, group: str, name: str) -> None:
    shared = root / group / f"{group.lower()}-shared.yml"
    content = shared.read_text(encoding="utf-8")
    entry = f"  {name}:\n    path: {group}/{name}\n"
    if f"  {name}:\n" in content:
        return
    if content.strip() == "packages: {}":
        content = "packages:\n"
    elif not content.endswith("\n"):
        content += "\n"
    write(shared, content + entry)


def create_library_component(root: Path, name: str) -> None:
    component = root / "Packages" / name
    if component.exists():
        raise RuntimeError(f"Packages/{name} already exists.")
    component.mkdir(parents=True)
    subprocess.run(["swift", "package", "init", "--type", "library", "--name", name, "--enable-swift-testing"], cwd=component, check=True, capture_output=True, text=True)
    add_package_mapping(root, "Packages", name)


def create_app_component(root: Path, product_name: str, component_name: str, platform: str, prefix: str, org: str, team: str) -> None:
    display = SUPPORTED_PLATFORMS[platform]
    target = f"{component_name}{display}"
    app_root = root / "Apps" / target
    if app_root.exists():
        raise RuntimeError(f"Apps/{target} already exists.")
    add_root_include(root, f"Apps/{target}/target.yml")
    write(app_root / "target.yml", target_spec(component_name, platform, prefix, org, team, f"{product_name}Core"))
    write(app_root / "Configurations/App.xcconfig", '#include "../../Apps-shared.xcconfig"\nMARKETING_VERSION = 0.0.1\nCODE_SIGN_STYLE = Automatic\n')
    write(app_root / "Configurations/Version.xcconfig", "DEBUG_BUILD_NUMBER = 1\nRELEASE_BUILD_NUMBER = 1\n")
    for config in CONFIGURATIONS:
        build_number = "$(DEBUG_BUILD_NUMBER)" if config == "Debug" else "$(RELEASE_BUILD_NUMBER)"
        content = '#include "App.xcconfig"\n#include "Version.xcconfig"\nCURRENT_PROJECT_VERSION = ' + build_number + "\n"
        if config == "Debug":
            content += "ONLY_ACTIVE_ARCH = YES\n"
        else:
            content += "SWIFT_OPTIMIZATION_LEVEL = -O\n"
        write(app_root / f"Configurations/{config}.xcconfig", content)
    write(app_root / f"Sources/{prefix}App.swift", f'import SwiftUI\n\n@main\nstruct {prefix}{display}App: App {{\n    var body: some Scene {{ WindowGroup {{ Text("{target}") }} }}\n}}\n')
    for folder in ("Views", "Datamodels", "Services"):
        write(app_root / f"Sources/{folder}/.gitkeep", "")
    write(app_root / "Resources/Info.plist", '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>CFBundleShortVersionString</key><string>$(MARKETING_VERSION)</string><key>CFBundleVersion</key><string>$(CURRENT_PROJECT_VERSION)</string></dict></plist>\n')
    write(app_root / f"Resources/{target}.entitlements", '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict/></plist>\n')
    write(app_root / "Resources/Assets.xcassets/Contents.json", '{"info":{"author":"xcode","version":1}}\n')
    write(app_root / "Resources/Assets.xcassets/AppIcon.appiconset/Contents.json", '{"images":[],"info":{"author":"xcode","version":1}}\n')
    write(app_root / "Resources/Assets.xcassets/AccentColor.colorset/Contents.json", '{"colors":[],"info":{"author":"xcode","version":1}}\n')
    write(app_root / "Resources/Localizable.xcstrings", '{"sourceLanguage":"en","strings":{},"version":"1.0"}\n')
    tests_root = root / "Apps" / f"{target}Tests"
    write(tests_root / f"Sources/{target}Tests.swift", f'import Testing\n@testable import {target}\n\n@Test func example() {{ #expect(true) }}\n')
    if platform != "watchos":
        ui_root = root / "Apps" / f"{target}UITests"
        write(ui_root / f"Sources/{target}UITests.swift", f'import XCTest\n\nfinal class {target}UITests: XCTestCase {{\n    func testLaunch() {{}}\n}}\n')


def find_target_spec(root: Path, target_name: str) -> Path | None:
    declaration = re.compile(rf"^  {re.escape(target_name)}:\s*$", re.MULTILINE)
    for path in sorted((root / "Apps").glob("*/target.y*ml")):
        if declaration.search(path.read_text(encoding="utf-8")):
            return path
    return None


def embed_extension_in_host(root: Path, host_target: str, extension_target: str) -> None:
    spec = find_target_spec(root, host_target)
    if spec is None:
        raise RuntimeError(f"Host application target {host_target!r} was not found under Apps/.")
    content = spec.read_text(encoding="utf-8")
    if f"- target: {extension_target}" in content:
        return
    lines = content.splitlines()
    target_start = next((index for index, line in enumerate(lines) if line == f"  {host_target}:"), None)
    if target_start is None:
        raise RuntimeError(f"Could not locate the {host_target!r} target declaration in {spec.relative_to(root)}.")
    target_end = next((index for index in range(target_start + 1, len(lines)) if re.match(r"^  \S.*:\s*$", lines[index])), len(lines))
    dependencies = next((index for index in range(target_start + 1, target_end) if lines[index] == "    dependencies:"), None)
    entry = [f"      - target: {extension_target}", "        embed: true"]
    if dependencies is None:
        lines[target_end:target_end] = ["    dependencies:", *entry]
    else:
        dependency_end = next((index for index in range(dependencies + 1, target_end) if re.match(r"^    \S.*:\s*$", lines[index])), target_end)
        lines[dependency_end:dependency_end] = entry
    write(spec, "\n".join(lines) + "\n")


def extension_target_spec(
    name: str,
    platform: str,
    org: str,
    team: str,
    product_type: str,
) -> str:
    display = SUPPORTED_PLATFORMS[platform]
    xcodegen_type = "app-extension" if product_type == "app-extension" else "extensionkit-extension"
    return f"""targets:
  {name}:
    type: {xcodegen_type}
    platform: {display}
    sources:
      - path: Apps/{name}/Sources
        type: syncedFolder
      - path: Apps/{name}/Resources
        type: syncedFolder
    info:
      path: Apps/{name}/Resources/Info.plist
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: {org}.{name.lower()}
        DEVELOPMENT_TEAM: {team}
        CODE_SIGN_STYLE: Automatic
        CODE_SIGN_ENTITLEMENTS: Apps/{name}/Resources/{name}.entitlements
    configFiles:
      Debug: Apps/{name}/Configurations/Debug.xcconfig
      Staging: Apps/{name}/Configurations/Staging.xcconfig
      Release: Apps/{name}/Configurations/Release.xcconfig
      AppStore: Apps/{name}/Configurations/AppStore.xcconfig
      DirectDistribution: Apps/{name}/Configurations/DirectDistribution.xcconfig
      AltStore: Apps/{name}/Configurations/AltStore.xcconfig
"""


def create_extension_component(
    root: Path,
    name: str,
    platform: str,
    host_target: str,
    product_type: str,
    extension_point_identifier: str,
    org: str,
    team: str,
) -> None:
    extension_root = root / "Apps" / name
    if extension_root.exists():
        raise RuntimeError(f"Apps/{name} already exists.")
    add_root_include(root, f"Apps/{name}/target.yml")
    write(extension_root / "target.yml", extension_target_spec(name, platform, org, team, product_type))
    write(extension_root / "Configurations/Extension.xcconfig", '#include "../../Apps-shared.xcconfig"\nMARKETING_VERSION = 0.0.1\nCODE_SIGN_STYLE = Automatic\n')
    for config in CONFIGURATIONS:
        write(extension_root / f"Configurations/{config}.xcconfig", '#include "Extension.xcconfig"\n')
    write(extension_root / "Sources/Extension.swift", "import Foundation\n\n// Implement the documented extension-point entry type here.\n")
    write(
        extension_root / "Resources/Info.plist",
        '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>NSExtension</key><dict><key>NSExtensionPointIdentifier</key><string>'
        + extension_point_identifier
        + "</string></dict></dict></plist>\n",
    )
    write(extension_root / f"Resources/{name}.entitlements", '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict/></plist>\n')
    embed_extension_in_host(root, host_target, name)


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def pbx_target_records(text: str) -> list[tuple[str, str | None]]:
    records: list[tuple[str, str | None]] = []
    for match in re.finditer(r"isa = PBXNativeTarget;(?P<body>[\s\S]{0,1800}?)\s*};", text):
        body = match.group("body")
        name_match = re.search(r"\bname = (?P<name>[^;]+);", body)
        product_match = re.search(r"\bproductType = (?P<type>[^;]+);", body)
        if name_match:
            records.append((name_match.group("name").strip().strip('"'), product_match.group("type").strip().strip('"') if product_match else None))
    return records


def pbx_extension_hosts(text: str, app_names: list[str], extension_names: list[str]) -> dict[str, str]:
    hosts: dict[str, str] = {}
    for extension in extension_names:
        if re.search(rf"\b{re.escape(extension)}\.appex in Embed App Extensions\b", text) and len(app_names) == 1:
            hosts[extension] = app_names[0]
    return hosts


def xcodegen_target_records(text: str) -> list[tuple[str, str | None, str | None, str | None]]:
    records: list[tuple[str, str | None, str | None, str | None]] = []
    targets_match = re.search(r"^targets:\s*$", text, re.MULTILINE)
    if not targets_match:
        return records
    tail = text[targets_match.end():]
    section_end = re.search(r"^\S[^:]*:\s*$", tail, re.MULTILINE)
    section = tail[:section_end.start()] if section_end else tail
    matches = list(re.finditer(r"^  (?P<name>[^\s][^:]*):\s*$", section, re.MULTILINE))
    for index, match in enumerate(matches):
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        body = section[match.end():body_end]
        type_match = re.search(r"^    type:\s*([^\s#]+)", body, re.MULTILINE)
        platform_match = re.search(r"^    platform:\s*([^\s#]+)", body, re.MULTILINE)
        dependency_match = re.search(r"^      - target:\s*([^\s#]+)[\s\S]{0,120}?^        embed:\s*true", body, re.MULTILINE)
        records.append((match.group("name").strip().strip('"'), type_match.group(1) if type_match else None, platform_match.group(1).lower() if platform_match else None, dependency_match.group(1) if dependency_match else None))
    return records


def manifest_component(manifest: Path, root: Path) -> Component:
    text = read_text(manifest)
    name_match = re.search(r"Package\s*\(\s*name:\s*\"([^\"]+)\"", text)
    name = name_match.group(1) if name_match else manifest.parent.name
    executable = bool(re.search(r"\.(?:executable|executableTarget)\s*\(", text))
    framework = "hummingbird" if re.search(r"Hummingbird", text, re.IGNORECASE) else "vapor" if re.search(r"\bVapor\b", text) else None
    kind = "service" if executable else "library"
    destination = f"{'Services' if kind == 'service' else 'Packages'}/{name}"
    owner = relative(manifest.parent, root) or "."
    paths = [owner] if owner != "." else [relative(manifest, root)]
    if owner == ".":
        for child in ("Sources", "Tests", "Plugins"):
            candidate = manifest.parent / child
            if candidate.exists():
                paths.append(relative(candidate, root))
    evidence = [f"SwiftPM manifest {relative(manifest, root)}", "executable product or target" if executable else "library package"]
    if framework:
        evidence.append(f"{framework} dependency")
    unresolved = [] if name_match else ["Package.swift does not expose a literal package name"]
    return Component(name, kind, owner, destination, evidence, product_type=framework, owned_paths=paths, unresolved=unresolved)


def inventory_components(root: Path) -> tuple[list[Component], dict[str, Any]]:
    projects = sorted(path for path in root.rglob("*.xcodeproj") if ".build" not in path.parts)
    workspaces = sorted(path for path in root.rglob("*.xcworkspace") if ".build" not in path.parts)
    specs = sorted(path for path in root.rglob("project.y*ml") if ".build" not in path.parts)
    manifests = sorted(path for path in root.rglob("Package.swift") if ".build" not in path.parts)
    components = [manifest_component(path, root) for path in manifests]
    pbx_settings: set[str] = set()
    target_records: list[tuple[str, str | None]] = []
    pbx_texts: list[str] = []
    for project in projects:
        text = read_text(project / "project.pbxproj")
        pbx_texts.append(text)
        target_records.extend(pbx_target_records(text))
        pbx_settings.update(re.findall(r"\b(?:PRODUCT_BUNDLE_IDENTIFIER|CODE_SIGN_ENTITLEMENTS|DEVELOPMENT_TEAM|INFOPLIST_FILE|MARKETING_VERSION|CURRENT_PROJECT_VERSION|SWIFT_VERSION)\s*=", text))
    sdk_roots = {match.lower() for text in pbx_texts for match in re.findall(r"\bSDKROOT\s*=\s*([^;\s]+)", text)}
    inferred_platform = "ios" if sdk_roots and sdk_roots <= {"iphoneos"} else "macos" if sdk_roots and sdk_roots <= {"macosx"} else None
    app_names = [name for name, product in target_records if XCODE_PRODUCT_TYPES.get(product or "") == "app"]
    extension_names = [name for name, product in target_records if XCODE_PRODUCT_TYPES.get(product or "") == "extension"]
    hosts: dict[str, str] = {}
    for text in pbx_texts:
        hosts.update(pbx_extension_hosts(text, app_names, extension_names))
    flat_owned = [name for name in ("Sources", "Resources", "Tests", "Configurations", "Shared", "Extensions") if (root / name).exists()]
    for name, product in target_records:
        kind = XCODE_PRODUCT_TYPES.get(product or "")
        if kind is None:
            components.append(Component(name, "unsupported", ".", "", [f"PBX product type {product or 'missing'}"], product_type=product, unresolved=["unsupported or missing Xcode product type"]))
            continue
        destination = f"Apps/{name}"
        host = hosts.get(name)
        unresolved: list[str] = []
        if kind in {"app", "extension", "test", "ui-test"} and not inferred_platform:
            unresolved.append("target platform requires reviewed mapping evidence")
        if kind == "extension" and not host:
            unresolved.append("extension host target is not explicit or is ambiguous")
        owned = flat_owned if kind == "app" and len(app_names) == 1 else []
        components.append(Component(name, kind, ".", destination, [f"PBX native target product type {product}"], host_target=host, platform=inferred_platform, product_type=product, owned_paths=owned, unresolved=unresolved))
    discovered_names = {component.name for component in components}
    xcodegen_records = [record for spec in specs for record in xcodegen_target_records(read_text(spec))]
    xcodegen_apps = [name for name, product, _, _ in xcodegen_records if product == "application"]
    xcodegen_hosts = {dependency: name for name, product, _, dependency in xcodegen_records if product == "application" and dependency}
    for name, product, platform, _ in xcodegen_records:
        if name in discovered_names:
            continue
        kind = {"application": "app", "app-extension": "extension", "extensionkit-extension": "extension", "bundle.unit-test": "test", "bundle.ui-testing": "ui-test"}.get(product or "")
        unresolved: list[str] = []
        if kind is None:
            components.append(Component(name, "unsupported", ".", "", [f"XcodeGen target type {product or 'missing'}"], product_type=product, unresolved=["unsupported or missing XcodeGen target type"]))
            continue
        normalized_platform = {"ios": "ios", "macos": "macos", "tvos": "tvos", "watchos": "watchos", "visionos": "visionos"}.get(platform or "")
        if not normalized_platform:
            unresolved.append("target platform requires reviewed mapping evidence")
        host = xcodegen_hosts.get(name)
        if kind == "extension" and not host:
            unresolved.append("extension host target is not explicit or is ambiguous")
        owned = flat_owned if kind == "app" and len(xcodegen_apps) == 1 else []
        canonical_product = "com.apple.product-type.app-extension" if product == "app-extension" else "com.apple.product-type.extensionkit-extension" if product == "extensionkit-extension" else product
        components.append(Component(name, kind, ".", f"Apps/{name}", [f"XcodeGen target type {product}"], host_target=host, platform=normalized_platform, product_type=canonical_product, owned_paths=owned, unresolved=unresolved))
    inventory = {
        "workspaces": [relative(path, root) for path in workspaces],
        "projects": [relative(path, root) for path in projects],
        "xcodegen_specs": [relative(path, root) for path in specs],
        "swift_manifests": [relative(path, root) for path in manifests],
        "xcconfigs": [relative(path, root) for path in sorted(root.rglob("*.xcconfig"))],
        "entitlements": [relative(path, root) for path in sorted(root.rglob("*.entitlements"))],
        "info_plists": [relative(path, root) for path in sorted(root.rglob("Info.plist"))],
        "asset_catalogs": [relative(path, root) for path in sorted(root.rglob("*.xcassets"))],
        "schemes": [relative(path, root) for path in sorted(root.rglob("*.xcscheme"))],
        "test_plans": [relative(path, root) for path in sorted(root.rglob("*.xctestplan"))],
        "pbx_settings_to_promote": sorted(item.removesuffix(" =") for item in pbx_settings),
        "cloud_inputs": [relative(path, root) for pattern in ("Dockerfile*", "fly.toml") for path in sorted(root.rglob(pattern))],
    }
    return components, inventory


def proposed_adoption_map(root: Path, components: list[Component]) -> dict[str, Any]:
    name = next((path.stem for path in sorted(root.glob("*.xcworkspace"))), None) or next((path.stem for path in sorted(root.glob("*.xcodeproj"))), None) or (components[0].name if components else None) or re.sub(r"[^A-Za-z0-9]", "", root.name.title()) or "Product"
    return {"schema_version": 1, "workspace_name": name, "components": [asdict(component) for component in components]}


def validate_adoption_map(root: Path, mapping: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if mapping.get("schema_version") != 1:
        errors.append("adoption map schema_version must be 1")
    name = mapping.get("workspace_name")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", name):
        errors.append("workspace_name must be an alphanumeric Xcode identifier")
    components = mapping.get("components")
    if not isinstance(components, list) or not components:
        errors.append("adoption map must contain at least one component")
        return errors
    destinations: set[str] = set()
    owned: dict[str, str] = {}
    app_names = {item.get("name") for item in components if isinstance(item, dict) and item.get("kind") == "app"}
    for index, item in enumerate(components):
        label = f"components[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        kind, component_name, destination = item.get("kind"), item.get("name"), item.get("proposed_destination")
        if kind not in {"app", "extension", "test", "ui-test", "library", "service"}:
            errors.append(f"{label}.kind is unsupported: {kind!r}")
        if not isinstance(component_name, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", component_name):
            errors.append(f"{label}.name must be an alphanumeric target or package name")
        expected_prefix = "Apps/" if kind in {"app", "extension", "test", "ui-test"} else "Packages/" if kind == "library" else "Services/"
        if not isinstance(destination, str) or not destination.startswith(expected_prefix) or ".." in Path(destination).parts:
            errors.append(f"{label}.proposed_destination must be under {expected_prefix}")
        elif destination in destinations:
            errors.append(f"duplicate component destination: {destination}")
        else:
            destinations.add(destination)
        if kind in {"app", "extension", "test", "ui-test"} and item.get("platform") not in SUPPORTED_PLATFORMS:
            errors.append(f"{label}.platform requires explicit ios, macos, tvos, watchos, or visionos evidence")
        if kind == "extension":
            if item.get("host_target") not in app_names:
                errors.append(f"{label}.host_target must name one mapped application target")
            if item.get("product_type") not in {"com.apple.product-type.app-extension", "com.apple.product-type.extensionkit-extension"}:
                errors.append(f"{label}.product_type must be a supported documented extension product type")
            if not item.get("extension_point_identifier"):
                errors.append(f"{label}.extension_point_identifier is required")
        for source in item.get("owned_paths") or []:
            if not isinstance(source, str) or Path(source).is_absolute() or ".." in Path(source).parts:
                errors.append(f"{label}.owned_paths contains an unsafe path")
                continue
            if source in owned:
                errors.append(f"{source} is assigned to both {owned[source]} and {component_name}")
            owned[source] = str(component_name)
            if not (root / source).exists():
                errors.append(f"mapped source does not exist: {source}")
        if item.get("unresolved"):
            errors.append(f"{label} still has unresolved evidence: {', '.join(item['unresolved'])}")
    return errors


def move_owned_path(root: Path, source_name: str, destination_root: Path) -> None:
    source = root / source_name
    if source.name in {"Package.swift", "Sources", "Tests", "Plugins"}:
        destination = destination_root / source.name
    elif source.is_dir() and source_name.count("/") > 0:
        destination = destination_root
    else:
        destination = destination_root / source.name
    if destination.exists():
        raise RuntimeError(f"Adoption destination already exists: {relative(destination, root)}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))


def adopted_native_target_spec(item: dict[str, Any], org: str, team: str) -> str:
    name, kind, platform = item["name"], item["kind"], item["platform"]
    display = SUPPORTED_PLATFORMS[platform]
    if kind == "app":
        product_type = "application"
    elif kind == "extension":
        product_type = "app-extension" if item["product_type"] == "com.apple.product-type.app-extension" else "extensionkit-extension"
    elif kind == "test":
        product_type = "bundle.unit-test"
    else:
        product_type = "bundle.ui-testing"
    destination = item["proposed_destination"]
    lines = [
        "targets:", f"  {name}:", f"    type: {product_type}", f"    platform: {display}", "    sources:",
        f"      - path: {destination}/Sources", "        type: syncedFolder", "        optional: true",
        f"      - path: {destination}/Resources", "        type: syncedFolder", "        optional: true",
        "    settings:", "      base:", f"        PRODUCT_BUNDLE_IDENTIFIER: {item.get('bundle_identifier') or org + '.' + name.lower()}",
        f"        DEVELOPMENT_TEAM: {item.get('development_team') or team}", "        CODE_SIGN_STYLE: Automatic",
    ]
    if kind == "extension":
        lines.extend(["    info:", f"      path: {destination}/Resources/Info.plist"])
    dependencies = item.get("dependencies") or []
    if kind in {"test", "ui-test"} and item.get("host_target"):
        dependencies = [*dependencies, item["host_target"]]
    if dependencies:
        lines.append("    dependencies:")
        lines.extend(f"      - target: {dependency}" for dependency in dependencies)
    return "\n".join(lines) + "\n"


def stage_adoption(root: Path, mapping: dict[str, Any], org: str, team: str) -> dict[str, Any]:
    snapshot = root / ".socket/adoption/original-inventory.json"
    if snapshot.exists():
        raise RuntimeError("An adoption is already staged; review or revert .socket/adoption before applying another map.")
    components, inventory = inventory_components(root)
    write(snapshot, json.dumps({"inventory": inventory, "components": [asdict(item) for item in components]}, indent=2, sort_keys=True) + "\n")
    original_spec = root / "project.yml"
    if original_spec.exists():
        write(root / ".socket/adoption/original-project.yml", original_spec.read_text(encoding="utf-8"))
    for directory in ("Apps", "Packages", "Services", "Configurations", "Scripts", "docs"):
        (root / directory).mkdir(exist_ok=True)
    name = mapping["workspace_name"]
    write(root / "project.yml", root_spec(name, []))
    write(root / "Apps/apps-shared.yml", app_shared_spec())
    write(root / "Apps/Apps-shared.xcconfig", '#include "../Configurations/Project.xcconfig"\n')
    write(root / "Packages/packages-shared.yml", "packages: {}\n")
    write(root / "Services/services-shared.yml", "packages: {}\n")
    write(root / "Configurations/Project.xcconfig", "SWIFT_VERSION = 6.0\nSWIFT_STRICT_CONCURRENCY = complete\n")
    for config in CONFIGURATIONS:
        write(root / f"Configurations/{config}.xcconfig", '#include "Project.xcconfig"\n')
    native_items = [item for item in mapping["components"] if item["kind"] in {"app", "extension", "test", "ui-test"}]
    for item in mapping["components"]:
        destination = root / item["proposed_destination"]
        for source in item.get("owned_paths") or []:
            move_owned_path(root, source, destination)
        if item["kind"] in {"library", "service"}:
            add_package_mapping(root, "Packages" if item["kind"] == "library" else "Services", item["name"])
        else:
            add_root_include(root, f"{item['proposed_destination']}/target.yml")
            write(destination / "target.yml", adopted_native_target_spec(item, org, team))
            if item["kind"] == "extension":
                info = destination / "Resources/Info.plist"
                if not info.exists():
                    write(info, '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>NSExtension</key><dict><key>NSExtensionPointIdentifier</key><string>' + item["extension_point_identifier"] + '</string></dict></dict></plist>\n')
    for item in native_items:
        if item["kind"] == "extension":
            embed_extension_in_host(root, item["host_target"], item["name"])
    candidate = root / ".socket/adoption-candidate"
    candidate.mkdir(parents=True, exist_ok=True)
    generated = subprocess.run(["xcodegen", "generate", "--spec", "project.yml", "--project", str(candidate), "--project-root", str(root)], cwd=root, capture_output=True, text=True, check=False)
    if generated.returncode != 0:
        raise RuntimeError(f"candidate XcodeGen generation failed:\n{generated.stderr}")
    candidate_pbx = read_text(candidate / f"{name}.xcodeproj/project.pbxproj")
    generated_targets = {target for target, _ in pbx_target_records(candidate_pbx)}
    expected_targets = {item["name"] for item in native_items}
    missing = sorted(expected_targets - generated_targets)
    report = {
        "expected_native_targets": sorted(expected_targets),
        "generated_native_targets": sorted(generated_targets),
        "missing_native_targets": missing,
        "candidate_project": relative(candidate / f"{name}.xcodeproj", root),
        "preserved_inventory": relative(snapshot, root),
    }
    write(root / ".socket/adoption/equivalence-report.json", json.dumps(report, indent=2, sort_keys=True) + "\n")
    if missing:
        raise RuntimeError("Candidate equivalence failed; missing native targets: " + ", ".join(missing))
    return report


def install(root: Path, name: str, prefix: str, platforms: list[str], org: str, team: str) -> None:
    write(root / "project.yml", root_spec(name, platforms))
    write(root / "Apps/apps-shared.yml", app_shared_spec())
    write(root / "Apps/Apps-shared.xcconfig", "#include \"../Configurations/Project.xcconfig\"\nASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES\nLOCALIZATION_PREFERS_STRING_CATALOGS = YES\nSTRING_CATALOG_GENERATE_SYMBOLS = YES\n")
    write(root / "Packages/packages-shared.yml", package_spec(name))
    write(root / "Services/services-shared.yml", "packages: {}\n")
    write(root / "Configurations/Project.xcconfig", "SWIFT_VERSION = 6.0\nSWIFT_STRICT_CONCURRENCY = complete\nSWIFT_APPROACHABLE_CONCURRENCY = YES\nDEAD_CODE_STRIPPING = YES\nENABLE_USER_SCRIPT_SANDBOXING = NO\n")
    for config in CONFIGURATIONS:
        settings = '#include "Project.xcconfig"\n'
        if config == "Debug":
            settings += "SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG $(inherited)\n"
        else:
            settings += "SWIFT_COMPILATION_MODE = wholemodule\nSWIFT_OPTIMIZATION_LEVEL = -O\n"
        write(root / f"Configurations/{config}.xcconfig", settings)
    write(root / ".gitignore", "Build/\nDerivedData/\nxcuserdata/\n*.xcuserstate\n")
    write(root / f"{name}.xcworkspace/contents.xcworkspacedata", f'<?xml version="1.0" encoding="UTF-8"?>\n<Workspace version="1.0">\n  <FileRef location="group:{name}.xcodeproj"/>\n</Workspace>\n')
    (root / "docs").mkdir()
    install_alignment_runtime(root)
    write(root / "Justfile", (root / "Justfile").read_text(encoding="utf-8") + "\nvalidate:\n  sh Scripts/validate.sh\npackage-test:\n  for manifest in Packages/*/Package.swift Services/*/Package.swift; do [ -f \"$manifest\" ] || continue; (cd \"$(dirname \"$manifest\")\" && swift test); done\ntest target:\n  xcodebuild -workspace *.xcworkspace -scheme \"{{target}}\" test\narchive target channel:\n  sh Scripts/release.sh \"{{target}}\" \"{{channel}}\"\napp-store target:\n  sh Scripts/release.sh \"{{target}}\" app-store\naltstore target:\n  sh Scripts/release.sh \"{{target}}\" altstore\ndirect-distribution target:\n  sh Scripts/release.sh \"{{target}}\" direct-distribution\n")
    write(root / "Scripts/increment-build-version.sh", "#!/usr/bin/env sh\nset -eu\ntarget=${1:?target required}; configuration=${2:?configuration required}; label=$(printf '%s' \"$configuration\" | tr '[:upper:]' '[:lower:]')\nfile=\"Apps/$target/Configurations/Version.xcconfig\"\ngit rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo \"Build counter requires a Git repository.\" >&2; exit 1; }\n[ \"$configuration\" = Debug ] && key=DEBUG_BUILD_NUMBER || key=RELEASE_BUILD_NUMBER\nvalue=$(awk -F ' = ' -v key=\"$key\" '$1 == key { print $2 }' \"$file\")\n[ -n \"$value\" ] || { echo \"Missing $key in $file\" >&2; exit 1; }\nawk -F ' = ' -v key=\"$key\" -v next=$((value + 1)) 'BEGIN { OFS = \" = \" } $1 == key { $2 = next } { print }' \"$file\" > \"$file.tmp\" && mv \"$file.tmp\" \"$file\"\nstaged=false; unstaged=false; git diff --cached --quiet || staged=true; git diff --quiet || unstaged=true\nif $staged && $unstaged; then git add \"$file\"; echo \"warning: staged build counter update; commit it manually as soon as possible.\" >&2; exit 0; fi\nif $staged; then patch=$(mktemp); git diff --cached --binary > \"$patch\"; git restore --staged :/; git add \"$file\"; git commit -m \"build: increment $target $label build\"; git apply --cached \"$patch\"; rm -f \"$patch\"; else git add \"$file\"; git commit -m \"build: increment $target $label build\"; fi\n", True)
    write(root / "Scripts/validate.sh", "#!/usr/bin/env sh\nset -eu\nswiftformat --lint --config .swiftformat Apps Packages Services\nswiftlint lint --config .swiftlint.yml --force-exclude Apps Packages Services\nxcodegen generate --spec project.yml\nworkspace=$(find . -maxdepth 1 -type d -name '*.xcworkspace' -print -quit)\nxcodebuild -list -workspace \"$workspace\"\nfor manifest in Packages/*/Package.swift Services/*/Package.swift; do [ -f \"$manifest\" ] || continue; (cd \"$(dirname \"$manifest\")\" && swift test); done\n", True)
    write(root / "Scripts/release.sh", "#!/usr/bin/env sh\nset -eu\ntarget=${1:?target required}; channel=${2:?channel required}\nworkspace=$(find . -maxdepth 1 -type d -name '*.xcworkspace' -print -quit)\ncase \"$channel\" in\n  staging) scheme=\"$target Staging\"; config=Staging ;;\n  app-store) scheme=\"$target App Store\"; config=AppStore ;;\n  altstore) scheme=\"$target AltStore\"; config=AltStore ;;\n  direct-distribution) scheme=\"$target Direct Distribution\"; config=DirectDistribution ;;\n  *) echo \"Unknown release channel: $channel\" >&2; exit 1 ;;\nesac\narchive=\"Build/$target-$channel.xcarchive\"\nxcodebuild -workspace \"$workspace\" -scheme \"$scheme\" -configuration \"$config\" -archivePath \"$archive\" archive\ncase \"$channel\" in\n  app-store) xcodebuild -exportArchive -archivePath \"$archive\" -exportPath \"Build/$target-app-store\" -exportOptionsPlist Scripts/ExportOptions/AppStore.plist; artifact=$(find \"Build/$target-app-store\" -type f \\( -name '*.ipa' -o -name '*.pkg' \\) -print -quit); [ -n \"$artifact\" ] || { echo \"App Store export produced no IPA or PKG.\" >&2; exit 1; }; case \"$target\" in *macOS) type=osx ;; *) type=ios ;; esac; xcrun altool --upload-app -f \"$artifact\" -t \"$type\" ;;\n  altstore) xcodebuild -exportArchive -archivePath \"$archive\" -exportPath \"Build/$target-altstore\" -exportOptionsPlist Scripts/ExportOptions/AltStore.plist ;;\n  direct-distribution) xcodebuild -exportArchive -archivePath \"$archive\" -exportPath \"Build/$target-direct\" -exportOptionsPlist Scripts/ExportOptions/DirectDistribution.plist; app=$(find \"Build/$target-direct\" -type d -name '*.app' -print -quit); [ -n \"$app\" ] || { echo \"Direct export produced no app bundle.\" >&2; exit 1; }; dmg=\"Build/$target-direct/$target.dmg\"; hdiutil create -volname \"$target\" -srcfolder \"$app\" -ov -format UDZO \"$dmg\"; xcrun notarytool submit \"$dmg\" --keychain-profile notarytool --wait; xcrun stapler staple \"$dmg\" ;;\nesac\n", True)
    write(root / "Scripts/ExportOptions/AppStore.plist", '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>method</key><string>app-store</string></dict></plist>\n')
    write(root / "Scripts/ExportOptions/AltStore.plist", '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>method</key><string>development</string></dict></plist>\n')
    write(root / "Scripts/ExportOptions/DirectDistribution.plist", '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>method</key><string>developer-id</string></dict></plist>\n')
    write(root / "ROADMAP.md", "# Roadmap\n\n## Managed workspace expansion\n\n- [ ] Extend `just align` ownership to additional documentation, templates, and repository scripts when each surface has a safe managed boundary.\n")
    for platform in platforms:
        display = SUPPORTED_PLATFORMS[platform]
        target = f"{name}{display}"
        app_root = root / "Apps" / target
        write(app_root / "target.yml", target_spec(name, platform, prefix, org, team))
        write(app_root / "Configurations/App.xcconfig", '#include "../../Apps-shared.xcconfig"\nMARKETING_VERSION = 0.0.1\nCODE_SIGN_STYLE = Automatic\n')
        write(app_root / "Configurations/Version.xcconfig", "DEBUG_BUILD_NUMBER = 1\nRELEASE_BUILD_NUMBER = 1\n")
        for config in CONFIGURATIONS:
            build_number = "$(DEBUG_BUILD_NUMBER)" if config == "Debug" else "$(RELEASE_BUILD_NUMBER)"
            content = '#include "App.xcconfig"\n#include "Version.xcconfig"\nCURRENT_PROJECT_VERSION = ' + build_number + "\n"
            if config == "Debug":
                content += "ONLY_ACTIVE_ARCH = YES\n"
            else:
                content += "SWIFT_OPTIMIZATION_LEVEL = -O\n"
            write(app_root / f"Configurations/{config}.xcconfig", content)
        write(app_root / f"Sources/{prefix}App.swift", f'import SwiftUI\n\n@main\nstruct {prefix}{display}App: App {{\n    var body: some Scene {{ WindowGroup {{ Text("{target}") }} }}\n}}\n')
        write(app_root / "Sources/Views/.gitkeep", "")
        write(app_root / "Sources/Datamodels/.gitkeep", "")
        write(app_root / "Sources/Services/.gitkeep", "")
        write(app_root / "Resources/Info.plist", '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>CFBundleShortVersionString</key><string>$(MARKETING_VERSION)</string><key>CFBundleVersion</key><string>$(CURRENT_PROJECT_VERSION)</string></dict></plist>\n')
        write(app_root / f"Resources/{target}.entitlements", '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict/></plist>\n')
        write(app_root / "Resources/Assets.xcassets/Contents.json", '{"info":{"author":"xcode","version":1}}\n')
        write(app_root / "Resources/Assets.xcassets/AppIcon.appiconset/Contents.json", '{"images":[],"info":{"author":"xcode","version":1}}\n')
        write(app_root / "Resources/Assets.xcassets/AccentColor.colorset/Contents.json", '{"colors":[],"info":{"author":"xcode","version":1}}\n')
        write(app_root / "Resources/Localizable.xcstrings", '{"sourceLanguage":"en","strings":{},"version":"1.0"}\n')
        tests_root = root / "Apps" / f"{target}Tests"
        write(tests_root / f"Sources/{target}Tests.swift", f'import Testing\n@testable import {target}\n\n@Test func example() {{ #expect(true) }}\n')
        if platform != "watchos":
            ui_root = root / "Apps" / f"{target}UITests"
            write(ui_root / f"Sources/{target}UITests.swift", f'import XCTest\n\nfinal class {target}UITests: XCTestCase {{\n    func testLaunch() {{}}\n}}\n')
    package_root = root / "Packages" / f"{name}Core"
    package_root.mkdir(parents=True)
    subprocess.run(["swift", "package", "init", "--type", "library", "--name", f"{name}Core", "--enable-swift-testing"], cwd=package_root, check=True, capture_output=True, text=True)
    write(package_root / "Package.swift", f'''// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "{name}Core",
    platforms: [.iOS(.v26), .macOS(.v26), .tvOS(.v26), .watchOS(.v26), .visionOS(.v26)],
    products: [.library(name: "{name}Core", targets: ["{name}Core"])],
    targets: [
        .target(name: "{name}Domain"),
        .target(name: "{name}UI", dependencies: ["{name}Domain"]),
        .target(name: "{name}Services", dependencies: ["{name}Domain"]),
        .target(name: "{name}Core", dependencies: ["{name}Domain", "{name}UI", "{name}Services"]),
        .testTarget(name: "{name}DomainTests", dependencies: ["{name}Domain"]),
        .testTarget(name: "{name}UITests", dependencies: ["{name}UI"]),
        .testTarget(name: "{name}ServicesTests", dependencies: ["{name}Services"]),
        .testTarget(name: "{name}CoreTests", dependencies: ["{name}Core"]),
    ]
)
''')
    write(package_root / f"Sources/{name}Core/{name}Core.swift", f"@_exported import {name}Domain\n@_exported import {name}UI\n@_exported import {name}Services\n")
    for module, folders in ((f"{name}Domain", ("Datamodels", "Actions")), (f"{name}UI", ("Components", "Styles")), (f"{name}Services", ("Clients", "DTOs"))):
        for folder in folders:
            write(package_root / f"Sources/{module}/{folder}/.gitkeep", "")
        write(package_root / f"Sources/{module}/{module}.swift", f"public enum {module} {{}}\n")
    for module in (f"{name}Core", f"{name}Domain", f"{name}UI", f"{name}Services"):
        write(package_root / f"Tests/{module}Tests/{module}Tests.swift", f"import Testing\n@testable import {module}\n\n@Test func example() {{ #expect(true) }}\n")


def main() -> int:
    args = parser().parse_args()
    platforms = [item.strip().lower() for item in args.platforms.split(",") if item.strip()]
    root = Path(args.repo_root).expanduser().resolve() if args.operation in {"adopt", "align", "add-component"} and args.repo_root else ((Path(args.destination).expanduser() / args.name).resolve() if args.name else Path(args.destination).expanduser().resolve())
    inputs = {"operation": args.operation, "name": args.name, "file_prefix": args.file_prefix, "destination": args.destination, "repo_root": args.repo_root, "platforms": platforms, "component_kind": args.component_kind, "component_name": args.component_name, "platform": args.platform, "framework": args.framework, "host_target": args.host_target, "extension_product_type": args.extension_product_type, "extension_point_identifier": args.extension_point_identifier, "adoption_map": args.adoption_map, "apply": args.apply, "org_identifier": args.org_identifier, "development_team": args.development_team, "dry_run": args.dry_run, "skip_validation": args.skip_validation}
    if args.operation == "adopt":
        if not args.repo_root:
            return blocked("--repo-root is required with --operation adopt.", inputs)
        if not root.is_dir():
            return blocked("The requested adoption root is not a directory.", inputs)
        if not workspace_findings(root):
            print(json.dumps({"status": "success", "path_type": "primary", "workspace_root": str(root), "normalized_inputs": inputs, "components": [], "migration_required": False, "next_step": "The repository is already canonical; use --operation align."}, indent=2, sort_keys=True))
            return 0
        components, inventory = inventory_components(root)
        mapping = proposed_adoption_map(root, components)
        if not components:
            return blocked("No SwiftPM manifest or Xcode native target evidence was found to adopt.", inputs)
        if not args.apply:
            unresolved = [f"{item.name}: {reason}" for item in components for reason in item.unresolved]
            payload = {"status": "blocked" if unresolved else "success", "path_type": "primary", "workspace_root": str(root), "normalized_inputs": inputs, "inventory": inventory, "components": [asdict(item) for item in components], "adoption_map": mapping, "migration_required": True, "unresolved": unresolved, "next_step": "Review the adoption_map, add required explicit ownership/host/platform/extension-point evidence, save it as JSON, then rerun with --adoption-map <path> --apply."}
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1 if unresolved else 0
        if not args.adoption_map:
            return blocked("--adoption-map is required with --operation adopt --apply.", inputs)
        map_path = Path(args.adoption_map).expanduser().resolve()
        if not map_path.is_file():
            return blocked("The reviewed --adoption-map file does not exist.", inputs)
        try:
            reviewed = json.loads(map_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return blocked(f"Could not read the reviewed adoption map: {exc}", inputs)
        errors = validate_adoption_map(root, reviewed)
        if errors:
            return blocked("Reviewed adoption map is not safe to apply: " + "; ".join(errors), inputs)
        if not shutil.which("xcodegen"):
            return blocked("XcodeGen is required to generate the adoption candidate project.", inputs)
        try:
            report = stage_adoption(root, reviewed, args.org_identifier, args.development_team)
            print(json.dumps({"status": "success", "path_type": "primary", "workspace_root": str(root), "normalized_inputs": inputs, "components": reviewed["components"], "equivalence": report, "migration_required": True, "next_step": "Review .socket/adoption/equivalence-report.json and candidate project before finalizing removal of superseded project files; no original project was deleted."}, indent=2, sort_keys=True))
            return 0
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            return blocked(str(exc), inputs)
    if args.operation == "add-component":
        if not args.repo_root or not args.component_kind or not args.component_name:
            return blocked("--repo-root, --component-kind, and --component-name are required with --operation add-component.", inputs)
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", args.component_name):
            return blocked("--component-name must be an alphanumeric Swift identifier beginning with a letter.", inputs)
        findings = workspace_findings(root, allow_missing_services=True) if root.is_dir() else ["The requested workspace root is not a directory."]
        if findings:
            return blocked(" ".join(findings), inputs)
        if args.component_kind == "app" and not args.platform:
            return blocked("--platform is required when adding an app component.", inputs)
        if args.component_kind == "app" and not re.fullmatch(r"[A-Z]{3}", args.file_prefix):
            return blocked("--file-prefix must contain exactly three uppercase ASCII letters.", inputs)
        if args.component_kind == "extension" and (not args.platform or not args.host_target or not args.extension_product_type or not args.extension_point_identifier):
            return blocked("--platform, --host-target, --extension-product-type, and --extension-point-identifier are required when adding an extension component.", inputs)
        if args.component_kind == "service" and not args.framework:
            return blocked("--framework is required when adding a service component.", inputs)
        if not args.dry_run and not shutil.which("xcodegen"):
            return blocked("XcodeGen is required to regenerate the workspace after adding a component.", inputs)
        actions = ensure_services_surface(root, dry_run=True) + [f"add {args.component_kind} component {args.component_name}", "regenerate the root XcodeGen project"]
        if args.dry_run:
            print(json.dumps({"status": "success", "path_type": "primary", "workspace_root": str(root), "normalized_inputs": inputs, "actions": actions}, indent=2, sort_keys=True))
            return 0
        try:
            ensure_services_surface(root)
            product = workspace_name(root)
            if args.component_kind == "library":
                create_library_component(root, args.component_name)
            elif args.component_kind == "app":
                create_app_component(root, product, args.component_name, args.platform, args.file_prefix, args.org_identifier, args.development_team)
            elif args.component_kind == "extension":
                create_extension_component(root, args.component_name, args.platform, args.host_target, args.extension_product_type, args.extension_point_identifier, args.org_identifier, args.development_team)
            else:
                adapter = subprocess.run([str(server_component_runner()), "--repo-root", str(root), "--name", args.component_name, "--framework", args.framework], capture_output=True, text=True, check=False)
                if adapter.returncode != 0:
                    raise RuntimeError(f"server component adapter failed:\n{adapter.stdout}\n{adapter.stderr}")
            generated = subprocess.run(["xcodegen", "generate", "--spec", "project.yml"], cwd=root, capture_output=True, text=True, check=False)
            if generated.returncode != 0:
                raise RuntimeError(f"xcodegen generate failed:\n{generated.stderr}")
            print(json.dumps({"status": "success", "path_type": "primary", "workspace_root": str(root), "normalized_inputs": inputs, "actions": actions, "next_step": "Open the existing root workspace; the new component is part of the same product entrypoint."}, indent=2, sort_keys=True))
            return 0
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            return blocked(str(exc), inputs)
    if args.operation == "align":
        if not args.repo_root:
            return blocked("--repo-root is required with --operation align.", inputs)
        if not args.dry_run and not shutil.which("xcodegen"):
            return blocked("XcodeGen is required to regenerate an aligned workspace.", inputs)
        findings = workspace_findings(root, allow_missing_services=True) if root.is_dir() else ["The requested workspace root is not a directory."]
        if findings:
            return blocked(" ".join(findings), inputs)
        try:
            actions = ensure_services_surface(root, args.dry_run) + install_alignment_runtime(root, args.dry_run)
            if not args.dry_run:
                generated = subprocess.run(["xcodegen", "generate", "--spec", "project.yml"], cwd=root, capture_output=True, text=True, check=False)
                if generated.returncode != 0:
                    raise RuntimeError(f"xcodegen generate failed:\n{generated.stderr}")
            print(json.dumps({"status": "success", "path_type": "primary", "workspace_root": str(root), "normalized_inputs": inputs, "actions": actions + ["regenerate the root XcodeGen project"], "next_step": "Run just setup once, then use just align as the single managed-guidance refresh command."}, indent=2, sort_keys=True))
            return 0
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            return blocked(str(exc), inputs)
    if not args.name:
        return blocked("--name is required when creating a new workspace.", inputs)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", args.name):
        return blocked("--name must be an alphanumeric Swift/Xcode identifier beginning with a letter.", inputs)
    if not re.fullmatch(r"[A-Z]{3}", args.file_prefix):
        return blocked("--file-prefix must contain exactly three uppercase ASCII letters.", inputs)
    service_first = args.component_kind == "service"
    library_first = args.component_kind == "library"
    component_first = service_first or library_first
    if component_first:
        platforms = []
        inputs["platforms"] = platforms
        if service_first and not args.framework:
            return blocked("--framework is required when creating a service-first workspace.", inputs)
    if (not component_first and not platforms) or any(platform not in SUPPORTED_PLATFORMS for platform in platforms):
        return blocked("--platforms must be a comma-separated subset of ios,macos,tvos,watchos,visionos.", inputs)
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        return blocked("The product root already contains files; use --operation align --repo-root <existing-root> for a canonical workspace.", inputs)
    xcodegen = shutil.which("xcodegen")
    if not xcodegen:
        return blocked("XcodeGen is required to create the root generated project.", inputs)
    actions = ["create one root XcodeGen project", "create Apps/, Packages/, and Services/ component roots", "create Packages/ local Swift package", "create root workspace wrapper"]
    if service_first:
        actions.append(f"create Services/{args.component_name or args.name + 'API'} with the {args.framework} workspace adapter")
    elif library_first:
        actions.append(f"create Packages/{args.component_name or args.name + 'Core'} as the first product component")
    payload: dict[str, object] = {"status": "success", "path_type": "primary", "workspace_root": str(root), "workspace_path": str(root / f"{args.name}.xcworkspace"), "project_path": str(root / f"{args.name}.xcodeproj"), "normalized_inputs": inputs, "actions": actions}
    if args.dry_run:
        payload["validation_result"] = "skipped (--dry-run)"
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    root.mkdir(parents=True)
    try:
        install(root, args.name, args.file_prefix, platforms, args.org_identifier, args.development_team)
        if library_first and args.component_name and args.component_name != f"{args.name}Core":
            create_library_component(root, args.component_name)
        if service_first:
            adapter_command = [str(server_component_runner()), "--repo-root", str(root), "--name", args.component_name or f"{args.name}API", "--framework", args.framework]
            if args.skip_validation:
                adapter_command.append("--skip-validation")
            adapter = subprocess.run(adapter_command, capture_output=True, text=True, check=False)
            if adapter.returncode != 0:
                raise RuntimeError(f"server component adapter failed:\n{adapter.stdout}\n{adapter.stderr}")
        generated = subprocess.run([xcodegen, "generate", "--spec", "project.yml"], cwd=root, capture_output=True, text=True, check=False)
        if generated.returncode != 0:
            raise RuntimeError(f"xcodegen generate failed:\n{generated.stderr}")
        runner = maintain_project_repo_runner()
        maintenance = subprocess.run([str(runner), "--repo-root", str(root), "--operation", "install", "--profile", "xcode-workspace"], capture_output=True, text=True, check=False)
        if maintenance.returncode != 0:
            raise RuntimeError(f"maintain-project-repo install failed:\n{maintenance.stdout}\n{maintenance.stderr}")
        validation = "skipped (--skip-validation)"
        if not args.skip_validation:
            check = subprocess.run(["xcodebuild", "-list", "-workspace", f"{args.name}.xcworkspace"], cwd=root, capture_output=True, text=True, check=False)
            if check.returncode != 0:
                raise RuntimeError(f"xcodebuild -list failed:\n{check.stderr}")
            validation = "passed (xcodebuild -list -workspace)"
        payload["validation_result"] = validation
        payload["next_step"] = "Open the root workspace; edit project.yml, included target specs, .xcconfig files, and Package.swift—not generated project data."
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        payload.update(status="failed", stderr=str(exc), next_step="Fix the reported bootstrap prerequisite or generated-spec error and rerun the workflow.")
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
