from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "release_workflow.py"
SPEC = importlib.util.spec_from_file_location("release_workflow", MODULE_PATH)
assert SPEC and SPEC.loader
release_workflow = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = release_workflow
SPEC.loader.exec_module(release_workflow)


def result(stdout: str = "", returncode: int = 0) -> object:
    return type("Result", (), {"returncode": returncode, "stdout": stdout, "stderr": ""})()


def test_snapshot_phase_requires_checks_and_rejects_failures() -> None:
    base = {
        "number": 7,
        "url": "https://github.test/pr/7",
        "state": "OPEN",
        "head_ref": "release/v2",
        "head_sha": "abc",
        "review_decision": "",
        "comments": 0,
    }

    assert release_workflow.PullRequestSnapshot(checks=(), **base).phase == "awaiting-github-state"
    assert (
        release_workflow.PullRequestSnapshot(checks=(("validate", "fail"),), **base).phase
        == "failed-checks"
    )
    assert (
        release_workflow.PullRequestSnapshot(checks=(("validate", "pass"),), **base).phase
        == "ready-to-advance"
    )


def test_snapshot_phase_requires_the_validate_job_and_an_open_pr() -> None:
    base = {
        "number": 7,
        "url": "https://github.test/pr/7",
        "head_ref": "release/v2",
        "head_sha": "abc",
        "review_decision": "",
        "comments": 0,
    }

    assert release_workflow.PullRequestSnapshot(
        state="OPEN", checks=(("unrelated", "pass"),), **base
    ).phase == "awaiting-required-checks"
    assert release_workflow.PullRequestSnapshot(
        state="CLOSED", checks=(("validate", "pass"),), **base
    ).phase == "closed"


def test_prepare_and_advance_are_blocked_on_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(release_workflow, "current_branch", lambda: "main")

    with pytest.raises(release_workflow.ReleaseWorkflowError, match="feature worktree"):
        release_workflow.ensure_feature_branch()


def test_find_main_worktree_uses_explicit_worktree_owner(monkeypatch: pytest.MonkeyPatch) -> None:
    output = """worktree /workspace/socket
HEAD abc
branch refs/heads/main

worktree /workspace/feature
HEAD def
branch refs/heads/release/v2
"""
    monkeypatch.setattr(release_workflow, "git", lambda *_args, **_kwargs: result(output))

    assert release_workflow.find_main_worktree() == Path("/workspace/socket")


def test_branch_accounting_requires_one_status_per_unmerged_branch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        release_workflow,
        "git",
        lambda *_args, **_kwargs: result("feature/a\nfeature/b\n"),
    )

    with pytest.raises(release_workflow.ReleaseWorkflowError, match="feature/b"):
        release_workflow.branch_accounting(tmp_path, {"feature/a": "preserved"})

    assert release_workflow.branch_accounting(
        tmp_path, {"feature/a": "preserved", "feature/b": "in-progress"}
    ) == {"feature/a": "preserved", "feature/b": "in-progress"}


def test_branch_accounting_rejects_blanket_or_unknown_status() -> None:
    with pytest.raises(release_workflow.ReleaseWorkflowError, match="Invalid branch accounting"):
        release_workflow.parse_accounting(["feature/a=allowed"])


def test_prepare_version_must_be_the_next_patch_minor_or_major(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        release_workflow.release_version,
        "determine_target_version",
        lambda _targets, mode, _custom: {
            "patch": "1.2.4",
            "minor": "1.3.0",
            "major": "2.0.0",
        }[mode],
    )

    release_workflow.ensure_next_stable_version([], "2.0.0")
    with pytest.raises(release_workflow.ReleaseWorkflowError, match="Choose one of"):
        release_workflow.ensure_next_stable_version([], "3.0.0")


def test_prepare_rejects_an_already_published_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        release_workflow,
        "git",
        lambda args, **_kwargs: result("v9.35.0\n" if args[:2] == ["tag", "-l"] else ""),
    )

    with pytest.raises(release_workflow.ReleaseWorkflowError, match="already exists locally"):
        release_workflow.ensure_unpublished("9.35.0")


def test_release_evidence_contains_only_prepublication_facts() -> None:
    evidence = release_workflow.release_version.ReleaseEvidence(
        commit="abc",
        captured_at="2026-08-20T12:00:00Z",
        marketplace_smoke={"status": "passed"},
        dependabot_alerts=(),
    )

    notes = release_workflow.append_release_evidence("# Notes\n", evidence, [])

    assert "temporary `CODEX_HOME`" in notes
    assert "GitHub release object" not in notes
    assert "marketplace upgrade" not in notes


def test_cli_exposes_one_release_lifecycle() -> None:
    help_text = Path(MODULE_PATH).read_text(encoding="utf-8")

    assert 'for operation in ("prepare", "inspect")' in help_text
    assert 'subparsers.add_parser("advance")' in help_text
    assert "patch-refresh" not in help_text
    assert "subtrees" not in help_text
