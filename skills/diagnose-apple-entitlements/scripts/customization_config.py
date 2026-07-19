#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0.2,<7"]
# ///
"""Load and persist entitlement-diagnosis customization state."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

SKILL_NAME = "diagnose-apple-entitlements"
ROOT = "~/.config/gaelic-ghost/apple-dev-skills"
KEYS = {"schemaVersion", "isCustomized", "settings"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path, required: bool = False) -> dict:
    if not path.exists():
        if required:
            fail(f"Missing YAML file: {path}")
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as error:
        fail(f"Invalid YAML in {path}: {error}")
    if not isinstance(value, dict):
        fail(f"Top-level YAML document must be a mapping in {path}")
    return value


def validate(value: dict, partial: bool = False) -> None:
    if set(value) - KEYS:
        fail(f"Unknown top-level keys: {', '.join(sorted(set(value) - KEYS))}")
    if not partial and set(value) != KEYS:
        fail("State must define schemaVersion, isCustomized, and settings")
    if "schemaVersion" in value and value["schemaVersion"] != 1:
        fail("schemaVersion must be 1")
    if "isCustomized" in value and not isinstance(value["isCustomized"], bool):
        fail("isCustomized must be boolean")
    if "settings" in value:
        if not isinstance(value["settings"], dict):
            fail("settings must be a mapping")
        for key, item in value["settings"].items():
            if not re.fullmatch(r"[A-Za-z0-9_]+", str(key)):
                fail(f"Invalid settings key: {key}")
            if isinstance(item, (dict, list)):
                fail(f"settings values must be scalar: {key}")


def destination() -> Path:
    root = Path(os.environ.get("APPLE_DEV_SKILLS_CONFIG_HOME", ROOT)).expanduser()
    return root / SKILL_NAME / "customization.yaml"


def current() -> dict:
    template = read(Path(__file__).resolve().parents[1] / "references/customization.template.yaml", True)
    saved = read(destination())
    validate(template)
    if saved:
        validate(saved)
    return {"schemaVersion": 1, "isCustomized": saved.get("isCustomized", False), "settings": {**template["settings"], **saved.get("settings", {})}}


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage entitlement-diagnosis customization")
    command = parser.add_subparsers(dest="command", required=True)
    command.add_parser("path")
    command.add_parser("effective")
    apply = command.add_parser("apply")
    apply.add_argument("--input", required=True)
    command.add_parser("reset")
    args = parser.parse_args()
    target = destination()
    if args.command == "path":
        print(target)
    elif args.command == "effective":
        print(yaml.safe_dump(current(), sort_keys=False), end="")
    elif args.command == "reset":
        if target.exists():
            target.unlink()
        print(target)
    else:
        incoming = read(Path(args.input), True)
        validate(incoming, partial=True)
        updated = {"schemaVersion": 1, "isCustomized": True, "settings": {**current()["settings"], **incoming.get("settings", {})}}
        validate(updated)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(yaml.safe_dump(updated, sort_keys=False), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
