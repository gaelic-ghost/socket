from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "maintain_project_roadmap.py"
SPEC = importlib.util.spec_from_file_location("maintain_project_roadmap", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["maintain_project_roadmap"] = MODULE
SPEC.loader.exec_module(MODULE)


def run(
    project_root: Path,
    run_mode: str = "check-only",
    roadmap_path: Path | None = None,
    config: Path | None = None,
):
    args = argparse.Namespace(
        project_root=str(project_root),
        roadmap_path=str(roadmap_path) if roadmap_path else None,
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


def valid_roadmap() -> str:
    return """
# Project Roadmap

Use this roadmap to track milestone-level delivery through checklist sections.

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 0: Foundation](#milestone-0-foundation)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Describe the long-term project outcome this roadmap is meant to deliver.

## Product Principles

- Keep roadmap updates explicit, reviewable, and tied to real delivery.

## Milestone Progress

- Milestone 0: Foundation - Planned

## Milestone 0: Foundation

### Status

Planned

### Scope

- [ ] Define the initial scope for this milestone.

### Tickets

- [ ] Add the first concrete implementation task for this milestone.

### Exit Criteria

- [ ] Describe what must be true before this milestone counts as complete.

## Backlog Candidates

- [ ] Record future work that is not yet attached to a milestone.

## History

- Initial roadmap scaffold created.
""".strip()


def test_valid_base_roadmap_has_no_findings(tmp_path: Path) -> None:
    write(tmp_path / "ROADMAP.md", valid_roadmap())
    report, _md = run(tmp_path)
    assert report["findings"] == []
    assert report["errors"] == []


def test_missing_table_of_contents_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "ROADMAP.md",
        valid_roadmap().replace(
            "## Table of Contents\n\n- [Vision](#vision)\n- [Product Principles](#product-principles)\n- [Milestone Progress](#milestone-progress)\n- [Milestone 0: Foundation](#milestone-0-foundation)\n- [Backlog Candidates](#backlog-candidates)\n- [History](#history)\n\n",
            "",
        ),
    )
    report, _md = run(tmp_path)
    finding_ids = {finding["finding_id"] for finding in report["findings"]}
    assert "missing-table-of-contents" in finding_ids


def test_missing_milestone_subsection_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "ROADMAP.md",
        valid_roadmap().replace(
            "\n### Exit Criteria\n\n- [ ] Describe what must be true before this milestone counts as complete.\n",
            "\n",
        ),
    )
    report, _md = run(tmp_path)
    finding_ids = {finding["finding_id"] for finding in report["findings"]}
    assert "milestone-0-missing-exit-criteria" in finding_ids


def test_apply_mode_regenerates_table_of_contents_for_additional_top_level_sections(tmp_path: Path) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    write(
        roadmap,
        valid_roadmap()
        + "\n\n## Notes\n\n- Keep extra roadmap notes in a separate top-level section when needed.\n",
    )
    report, _md = run(tmp_path, run_mode="apply")
    post_report, _post_md = run(tmp_path)
    finding_ids = {finding["finding_id"] for finding in post_report["findings"]}
    assert report["findings"] == []
    assert "stale-table-of-contents" not in finding_ids


def test_invalid_milestone_status_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "ROADMAP.md",
        valid_roadmap().replace("\n### Status\n\nPlanned\n", "\n### Status\n\nSomeday Maybe\n"),
    )
    report, _md = run(tmp_path)
    finding_ids = {finding["finding_id"] for finding in report["findings"]}
    assert "milestone-0-invalid-status" in finding_ids


def test_alias_heading_is_reported_and_apply_mode_migrates_it(tmp_path: Path) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    write(roadmap, valid_roadmap().replace("## Product Principles", "## Product principles"))

    report, _md = run(tmp_path)
    finding_ids = {finding["finding_id"] for finding in report["findings"]}
    assert "non-canonical-heading-product-principles" in finding_ids

    applied_report, _applied_md = run(tmp_path, run_mode="apply")
    updated = roadmap.read_text(encoding="utf-8")
    assert "## Product Principles" in updated
    assert "## Product principles" not in updated
    assert applied_report["findings"] == []


def test_apply_mode_bootstraps_missing_roadmap_from_template(tmp_path: Path) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    report, _md = run(tmp_path, run_mode="apply")
    assert roadmap.is_file()
    content = roadmap.read_text(encoding="utf-8")
    assert report["apply_actions"]
    assert report["apply_actions"][0]["action"] == "create-roadmap-from-template"
    assert "## Table of Contents" in content
    assert "## Product Principles" in content
    assert "## Milestone 0: Foundation" in content
    assert "### Status" in content
    assert "- Milestone 0: Foundation - Planned" in content
    assert "### Exit Criteria" in content
    assert "## History" in content
    assert report["findings"] == []


def test_apply_mode_repairs_missing_sections_and_progress(tmp_path: Path) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    write(
        roadmap,
        """
# Project Roadmap

## Vision

- Keep moving.

## Milestone 1: Delivery

### Scope

- [ ] Define work.
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = roadmap.read_text(encoding="utf-8")
    assert report["apply_actions"]
    assert "## Table of Contents" in updated
    assert "## Product Principles" in updated
    assert "## Milestone Progress" in updated
    assert "- Milestone 1: Delivery - Planned" in updated
    assert "### Status" in updated
    assert "### Tickets" in updated
    assert "### Exit Criteria" in updated
    assert "## Backlog Candidates" in updated
    assert "## History" in updated
    assert report["findings"] == []


def test_invalid_parallel_marker_is_reported_and_apply_mode_removes_it(tmp_path: Path) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    write(
        roadmap,
        valid_roadmap().replace(
            "- [ ] Define the initial scope for this milestone.",
            "- [ ] [P] Define the initial scope for this milestone.",
        ),
    )
    report, _md = run(tmp_path)
    finding_ids = {finding["finding_id"] for finding in report["findings"]}
    assert "parallel-marker-milestone-0" in finding_ids

    applied_report, _applied_md = run(tmp_path, run_mode="apply")
    updated = roadmap.read_text(encoding="utf-8")
    assert "[P]" not in updated.split("### Scope", 1)[1].split("### Tickets", 1)[0]
    assert applied_report["findings"] == []


def test_legacy_roadmap_is_migrated_in_apply_mode(tmp_path: Path) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    write(
        roadmap,
        """
# Project Roadmap

## Milestones

| Milestone | Status |
| --- | --- |
| Milestone 1: Delivery | In Progress |
| Milestone 2: Hardening | Planned |
""".strip(),
    )

    report, _md = run(tmp_path)
    finding_ids = {finding["finding_id"] for finding in report["findings"]}
    assert "legacy-format" in finding_ids

    applied_report, _applied_md = run(tmp_path, run_mode="apply")
    updated = roadmap.read_text(encoding="utf-8")
    assert "## Table of Contents" in updated
    assert "## Milestone 1: Delivery" in updated
    assert "## Milestone 2: Hardening" in updated
    assert "### Status" in updated
    assert "- Milestone 1: Delivery - In Progress" in updated
    assert "## Milestones" not in updated
    assert applied_report["findings"] == []


def test_custom_config_can_extend_base_schema(tmp_path: Path) -> None:
    config = tmp_path / "roadmap-config.yaml"
    write(
        config,
        """
schemaVersion: 1
isCustomized: true
profile: quarterly
settings:
  preservePreamble: true
  allowAdditionalSections: true
  statusValues:
    - Planned
    - In Progress
    - Completed
  requiredSections:
    - Vision
    - Product Principles
    - Milestone Progress
    - Review Cadence
    - Backlog Candidates
    - History
  sectionOrder:
    - Vision
    - Product Principles
    - Milestone Progress
    - __MILESTONES__
    - Review Cadence
    - Backlog Candidates
    - History
  requiredMilestoneSubsections:
    - Status
    - Scope
    - Tickets
    - Exit Criteria
  sectionTemplates:
    Review Cadence: |
      - Review roadmap progress every two weeks.
    History: |
      - Review history is tracked here.
  milestoneSubsectionTemplates:
    Status: |
      Planned
    Scope: |
      - [ ] Define milestone scope.
    Tickets: |
      - [ ] Add milestone tickets.
    Exit Criteria: |
      - [ ] Define milestone exit criteria.
""".strip(),
    )

    roadmap = tmp_path / "ROADMAP.md"
    write(roadmap, valid_roadmap())
    report, _md = run(tmp_path, config=config)
    finding_ids = {finding["finding_id"] for finding in report["findings"]}
    assert "missing-section-review-cadence" in finding_ids

    applied_report, _applied_md = run(tmp_path, run_mode="apply", config=config)
    updated = roadmap.read_text(encoding="utf-8")
    assert "## Review Cadence" in updated
    assert "## History" in updated
    assert applied_report["customization_state"]["is_customized"] is True
    assert applied_report["findings"] == []
