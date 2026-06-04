from __future__ import annotations

from pathlib import Path

from socket_steward.cli import _default_repo_root
from socket_steward.audit import run_audit
from socket_steward.plan import plan_docs_sync
from socket_steward.proposal import build_docs_sync_proposal, write_report
from socket_steward.workflow import apply_docs_sync, prepare_docs_sync


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_docs_audit_passes_for_current_root_docs() -> None:
    report = run_audit(REPO_ROOT, "docs")

    assert report.status in {"PASS", "WARN"}
    assert all(finding.severity != "error" for finding in report.findings)


def test_cli_default_repo_root_finds_socket_from_steward_package() -> None:
    assert _default_repo_root() == REPO_ROOT


def test_docs_audit_flags_completed_milestone_marked_in_progress(tmp_path: Path) -> None:
    for name in ("README.md", "CONTRIBUTING.md", "AGENTS.md", "TODO.md"):
        (tmp_path / name).write_text("# placeholder\n", encoding="utf-8")

    (tmp_path / "ROADMAP.md").write_text(
        """# Project Roadmap

## Vision

## Product Principles

## Backlog Candidates

## Milestone 99: Example complete milestone

### Status

In Progress

### Scope

- [x] Complete the scope.

### Tickets

- [x] Complete the ticket.

### Exit Criteria

- [x] Complete the exit criteria.
""",
        encoding="utf-8",
    )

    report = run_audit(tmp_path, "docs")

    assert report.status == "WARN"
    assert any(finding.code == "roadmap-status-stale" for finding in report.findings)


def test_unknown_audit_fails_with_human_readable_message() -> None:
    report = run_audit(REPO_ROOT, "unknown")

    assert report.status == "FAIL"
    assert report.findings[0].code == "unknown-audit"
    assert "Use one of: docs, guidance, marketplace" in report.findings[0].message


def test_docs_sync_plan_is_structured_and_read_only() -> None:
    plan = plan_docs_sync(REPO_ROOT)

    assert plan.name == "docs-sync"
    assert plan.status in {"PASS", "TODO"}
    assert all("apply" not in item.action.lower() for item in plan.items)


def test_docs_sync_proposal_is_markdown_and_read_only() -> None:
    report = build_docs_sync_proposal(REPO_ROOT)
    markdown = report.as_markdown()

    assert markdown.startswith("# Socket Steward Docs Sync Proposal")
    assert "does not apply file edits" in markdown
    assert "uv run scripts/validate_socket_metadata.py" in markdown


def test_report_writes_only_under_docs_agents(tmp_path: Path) -> None:
    report = build_docs_sync_proposal(REPO_ROOT)

    written_path = write_report(tmp_path, Path("docs/agents/report.md"), report)

    assert written_path == tmp_path / "docs" / "agents" / "report.md"
    assert written_path.read_text(encoding="utf-8").startswith(
        "# Socket Steward Docs Sync Proposal"
    )


def test_report_rejects_paths_outside_docs_agents(tmp_path: Path) -> None:
    report = build_docs_sync_proposal(REPO_ROOT)

    try:
        write_report(tmp_path, Path("README.md"), report)
    except ValueError as error:
        assert "under docs/agents" in str(error)
    else:
        raise AssertionError("write_report should reject paths outside docs/agents")


def test_prepare_docs_sync_runs_audit_plan_and_proposal() -> None:
    prepared = prepare_docs_sync(REPO_ROOT)

    assert prepared.status == "PASS"
    assert [audit.audit for audit in prepared.audits] == ["docs", "guidance", "marketplace"]
    assert prepared.plan.name == "docs-sync"
    assert prepared.proposal.name == "Socket Steward Docs Sync Proposal"


def test_apply_docs_sync_requires_confirmation(tmp_path: Path) -> None:
    try:
        apply_docs_sync(tmp_path, confirm=False)
    except ValueError as error:
        assert "--confirm" in str(error)
    else:
        raise AssertionError("apply_docs_sync should require confirmation")


def test_apply_docs_sync_refreshes_report_when_confirmed(tmp_path: Path) -> None:
    result = apply_docs_sync(tmp_path, confirm=True)

    assert result.status in {"PASS", "NEEDS-REVIEW"}
    assert result.report_path == tmp_path / "docs" / "agents" / "socket-steward-docs-sync.md"
    assert result.report_path.is_file()
