from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_command(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        args,
        cwd=cwd or REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=300,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "Command failed.\n"
            f"args={args!r}\n"
            f"cwd={str(cwd or REPO_ROOT)!r}\n"
            f"stdout=\n{completed.stdout}\n"
            f"stderr=\n{completed.stderr}"
        )
    return completed


def test_plugin_manifest_and_marketplace_contract() -> None:
    plugin_root = REPO_ROOT / "plugins" / "python-skills"
    manifest = json.loads((plugin_root / ".codex-plugin" / "plugin.json").read_text())
    claude_manifest = json.loads((plugin_root / ".claude-plugin" / "plugin.json").read_text())
    claude_marketplace = json.loads((REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text())
    readme_text = (REPO_ROOT / "README.md").read_text()

    assert manifest["name"] == "python-skills"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["displayName"] == "Python Skills"
    assert manifest["interface"]["category"] == "Productivity"
    assert claude_manifest["name"] == "python-skills"
    assert claude_manifest["version"] == manifest["version"]

    claude_entry = claude_marketplace["plugins"][0]
    assert claude_entry["name"] == "python-skills"
    assert claude_entry["source"] == "./plugins/python-skills"
    assert (plugin_root / "skills").is_symlink()
    assert (plugin_root / "skills").readlink().as_posix() == "../../skills"
    assert "plugins/python-skills/" in readme_text
    assert "root [`skills/`](./skills/) is the canonical authored workflow surface" in readme_text


def test_fastapi_scaffold_smoke(tmp_path: Path) -> None:
    target = tmp_path / "demo-api"
    run_command(
        "zsh",
        "skills/bootstrap-python-service/scripts/init_python_service.sh",
        "--name",
        "demo-api",
        "--path",
        str(target),
        "--no-git-init",
        "--bypassing-all-profiles",
    )

    assert (target / ".env").is_file()
    assert (target / ".env.local").is_file()
    assert "pydantic-settings" in (target / "pyproject.toml").read_text()


def test_fastmcp_scaffold_smoke(tmp_path: Path) -> None:
    target = tmp_path / "demo-mcp"
    run_command(
        "zsh",
        "skills/bootstrap-python-mcp-service/scripts/init_fastmcp_service.sh",
        "--name",
        "demo-mcp",
        "--path",
        str(target),
        "--no-git-init",
        "--bypassing-all-profiles",
    )

    assert (target / ".env").is_file()
    assert (target / ".env.local").is_file()
    assert "pydantic-settings" in (target / "pyproject.toml").read_text()


def test_workspace_scaffold_smoke(tmp_path: Path) -> None:
    target = tmp_path / "demo-workspace"
    run_command(
        "zsh",
        "skills/bootstrap-uv-python-workspace/scripts/init_uv_python_workspace.sh",
        "--name",
        "demo-workspace",
        "--path",
        str(target),
        "--members",
        "core-lib,api-service",
        "--profile-map",
        "core-lib=package,api-service=service",
        "--no-git-init",
        "--bypassing-all-profiles",
    )

    service_root = target / "packages" / "api-service"
    assert (service_root / ".env").is_file()
    assert (service_root / ".env.local").is_file()
    assert "pydantic-settings" in (service_root / "pyproject.toml").read_text()
