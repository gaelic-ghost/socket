from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_package_workflows_expose_package_context() -> None:
    for skill in (
        "swift-package-build-run-workflow",
        "swift-package-testing-workflow",
        "swift-package-extension-workflow",
    ):
        script = read(f"plugins/apple-dev-skills/skills/{skill}/scripts/run_workflow.py")
        assert "package_context" in script


def test_workspace_entrypoint_owns_all_component_roots() -> None:
    script = read("plugins/apple-dev-skills/skills/bootstrap-xcode-workspace/scripts/run_workflow.py")
    for phrase in (
        'choices=("create", "adopt", "add-component", "align")',
        'choices=("app", "extension", "library", "service")',
        "Services/services-shared.yml",
        "workspace-service-component",
        "ensure_services_surface",
    ):
        assert phrase in script


def test_active_xcode_guidance_uses_apps_peer_targets() -> None:
    shared = read("plugins/apple-dev-skills/shared/agents-snippets/apple-xcode-project-core.md")
    extension = read("plugins/apple-dev-skills/skills/app-extension-architecture-workflow/SKILL.md")
    for text in (shared, extension):
        assert "Apps/<Target>" in text or "Apps/<ExtensionTarget>" in text
        assert "never create a root `Extensions/`" in text
    assert "Extension targets use one `Extensions/" not in shared


def test_service_adapter_is_native_local_and_github_cloud_only() -> None:
    script = read("plugins/server-side-swift/skills/workspace-service-component/scripts/run_workflow.py")
    for phrase in (
        "brew services list",
        "SERVICE_POSTGRES_FORMULA",
        "docker/build-push-action@v7",
        "steps.build.outputs.digest",
        "id-token: write",
        "environment:",
        "if: github.event_name != 'pull_request'",
    ):
        assert phrase in script
    assert "docker compose" not in script.lower()
    assert "colima" not in script.lower()


def test_server_deployment_guidance_has_no_local_linux_or_direct_deploy_path() -> None:
    docker = read("plugins/server-side-swift/skills/docker-workflow/SKILL.md")
    fly = read("plugins/server-side-swift/skills/fly-io-deployment-workflow/SKILL.md")
    combined = f"{docker}\n{fly}".lower()
    for forbidden in ("`docker compose up", "`colima start", "`container machine start", "`docker build "):
        assert forbidden not in combined
    for required in ("github actions", "exact image", "protected environment", "rollback"):
        assert required in combined


def test_cloud_contract_records_immutable_container_and_archive_identities() -> None:
    guidance = read(
        "plugins/cloud-deployment-skills/skills/dockerized-service-release-deployment-workflow/SKILL.md"
    )
    assert "registry digest" in guidance
    assert "SHA-256 checksum" in guidance
    assert "clean GitHub Actions checkout" in guidance


def test_soto_is_default_and_official_sdk_requires_a_recorded_exception() -> None:
    skill = read("plugins/server-side-swift/skills/soto-aws-workflow/SKILL.md")
    exception = read(
        "plugins/server-side-swift/skills/soto-aws-workflow/references/official-sdk-exception.template.md"
    )
    for phrase in ("Soto is the default", "one `AWSClient`", "exactly once"):
        assert phrase in skill
    for field in ("Soto version checked", "Evidence link or reproduction", "Review or removal condition"):
        assert field in exception
    lifecycle = read(
        "plugins/server-side-swift/skills/soto-aws-workflow/references/awsclient-lifecycle.md"
    )
    assert "Long-Running Service" in lifecycle
    assert "Warm Lambda Environment" in lifecycle
    assert "try await client.shutdown()" in lifecycle
