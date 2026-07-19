from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8").lower()


def test_apple_container_1x_and_package_versions_are_separate() -> None:
    contents = text("plugins/server-side-swift/skills/apple-containerization-workflow/SKILL.md")
    for phrase in (
        "cli 1.x is the stable command surface",
        "remains a 0.x swift package",
        "do not preserve removed `container system property` commands",
        "container machine workflow",
        "`home-mount=none`",
        "observed `/dev/kvm`",
    ):
        assert phrase in contents


def test_portability_export_names_every_virtualization_owner() -> None:
    export = text("scripts/export_hermes_skills.py")
    grouping = text("skills.sh.json")
    for skill in (
        "choose-macos-virtualization-shape",
        "virtualization-framework-workflow",
        "linux-development-vm-workflow",
        "macos-development-vm-workflow",
        "prepare-isolated-analysis-lab",
        "apple-containerization-workflow",
    ):
        assert skill in export
        assert skill in grouping
