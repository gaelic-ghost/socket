from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch


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


def _write_symlinked_source_plugin(root: Path, plugin_name: str = "example-plugin") -> Path:
    repo_root = root / "repo"
    canonical_skills = repo_root / "skills" / "hello"
    canonical_skills.mkdir(parents=True)
    canonical_skill_doc = canonical_skills / "SKILL.md"
    canonical_skill_doc.write_text(
        "---\nname: hello\ndescription: Say hello.\n---\n\nSay hello.\n",
        encoding="utf-8",
    )
    plugin_root = repo_root / "plugins" / plugin_name
    (plugin_root / ".codex-plugin").mkdir(parents=True)
    (plugin_root / "hooks").mkdir(parents=True)
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
    (plugin_root / "hooks" / "hooks.json").write_text(json.dumps({"hooks": {}}, indent=2) + "\n", encoding="utf-8")
    (plugin_root / "skills").symlink_to(Path("../../skills"), target_is_directory=True)
    return plugin_root


def _init_git_repo(root: Path) -> None:
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True, capture_output=True, text=True)


def test_repo_scope_audit_reports_missing_targets(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    findings, source_summary, target_plugin_root, marketplace_path, _scope_root, _config_path, _plugin_key, errors = m.audit_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="copy",
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

    apply_actions, source_summary, target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="copy",
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

    apply_actions, _source_summary, target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="personal",
        action="install",
        repo_root=None,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "copy-plugin-tree" for action in apply_actions)
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    entry = marketplace["plugins"][0]
    assert target_plugin_root == fake_home / ".codex" / "plugins" / "example-plugin"
    assert entry["source"]["path"] == "./.codex/plugins/example-plugin"


def test_personal_scope_install_and_uninstall_testing_plugin_round_trip(tmp_path: Path, monkeypatch) -> None:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr(m.Path, "home", lambda: fake_home)
    source_plugin = _write_source_plugin(tmp_path / "source", plugin_name="testing-plugin")
    marketplace_path = fake_home / ".agents" / "plugins" / "marketplace.json"
    marketplace_path.parent.mkdir(parents=True)
    marketplace_path.write_text(
        json.dumps(
            {
                "name": "personal-testing-marketplace",
                "plugins": [
                    {
                        "name": "other-plugin",
                        "source": {"source": "local", "path": "./.codex/plugins/other-plugin"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Productivity",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    install_actions, _source_summary, target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="personal",
        action="install",
        repo_root=None,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "copy-plugin-tree" for action in install_actions)
    assert any(action["action"] == "write-marketplace-entry" for action in install_actions)
    assert target_plugin_root == fake_home / ".codex" / "plugins" / "testing-plugin"
    assert (target_plugin_root / ".codex-plugin" / "plugin.json").exists()
    assert (target_plugin_root / "skills" / "hello" / "SKILL.md").exists()

    install_marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert [item["name"] for item in install_marketplace["plugins"]] == ["other-plugin", "testing-plugin"]
    installed_entry = install_marketplace["plugins"][1]
    assert installed_entry["source"]["path"] == "./.codex/plugins/testing-plugin"
    assert installed_entry["policy"]["installation"] == "AVAILABLE"

    uninstall_actions, _source_summary, target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="personal",
        action="uninstall",
        repo_root=None,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "uninstall-plugin-tree" for action in uninstall_actions)
    assert any(action["action"] == "uninstall-marketplace-entry" for action in uninstall_actions)
    assert not target_plugin_root.exists()

    uninstall_marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert [item["name"] for item in uninstall_marketplace["plugins"]] == ["other-plugin"]


def test_apply_update_rewrites_marketplace_entry_without_dropping_other_plugins(tmp_path: Path) -> None:
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

    apply_actions, _source_summary, _target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="update",
        repo_root=repo_root,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "write-marketplace-entry" for action in apply_actions)
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    names = [item["name"] for item in marketplace["plugins"]]
    assert names == ["example-plugin", "other-plugin"]
    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/example-plugin"


def test_apply_uninstall_removes_plugin_tree_and_marketplace_entry(tmp_path: Path) -> None:
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

    apply_actions, _source_summary, _target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="uninstall",
        repo_root=repo_root,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "uninstall-plugin-tree" for action in apply_actions)
    assert any(action["action"] == "uninstall-marketplace-entry" for action in apply_actions)
    assert not target_plugin_root.exists()
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert [item["name"] for item in marketplace["plugins"]] == ["other-plugin"]


def test_apply_install_repo_scope_uses_existing_tree_when_source_matches_target(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    source_plugin = _write_source_plugin(repo_root / "plugins")

    apply_actions, _source_summary, target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "use-existing-plugin-tree" for action in apply_actions)
    assert not any(action["action"] == "copy-plugin-tree" for action in apply_actions)
    assert target_plugin_root == source_plugin
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/example-plugin"


def test_repo_scope_verify_flags_invalid_sibling_marketplace_entry(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source", plugin_name="agent-plugin-skills")
    repo_root = tmp_path / "repo"
    target_plugin_root = repo_root / "plugins" / "agent-plugin-skills"
    (target_plugin_root / ".codex-plugin").mkdir(parents=True)
    (target_plugin_root / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": "agent-plugin-skills",
                "version": "0.1.0",
                "description": "Installed plugin.",
                "skills": "./skills/",
                "interface": {"displayName": "Agent Plugin Skills", "category": "Productivity"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".agents" / "plugins").mkdir(parents=True)
    (repo_root / ".agents" / "plugins" / "marketplace.json").write_text(
        json.dumps(
            {
                "name": "local-repo",
                "plugins": [
                    {
                        "name": "repo-plugin",
                        "source": {"source": "local", "path": "./"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Productivity",
                    },
                    {
                        "name": "agent-plugin-skills",
                        "source": {"source": "local", "path": "./plugins/agent-plugin-skills"},
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

    findings, _source_summary, _target_plugin_root, marketplace_path, _scope_root, _config_path, _plugin_key, errors = m.audit_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="verify",
        repo_root=repo_root,
        install_mode="copy",
    )

    assert not errors
    issue_ids = {finding.issue_id for finding in findings}
    assert "invalid-marketplace-entry-empty-relative-source-path" in issue_ids
    assert str(marketplace_path) in {finding.path for finding in findings}


def test_repo_scope_defaults_to_current_working_directory(tmp_path: Path, monkeypatch) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    monkeypatch.chdir(repo_root)

    findings, _source_summary, target_plugin_root, marketplace_path, scope_root, _config_path, _plugin_key, errors = m.audit_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=None,
        install_mode="copy",
    )

    assert not errors
    assert {finding.issue_id for finding in findings} == {"missing-target-plugin-root", "missing-marketplace"}
    assert scope_root == repo_root
    assert target_plugin_root == repo_root / "plugins" / "example-plugin"
    assert marketplace_path == repo_root / ".agents" / "plugins" / "marketplace.json"


def test_parse_args_defaults_scope_to_personal(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")

    with patch.object(
        sys,
        "argv",
        [
            "install_plugin_to_socket.py",
            "--source-plugin-root",
            str(source_plugin),
            "--action",
            "install",
            "--run-mode",
            "check-only",
        ],
    ):
        args = m.parse_args()

    assert args.scope is None
    assert args.install_mode == "copy"


def test_resolve_scope_defaults_to_personal_without_config(tmp_path: Path) -> None:
    scope, config, errors = m.resolve_scope(None, tmp_path, None)

    assert not errors
    assert scope == "personal"
    assert config["source"] == "default"


def test_resolve_scope_uses_repo_profile_preference(tmp_path: Path) -> None:
    profile_path = tmp_path / ".codex" / "profiles" / "install-plugin-to-socket" / "customization.yaml"
    profile_path.parent.mkdir(parents=True)
    profile_path.write_text(
        "schemaVersion: 1\nprofile: repo-local-defaults\ndefaultInstallScope: repo-local\n",
        encoding="utf-8",
    )

    scope, config, errors = m.resolve_scope(None, tmp_path, None)

    assert not errors
    assert scope == "repo"
    assert config["source"] == "config"
    assert config["config_path"] == str(profile_path)


def test_resolve_scope_prefers_cli_over_profile(tmp_path: Path) -> None:
    profile_path = tmp_path / ".codex" / "profiles" / "install-plugin-to-socket" / "customization.yaml"
    profile_path.parent.mkdir(parents=True)
    profile_path.write_text("defaultInstallScope: repo\n", encoding="utf-8")

    scope, config, errors = m.resolve_scope("personal", tmp_path, None)

    assert not errors
    assert scope == "personal"
    assert config["source"] == "cli"


def test_resolve_scope_reports_invalid_profile_value(tmp_path: Path) -> None:
    profile_path = tmp_path / ".codex" / "profiles" / "install-plugin-to-socket" / "customization.yaml"
    profile_path.parent.mkdir(parents=True)
    profile_path.write_text("defaultInstallScope: moon-base\n", encoding="utf-8")

    scope, config, errors = m.resolve_scope(None, tmp_path, None)

    assert scope == "personal"
    assert config["source"] == "invalid-config"
    assert errors


def test_resolve_scope_reports_missing_explicit_config(tmp_path: Path) -> None:
    scope, config, errors = m.resolve_scope(None, tmp_path, str(tmp_path / "missing.yaml"))

    assert scope == "personal"
    assert config["source"] == "invalid-config"
    assert "does not exist" in errors[0]


def test_apply_install_repo_scope_can_stage_symlink(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    apply_actions, _source_summary, target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="symlink",
    )

    assert not errors
    assert any(action["action"] == "symlink-plugin-tree" for action in apply_actions)
    assert target_plugin_root.is_symlink()
    assert target_plugin_root.resolve() == source_plugin.resolve()
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert marketplace["plugins"][0]["source"]["path"] == "./plugins/example-plugin"


def test_audit_update_reports_symlink_mode_drift(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="copy",
    )

    findings, _source_summary, _target_plugin_root, _marketplace_path, _scope_root, _config_path, _plugin_key, errors = m.audit_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="update",
        repo_root=repo_root,
        install_mode="symlink",
    )

    assert not errors
    assert "stale-target-materialization" in {finding.issue_id for finding in findings}


def test_audit_update_reports_stale_copied_tree(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="copy",
    )

    updated_skill = source_plugin / "skills" / "hello" / "SKILL.md"
    updated_skill.write_text(
        "---\nname: hello\ndescription: Say hello with updates.\n---\n\nSay hello with updates.\n",
        encoding="utf-8",
    )

    findings, _source_summary, _target_plugin_root, _marketplace_path, _scope_root, _config_path, _plugin_key, errors = m.audit_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="update",
        repo_root=repo_root,
        install_mode="copy",
    )

    assert not errors
    assert "stale-target-copy" in {finding.issue_id for finding in findings}


def test_apply_update_recopies_stale_tree(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="copy",
    )
    updated_skill = source_plugin / "skills" / "hello" / "SKILL.md"
    updated_content = "---\nname: hello\ndescription: Say hello with updates.\n---\n\nSay hello with updates.\n"
    updated_skill.write_text(updated_content, encoding="utf-8")

    apply_actions, _source_summary, target_plugin_root, _marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="update",
        repo_root=repo_root,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "copy-plugin-tree" for action in apply_actions)
    assert (target_plugin_root / "skills" / "hello" / "SKILL.md").read_text(encoding="utf-8") == updated_content


def test_uninstall_removes_staged_symlink_without_touching_source(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="symlink",
    )
    target_plugin_root = repo_root / "plugins" / "example-plugin"

    apply_actions, _source_summary, _target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="uninstall",
        repo_root=repo_root,
        install_mode="symlink",
    )

    assert not errors
    assert any(action["action"] == "uninstall-plugin-tree" for action in apply_actions)
    assert not target_plugin_root.exists()
    assert source_plugin.exists()
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert marketplace["plugins"] == []


def test_audit_reports_tracked_tree_blocking_symlink_mode(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    _init_git_repo(repo_root)
    tracked_plugin = _write_source_plugin(repo_root / "plugins")
    subprocess.run(["git", "add", "."], cwd=repo_root, check=True, capture_output=True, text=True)

    findings, _source_summary, _target_plugin_root, _marketplace_path, _scope_root, _config_path, _plugin_key, errors = m.audit_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="update",
        repo_root=repo_root,
        install_mode="symlink",
    )

    assert not errors
    issue_ids = {finding.issue_id for finding in findings}
    assert "tracked-target-tree-blocks-symlink" in issue_ids
    assert tracked_plugin.exists()


def test_apply_refuses_symlink_mode_for_tracked_tree(tmp_path: Path) -> None:
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    _init_git_repo(repo_root)
    tracked_plugin = _write_source_plugin(repo_root / "plugins")
    subprocess.run(["git", "add", "."], cwd=repo_root, check=True, capture_output=True, text=True)

    apply_actions, _source_summary, target_plugin_root, marketplace_path, _config_path, _plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="update",
        repo_root=repo_root,
        install_mode="symlink",
    )

    assert not apply_actions
    assert errors
    assert "git-tracked plugin tree" in errors[0]
    assert target_plugin_root == tracked_plugin
    assert not marketplace_path.exists()
    assert not target_plugin_root.is_symlink()


def test_resolve_source_plugin_root_from_repo_root_marketplace(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    source_plugin = _write_source_plugin(repo_root / "plugins")
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    marketplace_path.parent.mkdir(parents=True)
    marketplace_path.write_text(
        json.dumps(
            {
                "name": "repo-marketplace",
                "plugins": [
                    {
                        "name": "example-plugin",
                        "source": {"source": "local", "path": "./plugins/example-plugin"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Productivity",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    assert m.resolve_source_plugin_root(repo_root) == source_plugin


def test_enable_and_disable_manage_plugin_config_state(tmp_path: Path, monkeypatch) -> None:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr(m.Path, "home", lambda: fake_home)
    source_plugin = _write_source_plugin(tmp_path / "source")

    m.apply_install(
        requested_source_root=source_plugin,
        scope="personal",
        action="install",
        repo_root=None,
        install_mode="copy",
    )

    enable_actions, _summary, _target, _marketplace, config_path, plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="personal",
        action="enable",
        repo_root=None,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "write-plugin-enabled-state" for action in enable_actions)
    assert config_path == fake_home / ".codex" / "config.toml"
    assert plugin_key == "example-plugin@local-personal"
    assert m.read_plugin_enabled_state(config_path, plugin_key) is True

    disable_actions, _summary, _target, _marketplace, config_path, plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="personal",
        action="disable",
        repo_root=None,
        install_mode="copy",
    )

    assert not errors
    assert any(action["action"] == "write-plugin-enabled-state" for action in disable_actions)
    assert m.read_plugin_enabled_state(config_path, plugin_key) is False


def test_promote_moves_repo_install_to_personal_scope(tmp_path: Path, monkeypatch) -> None:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr(m.Path, "home", lambda: fake_home)
    source_plugin = _write_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="copy",
    )
    m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="disable",
        repo_root=repo_root,
        install_mode="copy",
    )

    apply_actions, _summary, target_plugin_root, marketplace_path, config_path, plugin_key, errors = m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="promote",
        repo_root=repo_root,
        install_mode="copy",
    )

    assert not errors
    assert target_plugin_root == fake_home / ".codex" / "plugins" / "example-plugin"
    assert target_plugin_root.exists()
    assert not (repo_root / "plugins" / "example-plugin").exists()
    assert any(action["action"] == "uninstall-plugin-tree" and action["path"].endswith("/plugins/example-plugin") for action in apply_actions)
    personal_marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    assert [item["name"] for item in personal_marketplace["plugins"]] == ["example-plugin"]
    repo_marketplace = json.loads((repo_root / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
    assert repo_marketplace["plugins"] == []
    assert plugin_key == "example-plugin@local-personal"
    assert m.read_plugin_enabled_state(config_path, plugin_key) is False
    assert m.read_plugin_enabled_state(config_path, "example-plugin@local-repo") is None


def test_verify_reports_missing_enabled_state_for_config_toggle_workflows(tmp_path: Path, monkeypatch) -> None:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr(m.Path, "home", lambda: fake_home)
    source_plugin = _write_source_plugin(tmp_path / "source")

    m.apply_install(
        requested_source_root=source_plugin,
        scope="personal",
        action="install",
        repo_root=None,
        install_mode="copy",
    )

    findings, _summary, _target, _marketplace, _scope_root, config_path, plugin_key, errors = m.audit_install(
        requested_source_root=source_plugin,
        scope="personal",
        action="enable",
        repo_root=None,
        install_mode="copy",
    )

    assert not errors
    assert config_path == fake_home / ".codex" / "config.toml"
    assert plugin_key == "example-plugin@local-personal"
    assert "missing-plugin-enabled-state" in {finding.issue_id for finding in findings}


def test_copy_install_with_symlinked_source_tree_is_not_marked_stale(tmp_path: Path) -> None:
    source_plugin = _write_symlinked_source_plugin(tmp_path / "source")
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    m.apply_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="install",
        repo_root=repo_root,
        install_mode="copy",
    )

    findings, _summary, _target, _marketplace, _scope_root, _config_path, _plugin_key, errors = m.audit_install(
        requested_source_root=source_plugin,
        scope="repo",
        action="verify",
        repo_root=repo_root,
        install_mode="copy",
    )

    assert not errors
    assert "stale-target-copy" not in {finding.issue_id for finding in findings}
