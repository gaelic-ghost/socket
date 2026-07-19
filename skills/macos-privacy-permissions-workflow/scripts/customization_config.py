#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0.2,<7"]
# ///
"""Load and persist macOS privacy workflow customization state."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

SKILL_NAME = "macos-privacy-permissions-workflow"
CONFIG_HOME_ENV = "APPLE_DEV_SKILLS_CONFIG_HOME"
DEFAULT_CONFIG_ROOT = "~/.config/gaelic-ghost/apple-dev-skills"
ALLOWED_KEYS = {"schemaVersion", "isCustomized", "settings"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path, *, required: bool) -> dict:
    if not path.exists():
        if required:
            fail(f"Missing YAML file: {path}")
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as error:
        fail(f"Invalid YAML in {path}: {error}")
    if not isinstance(data, dict):
        fail(f"Top-level YAML document must be a mapping in {path}")
    return data


def validate(data: dict, *, partial: bool) -> None:
    unknown = set(data) - ALLOWED_KEYS
    if unknown:
        fail(f"Unknown top-level keys: {', '.join(sorted(unknown))}")
    if not partial and set(data) != ALLOWED_KEYS:
        fail("Customization state must define schemaVersion, isCustomized, and settings")
    if "schemaVersion" in data and data["schemaVersion"] != 1:
        fail("schemaVersion must be 1")
    if "isCustomized" in data and not isinstance(data["isCustomized"], bool):
        fail("isCustomized must be boolean")
    if "settings" in data:
        if not isinstance(data["settings"], dict):
            fail("settings must be a mapping")
        for key, value in data["settings"].items():
            if not re.fullmatch(r"[A-Za-z0-9_]+", str(key)):
                fail(f"Invalid settings key: {key}")
            if isinstance(value, (dict, list)):
                fail(f"settings values must be scalar: {key}")


def template_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "customization.template.yaml"


def durable_path() -> Path:
    root = Path(os.environ.get(CONFIG_HOME_ENV, DEFAULT_CONFIG_ROOT)).expanduser()
    return root / SKILL_NAME / "customization.yaml"


def effective() -> dict:
    base = load(template_path(), required=True)
    saved = load(durable_path(), required=False)
    validate(base, partial=False)
    validate(saved, partial=False) if saved else None
    merged = {
        "schemaVersion": saved.get("schemaVersion", base["schemaVersion"]),
        "isCustomized": saved.get("isCustomized", base["isCustomized"]),
        "settings": {**base["settings"], **saved.get("settings", {})},
    }
    validate(merged, partial=False)
    return merged


def render(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, default_flow_style=False)


def command_path(_: argparse.Namespace) -> None:
    print(durable_path())


def command_effective(_: argparse.Namespace) -> None:
    print(render(effective()), end="")


def command_apply(args: argparse.Namespace) -> None:
    incoming = load(Path(args.input), required=True)
    validate(incoming, partial=True)
    current = effective()
    updated = {
        "schemaVersion": 1,
        "isCustomized": True,
        "settings": {**current["settings"], **incoming.get("settings", {})},
    }
    validate(updated, partial=False)
    target = durable_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(updated), encoding="utf-8")
    print(target)


def command_reset(_: argparse.Namespace) -> None:
    target = durable_path()
    if target.exists():
        target.unlink()
    print(target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage macOS privacy workflow customization")
    commands = parser.add_subparsers(dest="command", required=True)
    path_parser = commands.add_parser("path")
    path_parser.set_defaults(func=command_path)
    effective_parser = commands.add_parser("effective")
    effective_parser.set_defaults(func=command_effective)
    apply_parser = commands.add_parser("apply")
    apply_parser.add_argument("--input", required=True)
    apply_parser.set_defaults(func=command_apply)
    reset_parser = commands.add_parser("reset")
    reset_parser.set_defaults(func=command_reset)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
