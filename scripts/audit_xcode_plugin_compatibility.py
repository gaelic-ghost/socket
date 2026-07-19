#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Inventory Socket plugin components and classify Xcode agent compatibility."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal


REPO_ROOT = Path(__file__).resolve().parent.parent
Status = Literal["likely", "partial", "blocked", "unknown"]


@dataclass(frozen=True)
class TargetAssessment:
    status: Status
    reason: str
    next_check: str


@dataclass(frozen=True)
class PluginAssessment:
    name: str
    source: str
    available: bool
    manifest: str | None
    skills: tuple[str, ...]
    mcp_servers: tuple[str, ...]
    mcp_risks: tuple[str, ...]
    hooks: tuple[str, ...]
    app_configs: tuple[str, ...]
    custom_agents: tuple[str, ...]
    openai_interface_metadata_count: int
    xcode_internal_plugin: TargetAssessment
    xcode_launched_codex: TargetAssessment
    external_agent_xcode_mcp: TargetAssessment


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return value


def marketplace_entries(repo_root: Path) -> tuple[dict[str, Any], ...]:
    document = load_json(repo_root / ".agents" / "plugins" / "marketplace.json")
    plugins = document.get("plugins")
    if not isinstance(plugins, list):
        raise ValueError(".agents/plugins/marketplace.json must define a plugins array.")
    return tuple(entry for entry in plugins if isinstance(entry, dict))


def resolve_source(repo_root: Path, entry: dict[str, Any]) -> tuple[str, Path | None]:
    source = entry.get("source")
    if isinstance(source, str):
        if source.startswith("./"):
            return source, repo_root / source[2:]
        return source, None
    if not isinstance(source, dict):
        return "unresolved", None
    kind = source.get("source")
    if kind == "local" and isinstance(source.get("path"), str):
        path = source["path"]
        if path.startswith("./"):
            return path, repo_root / path[2:]
    if kind == "url" and isinstance(source.get("url"), str):
        ref = source.get("ref")
        suffix = f"@{ref}" if isinstance(ref, str) else ""
        return f"{source['url']}{suffix}", None
    return f"{kind or 'unresolved'}", None


def skill_names(root: Path, manifest: dict[str, Any]) -> tuple[str, ...]:
    declared = manifest.get("skills", "./skills/")
    if not isinstance(declared, str) or not declared.startswith("./"):
        return ()
    skills_root = root / declared[2:]
    if not skills_root.is_dir():
        return ()
    return tuple(
        path.parent.name
        for path in sorted(skills_root.glob("*/SKILL.md"))
        if path.is_file()
    )


def mcp_config_paths(root: Path, manifest: dict[str, Any]) -> tuple[Path, ...]:
    declared = manifest.get("mcpServers")
    values = declared if isinstance(declared, list) else [declared]
    paths = [
        root / value[2:]
        for value in values
        if isinstance(value, str) and value.startswith("./")
    ]
    default = root / ".mcp.json"
    if not paths and default.is_file():
        paths.append(default)
    return tuple(path for path in paths if path.is_file())


def inspect_mcp(root: Path, paths: tuple[Path, ...]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    servers: set[str] = set()
    risks: set[str] = set()
    for path in paths:
        document = load_json(path)
        mapping = document.get("mcpServers", document)
        if not isinstance(mapping, dict):
            risks.add(f"{path.relative_to(root)} does not define an MCP server mapping")
            continue
        for name, value in mapping.items():
            if not isinstance(name, str) or not isinstance(value, dict):
                continue
            servers.add(name)
            serialized = json.dumps(value)
            cwd = value.get("cwd")
            command = value.get("command")
            if isinstance(cwd, str) and (cwd.startswith("../") or "/../" in cwd):
                risks.add(f"{name}: parent-relative working directory requires Xcode import proof")
            if "/Users/" in serialized or serialized.startswith("~"):
                risks.add(f"{name}: machine-local path is not portable")
            if "${PLUGIN_ROOT}" in serialized:
                risks.add(f"{name}: Codex PLUGIN_ROOT expansion is unverified in Xcode internal agents")
            if isinstance(command, str) and not command.startswith("https://"):
                risks.add(f"{name}: local command and dependencies require Xcode environment proof")
    return tuple(sorted(servers)), tuple(sorted(risks))


def declared_paths(
    root: Path,
    manifest: dict[str, Any],
    field: str,
    default: str | None,
) -> tuple[str, ...]:
    declared = manifest.get(field)
    values = declared if isinstance(declared, list) else [declared]
    resolved = [
        value[2:]
        for value in values
        if isinstance(value, str) and value.startswith("./") and (root / value[2:]).exists()
    ]
    if not resolved and default is not None and (root / default).exists():
        resolved.append(default)
    return tuple(sorted(resolved))


def assess_targets(
    *,
    available: bool,
    resolved: bool,
    skills: tuple[str, ...],
    mcp: tuple[str, ...],
    risks: tuple[str, ...],
    hooks: tuple[str, ...],
    apps: tuple[str, ...],
    agents: tuple[str, ...],
) -> tuple[TargetAssessment, TargetAssessment, TargetAssessment]:
    if not available:
        blocked = TargetAssessment(
            "blocked",
            "The Socket marketplace marks this plugin unavailable.",
            "Make the plugin installable before testing any Xcode target.",
        )
        return blocked, blocked, blocked
    if not resolved:
        unknown = TargetAssessment(
            "unknown",
            "The plugin payload is Git-backed outside this checkout, so this source audit cannot inspect its components.",
            "Resolve the pinned plugin source and rerun the component inventory before Xcode import testing.",
        )
        return unknown, unknown, unknown

    portable = bool(skills)
    runtime_components = bool(mcp or hooks or apps or agents)
    if not portable and not runtime_components:
        blocked = TargetAssessment(
            "blocked",
            "No Xcode-documented skill, MCP, hook, or subagent component is present.",
            "Add a supported component or keep the plugin host-specific by design.",
        )
        return blocked, blocked, blocked

    if portable and not runtime_components:
        internal = TargetAssessment(
            "likely",
            "The payload is skill-only, matching Xcode's documented plug-in component model.",
            "Import from the public Socket URL and invoke one representative skill in an Xcode internal agent.",
        )
        launched = TargetAssessment(
            "likely",
            "Xcode has previously mirrored imported skill payloads into its Codex-specific home.",
            "Confirm the skill appears in Xcode-launched Codex for the current beta build.",
        )
        external = TargetAssessment(
            "likely",
            "External agents can use the portable skills in their own host while Xcode access remains a separate MCP bridge.",
            "Confirm the external host sees the skill and Xcode's MCP bridge independently.",
        )
        return internal, launched, external

    internal_reason = "Xcode documents these component kinds, but runtime behavior needs current-beta proof."
    if risks:
        internal_reason += f" The audit found {len(risks)} MCP portability risk(s)."
    internal = TargetAssessment(
        "partial",
        internal_reason,
        "Import only a representative plugin and verify each skill, MCP server, hook, and subagent component separately.",
    )
    launched = TargetAssessment(
        "partial",
        "Xcode can mirror imported payloads into its Codex home, but hook trust, app behavior, custom agents, and MCP launch environments are not equivalent by assumption.",
        "Inspect Xcode's Codex-specific enabled state, then run one harmless check per component kind.",
    )
    external_status: Status = "likely" if portable else "partial"
    external = TargetAssessment(
        external_status,
        "External-agent Xcode MCP access is separate from Xcode plug-in import; portable skills remain useful, while host-specific runtime components stay in the external host.",
        "Verify the external host plugin and Xcode MCP connection as two independent dependencies.",
    )
    return internal, launched, external


def inspect_entry(repo_root: Path, entry: dict[str, Any]) -> PluginAssessment:
    name = str(entry.get("name", "(unnamed)"))
    source, root = resolve_source(repo_root, entry)
    available = (
        entry.get("policy", {}).get("installation") != "NOT_AVAILABLE"
        if isinstance(entry.get("policy"), dict)
        else True
    )
    manifest_path = root / ".codex-plugin" / "plugin.json" if root else None
    manifest = load_json(manifest_path) if manifest_path and manifest_path.is_file() else {}
    skills = skill_names(root, manifest) if root else ()
    mcp_paths = mcp_config_paths(root, manifest) if root else ()
    mcp, risks = inspect_mcp(root, mcp_paths) if root else ((), ())
    hooks = declared_paths(root, manifest, "hooks", "hooks/hooks.json") if root else ()
    apps = declared_paths(root, manifest, "apps", ".app.json") if root else ()
    agents = (
        tuple(path.relative_to(root).as_posix() for path in sorted(root.glob(".codex/agents/*.toml")))
        if root
        else ()
    )
    interface_count = len(tuple(root.glob("skills/*/agents/openai.yaml"))) if root else 0
    internal, launched, external = assess_targets(
        available=available,
        resolved=bool(root and manifest_path and manifest_path.is_file()),
        skills=skills,
        mcp=mcp,
        risks=risks,
        hooks=hooks,
        apps=apps,
        agents=agents,
    )
    return PluginAssessment(
        name=name,
        source=source,
        available=available,
        manifest=manifest_path.relative_to(repo_root).as_posix() if manifest_path and manifest_path.is_file() else None,
        skills=skills,
        mcp_servers=mcp,
        mcp_risks=risks,
        hooks=hooks,
        app_configs=apps,
        custom_agents=agents,
        openai_interface_metadata_count=interface_count,
        xcode_internal_plugin=internal,
        xcode_launched_codex=launched,
        external_agent_xcode_mcp=external,
    )


def build_report(repo_root: Path) -> tuple[PluginAssessment, ...]:
    return tuple(inspect_entry(repo_root, entry) for entry in marketplace_entries(repo_root))


def render_markdown(report: tuple[PluginAssessment, ...]) -> str:
    lines = [
        "# Socket Xcode Plug-in Compatibility Audit",
        "",
        "This is a source-only, read-only assessment. `likely` and `partial` still require current Xcode runtime proof.",
        "",
        "| Plugin | Skills | MCP | Hooks | Apps | Agents | Xcode internal | Xcode Codex | External agent |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for item in report:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item.name}`",
                    str(len(item.skills)),
                    str(len(item.mcp_servers)),
                    str(len(item.hooks)),
                    str(len(item.app_configs)),
                    str(len(item.custom_agents)),
                    item.xcode_internal_plugin.status,
                    item.xcode_launched_codex.status,
                    item.external_agent_xcode_mcp.status,
                ]
            )
            + " |"
        )
    lines.extend(["", "## Runtime-proof queue", ""])
    queued = [item for item in report if item.xcode_internal_plugin.status in {"partial", "unknown"}]
    if not queued:
        lines.append("No partial or unknown Xcode internal plug-ins.")
    for item in queued:
        lines.append(f"- `{item.name}`: {item.xcode_internal_plugin.reason} {item.xcode_internal_plugin.next_check}")
        lines.extend(f"  - {risk}" for risk in item.mcp_risks)
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(args.repo_root.resolve())
    if args.format == "json":
        print(json.dumps([asdict(item) for item in report], indent=2))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
