from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


EXACT_NO_FINDINGS = "No findings."
DEFAULT_SCOPE = "personal"
DEFAULT_INSTALL_MODE = "copy"
DEFAULT_REPO_INSTALL_TRACKING = "local-only"
DEFAULT_PERSONAL_MARKETPLACE_NAME = "local-personal"
DEFAULT_REPO_MARKETPLACE_NAME = "local-repo"
REPO_CONFIG_RELATIVE_PATH = Path(".codex") / "profiles" / "install-plugin-to-socket" / "customization.yaml"
GLOBAL_CONFIG_RELATIVE_PATH = Path(".config") / "gaelic-ghost" / "agent-plugin-skills" / "install-plugin-to-socket" / "customization.yaml"
CODEX_CONFIG_RELATIVE_PATH = Path(".codex") / "config.toml"
CODEX_APP_SERVER_TIMEOUT_SECONDS = 20


@dataclass
class Finding:
    path: str
    issue_id: str
    message: str


def _resolve_home() -> Path:
    return Path.home().resolve()


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _pretty_plugin_title(name: str) -> str:
    return name.replace("-", " ").title()


def _relative_to_root(path: Path, root: Path) -> str:
    return str(path.absolute().relative_to(root.absolute()))


def _path_within_root(path: Path, root: Path) -> bool:
    try:
        path.absolute().relative_to(root.absolute())
        return True
    except ValueError:
        return False


def _is_same_path(left: Path, right: Path) -> bool:
    return left.resolve() == right.resolve()


def _plugin_manifest_path(root: Path) -> Path:
    return root / ".codex-plugin" / "plugin.json"


def _repo_marketplace_path(repo_root: Path) -> Path:
    return repo_root / ".agents" / "plugins" / "marketplace.json"


def _repo_plugin_root(repo_root: Path, plugin_name: str) -> Path:
    return repo_root / "plugins" / plugin_name


def _legacy_repo_private_marketplace_path(repo_root: Path) -> Path:
    return repo_root / ".codex" / "plugins" / "marketplace.json"


def _legacy_repo_private_plugin_root(repo_root: Path, plugin_name: str) -> Path:
    return repo_root / ".codex" / "plugins" / plugin_name


def _normalize_scope(raw_scope: str | None) -> str | None:
    if raw_scope is None:
        return None
    normalized = raw_scope.strip().lower()
    if normalized in {"personal", "global"}:
        return "personal"
    if normalized in {"repo", "repo-local"}:
        return "repo"
    return None


def _normalize_repo_install_tracking(raw_tracking: str | None) -> str | None:
    if raw_tracking is None:
        return None
    normalized = raw_tracking.strip().lower()
    if normalized in {"tracked", "shared", "committed"}:
        return "tracked"
    if normalized in {"local-only", "local", "untracked"}:
        return "local-only"
    return None


def read_optional_config(project_root: Path, config_override: str | None) -> dict[str, object]:
    config_paths: list[Path] = []
    if config_override:
        override_path = Path(config_override).expanduser().resolve()
        if not override_path.is_file():
            return {
                "config_path": str(override_path),
                "config_error": "Requested `--config` path does not exist.",
            }
        config_paths.append(override_path)
    else:
        config_paths.append((project_root / REPO_CONFIG_RELATIVE_PATH).resolve())
        config_paths.append((_resolve_home() / GLOBAL_CONFIG_RELATIVE_PATH).resolve())

    for path in config_paths:
        if not path.is_file():
            continue
        text = _read_text(path)
        result: dict[str, object] = {"config_path": str(path)}
        for key in ["schemaVersion", "profile", "isCustomized", "defaultInstallScope", "repoInstallTracking"]:
            match = re.search(rf"^\s*{key}\s*:\s*(.+?)\s*$", text, flags=re.MULTILINE)
            if match:
                result[key] = match.group(1).strip().strip('"').strip("'")
        return result
    return {"config_path": "none"}


def resolve_scope(scope_arg: str | None, project_root: Path, config_override: str | None) -> tuple[str, dict[str, object], list[str]]:
    config = read_optional_config(project_root, config_override)
    errors: list[str] = []
    if isinstance(config, dict) and config.get("config_error") is not None:
        errors.append(str(config["config_error"]))
        return DEFAULT_SCOPE, {"source": "invalid-config", **config}, errors
    if scope_arg is not None:
        return scope_arg, {"source": "cli", **config}, errors

    configured_scope = _normalize_scope(config.get("defaultInstallScope") if isinstance(config, dict) else None)
    if isinstance(config, dict) and config.get("defaultInstallScope") is not None and configured_scope is None:
        errors.append(
            "Installer config sets `defaultInstallScope` to an unsupported value. Use `personal`, `global`, `repo`, or `repo-local`."
        )
        return DEFAULT_SCOPE, {"source": "invalid-config", **config}, errors
    if configured_scope is not None:
        return configured_scope, {"source": "config", **config}, errors
    return DEFAULT_SCOPE, {"source": "default", **config}, errors


def resolve_repo_install_tracking(
    tracking_arg: str | None,
    scope: str,
    scope_context: dict[str, object],
) -> tuple[str | None, str, list[str]]:
    errors: list[str] = []
    if scope != "repo":
        return None, "not-applicable", errors

    if tracking_arg is not None:
        normalized = _normalize_repo_install_tracking(tracking_arg)
        if normalized is None:
            errors.append("Installer repo install tracking must be `tracked` or `local-only`.")
            return DEFAULT_REPO_INSTALL_TRACKING, "invalid-cli", errors
        return normalized, "cli", errors

    configured_tracking = _normalize_repo_install_tracking(
        scope_context.get("repoInstallTracking") if isinstance(scope_context, dict) else None
    )
    if isinstance(scope_context, dict) and scope_context.get("repoInstallTracking") is not None and configured_tracking is None:
        errors.append("Installer config sets `repoInstallTracking` to an unsupported value. Use `tracked` or `local-only`.")
        return DEFAULT_REPO_INSTALL_TRACKING, "invalid-config", errors
    if configured_tracking is not None:
        return configured_tracking, "config", errors
    return DEFAULT_REPO_INSTALL_TRACKING, "default", errors


def _discover_plugin_roots_under(repo_root: Path) -> list[Path]:
    plugins_dir = repo_root / "plugins"
    if not plugins_dir.is_dir():
        return []
    return sorted(path for path in plugins_dir.iterdir() if _plugin_manifest_path(path).is_file())


def resolve_source_plugin_root(requested_root: Path, *, allow_repo_root_resolution: bool = False) -> Path:
    if _plugin_manifest_path(requested_root).is_file():
        return requested_root

    if not allow_repo_root_resolution:
        return requested_root

    candidates: list[Path] = []
    for marketplace_path in (_repo_marketplace_path(requested_root), _legacy_repo_private_marketplace_path(requested_root)):
        if not marketplace_path.is_file():
            continue
        try:
            payload = _load_json(marketplace_path)
        except json.JSONDecodeError:
            payload = {}
        plugins = payload.get("plugins", [])
        if not isinstance(plugins, list):
            continue
        scope_root = marketplace_path.parent.parent.parent
        for plugin in plugins:
            if not isinstance(plugin, dict):
                continue
            source = plugin.get("source")
            if not isinstance(source, dict):
                continue
            raw_path = source.get("path")
            if not isinstance(raw_path, str) or not raw_path.startswith("./"):
                continue
            candidate = (scope_root / raw_path[2:]).resolve()
            if _plugin_manifest_path(candidate).is_file():
                candidates.append(candidate)
    unique_candidates = sorted({candidate for candidate in candidates})
    if len(unique_candidates) == 1:
        return unique_candidates[0]

    discovered = _discover_plugin_roots_under(requested_root)
    if len(discovered) == 1:
        return discovered[0]

    return requested_root


def load_plugin_manifest(source_plugin_root: Path) -> dict[str, object]:
    return _load_json(_plugin_manifest_path(source_plugin_root))


def infer_plugin_name(source_plugin_root: Path, manifest: dict[str, object]) -> str:
    raw_name = manifest.get("name")
    if isinstance(raw_name, str) and raw_name.strip():
        return raw_name.strip()
    return source_plugin_root.name


def infer_category(manifest: dict[str, object]) -> str:
    interface = manifest.get("interface")
    if isinstance(interface, dict):
        category = interface.get("category")
        if isinstance(category, str) and category.strip():
            return category.strip()
    return "Productivity"


def _resolve_plugin_relative_path(source_plugin_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (source_plugin_root / path).resolve()


def audit_optional_plugin_surfaces(source_plugin_root: Path, manifest: dict[str, object]) -> tuple[list[Finding], dict[str, object]]:
    findings: list[Finding] = []
    surfaces: dict[str, object] = {}

    for manifest_key, issue_id, message in [
        ("skills", "missing-skills-surface", "Plugin manifest points at a `skills` path that does not exist."),
        ("mcpServers", "missing-mcp-surface", "Plugin manifest points at an `mcpServers` path that does not exist."),
        ("apps", "missing-app-surface", "Plugin manifest points at an `apps` path that does not exist."),
    ]:
        raw_path = manifest.get(manifest_key)
        if isinstance(raw_path, str) and raw_path.strip():
            resolved_path = _resolve_plugin_relative_path(source_plugin_root, raw_path.strip())
            surfaces[manifest_key] = {"path": raw_path.strip(), "exists": resolved_path.exists()}
            if not resolved_path.exists():
                findings.append(Finding(str(resolved_path), issue_id, message))

    hooks_path = source_plugin_root / "hooks" / "hooks.json"
    if hooks_path.parent.exists():
        surfaces["hooks"] = {"path": "./hooks/hooks.json", "exists": hooks_path.exists()}
        if not hooks_path.exists():
            findings.append(
                Finding(str(hooks_path), "missing-hooks-config", "Plugin has a `hooks/` directory but is missing `hooks/hooks.json`.")
            )

    interface = manifest.get("interface")
    if isinstance(interface, dict):
        asset_findings: list[dict[str, object]] = []
        for field_name in ("composerIcon", "logo"):
            raw_path = interface.get(field_name)
            if isinstance(raw_path, str) and raw_path.strip():
                resolved_path = _resolve_plugin_relative_path(source_plugin_root, raw_path.strip())
                exists = resolved_path.exists()
                asset_findings.append({"field": field_name, "path": raw_path.strip(), "exists": exists})
                if not exists:
                    findings.append(
                        Finding(
                            str(resolved_path),
                            "missing-interface-asset",
                            f"Plugin interface field `{field_name}` points at an asset path that does not exist.",
                        )
                    )
        screenshots = interface.get("screenshots")
        if isinstance(screenshots, list):
            for raw_path in screenshots:
                if not isinstance(raw_path, str) or not raw_path.strip():
                    continue
                resolved_path = _resolve_plugin_relative_path(source_plugin_root, raw_path.strip())
                exists = resolved_path.exists()
                asset_findings.append({"field": "screenshots", "path": raw_path.strip(), "exists": exists})
                if not exists:
                    findings.append(
                        Finding(
                            str(resolved_path),
                            "missing-interface-asset",
                            "Plugin interface `screenshots` includes an asset path that does not exist.",
                        )
                    )
        if asset_findings:
            surfaces["interfaceAssets"] = asset_findings

    return findings, surfaces


def build_source_plugin_summary(
    requested_root: Path,
    source_plugin_root: Path,
    manifest: dict[str, object],
    plugin_name: str,
) -> dict[str, object]:
    surface_findings, optional_surfaces = audit_optional_plugin_surfaces(source_plugin_root, manifest)
    summary = {
        "requested_root": str(requested_root),
        "source_root": str(source_plugin_root),
        "manifest_path": str(_plugin_manifest_path(source_plugin_root)),
        "name": plugin_name,
        "version": manifest.get("version", "unknown"),
        "description": manifest.get("description", ""),
        "category": infer_category(manifest),
    }
    if requested_root != source_plugin_root:
        summary["resolved_from"] = "auto-detected-plugin-root"
    if optional_surfaces:
        summary["optional_surfaces"] = optional_surfaces
    if surface_findings:
        summary["surface_findings"] = [asdict(item) for item in surface_findings]
    return summary


def scope_paths(scope: str, plugin_name: str, repo_root: Path | None) -> tuple[Path, Path, Path]:
    if scope == "repo":
        scope_root = repo_root.resolve() if repo_root is not None else Path.cwd().resolve()
        target_plugin_root = _repo_plugin_root(scope_root, plugin_name)
        marketplace_path = _repo_marketplace_path(scope_root)
        return scope_root, target_plugin_root, marketplace_path
    if scope == "personal":
        scope_root = _resolve_home()
        target_plugin_root = scope_root / ".codex" / "plugins" / plugin_name
        marketplace_path = scope_root / ".agents" / "plugins" / "marketplace.json"
        return scope_root, target_plugin_root, marketplace_path
    raise ValueError(f"Unsupported scope: {scope}")


def expected_marketplace_entry(scope_root: Path, target_plugin_root: Path, plugin_name: str, category: str) -> dict[str, object]:
    relative_path = "./" + _relative_to_root(target_plugin_root, scope_root)
    return {
        "name": plugin_name,
        "source": {
            "source": "local",
            "path": relative_path,
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": category,
    }


def expected_marketplace_name(scope: str) -> str:
    if scope == "repo":
        return DEFAULT_REPO_MARKETPLACE_NAME
    return DEFAULT_PERSONAL_MARKETPLACE_NAME


def ensure_marketplace_shape(existing: dict[str, object] | None, scope: str) -> dict[str, object]:
    if existing is None:
        marketplace_name = expected_marketplace_name(scope)
        return {
            "name": marketplace_name,
            "interface": {
                "displayName": _pretty_plugin_title(marketplace_name),
            },
            "plugins": [],
        }
    payload = dict(existing)
    if not isinstance(payload.get("name"), str) or not str(payload["name"]).strip():
        payload["name"] = expected_marketplace_name(scope)
    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        payload["plugins"] = []
    return payload


def marketplace_name_from_payload(payload: dict[str, object], scope: str) -> str:
    raw_name = payload.get("name")
    if isinstance(raw_name, str) and raw_name.strip():
        return raw_name.strip()
    return expected_marketplace_name(scope)


def merge_marketplace_entry(payload: dict[str, object], entry: dict[str, object]) -> tuple[dict[str, object], bool]:
    plugins = list(payload.get("plugins", []))
    changed = False
    replaced = False
    merged_plugins: list[object] = []
    for item in plugins:
        if isinstance(item, dict) and item.get("name") == entry["name"]:
            merged_plugins.append(entry)
            replaced = True
            if item != entry:
                changed = True
        else:
            merged_plugins.append(item)
    if not replaced:
        merged_plugins.append(entry)
        changed = True
    payload["plugins"] = merged_plugins
    return payload, changed


def remove_marketplace_entry(payload: dict[str, object], plugin_name: str) -> tuple[dict[str, object], bool]:
    plugins = list(payload.get("plugins", []))
    filtered = [item for item in plugins if not (isinstance(item, dict) and item.get("name") == plugin_name)]
    changed = len(filtered) != len(plugins)
    payload["plugins"] = filtered
    return payload, changed


def _legacy_repo_private_install_entry(
    repo_root: Path,
    plugin_name: str,
) -> tuple[Path, dict[str, object] | None, dict[str, object] | None]:
    marketplace_path = _legacy_repo_private_marketplace_path(repo_root)
    if not marketplace_path.is_file():
        return marketplace_path, None, None
    payload = _load_json(marketplace_path)
    plugins = payload.get("plugins", [])
    if not isinstance(plugins, list):
        return marketplace_path, payload, None
    for item in plugins:
        if not isinstance(item, dict) or item.get("name") != plugin_name:
            continue
        source = item.get("source")
        if not isinstance(source, dict):
            continue
        path = source.get("path")
        if path == f"./.codex/plugins/{plugin_name}":
            return marketplace_path, payload, item
    return marketplace_path, payload, None


def _legacy_repo_private_surface_paths(repo_root: Path, plugin_name: str) -> tuple[Path, Path]:
    return _legacy_repo_private_plugin_root(repo_root, plugin_name), _legacy_repo_private_marketplace_path(repo_root)


def codex_config_path(config_override: str | None = None) -> Path:
    if config_override is not None:
        return Path(config_override).expanduser().resolve()
    return (_resolve_home() / CODEX_CONFIG_RELATIVE_PATH).resolve()


def scope_codex_config_path(scope: str, repo_root: Path | None, config_override: str | None = None) -> Path:
    if config_override is not None:
        return Path(config_override).expanduser().resolve()
    return (_resolve_home() / CODEX_CONFIG_RELATIVE_PATH).resolve()


def plugin_config_key(plugin_name: str, marketplace_name: str) -> str:
    return f"{plugin_name}@{marketplace_name}"


def _run_codex_app_server_request(method: str, params: dict[str, object]) -> tuple[dict[str, object] | None, str | None]:
    codex_binary = shutil.which("codex")
    if codex_binary is None:
        return None, "Codex CLI is not available on PATH, so app-server plugin sync was skipped."

    payload = "\n".join(
        [
            json.dumps(
                {
                    "method": "initialize",
                    "id": 1,
                    "params": {
                        "clientInfo": {
                            "name": "agent-plugin-skills",
                            "title": "Agent Plugin Skills",
                            "version": "0.4.9",
                        }
                    },
                }
            ),
            json.dumps({"method": "initialized", "params": {}}),
            json.dumps({"method": method, "id": 2, "params": params}),
            "",
        ]
    )

    try:
        completed = subprocess.run(
            [codex_binary, "app-server"],
            input=payload,
            capture_output=True,
            text=True,
            check=False,
            timeout=CODEX_APP_SERVER_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None, f"Codex app-server did not answer `{method}` within {CODEX_APP_SERVER_TIMEOUT_SECONDS} seconds."
    except OSError as exc:
        return None, f"Codex app-server could not be started for `{method}`: {exc}"

    for line in completed.stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            message = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if message.get("id") != 2:
            continue
        if "result" in message and isinstance(message["result"], dict):
            return message["result"], None
        if "error" in message and isinstance(message["error"], dict):
            error_message = message["error"].get("message")
            if isinstance(error_message, str) and error_message.strip():
                return None, f"Codex app-server rejected `{method}`: {error_message.strip()}"
            return None, f"Codex app-server rejected `{method}`."

    stderr = completed.stderr.strip()
    if stderr:
        return None, f"Codex app-server did not return a `{method}` response. stderr: {stderr}"
    return None, f"Codex app-server did not return a `{method}` response."


def _read_plugin_state_via_codex_app_server(marketplace_path: Path, plugin_name: str) -> tuple[dict[str, object] | None, str | None]:
    result, error = _run_codex_app_server_request("plugin/list", {"limit": 200})
    if error is not None or result is None:
        return None, error

    marketplaces = result.get("marketplaces")
    if not isinstance(marketplaces, list):
        return None, "Codex app-server returned an unexpected `plugin/list` payload without marketplaces."

    target_marketplace = marketplace_path.resolve()
    for marketplace in marketplaces:
        if not isinstance(marketplace, dict):
            continue
        raw_path = marketplace.get("path")
        if not isinstance(raw_path, str):
            continue
        try:
            resolved_marketplace_path = Path(raw_path).resolve()
        except OSError:
            continue
        if resolved_marketplace_path != target_marketplace:
            continue
        plugins = marketplace.get("plugins")
        if not isinstance(plugins, list):
            return None, "Codex app-server returned marketplace data without a plugin list."
        for plugin in plugins:
            if not isinstance(plugin, dict):
                continue
            if plugin.get("name") == plugin_name:
                return plugin, None
        return None, f"Codex app-server did not find `{plugin_name}` in marketplace `{marketplace_path}`."

    return None, f"Codex app-server did not find marketplace `{marketplace_path}`."


def _install_plugin_via_codex_app_server(marketplace_path: Path, plugin_name: str) -> str | None:
    _result, error = _run_codex_app_server_request(
        "plugin/install",
        {
            "marketplacePath": str(marketplace_path.resolve()),
            "pluginName": plugin_name,
        },
    )
    return error


def _uninstall_plugin_via_codex_app_server(plugin_key: str) -> str | None:
    _result, error = _run_codex_app_server_request(
        "plugin/uninstall",
        {
            "pluginId": plugin_key,
        },
    )
    return error


def _plugin_section_pattern(plugin_key: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?ms)^\[plugins\."{re.escape(plugin_key)}"\]\n(?P<body>(?:^(?!\[).*\n?)*)'
    )


def _find_plugin_section_bounds(text: str, plugin_key: str) -> tuple[int, int] | None:
    lines = text.splitlines(keepends=True)
    target_header = f'[plugins."{plugin_key}"]\n'
    offset = 0
    for index, line in enumerate(lines):
        if line == target_header:
            start = offset
            end_offset = offset + len(line)
            for follow in lines[index + 1 :]:
                if follow.startswith("["):
                    break
                end_offset += len(follow)
            return start, end_offset
        offset += len(line)
    return None


def read_plugin_enabled_state(config_path: Path, plugin_key: str) -> bool | None:
    if not config_path.is_file():
        return None
    text = _read_text(config_path)
    bounds = _find_plugin_section_bounds(text, plugin_key)
    if bounds is None:
        return None
    body = text[bounds[0] : bounds[1]]
    enabled_match = re.search(r"(?m)^\s*enabled\s*=\s*(true|false)\s*$", body)
    if enabled_match is None:
        return None
    return enabled_match.group(1) == "true"


def _replace_or_append_plugin_section(text: str, plugin_key: str, enabled: bool) -> str:
    section_text = f'[plugins."{plugin_key}"]\nenabled = {"true" if enabled else "false"}\n'
    bounds = _find_plugin_section_bounds(text, plugin_key)
    if bounds is not None:
        return text[: bounds[0]] + section_text + text[bounds[1] :]
    stripped = text.rstrip()
    if stripped:
        return stripped + "\n\n" + section_text
    return section_text


def write_plugin_enabled_state(config_path: Path, plugin_key: str, enabled: bool) -> None:
    text = _read_text(config_path) if config_path.is_file() else ""
    updated = _replace_or_append_plugin_section(text, plugin_key, enabled)
    _write_text(config_path, updated)


def remove_plugin_enabled_state(config_path: Path, plugin_key: str) -> bool:
    if not config_path.is_file():
        return False
    text = _read_text(config_path)
    bounds = _find_plugin_section_bounds(text, plugin_key)
    if bounds is None:
        return False
    updated = text[: bounds[0]] + text[bounds[1] :]
    updated = re.sub(r"\n{3,}", "\n\n", updated).lstrip("\n")
    if updated and not updated.endswith("\n"):
        updated += "\n"
    _write_text(config_path, updated)
    return True


def build_verification_steps(
    scope: str,
    target_plugin_root: Path,
    marketplace_path: Path,
    plugin_name: str,
    action: str,
    plugin_key: str | None,
    config_path: Path | None,
    repo_install_tracking: str | None,
) -> list[str]:
    scope_label = "repo" if scope == "repo" else "personal"
    steps = [
        f"Restart Codex after updating {scope_label}-scope plugin wiring.",
        f"Open the plugin directory and verify that `{plugin_name}` appears from the marketplace at `{marketplace_path}`.",
        f"Confirm that Codex resolves the plugin from `{target_plugin_root}` after restart.",
    ]
    if action == "verify":
        steps[0] = f"Use this report to confirm whether the {scope_label}-scope staged plugin tree and marketplace entry still match the source plugin."
    if action in {"enable", "disable"} and plugin_key is not None and config_path is not None:
        steps.append(f"Confirm the plugin config entry `{plugin_key}` now has the intended enabled state in `{config_path}`.")
    if action == "promote":
        steps.append("Confirm the repo-local install surface no longer exposes this plugin if the promote workflow removed that staged install.")
    if scope == "repo" and repo_install_tracking == "tracked":
        steps.append("Treat the repo-scope plugin tree and marketplace change as intentional shared repo state, and commit those changes only if this repository wants repo-local plugin installs synced through git.")
    if scope == "repo" and repo_install_tracking == "local-only":
        steps.append("Treat the repo-scope plugin tree and marketplace change as local dev wiring unless this repository explicitly wants to share it, and avoid committing it by accident.")
    return steps


def _describe_target_materialization(target_plugin_root: Path) -> tuple[str, Path | None]:
    if not target_plugin_root.exists() and not target_plugin_root.is_symlink():
        return "missing", None
    if target_plugin_root.is_symlink():
        try:
            link_target = Path(os.readlink(target_plugin_root))
        except OSError:
            return "broken-symlink", None
        if not link_target.is_absolute():
            link_target = (target_plugin_root.parent / link_target).resolve()
        return "symlink", link_target
    return "copy", None


def _tree_digest(root: Path, *, follow_symlinks: bool = False) -> str:
    digest = hashlib.sha256()

    def visit(path: Path, relative_prefix: str = "") -> None:
        children = sorted(path.iterdir(), key=lambda item: item.name)
        for child in children:
            relative = f"{relative_prefix}/{child.name}" if relative_prefix else child.name
            if child.is_symlink():
                if not follow_symlinks:
                    digest.update(f"symlink:{relative}:".encode("utf-8"))
                    digest.update(os.readlink(child).encode("utf-8"))
                    continue
                resolved = child.resolve()
                if resolved.is_dir():
                    digest.update(f"dir:{relative}".encode("utf-8"))
                    visit(resolved, relative)
                    continue
                if resolved.is_file():
                    digest.update(f"file:{relative}:".encode("utf-8"))
                    digest.update(resolved.read_bytes())
                    continue
                digest.update(f"missing:{relative}".encode("utf-8"))
                continue
            if child.is_dir():
                digest.update(f"dir:{relative}".encode("utf-8"))
                visit(child, relative)
                continue
            if child.is_file():
                digest.update(f"file:{relative}:".encode("utf-8"))
                digest.update(child.read_bytes())

    visit(root)
    return digest.hexdigest()


def _copy_tree_is_stale(source_plugin_root: Path, target_plugin_root: Path) -> bool:
    if _is_same_path(source_plugin_root, target_plugin_root):
        return False
    if not target_plugin_root.exists() or target_plugin_root.is_symlink():
        return False
    return _tree_digest(source_plugin_root, follow_symlinks=True) != _tree_digest(target_plugin_root, follow_symlinks=True)


def _target_matches_install_mode(target_plugin_root: Path, source_plugin_root: Path, install_mode: str) -> bool:
    if _is_same_path(target_plugin_root, source_plugin_root):
        return True
    target_kind, link_target = _describe_target_materialization(target_plugin_root)
    if target_kind == "missing":
        return False
    if install_mode == "copy":
        return target_kind == "copy"
    if install_mode == "symlink":
        return target_kind == "symlink" and link_target is not None and _is_same_path(link_target, source_plugin_root)
    raise ValueError(f"Unsupported install mode: {install_mode}")


def _tracked_tree_blocks_symlink_mode(scope: str, scope_root: Path, target_plugin_root: Path) -> bool:
    if scope != "repo":
        return False
    git_dir = scope_root / ".git"
    if not git_dir.exists():
        return False
    target_relpath = target_plugin_root.absolute().relative_to(scope_root.absolute()).as_posix()
    result = subprocess.run(
        ["git", "-C", str(scope_root), "ls-files", "--", target_relpath],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False
    tracked_paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not tracked_paths:
        return False
    return tracked_paths != [target_relpath]


def _audit_install_surface(
    findings: list[Finding],
    scope: str,
    target_plugin_root: Path,
    marketplace_path: Path,
    source_plugin_root: Path,
    plugin_name: str,
    install_mode: str,
    expected_entry: dict[str, object],
    existing_marketplace: dict[str, object] | None,
    action: str,
    scope_root: Path,
) -> None:
    if action in {"install", "update", "verify", "enable", "disable", "repair"}:
        if install_mode == "symlink" and _tracked_tree_blocks_symlink_mode(scope, scope_root, target_plugin_root):
            findings.append(
                Finding(
                    str(target_plugin_root),
                    "tracked-target-tree-blocks-symlink",
                    "Repo scope symlink mode would replace a git-tracked plugin tree at the staged target path. Use copy mode for this repo, or migrate the tracked tree deliberately before switching to symlink mode.",
                )
            )
        if not target_plugin_root.exists():
            findings.append(Finding(str(target_plugin_root), "missing-target-plugin-root", "Staged plugin path is missing for the chosen scope."))
        elif not _plugin_manifest_path(target_plugin_root).exists():
            findings.append(Finding(str(target_plugin_root), "missing-target-manifest", "Target plugin root exists but does not contain `.codex-plugin/plugin.json`."))
        elif action in {"update", "verify", "enable", "disable", "repair"}:
            target_manifest = load_plugin_manifest(target_plugin_root)
            if infer_plugin_name(target_plugin_root, target_manifest) != plugin_name:
                findings.append(Finding(str(target_plugin_root), "target-plugin-name-mismatch", "Target plugin root does not match the source plugin name."))
        if target_plugin_root.exists() and not _target_matches_install_mode(target_plugin_root, source_plugin_root, install_mode):
            if install_mode == "copy":
                findings.append(Finding(str(target_plugin_root), "stale-target-materialization", "Target plugin root is symlinked, but the requested install mode expects a copied plugin tree."))
            else:
                findings.append(Finding(str(target_plugin_root), "stale-target-materialization", "Target plugin root is not a symlink to the requested source plugin root."))
        if install_mode == "copy" and _copy_tree_is_stale(source_plugin_root, target_plugin_root):
            findings.append(
                Finding(
                    str(target_plugin_root),
                    "stale-target-copy",
                    "Staged plugin copy does not match the current source plugin tree. Run `update` to copy the updated plugin contents into the staged Codex install path.",
                )
            )

        if existing_marketplace is None:
            findings.append(Finding(str(marketplace_path), "missing-marketplace", "Marketplace file is missing for the chosen scope."))
        else:
            plugins = existing_marketplace.get("plugins", [])
            match = None
            if isinstance(plugins, list):
                for item in plugins:
                    if isinstance(item, dict) and item.get("name") == plugin_name:
                        match = item
                        break
            if match is None:
                findings.append(Finding(str(marketplace_path), "missing-marketplace-entry", "Marketplace does not include an entry for this plugin."))
            elif match != expected_entry:
                findings.append(Finding(str(marketplace_path), "stale-marketplace-entry", "Marketplace entry does not match the expected local plugin wiring."))

    if action == "uninstall":
        if not target_plugin_root.exists() and not target_plugin_root.is_symlink():
            findings.append(Finding(str(target_plugin_root), "missing-uninstall-target", "Target plugin root is already absent for the chosen scope."))
        if existing_marketplace is None:
            findings.append(Finding(str(marketplace_path), "missing-marketplace", "Marketplace file is missing for the chosen scope."))
        else:
            plugins = existing_marketplace.get("plugins", [])
            has_entry = isinstance(plugins, list) and any(isinstance(item, dict) and item.get("name") == plugin_name for item in plugins)
            if not has_entry:
                findings.append(Finding(str(marketplace_path), "missing-marketplace-entry", "Marketplace does not include an entry for this plugin."))


def _audit_marketplace_payload(
    findings: list[Finding],
    marketplace_path: Path,
    scope_root: Path,
    existing_marketplace: dict[str, object] | None,
) -> None:
    if existing_marketplace is None:
        return
    plugins = existing_marketplace.get("plugins")
    if not isinstance(plugins, list):
        findings.append(
            Finding(
                str(marketplace_path),
                "invalid-marketplace-plugins",
                "Marketplace file must define a `plugins` array so Codex can load local plugins from this scope.",
            )
        )
        return

    for entry in plugins:
        if not isinstance(entry, dict):
            findings.append(
                Finding(
                    str(marketplace_path),
                    "invalid-marketplace-entry",
                    "Marketplace contains a non-object plugin entry, so Codex may skip the entire marketplace.",
                )
            )
            continue
        name = entry.get("name")
        display_name = name if isinstance(name, str) and name else "<unnamed-plugin>"
        source = entry.get("source")
        if not isinstance(source, dict):
            findings.append(
                Finding(
                    str(marketplace_path),
                    "invalid-marketplace-entry-source",
                    f"Marketplace entry `{display_name}` is missing a valid `source` mapping, so Codex may skip the entire marketplace.",
                )
            )
            continue
        path = source.get("path")
        if not isinstance(path, str):
            findings.append(
                Finding(
                    str(marketplace_path),
                    "invalid-marketplace-entry-source-path",
                    f"Marketplace entry `{display_name}` is missing a string `source.path`, so Codex may skip the entire marketplace.",
                )
            )
            continue
        if not path.startswith("./"):
            findings.append(
                Finding(
                    str(marketplace_path),
                    "invalid-marketplace-entry-source-path-prefix",
                    f"Marketplace entry `{display_name}` must use a `./`-prefixed local source path. Codex may skip the entire marketplace until that entry is repaired.",
                )
            )
            continue
        if path == "./":
            findings.append(
                Finding(
                    str(marketplace_path),
                    "invalid-marketplace-entry-empty-relative-source-path",
                    f"Marketplace entry `{display_name}` points at the marketplace root with `./`, but Codex requires a non-empty local plugin source path and may skip the entire marketplace until that entry is repaired.",
                )
            )
            continue
        resolved = (scope_root / path.removeprefix("./")).resolve()
        try:
            resolved.relative_to(scope_root)
        except ValueError:
            findings.append(
                Finding(
                    str(marketplace_path),
                    "invalid-marketplace-entry-source-path-escapes-root",
                    f"Marketplace entry `{display_name}` resolves outside the chosen scope root, so Codex may skip the entire marketplace until that entry is repaired.",
                )
            )
            continue


def _audit_plugin_config_state(
    findings: list[Finding],
    config_path: Path,
    plugin_key: str,
    desired_enabled: bool,
) -> None:
    state = read_plugin_enabled_state(config_path, plugin_key)
    if state is None:
        findings.append(
            Finding(
                str(config_path),
                "missing-plugin-enabled-state",
                f"Codex config does not include an explicit enabled state for `{plugin_key}`.",
            )
        )
        return
    if state != desired_enabled:
        findings.append(
            Finding(
                str(config_path),
                "stale-plugin-enabled-state",
                f"Codex config has `{plugin_key}` set to `{state}`, but the requested action expects `{desired_enabled}`.",
            )
        )


def audit_install(
    requested_source_root: Path,
    scope: str,
    action: str,
    repo_root: Path | None,
    install_mode: str,
    repo_install_tracking: str | None = None,
    codex_config_override: str | None = None,
) -> tuple[list[Finding], dict[str, object], Path, Path, Path, Path, str | None, list[str]]:
    findings: list[Finding] = []
    errors: list[str] = []
    source_plugin_root = resolve_source_plugin_root(
        requested_source_root,
        allow_repo_root_resolution=action == "verify",
    )
    manifest_path = _plugin_manifest_path(source_plugin_root)
    if not source_plugin_root.exists() or not source_plugin_root.is_dir():
        errors.append("Source plugin root does not exist or is not a directory.")
        fallback = requested_source_root
        return findings, {}, fallback, fallback, fallback, scope_codex_config_path(scope, repo_root, codex_config_override), None, errors
    if not manifest_path.exists():
        errors.append(
            "Source plugin is missing `.codex-plugin/plugin.json`. For mutating actions, `--source-plugin-root` must point at the canonical plugin root itself; repo-root auto-detection is only supported for `verify`."
        )
        fallback = source_plugin_root
        return findings, {}, fallback, fallback, fallback, scope_codex_config_path(scope, repo_root, codex_config_override), None, errors

    manifest = load_plugin_manifest(source_plugin_root)
    plugin_name = infer_plugin_name(source_plugin_root, manifest)
    source_summary = build_source_plugin_summary(requested_source_root, source_plugin_root, manifest, plugin_name)
    for item in source_summary.get("surface_findings", []):
        findings.append(Finding(**item))

    if action == "promote" and scope != "repo":
        errors.append("Promote requires repo scope as the source install surface.")
        fallback = source_plugin_root
        return findings, source_summary, fallback, fallback, fallback, scope_codex_config_path(scope, repo_root, codex_config_override), None, errors

    install_scope = "personal" if action == "promote" else scope
    scope_root, target_plugin_root, marketplace_path = scope_paths(install_scope, plugin_name, repo_root)

    if not _path_within_root(target_plugin_root, scope_root):
        errors.append("Target plugin root resolves outside the chosen scope root.")
        return findings, source_summary, target_plugin_root, marketplace_path, scope_root, scope_codex_config_path(install_scope, repo_root, codex_config_override), None, errors

    existing_marketplace = _load_json(marketplace_path) if marketplace_path.exists() else None
    payload = ensure_marketplace_shape(existing_marketplace, install_scope)
    marketplace_name = marketplace_name_from_payload(payload, install_scope)
    expected_entry = expected_marketplace_entry(scope_root, target_plugin_root, plugin_name, infer_category(manifest))
    relative_path = Path(expected_entry["source"]["path"][2:])
    if expected_entry["source"]["path"].startswith("./") is False:
        findings.append(Finding(str(marketplace_path), "invalid-source-path-prefix", "Marketplace source path must start with `./`."))
    if relative_path.is_absolute():
        findings.append(Finding(str(marketplace_path), "absolute-source-path", "Marketplace source path must remain relative to the marketplace root."))
    _audit_marketplace_payload(findings, marketplace_path, scope_root, existing_marketplace)

    _audit_install_surface(
        findings=findings,
        scope=install_scope,
        target_plugin_root=target_plugin_root,
        marketplace_path=marketplace_path,
        source_plugin_root=source_plugin_root,
        plugin_name=plugin_name,
        install_mode=install_mode,
        expected_entry=expected_entry,
        existing_marketplace=existing_marketplace,
        action=action,
        scope_root=scope_root,
    )

    effective_plugin_key: str | None = plugin_config_key(plugin_name, marketplace_name)
    config_path = scope_codex_config_path(install_scope, repo_root, codex_config_override)

    if action in {"enable", "disable"}:
        _audit_plugin_config_state(findings, config_path, effective_plugin_key, desired_enabled=action == "enable")

    if action in {"install", "update", "verify", "repair", "enable", "disable"}:
        plugin_state, _plugin_state_error = _read_plugin_state_via_codex_app_server(marketplace_path, plugin_name)
        if isinstance(plugin_state, dict) and plugin_state.get("installed") is False:
            findings.append(
                Finding(
                    str(marketplace_path),
                    "missing-plugin-installed-cache",
                    f"Codex still reports `{plugin_name}` as available but not installed in its local plugin cache.",
                )
            )

    if install_scope == "repo" and repo_install_tracking == "tracked" and install_mode == "symlink":
        findings.append(
            Finding(
                str(target_plugin_root),
                "tracked-repo-install-prefers-copy",
                "Repo-scope installs marked as tracked should use copy mode so the staged plugin tree can be shared through git. Symlink mode is local-only.",
            )
        )

    if install_scope == "repo":
        legacy_plugin_root, legacy_marketplace_path = _legacy_repo_private_surface_paths(scope_root, plugin_name)
        legacy_marketplace_path, _legacy_payload, legacy_entry = _legacy_repo_private_install_entry(scope_root, plugin_name)
        if legacy_entry is not None or legacy_plugin_root.exists() or legacy_plugin_root.is_symlink():
            findings.append(
                Finding(
                    str(legacy_marketplace_path),
                    "legacy-repo-private-install-surface",
                    f"Repo still has legacy private install-surface wiring for `{plugin_name}` under `.codex/plugins`. Run `repair` to remove that old repo-private copy and marketplace entry.",
                )
            )

    if action == "promote":
        repo_scope_root, repo_target_plugin_root, repo_marketplace_path = scope_paths("repo", plugin_name, repo_root)
        repo_existing_marketplace = _load_json(repo_marketplace_path) if repo_marketplace_path.exists() else None
        repo_payload = ensure_marketplace_shape(repo_existing_marketplace, "repo")
        repo_expected_entry = expected_marketplace_entry(repo_scope_root, repo_target_plugin_root, plugin_name, infer_category(manifest))
        _audit_install_surface(
            findings=findings,
            scope="repo",
            target_plugin_root=repo_target_plugin_root,
            marketplace_path=repo_marketplace_path,
            source_plugin_root=source_plugin_root,
            plugin_name=plugin_name,
            install_mode=install_mode,
            expected_entry=repo_expected_entry,
            existing_marketplace=repo_existing_marketplace,
            action="verify",
            scope_root=repo_scope_root,
        )
        repo_marketplace_name = marketplace_name_from_payload(repo_payload, "repo")
        repo_plugin_key = plugin_config_key(plugin_name, repo_marketplace_name)
        repo_config_path = scope_codex_config_path("repo", repo_scope_root, codex_config_override)
        if read_plugin_enabled_state(repo_config_path, repo_plugin_key) is None:
            findings.append(
                Finding(
                    str(repo_config_path),
                    "missing-plugin-enabled-state",
                    f"Codex config does not include an explicit enabled state for `{repo_plugin_key}`. Promote will default the personal install to enabled unless you set it first.",
                )
            )

    return findings, source_summary, target_plugin_root, marketplace_path, scope_root, config_path, effective_plugin_key, errors


def _remove_target_path(target_plugin_root: Path) -> None:
    if not target_plugin_root.exists() and not target_plugin_root.is_symlink():
        return
    if target_plugin_root.is_symlink() or target_plugin_root.is_file():
        target_plugin_root.unlink()
        return
    shutil.rmtree(target_plugin_root)


def _copy_plugin_tree(source_plugin_root: Path, target_plugin_root: Path) -> None:
    if _is_same_path(source_plugin_root, target_plugin_root):
        return
    target_plugin_root.parent.mkdir(parents=True, exist_ok=True)
    _remove_target_path(target_plugin_root)
    shutil.copytree(source_plugin_root, target_plugin_root)


def _symlink_plugin_tree(source_plugin_root: Path, target_plugin_root: Path) -> None:
    if _is_same_path(source_plugin_root, target_plugin_root):
        return
    target_plugin_root.parent.mkdir(parents=True, exist_ok=True)
    _remove_target_path(target_plugin_root)
    target_plugin_root.symlink_to(source_plugin_root, target_is_directory=True)


def _install_or_update_target(
    apply_actions: list[dict[str, str]],
    source_plugin_root: Path,
    target_plugin_root: Path,
    install_mode: str,
) -> None:
    if _is_same_path(source_plugin_root, target_plugin_root):
        apply_actions.append(
            {
                "action": "use-existing-plugin-tree",
                "path": str(target_plugin_root),
                "reason": "Source plugin root already matches the staged install target.",
            }
        )
        return
    if install_mode == "copy":
        _copy_plugin_tree(source_plugin_root, target_plugin_root)
        apply_actions.append({"action": "copy-plugin-tree", "path": str(target_plugin_root)})
        return
    if install_mode == "symlink":
        _symlink_plugin_tree(source_plugin_root, target_plugin_root)
        apply_actions.append(
            {
                "action": "symlink-plugin-tree",
                "path": str(target_plugin_root),
                "source": str(source_plugin_root),
            }
        )
        return
    raise ValueError(f"Unsupported install mode: {install_mode}")


def _write_marketplace_entry(
    apply_actions: list[dict[str, str]],
    marketplace_path: Path,
    payload: dict[str, object],
    expected_entry: dict[str, object],
    scope: str,
) -> str:
    payload, changed = merge_marketplace_entry(payload, expected_entry)
    marketplace_name = marketplace_name_from_payload(payload, scope)
    if changed or not marketplace_path.exists():
        _write_json(marketplace_path, payload)
        apply_actions.append({"action": "write-marketplace-entry", "path": str(marketplace_path)})
    return marketplace_name


def apply_install(
    requested_source_root: Path,
    scope: str,
    action: str,
    repo_root: Path | None,
    install_mode: str,
    repo_install_tracking: str | None = None,
    codex_config_override: str | None = None,
) -> tuple[list[dict[str, str]], dict[str, object], Path, Path, Path, str | None, list[str]]:
    apply_actions: list[dict[str, str]] = []
    errors: list[str] = []

    source_plugin_root = resolve_source_plugin_root(
        requested_source_root,
        allow_repo_root_resolution=action == "verify",
    )
    manifest_path = _plugin_manifest_path(source_plugin_root)
    if not source_plugin_root.exists() or not source_plugin_root.is_dir():
        errors.append("Source plugin root does not exist or is not a directory.")
        fallback = requested_source_root
        return apply_actions, {}, fallback, fallback, scope_codex_config_path(scope, repo_root, codex_config_override), None, errors
    if not manifest_path.exists():
        errors.append(
            "Source plugin is missing `.codex-plugin/plugin.json`. For mutating actions, `--source-plugin-root` must point at the canonical plugin root itself; repo-root auto-detection is only supported for `verify`."
        )
        fallback = source_plugin_root
        return apply_actions, {}, fallback, fallback, scope_codex_config_path(scope, repo_root, codex_config_override), None, errors

    manifest = load_plugin_manifest(source_plugin_root)
    plugin_name = infer_plugin_name(source_plugin_root, manifest)
    source_summary = build_source_plugin_summary(requested_source_root, source_plugin_root, manifest, plugin_name)

    if action == "promote" and scope != "repo":
        errors.append("Promote requires repo scope as the source install surface.")
        fallback = source_plugin_root
        return apply_actions, source_summary, fallback, fallback, scope_codex_config_path(scope, repo_root, codex_config_override), None, errors

    install_scope = "personal" if action == "promote" else scope
    scope_root, target_plugin_root, marketplace_path = scope_paths(install_scope, plugin_name, repo_root)
    existing_marketplace = _load_json(marketplace_path) if marketplace_path.exists() else None
    payload = ensure_marketplace_shape(existing_marketplace, install_scope)
    expected_entry = expected_marketplace_entry(scope_root, target_plugin_root, plugin_name, infer_category(manifest))
    marketplace_name = marketplace_name_from_payload(payload, install_scope)
    config_path = scope_codex_config_path(install_scope, repo_root, codex_config_override)
    plugin_key: str | None = plugin_config_key(plugin_name, marketplace_name)

    if action in {"install", "update", "repair"}:
        if install_scope == "repo" and repo_install_tracking == "tracked" and install_mode == "symlink":
            errors.append("Repo scope installs marked as tracked must use copy mode so the staged plugin tree can be shared through git. Symlink mode is local-only.")
            return apply_actions, source_summary, target_plugin_root, marketplace_path, config_path, plugin_key, errors
        if install_mode == "symlink" and _tracked_tree_blocks_symlink_mode(install_scope, scope_root, target_plugin_root):
            errors.append("Repo scope symlink mode is blocked because the staged target path is a git-tracked plugin tree. Use copy mode for this repo, or migrate the tracked tree deliberately before switching to symlink mode.")
            return apply_actions, source_summary, target_plugin_root, marketplace_path, config_path, plugin_key, errors
        try:
            _install_or_update_target(apply_actions, source_plugin_root, target_plugin_root, install_mode)
        except ValueError as exc:
            errors.append(str(exc))
            return apply_actions, source_summary, target_plugin_root, marketplace_path, config_path, plugin_key, errors
        payload, changed = merge_marketplace_entry(payload, expected_entry)
        marketplace_name = marketplace_name_from_payload(payload, install_scope)
        plugin_key = plugin_config_key(plugin_name, marketplace_name)
        if changed or not marketplace_path.exists():
            _write_json(marketplace_path, payload)
            apply_actions.append({"action": "write-marketplace-entry", "path": str(marketplace_path)})
        if action == "install" and plugin_key is not None:
            write_plugin_enabled_state(config_path, plugin_key, True)
            apply_actions.append(
                {"action": "write-plugin-enabled-state", "path": str(config_path), "plugin_key": plugin_key, "enabled": "true"}
            )
        install_error = _install_plugin_via_codex_app_server(marketplace_path, plugin_name)
        if install_error is None:
            apply_actions.append(
                {
                    "action": "codex-plugin-install",
                    "path": str(marketplace_path),
                    "plugin_name": plugin_name,
                }
            )
        else:
            apply_actions.append(
                {
                    "action": "codex-plugin-install-fallback",
                    "path": str(marketplace_path),
                    "plugin_name": plugin_name,
                    "message": install_error,
                }
            )
        if install_scope == "repo":
            legacy_plugin_root, legacy_marketplace_path = _legacy_repo_private_surface_paths(scope_root, plugin_name)
            legacy_marketplace_path, legacy_payload, legacy_entry = _legacy_repo_private_install_entry(scope_root, plugin_name)
            if legacy_plugin_root.exists() or legacy_plugin_root.is_symlink():
                _remove_target_path(legacy_plugin_root)
                apply_actions.append({"action": "remove-legacy-repo-private-plugin-tree", "path": str(legacy_plugin_root)})
            if legacy_payload is not None and legacy_entry is not None:
                legacy_payload, legacy_changed = remove_marketplace_entry(legacy_payload, plugin_name)
                if legacy_changed:
                    _write_json(legacy_marketplace_path, legacy_payload)
                    apply_actions.append({"action": "remove-legacy-repo-private-marketplace-entry", "path": str(legacy_marketplace_path)})

    elif action == "uninstall":
        if plugin_key is not None:
            uninstall_error = _uninstall_plugin_via_codex_app_server(plugin_key)
            if uninstall_error is None:
                apply_actions.append({"action": "codex-plugin-uninstall", "plugin_key": plugin_key})
            else:
                apply_actions.append(
                    {
                        "action": "codex-plugin-uninstall-fallback",
                        "plugin_key": plugin_key,
                        "message": uninstall_error,
                    }
                )
        if target_plugin_root.exists() or target_plugin_root.is_symlink():
            _remove_target_path(target_plugin_root)
            apply_actions.append({"action": "uninstall-plugin-tree", "path": str(target_plugin_root)})
        payload, changed = remove_marketplace_entry(payload, plugin_name)
        if changed:
            _write_json(marketplace_path, payload)
            apply_actions.append({"action": "uninstall-marketplace-entry", "path": str(marketplace_path)})
        if install_scope == "repo":
            legacy_plugin_root, legacy_marketplace_path = _legacy_repo_private_surface_paths(scope_root, plugin_name)
            if legacy_plugin_root.exists() or legacy_plugin_root.is_symlink():
                _remove_target_path(legacy_plugin_root)
                apply_actions.append({"action": "remove-legacy-repo-private-plugin-tree", "path": str(legacy_plugin_root)})
            legacy_marketplace_path, legacy_payload, legacy_entry = _legacy_repo_private_install_entry(scope_root, plugin_name)
            if legacy_payload is not None and legacy_entry is not None:
                legacy_payload, legacy_changed = remove_marketplace_entry(legacy_payload, plugin_name)
                if legacy_changed:
                    _write_json(legacy_marketplace_path, legacy_payload)
                    apply_actions.append({"action": "remove-legacy-repo-private-marketplace-entry", "path": str(legacy_marketplace_path)})
        if plugin_key is not None and remove_plugin_enabled_state(config_path, plugin_key):
            apply_actions.append({"action": "remove-plugin-enabled-state", "path": str(config_path), "plugin_key": plugin_key})

    elif action == "enable":
        write_plugin_enabled_state(config_path, plugin_key, True)
        apply_actions.append({"action": "write-plugin-enabled-state", "path": str(config_path), "plugin_key": plugin_key, "enabled": "true"})

    elif action == "disable":
        write_plugin_enabled_state(config_path, plugin_key, False)
        apply_actions.append({"action": "write-plugin-enabled-state", "path": str(config_path), "plugin_key": plugin_key, "enabled": "false"})

    elif action == "promote":
        repo_scope_root, repo_target_plugin_root, repo_marketplace_path = scope_paths("repo", plugin_name, repo_root)
        repo_existing_marketplace = _load_json(repo_marketplace_path) if repo_marketplace_path.exists() else None
        repo_payload = ensure_marketplace_shape(repo_existing_marketplace, "repo")
        repo_marketplace_name = marketplace_name_from_payload(repo_payload, "repo")
        repo_plugin_key = plugin_config_key(plugin_name, repo_marketplace_name)
        repo_config_path = scope_codex_config_path("repo", repo_scope_root, codex_config_override)
        repo_enabled_state = read_plugin_enabled_state(repo_config_path, repo_plugin_key)

        if install_mode == "symlink" and _tracked_tree_blocks_symlink_mode("personal", _resolve_home(), target_plugin_root):
            errors.append("Personal scope symlink mode is blocked by the current staged target path.")
            return apply_actions, source_summary, target_plugin_root, marketplace_path, config_path, plugin_key, errors

        try:
            _install_or_update_target(apply_actions, source_plugin_root, target_plugin_root, install_mode)
        except ValueError as exc:
            errors.append(str(exc))
            return apply_actions, source_summary, target_plugin_root, marketplace_path, config_path, plugin_key, errors

        payload, changed = merge_marketplace_entry(payload, expected_entry)
        marketplace_name = marketplace_name_from_payload(payload, "personal")
        plugin_key = plugin_config_key(plugin_name, marketplace_name)
        if changed or not marketplace_path.exists():
            _write_json(marketplace_path, payload)
            apply_actions.append({"action": "write-marketplace-entry", "path": str(marketplace_path)})

        write_plugin_enabled_state(config_path, plugin_key, True if repo_enabled_state is None else repo_enabled_state)
        apply_actions.append(
            {
                "action": "write-plugin-enabled-state",
                "path": str(config_path),
                "plugin_key": plugin_key,
                "enabled": "true" if repo_enabled_state is None else ("true" if repo_enabled_state else "false"),
            }
        )
        install_error = _install_plugin_via_codex_app_server(marketplace_path, plugin_name)
        if install_error is None:
            apply_actions.append(
                {
                    "action": "codex-plugin-install",
                    "path": str(marketplace_path),
                    "plugin_name": plugin_name,
                }
            )
        else:
            apply_actions.append(
                {
                    "action": "codex-plugin-install-fallback",
                    "path": str(marketplace_path),
                    "plugin_name": plugin_name,
                    "message": install_error,
                }
            )

        if repo_target_plugin_root.exists() or repo_target_plugin_root.is_symlink():
            _remove_target_path(repo_target_plugin_root)
            apply_actions.append({"action": "uninstall-plugin-tree", "path": str(repo_target_plugin_root)})
        if repo_existing_marketplace is not None:
            repo_payload, repo_changed = remove_marketplace_entry(repo_payload, plugin_name)
            if repo_changed:
                _write_json(repo_marketplace_path, repo_payload)
                apply_actions.append({"action": "uninstall-marketplace-entry", "path": str(repo_marketplace_path)})
        if remove_plugin_enabled_state(repo_config_path, repo_plugin_key):
            apply_actions.append({"action": "remove-plugin-enabled-state", "path": str(repo_config_path), "plugin_key": repo_plugin_key})
        legacy_plugin_root, legacy_marketplace_path = _legacy_repo_private_surface_paths(repo_scope_root, plugin_name)
        if legacy_plugin_root.exists() or legacy_plugin_root.is_symlink():
            _remove_target_path(legacy_plugin_root)
            apply_actions.append({"action": "remove-legacy-repo-private-plugin-tree", "path": str(legacy_plugin_root)})
        legacy_marketplace_path, legacy_payload, legacy_entry = _legacy_repo_private_install_entry(repo_scope_root, plugin_name)
        if legacy_payload is not None and legacy_entry is not None:
            legacy_payload, legacy_changed = remove_marketplace_entry(legacy_payload, plugin_name)
            if legacy_changed:
                _write_json(legacy_marketplace_path, legacy_payload)
                apply_actions.append({"action": "remove-legacy-repo-private-marketplace-entry", "path": str(legacy_marketplace_path)})

    elif action == "verify":
        pass

    else:
        errors.append(f"Unsupported action: {action}")

    return apply_actions, source_summary, target_plugin_root, marketplace_path, config_path, plugin_key, errors


def build_report(
    source_plugin: dict[str, object],
    scope: str,
    action: str,
    run_mode: str,
    install_mode: str,
    repo_install_tracking: str | None,
    target_plugin_root: Path,
    marketplace_path: Path,
    config_path: str,
    scope_source: str,
    repo_install_tracking_source: str,
    plugin_config_key_name: str | None,
    findings: list[Finding],
    apply_actions: list[dict[str, str]],
    errors: list[str],
) -> dict[str, object]:
    restart_required = run_mode == "apply" and bool(apply_actions)
    return {
        "run_context": {
            "run_mode": run_mode,
            "config_path": config_path,
            "scope_source": scope_source,
            "repo_install_tracking_source": repo_install_tracking_source,
        },
        "scope": scope,
        "action": action,
        "install_mode": install_mode,
        "repo_install_tracking": repo_install_tracking,
        "source_plugin": source_plugin,
        "target_plugin_root": str(target_plugin_root),
        "marketplace_path": str(marketplace_path),
        "codex_config_path": config_path,
        "plugin_config_key": plugin_config_key_name,
        "findings": [asdict(item) for item in findings],
        "apply_actions": apply_actions,
        "restart_required": restart_required,
        "verification_steps": build_verification_steps(
            scope=scope,
            target_plugin_root=target_plugin_root,
            marketplace_path=marketplace_path,
            plugin_name=str(source_plugin.get("name", "")),
            action=action,
            plugin_key=plugin_config_key_name,
            config_path=Path(config_path),
            repo_install_tracking=repo_install_tracking,
        ),
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit and apply local Codex plugin install wiring at repo or personal scope"
    )
    parser.add_argument("--source-plugin-root", required=True)
    parser.add_argument("--scope", choices=("repo", "personal"))
    parser.add_argument("--action", choices=("install", "update", "uninstall", "verify", "repair", "enable", "disable", "promote"), required=True)
    parser.add_argument("--run-mode", choices=("check-only", "apply"), required=True)
    parser.add_argument("--repo-root")
    parser.add_argument("--config")
    parser.add_argument("--codex-config-path")
    parser.add_argument("--install-mode", choices=("copy", "symlink"), default=DEFAULT_INSTALL_MODE)
    parser.add_argument("--repo-install-tracking", choices=("tracked", "local-only"))
    parser.add_argument("--print-md", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested_source_root = Path(args.source_plugin_root).resolve()
    project_root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd().resolve()
    scope, scope_context, scope_errors = resolve_scope(args.scope, project_root, args.config)
    repo_install_tracking, repo_install_tracking_source, tracking_errors = resolve_repo_install_tracking(
        args.repo_install_tracking,
        scope,
        scope_context,
    )
    repo_root = project_root if scope == "repo" else (Path(args.repo_root).resolve() if args.repo_root else None)

    findings, source_summary, target_plugin_root, marketplace_path, _scope_root, config_path, plugin_key, errors = audit_install(
        requested_source_root=requested_source_root,
        scope=scope,
        action=args.action,
        repo_root=repo_root,
        install_mode=args.install_mode,
        repo_install_tracking=repo_install_tracking,
        codex_config_override=args.codex_config_path,
    )
    errors.extend(scope_errors)
    errors.extend(tracking_errors)

    apply_actions: list[dict[str, str]] = []
    if not errors and args.run_mode == "apply":
        apply_actions, source_summary, target_plugin_root, marketplace_path, config_path, plugin_key, apply_errors = apply_install(
            requested_source_root=requested_source_root,
            scope=scope,
            action=args.action,
            repo_root=repo_root,
            install_mode=args.install_mode,
            repo_install_tracking=repo_install_tracking,
            codex_config_override=args.codex_config_path,
        )
        errors.extend(apply_errors)
        findings, source_summary, target_plugin_root, marketplace_path, _scope_root, config_path, plugin_key, post_errors = audit_install(
            requested_source_root=requested_source_root,
            scope=scope,
            action=args.action,
            repo_root=repo_root,
            install_mode=args.install_mode,
            repo_install_tracking=repo_install_tracking,
            codex_config_override=args.codex_config_path,
        )
        errors.extend(post_errors)

    report = build_report(
        source_plugin=source_summary,
        scope="personal" if args.action == "promote" else scope,
        action=args.action,
        run_mode=args.run_mode,
        install_mode=args.install_mode,
        repo_install_tracking=repo_install_tracking,
        target_plugin_root=target_plugin_root,
        marketplace_path=marketplace_path,
        config_path=str(config_path),
        scope_source=str(scope_context.get("source", "default")),
        repo_install_tracking_source=repo_install_tracking_source,
        plugin_config_key_name=plugin_key,
        findings=findings,
        apply_actions=apply_actions,
        errors=errors,
    )
    if args.print_md and not findings and not apply_actions and not errors:
        print(EXACT_NO_FINDINGS)
    else:
        print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
