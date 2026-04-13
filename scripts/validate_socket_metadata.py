#!/usr/bin/env python3
"""Validate root marketplace wiring for the socket superproject."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Required JSON file is missing: {path}")
    except json.JSONDecodeError as exc:
        fail(f"JSON file is invalid at {path}:{exc.lineno}:{exc.colno}: {exc.msg}")


def validate_plugin_entry(entry: object, seen_names: set[str]) -> None:
    if not isinstance(entry, dict):
        fail("Each marketplace plugin entry must be a JSON object.")

    name = entry.get("name")
    if not isinstance(name, str) or not name:
        fail("Each marketplace plugin entry must define a non-empty string `name`.")
    if name in seen_names:
        fail(f"Marketplace plugin name `{name}` is duplicated.")
    seen_names.add(name)

    source = entry.get("source")
    if not isinstance(source, dict):
        fail(f"Marketplace plugin `{name}` is missing its `source` object.")
    source_kind = source.get("source")
    if source_kind != "local":
        fail(
            f"Marketplace plugin `{name}` must use a local source in this superproject, "
            f"but found `{source_kind}`."
        )
    relative_path = source.get("path")
    if not isinstance(relative_path, str) or not relative_path.startswith("./"):
        fail(
            f"Marketplace plugin `{name}` must use a repo-relative `./...` source.path, "
            f"but found `{relative_path}`."
        )

    plugin_root = (REPO_ROOT / relative_path).resolve()
    try:
        plugin_root.relative_to(REPO_ROOT.resolve())
    except ValueError:
        fail(
            f"Marketplace plugin `{name}` points outside the repository root: {relative_path}"
        )

    if not plugin_root.is_dir():
        fail(
            f"Marketplace plugin `{name}` points at a missing packaged plugin directory: "
            f"{relative_path}"
        )

    plugin_manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    if not plugin_manifest_path.is_file():
        fail(
            f"Marketplace plugin `{name}` is missing its packaged manifest at "
            f"{plugin_manifest_path.relative_to(REPO_ROOT)}."
        )

    plugin_manifest = load_json(plugin_manifest_path)
    if not isinstance(plugin_manifest, dict):
        fail(
            f"Packaged plugin manifest for `{name}` must decode to a JSON object: "
            f"{plugin_manifest_path.relative_to(REPO_ROOT)}"
        )

    manifest_name = plugin_manifest.get("name")
    if manifest_name != name:
        fail(
            f"Marketplace plugin `{name}` points at a packaged manifest that declares "
            f"`{manifest_name}` instead."
        )


def main() -> None:
    print("Validating root marketplace presence...")
    marketplace = load_json(MARKETPLACE_PATH)
    if not isinstance(marketplace, dict):
        fail("Root marketplace must decode to a JSON object.")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("Root marketplace must contain a non-empty `plugins` array.")

    print("Validating packaged plugin paths...")
    seen_names: set[str] = set()
    for entry in plugins:
        validate_plugin_entry(entry, seen_names)

    print("Socket marketplace validation passed.")


if __name__ == "__main__":
    main()
