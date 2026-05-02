#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Clean up pre-Git-marketplace socket plugin install artifacts."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


KNOWN_SOCKET_PLUGINS = {
    "agent-plugin-skills",
    "apple-dev-skills",
    "cardhop-app",
    "dotnet-skills",
    "productivity-skills",
    "python-skills",
    "rust-skills",
    "speak-swiftly-server",
    "spotify",
    "things-app",
    "web-dev-skills",
}

CANONICAL_MARKETPLACE_NAMES = KNOWN_SOCKET_PLUGINS | {"socket"}


@dataclass(frozen=True)
class PlannedAction:
    kind: str
    target: Path
    description: str


@dataclass(frozen=True)
class RewriteMarketplace:
    path: Path
    data: dict[str, Any] | None
    removed_names: tuple[str, ...]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Cannot inspect legacy marketplace because JSON is invalid at "
            f"{path}:{exc.lineno}:{exc.colno}: {exc.msg}"
        ) from exc


def plugin_name_from_manifest(plugin_root: Path) -> str | None:
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        return None
    name = manifest.get("name")
    if isinstance(name, str):
        return name
    return None


def is_legacy_socket_plugin_dir(path: Path) -> bool:
    if not path.is_dir():
        return False
    if "cache" in path.parts:
        return False
    return plugin_name_from_manifest(path) in KNOWN_SOCKET_PLUGINS


def is_legacy_socket_marketplace_entry(entry: object) -> bool:
    if not isinstance(entry, dict):
        return False
    name = entry.get("name")
    if name not in KNOWN_SOCKET_PLUGINS:
        return False
    source = entry.get("source")
    if isinstance(source, str):
        return source.startswith("./") or source.startswith("/") or source.startswith("~")
    if not isinstance(source, dict):
        return False
    if source.get("source") != "local":
        return False
    path = source.get("path")
    return isinstance(path, str) and (
        path.startswith("./") or path.startswith("/") or path.startswith("~")
    )


def plan_marketplace_cleanup(personal_marketplace: Path) -> RewriteMarketplace | None:
    marketplace = load_json(personal_marketplace)
    if marketplace is None:
        return None
    if not isinstance(marketplace, dict):
        raise SystemExit(
            f"Cannot inspect legacy marketplace because it is not a JSON object: "
            f"{personal_marketplace}"
        )

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        return None

    kept: list[object] = []
    removed: list[str] = []
    for entry in plugins:
        if is_legacy_socket_marketplace_entry(entry):
            name = entry.get("name") if isinstance(entry, dict) else None
            removed.append(str(name))
        else:
            kept.append(entry)

    if not removed:
        return None

    if not kept and marketplace.get("name") == "socket":
        return RewriteMarketplace(personal_marketplace, None, tuple(sorted(removed)))

    rewritten = dict(marketplace)
    rewritten["plugins"] = kept
    return RewriteMarketplace(personal_marketplace, rewritten, tuple(sorted(removed)))


def plan_plugin_dir_cleanup(codex_plugins_root: Path) -> list[PlannedAction]:
    actions: list[PlannedAction] = []
    for plugin_name in sorted(KNOWN_SOCKET_PLUGINS):
        plugin_dir = codex_plugins_root / plugin_name
        if is_legacy_socket_plugin_dir(plugin_dir):
            actions.append(
                PlannedAction(
                    kind="remove-directory",
                    target=plugin_dir,
                    description=(
                        f"Remove copied legacy plugin payload `{plugin_name}` from "
                        f"{plugin_dir}"
                    ),
                )
            )
    return actions


def stale_config_plugin_tables(config_path: Path) -> list[str]:
    if not config_path.is_file():
        return []
    stale_tables: list[str] = []
    for line in config_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("[plugins.") or not stripped.endswith("]"):
            continue
        table_name = stripped.removeprefix("[plugins.").removesuffix("]").strip('"')
        if "@" not in table_name:
            continue
        plugin_name, marketplace_name = table_name.rsplit("@", 1)
        if (
            plugin_name in KNOWN_SOCKET_PLUGINS
            and marketplace_name not in CANONICAL_MARKETPLACE_NAMES
        ):
            stale_tables.append(table_name)
    return stale_tables


def backup_path_for(target: Path, *, home: Path, backup_root: Path) -> Path:
    try:
        relative = target.resolve().relative_to(home.resolve())
    except ValueError:
        relative = Path(target.name)
    return backup_root / relative


def backup_target(target: Path, *, home: Path, backup_root: Path) -> Path:
    destination = backup_path_for(target, home=home, backup_root=backup_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if target.is_dir():
        shutil.copytree(target, destination)
    else:
        shutil.copy2(target, destination)
    return destination


def apply_marketplace_rewrite(rewrite: RewriteMarketplace, *, home: Path, backup_root: Path) -> None:
    backup_target(rewrite.path, home=home, backup_root=backup_root)
    if rewrite.data is None:
        rewrite.path.unlink()
        return
    rewrite.path.write_text(json.dumps(rewrite.data, indent=2) + "\n", encoding="utf-8")


def apply_action(action: PlannedAction, *, home: Path, backup_root: Path) -> None:
    backup_target(action.target, home=home, backup_root=backup_root)
    if action.kind == "remove-directory":
        shutil.rmtree(action.target)
        return
    raise AssertionError(f"Unsupported action kind: {action.kind}")


def print_plan(
    *,
    marketplace_rewrite: RewriteMarketplace | None,
    actions: list[PlannedAction],
    stale_tables: list[str],
    apply: bool,
    backup_root: Path,
) -> None:
    mode = "Applying" if apply else "Dry run"
    print(f"{mode}: legacy socket install cleanup")

    if marketplace_rewrite is None and not actions and not stale_tables:
        print("No legacy socket install artifacts were found.")
        return

    if marketplace_rewrite is not None:
        target = marketplace_rewrite.path
        if marketplace_rewrite.data is None:
            print(f"- Remove personal marketplace file after backing it up: {target}")
        else:
            print(f"- Rewrite personal marketplace after backing it up: {target}")
        print(
            "  Removes legacy plugin entries: "
            + ", ".join(marketplace_rewrite.removed_names)
        )

    for action in actions:
        print(f"- {action.description}")

    if stale_tables:
        print("- Stale non-socket plugin enablement entries found in config.toml:")
        for table_name in stale_tables:
            print(f"  - [plugins.\"{table_name}\"]")
        print("  These are reported only; this helper does not rewrite config.toml yet.")

    if apply:
        print(f"Backups written under: {backup_root}")
    else:
        print("No files changed. Re-run with --apply to perform this cleanup.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Remove legacy copied socket plugin payloads and personal marketplace entries "
            "after migrating to the Git-backed socket marketplace."
        )
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory to inspect. Defaults to the current user's home.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Back up and remove the detected legacy artifacts.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    home = args.home.expanduser().resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = home / ".codex" / "backups" / "socket-legacy-install-cleanup" / timestamp

    personal_marketplace = home / ".agents" / "plugins" / "marketplace.json"
    codex_plugins_root = home / ".codex" / "plugins"
    config_path = home / ".codex" / "config.toml"

    marketplace_rewrite = plan_marketplace_cleanup(personal_marketplace)
    actions = plan_plugin_dir_cleanup(codex_plugins_root)
    stale_tables = stale_config_plugin_tables(config_path)

    print_plan(
        marketplace_rewrite=marketplace_rewrite,
        actions=actions,
        stale_tables=stale_tables,
        apply=args.apply,
        backup_root=backup_root,
    )

    if not args.apply:
        return

    if marketplace_rewrite is not None:
        apply_marketplace_rewrite(marketplace_rewrite, home=home, backup_root=backup_root)
    for action in actions:
        apply_action(action, home=home, backup_root=backup_root)


if __name__ == "__main__":
    main()
