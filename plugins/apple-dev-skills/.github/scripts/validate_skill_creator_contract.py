#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
SKILL_CREATOR_DIR = Path("/Users/galew/.codex/skills/.system/skill-creator")
QUICK_VALIDATE_PATH = SKILL_CREATOR_DIR / "scripts/quick_validate.py"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_quick_validate():
    spec = importlib.util.spec_from_file_location("skill_creator_quick_validate", QUICK_VALIDATE_PATH)
    if spec is None or spec.loader is None:
        fail(f"Unable to load validator from {QUICK_VALIDATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    validator = load_quick_validate()
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if (path / "SKILL.md").exists())
    if not skill_dirs:
        fail("No skills found to validate")

    for skill_dir in skill_dirs:
        valid, message = validator.validate_skill(skill_dir)
        if not valid:
            fail(f"{skill_dir}: {message}")

        skill_name = load_frontmatter_name(skill_dir)
        validate_openai_yaml(skill_dir, skill_name)
        print(f"[OK] {skill_name}")

    print("Skill creator contract validation passed.")


if __name__ == "__main__":
    main()
