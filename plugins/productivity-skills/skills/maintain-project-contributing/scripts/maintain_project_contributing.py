#!/usr/bin/env python3
"""Audit and apply bounded CONTRIBUTING.md maintenance for ordinary software projects."""

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
    "Overview",
    "Contribution Workflow",
    "Local Setup",
    "Naming Conventions",
    "Verification",
    "Pull Request Expectations",
]
LOCAL_SETUP_SUBSECTIONS = ["Runtime Config", "Runtime Behavior"]
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"<[^>]+>"),
]
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
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
        description="Audit and optionally apply bounded CONTRIBUTING.md maintenance for ordinary software projects."
    )
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--contributing-path", help="Optional CONTRIBUTING.md path override")
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


def parse_title(preamble: str) -> Optional[str]:
    for line in preamble.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def detect_profile(project_root: Path) -> Dict[str, object]:
    candidates: List[str] = []
    reasons: Dict[str, List[str]] = {
        "library-package": [],
        "cli-tool": [],
        "app-service": [],
        "monorepo-workspace": [],
    }

    if any((project_root / path).exists() for path in ("pnpm-workspace.yaml", "turbo.json", "nx.json")):
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


def repo_name(project_root: Path) -> str:
    package_json = project_root / "package.json"
    if package_json.is_file():
        data = load_json(package_json)
        if isinstance(data.get("name"), str) and data["name"].strip():
            return data["name"].strip()

    pyproject = project_root / "pyproject.toml"
    if pyproject.is_file():
        data = load_toml(pyproject)
        project_table = data.get("project")
        if isinstance(project_table, dict) and isinstance(project_table.get("name"), str):
            return project_table["name"].strip()

    cargo = project_root / "Cargo.toml"
    if cargo.is_file():
        match = re.search(r'^\s*name\s*=\s*"([^"]+)"', read_text(cargo), flags=re.MULTILINE)
        if match:
            return match.group(1).strip()

    return project_root.name


def detect_setup_command(project_root: Path) -> Optional[str]:
    if (project_root / "pyproject.toml").is_file():
        return "uv sync"
    if (project_root / "package.json").is_file():
        return "pnpm install"
    if (project_root / "Cargo.toml").is_file():
        return "cargo build"
    if (project_root / "Package.swift").is_file():
        return "swift build"
    return None


def detect_verification_command(project_root: Path) -> Optional[str]:
    if (project_root / "pyproject.toml").is_file():
        return "uv run pytest"
    if (project_root / "package.json").is_file():
        return "pnpm test"
    if (project_root / "Cargo.toml").is_file():
        return "cargo test"
    if (project_root / "Package.swift").is_file():
        return "swift test"
    return None


def detect_runtime_behavior_hint(profile: str) -> str:
    if profile == "app-service":
        return "Explain the local runtime entrypoint, any background services, and how contributors should confirm the app or service is actually running."
    if profile == "cli-tool":
        return "Explain how contributors should exercise the CLI locally, including any fixture data or shell environment required to reproduce command behavior."
    if profile == "monorepo-workspace":
        return "Explain which package or app to run for the intended change, plus any workspace-wide background tasks contributors need to keep active."
    return "Explain any local processes, demo entrypoints, or execution steps contributors need before they can validate their changes."


def build_default_body(project_root: Path, profile: str) -> Dict[str, str]:
    setup_command = detect_setup_command(project_root)
    verification_command = detect_verification_command(project_root)

    setup_block = (
        f"```bash\n{setup_command}\n```"
        if setup_command
        else "Document the repository's local setup steps here."
    )
    verification_block = (
        f"```bash\n{verification_command}\n```"
        if verification_command
        else "Document the repository's canonical validation commands here."
    )

    return {
        "Overview": "Use this guide when preparing changes for review so the repository stays easy to run, verify, and extend.",
        "Contribution Workflow": "\n".join(
            [
                "- Start from a clean branch or worktree.",
                "- Keep changes bounded to one coherent purpose.",
                "- Update nearby docs or tests when behavior changes.",
            ]
        ),
        "Local Setup": "\n\n".join(
            [
                "### Runtime Config",
                setup_block,
                "Call out required local configuration files, secrets, or environment variables before contributors try to run the project.",
                "### Runtime Behavior",
                detect_runtime_behavior_hint(profile),
            ]
        ),
        "Naming Conventions": "\n".join(
            [
                "- Match the repository's existing terminology, casing, and file naming patterns.",
                "- Keep new public names aligned with the nouns already used in code, docs, and commands.",
                "- Rename only when the meaning changes or a real collision requires it.",
            ]
        ),
        "Verification": verification_block,
        "Pull Request Expectations": "\n".join(
            [
                "- Summarize what changed and why.",
                "- Note any user-facing or maintainer-facing follow-up work.",
                "- Include the validation you ran before requesting review.",
            ]
        ),
    }


def normalize_title(preamble: str, project_root: Path) -> str:
    desired = f"# Contributing to {repo_name(project_root)}"
    title = parse_title(preamble)
    if title:
        return f"# {title}"
    return desired


def local_setup_subsections(body: str) -> Dict[str, str]:
    matches = list(H3_RE.finditer(body))
    if not matches:
        return {}

    result: Dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        heading = match.group(1).strip()
        result[heading] = body[start:end].strip("\n")
    return result


def merge_local_setup(existing_body: str, default_body: str) -> str:
    existing = local_setup_subsections(existing_body)
    default = local_setup_subsections(default_body)
    parts: List[str] = []
    for heading in LOCAL_SETUP_SUBSECTIONS:
        body = existing.get(heading, "").strip() or default.get(heading, "").strip()
        parts.append(f"### {heading}\n\n{body}".strip())

    if not existing:
        return "\n\n".join(parts)

    leading_text = H3_RE.split(existing_body, maxsplit=1)[0].strip()
    if leading_text:
        return leading_text + "\n\n" + "\n\n".join(parts)
    return "\n\n".join(parts)


def reconstruct_document(project_root: Path, profile: str, existing_text: str) -> str:
    preamble, sections = split_sections(existing_text)
    section_lookup = section_map(sections)
    defaults = build_default_body(project_root, profile)

    rendered_sections: List[str] = []
    for heading in SECTION_ORDER:
        if heading == "Local Setup":
            body = merge_local_setup(section_lookup.get(heading, ""), defaults[heading])
        else:
            body = section_lookup.get(heading, "").strip() or defaults[heading]
        rendered_sections.append(f"## {heading}\n\n{body}".strip())

    extra_sections = [item for item in sections if item[0] not in SECTION_ORDER]
    for heading, body in extra_sections:
        rendered_sections.append(f"## {heading}\n\n{body}".strip())

    title = normalize_title(preamble, project_root)
    document = "\n\n".join([title, *rendered_sections]) + "\n"
    return normalize_whitespace(document)


def audit_document(project_root: Path, contributing_path: Path, text: str, profile: Dict[str, object]) -> Dict[str, List[Issue]]:
    preamble, sections = split_sections(text)
    section_lookup = section_map(sections)
    schema_violations: List[Issue] = []
    command_issues: List[Issue] = []
    content_issues: List[Issue] = []

    if parse_title(preamble) is None:
        schema_violations.append(
            Issue(
                issue_id="missing-title",
                category="missing-title",
                severity="high",
                file=str(contributing_path),
                evidence="CONTRIBUTING.md does not start with a level-1 title.",
                recommended_fix="Add a clear '# Contributing to <project>' title.",
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
                    file=str(contributing_path),
                    evidence=f"Missing required top-level section '{heading}'.",
                    recommended_fix=f"Add a '## {heading}' section in canonical order.",
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
                file=str(contributing_path),
                evidence="Canonical CONTRIBUTING.md sections are not in the expected order.",
                recommended_fix="Reorder the canonical sections to match the shared schema.",
                auto_fixable=True,
            )
        )

    local_setup_body = section_lookup.get("Local Setup", "")
    local_subsections = local_setup_subsections(local_setup_body)
    for heading in LOCAL_SETUP_SUBSECTIONS:
        if heading not in local_subsections:
            schema_violations.append(
                Issue(
                    issue_id=f"missing-local-setup-{heading.lower().replace(' ', '-')}",
                    category="missing-required-subsection",
                    severity="high",
                    file=str(contributing_path),
                    evidence=f"Local Setup is missing the required '{heading}' subsection.",
                    recommended_fix=f"Add '### {heading}' under '## Local Setup'.",
                    auto_fixable=True,
                )
            )

    naming_body = section_lookup.get("Naming Conventions", "").strip()
    if naming_body and len(naming_body.split()) < 8:
        content_issues.append(
            Issue(
                issue_id="thin-naming-conventions",
                category="content-thin",
                severity="medium",
                file=str(contributing_path),
                evidence="Naming Conventions exists but is too thin to guide contributors.",
                recommended_fix="Expand the section to cover terminology, casing, and alignment with existing repo naming.",
                auto_fixable=True,
            )
        )

    verification_body = section_lookup.get("Verification", "").strip()
    if not verification_body:
        content_issues.append(
            Issue(
                issue_id="empty-verification",
                category="empty-section",
                severity="medium",
                file=str(contributing_path),
                evidence="Verification section is empty.",
                recommended_fix="Add grounded validation guidance or commands.",
                auto_fixable=True,
            )
        )

    for match in FENCED_BLOCK_RE.finditer(text):
        block = match.group(1).strip()
        if not block:
            command_issues.append(
                Issue(
                    issue_id=f"empty-shell-block-{match.start()}",
                    category="empty-command-block",
                    severity="medium",
                    file=str(contributing_path),
                    evidence="Found an empty fenced shell block.",
                    recommended_fix="Remove the empty block or replace it with grounded commands.",
                    auto_fixable=True,
                )
            )
            continue
        if any(pattern.search(block) for pattern in PLACEHOLDER_PATTERNS):
            command_issues.append(
                Issue(
                    issue_id=f"placeholder-command-block-{match.start()}",
                    category="placeholder-command",
                    severity="high",
                    file=str(contributing_path),
                    evidence="Found a fenced shell block with placeholder content.",
                    recommended_fix="Replace the placeholder block with grounded commands or prose.",
                    auto_fixable=True,
                )
            )

    if any(pattern.search(text) for pattern in PLACEHOLDER_PATTERNS):
        content_issues.append(
            Issue(
                issue_id="placeholder-content",
                category="placeholder-content",
                severity="medium",
                file=str(contributing_path),
                evidence="Found TODO/TBD or angle-bracket placeholder content in CONTRIBUTING.md.",
                recommended_fix="Replace placeholders with grounded contributor guidance.",
                auto_fixable=True,
            )
        )

    setup_command = detect_setup_command(project_root)
    if setup_command and setup_command not in text:
        content_issues.append(
            Issue(
                issue_id="missing-setup-command",
                category="missing-grounded-command",
                severity="low",
                file=str(contributing_path),
                evidence=f"The repo suggests '{setup_command}' as a grounded setup command, but CONTRIBUTING.md does not mention it.",
                recommended_fix="Mention the grounded setup command or provide equivalent setup guidance.",
                auto_fixable=True,
            )
        )

    verification_command = detect_verification_command(project_root)
    if verification_command and verification_command not in text:
        content_issues.append(
            Issue(
                issue_id="missing-verification-command",
                category="missing-grounded-command",
                severity="low",
                file=str(contributing_path),
                evidence=f"The repo suggests '{verification_command}' as a grounded verification command, but CONTRIBUTING.md does not mention it.",
                recommended_fix="Mention the grounded verification command or provide equivalent validation guidance.",
                auto_fixable=True,
            )
        )

    return {
        "schema_violations": schema_violations,
        "command_integrity_issues": command_issues,
        "content_quality_issues": content_issues,
    }


def format_report(report: Dict[str, object]) -> str:
    total_issues = (
        len(report["schema_violations"])
        + len(report["command_integrity_issues"])
        + len(report["content_quality_issues"])
    )
    if total_issues == 0 and not report["errors"]:
        return "No findings."

    lines = [
        "# CONTRIBUTING.md Maintenance Report",
        "",
        f"- Target: `{report['run_context']['contributing_path']}`",
        f"- Mode: `{report['run_context']['run_mode']}`",
        f"- Profile: `{report['profile_assignment']['selected_profile']}`",
    ]

    for key, title in (
        ("schema_violations", "Schema Violations"),
        ("command_integrity_issues", "Command Integrity Issues"),
        ("content_quality_issues", "Content Quality Issues"),
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

    contributing_path = (
        Path(args.contributing_path).expanduser().resolve()
        if args.contributing_path
        else project_root / "CONTRIBUTING.md"
    )
    profile = detect_profile(project_root)

    errors: List[str] = []
    fixes_applied: List[Dict[str, str]] = []

    existing_text = read_text(contributing_path) if contributing_path.is_file() else ""
    audit = audit_document(project_root, contributing_path, existing_text, profile) if existing_text else {
        "schema_violations": [
            Issue(
                issue_id="missing-contributing-file",
                category="missing-file",
                severity="high",
                file=str(contributing_path),
                evidence="CONTRIBUTING.md does not exist.",
                recommended_fix="Create the canonical CONTRIBUTING.md file.",
                auto_fixable=True,
            )
        ],
        "command_integrity_issues": [],
        "content_quality_issues": [],
    }

    if args.run_mode == "apply":
        new_text = reconstruct_document(project_root, profile["selected_profile"], existing_text)
        if not contributing_path.parent.exists():
            contributing_path.parent.mkdir(parents=True, exist_ok=True)
        if normalize_whitespace(existing_text) != new_text:
            write_text(contributing_path, new_text)
            fixes_applied.append(
                {
                    "action": "updated-contributing",
                    "file": str(contributing_path),
                    "description": "Created or normalized CONTRIBUTING.md to the canonical contribution-guide schema.",
                }
            )
            existing_text = new_text

        audit = audit_document(project_root, contributing_path, existing_text, profile)
        for issue_group in audit.values():
            for issue in issue_group:
                issue.fixed = False

    report = {
        "run_context": {
            "project_root": str(project_root),
            "contributing_path": str(contributing_path),
            "run_mode": args.run_mode,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "profile_assignment": profile,
        "schema_violations": [issue.to_dict() for issue in audit["schema_violations"]],
        "command_integrity_issues": [issue.to_dict() for issue in audit["command_integrity_issues"]],
        "content_quality_issues": [issue.to_dict() for issue in audit["content_quality_issues"]],
        "fixes_applied": fixes_applied,
        "post_fix_status": {
            "remaining_issue_count": (
                len(audit["schema_violations"])
                + len(audit["command_integrity_issues"])
                + len(audit["content_quality_issues"])
            ),
            "is_clean": (
                len(audit["schema_violations"]) == 0
                and len(audit["command_integrity_issues"]) == 0
                and len(audit["content_quality_issues"]) == 0
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
        or bool(report["command_integrity_issues"])
        or bool(report["content_quality_issues"])
        or bool(report["errors"])
    )
    if args.fail_on_issues and has_issues:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
