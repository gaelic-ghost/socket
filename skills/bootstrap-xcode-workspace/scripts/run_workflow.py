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
from pathlib import Path

SUPPORTED_PLATFORMS = {
    "ios": "iOS",
    "macos": "macOS",
    "tvos": "tvOS",
    "watchos": "watchOS",
    "visionos": "visionOS",
}
CONFIGURATIONS = ("Debug", "Staging", "Release", "AppStore", "DirectDistribution", "AltStore")


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
    result.add_argument("--repo-root", help="Align an existing canonical workspace root instead of creating a new product.")
    result.add_argument("--operation", choices=("create", "align"), default="create")
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


def workspace_findings(root: Path) -> list[str]:
    findings: list[str] = []
    if len(list(root.glob("*.xcworkspace"))) != 1:
        findings.append("Expected exactly one root .xcworkspace.")
    if len(list(root.glob("*.xcodeproj"))) != 1:
        findings.append("Expected exactly one generated root .xcodeproj.")
    required = ("project.yml", "Apps/apps-shared.yml", "Apps/Apps-shared.xcconfig", "Packages/packages-shared.yml")
    findings.extend(f"Expected {path}." for path in required if not (root / path).is_file())
    if not list((root / "Apps").glob("**/target.y*ml")):
        findings.append("Expected at least one target.yml under Apps/.")
    if not list((root / "Packages").glob("**/Package.swift")):
        findings.append("Expected at least one Package.swift under Packages/.")
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
        "for file in AGENTS-root.md AGENTS-apps.md AGENTS-packages.md CONTRIBUTING.md pre-commit; do curl --fail --silent --show-error \"$base/$file\" -o \"$tmp/$file\"; done",
        "for file in AGENTS-root.md AGENTS-apps.md AGENTS-packages.md CONTRIBUTING.md; do [ \"$(grep -c 'socket-managed:begin' \"$tmp/$file\")\" -eq 1 ] && [ \"$(grep -c 'socket-managed:end' \"$tmp/$file\")\" -eq 1 ] || { echo \"just align: remote $file has invalid managed markers; no files were changed.\" >&2; exit 1; }; done",
        "[ -s \"$tmp/pre-commit\" ] || { echo \"just align: remote pre-commit hook is empty; no files were changed.\" >&2; exit 1; }",
        "for file in AGENTS.md Apps/AGENTS.md Packages/AGENTS.md CONTRIBUTING.md; do [ \"$(grep -c 'socket-managed:begin' \"$file\")\" -eq 1 ] && [ \"$(grep -c 'socket-managed:end' \"$file\")\" -eq 1 ] || { echo \"just align: $file has invalid managed markers; no files were changed.\" >&2; exit 1; }; done",
        "replace() { source=$1; destination=$2; awk -v replacement=\"$source\" '/<!-- socket-managed:begin/ { while ((getline line < replacement) > 0) { print line; if (line ~ /<!-- socket-managed:end/) break }; in_managed=1; next } in_managed { if (/<!-- socket-managed:end/) in_managed=0; next } { print }' \"$destination\" > \"$tmp/out\"; mv \"$tmp/out\" \"$destination\"; }",
        "replace \"$tmp/AGENTS-root.md\" AGENTS.md", "replace \"$tmp/AGENTS-apps.md\" Apps/AGENTS.md", "replace \"$tmp/AGENTS-packages.md\" Packages/AGENTS.md", "replace \"$tmp/CONTRIBUTING.md\" CONTRIBUTING.md",
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
    docs = (("AGENTS-root.md", root / "AGENTS.md"), ("AGENTS-apps.md", root / "Apps/AGENTS.md"), ("AGENTS-packages.md", root / "Packages/AGENTS.md"), ("CONTRIBUTING.md", root / "CONTRIBUTING.md"))
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
    includes = ["  - path: Apps/apps-shared.yml\n    relativePaths: false", "  - path: Packages/packages-shared.yml\n    relativePaths: false"]
    includes.extend(f"  - path: Apps/{name}{SUPPORTED_PLATFORMS[platform]}/target.yml\n    relativePaths: false" for platform in platforms)
    return "\n".join([
        f"name: {name}", "include:", *includes, "options:",
        "  minimumXcodeGenVersion: 2.46.0", "  projectFormat: xcode16_3", "  defaultConfig: Debug",
        "  defaultSourceDirectoryType: syncedFolder", "  schemePathPrefix: ../", "  localPackagesGroup: Packages",
        "  deploymentTarget:", "    iOS: \"26.1\"", "    macOS: \"26.1\"", "    tvOS: \"26.1\"", "    watchOS: \"26.1\"", "    visionOS: \"26.1\"",
        "configs:", *(f"  {config}: {'debug' if config == 'Debug' else 'release'}" for config in CONFIGURATIONS), "configFiles:",
        *(f"  {config}: Configurations/{config}.xcconfig" for config in CONFIGURATIONS),
        "fileGroups:", "  - Apps", "  - Packages", "  - Configurations", "  - Scripts", "  - docs", "",
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


def target_spec(name: str, platform: str, prefix: str, org: str, team: str) -> str:
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
      - package: {name}Core
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
    if platform in {"ios", "visionos"}: channels.append(("AltStore", "AltStore"))
    if platform == "macos": channels.append(("Direct Distribution", "DirectDistribution"))
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


def install(root: Path, name: str, prefix: str, platforms: list[str], org: str, team: str) -> None:
    write(root / "project.yml", root_spec(name, platforms))
    write(root / "Apps/apps-shared.yml", app_shared_spec())
    write(root / "Apps/Apps-shared.xcconfig", "#include \"../Configurations/Project.xcconfig\"\nASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES\nLOCALIZATION_PREFERS_STRING_CATALOGS = YES\nSTRING_CATALOG_GENERATE_SYMBOLS = YES\n")
    write(root / "Packages/packages-shared.yml", package_spec(name))
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
    write(root / "Justfile", (root / "Justfile").read_text(encoding="utf-8") + "\nvalidate:\n  sh Scripts/validate.sh\npackage-test:\n  for manifest in Packages/*/Package.swift; do (cd \"$(dirname \"$manifest\")\" && swift test); done\ntest target:\n  xcodebuild -workspace *.xcworkspace -scheme \"{{target}}\" test\narchive target channel:\n  sh Scripts/release.sh \"{{target}}\" \"{{channel}}\"\napp-store target:\n  sh Scripts/release.sh \"{{target}}\" app-store\naltstore target:\n  sh Scripts/release.sh \"{{target}}\" altstore\ndirect-distribution target:\n  sh Scripts/release.sh \"{{target}}\" direct-distribution\n")
    write(root / "Scripts/increment-build-version.sh", "#!/usr/bin/env sh\nset -eu\ntarget=${1:?target required}; configuration=${2:?configuration required}; label=$(printf '%s' \"$configuration\" | tr '[:upper:]' '[:lower:]')\nfile=\"Apps/$target/Configurations/Version.xcconfig\"\ngit rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo \"Build counter requires a Git repository.\" >&2; exit 1; }\n[ \"$configuration\" = Debug ] && key=DEBUG_BUILD_NUMBER || key=RELEASE_BUILD_NUMBER\nvalue=$(awk -F ' = ' -v key=\"$key\" '$1 == key { print $2 }' \"$file\")\n[ -n \"$value\" ] || { echo \"Missing $key in $file\" >&2; exit 1; }\nawk -F ' = ' -v key=\"$key\" -v next=$((value + 1)) 'BEGIN { OFS = \" = \" } $1 == key { $2 = next } { print }' \"$file\" > \"$file.tmp\" && mv \"$file.tmp\" \"$file\"\nstaged=false; unstaged=false; git diff --cached --quiet || staged=true; git diff --quiet || unstaged=true\nif $staged && $unstaged; then git add \"$file\"; echo \"warning: staged build counter update; commit it manually as soon as possible.\" >&2; exit 0; fi\nif $staged; then patch=$(mktemp); git diff --cached --binary > \"$patch\"; git restore --staged :/; git add \"$file\"; git commit -m \"build: increment $target $label build\"; git apply --cached \"$patch\"; rm -f \"$patch\"; else git add \"$file\"; git commit -m \"build: increment $target $label build\"; fi\n", True)
    write(root / "Scripts/validate.sh", "#!/usr/bin/env sh\nset -eu\nswiftformat --lint --config .swiftformat Apps Packages\nswiftlint lint --config .swiftlint.yml --force-exclude Apps Packages\nxcodegen generate --spec project.yml\nworkspace=$(find . -maxdepth 1 -type d -name '*.xcworkspace' -print -quit)\nxcodebuild -list -workspace \"$workspace\"\nfor manifest in Packages/*/Package.swift; do (cd \"$(dirname \"$manifest\")\" && swift test); done\n", True)
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
            if config == "Debug": content += "ONLY_ACTIVE_ARCH = YES\n"
            else: content += "SWIFT_OPTIMIZATION_LEVEL = -O\n"
            write(app_root / f"Configurations/{config}.xcconfig", content)
        write(app_root / f"Sources/{prefix}App.swift", f'import SwiftUI\n\n@main\nstruct {prefix}{display}App: App {{\n    var body: some Scene {{ WindowGroup {{ Text("{target}") }} }}\n}}\n')
        write(app_root / "Sources/Views/.gitkeep", "")
        write(app_root / "Sources/Datamodels/.gitkeep", "")
        write(app_root / "Sources/Services/.gitkeep", "")
        write(app_root / "Resources/Info.plist", f'<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>CFBundleShortVersionString</key><string>$(MARKETING_VERSION)</string><key>CFBundleVersion</key><string>$(CURRENT_PROJECT_VERSION)</string></dict></plist>\n')
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
    root = Path(args.repo_root).expanduser().resolve() if args.operation == "align" and args.repo_root else ((Path(args.destination).expanduser() / args.name).resolve() if args.name else Path(args.destination).expanduser().resolve())
    inputs = {"operation": args.operation, "name": args.name, "file_prefix": args.file_prefix, "destination": args.destination, "repo_root": args.repo_root, "platforms": platforms, "org_identifier": args.org_identifier, "development_team": args.development_team, "dry_run": args.dry_run, "skip_validation": args.skip_validation}
    if args.operation == "align":
        if not args.repo_root:
            return blocked("--repo-root is required with --operation align.", inputs)
        if not args.dry_run and not shutil.which("xcodegen"):
            return blocked("XcodeGen is required to regenerate an aligned workspace.", inputs)
        findings = workspace_findings(root) if root.is_dir() else ["The requested workspace root is not a directory."]
        if findings:
            return blocked(" ".join(findings), inputs)
        try:
            actions = install_alignment_runtime(root, args.dry_run)
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
    if not platforms or any(platform not in SUPPORTED_PLATFORMS for platform in platforms):
        return blocked("--platforms must be a comma-separated subset of ios,macos,tvos,watchos,visionos.", inputs)
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        return blocked("The product root already contains files; use --operation align --repo-root <existing-root> for a canonical workspace.", inputs)
    xcodegen = shutil.which("xcodegen")
    if not xcodegen:
        return blocked("XcodeGen is required to create the root generated project.", inputs)
    payload: dict[str, object] = {"status": "success", "path_type": "primary", "workspace_root": str(root), "workspace_path": str(root / f"{args.name}.xcworkspace"), "project_path": str(root / f"{args.name}.xcodeproj"), "normalized_inputs": inputs, "actions": ["create one root XcodeGen project", "create Apps/ target fragments and shared templates", "create Packages/ local Swift package", "create root workspace wrapper"]}
    if args.dry_run:
        payload["validation_result"] = "skipped (--dry-run)"
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    root.mkdir(parents=True)
    try:
        install(root, args.name, args.file_prefix, platforms, args.org_identifier, args.development_team)
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
