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
                "plugins": [
                    {
                        "name": "example-skills",
                        "source": {
                            "source": "local",
                            "path": "./plugins/example-skills",
                        },
                    }
                ]
            },
            indent=2,
        )
        + "\n",
    )
    write(plugin_root / ".codex-plugin" / "plugin.json", json.dumps(manifest, indent=2) + "\n")
    (plugin_root / "skills" / "example").mkdir(parents=True)
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
