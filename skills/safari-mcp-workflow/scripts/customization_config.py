#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0.2,<7"]
# ///
"""Load and persist per-skill Safari MCP customization state."""

from __future__ import annotations

import argparse
import copy
import os
import re
import sys
from pathlib import Path

import yaml

SCHEMA_VERSION = 1
SKILL_NAME = "safari-mcp-workflow"
CONFIG_HOME_ENV = "APPLE_DEV_SKILLS_CONFIG_HOME"
DEFAULT_CONFIG_ROOT = "~/.config/gaelic-ghost/apple-dev-skills"
ALLOWED_TOP_LEVEL = {"schemaVersion", "isCustomized", "settings"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def quote_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def encode_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return quote_string("" if value is None else str(value))


def parse_yaml(path: Path) -> dict:
    if not path.exists():
        fail(f"Missing YAML file: {path}")
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        fail(f"Invalid YAML in {path}: {error}")
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        fail(f"Top-level YAML document must be a mapping in {path}")
    return loaded


def validate_config(config: dict, *, allow_partial: bool) -> None:
    unknown = set(config) - ALLOWED_TOP_LEVEL
    if unknown:
        fail(f"Unknown top-level keys: {', '.join(sorted(unknown))}")
    if not allow_partial and set(config) != ALLOWED_TOP_LEVEL:
        fail("Missing required customization keys: schemaVersion, isCustomized, settings")
    if "schemaVersion" in config and config["schemaVersion"] != SCHEMA_VERSION:
        fail(f"schemaVersion must be {SCHEMA_VERSION}")
    if "isCustomized" in config and not isinstance(config["isCustomized"], bool):
        fail("isCustomized must be boolean")
    if "settings" in config:
        if not isinstance(config["settings"], dict):
            fail("settings must be a mapping")
        for key, value in config["settings"].items():
            if not re.fullmatch(r"[A-Za-z0-9_]+", str(key)):
                fail(f"Invalid settings key: {key}")
            if isinstance(value, (dict, list)):
                fail(f"settings values must be scalar: {key}")


def merge_configs(base: dict, overlay: dict) -> dict:
    merged = {
        "schemaVersion": base.get("schemaVersion", SCHEMA_VERSION),
        "isCustomized": base.get("isCustomized", False),
        "settings": copy.deepcopy(base.get("settings", {})),
    }
    for key in ("schemaVersion", "isCustomized"):
        if key in overlay:
            merged[key] = overlay[key]
    if "settings" in overlay:
        merged["settings"].update(overlay["settings"])
    return merged


def dump_yaml(config: dict) -> str:
    lines = [
        f"schemaVersion: {config['schemaVersion']}",
        f"isCustomized: {'true' if config['isCustomized'] else 'false'}",
        "settings:",
    ]
    lines.extend(f"  {key}: {encode_scalar(value)}" for key, value in sorted(config["settings"].items()))
    return "\n".join(lines) + "\n"


def template_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "customization.template.yaml"


def durable_path() -> Path:
    root = Path(os.environ.get(CONFIG_HOME_ENV, DEFAULT_CONFIG_ROOT)).expanduser()
    return root / SKILL_NAME / "customization.yaml"


def load_template() -> dict:
    config = parse_yaml(template_path())
    validate_config(config, allow_partial=False)
    return config


def load_durable() -> dict:
    return parse_yaml(durable_path()) if durable_path().exists() else {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage Safari MCP workflow customization.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("path")
    commands.add_parser("effective")
    apply = commands.add_parser("apply")
    apply.add_argument("--input", required=True)
    commands.add_parser("reset")
    args = parser.parse_args()
    if args.command == "path":
        print(durable_path())
        return
    if args.command == "effective":
        print(dump_yaml(merge_configs(load_template(), load_durable())), end="")
        return
    if args.command == "reset":
        durable_path().unlink(missing_ok=True)
        print(durable_path())
        return
    incoming = parse_yaml(Path(args.input))
    validate_config(incoming, allow_partial=True)
    updated = merge_configs(merge_configs(load_template(), load_durable()), incoming)
    updated["schemaVersion"] = SCHEMA_VERSION
    updated["isCustomized"] = True
    validate_config(updated, allow_partial=False)
    durable_path().parent.mkdir(parents=True, exist_ok=True)
    durable_path().write_text(dump_yaml(updated), encoding="utf-8")
    print(durable_path())


if __name__ == "__main__":
    main()
