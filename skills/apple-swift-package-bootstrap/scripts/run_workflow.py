#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Unified runtime entrypoint for apple-swift-package-bootstrap."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import customization_config


def load_effective_config() -> dict:
    return customization_config.merge_configs(
        customization_config.load_template(),
        customization_config.load_durable(),
    )


def parse_output(stdout: str) -> dict:
    result = {
        "resolved_path": None,
        "validation_result": None,
        "git_initialized": None,
        "agents_copied": None,
        "testing_mode": None,
    }
    for line in stdout.splitlines():
        if line.startswith("Created Swift package: "):
            result["resolved_path"] = line.split(": ", 1)[1].strip()
        elif line.startswith("Validation: "):
            result["validation_result"] = line.split(": ", 1)[1].strip()
        elif line.startswith("Git: "):
            result["git_initialized"] = line.endswith("initialized")
        elif line.startswith("AGENTS: "):
            result["agents_copied"] = line.endswith("copied")
        elif line.startswith("Testing mode: "):
            result["testing_mode"] = line.split(": ", 1)[1].strip()
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name")
    parser.add_argument("--type")
    parser.add_argument("--destination")
    parser.add_argument("--platform")
    parser.add_argument("--version-profile")
    parser.add_argument("--testing-mode")
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_effective_config()
    settings = config["settings"]

    name = args.name
    pkg_type = args.type or str(settings.get("defaultPackageType", "library"))
    destination = args.destination or "."
    platform = args.platform or str(settings.get("defaultPlatformPreset", "multiplatform"))
    version_profile = args.version_profile or str(settings.get("defaultVersionProfile", "current-minus-one"))
    testing_mode = args.testing_mode or str(settings.get("defaultTestingMode", "swift-testing"))
    initialize_git = bool(settings.get("initializeGit", True))
    copy_agents = bool(settings.get("copyAgentsMd", True))

    normalized_inputs = {
        "name": name,
        "type": pkg_type,
        "destination": destination,
        "platform": platform,
        "version_profile": version_profile,
        "testing_mode": testing_mode,
        "skip_validation": args.skip_validation,
        "initialize_git": initialize_git,
        "copy_agents_md": copy_agents,
    }

    if not name:
        payload = {
            "status": "blocked",
            "path_type": "primary",
            "resolved_path": None,
            "normalized_inputs": normalized_inputs,
            "validation_result": None,
            "next_step": "Provide --name to create a new Swift package.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    script_path = Path(__file__).with_name("bootstrap_swift_package.sh")
    if not script_path.exists():
        payload = {
            "status": "success",
            "path_type": "fallback",
            "resolved_path": None,
            "normalized_inputs": normalized_inputs,
            "validation_result": None,
            "next_step": "The bootstrap script is missing. Fall back to manual swift package init guidance.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    command = [
        str(script_path),
        "--name",
        name,
        "--type",
        pkg_type,
        "--destination",
        destination,
        "--platform",
        platform,
        "--version-profile",
        version_profile,
        "--testing-mode",
        testing_mode,
    ]
    if args.skip_validation:
        command.append("--skip-validation")
    if not initialize_git:
        command.append("--skip-git-init")
    if not copy_agents:
        command.append("--skip-copy-agents")

    if args.dry_run:
        payload = {
            "status": "success",
            "path_type": "primary",
            "resolved_path": str(Path(destination).expanduser() / name),
            "normalized_inputs": normalized_inputs,
            "validation_result": "skipped (--dry-run)",
            "command": command,
            "next_step": "Run the bootstrap workflow without --dry-run to create the package.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    parsed = parse_output(proc.stdout)
    payload = {
        "status": "success" if proc.returncode == 0 else "failed",
        "path_type": "primary",
        "resolved_path": parsed["resolved_path"],
        "normalized_inputs": normalized_inputs,
        "validation_result": parsed["validation_result"],
        "git_initialized": parsed["git_initialized"],
        "agents_copied": parsed["agents_copied"],
        "testing_mode": parsed["testing_mode"],
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "next_step": (
            "Use apple-xcode-workflow for build, test, or xcodebuild-based package work when Xcode-managed tooling is required."
            if proc.returncode == 0
            else "Fix the bootstrap error and rerun the workflow."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
