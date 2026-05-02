#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
from __future__ import annotations

import argparse
import json
import os
import sys
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


def expected_files(repo_root: Path, _plugin_name: str) -> dict[Path, str]:
    return {
        repo_root / ".gitignore": """.venv/
__pycache__/
.pytest_cache/
*.pyc
.claude/settings.local.json
.claude/local-settings.json
.claude/.local/
""",
        repo_root / "README.md": f"# {repo_root.name}\n\nInstallable maintainer skills for skills-export repositories.\n",
        repo_root / "AGENTS.md": """# AGENTS.md

Root `skills/` is canonical.

Default user-facing Codex plugin install and update guidance to Git-backed marketplace sources with `codex plugin marketplace add <owner>/<repo>` and `codex plugin marketplace upgrade <marketplace-name>`. Explicit refs such as `<owner>/<repo>@vX.Y.Z` are for pinned reproducible installs. Manual local marketplace roots and copied plugin payloads are development, unpublished-testing, or fallback paths.

Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch.

Do not commit dependency declarations, lockfiles, scripts, docs, examples, generated project files, or CI config that point at machine-local paths such as `/Users/...`, `~/...`, `../...`, local worktrees, or private checkout paths.

Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly. If local integration is needed, keep it uncommitted or convert it to a tagged release, branch, or registry dependency before sharing.
""",
        repo_root / "ROADMAP.md": "# Project Roadmap\n\n## Vision\n\n- Define the long-term outcome for this skills-export repository.\n",
        repo_root / "docs" / "maintainers" / "reality-audit.md": "# Repo Reality Audit\n\nRoot `skills/` is canonical.\n",
        repo_root / "docs" / "maintainers" / "workflow-atlas.md": "# Workflow Atlas\n\nBootstrap repos first, then author individual skills.\n",
    }


def expected_symlinks(repo_root: Path, _plugin_name: str) -> dict[Path, str]:
    return {
        repo_root / ".agents" / "skills": "../skills",
        repo_root / ".claude" / "skills": "../skills",
    }


def audit_repo(repo_root: Path, plugin_name: str) -> list[Finding]:
    findings: list[Finding] = []
    for path in expected_files(repo_root, plugin_name):
        if not path.exists():
            findings.append(Finding(str(path.relative_to(repo_root)), "missing-path", "Required bootstrap path is missing."))
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
    if (repo_root / "plugins").exists():
        findings.append(Finding("plugins", "forbidden-path", "Nested plugin directories are forbidden for this repo model."))
    if (repo_root / ".agents" / "plugins" / "marketplace.json").exists():
        findings.append(
            Finding(
                ".agents/plugins/marketplace.json",
                "forbidden-path",
                "Repo marketplace files are forbidden for this repo model.",
            )
        )
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
    for directory in [repo_root / "skills", repo_root / "docs" / "maintainers"]:
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
        "run_context": {"repo_root": str(repo_root), "plugin_name": plugin_name, "run_mode": run_mode},
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
        print("Repository root does not exist or is not a directory.", file=sys.stderr)
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
