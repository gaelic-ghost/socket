#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Checklist ROADMAP maintainer with deterministic check-only and apply modes."""

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

H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
CHECKBOX_RE = re.compile(r"^\s*-\s+\[( |x)\]\s+.+$")
ANY_CHECKBOX_RE = re.compile(r"^\s*-\s+\[[^\]]\]\s+.+$")
MILESTONE_HEADING_RE = re.compile(r"^Milestone\s+(\d+)\s*:\s*(.+?)\s*$")
PROGRESS_LINE_RE = re.compile(r"^\s*-\s+Milestone\s+(\d+)\s*:\s*(.+?)\s+-\s+(.+?)\s*$")
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"<[^>]+>"),
]

MILESTONE_SLOT = "__MILESTONES__"


@dataclass
class Finding:
    finding_id: str
    category: str
    severity: str
    message: str
    file: str
    auto_fixable: bool

    def to_dict(self) -> Dict[str, object]:
        return {
            "finding_id": self.finding_id,
            "category": self.category,
            "severity": self.severity,
            "message": self.message,
            "file": self.file,
            "auto_fixable": self.auto_fixable,
        }


@dataclass
class ApplyAction:
    action: str
    reason: str
    file: str

    def to_dict(self) -> Dict[str, str]:
        return {"action": self.action, "reason": self.reason, "file": self.file}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit and optionally apply bounded checklist ROADMAP maintenance from a hard-enforced schema."
    )
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--roadmap-path", help="Optional roadmap path (default: <project-root>/ROADMAP.md)")
    parser.add_argument("--run-mode", required=True, choices=["check-only", "apply"], help="Execution mode")
    parser.add_argument("--config", help="Optional roadmap config override")
    parser.add_argument("--json-out", help="Write JSON report path")
    parser.add_argument("--md-out", help="Write markdown report path")
    parser.add_argument("--print-json", action="store_true", help="Print JSON report")
    parser.add_argument("--print-md", action="store_true", help="Print markdown report")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit non-zero when findings remain")
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
    default_path = Path(__file__).resolve().parents[1] / "config" / "roadmap-customization.template.yaml"
    default_config = read_yaml(default_path)
    loaded_path = default_path

    if config_override:
        override_path = Path(config_override).expanduser().resolve()
        merged = deep_merge(default_config, read_yaml(override_path))
        merged["isCustomized"] = True
        merged["configPath"] = str(override_path)
        merged["defaultConfigPath"] = str(default_path)
        return merged

    project_config = project_root / "config" / "roadmap-customization.yaml"
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
    value = settings.get("requiredSections", [])
    return [str(item) for item in value] if isinstance(value, list) else []


def section_order(settings: Dict[str, object]) -> List[str]:
    value = settings.get("sectionOrder", [])
    return [str(item) for item in value] if isinstance(value, list) else []


def required_milestone_subsections(settings: Dict[str, object]) -> List[str]:
    value = settings.get("requiredMilestoneSubsections", [])
    return [str(item) for item in value] if isinstance(value, list) else []


def status_values(settings: Dict[str, object]) -> List[str]:
    value = settings.get("statusValues", [])
    return [str(item) for item in value] if isinstance(value, list) else []


def section_aliases(settings: Dict[str, object]) -> Dict[str, List[str]]:
    raw = settings.get("sectionAliases", {})
    if not isinstance(raw, dict):
        return {}
    return {str(key): [str(item) for item in value] for key, value in raw.items() if isinstance(value, list)}


def subsection_aliases(settings: Dict[str, object]) -> Dict[str, List[str]]:
    raw = settings.get("milestoneSubsectionAliases", {})
    if not isinstance(raw, dict):
        return {}
    return {str(key): [str(item) for item in value] for key, value in raw.items() if isinstance(value, list)}


def section_templates(settings: Dict[str, object]) -> Dict[str, str]:
    raw = settings.get("sectionTemplates", {})
    if not isinstance(raw, dict):
        return {}
    return {str(key): str(value).strip() for key, value in raw.items()}


def milestone_subsection_templates(settings: Dict[str, object]) -> Dict[str, str]:
    raw = settings.get("milestoneSubsectionTemplates", {})
    if not isinstance(raw, dict):
        return {}
    return {str(key): str(value).strip() for key, value in raw.items()}


def allow_additional_sections(settings: Dict[str, object]) -> bool:
    return bool(settings.get("allowAdditionalSections", True))


def preserve_preamble(settings: Dict[str, object]) -> bool:
    return bool(settings.get("preservePreamble", True))


def slugify_heading(heading: str) -> str:
    slug = heading.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def build_toc(headings: Sequence[str]) -> str:
    return "\n".join(f"- [{heading}](#{slugify_heading(heading)})" for heading in headings)


def toc_entries(body: str) -> List[str]:
    entries: List[str] = []
    for line in body.splitlines():
        match = re.match(r"^\s*-\s+\[(.+?)\]\(#(.+?)\)\s*$", line.strip())
        if match:
            entries.append(match.group(1).strip())
    return entries


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


def section_map(sections: Sequence[Tuple[str, str]]) -> Dict[str, str]:
    return {heading: body for heading, body in sections}


def parse_title(preamble: str) -> Tuple[Optional[str], List[str]]:
    lines = [line.rstrip() for line in preamble.splitlines()]
    title: Optional[str] = None
    extras: List[str] = []
    title_index: Optional[int] = None

    for idx, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            title_index = idx
            break

    if title_index is None:
        return None, lines

    for idx, line in enumerate(lines):
        if idx == title_index:
            continue
        extras.append(line)
    return title, extras


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


def normalize_preamble(preamble: str, keep_extras: bool) -> str:
    title, extras = parse_title(preamble)
    normalized_title = title or "Project Roadmap"

    lines = [f"# {normalized_title}"]
    if keep_extras:
        extra_lines = collapse_blank_lines(extras)
        if extra_lines:
            lines.extend(["", *extra_lines])
    return "\n".join(lines).strip()


def is_milestone_heading(heading: str) -> bool:
    return MILESTONE_HEADING_RE.match(heading) is not None


def parse_milestone_heading(heading: str) -> Optional[Tuple[int, str]]:
    match = MILESTONE_HEADING_RE.match(heading)
    if not match:
        return None
    return int(match.group(1)), match.group(2).strip()


def parse_progress(body: str) -> Dict[int, Tuple[str, str]]:
    progress: Dict[int, Tuple[str, str]] = {}
    for line in body.splitlines():
        match = PROGRESS_LINE_RE.match(line)
        if match:
            progress[int(match.group(1))] = (match.group(2).strip(), match.group(3).strip())
    return progress


def alias_lookup(settings: Dict[str, object]) -> Dict[str, str]:
    aliases = section_aliases(settings)
    reverse: Dict[str, str] = {}
    for canonical, names in aliases.items():
        for alias in names:
            reverse[alias] = canonical
    return reverse


def subsection_alias_lookup(settings: Dict[str, object]) -> Dict[str, str]:
    aliases = subsection_aliases(settings)
    reverse: Dict[str, str] = {}
    for canonical, names in aliases.items():
        for alias in names:
            reverse[alias] = canonical
    return reverse


def render_template_bootstrap() -> str:
    template_path = Path(__file__).resolve().parents[1] / "assets" / "ROADMAP.template.md"
    return normalize_whitespace(read_text(template_path))


def has_legacy_format(text: str) -> bool:
    if re.search(r"^##\s+Current Milestone\s*$", text, flags=re.MULTILINE):
        return True
    if re.search(r"^##\s+Milestones\s*$", text, flags=re.MULTILINE) and "|" in text:
        return True
    if re.search(r"\|\s*Milestone\s*\|", text, flags=re.IGNORECASE):
        return True
    return False


def parse_legacy_milestones(text: str) -> List[Tuple[int, str, str]]:
    rows: List[Tuple[int, str, str]] = []
    lines = text.splitlines()
    in_table = False
    for line in lines:
        if re.match(r"^\|\s*Milestone\s*\|", line, flags=re.IGNORECASE):
            in_table = True
            continue
        if in_table and re.match(r"^\|\s*[-:]+\s*\|", line):
            continue
        if in_table and line.strip().startswith("|"):
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) >= 2:
                name = cols[0]
                status = cols[1]
                match = re.search(r"(\d+)", name)
                idx = int(match.group(1)) if match else len(rows)
                title = re.sub(r"^Milestone\s*\d+\s*[:\-]?\s*", "", name, flags=re.IGNORECASE).strip() or name
                rows.append((idx, title, status))
        elif in_table and line.strip() == "":
            in_table = False
    return sorted(rows, key=lambda item: item[0])


def build_migrated_from_legacy(text: str, settings: Dict[str, object]) -> str:
    rows = parse_legacy_milestones(text)
    if not rows:
        rows = [(0, "Foundation", "Planned")]

    section_template_map = section_templates(settings)
    subsection_template_map = milestone_subsection_templates(settings)
    required = required_sections(settings)
    order = section_order(settings)
    milestone_children = required_milestone_subsections(settings)

    section_bodies: Dict[str, str] = {
        "Vision": "- Preserve the long-term project direction while migrating this roadmap into checklist format.",
        "Product Principles": "- Keep roadmap updates checklist-based, reviewable, and tied to real delivery.",
        "Backlog Candidates": section_template_map.get("Backlog Candidates", ""),
    }

    milestones: List[Tuple[int, str, str]] = []
    for idx, title, status in rows:
        lines: List[str] = []
        for child in milestone_children:
            template = subsection_template_map.get(child, "")
            if child == "Status":
                template = status.strip() or template
            elif child == "Scope":
                template = f"- [ ] Preserve or restate the milestone scope from the legacy roadmap entry ({status})."
            elif child == "Tickets":
                template = "- [ ] Reconcile legacy milestone work into explicit checklist tickets."
            elif child == "Exit Criteria":
                template = "- [ ] Confirm this migrated milestone is complete, current, and internally consistent."
            lines.extend([f"### {child}", "", template.strip(), ""])
        milestones.append((idx, title, "\n".join(lines).strip()))

    progress_lines = [f"- Milestone {idx}: {title} - {status.strip() or 'Planned'}" for idx, title, status in rows]
    section_bodies["Milestone Progress"] = "\n".join(progress_lines).strip()

    return render_document(
        title="Project Roadmap",
        preamble_lines=[],
        ordered_section_bodies=section_bodies,
        milestones=milestones,
        extra_sections=[],
        order=order,
        required=required,
        allow_additional=allow_additional_sections(settings),
    )


def normalize_milestone_subsection_body(body: str, subsection_name: str) -> str:
    normalized_lines: List[str] = []
    for line in body.splitlines():
        fixed = re.sub(r"^\s*-\s+\[(X)\]\s+", "- [x] ", line)
        if "[P]" in fixed and subsection_name != "Tickets":
            fixed = fixed.replace("[P]", "").replace("  ", " ").rstrip()
        normalized_lines.append(fixed)
    return "\n".join(normalized_lines).strip()


def render_milestone_body(existing_body: str, settings: Dict[str, object]) -> str:
    required_children = required_milestone_subsections(settings)
    template_map = milestone_subsection_templates(settings)
    alias_map = subsection_alias_lookup(settings)
    _preamble, subsections = split_subsections(existing_body)
    canonical_lookup: Dict[str, str] = {}

    for name, body in subsections:
        canonical = alias_map.get(name, name)
        canonical_lookup[canonical] = body

    lines: List[str] = []
    for idx, child in enumerate(required_children):
        child_body = canonical_lookup.get(child, "").strip() or template_map.get(child, "")
        child_body = normalize_milestone_subsection_body(child_body, child)
        lines.extend([f"### {child}", "", child_body.strip()])
        if idx < len(required_children) - 1:
            lines.append("")

    extras = [(name, body) for name, body in subsections if alias_map.get(name, name) not in set(required_children)]
    if extras:
        lines.append("")
        for idx, (name, body) in enumerate(extras):
            lines.extend([f"### {name}", "", body.strip()])
            if idx < len(extras) - 1:
                lines.append("")

    return "\n".join(lines).strip()


def render_document(
    title: str,
    preamble_lines: Sequence[str],
    ordered_section_bodies: Dict[str, str],
    milestones: Sequence[Tuple[int, str, str]],
    extra_sections: Sequence[Tuple[str, str]],
    order: Sequence[str],
    required: Sequence[str],
    allow_additional: bool,
) -> str:
    rendered_lines: List[str] = [f"# {title}"]
    if preamble_lines:
        rendered_lines.extend(["", *preamble_lines])

    toc_headings: List[str] = []
    for item in order:
        if item == MILESTONE_SLOT:
            toc_headings.extend(f"Milestone {idx}: {name}" for idx, name, _body in milestones)
        else:
            toc_headings.append(item)
    if allow_additional:
        toc_headings.extend(heading for heading, _body in extra_sections)

    rendered_lines.extend(["", "## Table of Contents", "", build_toc(toc_headings)])

    for item in order:
        if item == MILESTONE_SLOT:
            for idx, name, body in milestones:
                rendered_lines.extend(["", f"## Milestone {idx}: {name}", "", body.strip()])
            continue
        body = ordered_section_bodies.get(item, "").strip()
        rendered_lines.extend(["", f"## {item}", "", body])

    if allow_additional:
        for heading, body in extra_sections:
            rendered_lines.extend(["", f"## {heading}", "", body.strip()])

    return normalize_whitespace("\n".join(rendered_lines))


def validate_schema(
    roadmap_path: Path,
    roadmap_text: str,
    config: Dict[str, object],
) -> List[Finding]:
    settings = config_settings(config)
    required = required_sections(settings)
    section_alias_map = alias_lookup(settings)
    milestone_child_alias_map = subsection_alias_lookup(settings)
    required_children = required_milestone_subsections(settings)
    allowed_status_values = status_values(settings)

    findings: List[Finding] = []
    preamble, sections = split_sections(roadmap_text)
    lookup = section_map(sections)
    title, _extras = parse_title(preamble)

    if not title:
        findings.append(
            Finding(
                finding_id="missing-title",
                category="schema",
                severity="high",
                message="ROADMAP is missing a top-level '# <title>' heading.",
                file=str(roadmap_path),
                auto_fixable=True,
            )
        )

    if "Table of Contents" not in lookup:
        findings.append(
            Finding(
                finding_id="missing-table-of-contents",
                category="schema",
                severity="medium",
                message="ROADMAP is missing the required '## Table of Contents' section.",
                file=str(roadmap_path),
                auto_fixable=True,
            )
        )

    headings = [heading for heading, _body in sections]
    milestones = [(heading, body) for heading, body in sections if is_milestone_heading(heading)]
    milestone_numbers: List[int] = []

    for heading in required:
        if heading not in lookup:
            alias_found = next((alias for alias, canonical in section_alias_map.items() if canonical == heading and alias in lookup), None)
            if alias_found:
                findings.append(
                    Finding(
                        finding_id=f"non-canonical-heading-{slugify_heading(heading)}",
                        category="schema",
                        severity="medium",
                        message=f"ROADMAP uses alias heading '## {alias_found}' where the canonical schema expects '## {heading}'.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )
            else:
                findings.append(
                    Finding(
                        finding_id=f"missing-section-{slugify_heading(heading)}",
                        category="schema",
                        severity="high",
                        message=f"ROADMAP is missing required section '## {heading}'.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )

    if not milestones:
        findings.append(
            Finding(
                finding_id="missing-milestones",
                category="schema",
                severity="high",
                message="ROADMAP is missing milestone sections (expected headings like '## Milestone N: Name').",
                file=str(roadmap_path),
                auto_fixable=True,
            )
        )

    for heading, body in milestones:
        parsed = parse_milestone_heading(heading)
        if not parsed:
            continue
        number, _name = parsed
        milestone_numbers.append(number)
        _sub_preamble, subsections = split_subsections(body)
        found_names = [milestone_child_alias_map.get(name, name) for name, _sub_body in subsections]
        subsection_lookup = {milestone_child_alias_map.get(name, name): sub_body for name, sub_body in subsections}
        for child in required_children:
            if child not in found_names:
                findings.append(
                    Finding(
                        finding_id=f"milestone-{number}-missing-{slugify_heading(child)}",
                        category="schema",
                        severity="high",
                        message=f"Milestone {number} is missing required subsection '### {child}'.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )
                continue
            lines = [line for line in subsection_lookup[child].splitlines() if line.strip()]
            if child != "Status" and not any(CHECKBOX_RE.match(line) for line in lines):
                findings.append(
                    Finding(
                        finding_id=f"milestone-{number}-{slugify_heading(child)}-missing-checklists",
                        category="schema",
                        severity="medium",
                        message=f"Milestone {number} subsection '{child}' should contain checklist items.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )
        status_body = subsection_lookup.get("Status", "").strip()
        if status_body:
            status_lines = [line.strip() for line in status_body.splitlines() if line.strip()]
            if len(status_lines) != 1:
                findings.append(
                    Finding(
                        finding_id=f"milestone-{number}-status-format",
                        category="schema",
                        severity="medium",
                        message=f"Milestone {number} status should be a single plain status value.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )
            elif allowed_status_values and status_lines[0] not in allowed_status_values:
                findings.append(
                    Finding(
                        finding_id=f"milestone-{number}-invalid-status",
                        category="schema",
                        severity="medium",
                        message=f"Milestone {number} status '{status_lines[0]}' is not in the allowed status vocabulary.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )

        current_block = ""
        for line in body.splitlines():
            if line.startswith("### "):
                current_block = milestone_child_alias_map.get(line[4:].strip(), line[4:].strip())
                continue
            if ANY_CHECKBOX_RE.match(line) and not CHECKBOX_RE.match(line):
                findings.append(
                    Finding(
                        finding_id=f"invalid-checkbox-milestone-{number}-{slugify_heading(line)}",
                        category="schema",
                        severity="medium",
                        message=f"Milestone {number} contains invalid checkbox syntax; use [ ] or [x].",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )
            if "[P]" in line and current_block != "Tickets":
                findings.append(
                    Finding(
                        finding_id=f"parallel-marker-milestone-{number}",
                        category="schema",
                        severity="medium",
                        message=f"Milestone {number} uses '[P]' outside the 'Tickets' subsection.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )

        if any(pattern.search(body) for pattern in PLACEHOLDER_PATTERNS):
            findings.append(
                Finding(
                    finding_id=f"placeholder-content-milestone-{number}",
                    category="content-quality",
                    severity="medium",
                    message=f"Milestone {number} contains placeholder-style content.",
                    file=str(roadmap_path),
                    auto_fixable=False,
                )
            )

    if milestone_numbers and milestone_numbers != sorted(milestone_numbers):
        findings.append(
            Finding(
                finding_id="milestone-order",
                category="schema",
                severity="medium",
                message="Milestone sections are not in deterministic ascending order.",
                file=str(roadmap_path),
                auto_fixable=True,
            )
        )

    if "Milestone Progress" in lookup and milestones:
        progress = parse_progress(lookup["Milestone Progress"])
        parsed_milestones = [
            parsed
            for parsed in (parse_milestone_heading(heading) for heading, _body in milestones)
            if parsed is not None
        ]
        milestone_statuses: Dict[int, str] = {}
        for heading, body in milestones:
            parsed = parse_milestone_heading(heading)
            if not parsed:
                continue
            number, _name = parsed
            _sub_preamble, subsections = split_subsections(body)
            subsection_lookup = {milestone_child_alias_map.get(name, name): sub_body for name, sub_body in subsections}
            status_lines = [line.strip() for line in subsection_lookup.get("Status", "").splitlines() if line.strip()]
            milestone_statuses[number] = status_lines[0] if status_lines else ""
        expected = [
            f"Milestone {number}: {name} - {milestone_statuses.get(number, '').strip()}"
            for number, name in sorted(parsed_milestones, key=lambda item: item[0])
        ]
        actual = [f"Milestone {number}: {title} - {status}" for number, (title, status) in sorted(progress.items())]
        if actual != expected:
            findings.append(
                Finding(
                    finding_id="stale-milestone-progress",
                    category="schema",
                    severity="medium",
                    message="Milestone Progress does not match the current milestone section list, order, and statuses.",
                    file=str(roadmap_path),
                    auto_fixable=True,
                )
            )

    if "Table of Contents" in lookup:
        expected_toc = [heading for heading, _body in sections if heading != "Table of Contents"]
        actual_toc = toc_entries(lookup["Table of Contents"])
        if actual_toc != expected_toc:
            findings.append(
                Finding(
                    finding_id="stale-table-of-contents",
                    category="schema",
                    severity="low",
                    message="Table of contents entries do not match the canonical roadmap headings in order.",
                    file=str(roadmap_path),
                    auto_fixable=True,
                )
            )

    positions = {heading: index for index, heading in enumerate(headings)}
    if "Milestone Progress" in positions and milestones:
        first_milestone_position = min(positions[heading] for heading, _body in milestones)
        if positions["Milestone Progress"] > first_milestone_position:
            findings.append(
                Finding(
                    finding_id="milestone-progress-order",
                    category="schema",
                    severity="medium",
                    message="'Milestone Progress' should appear before milestone sections.",
                    file=str(roadmap_path),
                    auto_fixable=True,
                )
            )
    if "Backlog Candidates" in positions and milestones:
        last_milestone_position = max(positions[heading] for heading, _body in milestones)
        if positions["Backlog Candidates"] < last_milestone_position:
            findings.append(
                Finding(
                    finding_id="backlog-order",
                    category="schema",
                    severity="medium",
                    message="'Backlog Candidates' should appear after milestone sections.",
                    file=str(roadmap_path),
                    auto_fixable=True,
                )
            )

    if has_legacy_format(roadmap_text):
        findings.append(
            Finding(
                finding_id="legacy-format",
                category="schema",
                severity="high",
                message="Legacy roadmap sections detected (`Current Milestone` / `Milestones` table).",
                file=str(roadmap_path),
                auto_fixable=True,
            )
        )

    return findings


def apply_fixes(project_root: Path, roadmap_path: Path, roadmap_text: str, config: Dict[str, object]) -> Tuple[str, List[ApplyAction]]:
    if not roadmap_text.strip():
        bootstrap = render_template_bootstrap()
        write_text(roadmap_path, bootstrap)
        return (
            bootstrap,
            [
                ApplyAction(
                    action="create-roadmap-from-template",
                    reason="Created a missing ROADMAP.md from the bundled canonical roadmap template.",
                    file=str(roadmap_path),
                )
            ],
        )

    settings = config_settings(config)
    required = required_sections(settings)
    order = section_order(settings)
    section_alias_map = alias_lookup(settings)
    template_map = section_templates(settings)
    allow_additional = allow_additional_sections(settings)
    keep_preamble = preserve_preamble(settings)

    if has_legacy_format(roadmap_text):
        migrated = build_migrated_from_legacy(roadmap_text, settings)
        write_text(roadmap_path, migrated)
        return (
            migrated,
            [
                ApplyAction(
                    action="migrate-legacy-roadmap",
                    reason="Migrated a legacy roadmap layout into the canonical checklist roadmap structure.",
                    file=str(roadmap_path),
                )
            ],
        )

    preamble, sections = split_sections(roadmap_text)
    normalized_preamble = normalize_preamble(preamble, keep_preamble)
    title, preamble_extras = parse_title(normalized_preamble)
    title = title or "Project Roadmap"
    preamble_lines = collapse_blank_lines(preamble_extras) if keep_preamble else []
    existing_lookup = section_map(sections)

    section_bodies: Dict[str, str] = {}
    extra_sections: List[Tuple[str, str]] = []
    milestones: List[Tuple[int, str, str]] = []
    progress = parse_progress(existing_lookup.get("Milestone Progress", ""))
    used_aliases: List[str] = []

    for heading, body in sections:
        if heading == "Table of Contents":
            continue
        parsed = parse_milestone_heading(heading)
        if parsed:
            number, name = parsed
            milestones.append((number, name, render_milestone_body(body, settings)))
            continue
        canonical = section_alias_map.get(heading, heading)
        if canonical in required:
            if heading != canonical:
                used_aliases.append(heading)
            section_bodies[canonical] = body.strip()
        elif allow_additional:
            extra_sections.append((heading, body.strip()))

    if not milestones:
        template_text = render_template_bootstrap()
        _template_preamble, template_sections = split_sections(template_text)
        for heading, body in template_sections:
            if is_milestone_heading(heading):
                parsed = parse_milestone_heading(heading)
                if parsed:
                    milestones.append((parsed[0], parsed[1], body.strip()))

    milestones = sorted(milestones, key=lambda item: item[0])

    for heading in required:
        if heading == "Milestone Progress":
            continue
        body = section_bodies.get(heading, "").strip() or template_map.get(heading, "")
        section_bodies[heading] = body.strip()

    milestone_alias_map = subsection_alias_lookup(settings)
    progress_lines = []
    for number, name, body in milestones:
        _sub_preamble, subsections = split_subsections(body)
        subsection_lookup = {milestone_alias_map.get(subheading, subheading): sub_body for subheading, sub_body in subsections}
        status_line_candidates = [line.strip() for line in subsection_lookup.get("Status", "").splitlines() if line.strip()]
        status_value = status_line_candidates[0] if status_line_candidates else progress.get(number, (name, "Planned"))[1]
        progress_lines.append(f"- Milestone {number}: {name} - {status_value}")
    section_bodies["Milestone Progress"] = "\n".join(progress_lines).strip()

    updated = render_document(
        title=title,
        preamble_lines=preamble_lines,
        ordered_section_bodies=section_bodies,
        milestones=milestones,
        extra_sections=extra_sections,
        order=order,
        required=required,
        allow_additional=allow_additional,
    )

    actions: List[ApplyAction] = []
    if updated != normalize_whitespace(roadmap_text):
        write_text(roadmap_path, updated)
        actions.append(
            ApplyAction(
                action="normalize-roadmap-schema",
                reason="Normalized the roadmap into the configured canonical checklist structure.",
                file=str(roadmap_path),
            )
        )
    if used_aliases:
        actions.append(
            ApplyAction(
                action="migrate-alias-headings",
                reason=f"Migrated alias headings into canonical heading names: {', '.join(sorted(set(used_aliases)))}.",
                file=str(roadmap_path),
            )
        )

    return updated, actions


def markdown_report(report: Dict[str, object]) -> str:
    lines = [
        "# Maintain Project Roadmap Report",
        "",
        "## Run Context",
        "",
        f"- Project root: `{report['run_context']['project_root']}`",
        f"- Roadmap path: `{report['run_context']['roadmap_path']}`",
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
        f"- Required milestone subsections: `{', '.join(report['schema_contract'].get('required_milestone_subsections', []))}`",
        "",
        "## Findings",
        "",
    ]

    if report["findings"]:
        lines.extend(
            f"- `{finding['severity']}` `{finding['finding_id']}`: {finding['message']}"
            for finding in report["findings"]
        )
    else:
        lines.append("- None.")

    lines.extend(["", "## Changes Applied", ""])
    if report["apply_actions"]:
        lines.extend(f"- `{action['action']}`: {action['reason']}" for action in report["apply_actions"])
    else:
        lines.append("- None.")

    lines.extend(["", "## Errors", ""])
    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- None.")

    return "\n".join(lines).rstrip() + "\n"


def unresolved_issues(report: Dict[str, object]) -> List[Dict[str, object]]:
    return list(report["findings"])


def schema_contract(config: Dict[str, object]) -> Dict[str, object]:
    settings = config_settings(config)
    return {
        "required_sections": required_sections(settings),
        "section_order": section_order(settings),
        "required_milestone_subsections": required_milestone_subsections(settings),
        "status_values": status_values(settings),
    }


def run_maintenance(args: argparse.Namespace) -> Tuple[Dict[str, object], str]:
    project_root = Path(args.project_root).expanduser().resolve()
    roadmap_path = Path(args.roadmap_path).expanduser().resolve() if args.roadmap_path else (project_root / "ROADMAP.md")

    report: Dict[str, object] = {
        "run_context": {
            "project_root": str(project_root),
            "roadmap_path": str(roadmap_path),
            "run_mode": args.run_mode,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        },
        "customization_state": {},
        "schema_contract": {},
        "findings": [],
        "apply_actions": [],
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

    if roadmap_path.is_file():
        roadmap_text = read_text(roadmap_path)
        findings = validate_schema(roadmap_path, roadmap_text, config)
        report["findings"] = [finding.to_dict() for finding in findings]
    elif args.run_mode == "apply":
        roadmap_text = ""
        report["findings"] = [
            Finding(
                finding_id="missing-roadmap",
                category="schema",
                severity="high",
                message=f"ROADMAP file is missing at {roadmap_path}.",
                file=str(roadmap_path),
                auto_fixable=True,
            ).to_dict()
        ]
    else:
        report["errors"].append(f"ROADMAP path does not exist: {roadmap_path}")
        return report, markdown_report(report)

    if args.run_mode == "apply" and not report["errors"]:
        updated_text, actions = apply_fixes(project_root, roadmap_path, roadmap_text, config)
        report["apply_actions"] = [action.to_dict() for action in actions]
        post_findings = validate_schema(roadmap_path, updated_text, config)
        report["findings"] = [finding.to_dict() for finding in post_findings]

    markdown = markdown_report(report)
    return report, markdown


def main() -> int:
    args = parse_args()
    report, markdown = run_maintenance(args)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.json_out:
        write_text(Path(args.json_out), payload)
    if args.md_out:
        write_text(Path(args.md_out), markdown)

    if args.print_json:
        sys.stdout.write(payload)
    elif args.print_md:
        sys.stdout.write(markdown)
    else:
        if not unresolved_issues(report) and not report["apply_actions"] and not report["errors"]:
            sys.stdout.write("No findings.\n")
        else:
            sys.stdout.write(markdown)

    if report["errors"]:
        return 1
    if args.fail_on_issues and (unresolved_issues(report) or report["errors"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
