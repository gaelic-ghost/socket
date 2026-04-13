#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
MAX_SKILL_NAME_LENGTH = 64


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_skill(skill_dir: Path) -> tuple[bool, str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as error:
        return False, f"Invalid YAML in frontmatter: {error}"

    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"

    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}
    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        allowed = ", ".join(sorted(allowed_properties))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter["name"]
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )

    description = frontmatter["description"]
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    return True, "Skill is valid!"


def load_frontmatter_name(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    _, frontmatter_text, _ = content.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    if not isinstance(frontmatter, dict):
        fail(f"Frontmatter in {skill_md} is not a YAML mapping")
    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        fail(f"Missing valid skill name in {skill_md}")
    return name.strip()


def validate_openai_yaml(skill_dir: Path, skill_name: str) -> None:
    openai_yaml_path = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml_path.exists():
        fail(f"Missing {openai_yaml_path}")

    payload = yaml.safe_load(openai_yaml_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        fail(f"{openai_yaml_path} is not a YAML mapping")

    interface = payload.get("interface")
    if not isinstance(interface, dict):
        fail(f"Missing interface section in {openai_yaml_path}")

    for key in ("display_name", "short_description", "default_prompt"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            fail(f"Missing non-empty interface.{key} in {openai_yaml_path}")

    short_description = interface["short_description"].strip()
    if not 25 <= len(short_description) <= 64:
        fail(
            f"interface.short_description in {openai_yaml_path} must be 25-64 characters; "
            f"got {len(short_description)}"
        )

    default_prompt = interface["default_prompt"]
    skill_token = f"${skill_name}"
    if skill_token not in default_prompt:
        fail(
            f"interface.default_prompt in {openai_yaml_path} must explicitly mention {skill_token}"
        )


def main() -> None:
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if (path / "SKILL.md").exists())
    if not skill_dirs:
        fail("No skills found to validate")

    for skill_dir in skill_dirs:
        valid, message = validate_skill(skill_dir)
        if not valid:
            fail(f"{skill_dir}: {message}")

        skill_name = load_frontmatter_name(skill_dir)
        validate_openai_yaml(skill_dir, skill_name)
        print(f"[OK] {skill_name}")

    print("Skill creator contract validation passed.")


if __name__ == "__main__":
    main()
