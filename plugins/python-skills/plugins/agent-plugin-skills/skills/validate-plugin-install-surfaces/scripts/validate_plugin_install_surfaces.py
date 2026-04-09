from __future__ import annotations

import argparse
import json
import os
import re
import shlex
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

import yaml


EXACT_NO_FINDINGS = "No findings."
EXPECTED_OWNER = "gaelic-ghost"
REQUIRED_OPENAI_INTERFACE_FIELDS = ("display_name", "short_description", "default_prompt")
SKILL_ADD_RE = re.compile(r"^npx\s+skills\s+add\b")


@dataclass
class Finding:
    path: str
    issue_id: str
    message: str
    surface: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--plugin-name")
    parser.add_argument("--md-out")
    parser.add_argument("--json-out")
    parser.add_argument("--print-md", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    parser.add_argument("--fail-on-findings", action="store_true")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(read_text(path)) or {}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def relative_to_repo(repo_root: Path, path: Path) -> str:
    return str(path.relative_to(repo_root))


def canonical_skill_dirs(repo_root: Path) -> list[Path]:
    skills_root = repo_root / "skills"
    if not skills_root.is_dir():
        return []
    return sorted(path for path in skills_root.iterdir() if path.is_dir())


def plugin_roots(repo_root: Path) -> list[Path]:
    plugins_root = repo_root / "plugins"
    if not plugins_root.is_dir():
        return []
    return sorted(path for path in plugins_root.iterdir() if path.is_dir())


def infer_plugin_name(repo_root: Path, explicit: Optional[str]) -> Optional[str]:
    if explicit:
        return explicit
    roots = plugin_roots(repo_root)
    if len(roots) == 1:
        return roots[0].name
    return None


def is_symlink_target(path: Path, expected_target: str) -> Optional[Finding]:
    rel = str(path)
    if not path.exists() and not path.is_symlink():
        return Finding(rel, "missing-symlink", f"Expected POSIX symlink to `{expected_target}`.", "mirror")
    if not path.is_symlink():
        return Finding(rel, "not-symlink", f"Expected POSIX symlink to `{expected_target}`.", "mirror")
    actual = os.readlink(path)
    if actual != expected_target:
        return Finding(rel, "wrong-symlink-target", f"Expected symlink target `{expected_target}`, found `{actual}`.", "mirror")
    return None


def parse_skill_frontmatter(text: str) -> dict[str, Any]:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def audit_skill_metadata(repo_root: Path, skill_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_md = skill_dir / "SKILL.md"
    rel_skill = relative_to_repo(repo_root, skill_dir)
    if not skill_md.exists():
        findings.append(Finding(rel_skill, "missing-skill-md", "Skill directory is missing `SKILL.md`.", "metadata"))
        return findings

    frontmatter = parse_skill_frontmatter(read_text(skill_md))
    if not frontmatter:
        findings.append(Finding(relative_to_repo(repo_root, skill_md), "missing-frontmatter", "`SKILL.md` is missing YAML frontmatter.", "metadata"))
    else:
        if frontmatter.get("name") != skill_dir.name:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, skill_md),
                    "skill-name-mismatch",
                    f"`SKILL.md` frontmatter name should match `{skill_dir.name}`.",
                    "metadata",
                )
            )
        if not frontmatter.get("description"):
            findings.append(
                Finding(
                    relative_to_repo(repo_root, skill_md),
                    "missing-skill-description",
                    "`SKILL.md` frontmatter is missing `description`.",
                    "metadata",
                )
            )

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        findings.append(
            Finding(
                relative_to_repo(repo_root, openai_yaml),
                "missing-openai-yaml",
                "Skill is missing `agents/openai.yaml`.",
                "metadata",
            )
        )
        return findings

    openai_payload = load_yaml(openai_yaml)
    interface = openai_payload.get("interface")
    if not isinstance(interface, dict):
        findings.append(
            Finding(
                relative_to_repo(repo_root, openai_yaml),
                "missing-openai-interface",
                "`agents/openai.yaml` must define an `interface` mapping.",
                "metadata",
            )
        )
        return findings

    for field in REQUIRED_OPENAI_INTERFACE_FIELDS:
        if not interface.get(field):
            findings.append(
                Finding(
                    relative_to_repo(repo_root, openai_yaml),
                    f"missing-openai-{field}",
                    f"`agents/openai.yaml` is missing `interface.{field}`.",
                    "metadata",
                )
            )

    return findings


def audit_plugin_metadata(repo_root: Path, plugin_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    codex_manifest = plugin_root / ".codex-plugin" / "plugin.json"
    claude_manifest = plugin_root / ".claude-plugin" / "plugin.json"

    if not codex_manifest.exists():
        findings.append(
            Finding(
                relative_to_repo(repo_root, codex_manifest),
                "missing-codex-plugin-manifest",
                "Plugin root is missing `.codex-plugin/plugin.json`.",
                "metadata",
            )
        )
    else:
        payload = load_json(codex_manifest)
        for field in ("name", "version", "description"):
            if not payload.get(field):
                findings.append(
                    Finding(
                        relative_to_repo(repo_root, codex_manifest),
                        f"missing-codex-{field}",
                        f"Codex plugin manifest is missing `{field}`.",
                        "metadata",
                    )
                )
        if payload.get("name") and payload["name"] != plugin_root.name:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, codex_manifest),
                    "codex-plugin-name-mismatch",
                    f"Codex plugin manifest name should match plugin directory `{plugin_root.name}`.",
                    "metadata",
                )
            )

    if not claude_manifest.exists():
        findings.append(
            Finding(
                relative_to_repo(repo_root, claude_manifest),
                "missing-claude-plugin-manifest",
                "Plugin root is missing `.claude-plugin/plugin.json`.",
                "metadata",
            )
        )
    else:
        payload = load_json(claude_manifest)
        for field in ("name", "version", "description"):
            if not payload.get(field):
                findings.append(
                    Finding(
                        relative_to_repo(repo_root, claude_manifest),
                        f"missing-claude-{field}",
                        f"Claude plugin manifest is missing `{field}`.",
                        "metadata",
                    )
                )
        if payload.get("name") and payload["name"] != plugin_root.name:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, claude_manifest),
                    "claude-plugin-name-mismatch",
                    f"Claude plugin manifest name should match plugin directory `{plugin_root.name}`.",
                    "metadata",
                )
            )

    return findings


def audit_marketplace(repo_root: Path, plugin_dirs: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    marketplace = repo_root / ".agents" / "plugins" / "marketplace.json"
    if not marketplace.exists():
        return [
            Finding(
                relative_to_repo(repo_root, marketplace),
                "missing-marketplace",
                "Repository is missing `.agents/plugins/marketplace.json`.",
                "metadata",
            )
        ]

    payload = load_json(marketplace)
    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        return [
            Finding(
                relative_to_repo(repo_root, marketplace),
                "invalid-marketplace-plugins",
                "Marketplace metadata must define a `plugins` array.",
                "metadata",
            )
        ]

    plugin_dir_names = {path.name for path in plugin_dirs}
    seen_plugin_names: set[str] = set()

    for entry in plugins:
        name = entry.get("name")
        source = entry.get("source") or {}
        path = source.get("path")
        if not name:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, marketplace),
                    "marketplace-missing-plugin-name",
                    "Marketplace entry is missing `name`.",
                    "metadata",
                )
            )
            continue
        seen_plugin_names.add(name)
        if name not in plugin_dir_names:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, marketplace),
                    "marketplace-plugin-missing-root",
                    f"Marketplace entry `{name}` does not match a plugin directory under `plugins/`.",
                    "metadata",
                )
            )
        if not isinstance(path, str):
            findings.append(
                Finding(
                    relative_to_repo(repo_root, marketplace),
                    "marketplace-missing-source-path",
                    f"Marketplace entry `{name}` is missing `source.path`.",
                    "metadata",
                )
            )
            continue
        if not path.startswith("./"):
            findings.append(
                Finding(
                    relative_to_repo(repo_root, marketplace),
                    "marketplace-nonrelative-source-path",
                    f"Marketplace entry `{name}` must use a `./`-prefixed local `source.path`.",
                    "metadata",
                )
            )
            continue
        if path == "./":
            findings.append(
                Finding(
                    relative_to_repo(repo_root, marketplace),
                    "marketplace-empty-relative-source-path",
                    f"Marketplace entry `{name}` points at the marketplace root with `./`, but Codex local plugin source paths must point at a non-empty staged plugin directory.",
                    "metadata",
                )
            )
            continue
        resolved = (repo_root / path.removeprefix("./")).resolve()
        try:
            resolved.relative_to(repo_root)
        except ValueError:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, marketplace),
                    "marketplace-source-path-escapes-root",
                    f"Marketplace entry `{name}` points outside the repository root.",
                    "metadata",
                )
            )
            continue
        if not resolved.exists():
            findings.append(
                Finding(
                    relative_to_repo(repo_root, marketplace),
                    "marketplace-source-path-missing",
                    f"Marketplace entry `{name}` points at a missing plugin root: `{path}`.",
                    "metadata",
                )
            )

    for plugin_dir in plugin_dirs:
        if plugin_dir.name not in seen_plugin_names:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, marketplace),
                    "plugin-root-missing-marketplace-entry",
                    f"Plugin root `{plugin_dir.name}` is not represented in `.agents/plugins/marketplace.json`.",
                    "metadata",
                )
            )

    return findings


def parse_skills_add_command(line: str) -> Optional[tuple[str, Optional[str]]]:
    stripped = line.strip()
    if not SKILL_ADD_RE.match(stripped):
        return None
    try:
        tokens = shlex.split(stripped)
    except ValueError:
        return None
    if len(tokens) < 4:
        return None
    target = tokens[3]
    skill_name: Optional[str] = None
    for idx, token in enumerate(tokens[4:], start=4):
        if token == "--skill" and idx + 1 < len(tokens):
            skill_name = tokens[idx + 1]
            break
        if token.startswith("--skill="):
            skill_name = token.split("=", 1)[1]
            break
    return target, skill_name


def audit_install_surfaces(repo_root: Path, skill_dirs: list[Path], plugin_dirs: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    readme = repo_root / "README.md"
    if not readme.exists():
        return [
            Finding(
                relative_to_repo(repo_root, readme),
                "missing-readme",
                "Repository is missing `README.md` for install-surface validation.",
                "install-surface",
            )
        ]

    text = read_text(readme)
    skill_names = {path.name for path in skill_dirs}
    repo_slug = f"{EXPECTED_OWNER}/{repo_root.name}"

    for line in text.splitlines():
        parsed = parse_skills_add_command(line)
        if parsed is None:
            continue
        target, skill_name = parsed
        if target != repo_slug:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, readme),
                    "readme-install-target-mismatch",
                    f"README install command should target `{repo_slug}`, found `{target}`.",
                    "install-surface",
                )
            )
        if skill_name and skill_name not in skill_names:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, readme),
                    "readme-install-missing-skill",
                    f"README install command references missing skill `{skill_name}`.",
                    "install-surface",
                )
            )

    if any((plugin_root / ".codex-plugin" / "plugin.json").exists() for plugin_root in plugin_dirs):
        if "Codex Plugin" not in text:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, readme),
                    "missing-codex-install-surface-docs",
                    "README should document the Codex Plugin install surface when `.codex-plugin/plugin.json` exists.",
                    "install-surface",
                )
            )
    if any((plugin_root / ".claude-plugin" / "plugin.json").exists() for plugin_root in plugin_dirs):
        if "Claude Code Plugin" not in text:
            findings.append(
                Finding(
                    relative_to_repo(repo_root, readme),
                    "missing-claude-install-surface-docs",
                    "README should document Claude Code plugin usage guidance when `.claude-plugin/plugin.json` exists.",
                    "install-surface",
                )
            )

    return findings


def audit_mirrors(repo_root: Path, plugin_name: Optional[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path, target in (
        (repo_root / ".agents" / "skills", "../skills"),
        (repo_root / ".claude" / "skills", "../skills"),
    ):
        issue = is_symlink_target(path, target)
        if issue is not None:
            issue.path = relative_to_repo(repo_root, path)
            findings.append(issue)

    if plugin_name is not None:
        plugin_skills = repo_root / "plugins" / plugin_name / "skills"
        issue = is_symlink_target(plugin_skills, "../../skills")
        if issue is not None:
            issue.path = relative_to_repo(repo_root, plugin_skills)
            findings.append(issue)

    return findings


def build_report(
    repo_root: Path,
    skill_dirs: list[Path],
    plugin_dirs: list[Path],
    plugin_name: Optional[str],
    metadata_findings: list[Finding],
    install_surface_findings: list[Finding],
    mirror_findings: list[Finding],
    errors: list[str],
) -> dict[str, Any]:
    return {
        "run_context": {
            "repo_root": str(repo_root),
            "plugin_name": plugin_name,
            "mode": "audit-only",
        },
        "canonical_skill_dirs": [relative_to_repo(repo_root, path) for path in skill_dirs],
        "plugin_roots": [relative_to_repo(repo_root, path) for path in plugin_dirs],
        "metadata_findings": [asdict(item) for item in metadata_findings],
        "install_surface_findings": [asdict(item) for item in install_surface_findings],
        "mirror_findings": [asdict(item) for item in mirror_findings],
        "errors": errors,
    }


def summarize_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = [
        "## Run Context",
        f"- Repo root: {report['run_context']['repo_root']}",
        f"- Plugin name: {report['run_context']['plugin_name']}",
        f"- Mode: {report['run_context']['mode']}",
        "",
        "## Canonical Skills",
    ]
    if not report["canonical_skill_dirs"]:
        lines.append("- None discovered")
    else:
        for item in report["canonical_skill_dirs"]:
            lines.append(f"- {item}")
    lines.extend(["", "## Plugin Roots"])
    if not report["plugin_roots"]:
        lines.append("- None discovered")
    else:
        for item in report["plugin_roots"]:
            lines.append(f"- {item}")

    for section_name, key in (
        ("Metadata Findings", "metadata_findings"),
        ("Install Surface Findings", "install_surface_findings"),
        ("Mirror Findings", "mirror_findings"),
    ):
        lines.extend(["", f"## {section_name}"])
        if not report[key]:
            lines.append("- None")
        else:
            for item in report[key]:
                lines.append(f"- {item['path']}: {item['message']}")

    lines.extend(["", "## Errors"])
    if not report["errors"]:
        lines.append("- None")
    else:
        for item in report["errors"]:
            lines.append(f"- {item}")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        print("Repository root does not exist or is not a directory.", file=os.sys.stderr)
        return 1

    errors: list[str] = []
    skill_dirs = canonical_skill_dirs(repo_root)
    plugin_dirs = plugin_roots(repo_root)
    plugin_name = infer_plugin_name(repo_root, args.plugin_name)

    metadata_findings: list[Finding] = []
    install_surface_findings: list[Finding] = []
    mirror_findings: list[Finding] = []

    for skill_dir in skill_dirs:
        metadata_findings.extend(audit_skill_metadata(repo_root, skill_dir))
    for plugin_root in plugin_dirs:
        metadata_findings.extend(audit_plugin_metadata(repo_root, plugin_root))
    metadata_findings.extend(audit_marketplace(repo_root, plugin_dirs))
    install_surface_findings.extend(audit_install_surfaces(repo_root, skill_dirs, plugin_dirs))
    mirror_findings.extend(audit_mirrors(repo_root, plugin_name))

    report = build_report(
        repo_root,
        skill_dirs,
        plugin_dirs,
        plugin_name,
        metadata_findings,
        install_surface_findings,
        mirror_findings,
        errors,
    )
    md_report = summarize_markdown(report)
    json_report = json.dumps(report, indent=2, sort_keys=True)

    if args.md_out:
        Path(args.md_out).expanduser().write_text(md_report, encoding="utf-8")
    if args.json_out:
        Path(args.json_out).expanduser().write_text(json_report + "\n", encoding="utf-8")
    if args.print_md:
        if not metadata_findings and not install_surface_findings and not mirror_findings and not errors:
            print(EXACT_NO_FINDINGS)
        else:
            print(md_report, end="")
    if args.print_json:
        print(json_report)

    if args.fail_on_findings and (metadata_findings or install_surface_findings or mirror_findings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
