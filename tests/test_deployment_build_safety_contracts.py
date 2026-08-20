from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8").lower()


def test_release_workflow_requires_target_and_session_preflight() -> None:
    contents = text(
        "plugins/cloud-deployment-skills/skills/"
        "dockerized-service-release-deployment-workflow/SKILL.md"
    )
    for phrase in (
        "deployment target's architecture",
        "build every cloud linux archive and oci image in a clean github actions checkout",
        "one build owns its docker client session until it exits",
        "do not run docker status",
        "inspect the real process rather than trusting the wrapper result",
    ):
        assert phrase in contents


def test_server_docker_workflow_enforces_github_only_cloud_builds() -> None:
    contents = text("plugins/server-side-swift/skills/docker-workflow/SKILL.md")
    for phrase in (
        "run docker, buildkit, and image-smoke-test commands in github actions only",
        "treat the actual child build process as the source of truth",
        "do not start a duplicate invocation",
        "do not issue docker status",
    ):
        assert phrase in contents


def test_workspace_service_adapter_uses_native_local_and_github_cloud_boundaries() -> None:
    contents = text("plugins/server-side-swift/skills/workspace-service-component/SKILL.md")
    assert "homebrew services" in contents
    assert "github actions" in contents
    assert "do not add docker compose" in contents
