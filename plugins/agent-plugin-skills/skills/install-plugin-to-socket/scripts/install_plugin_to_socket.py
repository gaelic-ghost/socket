from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path


EXACT_NO_FINDINGS = "No findings."


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


def _pretty_plugin_title(name: str) -> str:
    return name.replace("-", " ").title()


def _relative_to_root(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def _path_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def load_plugin_manifest(source_plugin_root: Path) -> dict[str, object]:
    manifest_path = source_plugin_root / ".codex-plugin" / "plugin.json"
    return _load_json(manifest_path)


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


def build_source_plugin_summary(source_plugin_root: Path, manifest: dict[str, object], plugin_name: str) -> dict[str, object]:
    return {
        "source_root": str(source_plugin_root),
        "manifest_path": str(source_plugin_root / ".codex-plugin" / "plugin.json"),
        "name": plugin_name,
        "version": manifest.get("version", "unknown"),
        "description": manifest.get("description", ""),
        "category": infer_category(manifest),
    }


def scope_paths(scope: str, plugin_name: str, repo_root: Path | None) -> tuple[Path, Path, Path]:
    if scope == "repo":
        if repo_root is None:
            raise ValueError("Repository root is required for repo scope.")
        scope_root = repo_root.resolve()
        target_plugin_root = scope_root / "plugins" / plugin_name
        marketplace_path = scope_root / ".agents" / "plugins" / "marketplace.json"
        return scope_root, target_plugin_root, marketplace_path
    if scope == "personal":
        scope_root = _resolve_home()
        target_plugin_root = scope_root / ".codex" / "plugins" / plugin_name
        marketplace_path = scope_root / ".agents" / "plugins" / "marketplace.json"
        return scope_root, target_plugin_root, marketplace_path
    raise ValueError(f"Unsupported scope: {scope}")


def expected_marketplace_entry(scope: str, scope_root: Path, target_plugin_root: Path, plugin_name: str, category: str) -> dict[str, object]:
    relative_path = "./" + _relative_to_root(target_plugin_root, scope_root)
    entry: dict[str, object] = {
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
    return entry


def expected_marketplace_name(scope: str, plugin_name: str) -> str:
    if scope == "repo":
        return "local-repo"
    return f"{plugin_name}-personal-local"


def ensure_marketplace_shape(existing: dict[str, object] | None, scope: str, plugin_name: str) -> dict[str, object]:
    if existing is None:
        return {
            "name": expected_marketplace_name(scope, plugin_name),
            "interface": {
                "displayName": _pretty_plugin_title(expected_marketplace_name(scope, plugin_name)),
            },
            "plugins": [],
        }
    payload = dict(existing)
    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        payload["plugins"] = []
    return payload


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


def build_verification_steps(scope: str, target_plugin_root: Path, marketplace_path: Path, plugin_name: str) -> list[str]:
    scope_label = "repo" if scope == "repo" else "personal"
    return [
        f"Restart Codex after updating {scope_label}-scope plugin wiring.",
        f"Open the plugin directory and verify that `{plugin_name}` appears from the marketplace at `{marketplace_path}`.",
        f"Confirm that Codex resolves the plugin from `{target_plugin_root}` after restart.",
    ]


def audit_install(
    source_plugin_root: Path,
    scope: str,
    action: str,
    repo_root: Path | None,
) -> tuple[list[Finding], dict[str, object], Path, Path, Path, list[str]]:
    findings: list[Finding] = []
    errors: list[str] = []
    manifest_path = source_plugin_root / ".codex-plugin" / "plugin.json"
    if not source_plugin_root.exists() or not source_plugin_root.is_dir():
        errors.append("Source plugin root does not exist or is not a directory.")
        return findings, {}, source_plugin_root, source_plugin_root, source_plugin_root, errors
    if not manifest_path.exists():
        errors.append("Source plugin is missing `.codex-plugin/plugin.json`.")
        return findings, {}, source_plugin_root, source_plugin_root, source_plugin_root, errors

    manifest = load_plugin_manifest(source_plugin_root)
    plugin_name = infer_plugin_name(source_plugin_root, manifest)
    source_summary = build_source_plugin_summary(source_plugin_root, manifest, plugin_name)
    scope_root, target_plugin_root, marketplace_path = scope_paths(scope, plugin_name, repo_root)

    if not _path_within_root(target_plugin_root, scope_root):
        errors.append("Target plugin root resolves outside the chosen scope root.")
        return findings, source_summary, target_plugin_root, marketplace_path, scope_root, errors

    expected_entry = expected_marketplace_entry(scope, scope_root, target_plugin_root, plugin_name, infer_category(manifest))
    relative_path = Path(expected_entry["source"]["path"][2:])
    if expected_entry["source"]["path"].startswith("./") is False:
        findings.append(Finding(str(marketplace_path), "invalid-source-path-prefix", "Marketplace source path must start with `./`."))
    if relative_path.is_absolute():
        findings.append(Finding(str(marketplace_path), "absolute-source-path", "Marketplace source path must remain relative to the marketplace root."))

    existing_marketplace = _load_json(marketplace_path) if marketplace_path.exists() else None

    if action in {"install", "refresh"}:
        if not target_plugin_root.exists():
            findings.append(Finding(str(target_plugin_root), "missing-target-plugin-root", "Local plugin copy is missing for the chosen scope."))
        elif not (target_plugin_root / ".codex-plugin" / "plugin.json").exists():
            findings.append(Finding(str(target_plugin_root), "missing-target-manifest", "Target plugin root exists but does not contain `.codex-plugin/plugin.json`."))
        elif action == "refresh":
            target_manifest = load_plugin_manifest(target_plugin_root)
            if infer_plugin_name(target_plugin_root, target_manifest) != plugin_name:
                findings.append(Finding(str(target_plugin_root), "target-plugin-name-mismatch", "Target plugin root does not match the source plugin name."))

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

    if action == "detach":
        if not target_plugin_root.exists():
            findings.append(Finding(str(target_plugin_root), "missing-detach-target", "Target plugin root is already absent for the chosen scope."))
        if existing_marketplace is None:
            findings.append(Finding(str(marketplace_path), "missing-marketplace", "Marketplace file is missing for the chosen scope."))
        else:
            plugins = existing_marketplace.get("plugins", [])
            has_entry = isinstance(plugins, list) and any(isinstance(item, dict) and item.get("name") == plugin_name for item in plugins)
            if not has_entry:
                findings.append(Finding(str(marketplace_path), "missing-marketplace-entry", "Marketplace does not include an entry for this plugin."))

    return findings, source_summary, target_plugin_root, marketplace_path, scope_root, errors


def _copy_plugin_tree(source_plugin_root: Path, target_plugin_root: Path) -> None:
    if source_plugin_root.resolve() == target_plugin_root.resolve():
        return
    target_plugin_root.parent.mkdir(parents=True, exist_ok=True)
    if target_plugin_root.exists():
        shutil.rmtree(target_plugin_root)
    shutil.copytree(source_plugin_root, target_plugin_root)


def apply_install(
    source_plugin_root: Path,
    scope: str,
    action: str,
    repo_root: Path | None,
) -> tuple[list[dict[str, str]], dict[str, object], Path, Path, list[str]]:
    apply_actions: list[dict[str, str]] = []
    errors: list[str] = []

    manifest = load_plugin_manifest(source_plugin_root)
    plugin_name = infer_plugin_name(source_plugin_root, manifest)
    source_summary = build_source_plugin_summary(source_plugin_root, manifest, plugin_name)
    scope_root, target_plugin_root, marketplace_path = scope_paths(scope, plugin_name, repo_root)
    expected_entry = expected_marketplace_entry(scope, scope_root, target_plugin_root, plugin_name, infer_category(manifest))

    existing_marketplace = _load_json(marketplace_path) if marketplace_path.exists() else None
    payload = ensure_marketplace_shape(existing_marketplace, scope, plugin_name)

    if action in {"install", "refresh"}:
        if source_plugin_root.resolve() == target_plugin_root.resolve():
            apply_actions.append(
                {
                    "action": "use-existing-plugin-tree",
                    "path": str(target_plugin_root),
                    "reason": "Source plugin root already matches the repo-scoped install target.",
                }
            )
        else:
            _copy_plugin_tree(source_plugin_root, target_plugin_root)
            apply_actions.append({"action": "copy-plugin-tree", "path": str(target_plugin_root)})
        payload, changed = merge_marketplace_entry(payload, expected_entry)
        if changed or not marketplace_path.exists():
            _write_json(marketplace_path, payload)
            apply_actions.append({"action": "write-marketplace-entry", "path": str(marketplace_path)})
    elif action == "detach":
        if target_plugin_root.exists():
            shutil.rmtree(target_plugin_root)
            apply_actions.append({"action": "remove-plugin-tree", "path": str(target_plugin_root)})
        payload, changed = remove_marketplace_entry(payload, plugin_name)
        if changed:
            _write_json(marketplace_path, payload)
            apply_actions.append({"action": "remove-marketplace-entry", "path": str(marketplace_path)})
    else:
        errors.append(f"Unsupported action: {action}")

    return apply_actions, source_summary, target_plugin_root, marketplace_path, errors


def build_report(
    source_plugin: dict[str, object],
    scope: str,
    action: str,
    run_mode: str,
    target_plugin_root: Path,
    marketplace_path: Path,
    findings: list[Finding],
    apply_actions: list[dict[str, str]],
    errors: list[str],
) -> dict[str, object]:
    restart_required = run_mode == "apply" and bool(apply_actions)
    return {
        "run_context": {
            "run_mode": run_mode,
        },
        "scope": scope,
        "action": action,
        "source_plugin": source_plugin,
        "target_plugin_root": str(target_plugin_root),
        "marketplace_path": str(marketplace_path),
        "findings": [asdict(item) for item in findings],
        "apply_actions": apply_actions,
        "restart_required": restart_required,
        "verification_steps": build_verification_steps(scope, target_plugin_root, marketplace_path, str(source_plugin.get("name", ""))),
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit and apply local Codex plugin install wiring at repo or personal scope"
    )
    parser.add_argument("--source-plugin-root", required=True)
    parser.add_argument("--scope", choices=("repo", "personal"), required=True)
    parser.add_argument("--action", choices=("install", "refresh", "detach"), required=True)
    parser.add_argument("--run-mode", choices=("check-only", "apply"), required=True)
    parser.add_argument("--repo-root")
    parser.add_argument("--print-md", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_plugin_root = Path(args.source_plugin_root).resolve()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else None

    findings, source_summary, target_plugin_root, marketplace_path, _scope_root, errors = audit_install(
        source_plugin_root=source_plugin_root,
        scope=args.scope,
        action=args.action,
        repo_root=repo_root,
    )

    apply_actions: list[dict[str, str]] = []
    if not errors and args.run_mode == "apply":
        apply_actions, source_summary, target_plugin_root, marketplace_path, apply_errors = apply_install(
            source_plugin_root=source_plugin_root,
            scope=args.scope,
            action=args.action,
            repo_root=repo_root,
        )
        errors.extend(apply_errors)
        findings, source_summary, target_plugin_root, marketplace_path, _scope_root, post_errors = audit_install(
            source_plugin_root=source_plugin_root,
            scope=args.scope,
            action=args.action,
            repo_root=repo_root,
        )
        errors.extend(post_errors)

    report = build_report(
        source_plugin=source_summary,
        scope=args.scope,
        action=args.action,
        run_mode=args.run_mode,
        target_plugin_root=target_plugin_root,
        marketplace_path=marketplace_path,
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
