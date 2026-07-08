#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Synchronize baseline repo guidance for an existing Xcode app repository."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


REQUIRED_STRINGS = [
    "xcode-build-run-workflow",
    "xcode-testing-workflow",
    "sync-xcode-project-guidance",
    "Never edit `.pbxproj` files directly.",
    "treat that diff as critical project state",
    "Scripts/repo-maintenance/validate-all.sh",
    "Scripts/repo-maintenance/sync-shared.sh",
    "Scripts/repo-maintenance/release.sh",
    "Sources/Views/Shared",
    "Sources/Services/Internal",
    "WhateverNameApp+ViewModel.swift",
    "<ViewName>+Controller.swift",
]

REQUIRED_XCODE_APP_DIRECTORIES = [
    "Sources/Views/Shared",
    "Sources/Views/macOS",
    "Sources/Views/iOS",
    "Sources/Models",
    "Sources/Services/Consumed",
    "Sources/Services/Internal",
    "Sources/Services/Provided",
]


def version_sort_key(path: Path) -> tuple[int, ...]:
    parts = []
    for component in path.name.split("."):
        try:
            parts.append(int(component))
        except ValueError:
            parts.append(-1)
    return tuple(parts)


def discover_xcode_state(repo_root: Path) -> dict:
    workspaces = sorted(str(path) for path in repo_root.rglob("*.xcworkspace"))
    projects = sorted(str(path) for path in repo_root.rglob("*.xcodeproj"))
    return {
        "workspace": workspaces[0] if workspaces else None,
        "project": projects[0] if projects else None,
        "is_xcode_repo": bool(workspaces or projects),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--workspace-path")
    parser.add_argument("--append-section", action="store_true")
    parser.add_argument("--copy-agents-template", action="store_true")
    parser.add_argument("--skip-validation", action="store_true")
    return parser


def read_asset(name: str) -> str:
    return (Path(__file__).resolve().parents[1] / "assets" / name).read_text(encoding="utf-8").rstrip() + "\n"


def local_environment_scheme_name(detected_state: dict, workspace_path: str | None) -> str:
    if workspace_path:
        return Path(workspace_path).stem
    for key in ("workspace", "project"):
        value = detected_state.get(key)
        if value:
            return Path(value).stem
    return "SCHEME_NAME"


def install_local_environment(repo_root: Path, detected_state: dict, workspace_path: str | None) -> str:
    template_path = (
        Path(__file__).resolve().parents[3]
        / "templates"
        / "codex-local-environments"
        / "xcode-project.toml"
    )
    target_path = repo_root / ".codex" / "environments" / "xcode-project.toml"

    if not template_path.is_file():
        raise RuntimeError(f"Codex local environment template is missing: {template_path}")
    if target_path.exists() and not target_path.is_file():
        raise RuntimeError(f"Codex local environment target exists but is not a regular file: {target_path}")

    scheme_name = local_environment_scheme_name(detected_state, workspace_path)
    template_text = template_path.read_text(encoding="utf-8").replace("SCHEME_NAME", scheme_name)
    if not target_path.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(template_text, encoding="utf-8")
        return f"installed .codex/environments/xcode-project.toml from template with scheme {scheme_name}"
    if target_path.read_text(encoding="utf-8") == template_text:
        return "left matching .codex/environments/xcode-project.toml unchanged"
    return "preserved existing .codex/environments/xcode-project.toml because it differs from the template"


def maintain_project_repo_runner() -> Path:
    script_path = Path(__file__).resolve()
    candidate_paths: list[Path] = []
    seen: set[Path] = set()

    def add_candidate(path: Path) -> None:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            candidate_paths.append(resolved)

    for root in script_path.parents:
        add_candidate(root / "productivity-skills" / "skills" / "maintain-project-repo" / "scripts" / "run_workflow.py")
        versioned_plugin_root = root / "productivity-skills"
        if versioned_plugin_root.is_dir():
            for version_dir in sorted(versioned_plugin_root.iterdir(), key=version_sort_key, reverse=True):
                add_candidate(
                    version_dir / "skills" / "maintain-project-repo" / "scripts" / "run_workflow.py"
                )

    for runner in candidate_paths:
        if runner.is_file():
            return runner

    expected = candidate_paths[0] if candidate_paths else script_path
    searched = "\n".join(f"- {path}" for path in candidate_paths)
    if not searched:
        searched = "- no candidate paths were generated"
    raise RuntimeError(
        "sync-xcode-project-guidance needs productivity-skills/maintain-project-repo "
        f"to refresh repo-maintenance files, but no runner was found. First expected path: {expected}. "
        "Searched candidate paths:\n"
        f"{searched}\n"
        "Install productivity-skills alongside apple-dev-skills, or add the socket "
        "marketplace with 'codex plugin marketplace add gaelic-ghost/socket' and "
        "enable both apple-dev-skills and productivity-skills from the Socket catalog, "
        "then rerun this workflow."
    )


def validate_agents(text: str) -> tuple[bool, list[str]]:
    missing = [needle for needle in REQUIRED_STRINGS if needle not in text]
    return not missing, missing


def audit_xcode_app_structure(repo_root: Path) -> dict:
    findings: list[dict[str, str]] = []

    for relative_path in REQUIRED_XCODE_APP_DIRECTORIES:
        if not (repo_root / relative_path).is_dir():
            findings.append(
                {
                    "code": "missing-directory",
                    "path": relative_path,
                    "message": f"Expected Xcode app structure directory is missing: {relative_path}",
                }
            )

    controllers_dir = repo_root / "Sources" / "Controllers"
    if controllers_dir.exists():
        findings.append(
            {
                "code": "legacy-controllers-directory",
                "path": "Sources/Controllers",
                "message": "Move UIKit/AppKit controller files beside their matching view under Sources/Views as <ViewName>+Controller.swift.",
            }
        )

    sources_dir = repo_root / "Sources"
    if sources_dir.is_dir():
        for view_model_path in sorted(sources_dir.rglob("*ViewModel.swift")):
            if view_model_path.name.endswith("+ViewModel.swift"):
                continue
            relative_path = view_model_path.relative_to(repo_root).as_posix()
            findings.append(
                {
                    "code": "unpaired-view-model-file",
                    "path": relative_path,
                    "message": "View model files should be paired with their owning app or view as <Owner>+ViewModel.swift or <ViewName>+Model.swift.",
                }
            )

        for model_path in sorted(sources_dir.rglob("*+Model.swift")):
            if "Sources/Views/" not in model_path.relative_to(repo_root).as_posix():
                relative_path = model_path.relative_to(repo_root).as_posix()
                findings.append(
                    {
                        "code": "view-model-outside-views",
                        "path": relative_path,
                        "message": "View-local <ViewName>+Model.swift files should live beside their matching view under Sources/Views.",
                    }
                )

        for controller_path in sorted(sources_dir.rglob("*+Controller.swift")):
            if "Sources/Views/" not in controller_path.relative_to(repo_root).as_posix():
                relative_path = controller_path.relative_to(repo_root).as_posix()
                findings.append(
                    {
                        "code": "controller-outside-views",
                        "path": relative_path,
                        "message": "UIKit/AppKit <ViewName>+Controller.swift files should live beside their matching view under Sources/Views.",
                    }
                )

        app_files = [
            path for path in sorted(sources_dir.glob("*App.swift"))
            if path.is_file() and not path.name.endswith("+ViewModel.swift")
        ]
        for app_path in app_files:
            paired_model = app_path.with_name(f"{app_path.stem}+ViewModel.swift")
            if not paired_model.is_file():
                relative_path = paired_model.relative_to(repo_root).as_posix()
                findings.append(
                    {
                        "code": "missing-app-view-model",
                        "path": relative_path,
                        "message": "App-wide @Observable state should live beside the app entry point as <AppName>App+ViewModel.swift.",
                    }
                )

        internal_services_dir = repo_root / "Sources" / "Services" / "Internal"
        if app_files and internal_services_dir.is_dir():
            service_files = sorted(internal_services_dir.glob("*AppService.swift"))
            if not service_files:
                findings.append(
                    {
                        "code": "missing-internal-app-service",
                        "path": "Sources/Services/Internal",
                        "message": "When the app has a main app-wide service, place it under Sources/Services/Internal as <AppName>AppService.swift.",
                    }
                )

    return {
        "status": "passed" if not findings else "needs-attention",
        "findings": findings,
    }


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    agents_path = repo_root / "AGENTS.md"
    detected_state = discover_xcode_state(repo_root)
    structure_audit = audit_xcode_app_structure(repo_root)
    actions: list[str] = []

    if not detected_state["is_xcode_repo"]:
        payload = {
            "status": "blocked",
            "path_type": "primary",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "validation_result": None,
            "structure_audit": structure_audit,
            "actions": actions,
            "stderr": "The repository does not contain an .xcodeproj or .xcworkspace marker.",
            "next_step": "Run this workflow on an existing Xcode app repo.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if agents_path.exists() and not agents_path.is_file():
        payload = {
            "status": "blocked",
            "path_type": "primary",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "validation_result": None,
            "structure_audit": structure_audit,
            "actions": actions,
            "stderr": "The target AGENTS.md path exists but is not a regular file.",
            "next_step": "Resolve the AGENTS.md path conflict and rerun the workflow.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if not agents_path.exists():
        if not args.copy_agents_template:
            payload = {
                "status": "blocked",
                "path_type": "primary",
                "repo_root": str(repo_root),
                "agents_path": str(agents_path),
                "detected_state": detected_state,
                "validation_result": None,
                "structure_audit": structure_audit,
                "actions": actions,
                "stderr": "AGENTS.md is missing and template copy is disabled.",
                "next_step": "Enable template copy or create AGENTS.md manually before rerunning.",
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1
        agents_path.write_text(read_asset("AGENTS.md"), encoding="utf-8")
        actions.append("created AGENTS.md from template")
    else:
        current = agents_path.read_text(encoding="utf-8")
        if "## Apple / Xcode Project Workflow" in current:
            actions.append("left existing AGENTS.md unchanged")
        elif args.append_section:
            appended = current.rstrip() + "\n\n" + read_asset("append-section.md")
            agents_path.write_text(appended, encoding="utf-8")
            actions.append("appended the bounded Xcode guidance section to AGENTS.md")
        else:
            payload = {
                "status": "blocked",
                "path_type": "primary",
                "repo_root": str(repo_root),
                "agents_path": str(agents_path),
                "detected_state": detected_state,
                "validation_result": None,
                "structure_audit": structure_audit,
                "actions": actions,
                "stderr": "AGENTS.md exists but the bounded Xcode guidance section is missing and append behavior is disabled.",
                "next_step": "Enable append behavior or merge the guidance section manually before rerunning.",
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

    validation_result = "skipped (--skip-validation)"
    if not args.skip_validation:
        text = agents_path.read_text(encoding="utf-8")
        is_valid, missing = validate_agents(text)
        if not is_valid:
            payload = {
                "status": "failed",
                "path_type": "primary",
                "repo_root": str(repo_root),
                "agents_path": str(agents_path),
                "detected_state": detected_state,
                "validation_result": "failed",
                "structure_audit": structure_audit,
                "actions": actions,
                "stderr": f"Synced AGENTS.md is missing required guidance: {', '.join(missing)}",
                "next_step": "Fix the guidance template or section content, then rerun the workflow.",
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1
        validation_result = "validated"

    try:
        actions.append(install_local_environment(repo_root, detected_state, args.workspace_path))
    except RuntimeError as exc:
        payload = {
            "status": "failed",
            "path_type": "primary",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "validation_result": validation_result,
            "structure_audit": structure_audit,
            "actions": actions,
            "stderr": str(exc),
            "next_step": "Resolve the Codex local environment template or target path issue, then rerun sync-xcode-project-guidance.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    try:
        runner = maintain_project_repo_runner()
    except RuntimeError as exc:
        payload = {
            "status": "failed",
            "path_type": "primary",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "validation_result": validation_result,
            "structure_audit": structure_audit,
            "actions": actions,
            "stderr": str(exc),
            "next_step": "Install productivity-skills alongside apple-dev-skills, or add the socket marketplace and enable both plugin entries from the Socket catalog, then rerun sync-xcode-project-guidance.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    proc_install_toolkit = subprocess.run(
        [
            str(runner),
            "--repo-root",
            str(repo_root),
            "--operation",
            "refresh",
            "--profile",
            "xcode-app",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc_install_toolkit.returncode != 0:
        payload = {
            "status": "failed",
            "path_type": "primary",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "validation_result": validation_result,
            "structure_audit": structure_audit,
            "actions": actions,
            "stdout": proc_install_toolkit.stdout,
            "stderr": proc_install_toolkit.stderr,
            "next_step": "Fix the maintain-project-repo refresh failure and rerun the workflow.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1
    actions.append("refreshed maintain-project-repo with the xcode-app profile")

    payload = {
        "status": "success",
        "path_type": "primary",
        "repo_root": str(repo_root),
        "agents_path": str(agents_path),
        "detected_state": detected_state,
        "validation_result": validation_result,
        "structure_audit": structure_audit,
        "actions": actions,
        "next_step": "Use xcode-build-run-workflow for active Xcode build or run work, use xcode-testing-workflow for test-focused work, and rerun sync-xcode-project-guidance after substantial plugin updates.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
