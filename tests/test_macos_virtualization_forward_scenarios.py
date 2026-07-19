from __future__ import annotations

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent


def skill(plugin: str, name: str) -> str:
    return (ROOT / "plugins" / plugin / "skills" / name / "SKILL.md").read_text(encoding="utf-8").lower()


@pytest.mark.parametrize(
    ("plugin", "name", "phrases"),
    [
        (
            "apple-dev-skills",
            "choose-macos-virtualization-shape",
            ("one portable linux application", "persistent oci-backed linux environment", "native macos security"),
        ),
        (
            "apple-dev-skills",
            "virtualization-framework-workflow",
            ("configuration construction", "headless", "add only required devices"),
        ),
        (
            "apple-dev-skills",
            "macos-development-vm-workflow",
            ("sip and relevant controls", "clean baseline", "restore-image support"),
        ),
        (
            "apple-dev-skills",
            "virtualization-framework-workflow",
            ("save/restore only in documented states", "configuration compatible", "not call saved machine state a disk snapshot"),
        ),
        (
            "server-side-swift",
            "apple-containerization-workflow",
            ("disposable application container", "persistent linux development environment", "home-mount=none"),
        ),
        (
            "server-side-swift",
            "apple-containerization-workflow",
            ("supported apple silicon", "compatible kernel configuration", "observed `/dev/kvm`"),
        ),
        (
            "cybersecurity-skills",
            "prepare-isolated-analysis-lab",
            ("offline static tooling", "default host folders/home sharing", "verify teardown"),
        ),
        (
            "cybersecurity-skills",
            "prepare-isolated-analysis-lab",
            ("monitored macos dynamic analysis", "baseline state or hashes", "virtualization artifacts"),
        ),
        (
            "apple-dev-skills",
            "choose-macos-virtualization-shape",
            ("do not call a linux container or linux vm evidence for native macos behavior", "gatekeeper", "tcc"),
        ),
        (
            "apple-dev-skills",
            "choose-macos-virtualization-shape",
            ("secure enclave", "recoveryos", "physical mac"),
        ),
    ],
)
def test_planned_forward_scenario_has_an_explicit_decision_path(
    plugin: str, name: str, phrases: tuple[str, ...]
) -> None:
    contents = skill(plugin, name)
    missing = [phrase for phrase in phrases if phrase not in contents]
    assert not missing, f"{plugin}:{name} is missing forward-test decisions: {missing}"
