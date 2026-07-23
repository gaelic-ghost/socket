#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0.2,<7"]
# ///
"""Maintain policy-only customization metadata for the tvOS playback workflow."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml

SKILL_NAME = "tvos-media-playback-workflow"
CONFIG_HOME_ENV = "APPLE_DEV_SKILLS_CONFIG_HOME"
DEFAULT_CONFIG_ROOT = "~/.config/gaelic-ghost/apple-dev-skills"
REQUIRED_KEYS = {"schemaVersion", "isCustomized", "settings"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def template_path() -> Path:
    return Path(__file__).parents[1] / "references" / "customization.template.yaml"


def load_yaml(path: Path, *, partial: bool = False) -> dict:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        fail(f"Missing YAML file: {path}")
    except yaml.YAMLError as exc:
        fail(f"Invalid YAML in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"Top-level YAML document must be a mapping in {path}")
    unknown = set(value) - REQUIRED_KEYS
    if unknown:
        fail(f"Unknown top-level keys: {', '.join(sorted(unknown))}")
    if not partial and set(value) != REQUIRED_KEYS:
        fail("Customization file must contain schemaVersion, isCustomized, and settings")
    if "schemaVersion" in value and value["schemaVersion"] != 1:
        fail("schemaVersion must be 1")
    if "isCustomized" in value and not isinstance(value["isCustomized"], bool):
        fail("isCustomized must be boolean")
    if "settings" in value:
        if not isinstance(value["settings"], dict):
            fail("settings must be a mapping")
        if any(isinstance(item, (dict, list)) for item in value["settings"].values()):
            fail("settings values must be scalar")
    return value


def load_template() -> dict:
    return load_yaml(template_path())


def config_path() -> Path:
    root = Path(os.environ.get(CONFIG_HOME_ENV, DEFAULT_CONFIG_ROOT)).expanduser()
    return root / SKILL_NAME / "customization.yaml"


def effective() -> dict:
    base = load_template()
    path = config_path()
    if not path.exists():
        return base
    overlay = load_yaml(path, partial=True)
    return {
        "schemaVersion": overlay.get("schemaVersion", base["schemaVersion"]),
        "isCustomized": overlay.get("isCustomized", base["isCustomized"]),
        "settings": {**base["settings"], **overlay.get("settings", {})},
    }


def emit(value: dict) -> None:
    print(yaml.safe_dump(value, sort_keys=False).strip())


def main() -> None:
    parser = argparse.ArgumentParser()
    command = parser.add_subparsers(dest="command", required=True)
    command.add_parser("effective")
    apply = command.add_parser("apply")
    apply.add_argument("--input", required=True)
    command.add_parser("reset")
    args = parser.parse_args()
    path = config_path()
    if args.command == "effective":
        emit(effective())
    elif args.command == "apply":
        overlay = load_yaml(Path(args.input), partial=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(overlay, sort_keys=False), encoding="utf-8")
        print(path)
    else:
        path.unlink(missing_ok=True)
        print(path)


if __name__ == "__main__":
    main()
