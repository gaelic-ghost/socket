#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Synchronize baseline repo guidance for an existing Swift package repository."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


REQUIRED_STRINGS = [
    "bootstrap-swift-package",
    "sync-swift-package-guidance",
    "swift-package-build-run-workflow",
    "swift-package-testing-workflow",
    "swift build",
    "swift test",
    "scripts/repo-maintenance/validate-all.sh",
    "scripts/repo-maintenance/sync-shared.sh",
    "scripts/repo-maintenance/release.sh",
    "swift-configuration",
    "Reloading",
    "YAML",
]

IGNORED_XCODE_MARKER_PARTS = {".build", ".swiftpm"}


def version_sort_key(path: Path) -> tuple[int, ...]:
    parts = []
    for component in path.name.split("."):
        try:
            parts.append(int(component))
        except ValueError:
            parts.append(-1)
    return tuple(parts)


def is_generated_xcode_marker(repo_root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(repo_root)
    except ValueError:
        return False
    return any(part in IGNORED_XCODE_MARKER_PARTS for part in relative.parts)


def discover_repo_state(repo_root: Path) -> dict:
    workspaces = sorted(
        str(path)
        for path in repo_root.rglob("*.xcworkspace")
        if not is_generated_xcode_marker(repo_root, path)
    )
    projects = sorted(
        str(path)
        for path in repo_root.rglob("*.xcodeproj")
        if not is_generated_xcode_marker(repo_root, path)
    )
    return {
        "package_manifest": str(repo_root / "Package.swift") if (repo_root / "Package.swift").exists() else None,
        "workspace": workspaces[0] if workspaces else None,
        "project": projects[0] if projects else None,
        "is_package_repo": (repo_root / "Package.swift").exists(),
        "is_ambiguous_repo": (repo_root / "Package.swift").exists() and bool(workspaces or projects),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--append-section", action="store_true")
    parser.add_argument("--copy-agents-template", action="store_true")
    parser.add_argument("--skip-validation", action="store_true")
    return parser


def read_asset(name: str) -> str:
    return (Path(__file__).resolve().parents[1] / "assets" / name).read_text(encoding="utf-8").rstrip() + "\n"


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
        "sync-swift-package-guidance needs productivity-skills/maintain-project-repo "
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


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    agents_path = repo_root / "AGENTS.md"
    detected_state = discover_repo_state(repo_root)
    actions: list[str] = []

    if not detected_state["is_package_repo"]:
        payload = {
            "status": "blocked",
            "path_type": "primary",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "validation_result": None,
            "actions": actions,
            "stderr": "The repository does not contain a Package.swift manifest at the requested root.",
            "next_step": "Run this workflow on an existing Swift package repo.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if detected_state["is_ambiguous_repo"]:
        payload = {
            "status": "blocked",
            "path_type": "primary",
            "repo_root": str(repo_root),
            "agents_path": str(agents_path),
            "detected_state": detected_state,
            "validation_result": None,
            "actions": actions,
            "stderr": "The requested repo root contains both Package.swift and Xcode app markers, so the guidance boundary is ambiguous.",
            "next_step": "Choose the plain Swift package root explicitly, or use the Xcode guidance-sync workflow instead.",
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
        if "## Swift Package Workflow" in current:
            actions.append("left existing AGENTS.md unchanged")
        elif args.append_section:
            appended = current.rstrip() + "\n\n" + read_asset("append-section.md")
            agents_path.write_text(appended, encoding="utf-8")
            actions.append("appended the bounded Swift package guidance section to AGENTS.md")
        else:
            payload = {
                "status": "blocked",
                "path_type": "primary",
                "repo_root": str(repo_root),
                "agents_path": str(agents_path),
                "detected_state": detected_state,
                "validation_result": None,
                "actions": actions,
                "stderr": "AGENTS.md exists but the bounded Swift package guidance section is missing and append behavior is disabled.",
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
                "actions": actions,
                "stderr": f"Synced AGENTS.md is missing required guidance: {', '.join(missing)}",
                "next_step": "Fix the guidance template or section content, then rerun the workflow.",
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1
        validation_result = "validated"

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
            "actions": actions,
            "stderr": str(exc),
            "next_step": "Install productivity-skills alongside apple-dev-skills, or add the socket marketplace and enable both plugin entries from the Socket catalog, then rerun sync-swift-package-guidance.",
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
            "swift-package",
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
            "actions": actions,
            "stdout": proc_install_toolkit.stdout,
            "stderr": proc_install_toolkit.stderr,
            "next_step": "Fix the maintain-project-repo refresh failure and rerun the workflow.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1
    actions.append("refreshed maintain-project-repo with the swift-package profile")

    payload = {
        "status": "success",
        "path_type": "primary",
        "repo_root": str(repo_root),
        "agents_path": str(agents_path),
        "detected_state": detected_state,
        "validation_result": validation_result,
        "actions": actions,
        "next_step": "Use swift-package-build-run-workflow or swift-package-testing-workflow for ordinary package work, rerun sync-swift-package-guidance after substantial plugin updates, and use xcode-build-run-workflow or xcode-testing-workflow only when package work needs Xcode-managed tooling.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
