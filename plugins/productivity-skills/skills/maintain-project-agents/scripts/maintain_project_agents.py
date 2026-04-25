#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Audit and apply bounded AGENTS.md maintenance from a hard-enforced schema."""

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
SHELL_FENCE_RE = re.compile(r"```([^\n`]*)\n(.*?)```", re.DOTALL)
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"<[^>]+>"),
]


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
        description="Audit and optionally apply bounded AGENTS.md maintenance from a hard-enforced schema."
    )
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--agents-path", help="Optional AGENTS path override")
    parser.add_argument("--run-mode", required=True, choices=["check-only", "apply"], help="Execution mode")
    parser.add_argument("--config", help="Optional AGENTS config override")
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


def split_sections(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    matches = list(H2_RE.finditer(text))
    if not matches:
        return text.strip(), []

    preamble = text[: matches[0].start()].rstrip()
    sections: List[Tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections.append((match.group(1).strip(), text[start:end].strip("\n")))
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
        subsections.append((match.group(1).strip(), body[start:end].strip("\n")))
    return preamble, subsections


def section_map(sections: Sequence[Tuple[str, str]]) -> Dict[str, str]:
    return {heading: body for heading, body in sections}


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


def normalize_preamble(preamble: str, preserve_preamble: bool) -> str:
    lines = [line.rstrip() for line in preamble.splitlines()]
    title_present = any(line.startswith("# ") for line in lines)
    summary: Optional[str] = None
    extras: List[str] = []

    for idx, line in enumerate(lines):
        if line.startswith("# "):
            for follow in lines[idx + 1 :]:
                if follow.strip():
                    summary = follow.strip()
                    break
            break

    for line in lines:
        if line.startswith("# "):
            continue
        if summary is None and line.strip():
            summary = line.strip()
            continue
        extras.append(line)

    normalized_title = "# AGENTS.md" if not title_present else next(line for line in lines if line.startswith("# "))
    normalized_summary = (
        summary
        or "Use this file for durable repo-local guidance that Codex should follow before changing code, docs, or project workflow surfaces in this repository."
    )
    output = [normalized_title, "", normalized_summary]
    if preserve_preamble:
        extra_lines = collapse_blank_lines(extras)
        if extra_lines:
            output.extend(["", *extra_lines])
    return "\n".join(output).strip()


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
    default_path = Path(__file__).resolve().parents[1] / "config" / "agents-customization.template.yaml"
    default_config = read_yaml(default_path)
    loaded_path = default_path

    if config_override:
        override_path = Path(config_override).expanduser().resolve()
        merged = deep_merge(default_config, read_yaml(override_path))
        merged["isCustomized"] = True
        merged["configPath"] = str(override_path)
        merged["defaultConfigPath"] = str(default_path)
        return merged

    project_config = project_root / "config" / "agents-customization.yaml"
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
    values = settings.get("requiredSections", [])
    return [str(item) for item in values] if isinstance(values, list) else []


def canonical_order(settings: Dict[str, object]) -> List[str]:
    values = settings.get("sectionOrder", [])
    return [str(item) for item in values] if isinstance(values, list) else []


def required_subsections(settings: Dict[str, object]) -> Dict[str, List[str]]:
    raw = settings.get("requiredSubsections", {})
    if not isinstance(raw, dict):
        return {}
    return {
        str(key): [str(item) for item in value]
        for key, value in raw.items()
        if isinstance(value, list)
    }


def section_aliases(settings: Dict[str, object]) -> Dict[str, List[str]]:
    raw = settings.get("sectionAliases", {})
    if not isinstance(raw, dict):
        return {}
    return {
        str(key): [str(item) for item in value]
        for key, value in raw.items()
        if isinstance(value, list)
    }


def subsection_aliases(settings: Dict[str, object]) -> Dict[str, List[str]]:
    raw = settings.get("subsectionAliases", {})
    if not isinstance(raw, dict):
        return {}
    return {
        str(key): [str(item) for item in value]
        for key, value in raw.items()
        if isinstance(value, list)
    }


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


def section_alias_lookup(settings: Dict[str, object]) -> Dict[str, str]:
    reverse: Dict[str, str] = {}
    for canonical, aliases in section_aliases(settings).items():
        for alias in aliases:
            reverse[alias] = canonical
    return reverse


def subsection_alias_lookup(settings: Dict[str, object]) -> Dict[Tuple[str, str], str]:
    reverse: Dict[Tuple[str, str], str] = {}
    for canonical_path, aliases in subsection_aliases(settings).items():
        if "/" not in canonical_path:
            continue
        parent, canonical_name = canonical_path.split("/", 1)
        for alias in aliases:
            reverse[(parent, alias)] = canonical_name
    return reverse


def render_template_bootstrap() -> str:
    template_path = Path(__file__).resolve().parents[1] / "assets" / "AGENTS.template.md"
    return normalize_whitespace(read_text(template_path))


def render_section_body(heading: str, existing_body: str, settings: Dict[str, object]) -> str:
    required_children = required_subsections(settings).get(heading, [])
    section_template_map = section_templates(settings)
    subsection_template_map = subsection_templates(settings)
    subsection_alias_map = subsection_alias_lookup(settings)

    if not required_children:
        return existing_body.strip() or section_template_map.get(heading, "")

    preamble, subsections = split_subsections(existing_body)
    subsection_lookup: Dict[str, str] = {}
    extra_subsections: List[Tuple[str, str]] = []
    for name, body in subsections:
        canonical_name = subsection_alias_map.get((heading, name), name)
        if canonical_name in required_children and canonical_name not in subsection_lookup:
            subsection_lookup[canonical_name] = body
        else:
            extra_subsections.append((name, body))

    lines: List[str] = []
    if preamble.strip():
        lines.extend([preamble.strip(), ""])

    for idx, child in enumerate(required_children):
        body = subsection_lookup.get(child, "").strip() or subsection_template_map.get(f"{heading}/{child}", "")
        lines.extend([f"### {child}", "", body.strip()])
        if idx < len(required_children) - 1 or extra_subsections:
            lines.append("")

    for idx, (name, body) in enumerate(extra_subsections):
        lines.extend([f"### {name}", "", body.strip()])
        if idx < len(extra_subsections) - 1:
            lines.append("")

    rendered = "\n".join(lines).strip()
    return rendered or section_template_map.get(heading, "")


def validate_schema(
    agents_path: Path,
    agents_text: str,
    config: Dict[str, object],
) -> Tuple[List[Issue], List[Issue], List[Issue], List[Issue]]:
    settings = config_settings(config)
    required = required_sections(settings)
    order = canonical_order(settings)
    subsection_map = required_subsections(settings)
    section_alias_map = section_alias_lookup(settings)
    subsection_alias_map = subsection_alias_lookup(settings)

    schema_issues: List[Issue] = []
    workflow_issues: List[Issue] = []
    validation_issues: List[Issue] = []
    boundary_issues: List[Issue] = []

    preamble, sections = split_sections(agents_text)
    lookup = section_map(sections)

    if not any(line.startswith("# ") for line in preamble.splitlines()):
        schema_issues.append(
            Issue(
                issue_id="missing-title",
                category="schema",
                severity="high",
                file=str(agents_path),
                evidence="AGENTS.md is missing a top-level '# AGENTS.md' title.",
                recommended_fix="Add a clear AGENTS.md title at the top of the file.",
                auto_fixable=True,
            )
        )

    if len([line for line in preamble.splitlines() if line.strip()]) < 2:
        schema_issues.append(
            Issue(
                issue_id="missing-summary",
                category="schema",
                severity="medium",
                file=str(agents_path),
                evidence="AGENTS.md is missing a short repo-local preamble beneath the title.",
                recommended_fix="Add a short preamble explaining what this AGENTS file governs.",
                auto_fixable=True,
            )
        )

    observed = [heading for heading, _body in sections]
    positions = {heading: idx for idx, heading in enumerate(observed)}
    for heading in required:
        if heading in lookup:
            continue
        alias_found = next(
            (alias for alias, canonical in section_alias_map.items() if canonical == heading and alias in lookup),
            None,
        )
        if alias_found:
            schema_issues.append(
                Issue(
                    issue_id=f"non-canonical-heading-{heading.lower().replace(' ', '-')}",
                    category="schema",
                    severity="medium",
                    file=str(agents_path),
                    evidence=f"AGENTS.md uses alias heading '## {alias_found}' where the canonical schema expects '## {heading}'.",
                    recommended_fix=f"Rename '## {alias_found}' to '## {heading}'.",
                    auto_fixable=True,
                )
            )
        else:
            schema_issues.append(
                Issue(
                    issue_id=f"missing-section-{heading.lower().replace(' ', '-')}",
                    category="schema",
                    severity="high",
                    file=str(agents_path),
                    evidence=f"AGENTS.md is missing required section '## {heading}'.",
                    recommended_fix=f"Add the required '## {heading}' section.",
                    auto_fixable=True,
                )
            )

    order_positions: List[int] = []
    for heading in order:
        if heading in positions:
            order_positions.append(positions[heading])
            continue
        alias_found = next(
            (alias for alias, canonical in section_alias_map.items() if canonical == heading and alias in positions),
            None,
        )
        if alias_found:
            order_positions.append(positions[alias_found])
    if order_positions and order_positions != sorted(order_positions):
        schema_issues.append(
            Issue(
                issue_id="canonical-section-order",
                category="schema",
                severity="medium",
                file=str(agents_path),
                evidence="Canonical AGENTS sections are not in the configured order.",
                recommended_fix="Normalize the top-level sections into canonical order.",
                auto_fixable=True,
            )
        )

    for parent, children in subsection_map.items():
        body = lookup.get(parent, "")
        if not body:
            alias_parent = next(
                (alias for alias, canonical in section_alias_map.items() if canonical == parent and alias in lookup),
                None,
            )
            body = lookup.get(alias_parent, "") if alias_parent else ""
        if not body:
            continue
        _sub_preamble, subsections = split_subsections(body)
        found = {
            subsection_alias_map.get((parent, name), name): subsection_body
            for name, subsection_body in subsections
        }
        for child in children:
            if child not in found:
                schema_issues.append(
                    Issue(
                        issue_id=f"missing-subsection-{parent.lower().replace(' ', '-')}-{child.lower().replace(' ', '-')}",
                        category="schema",
                        severity="high",
                        file=str(agents_path),
                        evidence=f"Section '## {parent}' is missing required subsection '### {child}'.",
                        recommended_fix=f"Add the required subsection '### {child}' under '## {parent}'.",
                        auto_fixable=True,
                    )
                )

    if any(pattern.search(agents_text) for pattern in PLACEHOLDER_PATTERNS):
        workflow_issues.append(
            Issue(
                issue_id="placeholder-content",
                category="workflow-drift",
                severity="medium",
                file=str(agents_path),
                evidence="AGENTS.md still contains TODO, TBD, or angle-bracket placeholder content.",
                recommended_fix="Replace placeholder text with grounded repository guidance.",
                auto_fixable=False,
            )
        )

    commands_body = lookup.get("Commands", "")
    _cmd_preamble, cmd_subsections = split_subsections(commands_body)
    cmd_lookup = {subsection_alias_map.get(("Commands", name), name): body for name, body in cmd_subsections}
    for child in ("Setup", "Validation"):
        body = cmd_lookup.get(child, "").strip()
        if not body:
            continue
        fences = list(SHELL_FENCE_RE.finditer(body))
        if not fences:
            validation_issues.append(
                Issue(
                    issue_id=f"missing-command-block-{child.lower()}",
                    category="validation-drift",
                    severity="medium",
                    file=str(agents_path),
                    evidence=f"Commands > {child} should include grounded command examples, preferably in fenced code blocks.",
                    recommended_fix=f"Add a fenced code block with grounded {child.lower()} commands.",
                    auto_fixable=False,
                )
            )
            continue
        for match in fences:
            info = match.group(1).strip()
            block = match.group(2).strip()
            if not info:
                validation_issues.append(
                    Issue(
                        issue_id=f"missing-code-fence-info-string-{child.lower()}-{match.start()}",
                        category="validation-drift",
                        severity="low",
                        file=str(agents_path),
                        evidence=f"Commands > {child} uses a fenced code block without a language info string.",
                        recommended_fix="Use fenced code blocks with an info string such as ```bash for command examples.",
                        auto_fixable=False,
                    )
                )
            if not block:
                validation_issues.append(
                    Issue(
                        issue_id=f"empty-command-block-{child.lower()}-{match.start()}",
                        category="validation-drift",
                        severity="medium",
                        file=str(agents_path),
                        evidence=f"Commands > {child} contains an empty fenced code block.",
                        recommended_fix="Remove the empty block or replace it with grounded commands.",
                        auto_fixable=True,
                    )
                )
            if any(pattern.search(block) for pattern in PLACEHOLDER_PATTERNS):
                validation_issues.append(
                    Issue(
                        issue_id=f"placeholder-command-block-{child.lower()}-{match.start()}",
                        category="validation-drift",
                        severity="high",
                        file=str(agents_path),
                        evidence=f"Commands > {child} contains a placeholder command block.",
                        recommended_fix="Replace the placeholder command block with grounded commands or prose.",
                        auto_fixable=False,
                    )
                )

    where_to_look_body = lookup.get("Repository Scope", "")
    _scope_preamble, scope_subsections = split_subsections(where_to_look_body)
    scope_lookup = {subsection_alias_map.get(("Repository Scope", name), name): body for name, body in scope_subsections}
    if scope_lookup.get("Where To Look First", "").strip() and len(scope_lookup["Where To Look First"].split()) < 6:
        workflow_issues.append(
            Issue(
                issue_id="thin-where-to-look-first",
                category="workflow-drift",
                severity="medium",
                file=str(agents_path),
                evidence="Repository Scope > Where To Look First is too thin to route agent reading behavior.",
                recommended_fix="Point to the most important docs, directories, or files agents should check first.",
                auto_fixable=False,
            )
        )

    safety_body = lookup.get("Safety Boundaries", "")
    _safety_preamble, safety_subsections = split_subsections(safety_body)
    safety_lookup = {subsection_alias_map.get(("Safety Boundaries", name), name): body for name, body in safety_subsections}
    for child in ("Never Do", "Ask Before"):
        body = safety_lookup.get(child, "").strip()
        if body and len(body.split()) < 6:
            boundary_issues.append(
                Issue(
                    issue_id=f"thin-safety-guidance-{child.lower().replace(' ', '-')}",
                    category="boundary-and-safety",
                    severity="medium",
                    file=str(agents_path),
                    evidence=f"Safety Boundaries > {child} is too thin to act as a useful guardrail.",
                    recommended_fix=f"Expand '{child}' with concrete, repo-grounded boundaries.",
                    auto_fixable=False,
                )
            )

    return schema_issues, workflow_issues, validation_issues, boundary_issues


def apply_fixes(
    agents_path: Path,
    agents_text: str,
    config: Dict[str, object],
) -> Tuple[str, List[Dict[str, str]]]:
    if not agents_text.strip():
        bootstrap = render_template_bootstrap()
        write_text(agents_path, bootstrap)
        return (
            bootstrap,
            [
                {
                    "action": "create-agents-from-template",
                    "file": str(agents_path),
                    "reason": "Created a missing AGENTS.md from the bundled canonical template.",
                }
            ],
        )

    settings = config_settings(config)
    required = required_sections(settings)
    order = canonical_order(settings)
    preserve_preamble = bool(settings.get("preservePreamble", True))
    allow_additional = bool(settings.get("allowAdditionalSections", True))
    section_alias_map = section_alias_lookup(settings)

    preamble, sections = split_sections(agents_text)
    normalized_preamble = normalize_preamble(preamble, preserve_preamble)

    canonical_lookup: Dict[str, str] = {}
    extra_sections: List[Tuple[str, str]] = []
    for heading, body in sections:
        canonical_heading = section_alias_map.get(heading, heading)
        if canonical_heading in order or canonical_heading in required:
            canonical_lookup[canonical_heading] = body
        elif allow_additional:
            extra_sections.append((heading, body))

    rendered_sections: List[Tuple[str, str]] = []
    for heading in order:
        body = render_section_body(heading, canonical_lookup.get(heading, ""), settings).strip()
        rendered_sections.append((heading, body))
    if allow_additional:
        rendered_sections.extend(extra_sections)

    parts = [normalized_preamble]
    for heading, body in rendered_sections:
        parts.extend(["", f"## {heading}", "", body.strip()])
    document = "\n".join(parts).strip() + "\n"
    return normalize_whitespace(document), [
        {
            "action": "normalize-agents-structure",
            "file": str(agents_path),
            "reason": "Normalized AGENTS.md to the canonical template-backed section schema.",
        }
    ]


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
        f"- Config: `{report['schema_contract']['config_path']}`",
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
            evidence = item.get("evidence") or item.get("reason") or item.get("message")
            lines.append(f"- {item.get('issue_id', item.get('action', 'item'))}: {evidence}")
    return "\n".join(lines).strip() + "\n"


def run_maintenance(args: argparse.Namespace) -> Tuple[Dict[str, object], str]:
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.is_dir():
        raise ValueError(f"Project root does not exist or is not a directory: {project_root}")

    agents_path = Path(args.agents_path).expanduser().resolve() if args.agents_path else project_root / "AGENTS.md"
    config = load_config(project_root, args.config)
    errors: List[str] = []
    fixes_applied: List[Dict[str, str]] = []
    existing_text = read_text(agents_path) if agents_path.is_file() else ""

    if args.run_mode == "apply":
        new_text, applied = apply_fixes(agents_path, existing_text, config)
        if not agents_path.parent.exists():
            agents_path.parent.mkdir(parents=True, exist_ok=True)
        if normalize_whitespace(existing_text) != new_text:
            write_text(agents_path, new_text)
            fixes_applied.extend(applied)
            existing_text = new_text

    if existing_text:
        schema_issues, workflow_issues, validation_issues, boundary_issues = validate_schema(
            agents_path, existing_text, config
        )
    else:
        schema_issues = [
            Issue(
                issue_id="missing-agents-file",
                category="schema",
                severity="high",
                file=str(agents_path),
                evidence="AGENTS.md does not exist.",
                recommended_fix="Create the canonical AGENTS.md file from the bundled template.",
                auto_fixable=True,
            )
        ]
        workflow_issues = []
        validation_issues = []
        boundary_issues = []

    report = {
        "run_context": {
            "project_root": str(project_root),
            "agents_path": str(agents_path),
            "run_mode": args.run_mode,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "schema_contract": {
            "config_path": config.get("configPath"),
            "default_config_path": config.get("defaultConfigPath"),
            "required_sections": required_sections(config_settings(config)),
            "section_order": canonical_order(config_settings(config)),
            "required_subsections": required_subsections(config_settings(config)),
        },
        "schema_violations": [issue.to_dict() for issue in schema_issues],
        "workflow_drift_issues": [issue.to_dict() for issue in workflow_issues],
        "validation_drift_issues": [issue.to_dict() for issue in validation_issues],
        "boundary_and_safety_issues": [issue.to_dict() for issue in boundary_issues],
        "fixes_applied": fixes_applied,
        "post_fix_status": {
            "remaining_issue_count": len(schema_issues) + len(workflow_issues) + len(validation_issues) + len(boundary_issues),
            "is_clean": not schema_issues and not workflow_issues and not validation_issues and not boundary_issues and not errors,
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
