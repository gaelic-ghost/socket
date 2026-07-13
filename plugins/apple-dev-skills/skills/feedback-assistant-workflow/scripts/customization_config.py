#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0.2,<7"]
# ///
"""Manage Feedback Assistant Workflow customization state."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import yaml

SKILL_NAME = "feedback-assistant-workflow"
CONFIG_HOME_ENV = "APPLE_DEV_SKILLS_CONFIG_HOME"
DEFAULT_CONFIG_ROOT = "~/.config/gaelic-ghost/apple-dev-skills"
DEFAULT = {"schemaVersion": 1, "isCustomized": False, "settings": {}}


def config_path() -> Path:
    root = Path(os.environ.get(CONFIG_HOME_ENV, DEFAULT_CONFIG_ROOT)).expanduser()
    return root / SKILL_NAME / "customization.yaml"


def load(path: Path, *, partial: bool = False) -> dict:
    if not path.exists():
        return {} if partial else DEFAULT.copy()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Customization must be a YAML mapping: {path}")
    unknown = set(data) - set(DEFAULT)
    if unknown:
        raise ValueError(f"Unsupported customization keys: {', '.join(sorted(unknown))}")
    if not partial and set(data) != set(DEFAULT):
        raise ValueError(f"Customization must contain schemaVersion, isCustomized, and settings: {path}")
    if "schemaVersion" in data and data["schemaVersion"] != 1:
        raise ValueError("schemaVersion must be 1")
    if "isCustomized" in data and not isinstance(data["isCustomized"], bool):
        raise ValueError("isCustomized must be boolean")
    if "settings" in data and not isinstance(data["settings"], dict):
        raise ValueError("settings must be a mapping")
    return data


def merged() -> dict:
    result = {"schemaVersion": 1, "isCustomized": False, "settings": {}}
    result.update(load(config_path(), partial=True))
    result["settings"] = dict(result.get("settings", {}))
    return result


def write(value: dict) -> None:
    target = config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
    print(target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage Feedback Assistant Workflow customization")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("path")
    commands.add_parser("effective")
    apply = commands.add_parser("apply")
    apply.add_argument("--input", required=True)
    commands.add_parser("reset")
    args = parser.parse_args()
    if args.command == "path":
        print(config_path())
    elif args.command == "effective":
        print(yaml.safe_dump(merged(), sort_keys=False), end="")
    elif args.command == "apply":
        update = load(Path(args.input), partial=True)
        value = merged()
        value.update(update)
        value["settings"] = {**merged()["settings"], **update.get("settings", {})}
        value["schemaVersion"] = 1
        value["isCustomized"] = True
        write(value)
    else:
        target = config_path()
        target.unlink(missing_ok=True)
        print(target)


if __name__ == "__main__":
    main()
