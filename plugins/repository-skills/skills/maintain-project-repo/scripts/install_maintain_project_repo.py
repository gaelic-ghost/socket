#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Install or refresh the managed maintain-project-repo files."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


PROFILE_CHOICES = {
    "generic": "Generic repo-maintenance baseline with no Swift or Xcode specialization.",
    "swift-package": "Swift Package Manager repo-maintenance profile for library, tool, and package repos.",
    "xcode-app": "Xcode app repo-maintenance profile for native Apple app repositories.",
}
PROFILE_TOOLKIT_ROOTS = {
    "generic": Path("scripts/repo-maintenance"),
    "swift-package": Path("scripts/repo-maintenance"),
    "xcode-app": Path("Scripts/repo-maintenance"),
}
PROFILE_OVERLAY_FILES = {
    "swift-package": [
        ("profiles/apple/repo-maintenance/.swiftformat", ".swiftformat"),
        ("profiles/apple/repo-maintenance/.swiftlint.yml", ".swiftlint.yml"),
        (
            "profiles/apple/repo-maintenance/hooks/pre-commit.sample",
            "scripts/repo-maintenance/hooks/pre-commit.sample",
        ),
    ],
    "xcode-app": [
        ("profiles/apple/repo-maintenance/.swiftformat", ".swiftformat"),
        ("profiles/apple/repo-maintenance/.swiftlint.yml", ".swiftlint.yml"),
        (
            "profiles/apple/repo-maintenance/hooks/pre-commit.sample",
            "scripts/repo-maintenance/hooks/pre-commit.sample",
        ),
    ],
}
PROFILE_WORKFLOW_FILES = {
    "swift-package": "profiles/apple/github/repo-maintenance-workflows/validate-repo-maintenance.yml",
    "xcode-app": "profiles/apple/github/repo-maintenance-workflows/validate-repo-maintenance.yml",
}
MANAGED_TOOLKIT_FILES = [
    ("repo-maintenance/validate-all.sh", "scripts/repo-maintenance/validate-all.sh"),
    ("repo-maintenance/sync-shared.sh", "scripts/repo-maintenance/sync-shared.sh"),
    ("repo-maintenance/release.sh", "scripts/repo-maintenance/release.sh"),
    ("repo-maintenance/lib/common.sh", "scripts/repo-maintenance/lib/common.sh"),
    ("repo-maintenance/validations/10-toolkit-layout.sh", "scripts/repo-maintenance/validations/10-toolkit-layout.sh"),
    ("repo-maintenance/validations/20-agents-guidance.sh", "scripts/repo-maintenance/validations/20-agents-guidance.sh"),
    ("repo-maintenance/validations/30-ci-wrapper.sh", "scripts/repo-maintenance/validations/30-ci-wrapper.sh"),
    ("repo-maintenance/syncing/README.md", "scripts/repo-maintenance/syncing/README.md"),
    ("repo-maintenance/release/10-preflight.sh", "scripts/repo-maintenance/release/10-preflight.sh"),
    ("repo-maintenance/release/20-tag-release.sh", "scripts/repo-maintenance/release/20-tag-release.sh"),
    ("repo-maintenance/release/30-push-release.sh", "scripts/repo-maintenance/release/30-push-release.sh"),
    ("repo-maintenance/release/40-github-release.sh", "scripts/repo-maintenance/release/40-github-release.sh"),
    ("repo-maintenance/config/validation.env", "scripts/repo-maintenance/config/validation.env"),
    ("repo-maintenance/config/release.env", "scripts/repo-maintenance/config/release.env"),
    ("repo-maintenance/hooks/pre-commit.sample", "scripts/repo-maintenance/hooks/pre-commit.sample"),
]
MANAGED_WORKFLOW_FILE = ".github/workflows/validate-repo-maintenance.yml"
DEFAULT_TOOLKIT_ROOT = Path("scripts/repo-maintenance")
EXECUTABLE_SUFFIXES = {".sh", ".py", ".sample"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--operation", choices=("install", "refresh", "report-only"), default="install")
    parser.add_argument("--profile", choices=sorted(PROFILE_CHOICES), default="generic")
    parser.add_argument("--skip-github-workflow", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def assets_root() -> Path:
    return Path(__file__).resolve().parents[1] / "assets"


def toolkit_root(profile: str) -> Path:
    return PROFILE_TOOLKIT_ROOTS[profile]


def profile_file(profile: str) -> Path:
    return toolkit_root(profile) / "config/profile.env"


def profile_target_path(profile: str, target_relative: str) -> Path:
    target = Path(target_relative)
    try:
        suffix = target.relative_to(DEFAULT_TOOLKIT_ROOT)
    except ValueError:
        return target
    return toolkit_root(profile) / suffix


def target_pairs(profile: str, skip_github_workflow: bool) -> list[tuple[Path, Path]]:
    root = assets_root()
    pairs: list[tuple[Path, Path]] = []

    def add_pair(source_relative: str, target_relative: str) -> None:
        target = profile_target_path(profile, target_relative)
        for index, (_, existing_target) in enumerate(pairs):
            if existing_target == target:
                pairs[index] = (root / source_relative, target)
                return
        pairs.append((root / source_relative, target))

    for source_relative, target_relative in MANAGED_TOOLKIT_FILES:
        add_pair(source_relative, target_relative)
    for source_relative, target_relative in PROFILE_OVERLAY_FILES.get(profile, []):
        add_pair(source_relative, target_relative)
    if not skip_github_workflow:
        workflow_source = PROFILE_WORKFLOW_FILES.get(
            profile,
            "github/repo-maintenance-workflows/validate-repo-maintenance.yml",
        )
        pairs.append(
            (
                root / workflow_source,
                Path(MANAGED_WORKFLOW_FILE),
            )
        )
    return pairs


def ensure_safe_target(repo_root: Path, relative_target: Path) -> None:
    target = repo_root / relative_target
    if target.exists() and not target.is_file():
        raise RuntimeError(
            f"The managed target path {target} exists but is not a regular file."
        )


def legacy_xcode_toolkit_migration(repo_root: Path, profile: str) -> tuple[Path, Path] | None:
    if profile != "xcode-app":
        return None

    legacy_root = repo_root / DEFAULT_TOOLKIT_ROOT
    desired_root = repo_root / toolkit_root(profile)
    if not legacy_root.exists():
        return None

    if desired_root.exists():
        try:
            if legacy_root.samefile(desired_root):
                return None
        except OSError:
            pass
        raise RuntimeError(
            "The xcode-app profile expects repo-maintenance under "
            f"{toolkit_root(profile).as_posix()}, but both {DEFAULT_TOOLKIT_ROOT.as_posix()} "
            f"and {toolkit_root(profile).as_posix()} already exist as separate paths. "
            "Choose the intentional toolkit root, preserve any repo-specific custom files, "
            "and rerun maintain-project-repo."
        )

    if not legacy_root.is_dir():
        raise RuntimeError(
            "The xcode-app profile expects repo-maintenance under "
            f"{toolkit_root(profile).as_posix()}, but the legacy path "
            f"{DEFAULT_TOOLKIT_ROOT.as_posix()} exists and is not a directory."
        )

    return legacy_root, desired_root


def apply_legacy_xcode_toolkit_migration(repo_root: Path, profile: str) -> str | None:
    migration = legacy_xcode_toolkit_migration(repo_root, profile)
    if migration is None:
        return None

    legacy_root, desired_root = migration
    desired_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(legacy_root), str(desired_root))
    try:
        legacy_root.parent.rmdir()
    except OSError:
        pass
    return (
        f"migrated legacy {DEFAULT_TOOLKIT_ROOT.as_posix()} to "
        f"{toolkit_root(profile).as_posix()} for xcode-app profile"
    )


def copy_file(source: Path, target: Path, profile: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if profile == "xcode-app":
        content = source.read_text(encoding="utf-8")
        content = content.replace("scripts/repo-maintenance", "Scripts/repo-maintenance")
        target.write_text(content, encoding="utf-8")
    else:
        shutil.copyfile(source, target)
    if source.suffix in EXECUTABLE_SUFFIXES:
        target.chmod(0o755)


def render_profile_env(profile: str) -> str:
    description = PROFILE_CHOICES[profile]
    return (
        "# Managed by maintain-project-repo. Do not hand-edit unless you also control the installer contract.\n"
        f'REPO_MAINTENANCE_PROFILE="{profile}"\n'
        f'REPO_MAINTENANCE_PROFILE_DESCRIPTION="{description}"\n'
    )


def write_profile_env(repo_root: Path, profile: str) -> None:
    target = repo_root / profile_file(profile)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_profile_env(profile), encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    actions: list[str] = []
    managed_files = [relative.as_posix() for _, relative in target_pairs(args.profile, args.skip_github_workflow)]
    managed_profile_file = profile_file(args.profile)
    managed_files.append(managed_profile_file.as_posix())

    if not repo_root.exists():
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "path_type": "primary",
                    "repo_root": str(repo_root),
                    "managed_files": managed_files,
                    "actions": actions,
                    "stderr": "The requested repo root does not exist.",
                    "next_step": "Create or choose an existing repository root and rerun the workflow.",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    if not repo_root.is_dir():
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "path_type": "primary",
                    "repo_root": str(repo_root),
                    "managed_files": managed_files,
                    "actions": actions,
                    "stderr": "The requested repo root is not a directory.",
                    "next_step": "Use a directory path for --repo-root and rerun the workflow.",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    try:
        planned_migration = legacy_xcode_toolkit_migration(repo_root, args.profile)
        for _, relative_target in target_pairs(args.profile, args.skip_github_workflow):
            ensure_safe_target(repo_root, relative_target)
        ensure_safe_target(repo_root, managed_profile_file)
    except RuntimeError as exc:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "path_type": "primary",
                    "repo_root": str(repo_root),
                    "managed_files": managed_files,
                    "actions": actions,
                    "stderr": str(exc),
                    "next_step": "Resolve the conflicting target path and rerun the workflow.",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    if args.operation == "report-only" or args.dry_run:
        if planned_migration is not None:
            actions.append(
                f"migrate legacy {DEFAULT_TOOLKIT_ROOT.as_posix()} to "
                f"{toolkit_root(args.profile).as_posix()} for xcode-app profile"
            )
        for source, relative_target in target_pairs(args.profile, args.skip_github_workflow):
            target = repo_root / relative_target
            if target.exists():
                actions.append(f"refresh {relative_target.as_posix()} from {source.relative_to(assets_root()).as_posix()}")
            else:
                actions.append(f"install {relative_target.as_posix()} from {source.relative_to(assets_root()).as_posix()}")
        profile_target = repo_root / managed_profile_file
        if profile_target.exists():
            actions.append(f"refresh {managed_profile_file.as_posix()} for {args.profile} profile")
        else:
            actions.append(f"install {managed_profile_file.as_posix()} for {args.profile} profile")
        print(
            json.dumps(
                {
                    "status": "success",
                    "path_type": "fallback",
                    "repo_root": str(repo_root),
                    "profile": args.profile,
                    "managed_files": managed_files,
                    "actions": actions,
                    "validation_result": "skipped (--dry-run)" if args.dry_run else "skipped (report-only)",
                    "next_step": "Run without --dry-run or report-only to install or refresh maintain-project-repo.",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    migration_action = apply_legacy_xcode_toolkit_migration(repo_root, args.profile)
    if migration_action is not None:
        actions.append(migration_action)

    for source, relative_target in target_pairs(args.profile, args.skip_github_workflow):
        target = repo_root / relative_target
        action = "refreshed" if target.exists() else "installed"
        copy_file(source, target, args.profile)
        actions.append(f"{action} {relative_target.as_posix()}")
    profile_target = repo_root / managed_profile_file
    profile_action = "refreshed" if profile_target.exists() else "installed"
    write_profile_env(repo_root, args.profile)
    actions.append(f"{profile_action} {managed_profile_file.as_posix()} for {args.profile} profile")

    print(
        json.dumps(
            {
                "status": "success",
                "path_type": "primary",
                "repo_root": str(repo_root),
                "profile": args.profile,
                "managed_files": managed_files,
                "actions": actions,
                "validation_result": "managed files synced",
                "next_step": f"Use {toolkit_root(args.profile).as_posix()}/validate-all.sh locally and keep CI as a thin wrapper around that command.",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
