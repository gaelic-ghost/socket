from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "maintain_project_agents.py"
SPEC = importlib.util.spec_from_file_location("maintain_project_agents", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["maintain_project_agents"] = MODULE
SPEC.loader.exec_module(MODULE)


def run(project_root: Path, run_mode: str = "check-only", agents_path: Path | None = None):
    args = argparse.Namespace(
        project_root=str(project_root),
        agents_path=str(agents_path) if agents_path else None,
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


def test_valid_agents_file_has_no_findings(tmp_path: Path) -> None:
    write(
        tmp_path / "AGENTS.md",
        """
# AGENTS.md

Use this file for durable repo-local guidance that Codex should follow before changing code, docs, or project workflow surfaces in this repository.

## Repository Scope

### What This File Covers

This root-level file governs the repo-wide working rules for Codex in this repository.

### Where To Look First

Check the root README, the maintainer docs, and the primary source directories before reading broadly.

## Working Rules

### Change Scope

Keep work bounded to the requested surface and surface any wider architectural pivot before implementing it.

### Source of Truth

Treat repo-local docs, checked-in config, and the nearest relevant source files as the source of truth before guessing.

### Communication and Escalation

Stop and surface tradeoffs whenever the work needs a non-obvious scope change or design decision.

## Commands

### Setup

```bash
uv sync
```

### Validation

```bash
uv run pytest
```

### Optional Project Commands

There are no additional project commands worth calling out at the root level right now.

## Review and Delivery

### Review Expectations

Explain what changed, why it changed, and the most important review context.

### Definition of Done

Work is done when the requested change is implemented, nearby docs or tests are updated if needed, and the grounded checks have been run.

## Safety Boundaries

### Never Do

- Never invent commands, policies, or repo structure that are not grounded in the repository.
- Never auto-commit or auto-push without an explicit request.

### Ask Before

- Ask before widening scope into a larger refactor or architectural change.
- Ask before changing repo-wide automation or policy surfaces.

## Local Overrides

There are no more specific AGENTS files called out here right now. If a nested AGENTS file appears later, the closer file should refine this root guidance.
""".strip(),
    )

    report, markdown = run(tmp_path)
    assert report["schema_violations"] == []
    assert report["workflow_drift_issues"] == []
    assert report["validation_drift_issues"] == []
    assert report["boundary_and_safety_issues"] == []
    assert report["errors"] == []
    assert markdown == "No findings."


def test_apply_creates_agents_from_template_when_missing(tmp_path: Path) -> None:
    report, _markdown = run(tmp_path, run_mode="apply")
    created = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "# AGENTS.md" in created
    assert "## Repository Scope" in created
    assert "## Commands" in created
    assert "## Local Overrides" in created


def test_apply_normalizes_structure_and_aliases(tmp_path: Path) -> None:
    write(
        tmp_path / "AGENTS.md",
        """
# AGENTS.md

Short repo guidance.

## Repository Expectations

### Purpose

This root-level file governs the repo-wide working rules for Codex in this repository.

### Priority Files

Check the root README first.

## Standards and Guidance

### Scope

Keep work bounded.

### Truth Sources

Use repo-local docs first.

### Escalation

Surface tradeoffs when scope changes.

## Validation

### Setup

```bash
uv sync
```

### Validation

```bash
uv run pytest
```

### Project Commands

No extra commands.

## Review

### PR Expectations

Share reviewer context.

### Done

Make sure checks ran.

## Safety and Boundaries

### Never

Do not invent repo policy.

### Approval Gates

Ask before wider refactors.

## Local Overrides

No nested overrides are defined here.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="apply")
    updated = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "## Repository Expectations" not in updated
    assert "## Repository Scope" in updated
    assert "## Standards and Guidance" not in updated
    assert "## Working Rules" in updated
    assert "\n## Validation\n" not in updated
    assert "## Commands" in updated
    assert "### Purpose" not in updated
    assert "### What This File Covers" in updated
    assert report["schema_violations"] == []


def test_check_only_flags_missing_required_section(tmp_path: Path) -> None:
    write(
        tmp_path / "AGENTS.md",
        """
# AGENTS.md

Short repo guidance.

## Repository Scope

### What This File Covers

This root-level file governs the repo-wide working rules for Codex in this repository.

### Where To Look First

Check the root README first.

## Commands

### Setup

```bash
uv sync
```

### Validation

```bash
uv run pytest
```

### Optional Project Commands

No extra commands.

## Local Overrides

No nested overrides are defined here.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="check-only")
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-section-working-rules" in issue_ids


def test_check_only_flags_command_blocks_without_info_string(tmp_path: Path) -> None:
    write(
        tmp_path / "AGENTS.md",
        """
# AGENTS.md

Short repo guidance.

## Repository Scope

### What This File Covers

This root-level file governs the repo-wide working rules for Codex in this repository.

### Where To Look First

Check the root README first.

## Working Rules

### Change Scope

Keep work bounded.

### Source of Truth

Use repo-local docs first.

### Communication and Escalation

Surface tradeoffs when scope changes.

## Commands

### Setup

```
uv sync
```

### Validation

```
uv run pytest
```

### Optional Project Commands

No extra commands.

## Review and Delivery

### Review Expectations

Share reviewer context.

### Definition of Done

Make sure checks ran.

## Safety Boundaries

### Never Do

Do not invent repo policy.

### Ask Before

Ask before wider refactors.

## Local Overrides

No nested overrides are defined here.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="check-only")
    issue_ids = {issue["issue_id"] for issue in report["validation_drift_issues"]}
    assert any(issue_id.startswith("missing-code-fence-info-string-setup-") for issue_id in issue_ids)
    assert any(issue_id.startswith("missing-code-fence-info-string-validation-") for issue_id in issue_ids)
