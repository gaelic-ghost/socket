#!/usr/bin/env python3
"""Generate Socket's checked-in Hermes skill-tap export from its authored skills."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "plugins" / "agent-portability-skills" / "skills"
EXPORT_ROOT = REPO_ROOT / "skills"
EXPORTED_SKILLS = (
    "bootstrap-skills-plugin-repo",
    "hermes-agent-compatibility",
    "sync-skills-repo-guidance",
)


class ExportError(RuntimeError):
    """Raised when the Hermes skill export cannot be created or verified."""


def validate_sources(source_root: Path | None = None) -> None:
    source_root = SOURCE_ROOT if source_root is None else source_root
    for skill_name in EXPORTED_SKILLS:
        skill_path = source_root / skill_name / "SKILL.md"
        if not skill_path.is_file():
            raise ExportError(
                f"Hermes export source is missing {skill_name}/SKILL.md under {source_root}."
            )


def write_export(
    source_root: Path | None = None,
    export_root: Path | None = None,
) -> None:
    source_root = SOURCE_ROOT if source_root is None else source_root
    export_root = EXPORT_ROOT if export_root is None else export_root
    validate_sources(source_root)
    with tempfile.TemporaryDirectory(prefix="socket-hermes-skills.", dir=export_root.parent) as temp_dir:
        staged_root = Path(temp_dir) / "skills"
        staged_root.mkdir()
        for skill_name in EXPORTED_SKILLS:
            shutil.copytree(source_root / skill_name, staged_root / skill_name)
        if export_root.exists():
            shutil.rmtree(export_root)
        staged_root.replace(export_root)


def has_exact_export(
    source_root: Path | None = None,
    export_root: Path | None = None,
) -> bool:
    source_root = SOURCE_ROOT if source_root is None else source_root
    export_root = EXPORT_ROOT if export_root is None else export_root
    if not export_root.is_dir():
        return False
    source_names = {path.name for path in source_root.iterdir() if path.name in EXPORTED_SKILLS}
    export_names = {path.name for path in export_root.iterdir()}
    if source_names != set(EXPORTED_SKILLS) or export_names != set(EXPORTED_SKILLS):
        return False
    for skill_name in EXPORTED_SKILLS:
        comparison = filecmp.dircmp(source_root / skill_name, export_root / skill_name)
        if comparison.left_only or comparison.right_only or comparison.funny_files:
            return False
        for _, mismatches, errors in _walk_comparison(comparison):
            if mismatches or errors:
                return False
    return True


def _walk_comparison(comparison: filecmp.dircmp) -> list[tuple[list[str], list[str], list[str]]]:
    results = [(comparison.left_only, comparison.diff_files, comparison.funny_files)]
    for child in comparison.subdirs.values():
        results.extend(_walk_comparison(child))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify the checked-in Socket Hermes skill-tap export."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the checked-in export differs from its authored source.",
    )
    args = parser.parse_args(argv)
    if args.check:
        validate_sources()
        if not has_exact_export():
            raise ExportError(
                "Root skills/ is stale or incomplete. Run `uv run scripts/export_hermes_skills.py` "
                "and commit the refreshed export."
            )
        print("Hermes skill-tap export matches its authored source.")
        return 0
    write_export()
    print("Generated the checked-in Hermes skill-tap export at skills/.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ExportError as error:
        print(f"export-hermes-skills: {error}")
        raise SystemExit(1)
