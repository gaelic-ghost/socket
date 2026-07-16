from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "validate_claude_compatibility.py"
SPEC = importlib.util.spec_from_file_location("validate_claude_compatibility", MODULE_PATH)
assert SPEC and SPEC.loader
validate_claude_compatibility = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_claude_compatibility
SPEC.loader.exec_module(validate_claude_compatibility)


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def make_repo(tmp_path: Path) -> Path:
    write(
        tmp_path / ".agents" / "plugins" / "marketplace.json",
        json.dumps(
            {
                "name": "socket",
                "plugins": [
                    {
                        "name": "example-skills",
                        "source": {"source": "local", "path": "./plugins/example-skills"},
                    }
                ],
            }
        ),
    )
    write(tmp_path / "plugins" / "example-skills" / "skills" / "example" / "SKILL.md", "---\nname: example\n---\n")
    write(
        tmp_path / ".claude-plugin" / "marketplace.json",
        json.dumps(
            {
                "name": "socket",
                "owner": {"name": "Test Owner"},
                "description": "Test Claude marketplace.",
                "plugins": [
                    {
                        "name": "example-skills",
                        "source": "./plugins/example-skills",
                        "description": "Example skills.",
                        "strict": False,
                    }
                ],
            }
        ),
    )
    write(
        tmp_path / "docs" / "maintainers" / "claude-compatibility.json",
        json.dumps(
            {
                "schemaVersion": 1,
                "catalog": "socket",
                "entries": {
                    "example-skills": {
                        "claudeCode": "supported",
                        "cowork": "skills_only",
                        "note": "Instruction-only workflow.",
                    }
                },
            }
        ),
    )
    return tmp_path


def configure_paths(repo_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(validate_claude_compatibility, "REPO_ROOT", repo_root)
    monkeypatch.setattr(validate_claude_compatibility, "CODEX_MARKETPLACE_PATH", repo_root / ".agents" / "plugins" / "marketplace.json")
    monkeypatch.setattr(validate_claude_compatibility, "CLAUDE_MARKETPLACE_PATH", repo_root / ".claude-plugin" / "marketplace.json")
    monkeypatch.setattr(validate_claude_compatibility, "INVENTORY_PATH", repo_root / "docs" / "maintainers" / "claude-compatibility.json")
    monkeypatch.setattr(validate_claude_compatibility, "EXCLUDED_CLAUDE_PLUGINS", set())


def test_main_accepts_complete_classification(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)

    assert validate_claude_compatibility.main() == 0


def test_main_rejects_catalog_plugin_without_strict_false(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)
    marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
    document = json.loads(marketplace_path.read_text(encoding="utf-8"))
    document["plugins"][0]["strict"] = True
    marketplace_path.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(validate_claude_compatibility.ValidationError, match="strict to false"):
        validate_claude_compatibility.main()


def test_main_rejects_local_mcp_for_cowork(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)
    inventory_path = repo_root / "docs" / "maintainers" / "claude-compatibility.json"
    document = json.loads(inventory_path.read_text(encoding="utf-8"))
    document["entries"]["example-skills"]["claudeCode"] = "local_mcp"
    document["entries"]["example-skills"]["cowork"] = "remote_mcp"
    inventory_path.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(validate_claude_compatibility.ValidationError, match="must be Cowork skills_only"):
        validate_claude_compatibility.main()
