from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validate_socket = load_module("validate_socket", "validate_socket.py")
validate_skill_metadata = load_module(
    "validate_socket_skill_metadata", "validate_socket_skill_metadata.py"
)


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def test_core_profile_uses_root_owned_checks_only() -> None:
    checks = validate_socket.checks_for_profile("core")

    assert [check.name for check in checks] == [
        "root marketplace metadata",
        "shared skill metadata",
        "root tests",
        "root type checks",
        "root lint",
    ]


def test_full_profile_adds_compatibility_and_child_checks_once() -> None:
    checks = validate_socket.checks_for_profile("full")
    names = [check.name for check in checks]

    assert names.count("Agent Portability Skills tests") == 1
    assert names.count("Repository Skills tests") == 1
    assert names.count("Cybersecurity Skills tests") == 1
    assert names.count("Reverse Engineering Skills tests") == 1
    assert "Hermes compatibility" in names
    assert "Claude compatibility" in names
    assert "release readiness" not in names


def test_validation_profiles_do_not_duplicate_release_choreography() -> None:
    source = (ROOT / "scripts" / "validate_socket.py").read_text(encoding="utf-8")

    assert '"release"' not in source
    assert "release-ready" not in source


def test_full_validation_workflow_installs_declared_zsh_runtime() -> None:
    workflow = (ROOT / ".github" / "workflows" / "validate-socket.yml").read_text(
        encoding="utf-8"
    )

    assert "sudo apt-get install --yes zsh" in workflow
    assert "uv run scripts/validate_socket.py --profile full" in workflow


def test_dry_run_does_not_execute_a_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def unexpected_run(*args: object, **kwargs: object) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(validate_socket.subprocess, "run", unexpected_run)
    validate_socket.run_check(validate_socket.CORE_CHECKS[0], dry_run=True)

    assert not called


def test_shared_skill_validator_accepts_valid_plugin(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    plugin_root = tmp_path / "plugins" / "example-skills"
    write(plugin_root / ".codex-plugin" / "plugin.json", "{}\n")
    write(plugin_root / "AGENTS.md", "# Guidance\n")
    write(
        plugin_root / "skills" / "example-skill" / "SKILL.md",
        "---\nname: example-skill\ndescription: A valid skill.\n---\n",
    )
    write(
        plugin_root / "skills" / "example-skill" / "agents" / "openai.yaml",
        "interface:\n  default_prompt: Use $example-skill.\n",
    )
    monkeypatch.setattr(validate_skill_metadata, "REPO_ROOT", tmp_path)

    assert validate_skill_metadata.main() == 0


def test_shared_skill_validator_rejects_directory_name_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugin_root = tmp_path / "plugins" / "example-skills"
    write(plugin_root / ".codex-plugin" / "plugin.json", "{}\n")
    write(plugin_root / "AGENTS.md", "# Guidance\n")
    write(
        plugin_root / "skills" / "example-skill" / "SKILL.md",
        "---\nname: wrong-name\ndescription: A valid skill.\n---\n",
    )
    monkeypatch.setattr(validate_skill_metadata, "REPO_ROOT", tmp_path)

    with pytest.raises(SystemExit):
        validate_skill_metadata.main()


@pytest.mark.parametrize(
    ("interface", "match"),
    [
        ("interface: {}\n", "non-empty interface"),
        ("interface:\n  default_prompt: Use this skill.\n", "invocation token"),
        ("interface:\n  default_prompt: Use $example-skill.\n  display_name: ''\n", "display_name"),
    ],
)
def test_shared_skill_validator_rejects_invalid_openai_interface(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    interface: str,
    match: str,
) -> None:
    plugin_root = tmp_path / "plugins" / "example-skills"
    write(plugin_root / ".codex-plugin" / "plugin.json", "{}\n")
    write(plugin_root / "AGENTS.md", "# Guidance\n")
    write(
        plugin_root / "skills" / "example-skill" / "SKILL.md",
        "---\nname: example-skill\ndescription: A valid skill.\n---\n",
    )
    write(plugin_root / "skills" / "example-skill" / "agents" / "openai.yaml", interface)
    monkeypatch.setattr(validate_skill_metadata, "REPO_ROOT", tmp_path)

    with pytest.raises(SystemExit):
        validate_skill_metadata.main()
    assert match in capsys.readouterr().err
