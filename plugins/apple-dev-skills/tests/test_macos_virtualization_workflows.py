from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def assert_skill_contract(skill: str, *phrases: str) -> None:
    contents = read(f"skills/{skill}/SKILL.md").lower()
    missing = [phrase for phrase in phrases if phrase.lower() not in contents]
    assert not missing, f"{skill} is missing virtualization contract phrases: {missing}"


def test_shape_router_selects_one_boundary_and_records_uncertainty() -> None:
    assert_skill_contract(
        "choose-macos-virtualization-shape",
        "do not return an undecided product menu",
        "apple `container`",
        "persistent oci-backed linux environment",
        "native macos security",
        "secure enclave",
        "virtualization shape record",
    )


def test_framework_workflow_keeps_guest_and_state_models_separate() -> None:
    assert_skill_contract(
        "virtualization-framework-workflow",
        "macos or linux virtualization framework path",
        "require the virtualization entitlement",
        "`validate()` before start",
        "do not call saved machine state a disk snapshot",
        "announce before any visible or resource-intensive launch",
    )


def test_linux_workflow_separates_machine_adapters_and_full_vm() -> None:
    assert_skill_contract(
        "linux-development-vm-workflow",
        "`container machine`",
        "lima/colima adapter",
        "full virtualization framework vm",
        "development convenience is not a security boundary",
        "nested virtualization",
    )


def test_macos_workflow_separates_identity_disk_state_and_evidence() -> None:
    assert_skill_contract(
        "macos-development-vm-workflow",
        "restore images, identity, disks, saved state, clones",
        "sip and relevant controls",
        "do not conflate saved machine state with disk state",
        "physical mac",
    )


def test_inventory_metadata_and_customization_contracts_include_all_four() -> None:
    validator = read(".github/scripts/validate_repo_docs.sh")
    readme = read("README.md")
    manifest = read(".codex-plugin/plugin.json")
    for skill in (
        "choose-macos-virtualization-shape",
        "virtualization-framework-workflow",
        "linux-development-vm-workflow",
        "macos-development-vm-workflow",
    ):
        assert f"./skills/{skill}/SKILL.md" in validator
        assert f"`{skill}`" in readme
        assert (ROOT / "skills" / skill / "agents" / "openai.yaml").is_file()
        assert (ROOT / "skills" / skill / "references" / "customization.template.yaml").is_file()
        assert (ROOT / "skills" / skill / "scripts" / "customization_config.py").is_file()
    assert "Expected exactly 59 active skills" in validator
    assert "virtualization-framework" in manifest
