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
    projects = sorted((root / "Apps").glob("**/*.xcodeproj")) if (root / "Apps").is_dir() else []
    packages = sorted(path.parent for path in (root / "Packages").glob("**/Package.swift")) if (root / "Packages").is_dir() else []
    specs = sorted((root / "Apps").glob("**/project.y*ml")) if (root / "Apps").is_dir() else []
    services = sorted(path for path in (root / "Services").iterdir() if path.is_dir()) if (root / "Services").is_dir() else []
    return {
        "workspaces": [str(path) for path in workspaces],
        "app_projects": [str(path) for path in projects],
        "packages": [str(path) for path in packages],
        "xcodegen_specs": [str(path) for path in specs],
        "services": [str(path) for path in services],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).expanduser().resolve()
    state = discover(root) if root.is_dir() else {key: [] for key in ("workspaces", "app_projects", "packages", "xcodegen_specs", "services")}
    findings = []
    if not root.is_dir():
        findings.append("The requested workspace root is not a directory.")
    if len(state["workspaces"]) != 1:
        findings.append("Expected exactly one root .xcworkspace before workspace guidance can be synced.")
    if not (root / "Apps").is_dir():
        findings.append("Expected an Apps/ directory for app projects.")
    if not (root / "Packages").is_dir():
        findings.append("Expected a Packages/ directory for local Swift packages.")
    elif not state["packages"]:
        findings.append("Expected at least one Package.swift under Packages/.")
    if (root / "Apps").is_dir() and not state["app_projects"]:
        findings.append("Expected at least one .xcodeproj under Apps/.")
    status = "success" if not findings else "blocked"
    payload = {
        "status": status,
        "path_type": "fallback" if args.dry_run else "primary",
        "repo_root": str(root),
        "detected_state": state,
        "findings": findings,
        "actions": ["report workspace-root composition and route child app/package guidance"],
        "next_step": "Use sync-xcode-project-guidance and sync-swift-package-guidance for each discovered child root.",
    }
    agents_path = root / "AGENTS.md"
    section = (Path(__file__).resolve().parents[1] / "assets" / "append-section.md").read_text(encoding="utf-8")
    if status == "success":
        if not agents_path.exists():
            payload["actions"].append("create root AGENTS.md with workspace guidance")
            if not args.dry_run:
                agents_path.write_text("# AGENTS.md\n\n" + section, encoding="utf-8")
        elif not agents_path.is_file():
            payload.update(status="blocked", findings=[*findings, "AGENTS.md exists but is not a regular file."])
        elif "## Apple / Xcode Workspace Workflow" not in agents_path.read_text(encoding="utf-8"):
            payload["actions"].append("append bounded workspace guidance to root AGENTS.md")
            if not args.dry_run:
                with agents_path.open("a", encoding="utf-8") as handle:
                    handle.write("\n" + section)
        else:
            payload["actions"].append("preserve existing root workspace guidance")
    status = payload["status"]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
