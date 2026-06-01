from __future__ import annotations

from pathlib import Path

from socket_steward.audit import run_audit


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
