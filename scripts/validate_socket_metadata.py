#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Validate root marketplace wiring for the socket superproject."""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path
from typing import NoReturn, cast


REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
GIT_SOURCE_KINDS = {"url", "git-subdir"}
INSTALLATION_POLICIES = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
AUTHENTICATION_POLICIES = {"ON_INSTALL", "ON_FIRST_USE"}
MARKETPLACE_INTERFACE_ASSET_FIELDS = {"banner"}
PLUGIN_INTERFACE_ASSET_FIELDS = {"composerIcon", "logo"}
PLUGIN_INTERFACE_ASSET_LIST_FIELDS = {"screenshots"}
CUSTOM_AGENT_REQUIRED_FIELDS = {"name", "description", "developer_instructions"}
CUSTOM_AGENT_REVIEW_TERMS = ("draft", "review")
REVIEW_PACKET_AGENT_NAME_PARTS = ("steward", "auditor", "triager")
REVIEW_PACKET_AGENT_NAMES = {"skills-repo-guidance-sync"}
REVIEW_PACKET_AGENT_REPORT_TERMS = ("review packet", "proposed patch set", "validation handoff")
MCP_SERVER_TRANSPORT_FIELDS = ("command", "url")


def fail(message: str) -> NoReturn:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Required JSON file is missing: {path}")
    except json.JSONDecodeError as exc:
        fail(f"JSON file is invalid at {path}:{exc.lineno}:{exc.colno}: {exc.msg}")


def load_toml(path: Path) -> dict[str, object]:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Required TOML file is missing: {path}")
    except tomllib.TOMLDecodeError as exc:
        fail(f"TOML file is invalid at {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"TOML file must decode to an object: {path}")
    return data


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


def validate_marketplace_interface(marketplace: dict[str, object]) -> None:
    interface = marketplace.get("interface")
    if not isinstance(interface, dict):
        fail("Root marketplace must define an `interface` object.")

    display_name = interface.get("displayName")
    if not isinstance(display_name, str) or not display_name:
        fail("Root marketplace interface must define a non-empty `displayName`.")

    for field_name in MARKETPLACE_INTERFACE_ASSET_FIELDS:
        field_value = interface.get(field_name)
        if field_value is None:
            continue
        if not isinstance(field_value, str) or not field_value.startswith("./"):
            fail(
                f"Root marketplace interface `{field_name}` must use a repo-relative "
                f"`./...` path, but found `{field_value}`."
            )

        asset_path = (REPO_ROOT / field_value).resolve()
        try:
            asset_path.relative_to(REPO_ROOT.resolve())
        except ValueError:
            fail(
                f"Root marketplace interface `{field_name}` points outside the "
                f"repository root: {field_value}"
            )
        if not asset_path.is_file():
            fail(
                f"Root marketplace interface `{field_name}` points at a missing file: "
                f"{field_value}"
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


def validate_mcp_server_entry(*, plugin_name: str, server_name: str, server_config: object) -> None:
    if not isinstance(server_config, dict):
        fail(
            f"MCP server `{server_name}` for `{plugin_name}` must be a JSON object, "
            f"but found `{server_config}`."
        )

    transport_fields = [field for field in MCP_SERVER_TRANSPORT_FIELDS if field in server_config]
    if len(transport_fields) != 1:
        allowed = " or ".join(MCP_SERVER_TRANSPORT_FIELDS)
        fail(
            f"MCP server `{server_name}` for `{plugin_name}` must define exactly one "
            f"transport field, {allowed}."
        )

    for field_name in transport_fields:
        field_value = server_config[field_name]
        if not isinstance(field_value, str) or not field_value:
            fail(
                f"MCP server `{server_name}` for `{plugin_name}` has an invalid "
                f"`{field_name}` value: {field_value}."
            )


def validate_mcp_config(*, plugin_name: str, mcp_config_path: Path, mcp_config: object) -> None:
    if not isinstance(mcp_config, dict):
        fail(
            f"MCP server configuration for `{plugin_name}` must decode to a JSON object: "
            f"{mcp_config_path.relative_to(REPO_ROOT)}"
        )

    if "mcpServers" in mcp_config:
        servers = mcp_config["mcpServers"]
        if not isinstance(servers, dict) or not servers:
            fail(
                f"MCP server configuration for `{plugin_name}` must define a non-empty "
                f"`mcpServers` object: {mcp_config_path.relative_to(REPO_ROOT)}"
            )
    else:
        servers = mcp_config
        if not servers:
            fail(
                f"MCP server configuration for `{plugin_name}` must define at least one "
                f"server: {mcp_config_path.relative_to(REPO_ROOT)}"
            )

    for server_name, server_config in servers.items():
        if not isinstance(server_name, str) or not server_name:
            fail(
                f"MCP server configuration for `{plugin_name}` has an invalid server "
                f"name: {server_name}."
            )
        validate_mcp_server_entry(
            plugin_name=plugin_name,
            server_name=server_name,
            server_config=server_config,
        )


def validate_plugin_interface_assets(
    *,
    plugin_name: str,
    plugin_root: Path,
    plugin_manifest: dict[str, object],
) -> None:
    interface = plugin_manifest.get("interface")
    if interface is None:
        return
    if not isinstance(interface, dict):
        fail(f"Packaged plugin manifest for `{plugin_name}` has an invalid `interface` object.")

    for field_name in PLUGIN_INTERFACE_ASSET_FIELDS:
        field_value = interface.get(field_name)
        if field_value is None:
            continue
        validate_manifest_path(
            plugin_name=plugin_name,
            plugin_root=plugin_root,
            field_name=f"interface.{field_name}",
            field_value=field_value,
            expected_kind="file",
        )

    for field_name in PLUGIN_INTERFACE_ASSET_LIST_FIELDS:
        field_value = interface.get(field_name)
        if field_value is None:
            continue
        if not isinstance(field_value, list):
            fail(
                f"Packaged plugin manifest for `{plugin_name}` must define "
                f"`interface.{field_name}` as a list of repo-relative paths."
            )
        for index, item in enumerate(field_value):
            validate_manifest_path(
                plugin_name=plugin_name,
                plugin_root=plugin_root,
                field_name=f"interface.{field_name}[{index}]",
                field_value=item,
                expected_kind="file",
            )


def validate_custom_agent_file(*, plugin_name: str, agent_path: Path) -> str:
    agent = load_toml(agent_path)
    relative_path = agent_path.relative_to(REPO_ROOT)

    for field_name in sorted(CUSTOM_AGENT_REQUIRED_FIELDS):
        field_value = agent.get(field_name)
        if not isinstance(field_value, str) or not field_value.strip():
            fail(
                f"Custom agent `{relative_path}` for `{plugin_name}` must define a "
                f"non-empty `{field_name}` string."
            )

    agent_name = cast(str, agent["name"])
    if agent_path.stem != agent_name:
        fail(
            f"Custom agent `{relative_path}` for `{plugin_name}` declares name "
            f"`{agent_name}` but the file stem is `{agent_path.stem}`."
        )

    sandbox_mode = agent.get("sandbox_mode")
    if sandbox_mode != "read-only":
        fail(
            f"Custom agent `{relative_path}` for `{plugin_name}` must use "
            '`sandbox_mode = "read-only"` until write-capable steward workflows '
            "have an explicit apply contract."
        )

    model = agent.get("model")
    if model is not None and (not isinstance(model, str) or not model.strip()):
        fail(
            f"Custom agent `{relative_path}` for `{plugin_name}` must define "
            "`model` as a non-empty string when present."
        )

    instructions = cast(str, agent["developer_instructions"])
    lowered_instructions = instructions.lower()
    for term in CUSTOM_AGENT_REVIEW_TERMS:
        if term not in lowered_instructions:
            fail(
                f"Custom agent `{relative_path}` for `{plugin_name}` must mention "
                f"`{term}` in developer_instructions so draft-patch output stays "
                "review-oriented."
            )

    if agent_name in REVIEW_PACKET_AGENT_NAMES or any(
        name_part in agent_name for name_part in REVIEW_PACKET_AGENT_NAME_PARTS
    ):
        for term in REVIEW_PACKET_AGENT_REPORT_TERMS:
            if term not in lowered_instructions:
                fail(
                    f"Custom agent `{relative_path}` for `{plugin_name}` must "
                    f"mention `{term}` in developer_instructions so draft-patch output "
                    "uses the shared review-packet contract."
                )

    nickname_candidates = agent.get("nickname_candidates")
    if nickname_candidates is not None:
        if not isinstance(nickname_candidates, list) or not nickname_candidates:
            fail(
                f"Custom agent `{relative_path}` for `{plugin_name}` must define "
                "`nickname_candidates` as a non-empty list when present."
            )
        for index, nickname in enumerate(nickname_candidates):
            if not isinstance(nickname, str) or not nickname.strip():
                fail(
                    f"Custom agent `{relative_path}` for `{plugin_name}` has an invalid "
                    f"`nickname_candidates[{index}]` value."
                )

    return agent_name


def validate_custom_agents(*, plugin_name: str, plugin_root: Path) -> None:
    agents_root = plugin_root / ".codex" / "agents"
    if not agents_root.exists():
        return
    if not agents_root.is_dir():
        fail(
            f"Custom agent path for `{plugin_name}` must be a directory: "
            f"{agents_root.relative_to(REPO_ROOT)}"
        )

    agent_paths = sorted(agents_root.glob("*.toml"))
    if not agent_paths:
        fail(
            f"Custom agent directory for `{plugin_name}` has no TOML files: "
            f"{agents_root.relative_to(REPO_ROOT)}"
        )

    seen_names: set[str] = set()
    for agent_path in agent_paths:
        agent_name = validate_custom_agent_file(plugin_name=plugin_name, agent_path=agent_path)
        if agent_name in seen_names:
            fail(f"Custom agent name `{agent_name}` is duplicated for `{plugin_name}`.")
        seen_names.add(agent_name)


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

    validate_plugin_interface_assets(
        plugin_name=name,
        plugin_root=plugin_root,
        plugin_manifest=plugin_manifest,
    )
    validate_custom_agents(plugin_name=name, plugin_root=plugin_root)

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
        validate_mcp_config(plugin_name=name, mcp_config_path=mcp_config_path, mcp_config=mcp_config)


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

    validate_marketplace_interface(marketplace)

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
