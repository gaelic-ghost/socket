#!/usr/bin/env python3
"""Validate shared skill and child-plugin metadata contracts across Socket."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, NoReturn

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_DESCRIPTION_LENGTH = 1024
OPTIONAL_INTERFACE_FIELDS = ("display_name", "short_description")


def fail(message: str) -> NoReturn:
    print(f"validate-socket-skill-metadata: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        fail(f"{path.relative_to(REPO_ROOT)} is not valid YAML: {error}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(REPO_ROOT)} must decode to a YAML mapping.")
    return value


def read_frontmatter(path: Path) -> dict[str, Any]:
    contents = path.read_text(encoding="utf-8")
    if not contents.startswith("---\n"):
        fail(f"{path.relative_to(REPO_ROOT)} must begin with YAML frontmatter.")
    raw_frontmatter, separator, _ = contents[4:].partition("\n---\n")
    if not separator:
        fail(f"{path.relative_to(REPO_ROOT)} has unterminated YAML frontmatter.")
    try:
        value = yaml.safe_load(raw_frontmatter)
    except yaml.YAMLError as error:
        fail(f"{path.relative_to(REPO_ROOT)} has invalid YAML frontmatter: {error}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(REPO_ROOT)} frontmatter must be a YAML mapping.")
    return value


def validate_skill(path: Path) -> None:
    metadata = read_frontmatter(path)
    expected_name = path.parent.name
    name = metadata.get("name")
    if name != expected_name:
        fail(
            f"{path.relative_to(REPO_ROOT)} must use its directory name "
            f"{expected_name!r}, but found {name!r}."
        )
    if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name):
        fail(f"{path.relative_to(REPO_ROOT)} must use a lowercase kebab-case skill name.")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        fail(f"{path.relative_to(REPO_ROOT)} must define a non-empty description.")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        fail(
            f"{path.relative_to(REPO_ROOT)} description exceeds "
            f"{MAX_DESCRIPTION_LENGTH} characters."
        )

    openai_metadata = path.parent / "agents" / "openai.yaml"
    if openai_metadata.exists():
        validate_openai_interface(openai_metadata, expected_name)


def validate_openai_interface(path: Path, skill_name: str) -> None:
    metadata = load_yaml(path)
    interface = metadata.get("interface")
    if not isinstance(interface, dict) or not interface:
        fail(f"{path.relative_to(REPO_ROOT)} must define a non-empty interface mapping.")

    default_prompt = interface.get("default_prompt")
    if not isinstance(default_prompt, str) or not default_prompt.strip():
        fail(f"{path.relative_to(REPO_ROOT)} must define a non-empty interface.default_prompt.")
    if f"${skill_name}" not in default_prompt:
        fail(
            f"{path.relative_to(REPO_ROOT)} interface.default_prompt must include "
            f"the ${skill_name} invocation token."
        )

    for field_name in OPTIONAL_INTERFACE_FIELDS:
        value = interface.get(field_name)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            fail(f"{path.relative_to(REPO_ROOT)} interface.{field_name} must be a non-empty string.")


def validate_child_guidance(plugin_root: Path) -> None:
    if not (plugin_root / "AGENTS.md").is_file():
        fail(f"{plugin_root.relative_to(REPO_ROOT)} is missing its child AGENTS.md guidance.")


def main() -> int:
    plugin_roots = sorted(
        path.parent.parent
        for path in REPO_ROOT.glob("plugins/*/.codex-plugin/plugin.json")
        if path.is_file()
    )
    for plugin_root in plugin_roots:
        validate_child_guidance(plugin_root)

    skill_paths = sorted(REPO_ROOT.glob("plugins/*/skills/*/SKILL.md"))
    if not skill_paths:
        fail("No authored plugin SKILL.md files were found.")
    for skill_path in skill_paths:
        validate_skill(skill_path)

    print(
        "Socket shared skill metadata validation passed "
        f"({len(plugin_roots)} plugins, {len(skill_paths)} skills)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
