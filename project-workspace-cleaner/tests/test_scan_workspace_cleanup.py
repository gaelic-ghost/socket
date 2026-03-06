from __future__ import annotations

import json
import importlib.util
import sys
import time
from pathlib import Path

import pytest


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "scan_workspace_cleanup.py"
    spec = importlib.util.spec_from_file_location("scan_workspace_cleanup", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


def test_resolve_config_uses_template_defaults() -> None:
    settings, active_path, source = m.resolve_config("")

    assert settings["workspaceRoot"] == "~/Workspace"
    assert settings["minMb"] == 50
    assert active_path.name == "customization.yaml"
    assert source.endswith("project-workspace-cleaner/config/customization.template.yaml")


def test_require_yaml_points_to_root_dev_baseline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(m, "yaml", None)

    with pytest.raises(RuntimeError, match="uv run --group dev python"):
        m.require_yaml()


def test_scan_repo_flags_build_output(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    build_dir = repo / "build"
    build_dir.mkdir()
    (build_dir / "artifact.bin").write_bytes(b"x" * 32)

    findings, skipped_paths = m.scan_repo(
        repo=repo,
        min_bytes=1,
        stale_days=90,
        now_ts=time.time(),
        dir_rules=m.DEFAULT_DIR_RULES,
        file_ext_rules=m.DEFAULT_FILE_EXT_RULES,
        severity_cutoffs=m.normalize_cutoffs(None),
    )

    assert skipped_paths == []
    assert any(
        finding.category == "build_output" and Path(finding.directory) == build_dir
        for finding in findings
    )


def test_find_repositories_discovers_nested_git_dirs(tmp_path: Path) -> None:
    repo_a = tmp_path / "repo-a"
    repo_b = tmp_path / "repo-b"
    repo_a.mkdir()
    repo_b.mkdir()
    (repo_a / ".git").mkdir()
    (repo_b / ".git").mkdir()

    repos = m.find_repositories(tmp_path)

    assert repos == [repo_a, repo_b]


def test_summarize_by_repo_orders_by_total_size(tmp_path: Path) -> None:
    finding_a = m.Finding(
        severity="high",
        score=80,
        repo=str(tmp_path / "repo-a"),
        directory=str(tmp_path / "repo-a" / "build"),
        category="build_output",
        size_bytes=200,
        size_human="200 B",
        why_flagged="A",
        suggested_cleanup="cleanup",
    )
    finding_b = m.Finding(
        severity="medium",
        score=60,
        repo=str(tmp_path / "repo-b"),
        directory=str(tmp_path / "repo-b" / "dist"),
        category="build_output",
        size_bytes=100,
        size_human="100 B",
        why_flagged="B",
        suggested_cleanup="cleanup",
    )

    rows = m.summarize_by_repo([finding_b, finding_a])

    assert rows[0]["repo"] == str(tmp_path / "repo-a")
    assert rows[0]["total_size_bytes"] == 200


def test_main_clean_workspace_outputs_exact_no_findings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "scan_workspace_cleanup.py",
            "--workspace",
            str(tmp_path),
            "--min-mb",
            "1",
        ],
    )

    rc = m.main()
    captured = capsys.readouterr()

    assert rc == 0
    assert captured.out.strip().endswith("No findings.\n\nRepo Summary\n- No flagged repositories.".strip())
    assert captured.err == ""


def test_main_partial_results_warning_when_scan_repo_skips_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()

    skipped = [m.SkippedPath(path=str(repo / "blocked"), operation="walk directory", error="permission denied")]
    monkeypatch.setattr(m, "find_repositories", lambda workspace: [repo])
    monkeypatch.setattr(m, "scan_repo", lambda repo, **kwargs: ([], skipped))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "scan_workspace_cleanup.py",
            "--workspace",
            str(tmp_path),
            "--min-mb",
            "1",
        ],
    )

    rc = m.main()
    captured = capsys.readouterr()

    assert rc == 0
    assert "Partial-results warning" in captured.out
    assert "permission denied" in captured.out
    assert captured.err == ""


def test_main_json_output_includes_partial_results_and_skipped_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    skipped = [m.SkippedPath(path=str(repo / "blocked"), operation="walk directory", error="permission denied")]

    monkeypatch.setattr(m, "find_repositories", lambda workspace: [repo])
    monkeypatch.setattr(m, "scan_repo", lambda repo, **kwargs: ([], skipped))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "scan_workspace_cleanup.py",
            "--workspace",
            str(tmp_path),
            "--json",
            "--min-mb",
            "1",
        ],
    )

    rc = m.main()
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload["partial_results"] is True
    assert payload["skipped_paths"][0]["error"] == "permission denied"


def test_main_config_override_beats_template_workspace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    workspace = tmp_path / "custom-workspace"
    workspace.mkdir()
    repo = workspace / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    config_path = tmp_path / "override.yaml"
    config_path.write_text(
        "\n".join(
            [
                "settings:",
                f"  workspaceRoot: {workspace}",
                "  minMb: 1",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "scan_workspace_cleanup.py",
            "--config",
            str(config_path),
        ],
    )

    rc = m.main()
    captured = capsys.readouterr()

    assert rc == 0
    assert f"Workspace: {workspace}" in captured.out
