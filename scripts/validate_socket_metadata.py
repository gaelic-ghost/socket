#!/usr/bin/env python3
"""Validate root marketplace wiring for the socket superproject."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"


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


def validate_plugin_entry(entry: object, seen_names: set[str]) -> None:
    if not isinstance(entry, dict):
        fail("Each marketplace plugin entry must be a JSON object.")

    name = entry.get("name")
    if not isinstance(name, str) or not name:
        fail("Each marketplace plugin entry must define a non-empty string `name`.")
    if name in seen_names:
        fail(f"Marketplace plugin name `{name}` is duplicated.")
    seen_names.add(name)

    source = entry.get("source")
    if not isinstance(source, dict):
        fail(f"Marketplace plugin `{name}` is missing its `source` object.")
    source_kind = source.get("source")
    if source_kind != "local":
        fail(
            f"Marketplace plugin `{name}` must use a local source in this superproject, "
            f"but found `{source_kind}`."
        )
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


def main() -> None:
    print("Validating root marketplace presence...")
    marketplace = load_json(MARKETPLACE_PATH)
    if not isinstance(marketplace, dict):
        fail("Root marketplace must decode to a JSON object.")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("Root marketplace must contain a non-empty `plugins` array.")

    print("Validating packaged plugin paths...")
    seen_names: set[str] = set()
    for entry in plugins:
        validate_plugin_entry(entry, seen_names)

    print("Socket marketplace validation passed.")


if __name__ == "__main__":
    main()
