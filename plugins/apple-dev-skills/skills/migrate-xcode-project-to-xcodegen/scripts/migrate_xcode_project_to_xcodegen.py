#!/usr/bin/env python3
"""Audit an Xcode app project before migrating or modernizing XcodeGen."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


XCConfig_OWNER_SETTINGS = {
    "ASSETCATALOG_COMPILER_APPICON_NAME",
    "ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS",
    "CODE_SIGN_ENTITLEMENTS",
    "CURRENT_PROJECT_VERSION",
    "DEAD_CODE_STRIPPING",
    "ENABLE_APP_SANDBOX",
    "ENABLE_HARDENED_RUNTIME",
    "ENABLE_USER_SCRIPT_SANDBOXING",
    "MARKETING_VERSION",
    "PRODUCT_BUNDLE_IDENTIFIER",
    "SWIFT_APPROACHABLE_CONCURRENCY",
    "SWIFT_STRICT_CONCURRENCY",
    "SWIFT_VERSION",
}

BASELINE_PROJECT_YML_NEEDLES = {
    "default_source_directory_type": "defaultSourceDirectoryType: syncedFolder",
    "synced_folder_sources": "type: syncedFolder",
    "config_files": "configFiles:",
    "resources_root": "Sources/Resources",
    "app_entitlements": "Sources/Support/App.entitlements",
    "version_marketing": "CFBundleShortVersionString: $(MARKETING_VERSION)",
    "version_build": "CFBundleVersion: $(CURRENT_PROJECT_VERSION)",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def sorted_relative(paths: list[Path], root: Path) -> list[str]:
    return sorted(rel(path, root) for path in paths)


def find_first(root: Path, pattern: str) -> Path | None:
    matches = sorted(root.rglob(pattern), key=lambda item: str(item))
    return matches[0] if matches else None


def discover_project_files(repo_root: Path, project_path: str | None, project_yml: str | None) -> dict[str, Any]:
    explicit_project = Path(project_path).expanduser() if project_path else None
    if explicit_project and not explicit_project.is_absolute():
        explicit_project = repo_root / explicit_project

    explicit_yml = Path(project_yml).expanduser() if project_yml else None
    if explicit_yml and not explicit_yml.is_absolute():
        explicit_yml = repo_root / explicit_yml

    projects = [
        explicit_project
    ] if explicit_project and explicit_project.exists() and explicit_project.suffix == ".xcodeproj" else []
    workspaces = [
        explicit_project
    ] if explicit_project and explicit_project.exists() and explicit_project.suffix == ".xcworkspace" else []

    if not projects:
        projects = sorted(repo_root.rglob("*.xcodeproj"), key=lambda item: str(item))
    if not workspaces:
        workspaces = sorted(repo_root.rglob("*.xcworkspace"), key=lambda item: str(item))

    yml = explicit_yml if explicit_yml and explicit_yml.exists() else repo_root / "project.yml"
    if not yml.exists():
        yml = find_first(repo_root, "project.yml")

    project = projects[0] if projects else None
    pbxproj = project / "project.pbxproj" if project else None
    if pbxproj and not pbxproj.exists():
        pbxproj = None

    return {
        "projects": sorted_relative(projects, repo_root),
        "workspaces": sorted_relative(workspaces, repo_root),
        "project": rel(project, repo_root) if project else None,
        "workspace": rel(workspaces[0], repo_root) if workspaces else None,
        "pbxproj": rel(pbxproj, repo_root) if pbxproj else None,
        "project_yml": rel(yml, repo_root) if yml and yml.exists() else None,
    }


def extract_pbxproj_settings(pbxproj_text: str) -> list[str]:
    keys = set(re.findall(r"\b([A-Z][A-Z0-9_]+)\s*=", pbxproj_text))
    return sorted(keys & XCConfig_OWNER_SETTINGS)


def extract_pbxproj_target_names(pbxproj_text: str) -> list[str]:
    names = set(re.findall(r"isa = PBXNativeTarget;[\s\S]{0,500}?name = ([^;]+);", pbxproj_text))
    cleaned = {name.strip().strip('"') for name in names if name.strip()}
    return sorted(cleaned)


def audit_project_yml(project_yml_path: Path | None) -> dict[str, Any]:
    if not project_yml_path or not project_yml_path.exists():
        return {
            "present": False,
            "baseline_gaps": sorted(BASELINE_PROJECT_YML_NEEDLES),
        }

    text = read_text(project_yml_path)
    gaps = [name for name, needle in BASELINE_PROJECT_YML_NEEDLES.items() if needle not in text]
    return {
        "present": True,
        "path": str(project_yml_path),
        "baseline_gaps": sorted(gaps),
        "uses_synced_folder": "syncedFolder" in text,
        "uses_config_files": "configFiles:" in text,
        "declares_minimum_xcodegen": "minimumXcodeGenVersion:" in text,
    }


def audit_files(repo_root: Path) -> dict[str, Any]:
    xcconfigs = sorted(repo_root.rglob("*.xcconfig"), key=lambda item: str(item))
    entitlements = sorted(repo_root.rglob("*.entitlements"), key=lambda item: str(item))
    info_plists = sorted(path for path in repo_root.rglob("Info.plist") if path.is_file())
    asset_catalogs = sorted(repo_root.rglob("*.xcassets"), key=lambda item: str(item))
    schemes = sorted(repo_root.rglob("*.xcscheme"), key=lambda item: str(item))
    test_plans = sorted(repo_root.rglob("*.xctestplan"), key=lambda item: str(item))
    return {
        "xcconfigs": sorted_relative(xcconfigs, repo_root),
        "entitlements": sorted_relative(entitlements, repo_root),
        "info_plists": sorted_relative(info_plists, repo_root),
        "asset_catalogs": sorted_relative(asset_catalogs, repo_root),
        "schemes": sorted_relative(schemes, repo_root),
        "test_plans": sorted_relative(test_plans, repo_root),
        "has_default_app_entitlements": (repo_root / "Sources/Support/App.entitlements").exists(),
        "has_default_assets": (repo_root / "Sources/Resources/Assets.xcassets").exists(),
    }


def choose_path(mode: str, discovered: dict[str, Any]) -> tuple[str | None, str | None]:
    has_project_yml = bool(discovered["project_yml"])
    has_xcode_project = bool(discovered["project"] or discovered["workspace"])

    if mode == "xcode-managed":
        if not has_xcode_project:
            return None, "requested xcode-managed migration but no .xcodeproj or .xcworkspace was found"
        return "xcode-managed-to-xcodegen", None
    if mode == "xcodegen-modernize":
        if not has_project_yml:
            return None, "requested XcodeGen modernization but no project.yml was found"
        return "modernize-xcodegen", None
    if has_project_yml:
        return "modernize-xcodegen", None
    if has_xcode_project:
        return "xcode-managed-to-xcodegen", None
    return None, "no .xcodeproj, .xcworkspace, or project.yml was found"


def build_recommendations(
    migration_path: str,
    project_yml_audit: dict[str, Any],
    file_audit: dict[str, Any],
    pbxproj_settings: list[str],
) -> list[str]:
    recommendations = [
        "Review tracked .pbxproj diffs and treat them as intentional project state before generating.",
        "Create or update project.yml only after target, source, resource, package, scheme, and test-plan state is inventoried.",
        "Run xcodegen generate in a reviewed branch or temp clone, then compare generated build settings before replacing project state.",
    ]

    if migration_path == "xcode-managed-to-xcodegen":
        recommendations.insert(1, "Create the XcodeGen scaffold from the current project inventory instead of starting from an empty template.")

    if project_yml_audit["baseline_gaps"]:
        recommendations.append("Update project.yml for current baseline gaps: " + ", ".join(project_yml_audit["baseline_gaps"]) + ".")
    if pbxproj_settings:
        recommendations.append("Promote pbxproj build settings into .xcconfig owners: " + ", ".join(pbxproj_settings) + ".")
    if not file_audit["xcconfigs"]:
        recommendations.append("Add checked-in Configurations/*.xcconfig layers before preserving build settings.")
    if not file_audit["has_default_app_entitlements"]:
        recommendations.append("Add Sources/Support/App.entitlements and wire CODE_SIGN_ENTITLEMENTS through the app .xcconfig.")
    if not file_audit["has_default_assets"]:
        recommendations.append("Add Sources/Resources/Assets.xcassets with AppIcon and AccentColor placeholders.")
    return recommendations


def build_validation_commands(discovered: dict[str, Any]) -> list[str]:
    project_arg = ""
    if discovered["workspace"]:
        project_arg = f"-workspace {discovered['workspace']}"
    elif discovered["project"]:
        project_arg = f"-project {discovered['project']}"

    commands = ["xcodegen generate", f"xcodebuild {project_arg} -list".strip()]
    commands.append(f"xcodebuild {project_arg} -scheme <Scheme> -showBuildSettings".strip())
    commands.append(f"xcodebuild {project_arg} -scheme <Scheme> -configuration Debug build".strip())
    return commands


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--project-path")
    parser.add_argument("--project-yml")
    parser.add_argument("--mode", choices=("auto", "xcode-managed", "xcodegen-modernize"), default="auto")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        payload = {
            "status": "blocked",
            "path_type": "fallback",
            "output": {
                "repo_root": str(repo_root),
                "reason": "repo_root_missing_or_not_directory",
                "next_step": "Pass --repo-root pointing at an existing Xcode app repository.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    discovered = discover_project_files(repo_root, args.project_path, args.project_yml)
    migration_path, block_reason = choose_path(args.mode, discovered)
    if block_reason:
        payload = {
            "status": "blocked",
            "path_type": "fallback",
            "output": {
                "repo_root": str(repo_root),
                "mode": args.mode,
                "discovered": discovered,
                "reason": block_reason,
                "next_step": "Pass an explicit --project-path or --project-yml, or use the bootstrap skill for a new app.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    pbxproj_path = repo_root / discovered["pbxproj"] if discovered["pbxproj"] else None
    pbxproj_text = read_text(pbxproj_path) if pbxproj_path else ""
    project_yml_path = repo_root / discovered["project_yml"] if discovered["project_yml"] else None
    project_yml_audit = audit_project_yml(project_yml_path)
    file_audit = audit_files(repo_root)
    pbxproj_settings = extract_pbxproj_settings(pbxproj_text)

    output = {
        "repo_root": str(repo_root),
        "mode": args.mode,
        "dry_run": bool(args.dry_run),
        "migration_path": migration_path,
        "discovered": discovered,
        "project_yml_audit": project_yml_audit,
        "file_audit": file_audit,
        "pbxproj_audit": {
            "present": bool(pbxproj_path),
            "target_names": extract_pbxproj_target_names(pbxproj_text),
            "settings_to_promote": pbxproj_settings,
        },
        "recommended_phases": build_recommendations(migration_path or "", project_yml_audit, file_audit, pbxproj_settings),
        "validation_commands": build_validation_commands(discovered),
        "next_step": "Review the audit, promote intentional project state into tracked files, then regenerate and compare.",
    }
    payload = {"status": "success", "path_type": "primary", "output": output}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
