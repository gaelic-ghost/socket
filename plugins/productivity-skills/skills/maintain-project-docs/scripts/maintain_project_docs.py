#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


SKILL_ROOT = Path(__file__).resolve().parents[1]
PRODUCTIVITY_ROOT = SKILL_ROOT.parents[1]


@dataclass(frozen=True)
class DocumentWorkflow:
    key: str
    label: str
    filename: str
    script: Path
    path_arg: str


DOCUMENT_WORKFLOWS: Tuple[DocumentWorkflow, ...] = (
    DocumentWorkflow(
        key="readme",
        label="README",
        filename="README.md",
        script=PRODUCTIVITY_ROOT / "skills/maintain-project-readme/scripts/maintain_project_readme.py",
        path_arg="--readme-path",
    ),
    DocumentWorkflow(
        key="contributing",
        label="CONTRIBUTING",
        filename="CONTRIBUTING.md",
        script=PRODUCTIVITY_ROOT / "skills/maintain-project-contributing/scripts/maintain_project_contributing.py",
        path_arg="--contributing-path",
    ),
    DocumentWorkflow(
        key="agents",
        label="AGENTS",
        filename="AGENTS.md",
        script=PRODUCTIVITY_ROOT / "skills/maintain-project-agents/scripts/maintain_project_agents.py",
        path_arg="--agents-path",
    ),
    DocumentWorkflow(
        key="accessibility",
        label="ACCESSIBILITY",
        filename="ACCESSIBILITY.md",
        script=PRODUCTIVITY_ROOT / "skills/maintain-project-accessibility/scripts/maintain_project_accessibility.py",
        path_arg="--accessibility-path",
    ),
    DocumentWorkflow(
        key="roadmap",
        label="ROADMAP",
        filename="ROADMAP.md",
        script=PRODUCTIVITY_ROOT / "skills/maintain-project-roadmap/scripts/maintain_project_roadmap.py",
        path_arg="--roadmap-path",
    ),
)

ISSUE_KEYS = (
    "schema_violations",
    "content_quality_issues",
    "command_integrity_issues",
    "workflow_drift_issues",
    "validation_drift_issues",
    "boundary_and_safety_issues",
    "claim_integrity_issues",
    "verification_evidence_issues",
    "post_fix_status",
)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a coordinated project documentation maintenance sweep.")
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--run-mode", required=True, choices=["check-only", "apply"], help="Execution mode")
    parser.add_argument("--include", help="Comma-separated document workflow keys to include")
    parser.add_argument("--skip", help="Comma-separated document workflow keys to skip")
    parser.add_argument("--json-out", help="Write JSON report path")
    parser.add_argument("--md-out", help="Write markdown report path")
    parser.add_argument("--print-json", action="store_true", help="Print JSON report")
    parser.add_argument("--print-md", action="store_true", help="Print markdown report")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit non-zero when findings remain")
    parser.add_argument(
        "--collect-source-tickets",
        action="store_true",
        help="Pass source TODO/FIXME collection through to the roadmap workflow.",
    )
    parser.add_argument(
        "--collect-github-issues",
        action="store_true",
        help="Pass GitHub issue collection through to the roadmap workflow.",
    )
    parser.add_argument("--github-repo", help="Optional OWNER/REPO override for roadmap GitHub issue collection")
    return parser.parse_args(argv)


def split_keys(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [part.strip().lower() for part in raw.split(",") if part.strip()]


def select_workflows(include: Optional[str], skip: Optional[str]) -> Tuple[List[DocumentWorkflow], List[str]]:
    known = {workflow.key: workflow for workflow in DOCUMENT_WORKFLOWS}
    errors: List[str] = []
    include_keys = split_keys(include)
    skip_keys = set(split_keys(skip))
    for key in [*include_keys, *skip_keys]:
        if key not in known:
            errors.append(f"Unknown document workflow key: {key}")
    selected = [known[key] for key in include_keys if key in known] if include_keys else list(DOCUMENT_WORKFLOWS)
    return [workflow for workflow in selected if workflow.key not in skip_keys], errors


def build_child_command(args: argparse.Namespace, workflow: DocumentWorkflow, project_root: Path) -> List[str]:
    command = [
        sys.executable,
        str(workflow.script),
        "--project-root",
        str(project_root),
        workflow.path_arg,
        str(project_root / workflow.filename),
        "--run-mode",
        args.run_mode,
        "--print-json",
    ]
    if workflow.key == "roadmap":
        if args.collect_source_tickets:
            command.append("--collect-source-tickets")
        if args.collect_github_issues:
            command.append("--collect-github-issues")
        if args.github_repo:
            command.extend(["--github-repo", args.github_repo])
    return command


def run_child(args: argparse.Namespace, workflow: DocumentWorkflow, project_root: Path) -> Dict[str, object]:
    command = build_child_command(args, workflow, project_root)
    proc = subprocess.run(command, cwd=project_root, capture_output=True, text=True, check=False)
    child: Dict[str, object] = {
        "key": workflow.key,
        "label": workflow.label,
        "path": str(project_root / workflow.filename),
        "returncode": proc.returncode,
        "report": {},
        "errors": [],
    }
    if proc.stderr.strip():
        child["stderr"] = proc.stderr.strip()
    try:
        child["report"] = json.loads(proc.stdout)
    except json.JSONDecodeError:
        child["errors"].append(f"{workflow.label} workflow did not return JSON output.")
        if proc.stdout.strip():
            child["stdout"] = proc.stdout.strip()
    if proc.returncode != 0:
        child["errors"].append(f"{workflow.label} workflow exited with status {proc.returncode}.")
    return child


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def heading_present(text: str, heading: str) -> bool:
    pattern = rf"(?im)^#+\s+{re.escape(heading)}\s*$"
    return re.search(pattern, text) is not None


def responsibility_issue(file: Path, issue_id: str, message: str, destination: str) -> Dict[str, object]:
    return {
        "issue_id": issue_id,
        "severity": "warning",
        "file": str(file),
        "message": message,
        "suggested_owner": destination,
    }


def audit_responsibility_boundaries(project_root: Path, selected: Sequence[DocumentWorkflow]) -> List[Dict[str, object]]:
    selected_keys = {workflow.key for workflow in selected}
    issues: List[Dict[str, object]] = []

    def maybe_read(key: str, filename: str) -> Tuple[Path, str]:
        path = project_root / filename
        if key not in selected_keys or not path.is_file():
            return path, ""
        return path, read_text(path)

    readme_path, readme = maybe_read("readme", "README.md")
    if readme:
        for heading in ("Contribution Workflow", "Review Expectations", "Release Process"):
            if heading_present(readme, heading):
                issues.append(
                    responsibility_issue(
                        readme_path,
                        "readme-contains-maintainer-workflow",
                        f"README.md contains a `{heading}` section; keep README product-focused and link out.",
                        "CONTRIBUTING.md or maintainer docs",
                    )
                )

    contributing_path, contributing = maybe_read("contributing", "CONTRIBUTING.md")
    if contributing:
        for heading in ("Product Principles", "Milestones", "Small Tickets"):
            if heading_present(contributing, heading):
                issues.append(
                    responsibility_issue(
                        contributing_path,
                        "contributing-contains-planning-content",
                        f"CONTRIBUTING.md contains a `{heading}` section; keep planning and backlog content in ROADMAP.md.",
                        "ROADMAP.md",
                    )
                )

    agents_path, agents = maybe_read("agents", "AGENTS.md")
    if agents:
        for heading in ("Quick Start", "Usage", "Known Gaps"):
            if heading_present(agents, heading):
                destination = "README.md" if heading in {"Quick Start", "Usage"} else "ACCESSIBILITY.md"
                issues.append(
                    responsibility_issue(
                        agents_path,
                        "agents-contains-non-agent-content",
                        f"AGENTS.md contains a `{heading}` section; keep agent guidance focused on durable operating rules.",
                        destination,
                    )
                )

    accessibility_path, accessibility = maybe_read("accessibility", "ACCESSIBILITY.md")
    if accessibility and re.search(r"(?i)\bfully compliant\b|\bguaranteed compliant\b", accessibility):
        issues.append(
            responsibility_issue(
                accessibility_path,
                "accessibility-unsupported-conformance-language",
                "ACCESSIBILITY.md uses strong conformance language that should be backed by explicit evidence.",
                "ACCESSIBILITY.md evidence section",
            )
        )

    roadmap_path, roadmap = maybe_read("roadmap", "ROADMAP.md")
    if roadmap:
        for heading in ("Contribution Workflow", "Local Setup", "Safety Boundaries"):
            if heading_present(roadmap, heading):
                destination = "CONTRIBUTING.md" if heading != "Safety Boundaries" else "AGENTS.md"
                issues.append(
                    responsibility_issue(
                        roadmap_path,
                        "roadmap-contains-procedural-guidance",
                        f"ROADMAP.md contains a `{heading}` section; keep roadmap content focused on planning.",
                        destination,
                    )
                )
    return issues


def child_issue_count(child: Dict[str, object]) -> int:
    report = child.get("report")
    if not isinstance(report, dict):
        return len(child.get("errors", []))
    return sum(len(report.get(key, [])) for key in ISSUE_KEYS if isinstance(report.get(key), list)) + len(
        child.get("errors", [])
    )


def child_fixes(child: Dict[str, object]) -> List[Dict[str, object]]:
    report = child.get("report")
    if not isinstance(report, dict):
        return []
    fixes = report.get("fixes_applied", [])
    return fixes if isinstance(fixes, list) else []


def child_post_fix_status(child: Dict[str, object]) -> List[Dict[str, object]]:
    report = child.get("report")
    if not isinstance(report, dict):
        return []
    post_fix = report.get("post_fix_status", [])
    return post_fix if isinstance(post_fix, list) else []


def markdown_report(report: Dict[str, object]) -> str:
    lines: List[str] = [
        "# Project Docs Maintenance Report",
        "",
        "## Document Workflows",
        "",
    ]
    for child in report["document_reports"]:
        issue_count = child_issue_count(child)
        lines.append(f"- `{child['key']}`: exit `{child['returncode']}`, {issue_count} issue(s)")

    lines.extend(["", "## Responsibility Issues", ""])
    if report["responsibility_issues"]:
        lines.extend(
            f"- `{issue['severity']}` `{issue['issue_id']}` in `{issue['file']}`: {issue['message']} Suggested owner: {issue['suggested_owner']}."
            for issue in report["responsibility_issues"]
        )
    else:
        lines.append("- None.")

    lines.extend(["", "## Fixes Applied", ""])
    if report["fixes_applied"]:
        for fix in report["fixes_applied"]:
            action = fix.get("action", "unknown")
            reason = fix.get("reason", "")
            file = fix.get("file", "")
            lines.append(f"- `{action}` in `{file}`: {reason}")
    else:
        lines.append("- None.")

    lines.extend(["", "## Errors", ""])
    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- None.")
    return "\n".join(lines).rstrip() + "\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def unresolved_issues(report: Dict[str, object]) -> bool:
    return bool(report["responsibility_issues"] or report["errors"] or report["post_fix_status"]) or any(
        child_issue_count(child) for child in report["document_reports"]
    )


def run_maintenance(args: argparse.Namespace) -> Tuple[Dict[str, object], str]:
    project_root = Path(args.project_root).expanduser().resolve()
    selected, selection_errors = select_workflows(args.include, args.skip)
    report: Dict[str, object] = {
        "run_context": {
            "project_root": str(project_root),
            "run_mode": args.run_mode,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "collect_source_tickets": bool(args.collect_source_tickets),
            "collect_github_issues": bool(args.collect_github_issues),
            "github_repo": args.github_repo or "",
        },
        "document_order": [workflow.key for workflow in selected],
        "document_reports": [],
        "responsibility_issues": [],
        "fixes_applied": [],
        "post_fix_status": [],
        "errors": selection_errors,
    }
    if not project_root.is_dir():
        report["errors"].append(f"Project root does not exist or is not a directory: {project_root}")
        return report, markdown_report(report)

    if not report["errors"]:
        for workflow in selected:
            child = run_child(args, workflow, project_root)
            report["document_reports"].append(child)
            report["fixes_applied"].extend(child_fixes(child))
            report["post_fix_status"].extend(child_post_fix_status(child))
            report["errors"].extend(child["errors"])
        report["responsibility_issues"] = audit_responsibility_boundaries(project_root, selected)

    return report, markdown_report(report)


def main() -> int:
    args = parse_args()
    report, md = run_maintenance(args)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.json_out:
        write_text(Path(args.json_out), payload)
    if args.md_out:
        write_text(Path(args.md_out), md)

    if args.print_json:
        sys.stdout.write(payload)
    elif args.print_md:
        sys.stdout.write(md)
    else:
        if not unresolved_issues(report):
            sys.stdout.write("No findings.\n")
        else:
            sys.stdout.write(md)

    if report["errors"]:
        return 1
    if args.fail_on_issues and unresolved_issues(report):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
