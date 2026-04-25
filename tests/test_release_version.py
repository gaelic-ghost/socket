from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "release_version.py"
SPEC = importlib.util.spec_from_file_location("release_version", MODULE_PATH)
assert SPEC and SPEC.loader
release_version = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = release_version
SPEC.loader.exec_module(release_version)


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def make_repo(tmp_path: Path) -> Path:
    write(
        tmp_path / "pyproject.toml",
        """[project]
name = "socket-maintenance"
version = "1.2.3"
""",
    )
    write(
        tmp_path / "uv.lock",
        """version = 1

[[package]]
name = "socket-maintenance"
version = "1.2.3"
""",
    )
    write(
        tmp_path / "plugins" / "python-skills" / "pyproject.toml",
        """[project]
name = "python-skills-maintainer"
version = "1.2.3"
""",
    )
    write(
        tmp_path / "plugins" / "python-skills" / "uv.lock",
        """version = 1

[[package]]
name = "python-skills-maintainer"
version = "1.2.3"
""",
    )
    write(
        tmp_path / "plugins" / "python-skills" / ".codex-plugin" / "plugin.json",
        json.dumps({"name": "python-skills", "version": "1.2.3"}, indent=2) + "\n",
    )
    write(
        tmp_path / "plugins" / "things-app" / ".codex-plugin" / "plugin.json",
        json.dumps({"name": "things-app", "version": "1.2.3"}, indent=2) + "\n",
    )
    write(
        tmp_path / "plugins" / "things-app" / "mcp" / "pyproject.toml",
        """[project]
name = "things-mcp"
version = "1.2.3"
""",
    )
    write(
        tmp_path / "plugins" / "things-app" / "mcp" / "uv.lock",
        """version = 1

[[package]]
name = "things-mcp"
version = "1.2.3"
""",
    )
    write(
        tmp_path / "plugins" / "SpeakSwiftlyServer" / ".codex-plugin" / "plugin.json",
        json.dumps({"name": "speak-swiftly-server", "version": "9.8.7"}, indent=2) + "\n",
    )
    return tmp_path


def test_discover_targets_ignores_build_artifacts(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    write(
        root / "plugins" / "SpeakSwiftlyServer" / ".build" / "checkouts" / "ignored" / "pyproject.toml",
        """[project]
name = "ignored"
version = "9.9.9"
""",
    )

    targets = release_version.discover_targets(root)

    paths = [target.display_path for target in targets]
    assert "plugins/SpeakSwiftlyServer/.build/checkouts/ignored/pyproject.toml" not in paths
    assert "plugins/SpeakSwiftlyServer/.codex-plugin/plugin.json" not in paths
    assert "pyproject.toml" in paths
    assert "plugins/python-skills/.codex-plugin/plugin.json" in paths


def test_patch_requires_aligned_versions(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    plugin_path = root / "plugins" / "things-app" / ".codex-plugin" / "plugin.json"
    plugin_data = json.loads(plugin_path.read_text(encoding="utf-8"))
    plugin_data["version"] = "2.0.0"
    plugin_path.write_text(json.dumps(plugin_data, indent=2) + "\n", encoding="utf-8")

    targets = release_version.discover_targets(root)

    with pytest.raises(release_version.VersionToolError):
        release_version.determine_target_version(targets, "patch", None)


def test_custom_updates_manifests_and_lockfiles(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    targets = release_version.discover_targets(root)

    changed_files, unchanged_files = release_version.apply_version(root, targets, "4.5.6")

    assert "pyproject.toml" in changed_files
    assert "uv.lock" in changed_files
    assert "plugins/python-skills/.codex-plugin/plugin.json" in changed_files
    assert "plugins/things-app/mcp/uv.lock" in changed_files
    assert unchanged_files == []
    assert 'version = "4.5.6"' in (root / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "4.5.6"' in (root / "uv.lock").read_text(encoding="utf-8")
    speak_swiftly_data = json.loads(
        (root / "plugins" / "SpeakSwiftlyServer" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    assert speak_swiftly_data["version"] == "9.8.7"
    plugin_data = json.loads(
        (root / "plugins" / "python-skills" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    assert plugin_data["version"] == "4.5.6"


def test_custom_is_idempotent_when_everything_already_matches(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    targets = release_version.discover_targets(root)

    changed_files, unchanged_files = release_version.apply_version(root, targets, "1.2.3")

    assert changed_files == []
    assert "pyproject.toml" in unchanged_files
    assert "uv.lock" in unchanged_files


def test_main_inventory_reports_misalignment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    root = make_repo(tmp_path)
    plugin_path = root / "plugins" / "things-app" / ".codex-plugin" / "plugin.json"
    plugin_data = json.loads(plugin_path.read_text(encoding="utf-8"))
    plugin_data["version"] = "2.0.0"
    plugin_path.write_text(json.dumps(plugin_data, indent=2) + "\n", encoding="utf-8")
    monkeypatch.setattr(release_version, "repo_root", lambda: root)

    exit_code = release_version.main(["inventory"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Version sets: 1.2.3, 2.0.0" in output
