from __future__ import annotations

import importlib.util
import time
from pathlib import Path

import pytest


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "scan_workspace_cleanup.py"
    spec = importlib.util.spec_from_file_location("scan_workspace_cleanup", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    import sys

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
