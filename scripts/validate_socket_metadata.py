#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Validate root marketplace wiring for the socket superproject."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
GIT_SOURCE_KINDS = {"url", "git-subdir"}
INSTALLATION_POLICIES = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
AUTHENTICATION_POLICIES = {"ON_INSTALL", "ON_FIRST_USE"}


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Required JSON file is missing: {path}")
    except json.JSONDecodeError as exc:
        fail(f"JSON file is invalid at {path}:{exc.lineno}:{exc.colno}: {exc.msg}")


def validate_optional_git_selector(
    *,
    plugin_name: str,
    source: dict[str, object],
) -> None:
    ref = source.get("ref")
    sha = source.get("sha")
    if ref is not None and (not isinstance(ref, str) or not ref):
        fail(f"Marketplace plugin `{plugin_name}` has an invalid Git source ref: {ref}")
    if sha is not None and (not isinstance(sha, str) or not sha):
        fail(f"Marketplace plugin `{plugin_name}` has an invalid Git source sha: {sha}")
    if ref is not None and sha is not None:
        fail(f"Marketplace plugin `{plugin_name}` must not set both Git source ref and sha.")


def validate_git_source(
    *,
    plugin_name: str,
    source: dict[str, object],
    source_kind: str,
) -> None:
    url = source.get("url")
    if not isinstance(url, str) or not url:
        fail(f"Marketplace plugin `{plugin_name}` must define a non-empty Git source url.")

    validate_optional_git_selector(plugin_name=plugin_name, source=source)

    if source_kind == "url":
        if "path" in source:
            fail(
                f"Marketplace plugin `{plugin_name}` uses a root Git source and must not "
                "also define source.path. Use `git-subdir` for repository subdirectories."
            )
        return

    path = source.get("path")
    if not isinstance(path, str) or not path.startswith("./"):
        fail(
            f"Marketplace plugin `{plugin_name}` uses `git-subdir` and must define a "
            f"`./...` source.path, but found `{path}`."
        )


def validate_manifest_path(
    *,
    plugin_name: str,
    plugin_root: Path,
    field_name: str,
    field_value: object,
    expected_kind: str,
) -> Path:
    if not isinstance(field_value, str) or not field_value.startswith("./"):
        fail(
            f"Packaged plugin manifest for `{plugin_name}` must use a root-relative "
            f"`./...` `{field_name}` path, but found `{field_value}`."
        )

    component_path = (plugin_root / field_value).resolve()
    try:
        component_path.relative_to(plugin_root)
    except ValueError:
        fail(
            f"Packaged plugin manifest for `{plugin_name}` points `{field_name}` outside "
            f"its plugin root: {field_value}"
        )

    if expected_kind == "directory" and not component_path.is_dir():
        fail(
            f"Packaged plugin manifest for `{plugin_name}` points `{field_name}` at a "
            f"missing directory: {component_path.relative_to(REPO_ROOT)}."
        )
    if expected_kind == "file" and not component_path.is_file():
        fail(
            f"Packaged plugin manifest for `{plugin_name}` points `{field_name}` at a "
            f"missing file: {component_path.relative_to(REPO_ROOT)}."
        )

    return component_path


def validate_policy(*, plugin_name: str, entry: dict[str, object]) -> str:
    policy = entry.get("policy")
    if not isinstance(policy, dict):
        fail(f"Marketplace plugin `{plugin_name}` is missing its `policy` object.")

    installation = policy.get("installation")
    if installation not in INSTALLATION_POLICIES:
        allowed = ", ".join(sorted(INSTALLATION_POLICIES))
        fail(
            f"Marketplace plugin `{plugin_name}` has invalid policy.installation "
            f"`{installation}`. Expected one of: {allowed}."
        )

    authentication = policy.get("authentication")
    if authentication not in AUTHENTICATION_POLICIES:
        allowed = ", ".join(sorted(AUTHENTICATION_POLICIES))
        fail(
            f"Marketplace plugin `{plugin_name}` has invalid policy.authentication "
            f"`{authentication}`. Expected one of: {allowed}."
        )

    category = entry.get("category")
    if not isinstance(category, str) or not category:
        fail(f"Marketplace plugin `{plugin_name}` must define a non-empty category.")

    return installation


def manifest_exports_content(*, plugin_root: Path, plugin_manifest: dict[str, object]) -> bool:
    skills_path = plugin_manifest.get("skills")
    if isinstance(skills_path, str):
        skills_root = (plugin_root / skills_path).resolve()
        try:
            skills_root.relative_to(plugin_root)
        except ValueError:
            return False
        if skills_root.is_dir() and any(skills_root.glob("*/SKILL.md")):
            return True

    for field_name in ("mcpServers", "hooks", "apps"):
        if plugin_manifest.get(field_name) is not None:
            return True

    return False


def validate_local_plugin_entry(
    *,
    name: str,
    source: dict[str, object],
    installation_policy: str,
) -> None:
    relative_path = source.get("path")
    if not isinstance(relative_path, str) or not relative_path.startswith("./"):
        fail(
            f"Marketplace plugin `{name}` must use a repo-relative `./...` source.path, "
            f"but found `{relative_path}`."
        )

    plugin_root = (REPO_ROOT / relative_path).resolve()
    try:
        plugin_root.relative_to(REPO_ROOT.resolve())
    except ValueError:
        fail(
            f"Marketplace plugin `{name}` points outside the repository root: {relative_path}"
        )

    if not plugin_root.is_dir():
        fail(
            f"Marketplace plugin `{name}` points at a missing packaged plugin directory: "
            f"{relative_path}"
        )

    plugin_manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    if not plugin_manifest_path.is_file():
        fail(
            f"Marketplace plugin `{name}` is missing its packaged manifest at "
            f"{plugin_manifest_path.relative_to(REPO_ROOT)}."
        )

    plugin_manifest = load_json(plugin_manifest_path)
    if not isinstance(plugin_manifest, dict):
        fail(
            f"Packaged plugin manifest for `{name}` must decode to a JSON object: "
            f"{plugin_manifest_path.relative_to(REPO_ROOT)}"
        )

    manifest_name = plugin_manifest.get("name")
    if manifest_name != name:
        fail(
            f"Marketplace plugin `{name}` points at a packaged manifest that declares "
            f"`{manifest_name}` instead."
        )

    if (
        installation_policy != "NOT_AVAILABLE"
        and not manifest_exports_content(plugin_root=plugin_root, plugin_manifest=plugin_manifest)
    ):
        fail(
            f"Marketplace plugin `{name}` is installable but does not export skills, "
            "MCP servers, hooks, or apps. Empty placeholder plugins must use "
            "policy.installation `NOT_AVAILABLE` until they ship content."
        )

    skills_dir = plugin_root / "skills"
    skills_path = plugin_manifest.get("skills")
    if skills_dir.is_dir():
        if skills_path is None:
            fail(
                f"Packaged plugin manifest for `{name}` must expose its root skills "
                f"directory with `\"skills\": \"./skills/\"`."
            )
        if skills_path != "./skills/":
            fail(
                f"Packaged plugin manifest for `{name}` must expose its root skills "
                f"directory with `\"skills\": \"./skills/\"`, but found `{skills_path}`."
            )
        validate_manifest_path(
            plugin_name=name,
            plugin_root=plugin_root,
            field_name="skills",
            field_value=skills_path,
            expected_kind="directory",
        )
    elif skills_path is not None:
        validate_manifest_path(
            plugin_name=name,
            plugin_root=plugin_root,
            field_name="skills",
            field_value=skills_path,
            expected_kind="directory",
        )

    mcp_servers_path = plugin_manifest.get("mcpServers")
    if mcp_servers_path is not None:
        mcp_config_path = validate_manifest_path(
            plugin_name=name,
            plugin_root=plugin_root,
            field_name="mcpServers",
            field_value=mcp_servers_path,
            expected_kind="file",
        )
        mcp_config = load_json(mcp_config_path)
        if not isinstance(mcp_config, dict):
            fail(
                f"MCP server configuration for `{name}` must decode to a JSON object: "
                f"{mcp_config_path.relative_to(REPO_ROOT)}"
            )


def validate_plugin_entry(entry: object, seen_names: set[str]) -> None:
    if not isinstance(entry, dict):
        fail("Each marketplace plugin entry must be a JSON object.")

    name = entry.get("name")
    if not isinstance(name, str) or not name:
        fail("Each marketplace plugin entry must define a non-empty string `name`.")
    if name in seen_names:
        fail(f"Marketplace plugin name `{name}` is duplicated.")
    seen_names.add(name)

    installation_policy = validate_policy(plugin_name=name, entry=entry)

    source = entry.get("source")
    if not isinstance(source, dict):
        fail(f"Marketplace plugin `{name}` is missing its `source` object.")
    source_kind = source.get("source")
    if source_kind == "local":
        validate_local_plugin_entry(
            name=name,
            source=source,
            installation_policy=installation_policy,
        )
        return
    if source_kind in GIT_SOURCE_KINDS:
        validate_git_source(plugin_name=name, source=source, source_kind=source_kind)
        return

    fail(
        f"Marketplace plugin `{name}` must use a supported source kind "
        f"(`local`, `url`, or `git-subdir`), but found `{source_kind}`."
    )


def main() -> None:
    print("Validating root marketplace presence...")
    marketplace = load_json(MARKETPLACE_PATH)
    if not isinstance(marketplace, dict):
        fail("Root marketplace must decode to a JSON object.")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("Root marketplace must contain a non-empty `plugins` array.")

    print("Validating marketplace entries...")
    seen_names: set[str] = set()
    for entry in plugins:
        validate_plugin_entry(entry, seen_names)

    print("Socket marketplace validation passed.")


if __name__ == "__main__":
    main()
