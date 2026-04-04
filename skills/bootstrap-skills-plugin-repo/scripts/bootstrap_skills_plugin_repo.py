from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


EXACT_NO_FINDINGS = "No findings."


@dataclass
class Finding:
    path: str
    issue_id: str
    message: str


def infer_plugin_name(repo_root: Path, explicit: str | None) -> str:
    return explicit or repo_root.name


def _pretty_slug(name: str) -> str:
    return name.replace("-", " ").title()


def expected_files(repo_root: Path, plugin_name: str) -> dict[Path, str]:
    plugin_root = repo_root / "plugins" / plugin_name
    plugin_title = _pretty_slug(plugin_name)
    return {
        repo_root / ".gitignore": (
            ".venv/\n"
            "__pycache__/\n"
            ".pytest_cache/\n"
            "*.pyc\n"
            "\n"
            "# Agent plugin repo local runtime state\n"
            ".codex/plugins/\n"
            ".codex/plugins/**\n"
            ".claude/settings.local.json\n"
            ".claude/local-settings.json\n"
            ".claude/.local/\n"
        ),
        repo_root / "README.md": (
            f"# {repo_root.name}\n\n"
            f"Canonical skill repository with plugin packaging under `plugins/{plugin_name}/`.\n\n"
            "## Codex Local Plugin Surfaces\n\n"
            f"- Repo-local packaged plugin surface: `plugins/{plugin_name}/`\n"
            "- Repo-local marketplace surface: `.agents/plugins/marketplace.json`\n"
            f"- Personal Codex installs live outside the repo at `~/.codex/plugins/{plugin_name}` with `~/.agents/plugins/marketplace.json`\n\n"
            "## Claude Plugin Surfaces\n\n"
            f"- Local Claude development should load the tracked plugin source directly with `claude --plugin-dir /absolute/path/to/plugins/{plugin_name}`\n"
            "- If this repo should be shareable as a Claude marketplace, track `.claude-plugin/marketplace.json` at the repo root\n\n"
            "## Git Tracking Guidance\n\n"
            "- Track canonical plugin source trees and shared marketplace catalogs in git.\n"
            "- Do not track consumer-side install copies, caches, or local-only runtime state.\n\n"
            "## Maintainer Python Tooling\n\n"
            "```bash\n"
            "uv sync --dev\n"
            "uv tool install ruff\n"
            "uv tool install mypy\n"
            "uv run --group dev pytest\n"
            "```\n"
        ),
        repo_root / "AGENTS.md": (
            "# AGENTS.md\n\n"
            "Use root `skills/` as the canonical authored skill surface.\n"
            f"Keep plugin packaging metadata under `plugins/{plugin_name}/`.\n"
            "Keep repo-local Codex marketplace wiring under `.agents/plugins/marketplace.json`.\n"
            f"Document personal Codex installs separately at `~/.codex/plugins/{plugin_name}` with `~/.agents/plugins/marketplace.json`.\n"
            "If the repo itself is meant to be addable as a Claude marketplace, keep `.claude-plugin/marketplace.json` at the repo root.\n"
            "Use POSIX symlink mirrors for `.agents/skills` and `.claude/skills`.\n"
            "Track shared marketplace catalogs and canonical plugin sources in git.\n"
            "Ignore local install copies, caches, and local-only runtime settings.\n"
            "Keep `ruff` and `mypy` available as `uv`-managed tools by default.\n"
        ),
        repo_root / "ROADMAP.md": "# Project Roadmap\n\n## Milestone Progress\n\n- [ ] Milestone 0: Foundation\n",
        repo_root / "docs" / "maintainers" / "reality-audit.md": (
            "# Repo Reality Audit\n\n"
            "Root `skills/` is canonical. Plugin metadata lives under `plugins/`.\n"
            "Shared marketplace catalogs belong in git when the repo is itself a distribution surface.\n"
            "Maintainer Python tooling should keep `ruff` and `mypy` installed via `uv tool install`.\n"
        ),
        repo_root / "docs" / "maintainers" / "workflow-atlas.md": (
            "# Workflow Atlas\n\n"
            "Bootstrap repos first, then author individual skills.\n"
            "Track shared marketplace catalogs and canonical plugin sources in git.\n"
            "After bootstrap, install `ruff` and `mypy` with `uv tool install` before regular validation work.\n"
        ),
        plugin_root / ".codex-plugin" / "plugin.json": json.dumps(
            {
                "name": plugin_name,
                "version": "0.0.0-local",
                "description": f"{plugin_title} plugin scaffold.",
                "skills": "./skills/",
                "interface": {
                    "displayName": plugin_title,
                    "shortDescription": f"{plugin_title} plugin scaffold.",
                    "category": "Productivity",
                },
            },
            indent=2,
        )
        + "\n",
        plugin_root / ".claude-plugin" / "plugin.json": json.dumps(
            {
                "name": plugin_name,
                "description": f"{plugin_title} plugin scaffold.",
                "version": "0.0.0",
            },
            indent=2,
        )
        + "\n",
        repo_root / ".claude-plugin" / "marketplace.json": json.dumps(
            {
                "name": plugin_name,
                "owner": {"name": plugin_title},
                "plugins": [
                    {
                        "name": plugin_name,
                        "source": f"./plugins/{plugin_name}",
                        "description": f"{plugin_title} plugin scaffold.",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        plugin_root / "hooks" / "hooks.json": json.dumps({"hooks": {}}, indent=2) + "\n",
        repo_root / ".agents" / "plugins" / "marketplace.json": json.dumps(
            {
                "name": f"{plugin_name}-local",
                "interface": {"displayName": f"{plugin_title} Local Plugins"},
                "plugins": [
                    {
                        "name": plugin_name,
                        "source": {"source": "local", "path": f"./plugins/{plugin_name}"},
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Productivity",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
    }


def expected_symlinks(repo_root: Path, plugin_name: str) -> dict[Path, str]:
    return {
        repo_root / ".agents" / "skills": "../skills",
        repo_root / ".claude" / "skills": "../skills",
        repo_root / "plugins" / plugin_name / "skills": "../../skills",
    }


def audit_repo(repo_root: Path, plugin_name: str) -> list[Finding]:
    findings: list[Finding] = []
    for path in expected_files(repo_root, plugin_name):
        if not path.exists():
            findings.append(
                Finding(str(path.relative_to(repo_root)), "missing-path", "Required bootstrap path is missing.")
            )
    for path, target in expected_symlinks(repo_root, plugin_name).items():
        rel = str(path.relative_to(repo_root))
        if not path.exists() and not path.is_symlink():
            findings.append(Finding(rel, "missing-symlink", f"Expected symlink to {target}."))
            continue
        if not path.is_symlink():
            findings.append(Finding(rel, "not-symlink", f"Expected POSIX symlink to {target}."))
            continue
        actual_target = os.readlink(path)
        if actual_target != target:
            findings.append(Finding(rel, "wrong-symlink-target", f"Expected {target}, found {actual_target}."))
    return findings


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def apply_repo(repo_root: Path, plugin_name: str) -> tuple[list[dict[str, str]], list[str]]:
    actions: list[dict[str, str]] = []
    created_paths: list[str] = []
    for path, content in expected_files(repo_root, plugin_name).items():
        if path.exists():
            continue
        _ensure_parent(path)
        path.write_text(content, encoding="utf-8")
        actions.append({"action": "create-file", "path": str(path.relative_to(repo_root))})
        created_paths.append(str(path.relative_to(repo_root)))
    for directory in [
        repo_root / "skills",
        repo_root / "plugins",
        repo_root / "plugins" / plugin_name / "assets",
        repo_root / "plugins" / plugin_name / "bin",
    ]:
        if directory.exists():
            continue
        directory.mkdir(parents=True, exist_ok=True)
        actions.append({"action": "create-dir", "path": str(directory.relative_to(repo_root))})
        created_paths.append(str(directory.relative_to(repo_root)))
    for path, target in expected_symlinks(repo_root, plugin_name).items():
        if path.is_symlink() and os.readlink(path) == target:
            continue
        if path.exists() and not path.is_symlink():
            actions.append(
                {
                    "action": "skip-existing-path",
                    "path": str(path.relative_to(repo_root)),
                    "reason": "Existing non-symlink path must be reviewed manually.",
                }
            )
            continue
        _ensure_parent(path)
        if path.is_symlink():
            path.unlink()
        os.symlink(target, path)
        actions.append({"action": "create-symlink", "path": str(path.relative_to(repo_root)), "target": target})
        created_paths.append(str(path.relative_to(repo_root)))
    return actions, created_paths


def build_report(repo_root: Path, plugin_name: str, run_mode: str, findings: list[Finding], apply_actions: list[dict[str, str]], created_paths: list[str], errors: list[str]) -> dict[str, object]:
    return {
        "run_context": {
            "repo_root": str(repo_root),
            "plugin_name": plugin_name,
            "run_mode": run_mode,
        },
        "findings": [asdict(item) for item in findings],
        "apply_actions": apply_actions,
        "created_paths": created_paths,
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--run-mode", choices=("check-only", "apply"), required=True)
    parser.add_argument("--plugin-name")
    parser.add_argument("--print-md", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        print("Repository root does not exist or is not a directory.", file=os.sys.stderr)
        return 1
    plugin_name = infer_plugin_name(repo_root, args.plugin_name)
    errors: list[str] = []
    findings = audit_repo(repo_root, plugin_name)
    apply_actions: list[dict[str, str]] = []
    created_paths: list[str] = []
    if args.run_mode == "apply":
        apply_actions, created_paths = apply_repo(repo_root, plugin_name)
        findings = audit_repo(repo_root, plugin_name)
    report = build_report(repo_root, plugin_name, args.run_mode, findings, apply_actions, created_paths, errors)
    if args.print_md and not findings and not apply_actions and not errors:
        print(EXACT_NO_FINDINGS)
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
