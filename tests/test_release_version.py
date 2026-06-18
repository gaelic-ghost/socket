from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

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


def make_evidence() -> Any:
    return release_version.ReleaseEvidence(
        commit="socket-head",
        captured_at="2026-06-18T12:00:00Z",
        marketplace_smoke={
            "status": "passed",
            "marketplace": "socket",
            "source_type": "local",
        },
        dependabot_alerts=(),
    )


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
    assert "as the final cache-refresh step only" in output


def test_patch_refresh_captures_evidence_and_runs_cache_refresh_last(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path)
    commands: list[tuple[str, tuple[str, ...]]] = []

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        command = tuple(args)
        commands.append(("git", command))
        outputs: dict[tuple[str, ...], str] = {
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

    def fake_run_command(
        repo_root: Path,
        args: list[str],
        check: bool = True,
        env: dict[str, str] | None = None,
    ) -> object:
        assert repo_root == root
        assert env is None
        command = tuple(args)
        commands.append(("cmd", command))
        return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    def fake_capture_release_evidence(repo_root: Path, output_path: Path) -> object:
        assert repo_root == root
        assert output_path == root / ".socket-release-evidence.json"
        commands.append(("evidence", (str(output_path),)))
        return make_evidence()

    monkeypatch.setattr(release_version, "run_git", fake_run_git)
    monkeypatch.setattr(release_version, "run_command", fake_run_command)
    monkeypatch.setattr(release_version, "capture_release_evidence", fake_capture_release_evidence)

    targets = release_version.discover_targets(root)
    exit_code = release_version.render_patch_refresh(root, targets, allow_unmerged_branches=False)

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Patch-refresh release completed for v1.2.4." in output
    assert commands[-1] == ("cmd", ("codex", "plugin", "marketplace", "upgrade", "socket"))
    assert ("cmd", ("uv", "run", "scripts/validate_socket_metadata.py")) in commands
    assert ("git", ("push", "origin", "main")) in commands
    assert ("git", ("push", "origin", "v1.2.4")) in commands
    assert commands.index(("evidence", (str(root / ".socket-release-evidence.json"),))) < commands.index(
        ("git", ("tag", "v1.2.4"))
    )
    assert any(command[0] == "cmd" and command[1][:3] == ("gh", "release", "create") for command in commands)
    assert ("cmd", ("gh", "release", "view", "v1.2.4")) in commands
    assert "Capturing release evidence..." in output


def test_capture_release_evidence_records_marketplace_smoke_and_dependabot(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    output_path = root / ".socket-release-evidence.json"

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        outputs: dict[tuple[str, ...], str] = {
            ("status", "--porcelain"): "",
            ("rev-parse", "HEAD"): "socket-head\n",
        }
        return type(
            "Result",
            (),
            {"returncode": 0, "stdout": outputs[tuple(args)], "stderr": ""},
        )()

    def fake_run_command(
        repo_root: Path,
        args: list[str],
        check: bool = True,
        env: dict[str, str] | None = None,
    ) -> object:
        assert repo_root == root
        command = tuple(args)
        if command == ("codex", "plugin", "marketplace", "add", str(root)):
            assert env is not None
            codex_home = Path(env["CODEX_HOME"])
            write(
                codex_home / "config.toml",
                f"""[marketplaces.socket]
source_type = "local"
source = "{root}"
""",
            )
            return type("Result", (), {"returncode": 0, "stdout": "Added marketplace `socket`.", "stderr": ""})()
        if command == ("codex", "plugin", "marketplace", "remove", "socket"):
            assert env is not None
            (Path(env["CODEX_HOME"]) / "config.toml").write_text("", encoding="utf-8")
            return type("Result", (), {"returncode": 0, "stdout": "Removed marketplace `socket`.", "stderr": ""})()
        if command == ("gh", "api", release_version.DEPENDABOT_ALERTS_ENDPOINT):
            assert env is None
            payload = [
                {
                    "number": 42,
                    "dependency": {
                        "package": {"name": "example-package"},
                        "manifest_path": "plugins/example/uv.lock",
                    },
                    "security_advisory": {"severity": "high"},
                }
            ]
            return type(
                "Result",
                (),
                {"returncode": 0, "stdout": json.dumps(payload), "stderr": ""},
            )()
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(release_version, "run_git", fake_run_git)
    monkeypatch.setattr(release_version, "run_command", fake_run_command)

    evidence = release_version.capture_release_evidence(root, output_path)
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert evidence.commit == "socket-head"
    assert evidence.marketplace_smoke["status"] == "passed"
    assert evidence.dependabot_alerts[0]["number"] == 42
    assert payload["dependabot"]["open_alert_count"] == 1
    assert payload["dependabot"]["alerts"][0]["package"] == "example-package"


def test_release_notes_include_captured_evidence() -> None:
    notes = release_version.release_notes("1.2.4", [], make_evidence())

    assert "temporary `CODEX_HOME` Socket marketplace add/remove smoke test" in notes
    assert "found 0 open alert(s)" in notes
    assert "Captured release evidence at `2026-06-18T12:00:00Z`" in notes


def test_load_release_evidence_rejects_a_different_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    evidence_file = root / ".socket-release-evidence.json"
    evidence_file.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "commit": "older-commit",
                "captured_at": "2026-06-18T12:00:00Z",
                "marketplace_smoke": {"status": "passed"},
                "dependabot": {"alerts": []},
            }
        ),
        encoding="utf-8",
    )

    def fake_run_git(repo_root: Path, args: list[str], check: bool = True) -> object:
        assert repo_root == root
        assert args == ["rev-parse", "HEAD"]
        return type("Result", (), {"returncode": 0, "stdout": "current-commit\n", "stderr": ""})()

    monkeypatch.setattr(release_version, "run_git", fake_run_git)

    with pytest.raises(release_version.VersionToolError, match="stale"):
        release_version.load_release_evidence(root, evidence_file)


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
