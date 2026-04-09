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
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    write(
        tmp_path / "AGENTS.md",
        """
# AGENTS.md

## Repository Expectations

- Keep edits bounded to the requested repo surface.
- Treat repo-local files and docs as the source of truth before inventing workflow claims.
- Surface architectural pivots explicitly instead of silently widening scope.

## Standards and Guidance

- Prefer `uv` for the primary project toolchain.
- Keep naming, command vocabulary, and file ownership consistent across docs, scripts, and code.
- Prefer repo-specific guidance over generic agent boilerplate.

## Project Workflows

Explain how agents should keep changes bounded, update nearby docs or tests, and avoid speculative architectural pivots.

## Validation

```bash
uv sync
```

```bash
uv run pytest
```

## Safety and Boundaries

- Never invent commands, secrets, packaging surfaces, or policies that are not grounded in the repository.
- Never auto-commit, auto-push, or open a PR unless the user explicitly asks.
- Treat AGENTS guidance as maintainer or operator policy, not as public README content.
""".strip(),
    )

    report, markdown = run(tmp_path)

    assert report["schema_violations"] == []
    assert report["workflow_drift_issues"] == []
    assert report["validation_drift_issues"] == []
    assert report["boundary_and_safety_issues"] == []
    assert report["errors"] == []
    assert markdown == "No findings."


def test_apply_adds_missing_validation_and_safety_sections(tmp_path: Path) -> None:
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
        tmp_path / "AGENTS.md",
        """
# AGENTS.md

## Repository Expectations

- Keep edits bounded.

## Standards and Guidance

- Keep names consistent.

## Project Workflows

Explain which package or app surface the agent should change and how to keep the work scoped.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="apply")
    updated = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "## Validation" in updated
    assert "## Safety and Boundaries" in updated
    assert "pnpm test" in updated
    assert report["schema_violations"] == []


def test_apply_creates_agents_when_missing(tmp_path: Path) -> None:
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
    created = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "# AGENTS.md" in created
    assert "## Project Workflows" in created
    assert "## Validation" in created
    assert "```bash\ncargo test\n```" in created
