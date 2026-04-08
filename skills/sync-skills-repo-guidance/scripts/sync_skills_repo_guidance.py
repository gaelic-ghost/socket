from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


EXACT_NO_FINDINGS = "No findings."
README_SNIPPETS = [
    "Installable maintainer skills for skills-export repositories.",
    "OpenAI's current documented Codex plugin system is too restricted to provide proper repo-private plugin scoping.",
    "npx skills add gaelic-ghost/agent-plugin-skills --all",
    "uv tool install ruff",
    "uv tool install mypy",
]
AGENTS_SNIPPETS = [
    "Root `skills/` is the canonical authored and exported surface",
    "Do not recreate nested plugin directories",
    "Do not recreate `skills/install-plugin-to-socket` or `skills/validate-plugin-install-surfaces`",
]
AUDIT_SNIPPETS = [
    "This repository does not track a nested plugin directory for itself.",
    "This repository does not ship `install-plugin-to-socket`.",
    "This repository does not ship `validate-plugin-install-surfaces`.",
]
GITIGNORE_SNIPPETS = [".claude/settings.local.json"]
FORBIDDEN_SNIPPETS = [
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    "claude --plugin-dir",
    "~/.codex/plugins/",
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
            findings.append(Finding(str(path.relative_to(repo_root)), f"{issue_prefix}-missing-snippet", f"Expected to mention: {snippet}"))
    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in text:
            findings.append(Finding(str(path.relative_to(repo_root)), f"{issue_prefix}-forbidden-snippet", f"Forbidden snippet still present: {snippet}"))
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


def audit_repo(repo_root: Path, plugin_name: str) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_check_file_contains(repo_root, repo_root / "README.md", README_SNIPPETS, "readme"))
    findings.extend(_check_file_contains(repo_root, repo_root / "AGENTS.md", AGENTS_SNIPPETS, "agents"))
    findings.extend(_check_file_contains(repo_root, repo_root / ".gitignore", GITIGNORE_SNIPPETS, "gitignore"))
    findings.extend(_check_file_contains(repo_root, repo_root / "docs" / "maintainers" / "reality-audit.md", AUDIT_SNIPPETS, "reality-audit"))
    findings.extend(_check_symlink(repo_root, repo_root / ".agents" / "skills", "../skills"))
    findings.extend(_check_symlink(repo_root, repo_root / ".claude" / "skills", "../skills"))
    if (repo_root / "plugins").exists():
        findings.append(Finding("plugins", "forbidden-path", "Nested plugin directories are forbidden for this repo model."))
    return findings


def build_report(repo_root: Path, plugin_name: str, run_mode: str, findings: list[Finding], errors: list[str]) -> dict[str, object]:
    return {"run_context": {"repo_root": str(repo_root), "plugin_name": plugin_name, "run_mode": run_mode}, "findings": [asdict(item) for item in findings], "errors": errors}


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
    report = build_report(repo_root, plugin_name, args.run_mode, findings, [])
    if args.print_md and not findings:
        print(EXACT_NO_FINDINGS)
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
