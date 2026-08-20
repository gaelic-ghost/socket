from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_retired_standalone_and_sync_skills_are_absent() -> None:
    for relative in (
        "plugins/apple-dev-skills/skills/sync-swift-package-guidance",
        "plugins/server-side-swift/skills/bootstrap-hummingbird-service",
        "plugins/server-side-swift/skills/bootstrap-vapor-service",
        "plugins/server-side-swift/skills/sync-hummingbird-service-guidance",
    ):
        assert not (ROOT / relative / "SKILL.md").exists()


def test_package_workflows_have_no_repo_classifier_or_mixed_root_opt_in() -> None:
    for skill in (
        "swift-package-workflow",
        "swift-package-build-run-workflow",
        "swift-package-testing-workflow",
        "swift-package-extension-workflow",
    ):
        script = read(f"plugins/apple-dev-skills/skills/{skill}/scripts/run_workflow.py")
        assert "mixed_root" not in script
        assert "mixed-root-opt-in" not in script
        assert "repo_shape" not in script
        assert "xcode_markers" not in script
        assert "package_context" in script


def test_workspace_entrypoint_owns_all_component_roots() -> None:
    script = read("plugins/apple-dev-skills/skills/bootstrap-xcode-workspace/scripts/run_workflow.py")
    for phrase in (
        'choices=("create", "add-component", "align")',
        'choices=("app", "library", "service")',
        "Services/services-shared.yml",
        "workspace-service-component",
        "ensure_services_surface",
    ):
        assert phrase in script


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
