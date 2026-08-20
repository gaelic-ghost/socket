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
    write(tmp_path / "pyproject.toml", '[project]\nname = "socket"\nversion = "1.2.3"\n')
    write(tmp_path / "uv.lock", '[[package]]\nname = "socket"\nversion = "1.2.3"\n')
    write(
        tmp_path / "plugins/example/.codex-plugin/plugin.json",
        json.dumps({"name": "example", "version": "1.2.3"}, indent=2) + "\n",
    )
    write(
        tmp_path / "plugins/example/pyproject.toml",
        '[project]\nname = "example"\nversion = "1.2.3"\n',
    )
    write(
        tmp_path / "plugins/example/uv.lock",
        '[[package]]\nname = "example"\nversion = "1.2.3"\n',
    )
    write(
        tmp_path / "plugins/SpeakSwiftlyServer/.codex-plugin/plugin.json",
        json.dumps({"name": "speak-swiftly", "version": "8.0.0"}, indent=2) + "\n",
    )
    return tmp_path


def test_discover_targets_excludes_external_and_build_artifacts(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    write(
        root / "plugins/example/.build/checkouts/ignored/pyproject.toml",
        '[project]\nname = "ignored"\nversion = "9.9.9"\n',
    )

    paths = [target.display_path for target in release_version.discover_targets(root)]

    assert "plugins/example/.build/checkouts/ignored/pyproject.toml" not in paths
    assert "plugins/SpeakSwiftlyServer/.codex-plugin/plugin.json" not in paths
    assert "plugins/example/.codex-plugin/plugin.json" in paths


def test_major_version_is_calculated_from_one_aligned_version_set(tmp_path: Path) -> None:
    targets = release_version.discover_targets(make_repo(tmp_path))

    assert release_version.determine_target_version(targets, "major", None) == "2.0.0"


def test_automatic_bump_rejects_split_versions(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    path = root / "plugins/example/.codex-plugin/plugin.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "2.0.0"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(release_version.VersionToolError, match="already share one version"):
        release_version.determine_target_version(
            release_version.discover_targets(root), "major", None
        )


def test_apply_version_updates_manifests_and_adjacent_lockfiles(tmp_path: Path) -> None:
    root = make_repo(tmp_path)

    changed, unchanged = release_version.apply_version(
        root, release_version.discover_targets(root), "2.0.0"
    )

    assert unchanged == []
    assert "pyproject.toml" in changed
    assert "uv.lock" in changed
    assert "plugins/example/.codex-plugin/plugin.json" in changed
    assert "plugins/example/uv.lock" in changed
    assert 'version = "2.0.0"' in (root / "plugins/example/uv.lock").read_text()


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
                "captured_at": "2026-08-20T12:00:00Z",
                "marketplace_smoke": {"status": "passed"},
                "dependabot": {"alerts": []},
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        release_version,
        "run_git",
        lambda *_args, **_kwargs: type(
            "Result", (), {"returncode": 0, "stdout": "current-commit\n", "stderr": ""}
        )(),
    )

    with pytest.raises(release_version.VersionToolError, match="stale"):
        release_version.load_release_evidence(root, evidence_file)


def test_release_version_module_has_no_release_choreography_entrypoint() -> None:
    assert not hasattr(release_version, "main")
    assert not hasattr(release_version, "render_patch_refresh")
    assert not hasattr(release_version, "release_notes")
