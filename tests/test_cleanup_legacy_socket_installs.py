from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parent.parent / "scripts" / "cleanup_legacy_socket_installs.py"
)
SPEC = importlib.util.spec_from_file_location("cleanup_legacy_socket_installs", MODULE_PATH)
assert SPEC and SPEC.loader
cleanup_legacy_socket_installs = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cleanup_legacy_socket_installs
SPEC.loader.exec_module(cleanup_legacy_socket_installs)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_plugin_manifest(plugin_root: Path, name: str) -> None:
    write_json(plugin_root / ".codex-plugin" / "plugin.json", {"name": name})


def test_plan_marketplace_cleanup_removes_only_known_socket_plugins(tmp_path: Path) -> None:
    marketplace_path = tmp_path / ".agents" / "plugins" / "marketplace.json"
    write_json(
        marketplace_path,
        {
            "name": "personal",
            "plugins": [
                {
                    "name": "apple-dev-skills",
                    "source": {
                        "source": "local",
                        "path": "/Users/example/socket/plugins/apple-dev-skills",
                    },
                },
                {
                    "name": "unrelated",
                    "source": {
                        "source": "local",
                        "path": "/Users/example/.codex/plugins/unrelated",
                    },
                },
            ],
        },
    )

    rewrite = cleanup_legacy_socket_installs.plan_marketplace_cleanup(marketplace_path)

    assert rewrite is not None
    assert rewrite.removed_names == ("apple-dev-skills",)
    assert rewrite.data is not None
    assert rewrite.data["plugins"] == [
        {
            "name": "unrelated",
            "source": {
                "source": "local",
                "path": "/Users/example/.codex/plugins/unrelated",
            },
        }
    ]


def test_plan_marketplace_cleanup_deletes_socket_only_marketplace(tmp_path: Path) -> None:
    marketplace_path = tmp_path / ".agents" / "plugins" / "marketplace.json"
    write_json(
        marketplace_path,
        {
            "name": "socket",
            "plugins": [
                {
                    "name": "agent-plugin-skills",
                    "source": {
                        "source": "local",
                        "path": "/Users/example/socket/plugins/agent-plugin-skills",
                    },
                }
            ],
        },
    )

    rewrite = cleanup_legacy_socket_installs.plan_marketplace_cleanup(marketplace_path)

    assert rewrite is not None
    assert rewrite.data is None
    assert rewrite.removed_names == ("agent-plugin-skills",)


def test_plan_plugin_dir_cleanup_skips_cache_and_unknown_payloads(tmp_path: Path) -> None:
    codex_plugins_root = tmp_path / ".codex" / "plugins"
    write_plugin_manifest(codex_plugins_root / "apple-dev-skills", "apple-dev-skills")
    write_plugin_manifest(codex_plugins_root / "unrelated", "unrelated")
    write_plugin_manifest(
        codex_plugins_root / "cache" / "socket" / "things-app" / "6.3.1",
        "things-app",
    )

    actions = cleanup_legacy_socket_installs.plan_plugin_dir_cleanup(codex_plugins_root)

    assert [action.target for action in actions] == [codex_plugins_root / "apple-dev-skills"]


def test_apply_backs_up_and_removes_legacy_directory(tmp_path: Path) -> None:
    home = tmp_path
    backup_root = home / ".codex" / "backups" / "test"
    plugin_dir = home / ".codex" / "plugins" / "python-skills"
    write_plugin_manifest(plugin_dir, "python-skills")
    action = cleanup_legacy_socket_installs.PlannedAction(
        kind="remove-directory",
        target=plugin_dir,
        description="remove test plugin",
    )

    cleanup_legacy_socket_installs.apply_action(action, home=home, backup_root=backup_root)

    assert not plugin_dir.exists()
    assert (
        backup_root
        / ".codex"
        / "plugins"
        / "python-skills"
        / ".codex-plugin"
        / "plugin.json"
    ).is_file()


def test_stale_config_plugin_tables_reports_non_socket_marketplaces(tmp_path: Path) -> None:
    config_path = tmp_path / ".codex" / "config.toml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(
        "\n".join(
            [
                '[plugins."apple-dev-skills@socket"]',
                "enabled = true",
                '[plugins."apple-dev-skills@local-repo"]',
                "enabled = true",
                '[plugins."unrelated@local-repo"]',
                "enabled = true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    stale_tables = cleanup_legacy_socket_installs.stale_config_plugin_tables(config_path)

    assert stale_tables == ["apple-dev-skills@local-repo"]
