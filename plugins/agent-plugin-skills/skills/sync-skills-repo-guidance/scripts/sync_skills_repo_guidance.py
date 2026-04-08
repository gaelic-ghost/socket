from __future__ import annotations

import argparse
import json
import os
import filecmp
from dataclasses import asdict, dataclass
from pathlib import Path


EXACT_NO_FINDINGS = "No findings."

README_SNIPPETS = [
    "root `skills/` as the canonical",
    "bundled copy of root",
    "plugins/",
    ".agents/plugins/marketplace.json",
    "~/.codex/plugins/",
    "restart Codex",
    "codex-tui.log",
    "/plugins",
    ".claude-plugin/marketplace.json",
    "claude --plugin-dir",
    "Track canonical plugin source trees and shared marketplace catalogs in git.",
    "OpenAI Codex Skills",
    "Claude Code Plugins",
    "uv tool install ruff",
    "uv tool install mypy",
]

AGENTS_SNIPPETS = [
    "canonical workflow-authoring surface",
    "real bundled directory",
    "plugin packaging root",
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    "Track canonical plugin source trees and shared marketplace catalogs in git.",
    "uv-managed tools",
]

AUDIT_SNIPPETS = [
    "Root `skills/` is the canonical workflow-authoring surface.",
    "real bundled directory",
    ".claude-plugin/marketplace.json",
    "plugin packaging root",
    "uv tool install",
]

GITIGNORE_SNIPPETS = [
    "# Agent plugin repo local runtime state",
    ".codex/plugins/",
    ".claude/settings.local.json",
]


@dataclass
class Finding:
    path: str
    issue_id: str
    message: str


def infer_plugin_name(repo_root: Path, explicit: str | None) -> str:
    return explicit or repo_root.name


def _check_file_contains(repo_root: Path, path: Path, snippets: list[str], issue_prefix: str) -> list[Finding]:
    findings: list[Finding] = []
    if not path.exists():
        findings.append(Finding(str(path.relative_to(repo_root)), "missing-path", "Expected repo guidance file is missing."))
        return findings
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            findings.append(
                Finding(
                    str(path.relative_to(repo_root)),
                    f"{issue_prefix}-missing-snippet",
                    f"Expected to mention: {snippet}",
                )
            )
    return findings


def _check_symlink(repo_root: Path, path: Path, target: str) -> list[Finding]:
    rel = str(path.relative_to(repo_root))
    if not path.exists() and not path.is_symlink():
        return [Finding(rel, "missing-symlink", f"Expected symlink to {target}.")]
    if not path.is_symlink():
        return [Finding(rel, "not-symlink", f"Expected POSIX symlink to {target}.")]
    actual = os.readlink(path)
    if actual != target:
        return [Finding(rel, "wrong-symlink-target", f"Expected {target}, found {actual}.")]
    return []


def _compare_directory_trees(source: Path, target: Path, prefix: str = "") -> list[str]:
    comparison = filecmp.dircmp(source, target)
    mismatches: list[str] = []
    for name in sorted(comparison.left_only):
        mismatches.append(f"missing bundled entry `{prefix}{name}`")
    for name in sorted(comparison.right_only):
        mismatches.append(f"unexpected bundled entry `{prefix}{name}`")
    _matches, mismatch, errors = filecmp.cmpfiles(source, target, comparison.common_files, shallow=False)
    for name in sorted(mismatch):
        mismatches.append(f"content differs for `{prefix}{name}`")
    for name in sorted(errors):
        mismatches.append(f"comparison failed for `{prefix}{name}`")
    for name in sorted(comparison.common_dirs):
        mismatches.extend(_compare_directory_trees(source / name, target / name, prefix=f"{prefix}{name}/"))
    return mismatches


def _check_packaged_skills(repo_root: Path, plugin_name: str) -> list[Finding]:
    source = repo_root / "skills"
    target = repo_root / "plugins" / plugin_name / "skills"
    rel = str(target.relative_to(repo_root))
    if not target.exists() and not target.is_symlink():
        return [Finding(rel, "missing-packaged-skills-dir", "Expected bundled plugin `skills/` directory.")]
    if target.is_symlink():
        return [Finding(rel, "packaged-skills-is-symlink", "Expected a real bundled plugin `skills/` directory, not a symlink.")]
    if not target.is_dir():
        return [Finding(rel, "packaged-skills-not-directory", "Expected bundled plugin `skills/` path to be a directory.")]
    if source.is_dir():
        mismatches = _compare_directory_trees(source, target)
        if mismatches:
            preview = "; ".join(mismatches[:5])
            if len(mismatches) > 5:
                preview += f"; plus {len(mismatches) - 5} more"
            return [Finding(rel, "packaged-skills-drift", f"Bundled plugin `skills/` directory is out of sync with root `skills/`: {preview}.")]
    return []


def audit_repo(repo_root: Path, plugin_name: str) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_check_file_contains(repo_root, repo_root / "README.md", README_SNIPPETS, "readme"))
    findings.extend(_check_file_contains(repo_root, repo_root / "AGENTS.md", AGENTS_SNIPPETS, "agents"))
    findings.extend(_check_file_contains(repo_root, repo_root / ".gitignore", GITIGNORE_SNIPPETS, "gitignore"))
    findings.extend(
        _check_file_contains(
            repo_root,
            repo_root / ".claude-plugin" / "marketplace.json",
            [plugin_name, f"./plugins/{plugin_name}"],
            "claude-marketplace",
        )
    )
    findings.extend(
        _check_file_contains(
            repo_root,
            repo_root / "docs" / "maintainers" / "reality-audit.md",
            AUDIT_SNIPPETS,
            "reality-audit",
        )
    )
    findings.extend(_check_symlink(repo_root, repo_root / ".agents" / "skills", "../skills"))
    findings.extend(_check_symlink(repo_root, repo_root / ".claude" / "skills", "../skills"))
    findings.extend(_check_packaged_skills(repo_root, plugin_name))
    return findings


def build_report(repo_root: Path, plugin_name: str, run_mode: str, findings: list[Finding], errors: list[str]) -> dict[str, object]:
    return {
        "run_context": {
            "repo_root": str(repo_root),
            "plugin_name": plugin_name,
            "run_mode": run_mode,
        },
        "findings": [asdict(item) for item in findings],
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
    findings = audit_repo(repo_root, plugin_name)
    errors: list[str] = []
    report = build_report(repo_root, plugin_name, args.run_mode, findings, errors)
    if args.print_md and not findings and not errors:
        print(EXACT_NO_FINDINGS)
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
