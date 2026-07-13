#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Unified runtime entrypoint for sync-xcode-project-guidance."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import customization_config


def load_effective_config() -> dict:
    return customization_config.merge_configs(
        customization_config.load_template(),
        customization_config.load_durable(),
    )


def discover_xcode_state(repo_root: Path) -> dict:
    workspaces = sorted(str(path) for path in repo_root.rglob("*.xcworkspace"))
    projects = sorted(str(path) for path in repo_root.rglob("*.xcodeproj"))
    return {
        "workspace": workspaces[0] if workspaces else None,
        "project": projects[0] if projects else None,
        "is_xcode_repo": bool(workspaces or projects),
        "is_swift_package_only": (repo_root / "Package.swift").exists() and not bool(workspaces or projects),
    }


def audit_xcode_app_structure(repo_root: Path) -> dict:
    required_directories = [
        "Sources/Views/Shared",
        "Sources/Views/macOS",
        "Sources/Views/iOS",
        "Sources/Models",
    ]
    findings = [
        {
            "code": "missing-directory",
            "path": relative_path,
            "message": f"Expected Xcode app structure directory is missing: {relative_path}",
        }
        for relative_path in required_directories
        if not (repo_root / relative_path).is_dir()
    ]
    if (repo_root / "Sources" / "Controllers").exists():
        findings.append(
            {
                "code": "legacy-controllers-directory",
                "path": "Sources/Controllers",
                "message": "Move UIKit/AppKit controller files beside their matching view under Sources/Views with a concatenated prefixed name such as GEAWhateverViewController.swift.",
            }
        )
    default_catalog = repo_root / "Sources" / "Resources" / "Localizable.xcstrings"
    if not default_catalog.is_file():
        findings.append(
            {
                "code": "missing-default-string-catalog",
                "path": "Sources/Resources/Localizable.xcstrings",
                "message": "Add the default String Catalog through Xcode or the owning XcodeGen spec, verify target membership and resource inclusion, then build so Xcode can populate it.",
            }
        )
    return {
        "status": "passed" if not findings else "needs-attention",
        "findings": findings,
    }


def blocked_payload(
    repo_root: str,
    detected_state: dict,
    next_step: str,
    *,
    stderr: str = "",
    validation_result: str | None = None,
) -> dict:
    return {
        "status": "blocked",
        "path_type": "primary",
        "repo_root": repo_root,
        "detected_state": detected_state,
        "agents_path": str(Path(repo_root) / "AGENTS.md"),
        "validation_result": validation_result,
        "stderr": stderr,
        "actions": [],
        "next_step": next_step,
    }


def normalize_write_mode(raw: object) -> tuple[str, bool, bool, bool]:
    value = str(raw or "sync-if-needed").strip().lower()
    mapping = {
        "sync-if-needed": (True, True, False),
        "create-missing-only": (True, False, False),
        "append-existing-only": (False, True, False),
        "report-only": (False, False, True),
    }
    copy_missing, append_existing, report_only = mapping.get(value, mapping["sync-if-needed"])
    normalized = value if value in mapping else "sync-if-needed"
    return normalized, copy_missing, append_existing, report_only


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root")
    parser.add_argument("--workspace-path")
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_effective_config()
    settings = config["settings"]

    repo_root = Path(args.repo_root or ".").expanduser().resolve()
    detected_state = discover_xcode_state(repo_root)
    structure_audit = audit_xcode_app_structure(repo_root)
    agents_path = repo_root / "AGENTS.md"
    write_mode, copy_missing, append_existing, report_only = normalize_write_mode(settings.get("writeMode", "sync-if-needed"))
    normalized_inputs = {
        "repo_root": str(repo_root),
        "workspace_path": args.workspace_path,
        "skip_validation": args.skip_validation,
        "write_mode": write_mode,
        "copy_agents_template_when_missing": copy_missing,
        "append_section_when_agents_exists": append_existing,
        "report_only": report_only,
    }

    if not repo_root.exists():
        print(
            json.dumps(
                blocked_payload(
                    str(repo_root),
                    detected_state,
                    "Resolve the repository root and rerun the workflow.",
                    stderr="The requested repo root does not exist.",
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    if not repo_root.is_dir():
        print(
            json.dumps(
                blocked_payload(
                    str(repo_root),
                    detected_state,
                    "Use a directory path for --repo-root and rerun the workflow.",
                    stderr="The requested repo root is not a directory.",
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    if detected_state["is_swift_package_only"]:
        print(
            json.dumps(
                blocked_payload(
                    str(repo_root),
                    detected_state,
                    "Use sync-swift-package-guidance when it exists, or use the Swift package guidance path instead.",
                    stderr="This repository looks like a Swift package without Xcode-managed app markers.",
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    if not detected_state["is_xcode_repo"]:
        print(
            json.dumps(
                blocked_payload(
                    str(repo_root),
                    detected_state,
                    "Use bootstrap-xcode-app-project for new app creation, or rerun this skill on an existing Xcode app repo.",
                    stderr="The repository does not contain an .xcodeproj or .xcworkspace marker.",
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    actions: list[str] = []
    if not agents_path.exists():
        if normalized_inputs["copy_agents_template_when_missing"]:
            actions.append("create AGENTS.md from assets/AGENTS.md")
        elif normalized_inputs["report_only"]:
            actions.append("report that AGENTS.md is missing and would need template creation")
    elif agents_path.exists():
        text = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
        if "## Apple / Xcode Project Workflow" in text:
            actions.append("leave existing AGENTS.md unchanged")
        elif normalized_inputs["append_section_when_agents_exists"]:
            actions.append("append the bounded Xcode guidance section to AGENTS.md")
        elif normalized_inputs["report_only"]:
            actions.append("report that AGENTS.md is missing the bounded Xcode guidance section")

    local_environment_path = repo_root / ".codex" / "environments" / "xcode-project.toml"
    if local_environment_path.exists():
        actions.append("inspect existing .codex/environments/xcode-project.toml without overwriting local edits")
    else:
        actions.append("install .codex/environments/xcode-project.toml from template")

    if args.dry_run:
        payload = {
            "status": "success",
            "path_type": "fallback",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "normalized_inputs": normalized_inputs,
            "validation_result": "skipped (--dry-run)",
            "structure_audit": structure_audit,
            "actions": actions,
            "next_step": "Run without --dry-run to sync AGENTS.md guidance for this Xcode repo.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if normalized_inputs["report_only"]:
        payload = {
            "status": "success",
            "path_type": "fallback",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "normalized_inputs": normalized_inputs,
            "validation_result": "skipped (writeMode=report-only)",
            "structure_audit": structure_audit,
            "actions": actions,
            "next_step": "Rerun with a mutating write mode if you want this workflow to create or append AGENTS.md guidance.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    helper_path = Path(__file__).with_name("sync_xcode_project_guidance.py")
    command = [
        str(helper_path),
        "--repo-root",
        str(repo_root),
    ]
    if args.workspace_path:
        command.extend(["--workspace-path", args.workspace_path])
    if normalized_inputs["append_section_when_agents_exists"]:
        command.append("--append-section")
    if normalized_inputs["copy_agents_template_when_missing"]:
        command.append("--copy-agents-template")
    if args.skip_validation:
        command.append("--skip-validation")

    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    payload = json.loads(proc.stdout) if proc.stdout.strip() else {
        "status": "failed",
        "path_type": "primary",
        "repo_root": str(repo_root),
        "agents_path": str(agents_path),
        "detected_state": detected_state,
        "normalized_inputs": normalized_inputs,
        "validation_result": None,
        "actions": actions,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "next_step": "Fix the guidance-sync error and rerun the workflow.",
    }
    payload.setdefault("normalized_inputs", normalized_inputs)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
