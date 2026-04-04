from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_skills_plugin_repo.py"
    spec = importlib.util.spec_from_file_location("bootstrap_skills_plugin_repo", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


def test_audit_repo_flags_missing_paths(tmp_path: Path) -> None:
    findings = m.audit_repo(tmp_path, "example-skills")

    issue_ids = {finding.issue_id for finding in findings}
    assert "missing-path" in issue_ids
    assert "missing-symlink" in issue_ids


def test_apply_repo_creates_expected_symlinks(tmp_path: Path) -> None:
    actions, created_paths = m.apply_repo(tmp_path, "example-skills")

    assert any(action["action"] == "create-symlink" for action in actions)
    assert (tmp_path / ".agents" / "skills").is_symlink()
    assert os.readlink(tmp_path / ".agents" / "skills") == "../skills"
    assert (tmp_path / ".claude" / "skills").is_symlink()
    assert (tmp_path / "plugins" / "example-skills" / "skills").is_symlink()
    assert "plugins/example-skills/.codex-plugin/plugin.json" in created_paths


def test_apply_repo_creates_marketplace_with_available_policy(tmp_path: Path) -> None:
    m.apply_repo(tmp_path, "example-skills")

    marketplace = json.loads((tmp_path / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))

    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/example-skills"
    assert marketplace["plugins"][0]["policy"]["installation"] == "AVAILABLE"


def test_apply_repo_seeds_python_tooling_guidance(tmp_path: Path) -> None:
    m.apply_repo(tmp_path, "example-skills")

    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    assert "uv tool install ruff" in readme
    assert "uv tool install mypy" in readme
    assert "uv run --group dev pytest" in readme
    assert "`uv`-managed tools" in agents
