from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "maintain_project_contributing.py"
)
SPEC = importlib.util.spec_from_file_location("maintain_project_contributing", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["maintain_project_contributing"] = MODULE
SPEC.loader.exec_module(MODULE)


def run(project_root: Path, run_mode: str = "check-only", contributing_path: Path | None = None):
    args = argparse.Namespace(
        project_root=str(project_root),
        contributing_path=str(contributing_path) if contributing_path else None,
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


def test_valid_contributing_file_has_no_findings(tmp_path: Path) -> None:
    write(
        tmp_path / "CONTRIBUTING.md",
        """
# Contributing to demo-project

Use this guide when preparing changes so the project stays understandable, runnable, and reviewable for the next contributor.

## Table of Contents

- [Overview](#overview)
- [Contribution Workflow](#contribution-workflow)
- [Local Setup](#local-setup)
- [Development Expectations](#development-expectations)
- [Pull Request Expectations](#pull-request-expectations)
- [Communication](#communication)
- [License and Contribution Terms](#license-and-contribution-terms)

## Overview

### Who This Guide Is For

This guide is for contributors making code, docs, and maintainer-facing workflow changes in this repository.

### Before You Start

Read the nearby project docs first, confirm the intended change, and make sure you understand any repo-level constraints before beginning.

## Contribution Workflow

### Choosing Work

Confirm the intended work before you begin so duplicate or conflicting changes do not drift.

### Making Changes

Keep changes bounded to one coherent purpose and update nearby docs or tests when behavior changes.

### Asking For Review

Ask for review once the change is understandable, validated, and ready for another maintainer to reason about.

## Local Setup

### Runtime Config

Document the concrete local configuration contributors need, including files, secrets, environment variables, or local services.

### Runtime Behavior

Explain what needs to be running locally and how contributors can tell the project is actually working.

## Development Expectations

### Naming Conventions

Match the repository's existing terminology, casing, and naming patterns so new work fits the surrounding code and docs cleanly.

### Verification

```bash
uv run pytest
```

## Pull Request Expectations

Summarize what changed, why it changed, and what reviewers should pay attention to first.

## Communication

Raise questions and scope uncertainty early so work stays aligned before it becomes expensive to unwind.

## License and Contribution Terms

See the project license for the default contribution terms.
""".strip(),
    )

    report, markdown = run(tmp_path)

    assert report["schema_violations"] == []
    assert report["command_integrity_issues"] == []
    assert report["content_quality_issues"] == []
    assert report["errors"] == []
    assert markdown == "No findings."


def test_apply_creates_contributing_from_template_when_missing(tmp_path: Path) -> None:
    report, _markdown = run(tmp_path, run_mode="apply")
    created = (tmp_path / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "# Contributing to" in created
    assert "## Table of Contents" in created
    assert "## Development Expectations" in created
    assert "### Verification" in created


def test_apply_normalizes_structure_and_aliases(tmp_path: Path) -> None:
    write(
        tmp_path / "CONTRIBUTING.md",
        """
# Contributing to demo-project

Short guide.

## Overview

### Audience

This guide is for contributors.

### Prerequisites

Read the nearby docs first.

## Development

### Naming

Follow existing names.

### Validation

```bash
pnpm test
```

## Contribution Workflow

### Picking Work

Choose work deliberately.

### Implementation Workflow

Keep changes focused.

### Requesting Review

Ask once the change is ready.

## Local Setup

### Runtime Config

Document local config.

### Runtime Behavior

Explain the running surface.

## Pull Request Expectations

Share enough reviewer context.

## Communication

Raise questions early.

## Contribution Terms

See the license.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="apply")
    updated = (tmp_path / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "## Table of Contents" in updated
    assert "## Development Expectations" in updated
    assert "## Contribution Terms" not in updated
    assert "## License and Contribution Terms" in updated
    assert "### Audience" not in updated
    assert "### Who This Guide Is For" in updated
    assert report["schema_violations"] == []


def test_check_only_flags_missing_table_of_contents(tmp_path: Path) -> None:
    write(
        tmp_path / "CONTRIBUTING.md",
        """
# Contributing to demo-project

Short guide.

## Overview

### Who This Guide Is For

This guide is for contributors.

### Before You Start

Read the nearby docs first.

## Contribution Workflow

### Choosing Work

Choose work deliberately.

### Making Changes

Keep changes focused.

### Asking For Review

Ask once the change is ready.

## Local Setup

### Runtime Config

Document local config.

### Runtime Behavior

Explain the running surface.

## Development Expectations

### Naming Conventions

Follow existing names.

### Verification

```bash
uv run pytest
```

## Pull Request Expectations

Share enough reviewer context.

## Communication

Raise questions early.

## License and Contribution Terms

See the license.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="check-only")

    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-table-of-contents" in issue_ids


def test_check_only_flags_verification_fence_without_info_string(tmp_path: Path) -> None:
    write(
        tmp_path / "CONTRIBUTING.md",
        """
# Contributing to demo-project

Short guide.

## Table of Contents

- [Overview](#overview)
- [Contribution Workflow](#contribution-workflow)
- [Local Setup](#local-setup)
- [Development Expectations](#development-expectations)
- [Pull Request Expectations](#pull-request-expectations)
- [Communication](#communication)
- [License and Contribution Terms](#license-and-contribution-terms)

## Overview

### Who This Guide Is For

This guide is for contributors.

### Before You Start

Read the nearby docs first.

## Contribution Workflow

### Choosing Work

Choose work deliberately.

### Making Changes

Keep changes focused.

### Asking For Review

Ask once the change is ready.

## Local Setup

### Runtime Config

Document local config.

### Runtime Behavior

Explain the running surface.

## Development Expectations

### Naming Conventions

Follow existing names.

### Verification

```
uv run pytest
```

## Pull Request Expectations

Share enough reviewer context.

## Communication

Raise questions early.

## License and Contribution Terms

See the license.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="check-only")

    issue_ids = {issue["issue_id"] for issue in report["command_integrity_issues"]}
    assert any(issue_id.startswith("missing-code-fence-info-string-") for issue_id in issue_ids)
