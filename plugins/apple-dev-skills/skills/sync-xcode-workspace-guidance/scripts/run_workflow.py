#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Audit and sync root guidance for an Apps/Packages Xcode workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def discover(root: Path) -> dict:
    workspaces = sorted(root.glob("*.xcworkspace"))
    projects = sorted(root.glob("*.xcodeproj"))
    packages = sorted(path.parent for path in (root / "Packages").glob("**/Package.swift")) if (root / "Packages").is_dir() else []
    target_specs = sorted((root / "Apps").glob("**/target.y*ml")) if (root / "Apps").is_dir() else []
    services = sorted(path for path in (root / "Services").iterdir() if path.is_dir()) if (root / "Services").is_dir() else []
    return {
        "workspaces": [str(path) for path in workspaces],
        "root_projects": [str(path) for path in projects],
        "packages": [str(path) for path in packages],
        "target_specs": [str(path) for path in target_specs],
        "services": [str(path) for path in services],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).expanduser().resolve()
    state = discover(root) if root.is_dir() else {key: [] for key in ("workspaces", "root_projects", "packages", "target_specs", "services")}
    findings = []
    if not root.is_dir():
        findings.append("The requested workspace root is not a directory.")
    if len(state["workspaces"]) != 1:
        findings.append("Expected exactly one root .xcworkspace before workspace guidance can be synced.")
    if not (root / "Apps").is_dir():
        findings.append("Expected an Apps/ directory for target specs.")
    elif not (root / "Apps" / "apps-shared.yml").is_file():
        findings.append("Expected Apps/apps-shared.yml for common XcodeGen target templates.")
    elif not (root / "Apps" / "Apps-shared.xcconfig").is_file():
        findings.append("Expected Apps/Apps-shared.xcconfig for shared app build settings.")
    elif not state["target_specs"]:
        findings.append("Expected at least one target.yml under Apps/.")
    if not (root / "Packages").is_dir():
        findings.append("Expected a Packages/ directory for local Swift packages.")
    elif not state["packages"]:
        findings.append("Expected at least one Package.swift under Packages/.")
    elif not (root / "Packages" / "packages-shared.yml").is_file():
        findings.append("Expected Packages/packages-shared.yml for local-package registration.")
    if not (root / "project.yml").is_file():
        findings.append("Expected root project.yml.")
    if len(state["root_projects"]) != 1:
        findings.append("Expected exactly one generated root .xcodeproj.")
    status = "success" if not findings else "blocked"
    actions = ["report root XcodeGen composition, target specs, package registration, and configuration layers"]
    payload: dict[str, object] = {
        "status": status,
        "path_type": "fallback" if args.dry_run else "primary",
        "repo_root": str(root),
        "detected_state": state,
        "findings": findings,
        "actions": actions,
        "next_step": "Refresh root project.yml, included target specs, and package manifests through their owning sources, then regenerate with XcodeGen.",
    }
    agents_path = root / "AGENTS.md"
    section = (Path(__file__).resolve().parents[1] / "assets" / "append-section.md").read_text(encoding="utf-8")
    if status == "success":
        if not agents_path.exists():
            actions.append("create root AGENTS.md with workspace guidance")
            if not args.dry_run:
                agents_path.write_text("# AGENTS.md\n\n" + section, encoding="utf-8")
        elif not agents_path.is_file():
            payload.update(status="blocked", findings=[*findings, "AGENTS.md exists but is not a regular file."])
        elif "## Apple / Xcode Workspace Workflow" not in agents_path.read_text(encoding="utf-8"):
            actions.append("append bounded workspace guidance to root AGENTS.md")
            if not args.dry_run:
                with agents_path.open("a", encoding="utf-8") as handle:
                    handle.write("\n" + section)
        else:
            actions.append("preserve existing root workspace guidance")
    status = str(payload["status"])
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
