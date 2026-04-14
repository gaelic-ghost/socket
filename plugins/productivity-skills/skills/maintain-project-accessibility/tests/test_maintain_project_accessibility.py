from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "maintain_project_accessibility.py"
SPEC = importlib.util.spec_from_file_location("maintain_project_accessibility", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["maintain_project_accessibility"] = MODULE
SPEC.loader.exec_module(MODULE)


def run(project_root: Path, run_mode: str = "check-only", accessibility_path: Path | None = None):
    args = argparse.Namespace(
        project_root=str(project_root),
        accessibility_path=str(accessibility_path) if accessibility_path else None,
        run_mode=run_mode,
        config=None,
        json_out=None,
        md_out=None,
        print_json=False,
        print_md=False,
        fail_on_issues=False,
    )
    return MODULE.run_maintenance(args)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def valid_accessibility_doc() -> str:
    return """
# Accessibility

This project targets WCAG 2.2 AA across its shipped web interface and contributor-maintained docs surfaces.

## Table of Contents

- [Overview](#overview)
- [Standards Baseline](#standards-baseline)
- [Accessibility Architecture](#accessibility-architecture)
- [Engineering Workflow](#engineering-workflow)
- [Known Gaps](#known-gaps)
- [User Support and Reporting](#user-support-and-reporting)
- [Verification and Evidence](#verification-and-evidence)

## Overview

### Status

Accessibility standards are defined and enforced for normal UI work in this repository.

### Scope

This document covers the shipped browser UI, content structure, and the contributor workflow for accessibility-relevant changes.

### Accessibility Goals

The project aims to keep core user journeys usable with keyboard navigation, assistive technology, zoom, and reduced-motion preferences.

## Standards Baseline

### Target Standard

This project targets WCAG 2.2 AA for its shipped web interface.

### Conformance Language Rules

This document describes the standards the project targets and the evidence it tracks. Do not describe the project as fully compliant unless a grounded review history supports that claim.

### Supported Platforms and Surfaces

The accessibility contract applies to the main web UI in current desktop and mobile browsers, plus contributor-maintained documentation that ships to users.

## Accessibility Architecture

### Semantic Structure

The UI uses real headings, landmarks, labels, and document structure so assistive technology can understand the page hierarchy.

### Input and Keyboard Model

All primary controls must stay reachable and operable with keyboard navigation and direct input.

### Focus Management

Focus order follows the visible interaction order, and dynamic UI changes must preserve or intentionally restore focus.

### Naming and Announcements

Interactive controls need stable accessible names, and dynamic state changes should be announced when they would otherwise be silent.

### Color, Contrast, and Motion

The UI must not rely on color alone for meaning, must preserve readable contrast, and must honor reduced-motion expectations for non-essential animation.

### Zoom, Reflow, and Responsive Behavior

Layouts should remain usable under zoom and narrow-width reflow without clipping essential content or controls.

### Media, Captions, and Alternatives

Non-text media needs equivalent text, captions, transcripts, or other documented alternatives when those surfaces are shipped.

## Engineering Workflow

### Design and Implementation Rules

Accessibility-impacting changes must preserve semantics, input behavior, labels, focus order, and visible state communication.

### Automated Testing

We run automated accessibility checks in the UI test suite and keep those checks green before merge.

### Manual Testing

Keyboard-only navigation, visible focus, zoom behavior, and screen-reader-sensitive flows are manually checked when UI behavior changes.

### Assistive Technology Coverage

The team actively spot-checks the shipped interface with VoiceOver and modern browser accessibility tooling during accessibility-relevant work.

### Definition of Done

Accessibility-relevant changes are not ready for review until they match this document's standards or update the known-gaps section in the same pass.

## Known Gaps

### Current Exceptions

There are no currently documented accessibility exceptions in the baseline demo file.

### Planned Remediation

If an exception is introduced, it must be tracked here with a concrete remediation path or explicit follow-up owner.

### Ownership

Maintainers who approve accessibility-relevant changes are responsible for keeping this document and its follow-up work current.

## User Support and Reporting

### Feedback Path

Accessibility issues should be reported through the normal project issue tracker or maintainer support path.

### Triage Expectations

Accessibility reports should be acknowledged promptly and either fixed, tracked as a known gap, or escalated with a clear next step.

## Verification and Evidence

### CI Signals

```bash
pnpm test
pnpm lint
```

### Audit Cadence

Accessibility review happens whenever UI behavior changes and during larger design or workflow resets.

### Review History

2026-04 baseline accessibility contract drafted and reviewed for the maintain-project-accessibility workflow.
""".strip()


def test_valid_accessibility_file_has_no_findings(tmp_path: Path) -> None:
    write(tmp_path / "ACCESSIBILITY.md", valid_accessibility_doc())

    report, markdown = run(tmp_path)

    assert report["schema_violations"] == []
    assert report["claim_integrity_issues"] == []
    assert report["verification_evidence_issues"] == []
    assert report["content_quality_issues"] == []
    assert report["errors"] == []
    assert markdown == "No findings."


def test_apply_creates_accessibility_from_template_when_missing(tmp_path: Path) -> None:
    report, _markdown = run(tmp_path, run_mode="apply")
    created = (tmp_path / "ACCESSIBILITY.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "# Accessibility" in created
    assert "## Table of Contents" in created
    assert "## Standards Baseline" in created
    assert "### Conformance Language Rules" in created


def test_apply_normalizes_structure_and_aliases(tmp_path: Path) -> None:
    write(
        tmp_path / "ACCESSIBILITY.md",
        """
# Accessibility

Targets WCAG 2.2 AA for the shipped web app.

## Overview

### Status

Accessibility standards are defined.

### Scope

This covers the shipped web app.

### Goals

The project aims to keep core user journeys usable with keyboard navigation and assistive technology.

## Standards

### Accessibility Standard

This project targets WCAG 2.2 AA for its shipped interface.

### Claim Rules

Do not overstate compliance claims without evidence.

### Supported Surfaces

The accessibility contract applies to the main web UI.

## A11y Architecture

### Semantic Structure

The UI uses semantic structure.

### Keyboard Model

Keyboard access must stay intact.

### Focus Management

Focus order follows the interaction flow.

### Labels and Announcements

Controls use stable labels and announcements.

### Contrast and Motion

The project preserves contrast and reduced-motion expectations.

### Zoom and Reflow

Layouts stay usable under zoom.

### Media Alternatives

Media ships with alternatives when needed.

## Workflow

### Implementation Rules

Accessibility-impacting changes must preserve semantics and labels.

### Automated Testing

Automated checks are kept green before merge.

### Manual Testing

Manual checks happen when UI behavior changes.

### AT Coverage

VoiceOver spot checks are used for key flows.

### Done Criteria

Accessibility-impacting work is not done until it meets the documented standards.

## Known Gaps

### Exceptions

There are no currently documented accessibility exceptions.

### Remediation

Exceptions are tracked with remediation details.

### Ownership

Maintainers keep this current.

## Support and Reporting

### Contact Path

Issues are reported through the normal project issue path.

### Triage Expectations

Reports are acknowledged promptly.

## Evidence

### Automation Signals

```bash
pnpm test
```

### Review Cadence

Review happens when UI behavior changes.

### Audit History

2026 baseline review.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="apply")
    updated = (tmp_path / "ACCESSIBILITY.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "## Table of Contents" in updated
    assert "## Standards Baseline" in updated
    assert "## Accessibility Architecture" in updated
    assert "## User Support and Reporting" in updated
    assert "## Verification and Evidence" in updated
    assert "### Accessibility Goals" in updated
    assert "### Target Standard" in updated
    assert "### Conformance Language Rules" in updated
    assert "### Supported Platforms and Surfaces" in updated
    assert "### Input and Keyboard Model" in updated
    assert "### CI Signals" in updated
    assert report["schema_violations"] == []


def test_check_only_flags_missing_table_of_contents(tmp_path: Path) -> None:
    write(
        tmp_path / "ACCESSIBILITY.md",
        valid_accessibility_doc().replace(
            "## Table of Contents\n\n- [Overview](#overview)\n- [Standards Baseline](#standards-baseline)\n- [Accessibility Architecture](#accessibility-architecture)\n- [Engineering Workflow](#engineering-workflow)\n- [Known Gaps](#known-gaps)\n- [User Support and Reporting](#user-support-and-reporting)\n- [Verification and Evidence](#verification-and-evidence)\n\n",
            "",
        ),
    )

    report, _markdown = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-table-of-contents" in issue_ids


def test_check_only_flags_unsupported_strong_claims(tmp_path: Path) -> None:
    write(
        tmp_path / "ACCESSIBILITY.md",
        valid_accessibility_doc().replace(
            "This document describes the standards the project targets and the evidence it tracks. Do not describe the project as fully compliant unless a grounded review history supports that claim.",
            "The project is fully WCAG 2.2 AA compliant across all shipped surfaces.",
        ),
    )

    report, _markdown = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["claim_integrity_issues"]}
    assert "unsupported-strong-compliance-claim" in issue_ids


def test_check_only_flags_placeholder_ci_signals(tmp_path: Path) -> None:
    write(
        tmp_path / "ACCESSIBILITY.md",
        valid_accessibility_doc().replace(
            "```bash\npnpm test\npnpm lint\n```",
            "```bash\n# TODO replace this with the real CI checks\n```",
        ),
    )

    report, _markdown = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["verification_evidence_issues"]}
    assert any(issue_id.startswith("placeholder-ci-block-") for issue_id in issue_ids)
