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
        "build release images in a clean ci checkout by default",
        "one build owns its docker client session until it exits",
        "do not run docker status",
        "inspect the real process rather than trusting the wrapper result",
    ):
        assert phrase in contents


def test_server_docker_workflow_serializes_real_build_processes() -> None:
    contents = text("plugins/server-side-swift/skills/docker-workflow/SKILL.md")
    for phrase in (
        "start that existing runtime as a normal implementation step",
        "treat the actual child build process as the source of truth",
        "do not start a duplicate invocation",
        "do not issue docker status",
    ):
        assert phrase in contents


def test_bootstrap_guidance_preserves_runtime_and_build_ownership() -> None:
    for relative in (
        "plugins/server-side-swift/skills/bootstrap-hummingbird-service/SKILL.md",
        "plugins/server-side-swift/skills/bootstrap-vapor-service/SKILL.md",
        "plugins/server-side-swift/skills/bootstrap-hummingbird-service/assets/AGENTS.md",
        "plugins/server-side-swift/skills/bootstrap-vapor-service/assets/AGENTS.md",
    ):
        contents = text(relative)
        assert "early-returning wrapper" in contents or "wrapper returning" in contents
        assert "runtime that is stopped" in contents
