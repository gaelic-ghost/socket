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
    docs = m.ScriptResult("maintain-plugin-docs", {"readme_findings": [], "roadmap_findings": [], "cross_doc_findings": [], "fixes_applied": []})

    report = m.build_report(repo_root, "audit-only", "all", [], docs)

    assert report["validation_findings"]["repo_model"] == []
    assert report["docs_findings"]["readme"] == []
    assert report["install_findings"] == []
    assert report["errors"] == []


def test_audit_repo_model_flags_forbidden_state(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "plugins").mkdir(parents=True)
    (repo_root / "README.md").write_text(".agents/plugins/marketplace.json\n", encoding="utf-8")

    findings = m.audit_repo_model(repo_root)

    issue_ids = {item["issue_id"] for item in findings}
    assert "forbidden-path" in issue_ids
    assert "forbidden-guidance" in issue_ids


def test_main_audit_only_prints_exact_no_findings_for_clean_run(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    docs = m.ScriptResult("maintain-plugin-docs", {"readme_findings": [], "roadmap_findings": [], "cross_doc_findings": [], "fixes_applied": []})

    with patch.object(m, "run_docs", return_value=docs), patch.object(
        sys,
        "argv",
        ["maintain_plugin_repo.py", "--repo-root", str(repo_root), "--print-md"],
    ):
        rc = m.main()

    assert rc == 0
    assert capsys.readouterr().out.strip() == "No findings."


def test_main_apply_safe_fixes_routes_docs_only(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    docs = m.ScriptResult(
        "maintain-plugin-docs",
        {
            "readme_findings": [],
            "roadmap_findings": [],
            "cross_doc_findings": [],
            "fixes_applied": [{"repo": "repo", "file": "README.md", "rule": "rewrite", "status": "applied"}],
        },
    )

    with patch.object(m, "run_docs", return_value=docs), patch.object(
        sys,
        "argv",
        ["maintain_plugin_repo.py", "--repo-root", str(repo_root), "--workflow", "apply-safe-fixes", "--print-json"],
    ):
        rc = m.main()

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["fixes_applied"][0]["file"] == "README.md"
    assert "maintain-plugin-docs" in report["owner_assignments"]
