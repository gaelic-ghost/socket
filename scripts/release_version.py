#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
IGNORED_PARTS = {".build", ".git", ".venv", "__pycache__", "node_modules"}
EXCLUDED_VERSION_PATHS = {
    Path("plugins/SpeakSwiftlyServer/.codex-plugin/plugin.json"),
}
SUBTREE_GATES: tuple[dict[str, str], ...] = ()


class VersionToolError(RuntimeError):
    """Raised when the release-version workflow cannot continue safely."""


@dataclass(frozen=True)
class VersionTarget:
    kind: str
    path: Path
    version: str
    project_name: str | None = None

    @property
    def display_path(self) -> str:
        return self.path.as_posix()


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def run_git(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise VersionToolError(f"`git {' '.join(args)}` failed. {detail}")
    return result


def run_command(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise VersionToolError(f"`{' '.join(args)}` failed. {detail}")
    return result


def validate_semver(version: str) -> str:
    if not SEMVER_RE.fullmatch(version):
        raise VersionToolError(
            f"Expected a semantic version like 1.2.3 for custom bumps, but got {version!r}."
        )
    return version


def normalize_release_version(version: str | None) -> str:
    if version is None:
        raise VersionToolError("release-ready requires the release version, for example 6.6.13.")
    return validate_semver(version.removeprefix("v"))


def bump_version(version: str, mode: str) -> str:
    match = SEMVER_RE.fullmatch(version)
    if not match:
        raise VersionToolError(
            f"Cannot calculate a {mode} bump from non-semver version {version!r}."
        )
    major, minor, patch = (int(match.group(index)) for index in range(1, 4))
    if mode == "patch":
        patch += 1
    elif mode == "minor":
        minor += 1
        patch = 0
    elif mode == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise VersionToolError(f"Unsupported bump mode: {mode}")
    return f"{major}.{minor}.{patch}"


def should_ignore(path: Path) -> bool:
    return path in EXCLUDED_VERSION_PATHS or any(part in IGNORED_PARTS for part in path.parts)


def discover_pyproject_targets(root: Path) -> list[VersionTarget]:
    targets: list[VersionTarget] = []
    candidate_paths = [root / "pyproject.toml"]
    candidate_paths.extend(sorted((root / "plugins").glob("*/pyproject.toml")))
    candidate_paths.extend(sorted((root / "plugins").glob("*/mcp/pyproject.toml")))
    for path in candidate_paths:
        rel_path = path.relative_to(root)
        if should_ignore(rel_path) or not path.is_file():
            continue
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        project = data.get("project")
        if not isinstance(project, dict):
            continue
        version = project.get("version")
        name = project.get("name")
        if not isinstance(version, str) or not isinstance(name, str):
            continue
        targets.append(
            VersionTarget(
                kind="pyproject",
                path=rel_path,
                version=version,
                project_name=name,
            )
        )
    return targets


def discover_plugin_targets(root: Path) -> list[VersionTarget]:
    targets: list[VersionTarget] = []
    for path in sorted((root / "plugins").glob("*/.codex-plugin/plugin.json")):
        rel_path = path.relative_to(root)
        if should_ignore(rel_path) or not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        version = data.get("version")
        if not isinstance(version, str):
            continue
        targets.append(VersionTarget(kind="plugin", path=rel_path, version=version))
    return targets


def discover_targets(root: Path) -> list[VersionTarget]:
    targets = discover_pyproject_targets(root) + discover_plugin_targets(root)
    return sorted(targets, key=lambda target: target.display_path)


def read_versions(targets: list[VersionTarget]) -> list[str]:
    return sorted({target.version for target in targets})


def determine_target_version(targets: list[VersionTarget], mode: str, custom_version: str | None) -> str:
    current_versions = read_versions(targets)
    if mode == "custom":
        if custom_version is None:
            raise VersionToolError("Custom mode requires an explicit semantic version.")
        return validate_semver(custom_version)
    if len(current_versions) != 1:
        joined_versions = ", ".join(current_versions)
        raise VersionToolError(
            "Patch, minor, and major bumps require every maintained version surface to "
            f"already share one version. Current versions: {joined_versions}. "
            "Run `scripts/release.sh custom X.Y.Z` once to align them first."
        )
    return bump_version(current_versions[0], mode)


def replace_project_version(text: str, desired_version: str) -> str:
    lines = text.splitlines(keepends=True)
    in_project = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "[project]":
            in_project = True
            continue
        if in_project and stripped.startswith("[") and stripped != "[project]":
            break
        if in_project and re.match(r'^version\s*=\s*"[^"]+"\s*$', stripped):
            newline = "\n" if line.endswith("\n") else ""
            prefix = line[: len(line) - len(line.lstrip())]
            lines[index] = f'{prefix}version = "{desired_version}"{newline}'
            return "".join(lines)
    raise VersionToolError("Could not find [project].version in pyproject.toml.")


def update_pyproject(path: Path, desired_version: str) -> bool:
    original_text = path.read_text(encoding="utf-8")
    updated_text = replace_project_version(original_text, desired_version)
    if updated_text == original_text:
        return False
    path.write_text(updated_text, encoding="utf-8")
    return True


def update_plugin_manifest(path: Path, desired_version: str) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") == desired_version:
        return False
    data["version"] = desired_version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True


def update_uv_lock(path: Path, project_name: str, desired_version: str) -> bool:
    if not path.is_file():
        return False
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    for index in range(len(lines) - 1):
        if lines[index].strip() == f'name = "{project_name}"' and lines[index + 1].lstrip().startswith("version = "):
            current_line = lines[index + 1]
            newline = "\n" if current_line.endswith("\n") else ""
            replacement = f'version = "{desired_version}"'
            if current_line.strip() == replacement:
                return False
            prefix = current_line[: len(current_line) - len(current_line.lstrip())]
            lines[index + 1] = f"{prefix}{replacement}{newline}"
            path.write_text("".join(lines), encoding="utf-8")
            return True
    raise VersionToolError(
        f"Expected to find package entry for {project_name!r} in {path.as_posix()}, but it was missing."
    )


def apply_version(root: Path, targets: list[VersionTarget], desired_version: str) -> tuple[list[str], list[str]]:
    changed_files: list[str] = []
    unchanged_files: list[str] = []
    for target in targets:
        full_path = root / target.path
        if target.kind == "pyproject":
            changed = update_pyproject(full_path, desired_version)
            lock_path = full_path.with_name("uv.lock")
            lock_changed = False
            if target.project_name is None:
                raise VersionToolError(f"Pyproject target {target.display_path} is missing its project name.")
            if lock_path.is_file():
                lock_changed = update_uv_lock(lock_path, target.project_name, desired_version)
            if changed:
                changed_files.append(target.display_path)
            else:
                unchanged_files.append(target.display_path)
            if lock_changed:
                changed_files.append(lock_path.relative_to(root).as_posix())
            elif lock_path.is_file():
                unchanged_files.append(lock_path.relative_to(root).as_posix())
        elif target.kind == "plugin":
            changed = update_plugin_manifest(full_path, desired_version)
            if changed:
                changed_files.append(target.display_path)
            else:
                unchanged_files.append(target.display_path)
        else:
            raise VersionToolError(f"Unsupported target kind {target.kind!r}.")
    return changed_files, unchanged_files


def render_inventory(targets: list[VersionTarget]) -> int:
    versions = read_versions(targets)
    print("Maintained version targets:")
    for target in targets:
        print(f"- {target.display_path}: {target.version} ({target.kind})")
    if len(versions) == 1:
        print(f"\nShared version: {versions[0]}")
    else:
        print(f"\nVersion sets: {', '.join(versions)}")
        print("Patch/minor/major bumps are blocked until these surfaces are aligned.")
    return 0


def previous_release_ref(root: Path) -> str | None:
    result = run_git(root, ["describe", "--tags", "--abbrev=0", "HEAD^"], check=False)
    if result.returncode != 0:
        return None
    ref = result.stdout.strip()
    return ref or None


def changed_files_since_previous_release(root: Path) -> set[str]:
    previous_ref = previous_release_ref(root)
    diff_args = ["diff", "--name-only", "HEAD"] if previous_ref is None else ["diff", "--name-only", f"{previous_ref}..HEAD"]
    result = run_git(root, diff_args)
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def ensure_clean_checkout(root: Path) -> None:
    result = run_git(root, ["status", "--porcelain"])
    if result.stdout.strip():
        raise VersionToolError(
            "Release-ready gate requires a clean checkout. Commit or stash local changes before tagging."
        )


def ensure_main_matches_origin(root: Path) -> None:
    branch = run_git(root, ["branch", "--show-current"]).stdout.strip()
    if branch != "main":
        raise VersionToolError(f"Release-ready gate must run on local main, but the current branch is {branch!r}.")
    head = run_git(root, ["rev-parse", "HEAD"]).stdout.strip()
    origin_main = run_git(root, ["rev-parse", "origin/main"]).stdout.strip()
    if head != origin_main:
        raise VersionToolError(
            "Release-ready gate requires local main to match origin/main before tagging. "
            "Push or fast-forward main first."
        )


def ensure_on_main(root: Path) -> None:
    branch = run_git(root, ["branch", "--show-current"]).stdout.strip()
    if branch != "main":
        raise VersionToolError(f"Patch-refresh must run on local main, but the current branch is {branch!r}.")


def ensure_tag_is_available(root: Path, version: str) -> None:
    tag = f"v{version}"
    local_tag = run_git(root, ["tag", "-l", tag]).stdout.strip()
    if local_tag:
        raise VersionToolError(f"Release tag {tag} already exists locally; do not create the GitHub release twice.")
    remote_tag = run_git(root, ["ls-remote", "--tags", "origin", f"refs/tags/{tag}"]).stdout.strip()
    if remote_tag:
        raise VersionToolError(f"Release tag {tag} already exists on origin; do not create the GitHub release twice.")


def ensure_versions_match_release(targets: list[VersionTarget], version: str) -> None:
    versions = read_versions(targets)
    if versions != [version]:
        joined_versions = ", ".join(versions)
        raise VersionToolError(
            f"Release-ready gate expected every maintained version surface to be {version}, "
            f"but found: {joined_versions}."
        )


def version_only_paths(targets: list[VersionTarget]) -> set[str]:
    paths: set[str] = set()
    for target in targets:
        paths.add(target.display_path)
        if target.kind == "pyproject":
            paths.add(target.path.with_name("uv.lock").as_posix())
    return paths


def ensure_subtree_gates(root: Path, changed_files: set[str], version_paths: set[str]) -> list[str]:
    accounted: list[str] = []
    for gate in SUBTREE_GATES:
        prefix = gate["prefix"]
        touched_paths = sorted(path for path in changed_files if path == prefix or path.startswith(f"{prefix}/"))
        if not touched_paths:
            accounted.append(f"{gate['name']}: untouched")
            continue
        substantive_paths = [path for path in touched_paths if path not in version_paths]
        if not substantive_paths:
            accounted.append(f"{gate['name']}: version-only changes; no subtree push required")
            continue
        split = run_git(root, ["subtree", "split", f"--prefix={prefix}", "HEAD"]).stdout.strip().splitlines()[-1]
        remote_ref = f"refs/heads/{gate['branch']}"
        remote = run_git(root, ["ls-remote", gate["remote"], remote_ref]).stdout.strip()
        remote_head = remote.split()[0] if remote else ""
        if split != remote_head:
            raise VersionToolError(
                f"{gate['name']} changed in this release, but {gate['remote']}/{gate['branch']} "
                "does not match the current subtree split. Run "
                f"`git subtree push --prefix={prefix} {gate['remote']} {gate['branch']}` before tagging or "
                "creating the GitHub release."
            )
        accounted.append(f"{gate['name']}: pushed to {gate['remote']}/{gate['branch']}")
    return accounted


def push_required_subtrees(root: Path, changed_files: set[str], version_paths: set[str]) -> list[str]:
    accounting: list[str] = []
    for gate in SUBTREE_GATES:
        prefix = gate["prefix"]
        touched_paths = sorted(path for path in changed_files if path == prefix or path.startswith(f"{prefix}/"))
        if not touched_paths:
            accounting.append(f"{gate['name']}: untouched")
            continue
        substantive_paths = [path for path in touched_paths if path not in version_paths]
        if not substantive_paths:
            accounting.append(f"{gate['name']}: version-only changes; no subtree push required")
            continue
        run_git(root, ["subtree", "push", f"--prefix={prefix}", gate["remote"], gate["branch"]])
        accounting.append(f"{gate['name']}: pushed to {gate['remote']}/{gate['branch']}")
    return accounting


def release_notes(version: str, subtree_accounting: list[str]) -> str:
    accounting_lines = "\n".join(f"- {line}" for line in subtree_accounting)
    if not accounting_lines:
        accounting_lines = "- No subtree push required; Socket owns the canonical plugin payloads for this release."
    return (
        f"# Socket v{version}\n\n"
        "## What changed\n\n"
        "- Bumped the shared Socket patch version for a trusted maintainer patch refresh.\n"
        "- Refreshed Git-backed Socket marketplace consumers after the release was published.\n\n"
        "## Breaking changes\n\n"
        "- None.\n\n"
        "## Migration/upgrade notes\n\n"
        "- Run `codex plugin marketplace upgrade socket` to refresh a local Codex install.\n\n"
        "## Verification performed\n\n"
        "- Ran `uv run scripts/validate_socket_metadata.py`.\n"
        "- Ran `scripts/release.sh release-ready "
        f"{version}`.\n"
        "- Verified the GitHub release object after creation.\n"
        "- Verified branch accounting before the marketplace upgrade.\n\n"
        "## Subtree accounting\n\n"
        f"{accounting_lines}\n"
    )


def local_branches_not_contained_by_main(root: Path) -> list[str]:
    result = run_git(root, ["branch", "--no-merged", "main"])
    return [line.strip().lstrip("* ").strip() for line in result.stdout.splitlines() if line.strip()]


def ensure_unmerged_branches_accounted(root: Path, *, allow_unmerged_branches: bool) -> list[str]:
    branches = local_branches_not_contained_by_main(root)
    if branches and not allow_unmerged_branches:
        joined = ", ".join(branches)
        raise VersionToolError(
            "Branch accounting found local branches not contained by main: "
            f"{joined}. Re-run with --allow-unmerged-branches only after each branch is explicitly accounted for."
        )
    return branches


def verify_branch_accounting(root: Path, *, allow_unmerged_branches: bool) -> list[str]:
    ahead = run_git(root, ["log", "origin/main..main", "--oneline"]).stdout.strip()
    if ahead:
        raise VersionToolError(
            "Branch accounting requires local main to have no commits ahead of origin/main. "
            "Push main before continuing."
        )
    return ensure_unmerged_branches_accounted(root, allow_unmerged_branches=allow_unmerged_branches)


def render_branch_accounting(branches: list[str], *, allow_unmerged_branches: bool) -> None:
    print("Branch accounting:")
    if not branches:
        print("- No local branches are outside main.")
        return
    status = "trusted maintainer override accepted" if allow_unmerged_branches else "requires manual accounting"
    for branch in branches:
        print(f"- {branch}: {status}")


def render_release_ready(root: Path, targets: list[VersionTarget], version: str) -> int:
    ensure_versions_match_release(targets, version)
    ensure_clean_checkout(root)
    ensure_main_matches_origin(root)
    ensure_tag_is_available(root, version)
    changed_files = changed_files_since_previous_release(root)
    subtree_accounting = ensure_subtree_gates(root, changed_files, version_only_paths(targets))
    print(f"Release-ready gate passed for v{version}.")
    print("Subtree accounting:")
    for line in subtree_accounting:
        print(f"- {line}")
    print(
        "Next release steps: create and push the tag, create and verify the GitHub release, "
        "run branch accounting, then run `codex plugin marketplace upgrade socket` as the final step only."
    )
    return 0


def render_patch_refresh(root: Path, targets: list[VersionTarget], *, allow_unmerged_branches: bool) -> int:
    ensure_on_main(root)
    ensure_clean_checkout(root)
    preflight_branches = ensure_unmerged_branches_accounted(root, allow_unmerged_branches=allow_unmerged_branches)
    if preflight_branches:
        render_branch_accounting(preflight_branches, allow_unmerged_branches=allow_unmerged_branches)
    desired_version = determine_target_version(targets, "patch", None)
    ensure_tag_is_available(root, desired_version)
    changed_files, unchanged_files = apply_version(root, targets, desired_version)
    print(f"Aligned maintained version surfaces to {desired_version}.")
    print("Updated files:")
    for path in changed_files:
        print(f"- {path}")
    if unchanged_files:
        print("Already current:")
        for path in unchanged_files:
            print(f"- {path}")

    print("Validating root marketplace metadata...")
    run_command(root, ["uv", "run", "scripts/validate_socket_metadata.py"])
    print("Committing patch version bump...")
    run_git(root, ["add", *changed_files])
    run_git(root, ["commit", "-m", f"release: bump socket patch to {desired_version}"])
    print("Pushing main...")
    run_git(root, ["push", "origin", "main"])

    refreshed_targets = discover_targets(root)
    changed_since_release = changed_files_since_previous_release(root)
    print("Checking required subtree pushes...")
    subtree_accounting = push_required_subtrees(root, changed_since_release, version_only_paths(refreshed_targets))
    print("Subtree push accounting:")
    for line in subtree_accounting:
        print(f"- {line}")

    print("Running release-ready gate...")
    render_release_ready(root, refreshed_targets, desired_version)
    tag = f"v{desired_version}"
    print(f"Tagging and pushing {tag}...")
    run_git(root, ["tag", tag])
    run_git(root, ["push", "origin", tag])
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as notes_file:
        notes_file.write(release_notes(desired_version, subtree_accounting))
        notes_path = Path(notes_file.name)
    try:
        print(f"Creating GitHub release {tag}...")
        run_command(
            root,
            [
                "gh",
                "release",
                "create",
                tag,
                "--verify-tag",
                "--title",
                tag,
                "--notes-file",
                str(notes_path),
            ],
        )
    finally:
        notes_path.unlink(missing_ok=True)
    print(f"Verifying GitHub release {tag}...")
    run_command(root, ["gh", "release", "view", tag])
    print("Verifying branch accounting...")
    branches = verify_branch_accounting(root, allow_unmerged_branches=allow_unmerged_branches)
    render_branch_accounting(branches, allow_unmerged_branches=allow_unmerged_branches)
    print("Refreshing the local Codex marketplace cache...")
    run_command(root, ["codex", "plugin", "marketplace", "upgrade", "socket"])
    print(f"Patch-refresh release completed for {tag}.")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory and update the maintained version surfaces in the socket superproject."
        )
    )
    parser.add_argument(
        "mode",
        choices=["inventory", "patch", "minor", "major", "custom", "release-ready", "patch-refresh"],
        help=(
            "Inventory, apply a semantic version bump, verify release gates before tagging, "
            "or run a trusted-maintainer patch refresh."
        ),
    )
    parser.add_argument(
        "version",
        nargs="?",
        help="Explicit semantic version for custom or release-ready mode, for example 1.2.3.",
    )
    parser.add_argument(
        "--allow-unmerged-branches",
        action="store_true",
        help=(
            "Allow patch-refresh to continue after listing local branches not contained by main. "
            "Use only after each branch has been explicitly accounted for."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = repo_root()
    targets = discover_targets(root)
    if not targets:
        raise VersionToolError("No maintained version targets were found in this repository.")
    if args.mode == "inventory":
        return render_inventory(targets)
    if args.mode == "release-ready":
        return render_release_ready(root, targets, normalize_release_version(args.version))
    if args.mode == "patch-refresh":
        if args.version is not None:
            raise VersionToolError("patch-refresh calculates the next patch version automatically; do not pass a version.")
        return render_patch_refresh(root, targets, allow_unmerged_branches=args.allow_unmerged_branches)
    if args.allow_unmerged_branches:
        raise VersionToolError("--allow-unmerged-branches is only valid with patch-refresh.")
    desired_version = determine_target_version(targets, args.mode, args.version)
    changed_files, unchanged_files = apply_version(root, targets, desired_version)
    if changed_files:
        print(f"Aligned maintained version surfaces to {desired_version}.")
        print("Updated files:")
        for path in changed_files:
            print(f"- {path}")
    else:
        print(f"All maintained version surfaces already match {desired_version}.")
    if unchanged_files:
        print("Already current:")
        for path in unchanged_files:
            print(f"- {path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except VersionToolError as error:
        print(f"release-version: {error}", file=sys.stderr)
        raise SystemExit(1)
