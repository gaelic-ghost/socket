from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


EXACT_NO_FINDINGS = "No findings."
FORBIDDEN_PATHS = [
    "plugins",
    ".agents/plugins/marketplace.json",
    ".claude-plugin/plugin.json",
    "skills/install-plugin-to-socket",
    "skills/validate-plugin-install-surfaces",
]
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit and coordinate bounded maintenance for a skills-export repository")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--workflow", choices=("audit-only", "apply-safe-fixes"), default="audit-only")
    parser.add_argument("--print-md", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    parser.add_argument("--fail-on-issues", action="store_true")
    return parser.parse_args()

def _repo_root(path: str) -> Path:
    return Path(path).expanduser().resolve()


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


def build_report(repo_root: Path, workflow: str, repo_findings: list[dict[str, str]]) -> dict[str, Any]:
    unresolved_issues = len(repo_findings)
    initial_issues = unresolved_issues
    return {
        "run_context": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "repo_root": str(repo_root),
            "workflow": workflow,
        },
        "repo_root": str(repo_root),
        "workflow": workflow,
        "owner_assignments": {
            "maintain-plugin-repo": {
                "role": "repo-level audit and forbidden-contract detection",
                "finding_count": len(repo_findings),
            },
        },
        "validation_findings": {"repo_model": repo_findings},
        "fixes_applied": [],
        "deferred_findings": [],
        "post_fix_status": {
            "initial_issues": initial_issues,
            "unresolved_issues": unresolved_issues,
            "resolved_issues": 0,
        },
        "errors": [],
    }


def summarize_markdown(report: dict[str, Any]) -> str:
    lines = [
        "## Run Context",
        f"- Repo root: {report['repo_root']}",
        f"- Workflow: {report['workflow']}",
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
    return "\n".join(lines).strip()


def main() -> int:
    args = parse_args()
    repo_root = _repo_root(args.repo_root)
    if not repo_root.exists() or not repo_root.is_dir():
        print("Repository root does not exist or is not a directory.", file=sys.stderr)
        return 1
    repo_findings = audit_repo_model(repo_root)
    report = build_report(repo_root, args.workflow, repo_findings)
    no_findings = not repo_findings and not report["fixes_applied"] and not report["errors"]
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
