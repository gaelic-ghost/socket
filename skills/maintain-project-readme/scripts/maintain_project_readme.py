#!/usr/bin/env python3
"""Audit and apply bounded README maintenance for ordinary software projects."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

COMMON_SECTION_ORDER = [
    "Table of Contents",
    "Overview",
    "Setup",
    "Usage",
    "Development",
    "Verification",
    "License",
]

PROFILE_SECTION_ORDER = {
    "library-package": ["API Notes"],
    "cli-tool": ["Command Reference"],
    "app-service": ["Configuration"],
    "monorepo-workspace": ["Repository Layout"],
}

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
        description="Audit and optionally apply bounded README maintenance for ordinary software projects."
    )
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--readme-path", help="Optional README path override")
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


def slugify_heading(heading: str) -> str:
    slug = heading.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


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


def parse_title_and_value_prop(preamble: str) -> Tuple[Optional[str], Optional[str]]:
    lines = [line.rstrip() for line in preamble.splitlines()]
    if not lines:
        return None, None
    title = None
    value_prop = None
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            for candidate in lines[idx + 1 :]:
                if candidate.strip():
                    value_prop = candidate.strip()
                    break
            break
    return title, value_prop


def normalize_preamble(preamble: str, repo_name: str) -> str:
    lines = [line.rstrip() for line in preamble.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)

    title_index: Optional[int] = None
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            title_index = idx
            break

    if title_index is None:
        lines.insert(0, f"# {repo_name}")
        title_index = 0

    value_prop_index: Optional[int] = None
    for idx in range(title_index + 1, len(lines)):
        if lines[idx].strip():
            value_prop_index = idx
            break

    if value_prop_index is None:
        insert_at = title_index + 1
        if insert_at >= len(lines) or lines[insert_at - 1].strip():
            lines.insert(insert_at, "")
            insert_at += 1
        lines.insert(insert_at, f"Project documentation for {repo_name}.")

    normalized = "\n".join(lines).strip()
    return normalized


def is_skills_or_plugin_repo(project_root: Path) -> bool:
    if (project_root / ".codex-plugin" / "plugin.json").is_file():
        return True
    skills_dir = project_root / "skills"
    if skills_dir.is_dir():
        for skill_file in skills_dir.glob("*/SKILL.md"):
            if skill_file.is_file():
                return True
    return False


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
        if isinstance(project_table, dict):
            scripts = project_table.get("scripts")
            gui_scripts = project_table.get("gui-scripts")
            if scripts or gui_scripts:
                candidates.append("cli-tool")
                reasons["cli-tool"].append("pyproject scripts detected")
        for table_name in ("dependency-groups",):
            if table_name in pyproject:
                candidates.append("library-package")
                reasons["library-package"].append("pyproject package metadata detected")
                break
        raw_text = read_text(pyproject_path).lower()
        if any(token in raw_text for token in ["fastapi", "flask", "django", "uvicorn", "streamlit", "gradio"]):
            candidates.append("app-service")
            reasons["app-service"].append("application/service dependency detected in pyproject")
        if "[project]" in raw_text or "[build-system]" in raw_text:
            candidates.append("library-package")
            reasons["library-package"].append("pyproject project metadata detected")

    package_json_path = project_root / "package.json"
    if package_json_path.is_file():
        package_json = load_json(package_json_path)
        if package_json.get("bin"):
            candidates.append("cli-tool")
            reasons["cli-tool"].append("package.json bin entry detected")
        if any(
            key in package_json
            for key in ["workspaces"]
        ):
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
        else:
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

    if has_file(
        project_root,
        "next.config.js",
        "next.config.mjs",
        "next.config.ts",
        "vite.config.js",
        "vite.config.ts",
        "docker-compose.yml",
        "docker-compose.yaml",
        "compose.yml",
        "compose.yaml",
        "Dockerfile",
    ):
        candidates.append("app-service")
        reasons["app-service"].append("app/service runtime file detected")

    unique_candidates = list(dict.fromkeys(candidates))
    if "monorepo-workspace" in unique_candidates:
        selected = "monorepo-workspace"
    elif len(unique_candidates) == 1:
        selected = unique_candidates[0]
    elif "app-service" in unique_candidates and "cli-tool" in unique_candidates:
        selected = "app-service"
    elif "cli-tool" in unique_candidates:
        selected = "cli-tool"
    elif "app-service" in unique_candidates:
        selected = "app-service"
    else:
        selected = "library-package"
        if selected not in unique_candidates:
            unique_candidates.append(selected)
            reasons["library-package"].append("defaulted to library/package profile")

    return {
        "selected_profile": selected,
        "ambiguous": len(unique_candidates) > 1,
        "candidates": unique_candidates,
        "reasons": {key: value for key, value in reasons.items() if value},
    }


def command_tool(line: str) -> Optional[str]:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if "<" in stripped and ">" in stripped:
        return "<placeholder>"

    parts = stripped.split()
    while parts and "=" in parts[0] and not parts[0].startswith(("./", "/", "uv", "pnpm", "npm", "cargo", "swift", "python", "docker")):
        parts = parts[1:]
    if not parts:
        return None
    if parts[0] == "docker" and len(parts) > 1 and parts[1] == "compose":
        return "docker-compose"
    return parts[0]


def validate_command_integrity(
    project_root: Path,
    readme_path: Path,
    readme_text: str,
    profile_info: Dict[str, object],
) -> List[Issue]:
    issues: List[Issue] = []
    has_python = (project_root / "pyproject.toml").is_file()
    has_node = (project_root / "package.json").is_file() or (project_root / "pnpm-workspace.yaml").is_file()
    has_rust = (project_root / "Cargo.toml").is_file()
    has_swift = (project_root / "Package.swift").is_file()
    has_docker = has_file(project_root, "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml", "Dockerfile")

    issue_index = 0
    for block in FENCED_BLOCK_RE.findall(readme_text):
        for raw_line in block.splitlines():
            tool = command_tool(raw_line)
            if tool is None:
                continue
            issue_index += 1
            if tool == "<placeholder>":
                issues.append(
                    Issue(
                        issue_id=f"command-placeholder-{issue_index}",
                        category="command-integrity",
                        severity="medium",
                        file=str(readme_path),
                        evidence=f"Command block contains placeholder syntax: {raw_line.strip()}",
                        recommended_fix="Replace placeholder command lines with real repo-grounded commands.",
                        auto_fixable=False,
                    )
                )
                continue

            invalid = (
                (tool in {"uv", "pytest"} and not has_python)
                or (tool in {"pnpm", "npm", "npx", "yarn"} and not has_node)
                or (tool == "cargo" and not has_rust)
                or (tool == "swift" and not has_swift)
                or (tool == "docker-compose" and not has_docker)
            )
            if invalid:
                issues.append(
                    Issue(
                        issue_id=f"unsupported-command-{issue_index}",
                        category="command-integrity",
                        severity="high",
                        file=str(readme_path),
                        evidence=f"README command does not match detected repo signals ({profile_info['selected_profile']}): {raw_line.strip()}",
                        recommended_fix="Replace the command with one supported by the repo's actual toolchain.",
                        auto_fixable=False,
                    )
                )
    return issues


def validate_schema(
    readme_path: Path,
    readme_text: str,
    profile_info: Dict[str, object],
) -> Tuple[List[Issue], List[Issue], List[Tuple[str, str]]]:
    schema_issues: List[Issue] = []
    content_issues: List[Issue] = []
    preamble, sections = split_sections(readme_text)
    section_lookup = section_map(sections)
    title, value_prop = parse_title_and_value_prop(preamble)

    if not title:
        schema_issues.append(
            Issue(
                issue_id="missing-title",
                category="schema",
                severity="high",
                file=str(readme_path),
                evidence="README is missing a top-level '# <project-name>' heading.",
                recommended_fix="Add a top-level title heading before the first H2 section.",
                auto_fixable=True,
            )
        )
    if not value_prop:
        schema_issues.append(
            Issue(
                issue_id="missing-value-proposition",
                category="schema",
                severity="medium",
                file=str(readme_path),
                evidence="README is missing a one-line value proposition beneath the title.",
                recommended_fix="Add a concise one-line value proposition beneath the title.",
                auto_fixable=True,
            )
        )

    required_sections = ["Overview", "Setup", "Usage", "Development", "Verification", "License"]
    for heading in required_sections:
        if heading not in section_lookup:
            schema_issues.append(
                Issue(
                    issue_id=f"missing-section-{slugify_heading(heading)}",
                    category="schema",
                    severity="high",
                    file=str(readme_path),
                    evidence=f"README is missing required section '## {heading}'.",
                    recommended_fix=f"Add the required '## {heading}' section.",
                    auto_fixable=True,
                )
            )
        elif not section_lookup[heading].strip():
            schema_issues.append(
                Issue(
                    issue_id=f"empty-section-{slugify_heading(heading)}",
                    category="schema",
                    severity="medium",
                    file=str(readme_path),
                    evidence=f"Section '## {heading}' is present but empty.",
                    recommended_fix=f"Add grounded content to '## {heading}'.",
                    auto_fixable=True,
                )
            )

    overview_body = section_lookup.get("Overview", "")
    if overview_body:
        motivation_present = any(heading.strip().lower() == "motivation" for heading in H3_RE.findall(overview_body))
        if not motivation_present:
            schema_issues.append(
                Issue(
                    issue_id="missing-motivation-subsection",
                    category="schema",
                    severity="high",
                    file=str(readme_path),
                    evidence="Overview section is missing the required '### Motivation' subsection.",
                    recommended_fix="Add a '### Motivation' subsection directly under '## Overview'.",
                    auto_fixable=True,
                )
            )

    all_required_after_optional = required_sections + PROFILE_SECTION_ORDER[profile_info["selected_profile"]]
    h2_count = len(sections)
    needs_toc = h2_count > 6
    if needs_toc and "Table of Contents" not in section_lookup:
        schema_issues.append(
            Issue(
                issue_id="missing-table-of-contents",
                category="schema",
                severity="low",
                file=str(readme_path),
                evidence="README has enough top-level sections to justify a table of contents, but none is present.",
                recommended_fix="Add a compact H2-only table of contents after the title/value proposition block.",
                auto_fixable=True,
            )
        )

    for heading in all_required_after_optional:
        body = section_lookup.get(heading)
        if body and any(pattern.search(body) for pattern in PLACEHOLDER_PATTERNS):
            content_issues.append(
                Issue(
                    issue_id=f"placeholder-content-{slugify_heading(heading)}",
                    category="content-quality",
                    severity="medium",
                    file=str(readme_path),
                    evidence=f"Section '## {heading}' contains placeholder-style content.",
                    recommended_fix="Replace placeholder content with repo-grounded wording.",
                    auto_fixable=False,
                )
            )

    if profile_info["ambiguous"]:
        content_issues.append(
            Issue(
                issue_id="ambiguous-profile-detection",
                category="content-quality",
                severity="low",
                file=str(readme_path),
                evidence=f"Repo profile detection found multiple candidates: {', '.join(profile_info['candidates'])}.",
                recommended_fix="Confirm the intended README profile if the selected structure does not fit the repo.",
                auto_fixable=False,
            )
        )

    return schema_issues, content_issues, sections


def section_template(repo_name: str, profile: str, heading: str) -> str:
    common_templates = {
        "Overview": (
            f"{repo_name} is maintained in this repository.\n\n"
            "Use this README to understand what the project provides, how to set it up, and how to verify local changes.\n\n"
            "### Motivation\n\n"
            "Describe why this project exists, who it helps, and what makes it worth using."
        ),
        "Setup": "Document the concrete local setup steps needed before someone can use or develop this project.",
        "Usage": "Show the most important way to use this project once setup is complete.",
        "Development": "Explain the local development workflow, including how contributors should make and validate changes.",
        "Verification": "List the grounded commands or checks used to verify local changes for this project.",
        "License": "See [LICENSE](./LICENSE).",
    }
    profile_templates = {
        ("library-package", "API Notes"): "Summarize the main package entrypoints, APIs, or integration surface that consumers should know about.",
        ("cli-tool", "Command Reference"): "List the key commands, flags, and examples that matter most for daily use.",
        ("app-service", "Configuration"): "Explain the required environment variables, local configuration, and runtime assumptions for this project.",
        ("monorepo-workspace", "Repository Layout"): "Describe the major packages, apps, or services in this workspace and where to find them.",
    }
    if (profile, heading) in profile_templates:
        return profile_templates[(profile, heading)]
    return common_templates[heading]


def build_toc(section_headings: Sequence[str]) -> str:
    lines = ["- [{0}](#{1})".format(heading, slugify_heading(heading)) for heading in section_headings if heading != "Table of Contents"]
    return "\n".join(lines)


def render_readme(
    normalized_preamble: str,
    repo_name: str,
    profile: str,
    existing_sections: Sequence[Tuple[str, str]],
) -> str:
    existing_lookup = section_map(existing_sections)
    existing_order = [heading for heading, _body in existing_sections]
    include_toc = "Table of Contents" in existing_lookup or len(existing_sections) > 6

    ordered_headings: List[str] = []
    if include_toc:
        ordered_headings.append("Table of Contents")
    ordered_headings.extend([heading for heading in COMMON_SECTION_ORDER if heading != "Table of Contents"])
    for heading in PROFILE_SECTION_ORDER[profile]:
        if heading in existing_lookup:
            ordered_headings.append(heading)
    for heading in existing_order:
        if heading not in ordered_headings:
            ordered_headings.append(heading)

    sections: List[Tuple[str, str]] = []
    for heading in ordered_headings:
        if heading == "Table of Contents":
            continue
        body = existing_lookup.get(heading, "").strip()
        if heading == "Overview":
            if not body:
                body = section_template(repo_name, profile, heading)
            elif "### Motivation" not in body:
                body = body.rstrip() + "\n\n### Motivation\n\nDescribe why this project exists, who it helps, and what makes it worth using."
        elif not body and heading in COMMON_SECTION_ORDER:
            body = section_template(repo_name, profile, heading)
        sections.append((heading, body))

    if include_toc:
        toc_body = build_toc([heading for heading, _body in sections])
        sections.insert(0, ("Table of Contents", toc_body))

    rendered = [normalized_preamble.strip()]
    for heading, body in sections:
        rendered.extend(["", f"## {heading}", "", body.strip()])
    return normalize_whitespace("\n".join(rendered))


def apply_fixes(project_root: Path, readme_path: Path, readme_text: str, profile_info: Dict[str, object]) -> Tuple[str, List[Dict[str, str]]]:
    preamble, sections = split_sections(readme_text)
    repo_name = project_root.name
    normalized_preamble = normalize_preamble(preamble, repo_name)

    updated = render_readme(normalized_preamble, repo_name, profile_info["selected_profile"], sections)
    actions: List[Dict[str, str]] = []
    if updated != normalize_whitespace(readme_text):
        write_text(readme_path, updated)
        actions.append(
            {
                "action": "rewrite-readme-structure",
                "file": str(readme_path),
                "reason": "Normalized README structure, repaired required sections, and ensured an Overview > Motivation subsection.",
            }
        )
    return updated, actions


def markdown_report(report: Dict[str, object]) -> str:
    lines = [
        "# Maintain Project README Report",
        "",
        "## Run Context",
        "",
        f"- Project root: `{report['run_context']['project_root']}`",
        f"- README path: `{report['run_context']['readme_path']}`",
        f"- Run mode: `{report['run_context']['run_mode']}`",
        f"- Timestamp: `{report['run_context']['timestamp_utc']}`",
        "",
        "## Profile Assignment",
        "",
        f"- Selected profile: `{report['profile_assignment'].get('selected_profile', 'unresolved')}`",
        f"- Ambiguous: `{report['profile_assignment'].get('ambiguous', False)}`",
        f"- Candidates: `{', '.join(report['profile_assignment'].get('candidates', []))}`",
        "",
        "## Schema Violations",
        "",
    ]
    if report["schema_violations"]:
        lines.extend(
            f"- `{issue['severity']}` `{issue['issue_id']}`: {issue['evidence']}"
            for issue in report["schema_violations"]
        )
    else:
        lines.append("- None.")

    lines.extend(["", "## Command Integrity Issues", ""])
    if report["command_integrity_issues"]:
        lines.extend(
            f"- `{issue['severity']}` `{issue['issue_id']}`: {issue['evidence']}"
            for issue in report["command_integrity_issues"]
        )
    else:
        lines.append("- None.")

    lines.extend(["", "## Content Quality Issues", ""])
    if report["content_quality_issues"]:
        lines.extend(
            f"- `{issue['severity']}` `{issue['issue_id']}`: {issue['evidence']}"
            for issue in report["content_quality_issues"]
        )
    else:
        lines.append("- None.")

    lines.extend(["", "## Fixes Applied", ""])
    if report["fixes_applied"]:
        lines.extend(f"- `{action['action']}`: {action['reason']}" for action in report["fixes_applied"])
    else:
        lines.append("- None.")

    lines.extend(["", "## Post-Fix Status", ""])
    if report["post_fix_status"]:
        lines.extend(
            f"- `{issue['severity']}` `{issue['issue_id']}`: {issue['evidence']}"
            for issue in report["post_fix_status"]
        )
    else:
        lines.append("- Clean.")

    lines.extend(["", "## Errors", ""])
    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- None.")

    return "\n".join(lines).rstrip() + "\n"


def unresolved_issues(report: Dict[str, object]) -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = []
    for key in ["schema_violations", "command_integrity_issues", "content_quality_issues", "post_fix_status"]:
        items.extend(report[key])
    return items


def run_maintenance(args: argparse.Namespace) -> Tuple[Dict[str, object], str]:
    project_root = Path(args.project_root).expanduser().resolve()
    readme_path = Path(args.readme_path).expanduser().resolve() if args.readme_path else project_root / "README.md"

    report: Dict[str, object] = {
        "run_context": {
            "project_root": str(project_root),
            "readme_path": str(readme_path),
            "run_mode": args.run_mode,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        },
        "profile_assignment": {},
        "schema_violations": [],
        "command_integrity_issues": [],
        "content_quality_issues": [],
        "fixes_applied": [],
        "post_fix_status": [],
        "errors": [],
    }

    if not project_root.is_dir():
        report["errors"].append(f"Project root does not exist or is not a directory: {project_root}")
        return report, markdown_report(report)
    if not readme_path.is_file():
        report["errors"].append(f"README path does not exist: {readme_path}")
        return report, markdown_report(report)
    if is_skills_or_plugin_repo(project_root):
        report["errors"].append(
            "Detected a skills/plugin repository. Use `maintain-skills-readme` instead of `maintain-project-readme`."
        )
        return report, markdown_report(report)

    readme_text = read_text(readme_path)
    profile_info = detect_profile(project_root)
    report["profile_assignment"] = profile_info

    schema_issues, content_issues, _sections = validate_schema(readme_path, readme_text, profile_info)
    command_issues = validate_command_integrity(project_root, readme_path, readme_text, profile_info)

    report["schema_violations"] = [issue.to_dict() for issue in schema_issues]
    report["command_integrity_issues"] = [issue.to_dict() for issue in command_issues]
    report["content_quality_issues"] = [issue.to_dict() for issue in content_issues]

    if args.run_mode == "apply" and not report["errors"]:
        _updated_text, actions = apply_fixes(project_root, readme_path, readme_text, profile_info)
        report["fixes_applied"] = actions
        refreshed_text = read_text(readme_path)
        post_schema, post_content, _ = validate_schema(readme_path, refreshed_text, profile_info)
        post_commands = validate_command_integrity(project_root, readme_path, refreshed_text, profile_info)
        report["post_fix_status"] = [
            issue.to_dict()
            for issue in [*post_schema, *post_commands, *post_content]
        ]

    md = markdown_report(report)
    return report, md


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
        if not unresolved_issues(report) and not report["errors"]:
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
