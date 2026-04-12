from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "maintain_project_readme.py"
SPEC = importlib.util.spec_from_file_location("maintain_project_readme", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["maintain_project_readme"] = MODULE
SPEC.loader.exec_module(MODULE)


def run(
    project_root: Path,
    run_mode: str = "check-only",
    readme_path: Path | None = None,
    config: Path | None = None,
):
    args = argparse.Namespace(
        project_root=str(project_root),
        readme_path=str(readme_path) if readme_path else None,
        run_mode=run_mode,
        config=str(config) if config else None,
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


def valid_readme() -> str:
    return """
# demo-project

A compact demo project for README maintenance.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [License](#license)

## Overview

### Status

demo-project is active and maintained as a reference repository for README schema work.

### What This Project Is

demo-project is a small repository used to exercise the README maintainer contract.

### Motivation

It keeps the shared README structure explicit and testable.

## Quick Start

Run the smallest happy path for trying the project quickly.

## Usage

Use the project according to the documented local workflow.

## Development

### Setup

Document the concrete setup steps needed before someone can develop this project.

### Workflow

Explain the normal local development workflow for maintainers and contributors.

### Validation

List the grounded checks used to verify local changes for this project.

## Repo Structure

```text
.
├── src/
├── tests/
└── README.md
```

## Release Notes

Track notable shipped changes in a consistent place for maintainers and readers.

## License

See [LICENSE](./LICENSE).
""".strip()


def test_valid_base_readme_has_no_findings(tmp_path: Path) -> None:
    write(tmp_path / "README.md", valid_readme())
    report, _md = run(tmp_path)
    assert report["schema_violations"] == []
    assert report["content_quality_issues"] == []
    assert report["errors"] == []


def test_missing_development_subsection_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "README.md",
        valid_readme().replace(
            "\n### Validation\n\nList the grounded checks used to verify local changes for this project.\n", "\n"
        ),
    )
    report, _md = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-subsection-development-validation" in issue_ids


def test_overlong_status_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "README.md",
        valid_readme().replace(
            "demo-project is active and maintained as a reference repository for README schema work.",
            "demo-project is active and maintained as a reference repository for README schema work. "
            "It is also used in several experiments, has multiple ongoing iterations, and continues to change "
            "often enough that this status statement is intentionally much too long for the README policy.",
        ),
    )
    report, _md = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["content_quality_issues"]}
    assert "status-section-too-long" in issue_ids


def test_alias_heading_is_reported_and_apply_mode_migrates_it(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    write(readme, valid_readme().replace("## Quick Start", "## Getting Started"))
    report, _md = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "non-canonical-heading-quick-start" in issue_ids

    applied_report, _applied_md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert "## Quick Start" in updated
    assert "## Getting Started" not in updated
    assert applied_report["post_fix_status"] == []


def test_missing_table_of_contents_is_reported_when_required(tmp_path: Path) -> None:
    write(
        tmp_path / "README.md",
        valid_readme().replace(
            "## Table of Contents\n\n- [Overview](#overview)\n- [Quick Start](#quick-start)\n- [Usage](#usage)\n- [Development](#development)\n- [Repo Structure](#repo-structure)\n- [Release Notes](#release-notes)\n- [License](#license)\n\n",
            "",
        ),
    )
    report, _md = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-table-of-contents" in issue_ids


def test_apply_mode_repairs_missing_sections_and_subsections(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-project

A compact demo project for README maintenance.

## Overview

demo-project keeps the structure tight.
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert report["fixes_applied"]
    assert "## Table of Contents" in updated
    assert "## Quick Start" in updated
    assert "### Status" in updated
    assert "### Setup" in updated
    assert "### Workflow" in updated
    assert "### Validation" in updated
    assert "## Repo Structure" in updated
    assert "## Release Notes" in updated
    assert report["post_fix_status"] == []


def test_apply_mode_preserves_preamble_content(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-project

A compact demo project for README maintenance.

![CI](https://example.com/badge.svg)

> Early access project.

Additional intro context that should remain before the canonical H2 block.

## Overview

demo-project keeps the structure tight.
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert report["fixes_applied"]
    assert "![CI](https://example.com/badge.svg)" in updated
    assert "> Early access project." in updated
    assert "Additional intro context that should remain before the canonical H2 block." in updated
    assert updated.index("![CI](https://example.com/badge.svg)") < updated.index("## Table of Contents")
    assert report["post_fix_status"] == []


def test_custom_config_can_extend_base_schema(tmp_path: Path) -> None:
    config = tmp_path / "readme-config.yaml"
    write(
        config,
        """
schemaVersion: 1
isCustomized: true
profile: service
settings:
  preservePreamble: true
  allowAdditionalSections: true
  requiredSections:
    - Overview
    - Quick Start
    - Usage
    - Development
    - Configuration
    - Repo Structure
    - Release Notes
    - License
  sectionOrder:
    - Overview
    - Quick Start
    - Usage
    - Development
    - Configuration
    - Repo Structure
    - Release Notes
    - License
  requiredSubsections:
    Overview:
      - Status
      - What This Project Is
      - Motivation
    Development:
      - Setup
      - Workflow
      - Validation
    Configuration:
      - Runtime Settings
  sectionTemplates:
    Configuration: |
      ### Runtime Settings

      Document the runtime settings required for this service.
  subsectionTemplates:
    Configuration/Runtime Settings: |
      Document the runtime settings required for this service.
""".strip(),
    )
    readme = tmp_path / "README.md"
    write(readme, valid_readme())
    report, _md = run(tmp_path, config=config)
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-section-configuration" in issue_ids

    applied_report, _applied_md = run(tmp_path, run_mode="apply", config=config)
    updated = readme.read_text(encoding="utf-8")
    assert "## Configuration" in updated
    assert "### Runtime Settings" in updated
    assert applied_report["customization_state"]["is_customized"] is True
    assert applied_report["post_fix_status"] == []


def test_repo_structure_without_tree_outline_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "README.md",
        valid_readme().replace(
            "```text\n.\n├── src/\n├── tests/\n└── README.md\n```", "Describe the important directories in prose."
        ),
    )
    report, _md = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["content_quality_issues"]}
    assert "repo-structure-missing-tree-outline" in issue_ids


def test_apply_mode_regenerates_table_of_contents_for_additional_top_level_sections(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    write(
        readme,
        valid_readme()
        + "\n\n## Install\n\nExplain how to install this repository's shipped surface.\n",
    )
    report, _md = run(tmp_path, run_mode="apply")
    post_report, _post_md = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in post_report["schema_violations"]}
    assert report["post_fix_status"] == []
    assert "stale-table-of-contents" not in issue_ids


def test_skills_repo_is_allowed(tmp_path: Path) -> None:
    write(tmp_path / ".codex-plugin" / "plugin.json", '{"name":"demo"}')
    write(tmp_path / "skills" / "demo-skill" / "SKILL.md", "---\nname: demo-skill\n---\n")
    write(tmp_path / "README.md", valid_readme().replace("# demo-project", "# demo"))
    report, _md = run(tmp_path)
    assert report["errors"] == []


def test_apply_mode_bootstraps_missing_readme_from_template(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    report, _md = run(tmp_path, run_mode="apply")
    assert readme.is_file()
    content = readme.read_text(encoding="utf-8")
    assert report["fixes_applied"]
    assert report["fixes_applied"][0]["action"] == "create-readme-from-template"
    assert "# " + tmp_path.name in content
    assert "## Table of Contents" in content
    assert "## Quick Start" in content
    assert "### Status" in content
    assert "### Setup" in content
    assert "### Validation" in content
    assert "## Repo Structure" in content
    assert "```text" in content
    assert "## Release Notes" in content
    assert report["post_fix_status"] == []
