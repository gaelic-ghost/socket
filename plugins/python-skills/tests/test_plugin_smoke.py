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
    manifest = json.loads((REPO_ROOT / ".codex-plugin" / "plugin.json").read_text())
    agents_text = (REPO_ROOT / "AGENTS.md").read_text()

    assert manifest["name"] == "python-skills"
    assert manifest["skills"] == "./skills/"
    assert manifest["homepage"] == "https://github.com/gaelic-ghost/socket/tree/main/plugins/python-skills"
    assert manifest["repository"] == "https://github.com/gaelic-ghost/socket"
    assert manifest["interface"]["displayName"] == "Python Skills"
    assert manifest["interface"]["category"] == "Developer Tools"
    assert manifest["interface"]["websiteURL"] == "https://github.com/gaelic-ghost/socket/tree/main/plugins/python-skills"

    assert ".codex-plugin/plugin.json" in agents_text
    assert "Root [`skills/`](./skills/) is the authored workflow surface" in agents_text


def test_fastmcp_docs_tool_is_host_provided_not_packaged_dependency() -> None:
    for skill_name in ("bootstrap-python-mcp-service", "integrate-fastapi-fastmcp"):
        skill_root = REPO_ROOT / "skills" / skill_name
        metadata = (skill_root / "agents" / "openai.yaml").read_text()
        skill = (skill_root / "SKILL.md").read_text()

        assert "fastmcp_docs" not in metadata
        assert "does not package that server" in skill


def test_service_and_testing_inventory_is_complete() -> None:
    expected = {
        "fastapi-service-workflow",
        "fastmcp-service-workflow",
        "python-testing-workflow",
    }
    actual = {path.parent.name for path in (REPO_ROOT / "skills").glob("*/SKILL.md")}

    assert expected <= actual

    for skill_name in expected:
        assert (REPO_ROOT / "skills" / skill_name / "agents" / "openai.yaml").is_file()


def test_bootstrap_skills_share_one_contract_reference() -> None:
    contract = REPO_ROOT / "shared" / "bootstrap-contract.md"
    assert contract.is_file()

    for skill_name in (
        "bootstrap-uv-python-workspace",
        "bootstrap-python-service",
        "bootstrap-python-mcp-service",
    ):
        skill = (REPO_ROOT / "skills" / skill_name / "SKILL.md").read_text()
        assert "../../shared/bootstrap-contract.md" in skill


def test_python_testing_scripts_use_the_shipped_profile_name() -> None:
    scripts_root = REPO_ROOT / "skills" / "python-testing-workflow" / "scripts"
    for script_name in ("bootstrap_pytest_uv.sh", "run_pytest_uv.sh"):
        script = (scripts_root / script_name).read_text()
        assert 'SKILL_NAME="python-testing-workflow"' in script


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
