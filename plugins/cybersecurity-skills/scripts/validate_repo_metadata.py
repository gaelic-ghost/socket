#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pyyaml>=6.0.2,<7",
# ]
# ///
"""Validate the Cybersecurity Skills authored and packaged surfaces."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
PLUGIN_MANIFEST = REPO_ROOT / ".codex-plugin" / "plugin.json"
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"\[[^]]*]\(([^)]+)\)")
MACHINE_LOCAL_MARKERS = ("/Users/", "~/", "../")


@dataclass(frozen=True)
class Finding:
    """Describe one actionable metadata validation failure."""

    path: str
    message: str


def parse_frontmatter(path: Path) -> tuple[dict[str, object] | None, str, list[Finding]]:
    """Split and validate one skill entry point's YAML frontmatter."""

    text = path.read_text(encoding="utf-8")
    relative_path = str(path.relative_to(REPO_ROOT))
    if not text.startswith("---\n"):
        return None, text, [Finding(relative_path, "must begin with YAML frontmatter")]
    try:
        raw_frontmatter, body = text[4:].split("\n---\n", 1)
    except ValueError:
        return None, text, [Finding(relative_path, "has unterminated YAML frontmatter")]
    try:
        parsed = yaml.safe_load(raw_frontmatter)
    except yaml.YAMLError as error:
        return None, body, [Finding(relative_path, f"has invalid YAML frontmatter: {error}")]
    if not isinstance(parsed, dict):
        return None, body, [Finding(relative_path, "frontmatter must be a YAML mapping")]
    return parsed, body, []


def validate_links(path: Path, body: str) -> list[Finding]:
    """Check that relative Markdown links remain inside the plugin and resolve."""

    findings: list[Finding] = []
    for target in MARKDOWN_LINK.findall(body):
        if target.startswith(("https://", "http://", "#", "mailto:")):
            continue
        relative_target = target.split("#", 1)[0]
        if not relative_target:
            continue
        resolved = (path.parent / relative_target).resolve()
        try:
            resolved.relative_to(REPO_ROOT.resolve())
        except ValueError:
            findings.append(Finding(str(path.relative_to(REPO_ROOT)), f"links outside the plugin root: {target}"))
            continue
        if not resolved.exists():
            findings.append(Finding(str(path.relative_to(REPO_ROOT)), f"links to a missing local resource: {target}"))
    return findings


def validate_openai_yaml(skill_dir: Path) -> list[Finding]:
    """Validate one skill's OpenAI interface metadata."""

    path = skill_dir / "agents" / "openai.yaml"
    relative_path = str(path.relative_to(REPO_ROOT))
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [Finding(str(skill_dir.relative_to(REPO_ROOT)), "is missing agents/openai.yaml")]
    except yaml.YAMLError as error:
        return [Finding(relative_path, f"contains invalid YAML: {error}")]
    if not isinstance(data, dict) or not isinstance(data.get("interface"), dict):
        return [Finding(relative_path, "must define an interface mapping")]
    findings: list[Finding] = []
    interface = data["interface"]
    for key in ("display_name", "short_description", "default_prompt"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            findings.append(Finding(relative_path, f"interface.{key} must be a non-empty string"))
    short_description = interface.get("short_description")
    if isinstance(short_description, str) and not 25 <= len(short_description) <= 64:
        findings.append(Finding(relative_path, "interface.short_description must be 25 to 64 characters"))
    default_prompt = interface.get("default_prompt")
    if isinstance(default_prompt, str) and f"${skill_dir.name}" not in default_prompt:
        findings.append(Finding(relative_path, f"interface.default_prompt must mention `${skill_dir.name}` explicitly"))
    return findings


def validate_skill(skill_dir: Path) -> list[Finding]:
    """Validate one authored skill folder."""

    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return [Finding(str(skill_dir.relative_to(REPO_ROOT)), "is missing its required SKILL.md")]
    frontmatter, body, findings = parse_frontmatter(path)
    if frontmatter is not None:
        unexpected = sorted(set(frontmatter) - {"name", "description"})
        if unexpected:
            findings.append(Finding(str(path.relative_to(REPO_ROOT)), f"frontmatter contains unsupported fields: {', '.join(unexpected)}"))
        name = frontmatter.get("name")
        if name != skill_dir.name:
            findings.append(Finding(str(path.relative_to(REPO_ROOT)), f"frontmatter name must match directory `{skill_dir.name}`"))
        if not isinstance(name, str) or not SKILL_NAME.fullmatch(name):
            findings.append(Finding(str(path.relative_to(REPO_ROOT)), "frontmatter name violates skill naming rules"))
        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            findings.append(Finding(str(path.relative_to(REPO_ROOT)), "frontmatter description must be non-empty"))
        elif len(description) > 1024:
            findings.append(Finding(str(path.relative_to(REPO_ROOT)), "frontmatter description exceeds 1024 characters"))
    if "TODO" in body:
        findings.append(Finding(str(path.relative_to(REPO_ROOT)), "contains unresolved TODO scaffold text"))
    for marker in MACHINE_LOCAL_MARKERS:
        if marker in body:
            findings.append(Finding(str(path.relative_to(REPO_ROOT)), f"contains prohibited path marker `{marker}`"))
    findings.extend(validate_links(path, body))
    findings.extend(validate_openai_yaml(skill_dir))
    return findings


def validate_manifest() -> list[Finding]:
    """Validate the plugin identity and authored skill export."""

    try:
        data = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [Finding(str(PLUGIN_MANIFEST.relative_to(REPO_ROOT)), "is missing")]
    except json.JSONDecodeError as error:
        return [Finding(str(PLUGIN_MANIFEST.relative_to(REPO_ROOT)), f"contains invalid JSON: {error}")]
    findings: list[Finding] = []
    if not isinstance(data, dict):
        return [Finding(str(PLUGIN_MANIFEST.relative_to(REPO_ROOT)), "must be a JSON object")]
    if data.get("name") != "cybersecurity-skills":
        findings.append(Finding(str(PLUGIN_MANIFEST.relative_to(REPO_ROOT)), "must use plugin name `cybersecurity-skills`"))
    if data.get("skills") != "./skills/":
        findings.append(Finding(str(PLUGIN_MANIFEST.relative_to(REPO_ROOT)), "must export the authored ./skills/ directory"))
    return findings


def main() -> int:
    """Run plugin-local validation and return a shell-compatible status."""

    findings = validate_manifest()
    skill_dirs = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir()) if SKILLS_ROOT.is_dir() else []
    if not skill_dirs:
        findings.append(Finding("skills", "must contain at least one exported skill directory"))
    for skill_dir in skill_dirs:
        findings.extend(validate_skill(skill_dir))
    if findings:
        print("Cybersecurity Skills validation failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding.path}: {finding.message}", file=sys.stderr)
        return 1
    print(f"Cybersecurity Skills validation passed for {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
