from __future__ import annotations

import os
import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_swiftasb_skills_marketplace_installs_in_temporary_codex_home(
    tmp_path: Path,
) -> None:
    codex = shutil.which("codex")
    if codex is None:
        pytest.skip("codex CLI is not available")

    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()

    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)

    result = subprocess.run(
        [codex, "plugin", "marketplace", "add", str(REPO_ROOT)],
        check=True,
        capture_output=True,
        env=env,
        text=True,
    )

    assert "Added marketplace `socket`" in result.stdout

    config_path = codex_home / "config.toml"
    assert config_path.is_file()

    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    socket_marketplace = config["marketplaces"]["socket"]
    assert socket_marketplace["source_type"] == "local"
    assert socket_marketplace["source"] == str(REPO_ROOT)

    marketplace_path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
    assert marketplace_path.is_file()

    plugin_root = REPO_ROOT / "plugins" / "swiftasb-skills"
    assert (plugin_root / ".codex-plugin" / "plugin.json").is_file()
    assert (plugin_root / "skills" / "explain-swiftasb" / "SKILL.md").is_file()
    assert (plugin_root / "skills" / "choose-integration-shape" / "SKILL.md").is_file()
    assert (plugin_root / "skills" / "build-swiftui-app" / "SKILL.md").is_file()
    assert (plugin_root / "skills" / "build-appkit-app" / "SKILL.md").is_file()
    assert (plugin_root / "skills" / "build-swift-package" / "SKILL.md").is_file()
    assert (plugin_root / "skills" / "diagnose-integration" / "SKILL.md").is_file()
