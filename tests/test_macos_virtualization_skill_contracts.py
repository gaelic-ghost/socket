from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8").lower()


def test_portability_export_names_every_virtualization_owner() -> None:
    export = text("scripts/export_hermes_skills.py")
    grouping = text("skills.sh.json")
    for skill in (
        "choose-macos-virtualization-shape",
        "virtualization-framework-workflow",
        "linux-development-vm-workflow",
        "macos-development-vm-workflow",
        "prepare-isolated-analysis-lab",
    ):
        assert skill in export
        assert skill in grouping
