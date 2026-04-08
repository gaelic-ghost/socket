#!/usr/bin/env python3
"""Audit and apply bounded AGENTS.md maintenance for ordinary projects."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

SECTION_ORDER = [
    "Repository Expectations",
    "Standards and Guidance",
    "Project Workflows",
    "Validation",
    "Safety and Boundaries",
]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"<[^>]+>"),
]
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FENCED_BLOCK_RE = re.compile(r"```(?:bash|sh|shell)\n(.*?)```", re.DOTALL)


@dataclass
class Issue:
    issue_id: str
    category: str
    severity: str
    file: str
    evidence: str
    recommended_fix: str
    auto_fixable: bool
    fixed: bool = False

    def to_dict(self) -> Dict[str, object]:
        return {
            "issue_id": self.issue_id,
            "category": self.category,
            "severity": self.severity,
            "file": self.file,
            "evidence": self.evidence,
            "recommended_fix": self.recommended_fix,
            "auto_fixable": self.auto_fixable,
            "fixed": self.fixed,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit and optionally apply bounded AGENTS.md maintenance for ordinary projects."
    )
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--agents-path", help="Optional AGENTS.md path override")
    parser.add_argument("--run-mode", required=True, choices=["check-only", "apply"], help="Execution mode")
    parser.add_argument("--json-out", help="Write JSON report path")
    parser.add_argument("--md-out", help="Write markdown report path")
    parser.add_argument("--print-json", action="store_true", help="Print JSON report")
    parser.add_argument("--print-md", action="store_true", help="Print markdown report")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit non-zero when unresolved issues remain")
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> Dict[str, object]:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}


def load_toml(path: Path) -> Dict[str, object]:
    try:
        return tomllib.loads(read_text(path))
    except tomllib.TOMLDecodeError:
        return {}


def normalize_whitespace(text: str) -> str:
    return text.strip() + "\n"


def split_sections(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    matches = list(H2_RE.finditer(text))
    if not matches:
        return text, []

    preamble = text[: matches[0].start()].rstrip()
    sections: List[Tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        heading = match.group(1).strip()
        body = text[start:end].strip("\n")
        sections.append((heading, body))
    return preamble, sections


def section_map(sections: Sequence[Tuple[str, str]]) -> Dict[str, str]:
    return {heading: body for heading, body in sections}


def has_file(project_root: Path, *relative_paths: str) -> bool:
    return any((project_root / relative_path).exists() for relative_path in relative_paths)


def detect_profile(project_root: Path) -> Dict[str, object]:
    candidates: List[str] = []
    reasons: Dict[str, List[str]] = {
        "library-package": [],
        "cli-tool": [],
        "app-service": [],
        "monorepo-workspace": [],
    }

    if has_file(project_root, "pnpm-workspace.yaml", "turbo.json", "nx.json"):
        candidates.append("monorepo-workspace")
        reasons["monorepo-workspace"].append("workspace manifest detected")

    pyproject_path = project_root / "pyproject.toml"
    if pyproject_path.is_file():
        pyproject = load_toml(pyproject_path)
        project_table = pyproject.get("project", {})
        if isinstance(project_table, dict) and (project_table.get("scripts") or project_table.get("gui-scripts")):
            candidates.append("cli-tool")
            reasons["cli-tool"].append("pyproject scripts detected")
        raw_text = read_text(pyproject_path).lower()
        if any(token in raw_text for token in ["fastapi", "flask", "django", "uvicorn", "streamlit", "gradio"]):
            candidates.append("app-service")
            reasons["app-service"].append("application/service dependency detected in pyproject")
        elif "[project]" in raw_text or "[build-system]" in raw_text:
            candidates.append("library-package")
            reasons["library-package"].append("pyproject package metadata detected")

    package_json_path = project_root / "package.json"
    if package_json_path.is_file():
        package_json = load_json(package_json_path)
        if package_json.get("bin"):
            candidates.append("cli-tool")
            reasons["cli-tool"].append("package.json bin entry detected")
        if package_json.get("workspaces"):
            candidates.append("monorepo-workspace")
            reasons["monorepo-workspace"].append("package.json workspaces detected")
        deps_blob = json.dumps(
            {
                "dependencies": package_json.get("dependencies", {}),
                "devDependencies": package_json.get("devDependencies", {}),
            }
        ).lower()
        if any(token in deps_blob for token in ['"next"', '"react"', '"vite"', '"express"', '"nestjs"', '"astro"']):
            candidates.append("app-service")
            reasons["app-service"].append("application/service dependency detected in package.json")
        elif not package_json.get("bin") and not package_json.get("workspaces"):
            candidates.append("library-package")
            reasons["library-package"].append("package.json package metadata detected")

    cargo_path = project_root / "Cargo.toml"
    if cargo_path.is_file():
        cargo_text = read_text(cargo_path)
        if "[workspace]" in cargo_text:
            candidates.append("monorepo-workspace")
            reasons["monorepo-workspace"].append("Cargo workspace detected")
        if "[[bin]]" in cargo_text:
            candidates.append("cli-tool")
            reasons["cli-tool"].append("Cargo binary target detected")
        if "[package]" in cargo_text:
            candidates.append("library-package")
            reasons["library-package"].append("Cargo package metadata detected")

    package_swift_path = project_root / "Package.swift"
    if package_swift_path.is_file():
        package_swift = read_text(package_swift_path)
        if ".executableTarget" in package_swift:
            candidates.append("cli-tool")
            reasons["cli-tool"].append("Swift executable target detected")
        if ".library" in package_swift or ".target" in package_swift:
            candidates.append("library-package")
            reasons["library-package"].append("Swift package target detected")

    unique_candidates = list(dict.fromkeys(candidates))
    if "monorepo-workspace" in unique_candidates:
        selected = "monorepo-workspace"
    elif "app-service" in unique_candidates:
        selected = "app-service"
    elif "cli-tool" in unique_candidates:
        selected = "cli-tool"
    elif "library-package" in unique_candidates:
        selected = "library-package"
    else:
        selected = "library-package"
        unique_candidates.append(selected)
        reasons["library-package"].append("default fallback profile")

    return {
        "candidate_profiles": unique_candidates,
        "selected_profile": selected,
        "reasons": reasons[selected],
    }


def detect_package_manager(project_root: Path) -> Optional[str]:
    if (project_root / "pyproject.toml").is_file():
        return "uv"
    if (project_root / "package.json").is_file():
        return "pnpm"
    if (project_root / "Cargo.toml").is_file():
        return "cargo"
    if (project_root / "Package.swift").is_file():
        return "swift"
    return None


def detect_validation_command(project_root: Path) -> Optional[str]:
    if (project_root / "pyproject.toml").is_file():
        return "uv run pytest"
    if (project_root / "package.json").is_file():
        return "pnpm test"
    if (project_root / "Cargo.toml").is_file():
        return "cargo test"
    if (project_root / "Package.swift").is_file():
        return "swift test"
    return None


def detect_build_command(project_root: Path) -> Optional[str]:
    if (project_root / "pyproject.toml").is_file():
        return "uv sync"
    if (project_root / "package.json").is_file():
        return "pnpm install"
    if (project_root / "Cargo.toml").is_file():
        return "cargo build"
    if (project_root / "Package.swift").is_file():
        return "swift build"
    return None


def build_default_body(project_root: Path, profile: str) -> Dict[str, str]:
    package_manager = detect_package_manager(project_root)
    build_command = detect_build_command(project_root)
    validation_command = detect_validation_command(project_root)
    package_manager_line = (
        f"- Prefer `{package_manager}` for the primary project toolchain."
        if package_manager
        else "- Prefer the repository's existing primary toolchain and keep command vocabulary consistent."
    )
    build_block = f"```bash\n{build_command}\n```" if build_command else "Document the repo's setup or sync command here."
    validation_block = (
        f"```bash\n{validation_command}\n```"
        if validation_command
        else "Document the repo's canonical validation command here."
    )

    if profile == "app-service":
        workflow_hint = "Explain how agents should change runtime code, config, and request paths without inventing service behavior or background process assumptions."
    elif profile == "cli-tool":
        workflow_hint = "Explain how agents should update command behavior, examples, and help text while keeping the shipped CLI surface grounded in the repo."
    elif profile == "monorepo-workspace":
        workflow_hint = "Explain how agents should choose the correct package or app surface for a change and avoid cross-workspace drift."
    else:
        workflow_hint = "Explain how agents should keep changes bounded, update nearby docs or tests, and avoid speculative architectural pivots."

    return {
        "Repository Expectations": "\n".join(
            [
                "- Keep edits bounded to the requested project surface.",
                "- Treat repo-local files and docs as the source of truth before inventing workflow claims.",
                "- Surface architectural pivots explicitly instead of silently widening scope.",
            ]
        ),
        "Standards and Guidance": "\n".join(
            [
                package_manager_line,
                "- Keep naming, command vocabulary, and file ownership consistent across docs, scripts, and code.",
                "- Prefer repo-specific guidance over generic agent boilerplate.",
            ]
        ),
        "Project Workflows": "\n".join(
            [
                workflow_hint,
                "- Update nearby documentation when the active workflow or public behavior changes.",
                "- Recheck the target file paths and packaging surfaces before claiming a repo layout.",
            ]
        ),
        "Validation": "\n\n".join(
            [
                build_block,
                validation_block,
            ]
        ),
        "Safety and Boundaries": "\n".join(
            [
                "- Never invent commands, secrets, packaging surfaces, or policies that are not grounded in the repository.",
                "- Never auto-commit, auto-push, or open a PR unless the user explicitly asks.",
                "- Treat AGENTS guidance as maintainer or operator policy, not as public README content.",
            ]
        ),
    }


def reconstruct_document(project_root: Path, profile: str, existing_text: str) -> str:
    preamble, sections = split_sections(existing_text)
    section_lookup = section_map(sections)
    defaults = build_default_body(project_root, profile)

    if not preamble.strip():
        preamble = "# AGENTS.md"
    elif not preamble.lstrip().startswith("# "):
        preamble = "# AGENTS.md\n\n" + preamble.strip()

    rendered_sections: List[str] = []
    for heading in SECTION_ORDER:
        body = section_lookup.get(heading, "").strip() or defaults[heading]
        rendered_sections.append(f"## {heading}\n\n{body}".strip())

    extra_sections = [item for item in sections if item[0] not in SECTION_ORDER]
    for heading, body in extra_sections:
        rendered_sections.append(f"## {heading}\n\n{body}".strip())

    document = "\n\n".join([preamble.strip(), *rendered_sections]) + "\n"
    return normalize_whitespace(document)


def audit_document(project_root: Path, agents_path: Path, text: str) -> Dict[str, List[Issue]]:
    preamble, sections = split_sections(text)
    section_lookup = section_map(sections)
    schema_violations: List[Issue] = []
    workflow_drift_issues: List[Issue] = []
    validation_drift_issues: List[Issue] = []
    boundary_and_safety_issues: List[Issue] = []

    if not preamble.lstrip().startswith("# "):
        schema_violations.append(
            Issue(
                issue_id="missing-title",
                category="missing-title",
                severity="high",
                file=str(agents_path),
                evidence="AGENTS.md does not start with a level-1 title or preamble heading.",
                recommended_fix="Add a clear '# AGENTS.md' title.",
                auto_fixable=True,
            )
        )

    observed_headings = [heading for heading, _body in sections]
    for heading in SECTION_ORDER:
        if heading not in section_lookup:
            schema_violations.append(
                Issue(
                    issue_id=f"missing-section-{heading.lower().replace(' ', '-')}",
                    category="missing-required-section",
                    severity="high",
                    file=str(agents_path),
                    evidence=f"Missing required AGENTS section '{heading}'.",
                    recommended_fix=f"Add a '## {heading}' section.",
                    auto_fixable=True,
                )
            )

    ordered_present = [heading for heading in observed_headings if heading in SECTION_ORDER]
    canonical_present = [heading for heading in SECTION_ORDER if heading in ordered_present]
    if ordered_present and ordered_present != canonical_present:
        schema_violations.append(
            Issue(
                issue_id="non-canonical-section-order",
                category="section-order",
                severity="medium",
                file=str(agents_path),
                evidence="Canonical AGENTS sections are not in the expected order.",
                recommended_fix="Reorder the canonical sections to match the shared AGENTS schema.",
                auto_fixable=True,
            )
        )

    for match in FENCED_BLOCK_RE.finditer(text):
        block = match.group(1).strip()
        if not block:
            validation_drift_issues.append(
                Issue(
                    issue_id=f"empty-shell-block-{match.start()}",
                    category="empty-command-block",
                    severity="medium",
                    file=str(agents_path),
                    evidence="Found an empty fenced shell block.",
                    recommended_fix="Remove the empty block or replace it with grounded commands.",
                    auto_fixable=True,
                )
            )
        elif any(pattern.search(block) for pattern in PLACEHOLDER_PATTERNS):
            validation_drift_issues.append(
                Issue(
                    issue_id=f"placeholder-command-block-{match.start()}",
                    category="placeholder-command",
                    severity="high",
                    file=str(agents_path),
                    evidence="Found a fenced shell block with placeholder content.",
                    recommended_fix="Replace the placeholder block with grounded commands or prose.",
                    auto_fixable=True,
                )
            )

    if any(pattern.search(text) for pattern in PLACEHOLDER_PATTERNS):
        workflow_drift_issues.append(
            Issue(
                issue_id="placeholder-content",
                category="placeholder-content",
                severity="medium",
                file=str(agents_path),
                evidence="Found TODO/TBD or angle-bracket placeholder content in AGENTS.md.",
                recommended_fix="Replace placeholders with grounded project guidance.",
                auto_fixable=True,
            )
        )

    workflow_body = section_lookup.get("Project Workflows", "").strip()
    if workflow_body and len(workflow_body.split()) < 12:
        workflow_drift_issues.append(
            Issue(
                issue_id="thin-project-workflows",
                category="content-thin",
                severity="medium",
                file=str(agents_path),
                evidence="Project Workflows exists but is too thin to guide agents through repo changes.",
                recommended_fix="Expand the workflow section with grounded repo-specific guidance.",
                auto_fixable=True,
            )
        )

    validation_body = section_lookup.get("Validation", "").strip()
    validation_command = detect_validation_command(project_root)
    if not validation_body:
        validation_drift_issues.append(
            Issue(
                issue_id="empty-validation",
                category="empty-section",
                severity="medium",
                file=str(agents_path),
                evidence="Validation section is empty.",
                recommended_fix="Add the repo's grounded validation commands.",
                auto_fixable=True,
            )
        )
    elif validation_command and validation_command not in text:
        validation_drift_issues.append(
            Issue(
                issue_id="missing-validation-command",
                category="missing-grounded-command",
                severity="low",
                file=str(agents_path),
                evidence=f"The repo suggests '{validation_command}' as a grounded validation command, but AGENTS.md does not mention it.",
                recommended_fix="Mention the grounded validation command or equivalent validation guidance.",
                auto_fixable=True,
            )
        )

    safety_body = section_lookup.get("Safety and Boundaries", "").strip()
    if not safety_body:
        boundary_and_safety_issues.append(
            Issue(
                issue_id="empty-safety-and-boundaries",
                category="missing-safety-guidance",
                severity="high",
                file=str(agents_path),
                evidence="Safety and Boundaries is missing or empty.",
                recommended_fix="Add explicit bounded-edit and no-invention guidance.",
                auto_fixable=True,
            )
        )
    elif len(safety_body.split()) < 12:
        boundary_and_safety_issues.append(
            Issue(
                issue_id="thin-safety-and-boundaries",
                category="content-thin",
                severity="medium",
                file=str(agents_path),
                evidence="Safety and Boundaries exists but is too thin to act as a real guardrail surface.",
                recommended_fix="Expand the section with concrete safety and scope boundaries.",
                auto_fixable=True,
            )
        )

    return {
        "schema_violations": schema_violations,
        "workflow_drift_issues": workflow_drift_issues,
        "validation_drift_issues": validation_drift_issues,
        "boundary_and_safety_issues": boundary_and_safety_issues,
    }


def format_report(report: Dict[str, object]) -> str:
    total_issues = (
        len(report["schema_violations"])
        + len(report["workflow_drift_issues"])
        + len(report["validation_drift_issues"])
        + len(report["boundary_and_safety_issues"])
    )
    if total_issues == 0 and not report["errors"]:
        return "No findings."

    lines = [
        "# AGENTS.md Maintenance Report",
        "",
        f"- Target: `{report['run_context']['agents_path']}`",
        f"- Mode: `{report['run_context']['run_mode']}`",
        f"- Profile: `{report['run_context']['profile']}`",
    ]

    for key, title in (
        ("schema_violations", "Schema Violations"),
        ("workflow_drift_issues", "Workflow Drift Issues"),
        ("validation_drift_issues", "Validation Drift Issues"),
        ("boundary_and_safety_issues", "Boundary And Safety Issues"),
        ("fixes_applied", "Fixes Applied"),
        ("errors", "Errors"),
    ):
        items = report[key]
        if not items:
            continue
        lines.extend(["", f"## {title}"])
        for item in items:
            evidence = item.get("evidence") or item.get("description") or item.get("message")
            lines.append(f"- {item.get('issue_id', item.get('action', 'item'))}: {evidence}")

    return "\n".join(lines).strip() + "\n"


def run_maintenance(args: argparse.Namespace) -> Tuple[Dict[str, object], str]:
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.is_dir():
        raise ValueError(f"Project root does not exist or is not a directory: {project_root}")

    agents_path = (
        Path(args.agents_path).expanduser().resolve()
        if args.agents_path
        else project_root / "AGENTS.md"
    )
    profile_assignment = detect_profile(project_root)
    errors: List[str] = []
    fixes_applied: List[Dict[str, str]] = []

    existing_text = read_text(agents_path) if agents_path.is_file() else ""
    audit = (
        audit_document(project_root, agents_path, existing_text)
        if existing_text
        else {
            "schema_violations": [
                Issue(
                    issue_id="missing-agents-file",
                    category="missing-file",
                    severity="high",
                    file=str(agents_path),
                    evidence="AGENTS.md does not exist.",
                    recommended_fix="Create the canonical AGENTS.md file.",
                    auto_fixable=True,
                )
            ],
            "workflow_drift_issues": [],
            "validation_drift_issues": [],
            "boundary_and_safety_issues": [],
        }
    )

    if args.run_mode == "apply":
        new_text = reconstruct_document(project_root, profile_assignment["selected_profile"], existing_text)
        if not agents_path.parent.exists():
            agents_path.parent.mkdir(parents=True, exist_ok=True)
        if normalize_whitespace(existing_text) != new_text:
            write_text(agents_path, new_text)
            fixes_applied.append(
                {
                    "action": "updated-agents",
                    "file": str(agents_path),
                    "description": "Created or normalized AGENTS.md to the canonical project-agents schema.",
                }
            )
            existing_text = new_text
        audit = audit_document(project_root, agents_path, existing_text)

    report = {
        "run_context": {
            "project_root": str(project_root),
            "agents_path": str(agents_path),
            "run_mode": args.run_mode,
            "profile": profile_assignment["selected_profile"],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "schema_violations": [issue.to_dict() for issue in audit["schema_violations"]],
        "workflow_drift_issues": [issue.to_dict() for issue in audit["workflow_drift_issues"]],
        "validation_drift_issues": [issue.to_dict() for issue in audit["validation_drift_issues"]],
        "boundary_and_safety_issues": [issue.to_dict() for issue in audit["boundary_and_safety_issues"]],
        "fixes_applied": fixes_applied,
        "post_fix_status": {
            "remaining_issue_count": (
                len(audit["schema_violations"])
                + len(audit["workflow_drift_issues"])
                + len(audit["validation_drift_issues"])
                + len(audit["boundary_and_safety_issues"])
            ),
            "is_clean": (
                len(audit["schema_violations"]) == 0
                and len(audit["workflow_drift_issues"]) == 0
                and len(audit["validation_drift_issues"]) == 0
                and len(audit["boundary_and_safety_issues"]) == 0
                and not errors
            ),
        },
        "errors": errors,
    }

    markdown = format_report(report)
    return report, markdown


def main() -> int:
    args = parse_args()
    try:
        report, markdown = run_maintenance(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(markdown, encoding="utf-8")
    if args.print_json:
        print(json.dumps(report, indent=2))
    if args.print_md:
        print(markdown, end="")

    has_issues = (
        bool(report["schema_violations"])
        or bool(report["workflow_drift_issues"])
        or bool(report["validation_drift_issues"])
        or bool(report["boundary_and_safety_issues"])
        or bool(report["errors"])
    )
    if args.fail_on_issues and has_issues:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
