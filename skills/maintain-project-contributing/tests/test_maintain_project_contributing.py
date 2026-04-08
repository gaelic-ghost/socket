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
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    write(
        tmp_path / "CONTRIBUTING.md",
        """
# Contributing to demo-lib

## Overview

Use this guide when preparing changes for review so the repository stays easy to run, verify, and extend.

## Contribution Workflow

- Start from a clean branch or worktree.
- Keep changes bounded to one coherent purpose.
- Update nearby docs or tests when behavior changes.

## Local Setup

### Runtime Config

```bash
uv sync
```

Call out required local configuration files, secrets, or environment variables before contributors try to run the project.

### Runtime Behavior

Explain any local processes, demo entrypoints, or execution steps contributors need before they can validate their changes.

## Naming Conventions

- Match the repository's existing terminology, casing, and file naming patterns.
- Keep new public names aligned with the nouns already used in code, docs, and commands.
- Rename only when the meaning changes or a real collision requires it.

## Verification

```bash
uv run pytest
```

## Pull Request Expectations

- Summarize what changed and why.
- Note any user-facing or maintainer-facing follow-up work.
- Include the validation you ran before requesting review.
""".strip(),
    )

    report, markdown = run(tmp_path)

    assert report["schema_violations"] == []
    assert report["command_integrity_issues"] == []
    assert report["content_quality_issues"] == []
    assert report["errors"] == []
    assert markdown == "No findings."


def test_apply_adds_missing_naming_conventions_and_local_setup_subsections(tmp_path: Path) -> None:
    write(
        tmp_path / "package.json",
        """
{
  "name": "demo-app",
  "dependencies": {
    "vite": "^5.0.0"
  }
}
""".strip(),
    )
    write(
        tmp_path / "CONTRIBUTING.md",
        """
# Contributing to demo-app

## Overview

Short overview.

## Contribution Workflow

- Keep changes focused.

## Local Setup

Explain setup briefly.

## Verification

```bash
pnpm test
```

## Pull Request Expectations

- Add context for reviewers.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="apply")
    updated = (tmp_path / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "## Naming Conventions" in updated
    assert "### Runtime Config" in updated
    assert "### Runtime Behavior" in updated
    assert report["schema_violations"] == []


def test_apply_creates_contributing_when_missing(tmp_path: Path) -> None:
    write(
        tmp_path / "Cargo.toml",
        """
[package]
name = "demo-crate"
version = "0.1.0"
edition = "2021"
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="apply")
    created = (tmp_path / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "# Contributing to demo-crate" in created
    assert "## Naming Conventions" in created
    assert "```bash\ncargo build\n```" in created
    assert "```bash\ncargo test\n```" in created
