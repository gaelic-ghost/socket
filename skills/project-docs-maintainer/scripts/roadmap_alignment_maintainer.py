#!/usr/bin/env python3
"""Checklist ROADMAP maintainer with check-only and apply modes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

DEFAULT_TEMPLATE = """# Project Roadmap

## Vision

- Define the long-term project outcome.

## Product principles

- Keep delivery deterministic and reviewable.

## Milestone Progress

- [ ] Milestone 0: Foundation

## Milestone 0: Foundation

Scope:

- [ ] Define initial scope.

Tickets:

- [ ] First implementation task.

Exit criteria:

- [ ] Scope, tickets, and validation are complete.
"""

REQUIRED_TOP_LEVEL = ["Vision", "Product principles", "Milestone Progress"]
REQUIRED_MILESTONE_SUBSECTIONS = ["Scope", "Tickets", "Exit criteria"]
CHECKBOX_RE = re.compile(r"^\s*-\s+\[( |x)\]\s+.+$")
ANY_CHECKBOX_RE = re.compile(r"^\s*-\s+\[[^\]]\]\s+.+$")
MILESTONE_HEADING_RE = re.compile(r"^##\s+Milestone\s+(\d+)\s*:\s*(.+?)\s*$")


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
    p = argparse.ArgumentParser(description="Check/apply checklist ROADMAP maintenance.")
    p.add_argument("--project-root", required=True, help="Absolute project root path")
    p.add_argument("--roadmap-path", help="Optional roadmap path (default: <project-root>/ROADMAP.md)")
    p.add_argument("--run-mode", required=True, choices=["check-only", "apply"], help="Execution mode")
    p.add_argument("--config", help="Optional config path override")
    p.add_argument("--json-out", help="Write JSON report path")
    p.add_argument("--md-out", help="Write markdown report path")
    p.add_argument("--print-json", action="store_true", help="Print JSON report")
    p.add_argument("--print-md", action="store_true", help="Print markdown report")
    p.add_argument("--fail-on-issues", action="store_true", help="Exit non-zero when findings remain")
    return p.parse_args()


def read_optional_config(project_root: Path, config_override: Optional[str]) -> Dict[str, object]:
    cfg_paths: List[Path] = []
    if config_override:
        cfg_paths.append(Path(config_override).expanduser().resolve())
    else:
        cfg_paths.append(project_root / "config" / "customization.yaml")
        cfg_paths.append(project_root / "config" / "customization.template.yaml")

    for path in cfg_paths:
        if path.is_file():
            # Keep parser dependency-free; consume only known scalars defensively.
            text = path.read_text(encoding="utf-8")
            result: Dict[str, object] = {"config_path": str(path)}
            for key in ["schemaVersion", "profile", "isCustomized", "planHistoryVerbosity", "changeLogVerbosity"]:
                m = re.search(rf"^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", text, flags=re.MULTILINE)
                if m:
                    result[key] = m.group(1).strip().strip('"')
            return result
    return {"config_path": "none"}


def split_sections(text: str) -> List[Tuple[str, List[str]]]:
    lines = text.splitlines()
    sections: List[Tuple[str, List[str]]] = []
    current_heading = "__preamble__"
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("## "):
            sections.append((current_heading, current_lines))
            current_heading = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections.append((current_heading, current_lines))
    return sections


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
                m = re.search(r"(\d+)", name)
                idx = int(m.group(1)) if m else len(rows)
                title = re.sub(r"^Milestone\s*\d+\s*[:\-]?\s*", "", name, flags=re.IGNORECASE).strip() or name
                rows.append((idx, title, status))
        elif in_table and line.strip() == "":
            in_table = False
    return sorted(rows, key=lambda item: item[0])


def status_to_checkbox(status: str) -> str:
    lowered = status.lower()
    if any(token in lowered for token in ["done", "complete", "completed", "shipped"]):
        return "[x]"
    return "[ ]"


def ensure_required_sections(findings: List[Finding], roadmap_path: Path, sections: List[Tuple[str, List[str]]]) -> None:
    headings = {h for h, _ in sections}
    for required in REQUIRED_TOP_LEVEL:
        if required not in headings:
            findings.append(
                Finding(
                    finding_id=f"missing-section-{required.lower().replace(' ', '-')}",
                    category="missing-required-section",
                    severity="high",
                    message=f"Missing required top-level section: {required}",
                    file=str(roadmap_path),
                    auto_fixable=True,
                )
            )


def milestone_sections(sections: Sequence[Tuple[str, List[str]]]) -> List[Tuple[int, str, List[str]]]:
    result: List[Tuple[int, str, List[str]]] = []
    for heading, lines in sections:
        m = MILESTONE_HEADING_RE.match(f"## {heading}")
        if m:
            result.append((int(m.group(1)), m.group(2).strip(), lines))
    return result


def validate_checkboxes(findings: List[Finding], roadmap_path: Path, lines: List[str]) -> None:
    for idx, line in enumerate(lines, start=1):
        if ANY_CHECKBOX_RE.match(line) and not CHECKBOX_RE.match(line):
            findings.append(
                Finding(
                    finding_id=f"invalid-checkbox-{idx}",
                    category="invalid-checkbox-syntax",
                    severity="medium",
                    message=f"Invalid checkbox syntax on line {idx}: use [ ] or [x].",
                    file=str(roadmap_path),
                    auto_fixable=True,
                )
            )


def validate_milestones(findings: List[Finding], roadmap_path: Path, sections: List[Tuple[str, List[str]]], all_lines: List[str]) -> None:
    milestones = milestone_sections(sections)
    if not milestones:
        findings.append(
            Finding(
                finding_id="missing-milestones",
                category="missing-milestone-sections",
                severity="high",
                message="No milestone sections found (expected headings like '## Milestone N: Name').",
                file=str(roadmap_path),
                auto_fixable=True,
            )
        )
        return

    ordered = [m[0] for m in milestones]
    if ordered != sorted(ordered):
        findings.append(
            Finding(
                finding_id="milestone-order",
                category="non-deterministic-milestone-order",
                severity="medium",
                message="Milestone sections are not in deterministic ascending order.",
                file=str(roadmap_path),
                auto_fixable=True,
            )
        )

    for idx, _title, body in milestones:
        joined = "\n".join(body)
        for subsection in REQUIRED_MILESTONE_SUBSECTIONS:
            if f"{subsection}:" not in joined:
                findings.append(
                    Finding(
                        finding_id=f"milestone-{idx}-missing-{subsection.lower().replace(' ', '-')}",
                        category="missing-milestone-subsection",
                        severity="high",
                        message=f"Milestone {idx} is missing subsection '{subsection}:'.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )

    current_block = ""
    for i, line in enumerate(all_lines, start=1):
        if line.strip() in {"Scope:", "Tickets:", "Exit criteria:"}:
            current_block = line.strip().rstrip(":")
            continue
        if line.startswith("## "):
            current_block = ""
        if "[P]" in line and current_block != "Tickets":
            findings.append(
                Finding(
                    finding_id=f"parallel-marker-{i}",
                    category="invalid-parallel-marker-placement",
                    severity="medium",
                    message=f"[P] marker on line {i} is outside a Tickets block.",
                    file=str(roadmap_path),
                    auto_fixable=True,
                )
            )


def build_migrated_from_legacy(text: str) -> str:
    rows = parse_legacy_milestones(text)
    if not rows:
        rows = [(0, "Foundation", "Planned")]

    lines: List[str] = [
        "# Project Roadmap",
        "",
        "## Vision",
        "",
        "- Preserved from legacy roadmap during checklist migration.",
        "",
        "## Product principles",
        "",
        "- Keep roadmap sections checklist-based and deterministic.",
        "",
        "## Milestone Progress",
        "",
    ]

    for idx, title, status in rows:
        lines.append(f"- {status_to_checkbox(status)} Milestone {idx}: {title} ({status})")

    lines.append("")

    for idx, title, status in rows:
        lines.extend(
            [
                f"## Milestone {idx}: {title}",
                "",
                "Scope:",
                "",
                f"- [ ] Preserve legacy scope details for status: {status}.",
                "",
                "Tickets:",
                "",
                "- [ ] Add or reconcile milestone tasks.",
                "",
                "Exit criteria:",
                "",
                "- [ ] Milestone checklist is complete and validated.",
                "",
            ]
        )

    lines.extend(
        [
            "## Risks and mitigations",
            "",
            "- Legacy roadmap converted to checklist format; verify historical fidelity.",
            "",
            "## Backlog candidates",
            "",
            "- Reintroduce any deferred legacy notes as explicit checklist items.",
            "",
        ]
    )
    return "\n".join(lines)


def ensure_apply_shape(text: str) -> str:
    sections = split_sections(text)
    headings = [h for h, _ in sections]
    lines = text.splitlines()

    if "Vision" not in headings or "Product principles" not in headings or "Milestone Progress" not in headings:
        return DEFAULT_TEMPLATE.rstrip() + "\n"

    # normalize checkbox markers and [P] placement soft-fix
    normalized: List[str] = []
    current_block = ""
    for line in lines:
        if line.strip() in {"Scope:", "Tickets:", "Exit criteria:"}:
            current_block = line.strip().rstrip(":")
            normalized.append(line)
            continue
        if line.startswith("## "):
            current_block = ""
            normalized.append(line)
            continue

        fixed = re.sub(r"^\s*-\s+\[(X)\]\s+", "- [x] ", line)
        if "[P]" in fixed and current_block != "Tickets":
            fixed = fixed.replace("[P]", "").replace("  ", " ").rstrip()
        normalized.append(fixed)

    return "\n".join(normalized).rstrip() + "\n"


def render_markdown(
    run_context: Dict[str, object],
    findings: List[Finding],
    apply_actions: List[ApplyAction],
    errors: List[str],
) -> str:
    if not findings and not apply_actions and not errors:
        return "No findings.\n"

    lines: List[str] = []
    lines.append("## Run Context")
    lines.append(f"- Timestamp: {run_context['timestamp_utc']}")
    lines.append(f"- Project root: {run_context['project_root']}")
    lines.append(f"- Roadmap path: {run_context['roadmap_path']}")
    lines.append(f"- Run mode: {run_context['run_mode']}")
    lines.append("")

    lines.append("## Findings")
    if not findings:
        lines.append("- None")
    else:
        for f in findings:
            lines.append(f"- [{f.severity}] {f.category}: {f.message}")
    lines.append("")

    lines.append("## Changes Applied")
    if not apply_actions:
        lines.append("- None")
    else:
        for action in apply_actions:
            lines.append(f"- {action.action}: {action.reason} ({action.file})")
    lines.append("")

    lines.append("## Errors")
    if not errors:
        lines.append("- None")
    else:
        for err in errors:
            lines.append(f"- {err}")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    errors: List[str] = []
    findings: List[Finding] = []
    apply_actions: List[ApplyAction] = []

    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists() or not project_root.is_dir():
        print(f"Project root does not exist or is not a directory: {project_root}", file=sys.stderr)
        return 1

    roadmap_path = Path(args.roadmap_path).expanduser().resolve() if args.roadmap_path else (project_root / "ROADMAP.md")
    config_state = read_optional_config(project_root, args.config)

    text = ""
    if roadmap_path.exists():
        text = roadmap_path.read_text(encoding="utf-8")

    legacy = has_legacy_format(text) if text else False

    if not roadmap_path.exists():
        findings.append(
            Finding(
                finding_id="missing-roadmap",
                category="missing-roadmap",
                severity="high",
                message=f"ROADMAP file is missing at {roadmap_path}",
                file=str(roadmap_path),
                auto_fixable=True,
            )
        )

    if text:
        sections = split_sections(text)
        ensure_required_sections(findings, roadmap_path, sections)
        validate_checkboxes(findings, roadmap_path, text.splitlines())
        validate_milestones(findings, roadmap_path, sections, text.splitlines())
        if legacy:
            findings.append(
                Finding(
                    finding_id="legacy-format",
                    category="legacy-roadmap-format",
                    severity="high",
                    message="Legacy roadmap sections detected (`Current Milestone`/`Milestones` table).",
                    file=str(roadmap_path),
                    auto_fixable=True,
                )
            )

    if args.run_mode == "apply":
        try:
            if not roadmap_path.exists():
                roadmap_path.write_text(DEFAULT_TEMPLATE.rstrip() + "\n", encoding="utf-8")
                apply_actions.append(ApplyAction("created", "Created checklist-standard ROADMAP.md", str(roadmap_path)))
            else:
                updated_text = text
                if legacy:
                    updated_text = build_migrated_from_legacy(text)
                    apply_actions.append(ApplyAction("migrated", "Migrated legacy roadmap to checklist format", str(roadmap_path)))
                updated_text = ensure_apply_shape(updated_text)
                if updated_text != text:
                    roadmap_path.write_text(updated_text, encoding="utf-8")
                    if not any(a.action in {"created", "migrated"} for a in apply_actions):
                        apply_actions.append(ApplyAction("updated", "Applied bounded checklist normalization", str(roadmap_path)))
            post_text = roadmap_path.read_text(encoding="utf-8")
            post_findings: List[Finding] = []
            post_sections = split_sections(post_text)
            ensure_required_sections(post_findings, roadmap_path, post_sections)
            validate_checkboxes(post_findings, roadmap_path, post_text.splitlines())
            validate_milestones(post_findings, roadmap_path, post_sections, post_text.splitlines())
            if has_legacy_format(post_text):
                post_findings.append(
                    Finding(
                        finding_id="legacy-format",
                        category="legacy-roadmap-format",
                        severity="high",
                        message="Legacy roadmap sections are still present after apply run.",
                        file=str(roadmap_path),
                        auto_fixable=True,
                    )
                )
            findings = post_findings
        except Exception as exc:  # defensive
            errors.append(f"apply error: {exc}")

    run_context = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project_root),
        "roadmap_path": str(roadmap_path),
        "run_mode": args.run_mode,
        "config": config_state,
    }

    report = {
        "run_context": run_context,
        "findings": [f.to_dict() for f in findings],
        "apply_actions": [a.to_dict() for a in apply_actions],
        "errors": errors,
    }

    markdown = render_markdown(run_context, findings, apply_actions, errors)

    if args.json_out:
        Path(args.json_out).expanduser().write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.md_out:
        Path(args.md_out).expanduser().write_text(markdown, encoding="utf-8")
    if args.print_json:
        print(json.dumps(report, indent=2))
    if args.print_md:
        print(markdown, end="")

    if args.fail_on_issues and (findings or errors):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
