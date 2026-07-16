#!/usr/bin/env python3
"""Validate Socket's Claude Code marketplace and Cowork compatibility inventory."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
CODEX_MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
INVENTORY_PATH = REPO_ROOT / "docs" / "maintainers" / "claude-compatibility.json"
EXCLUDED_CLAUDE_PLUGINS = {"agentdeck", "speak-swiftly", "spotify"}
PLUGIN_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_CODE_STATUSES = {"supported", "local_mcp", "remote_mcp", "not_supported"}
ALLOWED_COWORK_STATUSES = {"skills_only", "remote_mcp", "not_supported"}
MACHINE_LOCAL_PATH_RE = re.compile(r"(?:^|[\s'\"])~[/\\]|/Users/|(?:^|[\s'\"])\.\./")


class ValidationError(RuntimeError):
    """Raised when a checked-in Claude compatibility artifact is invalid."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} is not valid JSON: {error}") from error


def require_mapping(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{location} must be a JSON object.")
    return value


def require_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{location} must be a non-empty string.")
    return value


def codex_entries() -> dict[str, dict[str, Any]]:
    document = require_mapping(load_json(CODEX_MARKETPLACE_PATH), ".agents/plugins/marketplace.json")
    plugins = document.get("plugins")
    if not isinstance(plugins, list):
        raise ValidationError(".agents/plugins/marketplace.json must define a plugins array.")
    entries: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(plugins):
        entry = require_mapping(value, f"Codex plugin entry {index}")
        name = require_string(entry.get("name"), f"Codex plugin entry {index}.name")
        if name in entries:
            raise ValidationError(f"Codex marketplace repeats plugin {name!r}.")
        entries[name] = entry
    return entries


def source_path(entry: dict[str, Any], name: str) -> Path | None:
    source = entry.get("source")
    if isinstance(source, str):
        if not source.startswith("./"):
            raise ValidationError(f"Claude plugin {name!r} relative source must begin with './'.")
        return REPO_ROOT / source[2:]
    if not isinstance(source, dict):
        raise ValidationError(f"Claude plugin {name!r} source must be a string path or source object.")
    source_kind = require_string(source.get("source"), f"Claude plugin {name!r}.source.source")
    if source_kind == "url":
        require_string(source.get("url"), f"Claude plugin {name!r}.source.url")
        return None
    raise ValidationError(f"Claude plugin {name!r} uses unsupported source type {source_kind!r}.")


def load_mcp_servers(path: Path) -> dict[str, dict[str, Any]]:
    document = require_mapping(load_json(path), path.relative_to(REPO_ROOT).as_posix())
    servers = document.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} must define a non-empty mcpServers object for Claude.")
    typed_servers: dict[str, dict[str, Any]] = {}
    for name, value in servers.items():
        if not isinstance(name, str) or not isinstance(value, dict):
            raise ValidationError(f"{path.relative_to(REPO_ROOT)} must map string server names to objects.")
        transports = [field for field in ("command", "url") if field in value]
        if len(transports) != 1:
            raise ValidationError(
                f"{path.relative_to(REPO_ROOT)} server {name!r} must define exactly one transport: command or url."
            )
        if not isinstance(value[transports[0]], str) or not value[transports[0]].strip():
            raise ValidationError(f"{path.relative_to(REPO_ROOT)} server {name!r} has an empty transport value.")
        if MACHINE_LOCAL_PATH_RE.search(json.dumps(value)):
            raise ValidationError(f"{path.relative_to(REPO_ROOT)} server {name!r} contains a machine-local path.")
        if "${PLUGIN_ROOT}" in json.dumps(value):
            raise ValidationError(
                f"{path.relative_to(REPO_ROOT)} server {name!r} uses Codex-only ${{PLUGIN_ROOT}}; use ${{CLAUDE_PLUGIN_ROOT}}."
            )
        typed_servers[name] = value
    return typed_servers


def validate_marketplace(codex: dict[str, dict[str, Any]]) -> set[str]:
    document = require_mapping(load_json(CLAUDE_MARKETPLACE_PATH), ".claude-plugin/marketplace.json")
    if document.get("name") != "socket":
        raise ValidationError(".claude-plugin/marketplace.json must use the Socket marketplace name.")
    owner = require_mapping(document.get("owner"), ".claude-plugin/marketplace.json.owner")
    require_string(owner.get("name"), ".claude-plugin/marketplace.json.owner.name")
    require_string(document.get("description"), ".claude-plugin/marketplace.json.description")
    plugins = document.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise ValidationError(".claude-plugin/marketplace.json must define a non-empty plugins array.")

    names: set[str] = set()
    for index, value in enumerate(plugins):
        entry = require_mapping(value, f"Claude plugin entry {index}")
        name = require_string(entry.get("name"), f"Claude plugin entry {index}.name")
        if not PLUGIN_NAME_RE.fullmatch(name):
            raise ValidationError(f"Claude plugin {name!r} must be lowercase kebab-case.")
        if name in names:
            raise ValidationError(f"Claude marketplace repeats plugin {name!r}.")
        if name not in codex:
            raise ValidationError(f"Claude marketplace plugin {name!r} is absent from the Socket Codex marketplace.")
        if entry.get("strict") is not False:
            raise ValidationError(f"Claude plugin {name!r} must set strict to false so Socket keeps one authored payload.")
        require_string(entry.get("description"), f"Claude plugin {name!r}.description")
        root = source_path(entry, name)
        if root is not None:
            if not root.is_dir():
                raise ValidationError(f"Claude plugin {name!r} source directory is missing: {root.relative_to(REPO_ROOT)}.")
            if not (root / "skills").is_dir():
                raise ValidationError(f"Claude plugin {name!r} must expose a skills directory.")
            mcp_path = entry.get("mcpServers")
            if mcp_path is not None:
                relative_mcp_path = require_string(mcp_path, f"Claude plugin {name!r}.mcpServers")
                if not relative_mcp_path.startswith("./"):
                    raise ValidationError(f"Claude plugin {name!r}.mcpServers must be relative to its plugin root.")
                load_mcp_servers(root / relative_mcp_path[2:])
        names.add(name)

    expected = set(codex) - EXCLUDED_CLAUDE_PLUGINS
    if names != expected:
        missing = sorted(expected - names)
        extra = sorted(names - expected)
        details = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if extra:
            details.append(f"unexpected {', '.join(extra)}")
        raise ValidationError("Claude marketplace inventory differs from the approved Socket classification: " + "; ".join(details) + ".")
    return names


def validate_inventory(codex: dict[str, dict[str, Any]], claude_names: set[str]) -> None:
    document = require_mapping(load_json(INVENTORY_PATH), "docs/maintainers/claude-compatibility.json")
    if document.get("schemaVersion") != 1 or document.get("catalog") != "socket":
        raise ValidationError("Claude compatibility inventory must use schemaVersion 1 for the Socket catalog.")
    entries = require_mapping(document.get("entries"), "docs/maintainers/claude-compatibility.json.entries")
    if set(entries) != set(codex):
        raise ValidationError("Claude compatibility inventory must classify every Socket Codex marketplace plugin exactly once.")
    for name, value in entries.items():
        entry = require_mapping(value, f"Claude compatibility inventory entry {name!r}")
        code_status = entry.get("claudeCode")
        cowork_status = entry.get("cowork")
        if code_status not in ALLOWED_CODE_STATUSES:
            raise ValidationError(f"Claude compatibility inventory entry {name!r} has invalid claudeCode status {code_status!r}.")
        if cowork_status not in ALLOWED_COWORK_STATUSES:
            raise ValidationError(f"Claude compatibility inventory entry {name!r} has invalid cowork status {cowork_status!r}.")
        require_string(entry.get("note"), f"Claude compatibility inventory entry {name!r}.note")
        if name in EXCLUDED_CLAUDE_PLUGINS and code_status != "not_supported":
            raise ValidationError(f"Excluded Claude plugin {name!r} must be marked not_supported.")
        if name in claude_names and code_status == "not_supported":
            raise ValidationError(f"Installed Claude marketplace plugin {name!r} cannot be marked not_supported.")
        if code_status == "local_mcp" and cowork_status != "skills_only":
            raise ValidationError(f"Local-MCP plugin {name!r} must be Cowork skills_only.")


def main() -> int:
    codex = codex_entries()
    claude_names = validate_marketplace(codex)
    validate_inventory(codex, claude_names)
    print("Socket Claude Code and Cowork compatibility validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as error:
        print(f"validate-claude-compatibility: {error}")
        raise SystemExit(1)
