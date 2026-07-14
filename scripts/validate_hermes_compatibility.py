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
HERMES_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_FRIENDLY_DESCRIPTION_LENGTH = 240
MACHINE_LOCAL_PATH_RE = re.compile(r"(?:^|[\s'\"])~[/\\]|/Users/|(?:^|[\s'\"])\.\./")


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


def main() -> int:
    warnings = validate_exported_skills()
    validate_groupings()
    validate_mcp_examples()
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
