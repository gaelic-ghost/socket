#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
DEFAULT_RELEASE_EVIDENCE_PATH = Path(".socket-release-evidence.json")
DEPENDABOT_ALERTS_ENDPOINT = "repos/gaelic-ghost/socket/dependabot/alerts?state=open&per_page=100"


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


@dataclass(frozen=True)
class ReleaseEvidence:
    commit: str
    captured_at: str
    marketplace_smoke: dict[str, Any]
    dependabot_alerts: tuple[dict[str, str | int], ...]


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


def run_command(
    root: Path,
    args: list[str],
    check: bool = True,
    env: dict[str, str] | None = None,
    timeout_seconds: int | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            args,
            cwd=root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as error:
        raise VersionToolError(
            f"`{' '.join(args)}` timed out after {timeout_seconds}s."
        ) from error
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise VersionToolError(f"`{' '.join(args)}` failed. {detail}")
    return result


def run_git_in_path(
    path: Path,
    args: list[str],
    check: bool = True,
    timeout_seconds: int | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=path,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as error:
        raise VersionToolError(
            f"`git {' '.join(args)}` in {path} timed out after {timeout_seconds}s."
        ) from error
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise VersionToolError(f"`git {' '.join(args)}` in {path} failed. {detail}")
    return result


def validate_semver(version: str) -> str:
    if not SEMVER_RE.fullmatch(version):
        raise VersionToolError(
            f"Expected a semantic version like 1.2.3 for custom bumps, but got {version!r}."
        )
    return version


def evidence_path(root: Path, requested_path: str | None = None) -> Path:
    path = DEFAULT_RELEASE_EVIDENCE_PATH if requested_path is None else Path(requested_path)
    return path if path.is_absolute() else root / path


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_local_marketplace_smoke(root: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="socket-codex-home.") as temp_dir:
        codex_home = Path(temp_dir)
        command_env = os.environ.copy()
        command_env["CODEX_HOME"] = str(codex_home)
        added = False
        try:
            add_result = run_command(
                root,
                ["codex", "plugin", "marketplace", "add", str(root)],
                env=command_env,
            )
            added = True
            config_path = codex_home / "config.toml"
            if not config_path.is_file():
                raise VersionToolError(
                    "Temporary CODEX_HOME marketplace smoke test did not create config.toml after adding Socket."
                )
            config = tomllib.loads(config_path.read_text(encoding="utf-8"))
            marketplaces = config.get("marketplaces")
            socket_marketplace = marketplaces.get("socket") if isinstance(marketplaces, dict) else None
            if not isinstance(socket_marketplace, dict):
                raise VersionToolError(
                    "Temporary CODEX_HOME marketplace smoke test did not register marketplaces.socket."
                )
            if socket_marketplace.get("source_type") != "local":
                raise VersionToolError(
                    "Temporary CODEX_HOME marketplace smoke test expected marketplaces.socket.source_type "
                    f"to be 'local', but found {socket_marketplace.get('source_type')!r}."
                )
            if socket_marketplace.get("source") != str(root):
                raise VersionToolError(
                    "Temporary CODEX_HOME marketplace smoke test registered an unexpected Socket source: "
                    f"{socket_marketplace.get('source')!r}."
                )
        finally:
            if added:
                remove_result = run_command(
                    root,
                    ["codex", "plugin", "marketplace", "remove", "socket"],
                    env=command_env,
                )
                config_path = codex_home / "config.toml"
                if config_path.is_file() and config_path.read_text(encoding="utf-8").strip():
                    raise VersionToolError(
                        "Temporary CODEX_HOME marketplace smoke test left marketplace configuration behind "
                        "after removing Socket."
                    )
        return {
            "status": "passed",
            "marketplace": "socket",
            "source_type": "local",
            "add_output": add_result.stdout.strip(),
            "remove_output": remove_result.stdout.strip(),
            "cleanup": "temporary CODEX_HOME removed with no marketplace configuration left behind",
        }


def query_open_dependabot_alerts(root: Path) -> tuple[dict[str, str | int], ...]:
    result = run_command(root, ["gh", "api", DEPENDABOT_ALERTS_ENDPOINT])
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise VersionToolError(
            "GitHub Dependabot alert query returned output that was not valid JSON."
        ) from error
    if not isinstance(payload, list):
        raise VersionToolError(
            "GitHub Dependabot alert query returned an unexpected response shape; expected a JSON array."
        )
    alerts: list[dict[str, str | int]] = []
    for raw_alert in payload:
        if not isinstance(raw_alert, dict):
            raise VersionToolError(
                "GitHub Dependabot alert query returned an alert entry that was not a JSON object."
            )
        dependency = raw_alert.get("dependency")
        advisory = raw_alert.get("security_advisory")
        package = dependency.get("package") if isinstance(dependency, dict) else None
        alerts.append(
            {
                "number": int(raw_alert.get("number", 0)),
                "severity": str(advisory.get("severity", "unknown"))
                if isinstance(advisory, dict)
                else "unknown",
                "package": str(package.get("name", "unknown"))
                if isinstance(package, dict)
                else "unknown",
                "manifest_path": str(dependency.get("manifest_path", "unknown"))
                if isinstance(dependency, dict)
                else "unknown",
            }
        )
    return tuple(sorted(alerts, key=lambda alert: int(alert["number"])))


def capture_release_evidence(root: Path, output_path: Path) -> ReleaseEvidence:
    ensure_clean_checkout(root)
    commit = run_git(root, ["rev-parse", "HEAD"]).stdout.strip()
    if not commit:
        raise VersionToolError("Release evidence capture could not determine the current Git commit.")
    evidence = ReleaseEvidence(
        commit=commit,
        captured_at=utc_timestamp(),
        marketplace_smoke=run_local_marketplace_smoke(root),
        dependabot_alerts=query_open_dependabot_alerts(root),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "commit": evidence.commit,
                "captured_at": evidence.captured_at,
                "marketplace_smoke": evidence.marketplace_smoke,
                "dependabot": {
                    "endpoint": DEPENDABOT_ALERTS_ENDPOINT,
                    "open_alert_count": len(evidence.dependabot_alerts),
                    "alerts": list(evidence.dependabot_alerts),
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return evidence


def render_evidence_summary(evidence: ReleaseEvidence) -> str:
    severity_counts: dict[str, int] = {}
    for alert in evidence.dependabot_alerts:
        severity = str(alert.get("severity", "unknown"))
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    if severity_counts:
        severity_summary = ", ".join(
            f"{severity}: {count}" for severity, count in sorted(severity_counts.items())
        )
    else:
        severity_summary = "none"
    return (
        f"- Passed the temporary `CODEX_HOME` Socket marketplace add/remove smoke test at "
        f"commit `{evidence.commit}`.\n"
        f"- Queried the GitHub Dependabot alerts API and found "
        f"{len(evidence.dependabot_alerts)} open alert(s); severity counts: {severity_summary}.\n"
        f"- Captured release evidence at `{evidence.captured_at}`.\n"
    )


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
            "Choose one explicit target version and run `scripts/release.sh prepare X.Y.Z`."
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
            "Release evidence and reviewed-main gates require a clean checkout. "
            "Commit or stash local changes before continuing."
        )


def ensure_main_matches_origin(root: Path) -> None:
    branch = run_git(root, ["branch", "--show-current"]).stdout.strip()
    if branch != "main":
        raise VersionToolError(f"Reviewed-main verification must run on local main, but the current branch is {branch!r}.")
    head = run_git(root, ["rev-parse", "HEAD"]).stdout.strip()
    origin_main = run_git(root, ["rev-parse", "origin/main"]).stdout.strip()
    if head != origin_main:
        raise VersionToolError(
            "Reviewed-main verification requires local main to match origin/main before tagging. "
            "Push or fast-forward main first."
        )


def ensure_versions_match_release(targets: list[VersionTarget], version: str) -> None:
    versions = read_versions(targets)
    if versions != [version]:
        joined_versions = ", ".join(versions)
        raise VersionToolError(
            f"Reviewed-main verification expected every maintained version surface to be {version}, "
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


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def configured_socket_marketplace() -> tuple[Path, str]:
    home = codex_home()
    config_path = home / "config.toml"
    if not config_path.is_file():
        raise VersionToolError(
            f"Codex config not found at {config_path}; cannot recover Socket marketplace cache."
        )
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    marketplaces = config.get("marketplaces")
    socket_marketplace = marketplaces.get("socket") if isinstance(marketplaces, dict) else None
    if not isinstance(socket_marketplace, dict):
        raise VersionToolError(
            "Codex config does not contain marketplaces.socket; cannot recover Socket marketplace cache."
        )
    if socket_marketplace.get("source_type") != "git":
        raise VersionToolError(
            "Codex marketplaces.socket is not a Git-backed marketplace; "
            f"found source_type={socket_marketplace.get('source_type')!r}."
        )
    source = socket_marketplace.get("source")
    if not isinstance(source, str) or not source:
        raise VersionToolError("Codex marketplaces.socket does not have a non-empty Git source.")
    return home / ".tmp" / "marketplaces" / "socket", source


def refresh_socket_marketplace_cache(root: Path) -> None:
    command = ["codex", "plugin", "marketplace", "upgrade", "socket"]
    result = run_command(root, command, check=False, timeout_seconds=45)
    if result.returncode == 0:
        if result.stdout.strip():
            print(result.stdout.strip())
        return

    detail = result.stderr.strip() or result.stdout.strip()
    known_timeout = "timed out after 30s" in detail and "fatal: early EOF" in detail
    if not known_timeout:
        raise VersionToolError(f"`{' '.join(command)}` failed. {detail}")

    print(
        "Codex marketplace upgrade hit the known 30s clone timeout; "
        "fast-forwarding the existing Socket marketplace cache instead."
    )
    cache_root, configured_source = configured_socket_marketplace()
    if not (cache_root / ".git").is_dir():
        raise VersionToolError(
            f"Socket marketplace cache is missing at {cache_root}; cannot fast-forward fallback."
        )
    remote_url = run_git_in_path(cache_root, ["remote", "get-url", "origin"]).stdout.strip()
    if remote_url != configured_source:
        raise VersionToolError(
            "Socket marketplace cache origin does not match the configured marketplace source: "
            f"{remote_url!r} != {configured_source!r}."
        )
    run_git_in_path(cache_root, ["fetch", "origin", "main"], timeout_seconds=45)
    run_git_in_path(cache_root, ["merge", "--ff-only", "origin/main"], timeout_seconds=45)
    head = run_git_in_path(cache_root, ["rev-parse", "HEAD"]).stdout.strip()
    print(f"Socket marketplace cache fast-forwarded to {head}.")
