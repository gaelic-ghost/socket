#!/usr/bin/env python3
"""Audit and apply bounded ACCESSIBILITY.md maintenance from a hard-enforced schema."""

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
STRONG_CLAIM_PATTERNS = [
    re.compile(r"\b100%\s+accessible\b", re.IGNORECASE),
    re.compile(r"\bfully\s+accessible\b", re.IGNORECASE),
    re.compile(r"\bfully\s+compliant\b", re.IGNORECASE),
    re.compile(r"\bfully\s+conform(?:s|ant)\b", re.IGNORECASE),
    re.compile(r"\bWCAG\s*2\.[12]\s*AA\s+compliant\b", re.IGNORECASE),
    re.compile(r"\bWCAG\s*2\.2\s*AA\s+compliant\b", re.IGNORECASE),
    re.compile(r"\bSection\s+508\s+compliant\b", re.IGNORECASE),
]
TARGET_LANGUAGE_RE = re.compile(r"\b(targets?|working toward|aims for|strives for)\b", re.IGNORECASE)
REVIEW_HISTORY_DATE_RE = re.compile(r"\b(20\d{2}|19\d{2})\b")
NEGATED_CLAIM_PREFIX_RE = re.compile(r"\b(do not|don't|avoid|unless)\b", re.IGNORECASE)


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
        description="Audit and optionally apply bounded ACCESSIBILITY.md maintenance from a hard-enforced schema."
    )
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--accessibility-path", help="Optional ACCESSIBILITY path override")
    parser.add_argument("--run-mode", required=True, choices=["check-only", "apply"], help="Execution mode")
    parser.add_argument("--config", help="Optional ACCESSIBILITY config override")
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


def parse_title_and_summary(preamble: str) -> Tuple[Optional[str], Optional[str], List[str]]:
    lines = [line.rstrip() for line in preamble.splitlines()]
    title: Optional[str] = None
    summary: Optional[str] = None
    extras: List[str] = []
    title_index: Optional[int] = None
    summary_index: Optional[int] = None

    for idx, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            title_index = idx
            break

    if title_index is None:
        return None, None, lines

    for idx in range(title_index + 1, len(lines)):
        if lines[idx].strip():
            summary = lines[idx].strip()
            summary_index = idx
            break

    for idx, line in enumerate(lines):
        if idx in {title_index, summary_index}:
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


def normalize_preamble(preamble: str, preserve_preamble: bool) -> str:
    title, summary, extras = parse_title_and_summary(preamble)
    normalized_title = title or "Accessibility"
    normalized_summary = summary or "Describe the project's accessibility posture in one short sentence."
    lines = [f"# {normalized_title}", "", normalized_summary]
    if preserve_preamble:
        extra_lines = collapse_blank_lines(extras)
        if extra_lines:
            lines.extend(["", *extra_lines])
    return "\n".join(lines).strip()


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
    default_path = Path(__file__).resolve().parents[1] / "config" / "accessibility-customization.template.yaml"
    default_config = read_yaml(default_path)
    loaded_path = default_path

    if config_override:
        override_path = Path(config_override).expanduser().resolve()
        merged = deep_merge(default_config, read_yaml(override_path))
        merged["isCustomized"] = True
        merged["configPath"] = str(override_path)
        merged["defaultConfigPath"] = str(default_path)
        return merged

    project_config = project_root / "config" / "accessibility-customization.yaml"
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


def build_toc(headings: Sequence[str]) -> str:
    return "\n".join(f"- [{heading}](#{slugify_heading(heading)})" for heading in headings)


def toc_entries(body: str) -> List[str]:
    entries: List[str] = []
    for line in body.splitlines():
        match = re.match(r"^\s*-\s+\[(.+?)\]\(#(.+?)\)\s*$", line.strip())
        if match:
            entries.append(match.group(1).strip())
    return entries


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
    template_path = Path(__file__).resolve().parents[1] / "assets" / "ACCESSIBILITY.template.md"
    template = read_text(template_path)
    rendered = template.replace(
        "{{ONE_LINE_SUMMARY}}",
        "Describe the project's accessibility posture in one short sentence.",
    )
    return normalize_whitespace(rendered)


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
        child_body = subsection_lookup.get(child, "").strip() or subsection_template_map.get(f"{heading}/{child}", "")
        lines.extend([f"### {child}", "", child_body.strip()])
        if idx < len(required_children) - 1 or extra_subsections:
            lines.append("")

    for idx, (name, body) in enumerate(extra_subsections):
        lines.extend([f"### {name}", "", body.strip()])
        if idx < len(extra_subsections) - 1:
            lines.append("")

    rendered = "\n".join(lines).strip()
    return rendered or section_template_map.get(heading, "")


def find_unnegated_strong_claim(text: str) -> Optional[str]:
    for pattern in STRONG_CLAIM_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        prefix = text[max(0, match.start() - 40) : match.start()]
        if NEGATED_CLAIM_PREFIX_RE.search(prefix):
            continue
        return match.group(0)
    return None


def find_subsection_body(
    sections_lookup: Dict[str, str],
    section_name: str,
    subsection_name: str,
    settings: Dict[str, object],
) -> str:
    section_alias_map = section_alias_lookup(settings)
    subsection_alias_map = subsection_alias_lookup(settings)
    body = sections_lookup.get(section_name, "")
    if not body:
        alias_parent = next(
            (alias for alias, canonical in section_alias_map.items() if canonical == section_name and alias in sections_lookup),
            None,
        )
        body = sections_lookup.get(alias_parent, "") if alias_parent else ""
    if not body:
        return ""
    _preamble, subsections = split_subsections(body)
    found = {
        subsection_alias_map.get((section_name, name), name): subsection_body
        for name, subsection_body in subsections
    }
    return found.get(subsection_name, "").strip()


def validate_schema(
    accessibility_path: Path,
    accessibility_text: str,
    config: Dict[str, object],
) -> Tuple[List[Issue], List[Issue], List[Issue], List[Issue]]:
    settings = config_settings(config)
    required = required_sections(settings)
    order = canonical_order(settings)
    subsection_map = required_subsections(settings)
    section_alias_map = section_alias_lookup(settings)

    schema_issues: List[Issue] = []
    claim_issues: List[Issue] = []
    evidence_issues: List[Issue] = []
    content_issues: List[Issue] = []

    preamble, sections = split_sections(accessibility_text)
    lookup = section_map(sections)
    title, summary, _extras = parse_title_and_summary(preamble)

    if title != "Accessibility":
        schema_issues.append(
            Issue(
                issue_id="non-canonical-title",
                category="schema",
                severity="medium",
                file=str(accessibility_path),
                evidence="ACCESSIBILITY.md must use the canonical top-level title '# Accessibility'.",
                recommended_fix="Rename the top-level title to '# Accessibility'.",
                auto_fixable=True,
            )
        )
    if not summary:
        schema_issues.append(
            Issue(
                issue_id="missing-summary",
                category="schema",
                severity="medium",
                file=str(accessibility_path),
                evidence="ACCESSIBILITY.md is missing a short accessibility-facing summary beneath the title.",
                recommended_fix="Add a short summary sentence beneath the top-level title.",
                auto_fixable=True,
            )
        )

    if "Table of Contents" not in lookup:
        schema_issues.append(
            Issue(
                issue_id="missing-table-of-contents",
                category="schema",
                severity="medium",
                file=str(accessibility_path),
                evidence="ACCESSIBILITY.md is missing the required '## Table of Contents' section.",
                recommended_fix="Add a table of contents that mirrors the canonical top-level headings.",
                auto_fixable=True,
            )
        )

    observed_headings = [heading for heading, _body in sections]
    canonical_positions = {heading: idx for idx, heading in enumerate(observed_headings)}
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
                    issue_id=f"non-canonical-heading-{slugify_heading(heading)}",
                    category="schema",
                    severity="medium",
                    file=str(accessibility_path),
                    evidence=f"ACCESSIBILITY.md uses alias heading '## {alias_found}' where the canonical schema expects '## {heading}'.",
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
                    file=str(accessibility_path),
                    evidence=f"ACCESSIBILITY.md is missing required section '## {heading}'.",
                    recommended_fix=f"Add the required '## {heading}' section.",
                    auto_fixable=True,
                )
            )

    order_positions: List[int] = []
    for heading in order:
        if heading in canonical_positions:
            order_positions.append(canonical_positions[heading])
            continue
        alias_found = next(
            (alias for alias, canonical in section_alias_map.items() if canonical == heading and alias in canonical_positions),
            None,
        )
        if alias_found:
            order_positions.append(canonical_positions[alias_found])
    if order_positions and order_positions != sorted(order_positions):
        schema_issues.append(
            Issue(
                issue_id="canonical-section-order",
                category="schema",
                severity="medium",
                file=str(accessibility_path),
                evidence="Canonical ACCESSIBILITY sections are not in the configured order.",
                recommended_fix="Normalize the top-level sections into canonical order.",
                auto_fixable=True,
            )
        )

    subsection_alias_map = subsection_alias_lookup(settings)
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
        _preamble, subsections = split_subsections(body)
        found = {
            subsection_alias_map.get((parent, name), name): subsection_body
            for name, subsection_body in subsections
        }
        for child in children:
            if child not in found:
                schema_issues.append(
                    Issue(
                        issue_id=f"missing-subsection-{slugify_heading(parent)}-{slugify_heading(child)}",
                        category="schema",
                        severity="high",
                        file=str(accessibility_path),
                        evidence=f"Section '## {parent}' is missing required subsection '### {child}'.",
                        recommended_fix=f"Add the required subsection '### {child}' under '## {parent}'.",
                        auto_fixable=True,
                    )
                )

    if "Table of Contents" in lookup:
        expected_toc = [heading for heading in order if heading in required or heading in lookup]
        actual_toc = toc_entries(lookup["Table of Contents"])
        if actual_toc != expected_toc:
            schema_issues.append(
                Issue(
                    issue_id="stale-table-of-contents",
                    category="schema",
                    severity="low",
                    file=str(accessibility_path),
                    evidence="Table of contents entries do not match the canonical top-level section headings in order.",
                    recommended_fix="Regenerate the table of contents from the canonical section list.",
                    auto_fixable=True,
                )
            )

    for heading in required:
        body = lookup.get(heading)
        if not body:
            continue
        if not body.strip():
            schema_issues.append(
                Issue(
                    issue_id=f"empty-section-{slugify_heading(heading)}",
                    category="schema",
                    severity="medium",
                    file=str(accessibility_path),
                    evidence=f"Section '## {heading}' is present but empty.",
                    recommended_fix=f"Add grounded content to '## {heading}'.",
                    auto_fixable=True,
                )
            )
        if any(pattern.search(body) for pattern in PLACEHOLDER_PATTERNS):
            content_issues.append(
                Issue(
                    issue_id=f"placeholder-content-{slugify_heading(heading)}",
                    category="content-quality",
                    severity="medium",
                    file=str(accessibility_path),
                    evidence=f"Section '## {heading}' contains placeholder-style content.",
                    recommended_fix="Replace placeholder content with repo-grounded accessibility guidance.",
                    auto_fixable=False,
                )
            )

    target_standard_text = find_subsection_body(lookup, "Standards Baseline", "Target Standard", settings)
    conformance_rules_text = find_subsection_body(lookup, "Standards Baseline", "Conformance Language Rules", settings)
    known_gaps_text = find_subsection_body(lookup, "Known Gaps", "Current Exceptions", settings)
    ownership_text = find_subsection_body(lookup, "Known Gaps", "Ownership", settings)
    ci_signals_text = find_subsection_body(lookup, "Verification and Evidence", "CI Signals", settings)
    review_history_text = find_subsection_body(lookup, "Verification and Evidence", "Review History", settings)
    automated_testing_text = find_subsection_body(lookup, "Engineering Workflow", "Automated Testing", settings)
    manual_testing_text = find_subsection_body(lookup, "Engineering Workflow", "Manual Testing", settings)
    assistive_technology_text = find_subsection_body(lookup, "Engineering Workflow", "Assistive Technology Coverage", settings)

    if target_standard_text and not TARGET_LANGUAGE_RE.search(target_standard_text) and "wcag" not in target_standard_text.lower():
        claim_issues.append(
            Issue(
                issue_id="unclear-target-standard-language",
                category="claim-integrity",
                severity="medium",
                file=str(accessibility_path),
                evidence="Standards Baseline > Target Standard does not clearly name the target standard or baseline.",
                recommended_fix="Name the target standard explicitly, such as 'This project targets WCAG 2.2 AA.'",
                auto_fixable=False,
            )
        )

    strong_claim = find_unnegated_strong_claim(accessibility_text)
    if strong_claim:
        claim_issues.append(
            Issue(
                issue_id="unsupported-strong-compliance-claim",
                category="claim-integrity",
                severity="high",
                file=str(accessibility_path),
                evidence=f"ACCESSIBILITY.md uses strong compliance language: '{strong_claim}'.",
                recommended_fix="Use target-language or qualified evidence language unless the repo has grounded proof for a stronger claim.",
                auto_fixable=False,
            )
        )

    if conformance_rules_text:
        lowered_rules = conformance_rules_text.lower()
        if "target" not in lowered_rules and "claim" not in lowered_rules and "do not" not in lowered_rules:
            claim_issues.append(
                Issue(
                    issue_id="thin-conformance-language-rules",
                    category="claim-integrity",
                    severity="medium",
                    file=str(accessibility_path),
                    evidence="Standards Baseline > Conformance Language Rules does not clearly distinguish target standards from verified conformance claims.",
                    recommended_fix="Explain what the project may and may not claim about accessibility status.",
                    auto_fixable=False,
                )
            )

    if len(known_gaps_text.split()) < 4:
        content_issues.append(
            Issue(
                issue_id="thin-current-exceptions",
                category="content-quality",
                severity="medium",
                file=str(accessibility_path),
                evidence="Known Gaps > Current Exceptions is too thin to tell maintainers whether the project has any documented limitations.",
                recommended_fix="Document current accessibility limitations explicitly, or say there are no currently documented exceptions.",
                auto_fixable=False,
            )
        )

    if len(ownership_text.split()) < 4:
        content_issues.append(
            Issue(
                issue_id="thin-ownership-guidance",
                category="content-quality",
                severity="medium",
                file=str(accessibility_path),
                evidence="Known Gaps > Ownership is too thin to identify who keeps accessibility guidance and follow-up work current.",
                recommended_fix="Describe who owns this document and its remediation follow-up path.",
                auto_fixable=False,
            )
        )

    verification_blocks = [ci_signals_text, automated_testing_text, manual_testing_text, assistive_technology_text]
    if not any(text.strip() for text in verification_blocks):
        evidence_issues.append(
            Issue(
                issue_id="missing-verification-evidence",
                category="verification-evidence",
                severity="high",
                file=str(accessibility_path),
                evidence="ACCESSIBILITY.md does not document any concrete verification or testing evidence.",
                recommended_fix="Document the automated checks, manual checks, and assistive technology coverage that support the project's accessibility standards.",
                auto_fixable=False,
            )
        )

    if ci_signals_text:
        shell_blocks = list(SHELL_FENCE_RE.finditer(ci_signals_text))
        if shell_blocks:
            for match in shell_blocks:
                info = match.group(1).strip()
                block = match.group(2).strip()
                if not info:
                    evidence_issues.append(
                        Issue(
                            issue_id=f"missing-ci-fence-info-string-{match.start()}",
                            category="verification-evidence",
                            severity="low",
                            file=str(accessibility_path),
                            evidence="CI Signals uses a fenced code block without a language info string.",
                            recommended_fix="Use fenced code blocks with an info string such as ```bash for CI or automation commands.",
                            auto_fixable=False,
                        )
                    )
                if not block:
                    evidence_issues.append(
                        Issue(
                            issue_id=f"empty-ci-block-{match.start()}",
                            category="verification-evidence",
                            severity="medium",
                            file=str(accessibility_path),
                            evidence="CI Signals contains an empty fenced code block.",
                            recommended_fix="Replace the empty block with grounded automation commands or remove it.",
                            auto_fixable=True,
                        )
                    )
                if any(pattern.search(block) for pattern in PLACEHOLDER_PATTERNS):
                    evidence_issues.append(
                        Issue(
                            issue_id=f"placeholder-ci-block-{match.start()}",
                            category="verification-evidence",
                            severity="high",
                            file=str(accessibility_path),
                            evidence="CI Signals contains a placeholder command block.",
                            recommended_fix="Replace the placeholder command block with grounded CI or automation checks.",
                            auto_fixable=False,
                        )
                    )
        elif len(ci_signals_text.split()) < 6:
            evidence_issues.append(
                Issue(
                    issue_id="thin-ci-signals",
                    category="verification-evidence",
                    severity="medium",
                    file=str(accessibility_path),
                    evidence="Verification and Evidence > CI Signals is too thin to explain how automation supports the project's accessibility claims.",
                    recommended_fix="Add grounded CI or automation signals, preferably with fenced code blocks and language info strings when commands help.",
                    auto_fixable=False,
                )
            )

    if review_history_text and not REVIEW_HISTORY_DATE_RE.search(review_history_text):
        evidence_issues.append(
            Issue(
                issue_id="review-history-without-dates",
                category="verification-evidence",
                severity="low",
                file=str(accessibility_path),
                evidence="Verification and Evidence > Review History does not include any obvious dated checkpoints.",
                recommended_fix="Record notable accessibility review checkpoints with dates or version anchors when possible.",
                auto_fixable=False,
            )
        )

    return schema_issues, claim_issues, evidence_issues, content_issues


def apply_fixes(
    accessibility_path: Path,
    accessibility_text: str,
    config: Dict[str, object],
) -> Tuple[str, List[Dict[str, str]]]:
    if not accessibility_text.strip():
        bootstrap = render_template_bootstrap()
        write_text(accessibility_path, bootstrap)
        return (
            bootstrap,
            [
                {
                    "action": "create-accessibility-from-template",
                    "file": str(accessibility_path),
                    "reason": "Created a missing ACCESSIBILITY.md from the bundled canonical template.",
                }
            ],
        )

    settings = config_settings(config)
    required = required_sections(settings)
    order = canonical_order(settings)
    preserve_preamble = bool(settings.get("preservePreamble", True))
    allow_additional = bool(settings.get("allowAdditionalSections", True))
    section_alias_map = section_alias_lookup(settings)

    preamble, sections = split_sections(accessibility_text)
    normalized_preamble = normalize_preamble(preamble, preserve_preamble)

    canonical_lookup: Dict[str, str] = {}
    extra_sections: List[Tuple[str, str]] = []
    for heading, body in sections:
        if heading == "Table of Contents":
            continue
        canonical_heading = section_alias_map.get(heading, heading)
        if canonical_heading in order or canonical_heading in required:
            canonical_lookup[canonical_heading] = body
        elif allow_additional:
            extra_sections.append((heading, body))

    canonical_sections: List[Tuple[str, str]] = []
    for heading in order:
        body = render_section_body(heading, canonical_lookup.get(heading, ""), settings).strip()
        canonical_sections.append((heading, body))

    headings_for_toc = [heading for heading, _body in canonical_sections]
    if allow_additional:
        headings_for_toc.extend(heading for heading, _body in extra_sections)
    rendered_sections = [("Table of Contents", build_toc(headings_for_toc).strip()), *canonical_sections]
    if allow_additional:
        rendered_sections.extend(extra_sections)

    parts = [normalized_preamble]
    for heading, body in rendered_sections:
        parts.extend(["", f"## {heading}", "", body.strip()])
    document = "\n".join(parts).strip() + "\n"
    return normalize_whitespace(document), [
        {
            "action": "normalize-accessibility-structure",
            "file": str(accessibility_path),
            "reason": "Normalized ACCESSIBILITY.md to the canonical template-backed section schema.",
        }
    ]


def format_report(report: Dict[str, object]) -> str:
    total_issues = (
        len(report["schema_violations"])
        + len(report["claim_integrity_issues"])
        + len(report["verification_evidence_issues"])
        + len(report["content_quality_issues"])
    )
    if total_issues == 0 and not report["errors"]:
        return "No findings."

    lines = [
        "# ACCESSIBILITY.md Maintenance Report",
        "",
        f"- Target: `{report['run_context']['accessibility_path']}`",
        f"- Mode: `{report['run_context']['run_mode']}`",
        f"- Config: `{report['schema_contract']['config_path']}`",
    ]

    for key, title in (
        ("schema_violations", "Schema Violations"),
        ("claim_integrity_issues", "Claim Integrity Issues"),
        ("verification_evidence_issues", "Verification Evidence Issues"),
        ("content_quality_issues", "Content Quality Issues"),
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

    accessibility_path = (
        Path(args.accessibility_path).expanduser().resolve()
        if args.accessibility_path
        else project_root / "ACCESSIBILITY.md"
    )
    config = load_config(project_root, args.config)

    errors: List[str] = []
    fixes_applied: List[Dict[str, str]] = []
    existing_text = read_text(accessibility_path) if accessibility_path.is_file() else ""

    if args.run_mode == "apply":
        new_text, applied = apply_fixes(accessibility_path, existing_text, config)
        if not accessibility_path.parent.exists():
            accessibility_path.parent.mkdir(parents=True, exist_ok=True)
        if normalize_whitespace(existing_text) != new_text:
            write_text(accessibility_path, new_text)
            fixes_applied.extend(applied)
            existing_text = new_text

    if existing_text:
        schema_issues, claim_issues, evidence_issues, content_issues = validate_schema(
            accessibility_path,
            existing_text,
            config,
        )
    else:
        schema_issues = [
            Issue(
                issue_id="missing-accessibility-file",
                category="schema",
                severity="high",
                file=str(accessibility_path),
                evidence="ACCESSIBILITY.md does not exist.",
                recommended_fix="Create the canonical ACCESSIBILITY.md file from the bundled template.",
                auto_fixable=True,
            )
        ]
        claim_issues = []
        evidence_issues = []
        content_issues = []

    report = {
        "run_context": {
            "project_root": str(project_root),
            "accessibility_path": str(accessibility_path),
            "run_mode": args.run_mode,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "schema_contract": {
            "config_path": config.get("configPath"),
            "default_config_path": config.get("defaultConfigPath"),
            "required_table_of_contents": True,
            "required_sections": required_sections(config_settings(config)),
            "section_order": canonical_order(config_settings(config)),
            "required_subsections": required_subsections(config_settings(config)),
        },
        "schema_violations": [issue.to_dict() for issue in schema_issues],
        "claim_integrity_issues": [issue.to_dict() for issue in claim_issues],
        "verification_evidence_issues": [issue.to_dict() for issue in evidence_issues],
        "content_quality_issues": [issue.to_dict() for issue in content_issues],
        "fixes_applied": fixes_applied,
        "post_fix_status": {
            "remaining_issue_count": len(schema_issues) + len(claim_issues) + len(evidence_issues) + len(content_issues),
            "is_clean": not schema_issues and not claim_issues and not evidence_issues and not content_issues and not errors,
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
        or bool(report["claim_integrity_issues"])
        or bool(report["verification_evidence_issues"])
        or bool(report["content_quality_issues"])
        or bool(report["errors"])
    )
    if args.fail_on_issues and has_issues:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
