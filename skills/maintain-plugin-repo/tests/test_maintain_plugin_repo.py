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

    validator = m.ScriptResult("validate-plugin-install-surfaces", {"metadata_findings": [], "install_surface_findings": [], "mirror_findings": []})
    docs = m.ScriptResult("maintain-plugin-docs", {"readme_findings": [], "roadmap_findings": [], "cross_doc_findings": [], "fixes_applied": []})

    report = m.build_report(
        repo_root=repo_root,
        workflow="audit-only",
        doc_scope="all",
        plugin_name=None,
        source_plugin_root=None,
        target_repo_root=repo_root,
        install_scope="repo",
        install_mode="copy",
        apply_install_repairs=False,
        initial_validator_result=validator,
        validator_result=validator,
        docs_result=docs,
        install_result=None,
    )

    assert report["validation_findings"]["metadata"] == []
    assert report["docs_findings"]["readme"] == []
    assert report["install_findings"] == []
    assert report["deferred_findings"] == []
    assert report["errors"] == []


def test_build_report_defers_install_repairs_without_source_plugin_root(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    validator = m.ScriptResult("validate-plugin-install-surfaces", {"metadata_findings": [], "install_surface_findings": [], "mirror_findings": []})
    docs = m.ScriptResult("maintain-plugin-docs", {"readme_findings": [], "roadmap_findings": [], "cross_doc_findings": [], "fixes_applied": []})

    report = m.build_report(
        repo_root=repo_root,
        workflow="apply-safe-fixes",
        doc_scope="all",
        plugin_name=None,
        source_plugin_root=None,
        target_repo_root=repo_root,
        install_scope="repo",
        install_mode="copy",
        apply_install_repairs=True,
        initial_validator_result=validator,
        validator_result=validator,
        docs_result=docs,
        install_result=None,
    )

    assert report["deferred_findings"] == [
        {
            "owner": "install-plugin-to-socket",
            "reason": "Install repair was requested without `--source-plugin-root`, so local install repair was skipped.",
        }
    ]


def test_main_audit_only_prints_exact_no_findings_for_clean_run(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    validator = m.ScriptResult("validate-plugin-install-surfaces", {"metadata_findings": [], "install_surface_findings": [], "mirror_findings": []})
    docs = m.ScriptResult("maintain-plugin-docs", {"readme_findings": [], "roadmap_findings": [], "cross_doc_findings": [], "fixes_applied": []})

    with patch.object(m, "run_validator", return_value=validator), patch.object(m, "run_docs", return_value=docs), patch.object(
        sys,
        "argv",
        [
            "maintain_plugin_repo.py",
            "--repo-root",
            str(repo_root),
            "--print-md",
        ],
    ):
        rc = m.main()

    assert rc == 0
    assert capsys.readouterr().out.strip() == "No findings."


def test_main_apply_safe_fixes_routes_docs_and_install_reports(tmp_path: Path, capsys) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    source_plugin_root = tmp_path / "plugin"
    source_plugin_root.mkdir()

    validator_initial = m.ScriptResult(
        "validate-plugin-install-surfaces",
        {
            "metadata_findings": [{"path": "README.md", "issue_id": "x", "message": "metadata drift", "surface": "metadata"}],
            "install_surface_findings": [],
            "mirror_findings": [],
        },
    )
    validator_final = m.ScriptResult(
        "validate-plugin-install-surfaces",
        {"metadata_findings": [], "install_surface_findings": [], "mirror_findings": []},
    )
    docs = m.ScriptResult(
        "maintain-plugin-docs",
        {
            "readme_findings": [],
            "roadmap_findings": [],
            "cross_doc_findings": [],
            "fixes_applied": [{"repo": "repo", "file": "README.md", "rule": "rewrite", "status": "applied"}],
        },
    )
    install = m.ScriptResult(
        "install-plugin-to-socket",
        {
            "findings": [],
            "apply_actions": [{"action": "write-marketplace-entry", "path": "/tmp/repo/.agents/plugins/marketplace.json"}],
        },
    )

    with patch.object(m, "run_validator", side_effect=[validator_initial, validator_final]), patch.object(
        m, "run_docs", return_value=docs
    ), patch.object(m, "run_install", return_value=install), patch.object(
        sys,
        "argv",
        [
            "maintain_plugin_repo.py",
            "--repo-root",
            str(repo_root),
            "--workflow",
            "apply-safe-fixes",
            "--source-plugin-root",
            str(source_plugin_root),
            "--apply-install-repairs",
            "--print-json",
        ],
    ):
        rc = m.main()

    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["fixes_applied"][0]["file"] == "README.md"
    assert any(item["rule"] == "write-marketplace-entry" for item in report["fixes_applied"])
    assert report["owner_assignments"]["install-plugin-to-socket"]["attempted"] is True
    assert report["validation_findings"]["metadata"] == []
