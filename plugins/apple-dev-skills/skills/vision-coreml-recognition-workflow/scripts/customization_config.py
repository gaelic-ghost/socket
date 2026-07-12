#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Load and persist Vision Core ML recognition workflow customization state."""

from __future__ import annotations

import argparse
import copy
import os
import re
import sys
from pathlib import Path

import yaml

SCHEMA_VERSION = 1
SKILL_NAME = "vision-coreml-recognition-workflow"
CONFIG_HOME_ENV = "APPLE_DEV_SKILLS_CONFIG_HOME"
DEFAULT_CONFIG_ROOT = "~/.config/gaelic-ghost/apple-dev-skills"
ALLOWED_TOP_LEVEL = {"schemaVersion", "isCustomized", "settings"}


def fail(message: str) -> None:
    print(f"ERROR: {SKILL_NAME} customization: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_yaml(path: Path) -> dict:
    if not path.exists():
        fail(f"Missing YAML file: {path}")
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(f"Invalid YAML in {path}: {exc}")
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        fail(f"Top-level YAML document must be a mapping in {path}")
    return loaded


def validate(config: dict, *, partial: bool) -> None:
    unknown = set(config) - ALLOWED_TOP_LEVEL
    if unknown:
        fail(f"Unknown top-level keys: {', '.join(sorted(unknown))}")
    if not partial:
        missing = ALLOWED_TOP_LEVEL - set(config)
        if missing:
            fail(f"Missing required keys: {', '.join(sorted(missing))}")
    if "schemaVersion" in config and config["schemaVersion"] != SCHEMA_VERSION:
        fail(f"schemaVersion must be {SCHEMA_VERSION}")
    if "isCustomized" in config and not isinstance(config["isCustomized"], bool):
        fail("isCustomized must be boolean")
    if "settings" in config:
        if not isinstance(config["settings"], dict):
            fail("settings must be a mapping")
        for key, value in config["settings"].items():
            if not re.fullmatch(r"[A-Za-z0-9_]+", key):
                fail(f"Invalid settings key: {key}")
            if isinstance(value, (dict, list)):
                fail(f"settings values must be scalar: {key}")


def merged(base: dict, overlay: dict) -> dict:
    result = {
        "schemaVersion": base.get("schemaVersion", SCHEMA_VERSION),
        "isCustomized": base.get("isCustomized", False),
        "settings": copy.deepcopy(base.get("settings", {})),
    }
    for key in ("schemaVersion", "isCustomized"):
        if key in overlay:
            result[key] = overlay[key]
    if "settings" in overlay:
        result["settings"].update(overlay["settings"])
    return result


def template_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "customization.template.yaml"


def durable_path() -> Path:
    root = Path(os.environ.get(CONFIG_HOME_ENV, DEFAULT_CONFIG_ROOT)).expanduser()
    return root / SKILL_NAME / "customization.yaml"


def load_effective() -> dict:
    template = parse_yaml(template_path())
    validate(template, partial=False)
    durable = parse_yaml(durable_path()) if durable_path().exists() else {}
    if durable:
        validate(durable, partial=False)
    return merged(template, durable)


def dump(config: dict) -> str:
    return yaml.safe_dump(config, sort_keys=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Manage {SKILL_NAME} customization")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("path")
    commands.add_parser("effective")
    apply_parser = commands.add_parser("apply")
    apply_parser.add_argument("--input", required=True)
    commands.add_parser("reset")
    args = parser.parse_args()

    target = durable_path()
    if args.command == "path":
        print(target)
    elif args.command == "effective":
        print(dump(load_effective()), end="")
    elif args.command == "apply":
        incoming = parse_yaml(Path(args.input))
        validate(incoming, partial=True)
        updated = merged(load_effective(), incoming)
        updated["schemaVersion"] = SCHEMA_VERSION
        updated["isCustomized"] = True
        validate(updated, partial=False)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(dump(updated), encoding="utf-8")
        print(target)
    elif args.command == "reset":
        target.unlink(missing_ok=True)
        print(target)


if __name__ == "__main__":
    main()
