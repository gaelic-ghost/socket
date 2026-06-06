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
        tmp_path / "plugins" / "apple-dev-skills" / "pyproject.toml",
        """[project]
name = "apple-dev-skills-maintainer"
version = "1.2.3"
""",
    )
    write(
        tmp_path / "plugins" / "apple-dev-skills" / "uv.lock",
        """version = 1

[[package]]
name = "apple-dev-skills-maintainer"
version = "1.2.3"
""",
    )
    write(
        tmp_path / "plugins" / "apple-dev-skills" / ".codex-plugin" / "plugin.json",
        json.dumps({"name": "apple-dev-skills", "version": "1.2.3"}, indent=2) + "\n",
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
    assert "plugins/apple-dev-skills/.codex-plugin/plugin.json" in changed_files
    assert "plugins/apple-dev-skills/uv.lock" in changed_files
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


def test_release_ready_does_not_push_apple_dev_compatibility_repo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    targets = release_version.discover_targets(root)
    git_outputs = {
        ("status", "--porcelain"): "",
        ("branch", "--show-current"): "main\n",
        ("rev-parse", "HEAD"): "socket-head\n",
        ("rev-parse", "origin/main"): "socket-head\n",
        ("tag", "-l", "v1.2.3"): "",
        ("ls-remote", "--tags", "origin", "refs/tags/v1.2.3"): "",
        ("describe", "--tags", "--abbrev=0", "HEAD^"): "v1.2.2\n",
        ("diff", "--name-only", "v1.2.2..HEAD"): "plugins/apple-dev-skills/skills/example/SKILL.md\n",
    }

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        output = git_outputs[tuple(args)]
        return type("Result", (), {"returncode": 0, "stdout": output, "stderr": ""})()

    monkeypatch.setattr(release_version, "run_git", fake_run_git)

    exit_code = release_version.render_release_ready(root, targets, "1.2.3")

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Release-ready gate passed for v1.2.3." in output
    assert "pushed to apple-dev-skills/main" not in output


def test_release_ready_skips_subtree_push_for_version_only_child_change(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    targets = release_version.discover_targets(root)
    git_outputs = {
        ("status", "--porcelain"): "",
        ("branch", "--show-current"): "main\n",
        ("rev-parse", "HEAD"): "socket-head\n",
        ("rev-parse", "origin/main"): "socket-head\n",
        ("tag", "-l", "v1.2.3"): "",
        ("ls-remote", "--tags", "origin", "refs/tags/v1.2.3"): "",
        ("describe", "--tags", "--abbrev=0", "HEAD^"): "v1.2.2\n",
        (
            "diff",
            "--name-only",
            "v1.2.2..HEAD",
        ): (
            "plugins/apple-dev-skills/.codex-plugin/plugin.json\n"
            "plugins/apple-dev-skills/pyproject.toml\n"
            "plugins/apple-dev-skills/uv.lock\n"
        ),
    }

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        output = git_outputs[tuple(args)]
        return type("Result", (), {"returncode": 0, "stdout": output, "stderr": ""})()

    monkeypatch.setattr(release_version, "run_git", fake_run_git)

    exit_code = release_version.render_release_ready(root, targets, "1.2.3")

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Release-ready gate passed for v1.2.3." in output
    assert "apple-dev-skills" not in output


def test_release_ready_prints_cache_refresh_as_final_step(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    targets = release_version.discover_targets(root)
    git_outputs = {
        ("status", "--porcelain"): "",
        ("branch", "--show-current"): "main\n",
        ("rev-parse", "HEAD"): "socket-head\n",
        ("rev-parse", "origin/main"): "socket-head\n",
        ("tag", "-l", "v1.2.3"): "",
        ("ls-remote", "--tags", "origin", "refs/tags/v1.2.3"): "",
        ("describe", "--tags", "--abbrev=0", "HEAD^"): "v1.2.2\n",
        ("diff", "--name-only", "v1.2.2..HEAD"): "plugins/apple-dev-skills/skills/example/SKILL.md\n",
    }

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        output = git_outputs[tuple(args)]
        return type("Result", (), {"returncode": 0, "stdout": output, "stderr": ""})()

    monkeypatch.setattr(release_version, "run_git", fake_run_git)

    exit_code = release_version.render_release_ready(root, targets, "1.2.3")

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "pushed to apple-dev-skills/main" not in output
    assert "best-effort Mac mini refresh as the final cache-refresh steps only" in output


def test_patch_refresh_runs_cache_refreshes_last(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    commands: list[tuple[str, tuple[str, ...]]] = []
    monkeypatch.setenv("SOCKET_MAC_MINI_REFRESH", "always")

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        command = tuple(args)
        commands.append(("git", command))
        outputs = {
            ("branch", "--show-current"): "main\n",
            ("status", "--porcelain"): "",
            ("tag", "-l", "v1.2.4"): "",
            ("ls-remote", "--tags", "origin", "refs/tags/v1.2.4"): "",
            ("push", "origin", "main"): "",
            ("describe", "--tags", "--abbrev=0", "HEAD^"): "v1.2.3\n",
            (
                "diff",
                "--name-only",
                "v1.2.3..HEAD",
            ): (
                "pyproject.toml\n"
                "uv.lock\n"
                "plugins/apple-dev-skills/.codex-plugin/plugin.json\n"
                "plugins/apple-dev-skills/pyproject.toml\n"
                "plugins/apple-dev-skills/uv.lock\n"
            ),
            ("rev-parse", "HEAD"): "socket-head\n",
            ("rev-parse", "origin/main"): "socket-head\n",
            ("tag", "v1.2.4"): "",
            ("push", "origin", "v1.2.4"): "",
            ("log", "origin/main..main", "--oneline"): "",
            ("branch", "--no-merged", "main"): "",
        }
        if command[:1] == ("add",):
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        if command[:2] == ("commit", "-m"):
            assert command[2] == "release: bump socket patch to 1.2.4"
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        output = outputs[command]
        return type("Result", (), {"returncode": 0, "stdout": output, "stderr": ""})()

    def fake_run_command(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        command = tuple(args)
        commands.append(("cmd", command))
        return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(release_version, "run_git", fake_run_git)
    monkeypatch.setattr(release_version, "run_command", fake_run_command)

    targets = release_version.discover_targets(root)
    exit_code = release_version.render_patch_refresh(root, targets, allow_unmerged_branches=False)

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Patch-refresh release completed for v1.2.4." in output
    assert commands[-2] == ("cmd", ("codex", "plugin", "marketplace", "upgrade", "socket"))
    assert commands[-1] == (
        "cmd",
        (
            "ssh",
            "-o",
            "BatchMode=yes",
            "-o",
            "ConnectTimeout=5",
            "galem@mac-mini.local",
            "codex plugin marketplace upgrade socket",
        ),
    )
    assert ("cmd", ("uv", "run", "scripts/validate_socket_metadata.py")) in commands
    assert ("git", ("push", "origin", "main")) in commands
    assert ("git", ("push", "origin", "v1.2.4")) in commands
    assert any(command[0] == "cmd" and command[1][:3] == ("gh", "release", "create") for command in commands)
    assert ("cmd", ("gh", "release", "view", "v1.2.4")) in commands
    assert "Mac mini marketplace refresh succeeded on galem@mac-mini.local." in output


def test_patch_refresh_reports_mac_mini_refresh_failure_without_failing_release(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    commands: list[tuple[str, tuple[str, ...]]] = []
    monkeypatch.setenv("SOCKET_MAC_MINI_REFRESH", "always")

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        command = tuple(args)
        commands.append(("git", command))
        outputs = {
            ("branch", "--show-current"): "main\n",
            ("status", "--porcelain"): "",
            ("tag", "-l", "v1.2.4"): "",
            ("ls-remote", "--tags", "origin", "refs/tags/v1.2.4"): "",
            ("push", "origin", "main"): "",
            ("describe", "--tags", "--abbrev=0", "HEAD^"): "v1.2.3\n",
            ("diff", "--name-only", "v1.2.3..HEAD"): "pyproject.toml\nuv.lock\n",
            ("rev-parse", "HEAD"): "socket-head\n",
            ("rev-parse", "origin/main"): "socket-head\n",
            ("tag", "v1.2.4"): "",
            ("push", "origin", "v1.2.4"): "",
            ("log", "origin/main..main", "--oneline"): "",
            ("branch", "--no-merged", "main"): "",
        }
        if command[:1] == ("add",):
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        if command[:2] == ("commit", "-m"):
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        output = outputs[command]
        return type("Result", (), {"returncode": 0, "stdout": output, "stderr": ""})()

    def fake_run_command(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        command = tuple(args)
        commands.append(("cmd", command))
        if command[:1] == ("ssh",):
            assert check is False
            return type("Result", (), {"returncode": 255, "stdout": "", "stderr": "host unreachable"})()
        return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(release_version, "run_git", fake_run_git)
    monkeypatch.setattr(release_version, "run_command", fake_run_command)

    targets = release_version.discover_targets(root)
    exit_code = release_version.render_patch_refresh(root, targets, allow_unmerged_branches=False)

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Mac mini marketplace refresh could not run on galem@mac-mini.local. host unreachable" in output
    assert "Patch-refresh release completed for v1.2.4." in output


def test_mac_mini_refresh_skips_by_default_outside_gale_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    commands: list[tuple[str, ...]] = []
    monkeypatch.setenv("HOME", str(tmp_path / "collaborator"))
    monkeypatch.delenv("SOCKET_MAC_MINI_REFRESH", raising=False)

    def fake_run_command(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == tmp_path
        commands.append(tuple(args))
        return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(release_version, "run_command", fake_run_command)

    release_version.refresh_mac_mini_marketplace(tmp_path)

    output = capsys.readouterr().out
    assert commands == []
    assert "Mac mini marketplace refresh skipped because this release is not running from /Users/galew" in output


def test_patch_refresh_stops_before_marketplace_upgrade_when_branch_accounting_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    commands: list[tuple[str, tuple[str, ...]]] = []

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        command = tuple(args)
        commands.append(("git", command))
        outputs = {
            ("branch", "--show-current"): "main\n",
            ("status", "--porcelain"): "",
            ("tag", "-l", "v1.2.4"): "",
            ("ls-remote", "--tags", "origin", "refs/tags/v1.2.4"): "",
            ("push", "origin", "main"): "",
            ("describe", "--tags", "--abbrev=0", "HEAD^"): "v1.2.3\n",
            ("diff", "--name-only", "v1.2.3..HEAD"): "pyproject.toml\nuv.lock\n",
            ("rev-parse", "HEAD"): "socket-head\n",
            ("rev-parse", "origin/main"): "socket-head\n",
            ("tag", "v1.2.4"): "",
            ("push", "origin", "v1.2.4"): "",
            ("log", "origin/main..main", "--oneline"): "",
            ("branch", "--no-merged", "main"): "  feature/unfinished\n",
        }
        if command[:1] == ("add",):
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        if command[:2] == ("commit", "-m"):
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        output = outputs[command]
        return type("Result", (), {"returncode": 0, "stdout": output, "stderr": ""})()

    def fake_run_command(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        command = tuple(args)
        commands.append(("cmd", command))
        return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(release_version, "run_git", fake_run_git)
    monkeypatch.setattr(release_version, "run_command", fake_run_command)

    targets = release_version.discover_targets(root)
    with pytest.raises(release_version.VersionToolError, match="feature/unfinished"):
        release_version.render_patch_refresh(root, targets, allow_unmerged_branches=False)

    assert ("cmd", ("codex", "plugin", "marketplace", "upgrade", "socket")) not in commands
    assert not any(command[0] == "git" and command[1][:2] == ("commit", "-m") for command in commands)
    assert ("git", ("push", "origin", "main")) not in commands
    assert ("git", ("tag", "v1.2.4")) not in commands
