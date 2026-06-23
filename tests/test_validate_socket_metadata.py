from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "validate_socket_metadata.py"
SPEC = importlib.util.spec_from_file_location("validate_socket_metadata", MODULE_PATH)
assert SPEC and SPEC.loader
validate_socket_metadata = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_socket_metadata
SPEC.loader.exec_module(validate_socket_metadata)


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def make_marketplace_repo(tmp_path: Path, manifest: dict[str, object]) -> Path:
    repo_root = tmp_path
    plugin_root = repo_root / "plugins" / "example-skills"
    write(
        repo_root / ".agents" / "plugins" / "marketplace.json",
        json.dumps(
            {
                "interface": {
                    "displayName": "Test Marketplace",
                },
                "plugins": [
                    {
                        "name": "example-skills",
                        "source": {
                            "source": "local",
                            "path": "./plugins/example-skills",
                        },
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Developer Tools",
                    }
                ]
            },
            indent=2,
        )
        + "\n",
    )
    write(plugin_root / ".codex-plugin" / "plugin.json", json.dumps(manifest, indent=2) + "\n")
    write(plugin_root / "skills" / "example" / "SKILL.md", "---\nname: example\n---\n")
    return repo_root


def make_remote_marketplace_repo(
    tmp_path: Path,
    *,
    source: dict[str, object],
) -> Path:
    repo_root = tmp_path
    write(
        repo_root / ".agents" / "plugins" / "marketplace.json",
        json.dumps(
            {
                "interface": {
                    "displayName": "Test Marketplace",
                },
                "plugins": [
                    {
                        "name": "speak-swiftly",
                        "source": source,
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Productivity",
                    }
                ]
            },
            indent=2,
        )
        + "\n",
    )
    return repo_root


def run_validator(repo_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(validate_socket_metadata, "REPO_ROOT", repo_root)
    monkeypatch.setattr(
        validate_socket_metadata,
        "MARKETPLACE_PATH",
        repo_root / ".agents" / "plugins" / "marketplace.json",
    )
    validate_socket_metadata.main()


def test_main_accepts_plugin_manifest_with_root_skills_component(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
        },
    )

    run_validator(repo_root, monkeypatch)


def test_main_accepts_plugin_manifest_with_streamable_http_mcp_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
            "mcpServers": "./.mcp.json",
        },
    )
    write(
        repo_root / "plugins" / "example-skills" / ".mcp.json",
        json.dumps(
            {
                "mcpServers": {
                    "dice": {
                        "url": "https://mcp.dice.com/mcp",
                    }
                }
            },
            indent=2,
        )
        + "\n",
    )

    run_validator(repo_root, monkeypatch)


def test_main_rejects_mcp_config_without_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
            "mcpServers": "./.mcp.json",
        },
    )
    write(
        repo_root / "plugins" / "example-skills" / ".mcp.json",
        json.dumps({"mcpServers": {"dice": {"note": "missing transport"}}}, indent=2) + "\n",
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_accepts_plugin_manifest_with_interface_assets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
            "interface": {
                "composerIcon": "./assets/icon.jpg",
                "logo": "./assets/logo.jpg",
                "screenshots": ["./assets/screenshot.jpg"],
            },
        },
    )
    plugin_root = repo_root / "plugins" / "example-skills"
    write(plugin_root / "assets" / "icon.jpg", "icon")
    write(plugin_root / "assets" / "logo.jpg", "logo")
    write(plugin_root / "assets" / "screenshot.jpg", "screenshot")

    run_validator(repo_root, monkeypatch)


def test_main_accepts_plugin_with_read_only_custom_agent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
        },
    )
    write(
        repo_root / "plugins" / "example-skills" / ".codex" / "agents" / "swift-steward.toml",
        '\n'.join(
            [
                'name = "swift-steward"',
                'description = "Read-heavy Swift repo-maintenance steward."',
                'model = "gpt-5.4-mini"',
                'sandbox_mode = "read-only"',
                'nickname_candidates = ["Swift Steward"]',
                'developer_instructions = """Return a draft review packet with a proposed patch set and validation handoff. Do not apply edits."""',
                "",
            ]
        ),
    )

    run_validator(repo_root, monkeypatch)


def test_main_rejects_custom_agent_without_read_only_sandbox(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
        },
    )
    write(
        repo_root / "plugins" / "example-skills" / ".codex" / "agents" / "swift-steward.toml",
        '\n'.join(
            [
                'name = "swift-steward"',
                'description = "Read-heavy Swift repo-maintenance steward."',
                'sandbox_mode = "workspace-write"',
                'developer_instructions = """Return a draft review packet with a proposed patch set and validation handoff. Do not apply edits."""',
                "",
            ]
        ),
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_rejects_custom_agent_with_empty_model(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
        },
    )
    write(
        repo_root / "plugins" / "example-skills" / ".codex" / "agents" / "swift-steward.toml",
        '\n'.join(
            [
                'name = "swift-steward"',
                'description = "Read-heavy Swift repo-maintenance steward."',
                'model = ""',
                'sandbox_mode = "read-only"',
                'developer_instructions = """Return a draft patch plan for review. Do not apply edits."""',
                "",
            ]
        ),
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_rejects_review_packet_agent_without_report_contract(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
        },
    )
    write(
        repo_root / "plugins" / "example-skills" / ".codex" / "agents" / "repo-docs-auditor.toml",
        '\n'.join(
            [
                'name = "repo-docs-auditor"',
                'description = "Read-heavy docs auditor."',
                'sandbox_mode = "read-only"',
                'developer_instructions = """Return a draft patch plan for review. Do not apply edits."""',
                "",
            ]
        ),
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_rejects_named_review_packet_agent_without_report_contract(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
        },
    )
    write(
        repo_root
        / "plugins"
        / "example-skills"
        / ".codex"
        / "agents"
        / "skills-repo-guidance-sync.toml",
        '\n'.join(
            [
                'name = "skills-repo-guidance-sync"',
                'description = "Read-heavy skills guidance sync."',
                'sandbox_mode = "read-only"',
                'developer_instructions = """Return a draft guidance audit for review. Do not apply edits."""',
                "",
            ]
        ),
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_rejects_custom_agent_without_review_boundary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
        },
    )
    write(
        repo_root / "plugins" / "example-skills" / ".codex" / "agents" / "swift-steward.toml",
        '\n'.join(
            [
                'name = "swift-steward"',
                'description = "Read-heavy Swift repo-maintenance steward."',
                'sandbox_mode = "read-only"',
                'developer_instructions = """Return findings. Do not apply edits."""',
                "",
            ]
        ),
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_rejects_plugin_manifest_with_missing_interface_asset(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./skills/",
            "interface": {
                "composerIcon": "./assets/missing.jpg",
            },
        },
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_rejects_plugin_manifest_missing_root_skills_component(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
        },
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_accepts_unavailable_empty_placeholder_plugin(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path
    plugin_root = repo_root / "plugins" / "placeholder-skills"
    write(
        repo_root / ".agents" / "plugins" / "marketplace.json",
        json.dumps(
            {
                "interface": {
                    "displayName": "Test Marketplace",
                },
                "plugins": [
                    {
                        "name": "placeholder-skills",
                        "source": {
                            "source": "local",
                            "path": "./plugins/placeholder-skills",
                        },
                        "policy": {
                            "installation": "NOT_AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Developer Tools",
                    }
                ]
            },
            indent=2,
        )
        + "\n",
    )
    write(
        plugin_root / ".codex-plugin" / "plugin.json",
        json.dumps({"name": "placeholder-skills"}, indent=2) + "\n",
    )

    run_validator(repo_root, monkeypatch)


def test_main_accepts_root_git_plugin_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_remote_marketplace_repo(
        tmp_path,
        source={
            "source": "url",
            "url": "https://github.com/gaelic-ghost/SpeakSwiftlyServer.git",
            "ref": "main",
        },
    )

    run_validator(repo_root, monkeypatch)


def test_main_accepts_git_subdir_plugin_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_remote_marketplace_repo(
        tmp_path,
        source={
            "source": "git-subdir",
            "url": "https://github.com/example/codex-plugins.git",
            "path": "./plugins/speak-swiftly",
            "sha": "abc123",
        },
    )

    run_validator(repo_root, monkeypatch)


def test_main_rejects_root_git_source_with_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_remote_marketplace_repo(
        tmp_path,
        source={
            "source": "url",
            "url": "https://github.com/gaelic-ghost/SpeakSwiftlyServer.git",
            "path": "./plugins/speak-swiftly",
        },
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_rejects_git_subdir_source_without_relative_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_remote_marketplace_repo(
        tmp_path,
        source={
            "source": "git-subdir",
            "url": "https://github.com/example/codex-plugins.git",
        },
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)


def test_main_rejects_plugin_manifest_with_nonstandard_root_skills_component(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = make_marketplace_repo(
        tmp_path,
        {
            "name": "example-skills",
            "skills": "./other-skills/",
        },
    )

    with pytest.raises(SystemExit):
        run_validator(repo_root, monkeypatch)
