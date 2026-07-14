#!/usr/bin/env python3
"""Validate Socket's explicit Hermes Agent skill-tap compatibility surface."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

import export_hermes_skills


REPO_ROOT = Path(__file__).resolve().parent.parent
EXPORT_ROOT = REPO_ROOT / "skills"
GROUPINGS_PATH = REPO_ROOT / "skills.sh.json"
MCP_EXAMPLES_PATH = REPO_ROOT / "docs" / "maintainers" / "hermes-mcp-examples.yaml"
MCP_TRANSLATIONS_INDEX_PATH = REPO_ROOT / "docs" / "maintainers" / "hermes-mcp" / "index.yaml"
HERMES_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_FRIENDLY_DESCRIPTION_LENGTH = 240
MACHINE_LOCAL_PATH_RE = re.compile(r"(?:^|[\s'\"])~[/\\]|/Users/|(?:^|[\s'\"])\.\./")
ENV_PLACEHOLDER_RE = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}|\$([A-Z][A-Z0-9_]*)")
MCP_TRANSLATION_STATUSES = {"ready", "manual_setup_required", "not_supported"}


class ValidationError(RuntimeError):
    """Raised when the checked-in Hermes compatibility surface is invalid."""


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} is not valid YAML: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} must decode to a YAML mapping.")
    return value


def read_frontmatter(path: Path) -> dict[str, Any]:
    contents = path.read_text(encoding="utf-8")
    if not contents.startswith("---\n"):
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} must begin with YAML frontmatter.")
    _, separator, remaining = contents.partition("\n---\n")
    if not separator:
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} has unterminated YAML frontmatter.")
    try:
        value = yaml.safe_load(contents[4 : len(contents) - len(remaining) - len(separator)])
    except yaml.YAMLError as error:
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} has invalid YAML frontmatter: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} frontmatter must be a YAML mapping.")
    return value


def contains_machine_local_path(value: object) -> bool:
    if isinstance(value, str):
        return bool(MACHINE_LOCAL_PATH_RE.search(value))
    if isinstance(value, list):
        return any(contains_machine_local_path(item) for item in value)
    if isinstance(value, dict):
        return any(contains_machine_local_path(item) for item in value.values())
    return False


def validate_exported_skills() -> list[str]:
    warnings: list[str] = []
    try:
        if not export_hermes_skills.has_exact_export():
            raise ValidationError(
                "Root skills/ is stale or incomplete. Run `uv run scripts/export_hermes_skills.py` "
                "before validating Hermes compatibility."
            )
    except export_hermes_skills.ExportError as error:
        raise ValidationError(str(error)) from error

    for skill_name in export_hermes_skills.EXPORTED_SKILLS:
        skill_path = EXPORT_ROOT / skill_name / "SKILL.md"
        metadata = read_frontmatter(skill_path)
        name = metadata.get("name")
        description = metadata.get("description")
        if name != skill_name or not isinstance(name, str) or not HERMES_NAME_RE.fullmatch(name):
            raise ValidationError(
                f"{skill_path.relative_to(REPO_ROOT)} must use its lowercase hyphenated directory "
                f"name {skill_name!r}, but found {name!r}."
            )
        if not isinstance(description, str) or not description.strip():
            raise ValidationError(
                f"{skill_path.relative_to(REPO_ROOT)} must define a non-empty description."
            )
        if len(description) > MAX_FRIENDLY_DESCRIPTION_LENGTH:
            warnings.append(
                f"{skill_path.relative_to(REPO_ROOT)} description is {len(description)} characters; "
                f"Hermes discovery is clearer at {MAX_FRIENDLY_DESCRIPTION_LENGTH} or fewer."
            )
        if contains_machine_local_path(metadata):
            raise ValidationError(
                f"{skill_path.relative_to(REPO_ROOT)} frontmatter contains a machine-local or parent-relative path."
            )
    return warnings


def validate_groupings() -> None:
    try:
        document = json.loads(GROUPINGS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValidationError(f"skills.sh.json is not valid JSON: {error}") from error
    groupings = document.get("groupings") if isinstance(document, dict) else None
    if not isinstance(groupings, list) or not groupings:
        raise ValidationError("skills.sh.json must define a non-empty groupings array.")
    exported = set(export_hermes_skills.EXPORTED_SKILLS)
    grouped_names: set[str] = set()
    for grouping in groupings:
        if not isinstance(grouping, dict) or not isinstance(grouping.get("title"), str):
            raise ValidationError("Each skills.sh.json grouping must define a string title.")
        skills = grouping.get("skills")
        if not isinstance(skills, list) or not all(isinstance(skill, str) for skill in skills):
            raise ValidationError("Each skills.sh.json grouping must define a string skills array.")
        unknown = set(skills) - exported
        if unknown:
            raise ValidationError(
                "skills.sh.json refers to skills absent from the Hermes export: "
                f"{', '.join(sorted(unknown))}."
            )
        grouped_names.update(skills)
    missing = exported - grouped_names
    if missing:
        raise ValidationError(
            "skills.sh.json does not group every exported Hermes skill: "
            f"{', '.join(sorted(missing))}."
        )


def validate_mcp_examples() -> None:
    document = load_yaml_mapping(MCP_EXAMPLES_PATH)
    servers = document.get("mcp_servers")
    if not isinstance(servers, dict) or not servers:
        raise ValidationError("hermes-mcp-examples.yaml must define a non-empty mcp_servers mapping.")
    for name, config in servers.items():
        if not isinstance(name, str) or not isinstance(config, dict):
            raise ValidationError("Each Hermes MCP example must have a string name and mapping configuration.")
        transports = [field for field in ("command", "url") if field in config]
        if len(transports) != 1:
            raise ValidationError(
                f"Hermes MCP example {name!r} must define exactly one transport: command or url."
            )


def load_socket_mcp_servers(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} is not valid JSON: {error}") from error
    servers = document.get("mcpServers") if isinstance(document, dict) else None
    if servers is None:
        servers = document
    if not isinstance(servers, dict) or not servers:
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} must define a non-empty MCP server mapping.")
    if not all(isinstance(name, str) and isinstance(config, dict) for name, config in servers.items()):
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} must map string server names to configurations.")
    return servers


def placeholders_in(value: object) -> set[str]:
    if isinstance(value, str):
        return {match.group(1) or match.group(2) for match in ENV_PLACEHOLDER_RE.finditer(value)}
    if isinstance(value, list):
        return set().union(*(placeholders_in(item) for item in value)) if value else set()
    if isinstance(value, dict):
        return set().union(*(placeholders_in(item) for item in value.values())) if value else set()
    return set()


def validate_hermes_server(name: str, config: dict[str, Any], path: Path) -> set[str]:
    transports = [field for field in ("command", "url") if field in config]
    if len(transports) != 1:
        raise ValidationError(
            f"{path.relative_to(REPO_ROOT)} server {name!r} must define exactly one transport: command or url."
        )
    if "cwd" in config:
        raise ValidationError(
            f"{path.relative_to(REPO_ROOT)} server {name!r} uses unsupported Hermes field 'cwd'; use a documented portable launcher."
        )
    if not isinstance(config[transports[0]], str) or not config[transports[0]].strip():
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} server {name!r} has an empty {transports[0]!r}.")
    args = config.get("args")
    if args is not None and (not isinstance(args, list) or not all(isinstance(arg, str) for arg in args)):
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} server {name!r} args must be a string list.")
    env = config.get("env")
    if env is not None and (not isinstance(env, dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in env.items())):
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} server {name!r} env must be a string mapping.")
    if contains_machine_local_path(config):
        raise ValidationError(f"{path.relative_to(REPO_ROOT)} server {name!r} contains a machine-local path.")
    return placeholders_in(config)


def validate_mcp_translations() -> None:
    index = load_yaml_mapping(MCP_TRANSLATIONS_INDEX_PATH)
    translations = index.get("translations")
    if not isinstance(translations, dict) or not translations:
        raise ValidationError("hermes-mcp/index.yaml must define a non-empty translations mapping.")
    declared_sources = {path.relative_to(REPO_ROOT).as_posix() for path in REPO_ROOT.glob("plugins/**/.mcp.json")}
    indexed_sources: set[str] = set()
    for plugin_name, entry in translations.items():
        if not isinstance(plugin_name, str) or not isinstance(entry, dict):
            raise ValidationError("Each Hermes MCP translation index entry must be a plugin-name mapping.")
        source = entry.get("source")
        translation = entry.get("translation")
        status = entry.get("status")
        documented_environment = entry.get("required_environment")
        setup = entry.get("setup")
        if not isinstance(source, str) or source not in declared_sources:
            raise ValidationError(f"Hermes MCP translation {plugin_name!r} has no declared Socket .mcp.json source.")
        if not isinstance(translation, str) or not translation.startswith("docs/maintainers/hermes-mcp/"):
            raise ValidationError(f"Hermes MCP translation {plugin_name!r} must use a checked-in hermes-mcp translation path.")
        if not isinstance(status, str) or status not in MCP_TRANSLATION_STATUSES:
            raise ValidationError(f"Hermes MCP translation {plugin_name!r} has unsupported status {status!r}.")
        if not isinstance(documented_environment, list) or not all(isinstance(item, str) for item in documented_environment):
            raise ValidationError(f"Hermes MCP translation {plugin_name!r} must list documented required_environment names.")
        if not isinstance(setup, str) or not setup.strip():
            raise ValidationError(f"Hermes MCP translation {plugin_name!r} must include a setup note.")
        translation_path = REPO_ROOT / translation
        document = load_yaml_mapping(translation_path)
        servers = document.get("mcp_servers")
        if not isinstance(servers, dict) or not servers:
            raise ValidationError(f"{translation} must define a non-empty mcp_servers mapping.")
        source_servers = load_socket_mcp_servers(REPO_ROOT / source)
        if set(servers) != set(source_servers):
            raise ValidationError(f"{translation} server names must exactly match {source}.")
        placeholders: set[str] = set()
        for name, config in servers.items():
            if not isinstance(name, str) or not isinstance(config, dict):
                raise ValidationError(f"{translation} must map string server names to mappings.")
            placeholders.update(validate_hermes_server(name, config, translation_path))
        undocumented = placeholders - set(documented_environment)
        if undocumented:
            raise ValidationError(f"{translation} has undocumented environment placeholders: {', '.join(sorted(undocumented))}.")
        indexed_sources.add(source)
    missing = declared_sources - indexed_sources
    extra = indexed_sources - declared_sources
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing translations for {', '.join(sorted(missing))}")
        if extra:
            details.append(f"unknown translation sources {', '.join(sorted(extra))}")
        raise ValidationError("Hermes MCP translation inventory is incomplete: " + "; ".join(details) + ".")


def main() -> int:
    warnings = validate_exported_skills()
    validate_groupings()
    validate_mcp_examples()
    validate_mcp_translations()
    for warning in warnings:
        print(f"Warning: {warning}")
    print("Socket Hermes compatibility validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as error:
        print(f"validate-hermes-compatibility: {error}")
        raise SystemExit(1)
