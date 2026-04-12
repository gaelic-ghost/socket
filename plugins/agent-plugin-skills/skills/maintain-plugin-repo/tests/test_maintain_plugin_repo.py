from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import patch


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "maintain_plugin_repo.py"
    spec = importlib.util.spec_from_file_location("maintain_plugin_repo", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


def test_build_report_keeps_clean_runs_empty(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    report = m.build_report(repo_root, "audit-only", [])

    assert report["validation_findings"]["repo_model"] == []
    assert report["fixes_applied"] == []
    assert report["errors"] == []


def test_audit_repo_model_flags_forbidden_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "plugins").mkdir(parents=True)
    (repo_root / ".agents" / "plugins").mkdir(parents=True)
    (repo_root / ".agents" / "plugins" / "marketplace.json").write_text("{}", encoding="utf-8")

    findings = m.audit_repo_model(repo_root)

    issue_ids = {item["issue_id"] for item in findings}
    assert "forbidden-path" in issue_ids


def test_main_audit_only_prints_exact_no_findings_for_clean_run(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    with patch.object(sys, "argv", ["maintain_plugin_repo.py", "--repo-root", str(repo_root), "--print-md"]):
        rc = m.main()

    assert rc == 0
    assert capsys.readouterr().out.strip() == "No findings."


def test_main_apply_safe_fixes_keeps_empty_fix_list_when_no_safe_fixes_exist(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    with patch.object(sys, "argv", ["maintain_plugin_repo.py", "--repo-root", str(repo_root), "--workflow", "apply-safe-fixes", "--print-json"]):
        rc = m.main()

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["fixes_applied"] == []
    assert list(report["owner_assignments"].keys()) == ["maintain-plugin-repo"]
