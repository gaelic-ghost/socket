from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXACT_NO_FINDINGS = "No findings."
FORBIDDEN_PATHS = [
    "plugins",
    ".agents/plugins/marketplace.json",
    ".claude-plugin/plugin.json",
    "skills/install-plugin-to-socket",
    "skills/validate-plugin-install-surfaces",
]
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".toml", ".json"}


@dataclass
class ScriptResult:
    name: str
    report: dict[str, Any] | None
    error: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit and coordinate bounded maintenance for a skills-export repository")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--workflow", choices=("audit-only", "apply-safe-fixes"), default="audit-only")
    parser.add_argument("--doc-scope", choices=("readme", "roadmap", "all"), default="all")
    parser.add_argument("--print-md", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    parser.add_argument("--fail-on-issues", action="store_true")
    return parser.parse_args()


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _skills_root() -> Path:
    return _skill_root().parent


def _repo_root(path: str) -> Path:
    return Path(path).expanduser().resolve()


def _run_json_script(name: str, script_path: Path, args: list[str]) -> ScriptResult:
    command = [sys.executable, str(script_path), *args]
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
    except OSError as exc:
        return ScriptResult(name=name, report=None, error=f"{name} could not be started: {exc}")
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    if not stdout:
        return ScriptResult(name=name, report=None, error=stderr or f"{name} returned no output.")
    try:
        report = json.loads(stdout)
    except json.JSONDecodeError:
        return ScriptResult(name=name, report=None, error=stderr or f"{name} did not return valid JSON.")
    if completed.returncode != 0:
        return ScriptResult(name=name, report=report, error=stderr or f"{name} exited with status {completed.returncode}.")
    return ScriptResult(name=name, report=report)


def run_docs(repo_root: Path, doc_scope: str, apply_fixes: bool) -> ScriptResult:
    script = _skills_root() / "maintain-plugin-docs" / "scripts" / "maintain_plugin_docs.py"
    args = ["--workspace", str(repo_root.parent), "--repo-glob", repo_root.name, "--doc-scope", doc_scope, "--print-json"]
    if apply_fixes:
        args.append("--apply-fixes")
    return _run_json_script("maintain-plugin-docs", script, args)


def audit_repo_model(repo_root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for rel in FORBIDDEN_PATHS:
        path = repo_root / rel
        if path.exists() or path.is_symlink():
            findings.append(
                {
                    "path": rel,
                    "issue_id": "forbidden-path",
                    "message": "Repository contains a forbidden nested-plugin, marketplace, or deleted-skill path.",
                }
            )
    return findings


def _count_docs_findings(report: dict[str, Any] | None) -> int:
    if not report:
        return 0
    return sum(len(report.get(key, [])) for key in ("readme_findings", "roadmap_findings", "cross_doc_findings"))


def build_report(repo_root: Path, workflow: str, doc_scope: str, repo_findings: list[dict[str, str]], docs_result: ScriptResult) -> dict[str, Any]:
    docs_report = docs_result.report or {}
    fixes_applied = list(docs_report.get("fixes_applied", []))
    errors = [docs_result.error] if docs_result.error else []
    unresolved_issues = len(repo_findings) + _count_docs_findings(docs_report)
    initial_issues = unresolved_issues
    return {
        "run_context": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "repo_root": str(repo_root),
            "doc_scope": doc_scope,
            "workflow": workflow,
        },
        "repo_root": str(repo_root),
        "workflow": workflow,
        "owner_assignments": {
            "maintain-plugin-repo": {
                "role": "repo-level audit and forbidden-contract detection",
                "finding_count": len(repo_findings),
            },
            "maintain-plugin-docs": {
                "role": "README and ROADMAP maintenance",
                "finding_count": _count_docs_findings(docs_report),
            },
        },
        "validation_findings": {"repo_model": repo_findings},
        "docs_findings": {
            "readme": docs_report.get("readme_findings", []),
            "roadmap": docs_report.get("roadmap_findings", []),
            "cross_doc": docs_report.get("cross_doc_findings", []),
        },
        "install_findings": [],
        "fixes_applied": fixes_applied,
        "deferred_findings": [],
        "post_fix_status": {
            "initial_issues": initial_issues,
            "unresolved_issues": unresolved_issues,
            "resolved_issues": 0,
        },
        "errors": errors,
    }


def summarize_markdown(report: dict[str, Any]) -> str:
    lines = [
        "## Run Context",
        f"- Repo root: {report['repo_root']}",
        f"- Workflow: {report['workflow']}",
        f"- Doc scope: {report['run_context']['doc_scope']}",
        "",
        "## Owner Assignments",
    ]
    for owner, payload in report["owner_assignments"].items():
        lines.append(f"- {owner}: {payload['role']} ({payload['finding_count']} findings)")
    lines.extend(["", "## Repo Model Findings"])
    repo_items = report["validation_findings"]["repo_model"]
    if not repo_items:
        lines.append("- None")
    else:
        for item in repo_items:
            lines.append(f"- {item['path']}: {item['message']}")
    for title, key in (("README Findings", "readme"), ("ROADMAP Findings", "roadmap"), ("Cross-Doc Findings", "cross_doc")):
        lines.extend(["", f"## {title}"])
        items = report["docs_findings"][key]
        if not items:
            lines.append("- None")
        else:
            for item in items:
                lines.append(f"- {item['doc_file']}: {item['evidence']}")
    return "\n".join(lines).strip()


def main() -> int:
    args = parse_args()
    repo_root = _repo_root(args.repo_root)
    if not repo_root.exists() or not repo_root.is_dir():
        print("Repository root does not exist or is not a directory.", file=sys.stderr)
        return 1
    repo_findings = audit_repo_model(repo_root)
    docs_result = run_docs(repo_root, args.doc_scope, args.workflow == "apply-safe-fixes")
    report = build_report(repo_root, args.workflow, args.doc_scope, repo_findings, docs_result)
    no_findings = not repo_findings and not any(report["docs_findings"].values()) and not report["fixes_applied"] and not report["errors"]
    if args.print_md and no_findings:
        print(EXACT_NO_FINDINGS)
        return 0
    if args.print_md:
        print(summarize_markdown(report))
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
