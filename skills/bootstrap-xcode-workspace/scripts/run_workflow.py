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
    result.add_argument("--name", required=True)
    result.add_argument("--file-prefix", default="APP")
    result.add_argument("--destination", default=".")
    result.add_argument("--platforms", default="ios,macos")
    result.add_argument("--org-identifier", default="com.galewilliams")
    result.add_argument("--development-team", default="BC73766F69")
    result.add_argument("--dry-run", action="store_true")
    result.add_argument("--skip-validation", action="store_true")
    return result


def blocked(message: str, inputs: dict[str, object]) -> int:
    print(json.dumps({"status": "blocked", "path_type": "primary", "normalized_inputs": inputs, "stderr": message}, indent=2, sort_keys=True))
    return 1


def root_spec(name: str, platforms: list[str]) -> str:
    includes = ["  - path: Apps/apps-shared.yml\n    relativePaths: false", "  - path: Packages/packages-shared.yml\n    relativePaths: false"]
    includes.extend(f"  - path: Apps/{name}{SUPPORTED_PLATFORMS[platform]}/target.yml\n    relativePaths: false" for platform in platforms)
    return "\n".join([
        f"name: {name}", "include:", *includes, "options:",
        "  minimumXcodeGenVersion: 2.46.0", "  projectFormat: xcode16_3", "  defaultConfig: Debug",
        "  defaultSourceDirectoryType: syncedFolder", "  schemePathPrefix: ../", "  localPackagesGroup: Packages",
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
    configFiles:
      Debug: Apps/{target}Tests/Configurations/Debug.xcconfig
      Staging: Apps/{target}Tests/Configurations/Staging.xcconfig
      Release: Apps/{target}Tests/Configurations/Release.xcconfig
      AppStore: Apps/{target}Tests/Configurations/AppStore.xcconfig
      DirectDistribution: Apps/{target}Tests/Configurations/DirectDistribution.xcconfig
      AltStore: Apps/{target}Tests/Configurations/AltStore.xcconfig
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
    configFiles:
      Debug: Apps/{target}UITests/Configurations/Debug.xcconfig
      Staging: Apps/{target}UITests/Configurations/Staging.xcconfig
      Release: Apps/{target}UITests/Configurations/Release.xcconfig
      AppStore: Apps/{target}UITests/Configurations/AppStore.xcconfig
      DirectDistribution: Apps/{target}UITests/Configurations/DirectDistribution.xcconfig
      AltStore: Apps/{target}UITests/Configurations/AltStore.xcconfig
schemes:
  {target} UI Tests:
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
    build:
      targets: {{ {target}: all }}
    test:
      config: Debug
      targets:
        - name: {target}Tests
          parallelizable: true
  {target} All Tests:
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
    for source, destination in (("AGENTS-root.md", "AGENTS.md"), ("AGENTS-apps.md", "Apps/AGENTS.md"), ("AGENTS-packages.md", "Packages/AGENTS.md"), ("CONTRIBUTING.md", "CONTRIBUTING.md"), ("pre-commit", ".githooks/pre-commit")):
        write(root / destination, (Path(__file__).resolve().parents[1] / "assets" / "managed-guidance" / source).read_text(encoding="utf-8"), destination.endswith("pre-commit"))
    write(root / "Justfile", "set shell := [\"sh\", \"-eu\", \"-c\"]\n\nsetup:\n  sh Scripts/setup.sh\nalign:\n  sh Scripts/align.sh\nvalidate:\n  sh Scripts/validate.sh\npackage-test:\n  for manifest in Packages/*/Package.swift; do (cd \"$(dirname \"$manifest\")\" && swift test); done\ntest target:\n  xcodebuild -workspace *.xcworkspace -scheme \"{{target}}\" test\narchive target channel:\n  sh Scripts/release.sh \"{{target}}\" \"{{channel}}\"\napp-store target:\n  sh Scripts/release.sh \"{{target}}\" app-store\naltstore target:\n  sh Scripts/release.sh \"{{target}}\" altstore\ndirect-distribution target:\n  sh Scripts/release.sh \"{{target}}\" direct-distribution\n")
    write(root / "Scripts/setup.sh", "#!/usr/bin/env sh\nset -eu\nfor tool in git just swift xcodegen xcodebuild; do command -v \"$tool\" >/dev/null 2>&1 || { echo \"Missing required tool: $tool\" >&2; exit 1; }; done\ngit config core.hooksPath .githooks\n", True)
    write(root / "Scripts/align.sh", "#!/usr/bin/env sh\nset -eu\nbase=${SOCKET_TEMPLATE_BASE_URL:-https://raw.githubusercontent.com/gaelic-ghost/socket/main/plugins/apple-dev-skills/skills/bootstrap-xcode-workspace/assets/managed-guidance}\ntmp=$(mktemp -d)\ntrap 'rm -r \"$tmp\"' EXIT HUP INT TERM\nfor file in AGENTS-root.md AGENTS-apps.md AGENTS-packages.md CONTRIBUTING.md pre-commit; do curl --fail --silent --show-error \"$base/$file\" -o \"$tmp/$file\"; done\nfor file in AGENTS-root.md AGENTS-apps.md AGENTS-packages.md CONTRIBUTING.md; do grep -q 'socket-managed:begin' \"$tmp/$file\"; done\n[ -s \"$tmp/pre-commit\" ]\nreplace() { source=$1; destination=$2; grep -q 'socket-managed:begin' \"$destination\"; awk -v replacement=\"$source\" '/<!-- socket-managed:begin/ { while ((getline line < replacement) > 0) print line; in_managed=1; next } in_managed { if (/<!-- socket-managed:end/) in_managed=0; next } { print }' \"$destination\" > \"$tmp/out\"; mv \"$tmp/out\" \"$destination\"; }\nreplace \"$tmp/AGENTS-root.md\" AGENTS.md\nreplace \"$tmp/AGENTS-apps.md\" Apps/AGENTS.md\nreplace \"$tmp/AGENTS-packages.md\" Packages/AGENTS.md\nreplace \"$tmp/CONTRIBUTING.md\" CONTRIBUTING.md\ncp \"$tmp/pre-commit\" .githooks/pre-commit\nchmod +x .githooks/pre-commit\ngit config core.hooksPath .githooks\nxcodegen generate --spec project.yml\n", True)
    write(root / "Scripts/increment-build-version.sh", "#!/usr/bin/env sh\nset -eu\ntarget=${1:?target required}; configuration=${2:?configuration required}; label=$(printf '%s' \"$configuration\" | tr '[:upper:]' '[:lower:]')\nfile=\"Apps/$target/Configurations/Version.xcconfig\"\n[ \"$configuration\" = Debug ] && key=DEBUG_BUILD_NUMBER || key=RELEASE_BUILD_NUMBER\nvalue=$(awk -F ' = ' -v key=\"$key\" '$1 == key { print $2 }' \"$file\")\n[ -n \"$value\" ] || { echo \"Missing $key in $file\" >&2; exit 1; }\nawk -F ' = ' -v key=\"$key\" -v next=$((value + 1)) 'BEGIN { OFS = \" = \" } $1 == key { $2 = next } { print }' \"$file\" > \"$file.tmp\" && mv \"$file.tmp\" \"$file\"\ngit rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo \"Build counter requires a Git repository.\" >&2; exit 1; }\nstaged=false; unstaged=false; git diff --cached --quiet || staged=true; git diff --quiet || unstaged=true\nif $staged && $unstaged; then git add \"$file\"; echo \"warning: staged build counter update; commit it manually as soon as possible.\" >&2; exit 0; fi\nif $staged; then patch=$(mktemp); git diff --cached --binary > \"$patch\"; git restore --staged :/; git add \"$file\"; git commit -m \"build: increment $target $label build\"; git apply --cached \"$patch\"; rm -f \"$patch\"; else git add \"$file\"; git commit -m \"build: increment $target $label build\"; fi\n", True)
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
        for config in CONFIGURATIONS:
            write(tests_root / f"Configurations/{config}.xcconfig", '#include "../../Apps-shared.xcconfig"\nSWIFT_DEFAULT_ACTOR_ISOLATION = MainActor\n')
        write(tests_root / f"Sources/{target}Tests.swift", f'import Testing\n@testable import {target}\n\n@Test func example() {{ #expect(true) }}\n')
        if platform != "watchos":
            ui_root = root / "Apps" / f"{target}UITests"
            for config in CONFIGURATIONS:
                write(ui_root / f"Configurations/{config}.xcconfig", '#include "../../Apps-shared.xcconfig"\nSWIFT_DEFAULT_ACTOR_ISOLATION = MainActor\n')
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
    root = (Path(args.destination).expanduser() / args.name).resolve()
    inputs = {"name": args.name, "file_prefix": args.file_prefix, "destination": args.destination, "platforms": platforms, "org_identifier": args.org_identifier, "development_team": args.development_team, "dry_run": args.dry_run, "skip_validation": args.skip_validation}
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", args.name):
        return blocked("--name must be an alphanumeric Swift/Xcode identifier beginning with a letter.", inputs)
    if not re.fullmatch(r"[A-Z]{3}", args.file_prefix):
        return blocked("--file-prefix must contain exactly three uppercase ASCII letters.", inputs)
    if not platforms or any(platform not in SUPPORTED_PLATFORMS for platform in platforms):
        return blocked("--platforms must be a comma-separated subset of ios,macos,tvos,watchos,visionos.", inputs)
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        return blocked("The product root already contains files; use sync-xcode-workspace-guidance for an existing product.", inputs)
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
