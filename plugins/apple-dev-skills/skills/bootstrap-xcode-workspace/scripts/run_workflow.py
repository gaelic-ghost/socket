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

SUPPORTED_PLATFORMS = {"ios": "iOS", "macos": "macOS"}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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
    result.add_argument("--org-identifier", default="com.example")
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
        "  minimumXcodeGenVersion: 2.46.0", "  projectFormat: xcode16_0", "  defaultConfig: Debug",
        "  defaultSourceDirectoryType: syncedFolder", "  schemePathPrefix: ../", "  localPackagesGroup: Packages",
        "configs:", "  Debug: debug", "  Release: release", "configFiles:",
        "  Debug: Configurations/Debug.xcconfig", "  Release: Configurations/Release.xcconfig",
        "fileGroups:", "  - Apps", "  - Packages", "  - Configurations", "  - Docs", "",
    ])


def app_shared_spec() -> str:
    return """targetTemplates:
  SwiftUIApp:
    type: application
    settings:
      base:
        GENERATE_INFOPLIST_FILE: YES
        ASSETCATALOG_COMPILER_APPICON_NAME: AppIcon
  SwiftUIAppTests:
    type: bundle.unit-test
    settings:
      base:
        GENERATE_INFOPLIST_FILE: YES
schemeTemplates:
  AppScheme:
    run: { config: Debug }
    test:
      config: Debug
      gatherCoverageData: true
    archive: { config: Release }
    management: { shared: true }
"""


def package_spec(name: str) -> str:
    return f"""packages:
  {name}Core:
    path: Packages/{name}Core
"""


def target_spec(name: str, platform: str, prefix: str, org: str) -> str:
    display = SUPPORTED_PLATFORMS[platform]
    target = f"{name}{display}"
    suffix = platform if platform != "macos" else "mac"
    return f"""targets:
  {target}:
    templates: [SwiftUIApp]
    platform: {display}
    sources:
      - path: Apps/{target}/Sources
        type: syncedFolder
      - path: Apps/{target}/Resources
        type: syncedFolder
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: {org}.{name.lower()}.{suffix}
    configFiles:
      Debug: Apps/{target}/Configurations/Debug.xcconfig
      Release: Apps/{target}/Configurations/Release.xcconfig
    dependencies:
      - package: {name}Core
  {target}Tests:
    templates: [SwiftUIAppTests]
    platform: {display}
    sources:
      - path: Apps/{target}/Tests
        type: syncedFolder
    dependencies:
      - target: {target}
    configFiles:
      Debug: Apps/{target}/Configurations/Tests-Debug.xcconfig
      Release: Apps/{target}/Configurations/Tests-Release.xcconfig
schemes:
  {target}:
    templates: [AppScheme]
    build:
      targets:
        {target}: all
    test:
      targets:
        - name: {target}Tests
          parallelizable: true
"""


def install(root: Path, name: str, prefix: str, platforms: list[str], org: str) -> None:
    write(root / "project.yml", root_spec(name, platforms))
    write(root / "Apps/apps-shared.yml", app_shared_spec())
    write(root / "Apps/Apps-shared.xcconfig", "#include \"../Configurations/Project.xcconfig\"\nASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES\nLOCALIZATION_PREFERS_STRING_CATALOGS = YES\n")
    write(root / "Packages/packages-shared.yml", package_spec(name))
    write(root / "Configurations/Project.xcconfig", "SWIFT_VERSION = 6.0\nSWIFT_STRICT_CONCURRENCY = complete\n")
    write(root / "Configurations/Debug.xcconfig", '#include "Project.xcconfig"\nSWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG $(inherited)\n')
    write(root / "Configurations/Release.xcconfig", '#include "Project.xcconfig"\nSWIFT_COMPILATION_MODE = wholemodule\n')
    write(root / ".gitignore", "Build/\nDerivedData/\nxcuserdata/\n*.xcuserstate\n")
    write(root / f"{name}.xcworkspace/contents.xcworkspacedata", f'<?xml version="1.0" encoding="UTF-8"?>\n<Workspace version="1.0">\n  <FileRef location="group:{name}.xcodeproj"/>\n</Workspace>\n')
    (root / "Docs").mkdir()
    for platform in platforms:
        display = SUPPORTED_PLATFORMS[platform]
        target = f"{name}{display}"
        app_root = root / "Apps" / target
        write(app_root / "target.yml", target_spec(name, platform, prefix, org))
        write(app_root / "Configurations/App.xcconfig", '#include "../../Apps-shared.xcconfig"\n')
        write(app_root / "Configurations/Debug.xcconfig", '#include "App.xcconfig"\nONLY_ACTIVE_ARCH = YES\n')
        write(app_root / "Configurations/Release.xcconfig", '#include "App.xcconfig"\nSWIFT_OPTIMIZATION_LEVEL = -O\n')
        write(app_root / "Configurations/Tests-Debug.xcconfig", '#include "../../../Configurations/Debug.xcconfig"\nSWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG TESTING $(inherited)\n')
        write(app_root / "Configurations/Tests-Release.xcconfig", '#include "../../../Configurations/Release.xcconfig"\n')
        write(app_root / f"Sources/{prefix}App.swift", f'import SwiftUI\n\n@main\nstruct {prefix}{display}App: App {{\n    var body: some Scene {{ WindowGroup {{ Text("{target}") }} }}\n}}\n')
        write(app_root / f"Tests/{target}Tests.swift", f'import XCTest\n@testable import {target}\n\nfinal class {target}Tests: XCTestCase {{\n    func testExample() {{ XCTAssertTrue(true) }}\n}}\n')
        (app_root / "Resources/Assets.xcassets").mkdir(parents=True, exist_ok=True)
    package_root = root / "Packages" / f"{name}Core"
    package_root.mkdir(parents=True)
    subprocess.run(["swift", "package", "init", "--type", "library", "--name", f"{name}Core"], cwd=package_root, check=True, capture_output=True, text=True)


def main() -> int:
    args = parser().parse_args()
    platforms = [item.strip().lower() for item in args.platforms.split(",") if item.strip()]
    root = (Path(args.destination).expanduser() / args.name).resolve()
    inputs = {"name": args.name, "file_prefix": args.file_prefix, "destination": args.destination, "platforms": platforms, "org_identifier": args.org_identifier, "dry_run": args.dry_run, "skip_validation": args.skip_validation}
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", args.name):
        return blocked("--name must be an alphanumeric Swift/Xcode identifier beginning with a letter.", inputs)
    if not re.fullmatch(r"[A-Z]{3}", args.file_prefix):
        return blocked("--file-prefix must contain exactly three uppercase ASCII letters.", inputs)
    if not platforms or any(platform not in SUPPORTED_PLATFORMS for platform in platforms):
        return blocked("--platforms must be a comma-separated subset of ios,macos.", inputs)
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
        install(root, args.name, args.file_prefix, platforms, args.org_identifier)
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
