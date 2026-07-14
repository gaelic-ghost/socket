from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent
EXPORT_MODULE_PATH = ROOT / "scripts" / "export_hermes_skills.py"
EXPORT_SPEC = importlib.util.spec_from_file_location("export_hermes_skills", EXPORT_MODULE_PATH)
assert EXPORT_SPEC and EXPORT_SPEC.loader
export_hermes_skills = importlib.util.module_from_spec(EXPORT_SPEC)
sys.modules[EXPORT_SPEC.name] = export_hermes_skills
EXPORT_SPEC.loader.exec_module(export_hermes_skills)

MODULE_PATH = ROOT / "scripts" / "validate_hermes_compatibility.py"
SPEC = importlib.util.spec_from_file_location("validate_hermes_compatibility", MODULE_PATH)
assert SPEC and SPEC.loader
validate_hermes_compatibility = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate_hermes_compatibility
SPEC.loader.exec_module(validate_hermes_compatibility)


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def make_repo(tmp_path: Path) -> Path:
    source_root = tmp_path / "plugins" / "agent-portability-skills" / "skills"
    for skill_name in export_hermes_skills.EXPORTED_SKILLS:
        write(
            source_root / skill_name / "SKILL.md",
            f"---\nname: {skill_name}\ndescription: Test skill {skill_name}.\n---\n",
        )
    export_root = tmp_path / "skills"
    export_hermes_skills.write_export(source_root, export_root)
    write(
        tmp_path / "skills.sh.json",
        json.dumps(
            {
                "groupings": [
                    {"title": "Test Skills", "skills": list(export_hermes_skills.EXPORTED_SKILLS)}
                ]
            }
        ),
    )
    write(
        tmp_path / "docs" / "maintainers" / "hermes-mcp-examples.yaml",
        "mcp_servers:\n  example:\n    command: tool\n",
    )
    write(
        tmp_path / "plugins" / "example-skills" / ".mcp.json",
        '{"mcpServers": {"example": {"command": "tool"}}}',
    )
    write(
        tmp_path / "docs" / "maintainers" / "hermes-mcp" / "index.yaml",
        "translations:\n  example-skills:\n    source: plugins/example-skills/.mcp.json\n    translation: docs/maintainers/hermes-mcp/example-skills.yaml\n    status: ready\n    required_environment: []\n    setup: Ready for use.\n",
    )
    write(
        tmp_path / "docs" / "maintainers" / "hermes-mcp" / "example-skills.yaml",
        "mcp_servers:\n  example:\n    command: tool\n",
    )
    return tmp_path


def configure_paths(repo_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(export_hermes_skills, "SOURCE_ROOT", repo_root / "plugins" / "agent-portability-skills" / "skills")
    monkeypatch.setattr(export_hermes_skills, "MESSAGING_SOURCE_ROOT", repo_root / "plugins" / "agent-portability-skills" / "skills")
    monkeypatch.setattr(export_hermes_skills, "EXPORT_ROOT", repo_root / "skills")
    monkeypatch.setattr(validate_hermes_compatibility, "REPO_ROOT", repo_root)
    monkeypatch.setattr(validate_hermes_compatibility, "EXPORT_ROOT", repo_root / "skills")
    monkeypatch.setattr(validate_hermes_compatibility, "GROUPINGS_PATH", repo_root / "skills.sh.json")
    monkeypatch.setattr(validate_hermes_compatibility, "MCP_EXAMPLES_PATH", repo_root / "docs" / "maintainers" / "hermes-mcp-examples.yaml")
    monkeypatch.setattr(validate_hermes_compatibility, "MCP_TRANSLATIONS_INDEX_PATH", repo_root / "docs" / "maintainers" / "hermes-mcp" / "index.yaml")


def test_main_accepts_exact_export_and_valid_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)

    assert validate_hermes_compatibility.main() == 0


def test_main_rejects_stale_export(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)
    (repo_root / "skills" / "hermes-agent-compatibility" / "SKILL.md").write_text(
        "---\nname: hermes-agent-compatibility\ndescription: Drifted export.\n---\n",
        encoding="utf-8",
    )

    with pytest.raises(validate_hermes_compatibility.ValidationError, match="stale or incomplete"):
        validate_hermes_compatibility.validate_exported_skills()


def test_main_rejects_unknown_grouped_skill(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)
    write(
        repo_root / "skills.sh.json",
        json.dumps({"groupings": [{"title": "Test", "skills": ["unknown-skill"]}]}),
    )

    with pytest.raises(validate_hermes_compatibility.ValidationError, match="absent"):
        validate_hermes_compatibility.validate_groupings()


def test_main_rejects_machine_local_metadata(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)
    source = repo_root / "plugins" / "agent-portability-skills" / "skills" / "hermes-agent-compatibility" / "SKILL.md"
    source.write_text(
        "---\nname: hermes-agent-compatibility\ndescription: Test skill.\nmetadata:\n  path: /Users/example\n---\n",
        encoding="utf-8",
    )
    export_hermes_skills.write_export()

    with pytest.raises(validate_hermes_compatibility.ValidationError, match="machine-local"):
        validate_hermes_compatibility.validate_exported_skills()


def test_export_check_detects_missing_skill(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    for skill_name in export_hermes_skills.EXPORTED_SKILLS:
        write(source_root / skill_name / "SKILL.md", "---\nname: test\n---\n")
    export_root = tmp_path / "skills"
    export_hermes_skills.write_export(source_root, export_root)
    shutil.rmtree(export_root / "sync-skills-repo-guidance")

    assert not export_hermes_skills.has_exact_export(source_root, export_root)


def test_mcp_translation_rejects_missing_socket_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)
    (repo_root / "plugins" / "example-skills" / ".mcp.json").unlink()

    with pytest.raises(validate_hermes_compatibility.ValidationError, match="no declared Socket .mcp.json source"):
        validate_hermes_compatibility.validate_mcp_translations()


def test_mcp_translation_rejects_undocumented_environment_placeholder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = make_repo(tmp_path)
    configure_paths(repo_root, monkeypatch)
    write(
        repo_root / "docs" / "maintainers" / "hermes-mcp" / "example-skills.yaml",
        "mcp_servers:\n  example:\n    command: tool\n    env:\n      API_KEY: ${API_KEY}\n",
    )

    with pytest.raises(validate_hermes_compatibility.ValidationError, match="undocumented environment placeholders"):
        validate_hermes_compatibility.validate_mcp_translations()
