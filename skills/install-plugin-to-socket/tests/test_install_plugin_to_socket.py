from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "install_plugin_to_socket.py"
    spec = importlib.util.spec_from_file_location("install_plugin_to_socket", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


def _write_source_plugin(root: Path, plugin_name: str = "example-plugin") -> Path:
    plugin_root = root / plugin_name
    (plugin_root / ".codex-plugin").mkdir(parents=True)
    (plugin_root / "skills" / "hello").mkdir(parents=True)
    (plugin_root / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": plugin_name,
                "version": "0.1.0",
                "description": "Example plugin.",
                "skills": "./skills/",
                "interface": {
                    "displayName": "Example Plugin",
                    "category": "Productivity",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (plugin_root / "skills" / "hello" / "SKILL.md").write_text(
        "---\nname: hello\ndescription: Say hello.\n---\n\nSay hello.\n",
        encoding="utf-8",
    )
    return plugin_root


def test_repo_scope_audit_reports_missing_targets(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    findings, source_summary, target_plugin_root, marketplace_path, _scope_root, errors = m.audit_install(
        source_plugin_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
    )

    assert not errors
    issue_ids = {finding.issue_id for finding in findings}
    assert "missing-target-plugin-root" in issue_ids
    assert "missing-marketplace" in issue_ids
    assert source_summary["name"] == "example-plugin"
    assert target_plugin_root == repo_root / "plugins" / "example-plugin"
    assert marketplace_path == repo_root / ".agents" / "plugins" / "marketplace.json"


def test_apply_install_repo_scope_copies_plugin_and_writes_marketplace(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    apply_actions, source_summary, target_plugin_root, marketplace_path, errors = m.apply_install(
        source_plugin_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
    )

    assert not errors
    assert any(action["action"] == "copy-plugin-tree" for action in apply_actions)
    assert any(action["action"] == "write-marketplace-entry" for action in apply_actions)
    assert (target_plugin_root / ".codex-plugin" / "plugin.json").exists()
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    entry = marketplace["plugins"][0]
    assert entry["name"] == "example-plugin"
    assert entry["source"]["path"] == "./plugins/example-plugin"
    assert source_summary["version"] == "0.1.0"


def test_apply_install_personal_scope_uses_home_relative_paths(tmp_path: Path, monkeypatch) -> None:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr(m.Path, "home", lambda: fake_home)
    source_plugin = _write_source_plugin(tmp_path / "source")

    apply_actions, _source_summary, target_plugin_root, marketplace_path, errors = m.apply_install(
        source_plugin_root=source_plugin,
        scope="personal",
        action="install",
        repo_root=None,
    )

    assert not errors
    assert any(action["action"] == "copy-plugin-tree" for action in apply_actions)
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    entry = marketplace["plugins"][0]
    assert target_plugin_root == fake_home / ".codex" / "plugins" / "example-plugin"
    assert entry["source"]["path"] == "./.codex/plugins/example-plugin"


def test_apply_refresh_rewrites_marketplace_entry_without_dropping_other_plugins(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    (repo_root / ".agents" / "plugins").mkdir(parents=True)
    (repo_root / "plugins" / "example-plugin").mkdir(parents=True)
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    marketplace_path.write_text(
        json.dumps(
            {
                "name": "local-repo",
                "plugins": [
                    {
                        "name": "example-plugin",
                        "source": {"source": "local", "path": "./plugins/wrong-path"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Productivity",
                    },
                    {
                        "name": "other-plugin",
                        "source": {"source": "local", "path": "./plugins/other-plugin"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Productivity",
                    },
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    apply_actions, _source_summary, _target_plugin_root, marketplace_path, errors = m.apply_install(
        source_plugin_root=source_plugin,
        scope="repo",
        action="refresh",
        repo_root=repo_root,
    )

    assert not errors
    assert any(action["action"] == "write-marketplace-entry" for action in apply_actions)
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    names = [item["name"] for item in marketplace["plugins"]]
    assert names == ["example-plugin", "other-plugin"]
    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/example-plugin"


def test_apply_detach_removes_plugin_tree_and_marketplace_entry(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    target_plugin_root = repo_root / "plugins" / "example-plugin"
    (target_plugin_root / ".codex-plugin").mkdir(parents=True)
    (target_plugin_root / ".codex-plugin" / "plugin.json").write_text(
        (source_plugin / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    marketplace_path.parent.mkdir(parents=True)
    marketplace_path.write_text(
        json.dumps(
            {
                "name": "local-repo",
                "plugins": [
                    {
                        "name": "example-plugin",
                        "source": {"source": "local", "path": "./plugins/example-plugin"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Productivity",
                    },
                    {
                        "name": "other-plugin",
                        "source": {"source": "local", "path": "./plugins/other-plugin"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Productivity",
                    },
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    apply_actions, _source_summary, _target_plugin_root, marketplace_path, errors = m.apply_install(
        source_plugin_root=source_plugin,
        scope="repo",
        action="detach",
        repo_root=repo_root,
    )

    assert not errors
    assert any(action["action"] == "remove-plugin-tree" for action in apply_actions)
    assert any(action["action"] == "remove-marketplace-entry" for action in apply_actions)
    assert not target_plugin_root.exists()
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert [item["name"] for item in marketplace["plugins"]] == ["other-plugin"]
