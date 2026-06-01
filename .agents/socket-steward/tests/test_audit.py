from __future__ import annotations

from pathlib import Path

from socket_steward.audit import run_audit
from socket_steward.plan import plan_docs_sync
from socket_steward.proposal import build_docs_sync_proposal, write_report


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_docs_audit_passes_for_current_root_docs() -> None:
    report = run_audit(REPO_ROOT, "docs")

    assert report.status == "PASS"
    assert report.findings == ()


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
