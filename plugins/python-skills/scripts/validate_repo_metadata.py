#!/usr/bin/env -S uv run

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

README_REQUIRED_HEADINGS = [
    "# python-skills",
    "## Table of Contents",
    "## Overview",
    "## Setup",
    "## Usage",
    "## Development",
    "## Verification",
    "## Release Notes",
    "## Active Skills",
    "## Packaging",
    "## Repository Layout",
    "## License",
]

ROADMAP_REQUIRED_HEADINGS = [
    "# Project Roadmap",
    "## Table of Contents",
    "## Vision",
    "## Product Principles",
    "## Milestone Progress",
    "## Backlog Candidates",
    "## History",
]

PATH_REFERENCE_RE = re.compile(
    r"(?:\[[^\]]+\]\()?((?:scripts|references|assets|agents)/[A-Za-z0-9._/\-]+)(?:\))?"
)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
REQUIRED_FRONTMATTER_FIELDS = [
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
]
REQUIRED_METADATA_KEYS = ["owner", "repo", "category"]
REQUIRED_INTERFACE_KEYS = ["display_name", "short_description", "brand_color", "default_prompt"]
PLUGIN_REQUIRED_FIELDS = ["name", "version", "description", "skills", "interface"]
PLUGIN_INTERFACE_REQUIRED_FIELDS = [
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "websiteURL",
    "defaultPrompt",
    "brandColor",
]
PLUGIN_DIR_NAME = "python-skills"


@dataclass
class Finding:
    path: str
    message: str


def parse_frontmatter(text: str, path: Path) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"missing frontmatter in {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"invalid frontmatter in {path}")
    return data


def load_yaml(path: Path) -> dict[str, object]:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"invalid YAML in {path}")
    return data


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"invalid JSON object in {path}")
    return data


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_frontmatter(path: Path, frontmatter: dict[str, object], expected_name: str) -> list[Finding]:
    findings: list[Finding] = []
    rel_path = str(path)

    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in frontmatter:
            findings.append(Finding(rel_path, f"missing frontmatter field: {field}"))

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        findings.append(Finding(rel_path, "frontmatter name must be a non-empty string"))
    else:
        if name != expected_name:
            findings.append(Finding(rel_path, "frontmatter name does not match directory name"))
        if len(name) > 64 or not NAME_RE.fullmatch(name):
            findings.append(Finding(rel_path, "frontmatter name must match the Agent Skills naming rules"))

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        findings.append(Finding(rel_path, "frontmatter description must be a non-empty string"))
    elif len(description) > 1024:
        findings.append(Finding(rel_path, "frontmatter description exceeds 1024 characters"))

    license_value = frontmatter.get("license")
    if not isinstance(license_value, str) or not license_value.strip():
        findings.append(Finding(rel_path, "frontmatter license must be a non-empty string"))

    compatibility = frontmatter.get("compatibility")
    if not isinstance(compatibility, str) or not compatibility.strip():
        findings.append(Finding(rel_path, "frontmatter compatibility must be a non-empty string"))
    elif len(compatibility) > 500:
        findings.append(Finding(rel_path, "frontmatter compatibility exceeds 500 characters"))

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        findings.append(Finding(rel_path, "frontmatter metadata must be a mapping"))
    else:
        for key in REQUIRED_METADATA_KEYS:
            value = metadata.get(key)
            if not isinstance(value, str) or not value.strip():
                findings.append(Finding(rel_path, f"frontmatter metadata.{key} must be a non-empty string"))
        for key, value in metadata.items():
            if not isinstance(key, str) or not isinstance(value, str):
                findings.append(Finding(rel_path, "frontmatter metadata keys and values must be strings"))
                break

    allowed_tools = frontmatter.get("allowed-tools")
    if not isinstance(allowed_tools, str) or not allowed_tools.strip():
        findings.append(Finding(rel_path, "frontmatter allowed-tools must be a non-empty string"))

    return findings


def validate_openai_metadata(path: Path, metadata: dict[str, object]) -> list[Finding]:
    findings: list[Finding] = []
    rel_path = str(path)
    interface = metadata.get("interface")
    if not isinstance(interface, dict):
      return [Finding(rel_path, "missing interface mapping")]

    for key in REQUIRED_INTERFACE_KEYS:
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            findings.append(Finding(rel_path, f"missing or empty interface.{key}"))

    brand_color = interface.get("brand_color")
    if isinstance(brand_color, str) and not HEX_COLOR_RE.fullmatch(brand_color):
        findings.append(Finding(rel_path, "interface.brand_color must be a 6-digit hex color"))

    policy = metadata.get("policy")
    if not isinstance(policy, dict):
        findings.append(Finding(rel_path, "missing policy mapping"))
    else:
        allow_implicit = policy.get("allow_implicit_invocation")
        if not isinstance(allow_implicit, bool):
            findings.append(Finding(rel_path, "policy.allow_implicit_invocation must be a boolean"))

    dependencies = metadata.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            findings.append(Finding(rel_path, "dependencies must be a mapping when present"))
        else:
            tools = dependencies.get("tools")
            if tools is not None:
                if not isinstance(tools, list):
                    findings.append(Finding(rel_path, "dependencies.tools must be a list when present"))
                else:
                    for idx, tool in enumerate(tools):
                        if not isinstance(tool, dict):
                            findings.append(Finding(rel_path, f"dependencies.tools[{idx}] must be a mapping"))
                            continue
                        for key in ("type", "value"):
                            value = tool.get(key)
                            if not isinstance(value, str) or not value.strip():
                                findings.append(
                                    Finding(rel_path, f"dependencies.tools[{idx}].{key} must be a non-empty string")
                                )
    return findings


def find_skill_dirs(repo_root: Path) -> list[Path]:
    skills_root = repo_root / "skills"
    if not skills_root.exists():
        return []
    return sorted(
        path
        for path in skills_root.iterdir()
        if path.is_dir() and not path.name.startswith(".") and (path / "SKILL.md").exists()
    )


def validate_readme(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    readme = repo_root / "README.md"
    text = readme.read_text()
    for heading in README_REQUIRED_HEADINGS:
        if heading not in text:
            findings.append(Finding("README.md", f"missing heading: {heading}"))
    return findings


def validate_roadmap(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    roadmap = repo_root / "ROADMAP.md"
    text = roadmap.read_text()
    for heading in ROADMAP_REQUIRED_HEADINGS:
        if heading not in text:
            findings.append(Finding("ROADMAP.md", f"missing heading: {heading}"))
    if "### Status" not in text:
        findings.append(Finding("ROADMAP.md", "missing Status subsections"))
    if "### Scope" not in text:
        findings.append(Finding("ROADMAP.md", "missing Scope subsections"))
    if "### Tickets" not in text:
        findings.append(Finding("ROADMAP.md", "missing Tickets subsections"))
    if "### Exit Criteria" not in text:
        findings.append(Finding("ROADMAP.md", "missing Exit Criteria subsections"))
    return findings


def validate_skill_dir(repo_root: Path, skill_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_md = skill_dir / "SKILL.md"
    skill_text = skill_md.read_text()

    try:
        frontmatter = parse_frontmatter(skill_text, skill_md)
    except ValueError as exc:
        return [Finding(str(skill_md.relative_to(repo_root)), str(exc))]

    findings.extend(validate_frontmatter(skill_md.relative_to(repo_root), frontmatter, skill_dir.name))

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        findings.append(Finding(str(skill_dir.relative_to(repo_root)), "missing agents/openai.yaml"))
    else:
        try:
            metadata = load_yaml(openai_yaml)
            findings.extend(validate_openai_metadata(openai_yaml.relative_to(repo_root), metadata))
        except ValueError as exc:
            findings.append(Finding(str(openai_yaml.relative_to(repo_root)), str(exc)))

    for match in PATH_REFERENCE_RE.finditer(skill_text):
        rel_path = match.group(1)
        candidate = skill_dir / rel_path
        if not candidate.exists():
            findings.append(Finding(str(skill_md.relative_to(repo_root)), f"referenced path does not exist: {rel_path}"))

    return findings


def validate_plugin_manifest(
    repo_root: Path,
    manifest_path: Path,
    *,
    expected_name: str,
    require_skills_interface: bool,
) -> list[Finding]:
    findings: list[Finding] = []
    rel_path = str(manifest_path.relative_to(repo_root))

    if not manifest_path.exists():
        return [Finding(rel_path, "missing plugin manifest")]

    try:
        manifest = load_json(manifest_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return [Finding(rel_path, str(exc))]

    required_fields = PLUGIN_REQUIRED_FIELDS if require_skills_interface else ["name", "version", "description"]
    for field in required_fields:
        value = manifest.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            findings.append(Finding(rel_path, f"missing required plugin field: {field}"))

    plugin_name = manifest.get("name")
    if not isinstance(plugin_name, str) or not NAME_RE.fullmatch(plugin_name):
        findings.append(Finding(rel_path, "plugin name must match Codex plugin naming rules"))
    elif plugin_name != expected_name:
        findings.append(Finding(rel_path, f"plugin name must match {expected_name}"))

    version = manifest.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.\-]+)?$", version):
        findings.append(Finding(rel_path, "plugin version must look like a semantic version"))

    description = manifest.get("description")
    if not isinstance(description, str) or not description.strip():
        findings.append(Finding(rel_path, "plugin description must be a non-empty string"))

    for url_field in ("homepage", "repository"):
        value = manifest.get(url_field)
        if value is not None and (not isinstance(value, str) or not is_http_url(value)):
            findings.append(Finding(rel_path, f"{url_field} must be an http or https URL when present"))

    license_value = manifest.get("license")
    if license_value is not None and (not isinstance(license_value, str) or not license_value.strip()):
        findings.append(Finding(rel_path, "license must be a non-empty string when present"))

    if require_skills_interface:
        skills_path_value = manifest.get("skills")
        if not isinstance(skills_path_value, str) or not skills_path_value.startswith("./"):
            findings.append(Finding(rel_path, "skills must be a plugin-relative path starting with ./"))
        else:
            skills_path = (repo_root / skills_path_value.removeprefix("./")).resolve()
            expected_skills_root = (repo_root / "skills").resolve()
            if skills_path != expected_skills_root:
                findings.append(Finding(rel_path, "skills path must resolve to the repository skills/ directory"))
            if not skills_path.is_dir():
                findings.append(Finding(rel_path, "skills path does not resolve to an existing directory"))

        interface = manifest.get("interface")
        if not isinstance(interface, dict):
            findings.append(Finding(rel_path, "interface must be a mapping"))
        else:
            for field in PLUGIN_INTERFACE_REQUIRED_FIELDS:
                value = interface.get(field)
                if field == "capabilities":
                    if not isinstance(value, list) or not value or not all(
                        isinstance(item, str) and item.strip() for item in value
                    ):
                        findings.append(Finding(rel_path, "interface.capabilities must be a non-empty list of strings"))
                    continue
                if field == "defaultPrompt":
                    if not isinstance(value, list) or not value or not all(
                        isinstance(item, str) and item.strip() for item in value
                    ):
                        findings.append(Finding(rel_path, "interface.defaultPrompt must be a non-empty list of strings"))
                    continue
                if not isinstance(value, str) or not value.strip():
                    findings.append(Finding(rel_path, f"missing or empty interface.{field}"))

            brand_color = interface.get("brandColor")
            if isinstance(brand_color, str) and not HEX_COLOR_RE.fullmatch(brand_color):
                findings.append(Finding(rel_path, "interface.brandColor must be a 6-digit hex color"))

            website_url = interface.get("websiteURL")
            if isinstance(website_url, str) and not is_http_url(website_url):
                findings.append(Finding(rel_path, "interface.websiteURL must be an http or https URL"))

    return findings


def validate_claude_marketplace(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
    rel_path = str(marketplace_path.relative_to(repo_root))

    if not marketplace_path.exists():
        return [Finding(rel_path, "missing Claude marketplace file")]

    try:
        marketplace = load_json(marketplace_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return [Finding(rel_path, str(exc))]

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        return [Finding(rel_path, "plugins must be a non-empty list")]

    matched_plugin = None
    for plugin in plugins:
        if isinstance(plugin, dict) and plugin.get("name") == PLUGIN_DIR_NAME:
            matched_plugin = plugin
            break

    if matched_plugin is None:
        return [Finding(rel_path, f"Claude marketplace must include a {PLUGIN_DIR_NAME} plugin entry")]

    source = matched_plugin.get("source")
    if source != "./skills":
        findings.append(Finding(rel_path, "Claude marketplace source must be ./skills"))

    skills_root = repo_root / "skills"
    if not skills_root.is_dir():
        findings.append(Finding(rel_path, "Claude marketplace source does not point at an existing skills directory"))

    return findings


def validate_skill_mirrors(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    expected_symlinks = {
        repo_root / ".claude" / "skills": "../skills",
    }
    for path, target in expected_symlinks.items():
        rel_path = str(path.relative_to(repo_root))
        if not path.exists() and not path.is_symlink():
            findings.append(Finding(rel_path, f"missing symlink to {target}"))
            continue
        if not path.is_symlink():
            findings.append(Finding(rel_path, f"expected POSIX symlink to {target}"))
            continue
        if path.readlink().as_posix() != target:
            findings.append(Finding(rel_path, f"symlink target must be {target}"))
    return findings


def validate_doc_inventory(repo_root: Path, skill_dirs: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    readme_text = (repo_root / "README.md").read_text()
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        if f"`{skill_name}`" not in readme_text:
            findings.append(Finding("README.md", f"skill missing from root docs: {skill_name}"))
    return findings


def run(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_dirs = find_skill_dirs(repo_root)
    if not skill_dirs:
        findings.append(Finding("skills", "no bundled skill directories found under skills/"))
    findings.extend(validate_readme(repo_root))
    findings.extend(validate_roadmap(repo_root))
    plugin_root = repo_root / "plugins" / PLUGIN_DIR_NAME
    findings.extend(
        validate_plugin_manifest(
            repo_root,
            repo_root / ".codex-plugin" / "plugin.json",
            expected_name=PLUGIN_DIR_NAME,
            require_skills_interface=True,
        )
    )
    findings.extend(validate_claude_marketplace(repo_root))
    findings.extend(validate_skill_mirrors(repo_root))
    findings.extend(validate_doc_inventory(repo_root, skill_dirs))
    for skill_dir in skill_dirs:
        findings.extend(validate_skill_dir(repo_root, skill_dir))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate python-skills docs and metadata alignment.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--repo-root", default=".", help="Repository root to validate.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    findings = run(repo_root)

    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    elif findings:
        for finding in findings:
            print(f"{finding.path}: {finding.message}")
    else:
        print("No findings.")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
