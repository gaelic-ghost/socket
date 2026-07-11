#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0.2,<7"]
# ///
"""Load and persist safe per-skill customization preferences."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import yaml

SKILL_NAME = "apple-developer-provisioning-workflow"
CONFIG_HOME_ENV = "APPLE_DEV_SKILLS_CONFIG_HOME"
DEFAULT_CONFIG_ROOT = "~/.config/gaelic-ghost/apple-dev-skills"
ALLOWED_SETTINGS = {"preferredDiscoveryMode", "preferredCloudKitAdapter"}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: Apple Developer Provisioning Workflow customization: {message}")


def template_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "customization.template.yaml"


def durable_path() -> Path:
    root = Path(os.environ.get(CONFIG_HOME_ENV, DEFAULT_CONFIG_ROOT)).expanduser()
    return root / SKILL_NAME / "customization.yaml"


def load(path: Path, *, required: bool) -> dict:
    if not path.exists():
        if required:
            fail(f"missing customization template at {path}")
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as error:
        fail(f"invalid YAML in {path}: {error}")
    if not isinstance(value, dict):
        fail(f"top-level YAML must be a mapping in {path}")
    if set(value) - {"schemaVersion", "isCustomized", "settings"}:
        fail(f"unknown top-level keys in {path}")
    settings = value.get("settings") or {}
    if not isinstance(settings, dict) or set(settings) - ALLOWED_SETTINGS:
        fail(f"settings in {path} must contain only {sorted(ALLOWED_SETTINGS)}")
    if "schemaVersion" in value and value["schemaVersion"] != 1:
        fail(f"schemaVersion in {path} must be 1")
    if "isCustomized" in value and not isinstance(value["isCustomized"], bool):
        fail(f"isCustomized in {path} must be boolean")
    return value


def effective() -> dict:
    base = load(template_path(), required=True)
    overlay = load(durable_path(), required=False)
    settings = dict(base.get("settings") or {})
    settings.update(overlay.get("settings") or {})
    settings.setdefault("preferredDiscoveryMode", "xcode-local")
    settings.setdefault("preferredCloudKitAdapter", "cktool")
    result = {
        "schemaVersion": 1,
        "isCustomized": bool(overlay) or bool(base.get("isCustomized", False)),
        "settings": settings,
    }
    if result["settings"].get("preferredDiscoveryMode") not in {"xcode-local", "rest-first"}:
        fail("preferredDiscoveryMode must be xcode-local or rest-first")
    if result["settings"].get("preferredCloudKitAdapter") not in {"cktool", "cktool-js"}:
        fail("preferredCloudKitAdapter must be cktool or cktool-js")
    return result


def write(config: dict) -> None:
    path = durable_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")


def apply(override_path: Path) -> None:
    override = load(override_path, required=True)
    config = effective()
    config["settings"].update(override.get("settings") or {})
    config["isCustomized"] = True
    write(config)
    print(durable_path())


def reset() -> None:
    path = durable_path()
    if path.exists():
        path.unlink()
    print(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect or persist safe workflow preferences.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("path")
    commands.add_parser("effective")
    apply_command = commands.add_parser("apply")
    apply_command.add_argument("--input", required=True, type=Path)
    commands.add_parser("reset")
    set_command = commands.add_parser("set")
    set_command.add_argument("--discovery-mode", choices=["xcode-local", "rest-first"])
    set_command.add_argument("--cloudkit-adapter", choices=["cktool", "cktool-js"])
    args = parser.parse_args()

    if args.command == "path":
        print(durable_path())
    elif args.command == "effective":
        print(yaml.safe_dump(effective(), sort_keys=False), end="")
    elif args.command == "apply":
        apply(args.input)
    elif args.command == "reset":
        reset()
    else:
        config = effective()
        if args.discovery_mode:
            config["settings"]["preferredDiscoveryMode"] = args.discovery_mode
        if args.cloudkit_adapter:
            config["settings"]["preferredCloudKitAdapter"] = args.cloudkit_adapter
        config["isCustomized"] = True
        write(config)
        print(yaml.safe_dump(config, sort_keys=False), end="")


if __name__ == "__main__":
    main()
