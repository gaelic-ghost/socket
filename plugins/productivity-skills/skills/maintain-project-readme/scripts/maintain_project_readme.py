#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Audit and apply bounded README maintenance from a hard-enforced schema."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import yaml

H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"<[^>]+>"),
]
CONTRIBUTOR_PROCEDURE_HEADINGS = {
    "Setup",
    "Workflow",
    "Validation",
    "Local Setup",
    "Development Workflow",
    "Release Workflow",
    "Review Workflow",
    "Maintainer Workflow",
}


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
        description="Audit and optionally apply bounded README maintenance from a hard-enforced schema."
    )
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--readme-path", help="Optional README path override")
    parser.add_argument("--run-mode", required=True, choices=["check-only", "apply"], help="Execution mode")
    parser.add_argument("--config", help="Optional README config override")
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
        return text.strip(), []

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


def parse_title_and_summary(preamble: str) -> Tuple[Optional[str], Optional[str], List[str]]:
    lines = [line.rstrip() for line in preamble.splitlines()]
    title: Optional[str] = None
    summary: Optional[str] = None
    extras: List[str] = []

    if not lines:
        return None, None, extras

    title_index: Optional[int] = None
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            title_index = idx
            break

    if title_index is None:
        return None, None, lines

    summary_index: Optional[int] = None
    for idx in range(title_index + 1, len(lines)):
        if lines[idx].strip():
            summary = lines[idx].strip()
            summary_index = idx
            break

    for idx, line in enumerate(lines):
        if idx == title_index or idx == summary_index:
            continue
        extras.append(line)

    return title, summary, extras


def collapse_blank_lines(lines: Sequence[str]) -> List[str]:
    collapsed: List[str] = []
    previous_blank = False
    for line in lines:
        blank = line.strip() == ""
        if blank and previous_blank:
            continue
        collapsed.append(line)
        previous_blank = blank
    while collapsed and collapsed[0].strip() == "":
        collapsed.pop(0)
    while collapsed and collapsed[-1].strip() == "":
        collapsed.pop()
    return collapsed


def normalize_preamble(preamble: str, repo_name: str, preserve_preamble: bool) -> str:
    title, summary, extras = parse_title_and_summary(preamble)
    normalized_title = title or repo_name
    normalized_summary = summary or f"Project documentation for {repo_name}."

    lines = [f"# {normalized_title}", "", normalized_summary]
    if preserve_preamble:
        extra_lines = collapse_blank_lines(extras)
        if extra_lines:
            lines.extend(["", *extra_lines])
    return "\n".join(lines).strip()


def render_template_bootstrap(project_root: Path) -> str:
    template_path = Path(__file__).resolve().parents[1] / "assets" / "README.template.md"
    template = read_text(template_path)
    rendered = template.replace("{{PROJECT_NAME}}", project_root.name)
    rendered = rendered.replace("{{ONE_LINE_SUMMARY}}", f"Project documentation for {project_root.name}.")
    return normalize_whitespace(rendered)


def is_skills_or_plugin_repo(project_root: Path) -> bool:
    if (project_root / ".codex-plugin" / "plugin.json").is_file():
        return True
    skills_dir = project_root / "skills"
    if skills_dir.is_dir():
        for skill_file in skills_dir.glob("*/SKILL.md"):
            if skill_file.is_file():
                return True
    return False


def read_yaml(path: Path) -> Dict[str, object]:
    data = yaml.safe_load(read_text(path))
    return data if isinstance(data, dict) else {}


def deep_merge(base: Dict[str, object], override: Dict[str, object]) -> Dict[str, object]:
    merged: Dict[str, object] = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)  # type: ignore[arg-type]
        else:
            merged[key] = value
    return merged


def load_config(project_root: Path, config_override: Optional[str]) -> Dict[str, object]:
    default_path = Path(__file__).resolve().parents[1] / "config" / "readme-customization.template.yaml"
    default_config = read_yaml(default_path)
    loaded_path = default_path

    if config_override:
        override_path = Path(config_override).expanduser().resolve()
        merged = deep_merge(default_config, read_yaml(override_path))
        merged["isCustomized"] = True
        merged["configPath"] = str(override_path)
        merged["defaultConfigPath"] = str(default_path)
        return merged

    project_config = project_root / "config" / "readme-customization.yaml"
    if project_config.is_file():
        loaded_path = project_config
        merged = deep_merge(default_config, read_yaml(project_config))
        merged["isCustomized"] = True
    else:
        merged = dict(default_config)
        merged["isCustomized"] = bool(default_config.get("isCustomized", False))

    merged["configPath"] = str(loaded_path)
    merged["defaultConfigPath"] = str(default_path)
    return merged


def config_settings(config: Dict[str, object]) -> Dict[str, object]:
    settings = config.get("settings", {})
    return settings if isinstance(settings, dict) else {}


def required_sections(settings: Dict[str, object]) -> List[str]:
    sections = settings.get("requiredSections", [])
    return [str(item) for item in sections] if isinstance(sections, list) else []


def canonical_order(settings: Dict[str, object]) -> List[str]:
    order = settings.get("sectionOrder", [])
    return [str(item) for item in order] if isinstance(order, list) else []


def required_subsections(settings: Dict[str, object]) -> Dict[str, List[str]]:
    raw = settings.get("requiredSubsections", {})
    if not isinstance(raw, dict):
        return {}
    normalized: Dict[str, List[str]] = {}
    for key, value in raw.items():
        if isinstance(value, list):
            normalized[str(key)] = [str(item) for item in value]
    return normalized


def section_aliases(settings: Dict[str, object]) -> Dict[str, List[str]]:
    raw = settings.get("sectionAliases", {})
    if not isinstance(raw, dict):
        return {}
    normalized: Dict[str, List[str]] = {}
    for key, value in raw.items():
        if isinstance(value, list):
            normalized[str(key)] = [str(item) for item in value]
    return normalized


def section_templates(settings: Dict[str, object]) -> Dict[str, str]:
    raw = settings.get("sectionTemplates", {})
    if not isinstance(raw, dict):
        return {}
    return {str(key): str(value).strip() for key, value in raw.items()}


def subsection_templates(settings: Dict[str, object]) -> Dict[str, str]:
    raw = settings.get("subsectionTemplates", {})
    if not isinstance(raw, dict):
        return {}
    return {str(key): str(value).strip() for key, value in raw.items()}


def collect_subsection_headings(body: str) -> List[str]:
    return [heading.strip() for heading in H3_RE.findall(body)]


def build_toc(headings: Sequence[str]) -> str:
    return "\n".join(f"- [{heading}](#{slugify_heading(heading)})" for heading in headings)


def toc_entries(body: str) -> List[str]:
    entries: List[str] = []
    for line in body.splitlines():
        match = re.match(r"^\s*-\s+\[(.+?)\]\(#(.+?)\)\s*$", line.strip())
        if match:
            entries.append(match.group(1).strip())
    return entries


def alias_lookup(settings: Dict[str, object]) -> Dict[str, str]:
    aliases = section_aliases(settings)
    reverse: Dict[str, str] = {}
    for canonical, names in aliases.items():
        for alias in names:
            reverse[alias] = canonical
    return reverse


def validate_schema(
    readme_path: Path,
    readme_text: str,
    config: Dict[str, object],
) -> Tuple[List[Issue], List[Issue], List[Tuple[str, str]]]:
    settings = config_settings(config)
    required = required_sections(settings)
    order = canonical_order(settings)
    subsection_map = required_subsections(settings)
    alias_map = alias_lookup(settings)

    schema_issues: List[Issue] = []
    content_issues: List[Issue] = []
    preamble, sections = split_sections(readme_text)
    lookup = section_map(sections)
    title, summary, _extras = parse_title_and_summary(preamble)

    if not title:
        schema_issues.append(
            Issue(
                issue_id="missing-title",
                category="schema",
                severity="high",
                file=str(readme_path),
                evidence="README is missing a top-level '# <project-name>' heading.",
                recommended_fix="Add a top-level title before the canonical section block.",
                auto_fixable=True,
            )
        )
    if not summary:
        schema_issues.append(
            Issue(
                issue_id="missing-summary",
                category="schema",
                severity="high",
                file=str(readme_path),
                evidence="README is missing a one-line summary directly beneath the title.",
                recommended_fix="Add a concise one-line summary directly beneath the title.",
                auto_fixable=True,
            )
        )

    if "Table of Contents" not in lookup:
        schema_issues.append(
            Issue(
                issue_id="missing-table-of-contents",
                category="schema",
                severity="medium",
                file=str(readme_path),
                evidence="README is missing the required '## Table of Contents' section.",
                recommended_fix="Add an H2-only table of contents that mirrors the canonical top-level headings.",
                auto_fixable=True,
            )
        )
    current_positions: Dict[str, int] = {heading: idx for idx, (heading, _body) in enumerate(sections)}
    for heading in required:
        if heading not in lookup:
            alias_found = next((alias for alias, canonical in alias_map.items() if canonical == heading and alias in lookup), None)
            if alias_found:
                schema_issues.append(
                    Issue(
                        issue_id=f"non-canonical-heading-{slugify_heading(heading)}",
                        category="schema",
                        severity="medium",
                        file=str(readme_path),
                        evidence=f"README uses alias heading '## {alias_found}' where the canonical schema expects '## {heading}'.",
                        recommended_fix=f"Rename '## {alias_found}' to '## {heading}'.",
                        auto_fixable=True,
                    )
                )
            else:
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

    order_positions: List[int] = []
    for heading in order:
        if heading in current_positions:
            order_positions.append(current_positions[heading])
        else:
            alias_found = next((alias for alias, canonical in alias_map.items() if canonical == heading and alias in current_positions), None)
            if alias_found:
                order_positions.append(current_positions[alias_found])
    if order_positions and order_positions != sorted(order_positions):
        schema_issues.append(
            Issue(
                issue_id="canonical-section-order",
                category="schema",
                severity="medium",
                file=str(readme_path),
                evidence="Canonical README sections are not in the configured order.",
                recommended_fix="Normalize the top-level sections into canonical order.",
                auto_fixable=True,
            )
        )

    for parent, children in subsection_map.items():
        body = lookup.get(parent, "")
        if not body:
            continue
        found_children = collect_subsection_headings(body)
        for child in children:
            if child not in found_children:
                schema_issues.append(
                    Issue(
                        issue_id=f"missing-subsection-{slugify_heading(parent)}-{slugify_heading(child)}",
                        category="schema",
                        severity="high",
                        file=str(readme_path),
                        evidence=f"Section '## {parent}' is missing required subsection '### {child}'.",
                        recommended_fix=f"Add the required subsection '### {child}' under '## {parent}'.",
                        auto_fixable=True,
                )
            )

        if parent == "Overview":
            preamble, subsections = split_subsections(body)
            subsection_lookup = {name: subsection_body for name, subsection_body in subsections}
            status_body = subsection_lookup.get("Status", "").strip()
            if status_body:
                status_lines = [line for line in status_body.splitlines() if line.strip()]
                if len(status_lines) > 2 or len(status_body) > 220:
                    content_issues.append(
                        Issue(
                            issue_id="status-section-too-long",
                            category="content-quality",
                            severity="low",
                            file=str(readme_path),
                            evidence="Section 'Overview > Status' should stay very short and plain.",
                            recommended_fix="Reduce the Status subsection to a brief statement about maturity, availability, or inactivity.",
                            auto_fixable=False,
                        )
                    )

    if "Table of Contents" in lookup:
        expected_toc = [heading for heading, _body in sections if heading != "Table of Contents"]
        actual_toc = toc_entries(lookup["Table of Contents"])
        if actual_toc != expected_toc:
            schema_issues.append(
                Issue(
                    issue_id="stale-table-of-contents",
                    category="schema",
                    severity="low",
                    file=str(readme_path),
                    evidence="Table of contents entries do not match the canonical top-level section headings in order.",
                    recommended_fix="Regenerate the H2-only table of contents from the canonical section list.",
                    auto_fixable=True,
                )
            )

    for heading in required:
        body = lookup.get(heading)
        if not body:
            continue
        if any(pattern.search(body) for pattern in PLACEHOLDER_PATTERNS):
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
        if not body.strip():
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

        if heading == "Repo Structure" and "```text" not in body:
            content_issues.append(
                Issue(
                    issue_id="repo-structure-missing-tree-outline",
                    category="content-quality",
                    severity="medium",
                    file=str(readme_path),
                    evidence="Section '## Repo Structure' should contain a short directory tree or outline diagram.",
                    recommended_fix="Replace the Repo Structure prose with a short fenced `text` directory tree or outline.",
                    auto_fixable=False,
                )
            )
        if heading == "Development" and not required_subsections(settings).get("Development"):
            procedure_headings = [
                subsection for subsection in collect_subsection_headings(body) if subsection in CONTRIBUTOR_PROCEDURE_HEADINGS
            ]
            if procedure_headings:
                content_issues.append(
                    Issue(
                        issue_id="readme-development-contains-contributor-procedure",
                        category="content-quality",
                        severity="medium",
                        file=str(readme_path),
                        evidence=(
                            "Section '## Development' contains contributor-procedure subsections: "
                            + ", ".join(f"'### {heading}'" for heading in procedure_headings)
                            + "."
                        ),
                        recommended_fix=(
                            "Move setup, workflow, validation, release, branch, and review procedures to "
                            "`CONTRIBUTING.md` or a maintainer document, and keep README.md to a short pointer."
                        ),
                        auto_fixable=False,
                    )
                )

    return schema_issues, content_issues, sections


def split_subsections(body: str) -> Tuple[str, List[Tuple[str, str]]]:
    matches = list(H3_RE.finditer(body))
    if not matches:
        return body.strip(), []

    preamble = body[: matches[0].start()].strip()
    subsections: List[Tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        heading = match.group(1).strip()
        subsection_body = body[start:end].strip("\n")
        subsections.append((heading, subsection_body))
    return preamble, subsections


def render_section_body(
    heading: str,
    existing_body: str,
    settings: Dict[str, object],
) -> str:
    required_children = required_subsections(settings).get(heading, [])
    section_template_map = section_templates(settings)
    subsection_template_map = subsection_templates(settings)

    if not required_children:
        return existing_body.strip() or section_template_map.get(heading, "")

    preamble, subsections = split_subsections(existing_body)
    subsection_lookup = {name: body for name, body in subsections}
    ordered_lines: List[str] = []
    if preamble.strip():
        ordered_lines.extend([preamble.strip(), ""])

    for idx, child in enumerate(required_children):
        child_body = subsection_lookup.get(child, "").strip()
        if not child_body:
            child_body = subsection_template_map.get(f"{heading}/{child}", "")
        ordered_lines.extend([f"### {child}", "", child_body.strip()])
        if idx < len(required_children) - 1:
            ordered_lines.append("")

    used_children = set(required_children)
    extras = [(name, body) for name, body in subsections if name not in used_children]
    if extras:
        ordered_lines.append("")
        for idx, (name, body) in enumerate(extras):
            ordered_lines.extend([f"### {name}", "", body.strip()])
            if idx < len(extras) - 1:
                ordered_lines.append("")

    rendered = "\n".join(line for line in ordered_lines if line is not None).strip()
    return rendered or section_template_map.get(heading, "")


def apply_fixes(project_root: Path, readme_path: Path, readme_text: str, config: Dict[str, object]) -> Tuple[str, List[Dict[str, str]]]:
    if not readme_text.strip():
        bootstrap = render_template_bootstrap(project_root)
        write_text(readme_path, bootstrap)
        return (
            bootstrap,
            [
                {
                    "action": "create-readme-from-template",
                    "file": str(readme_path),
                    "reason": "Created a missing README.md from the bundled canonical README template.",
                }
            ],
        )

    settings = config_settings(config)
    required = required_sections(settings)
    order = canonical_order(settings)
    alias_map = alias_lookup(settings)
    preserve_preamble = bool(settings.get("preservePreamble", True))
    allow_additional = bool(settings.get("allowAdditionalSections", True))

    preamble, sections = split_sections(readme_text)
    repo_name = project_root.name
    normalized_preamble = normalize_preamble(preamble, repo_name, preserve_preamble)
    existing_lookup = section_map(sections)

    canonical_lookup: Dict[str, str] = {}
    extra_sections: List[Tuple[str, str]] = []
    used_aliases: set[str] = set()

    for heading, body in sections:
        if heading == "Table of Contents":
            continue
        if heading in order or heading in required:
            canonical_lookup[heading] = body
            continue
        if heading in alias_map:
            canonical_lookup[alias_map[heading]] = body
            used_aliases.add(heading)
            continue
        if allow_additional:
            extra_sections.append((heading, body))

    canonical_sections: List[Tuple[str, str]] = []
    for heading in order:
        existing_body = canonical_lookup.get(heading, existing_lookup.get(heading, ""))
        body = render_section_body(heading, existing_body, settings).strip()
        canonical_sections.append((heading, body))

    top_level_for_toc = [heading for heading, _body in canonical_sections]
    if allow_additional:
        top_level_for_toc.extend(heading for heading, _body in extra_sections)
    rendered_lines = [normalized_preamble.strip()]
    rendered_lines.extend(["", "## Table of Contents", "", build_toc(top_level_for_toc)])

    for heading, body in canonical_sections:
        rendered_lines.extend(["", f"## {heading}", "", body.strip()])

    if allow_additional:
        for heading, body in extra_sections:
            rendered_lines.extend(["", f"## {heading}", "", body.strip()])

    updated = normalize_whitespace("\n".join(rendered_lines))
    actions: List[Dict[str, str]] = []
    if updated != normalize_whitespace(readme_text):
        write_text(readme_path, updated)
        actions.append(
            {
                "action": "normalize-readme-schema",
                "file": str(readme_path),
                "reason": "Normalized the README into the configured canonical structure and preserved allowed preamble content.",
            }
        )
    if used_aliases:
        actions.append(
            {
                "action": "migrate-alias-headings",
                "file": str(readme_path),
                "reason": f"Migrated alias headings into canonical heading names: {', '.join(sorted(used_aliases))}.",
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
        "## Customization State",
        "",
        f"- Config path: `{report['customization_state'].get('config_path', 'none')}`",
        f"- Default config path: `{report['customization_state'].get('default_config_path', 'none')}`",
        f"- Profile: `{report['customization_state'].get('profile', 'base')}`",
        f"- Customized: `{report['customization_state'].get('is_customized', False)}`",
        "",
        "## Schema Contract",
        "",
        f"- Required sections: `{', '.join(report['schema_contract'].get('required_sections', []))}`",
        f"- Canonical order: `{', '.join(report['schema_contract'].get('section_order', []))}`",
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
    for key in ["schema_violations", "content_quality_issues", "post_fix_status"]:
        items.extend(report[key])
    return items


def schema_contract(config: Dict[str, object]) -> Dict[str, object]:
    settings = config_settings(config)
    return {
        "required_sections": required_sections(settings),
        "section_order": canonical_order(settings),
        "required_subsections": required_subsections(settings),
    }


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
        "customization_state": {},
        "schema_contract": {},
        "schema_violations": [],
        "content_quality_issues": [],
        "fixes_applied": [],
        "post_fix_status": [],
        "errors": [],
    }

    if not project_root.is_dir():
        report["errors"].append(f"Project root does not exist or is not a directory: {project_root}")
        return report, markdown_report(report)
    config = load_config(project_root, args.config)
    report["customization_state"] = {
        "config_path": config.get("configPath", "none"),
        "default_config_path": config.get("defaultConfigPath", "none"),
        "profile": config.get("profile", "base"),
        "is_customized": bool(config.get("isCustomized", False)),
    }
    report["schema_contract"] = schema_contract(config)

    if readme_path.is_file():
        readme_text = read_text(readme_path)
        schema_issues, content_issues, _sections = validate_schema(readme_path, readme_text, config)
        report["schema_violations"] = [issue.to_dict() for issue in schema_issues]
        report["content_quality_issues"] = [issue.to_dict() for issue in content_issues]
    elif args.run_mode == "apply":
        readme_text = ""
    else:
        report["errors"].append(f"README path does not exist: {readme_path}")
        return report, markdown_report(report)

    if args.run_mode == "apply" and not report["errors"]:
        _updated_text, actions = apply_fixes(project_root, readme_path, readme_text, config)
        report["fixes_applied"] = actions
        refreshed_text = read_text(readme_path)
        post_schema, post_content, _ = validate_schema(readme_path, refreshed_text, config)
        report["post_fix_status"] = [issue.to_dict() for issue in [*post_schema, *post_content]]

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
