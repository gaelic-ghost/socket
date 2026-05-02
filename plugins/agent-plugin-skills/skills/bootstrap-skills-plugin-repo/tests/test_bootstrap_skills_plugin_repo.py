from __future__ import annotations

import importlib.util
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


def test_apply_repo_creates_expected_discovery_mirrors(tmp_path: Path) -> None:
    actions, created_paths = m.apply_repo(tmp_path, "example-skills")

    assert any(action["action"] == "create-symlink" for action in actions)
    assert (tmp_path / ".agents" / "skills").is_symlink()
    assert os.readlink(tmp_path / ".agents" / "skills") == "../skills"
    assert (tmp_path / ".claude" / "skills").is_symlink()
    assert "README.md" in created_paths
    assert "AGENTS.md" in created_paths
    agents_text = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "Default user-facing Codex plugin install and update guidance to Git-backed marketplace sources" in agents_text
    assert "Resolve shared project dependencies only from GitHub repository URLs" in agents_text
    assert "Machine-local dependency paths are expressly prohibited" in agents_text


def test_audit_repo_flags_forbidden_nested_plugin_dir(tmp_path: Path) -> None:
    (tmp_path / "plugins").mkdir(parents=True)

    findings = m.audit_repo(tmp_path, "example-skills")

    assert any(finding.issue_id == "forbidden-path" for finding in findings)
