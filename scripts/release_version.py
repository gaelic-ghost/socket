#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
from __future__ import annotations

import argparse
import json
import re
import sys
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


def validate_semver(version: str) -> str:
    if not SEMVER_RE.fullmatch(version):
        raise VersionToolError(
            f"Expected a semantic version like 1.2.3 for custom bumps, but got {version!r}."
        )
    return version


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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory and update the maintained version surfaces in the socket superproject."
        )
    )
    parser.add_argument(
        "mode",
        choices=["inventory", "patch", "minor", "major", "custom"],
        help="Inventory current versions or apply a semantic version bump.",
    )
    parser.add_argument(
        "version",
        nargs="?",
        help="Explicit semantic version for custom mode, for example 1.2.3.",
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
