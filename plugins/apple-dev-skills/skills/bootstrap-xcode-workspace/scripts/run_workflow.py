#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Normalize a modular Apple workspace bootstrap contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SUPPORTED_PLATFORMS = {"ios", "macos", "tvos", "watchos", "visionos"}
SUPPORTED_SERVICES = {"none", "hummingbird", "vapor", "fsharp-azure"}


def is_valid_workspace_name(value: str) -> bool:
    """Return whether value is one safe directory and workspace-name component."""
    return bool(value) and value not in {".", ".."} and not Path(value).is_absolute() and len(Path(value).parts) == 1


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--name", required=True)
    result.add_argument("--destination", default=".")
    result.add_argument("--app-topology", default="separate-projects")
    result.add_argument("--platforms", default="ios,macos")
    result.add_argument("--service", default="none")
    result.add_argument("--dry-run", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    platforms = [value.strip().lower() for value in args.platforms.split(",") if value.strip()]
    destination = Path(args.destination).expanduser().resolve()
    if not is_valid_workspace_name(args.name):
        print(json.dumps({
            "status": "blocked",
            "path_type": "fallback",
            "stderr": "--name must be one non-empty directory name without path separators, '.' or '..'.",
            "actions": [],
        }, indent=2, sort_keys=True))
        return 1
    root = destination / args.name
    payload = {
        "status": "success",
        "path_type": "fallback",
        "workspace_root": str(root),
        "workspace_path": str(root / f"{args.name}.xcworkspace"),
        "normalized_inputs": {
            "name": args.name,
            "destination": args.destination,
            "app_topology": args.app_topology,
            "platforms": platforms,
            "service": args.service,
            "dry_run": args.dry_run,
        },
        "actions": [],
    }
    if args.app_topology not in {"separate-projects", "multiplatform-target"}:
        payload.update(status="blocked", stderr="Choose app topology separate-projects or multiplatform-target.")
    elif not platforms or any(platform not in SUPPORTED_PLATFORMS for platform in platforms):
        payload.update(status="blocked", stderr="Choose platforms from ios, macos, tvos, watchos, or visionos.")
    elif args.app_topology == "multiplatform-target" and "watchos" in platforms:
        payload.update(status="blocked", stderr="watchOS requires a separate target/project; remove it from multiplatform-target platforms.")
    elif args.service not in SUPPORTED_SERVICES:
        payload.update(status="blocked", stderr="Choose service none, hummingbird, vapor, or fsharp-azure.")
    elif root.exists() and (not root.is_dir() or any(root.iterdir())):
        payload.update(status="blocked", stderr="The workspace root already contains files; choose an empty destination or use sync-xcode-workspace-guidance.")
    else:
        payload["actions"] = [
            "create Apps/, Packages/, and optional Services/ directories",
            "bootstrap Core packages before their consuming app projects",
            "generate each app project with bootstrap-xcode-app-project",
            "declare local packages in each consuming app project.yml",
            "create the .xcworkspace through Xcode and add app projects at workspace root level",
        ]
        if args.service != "none":
            payload["actions"].append(f"bootstrap optional {args.service} service under Services/")
        payload["next_step"] = "Run the named child skills in the reported order; use Xcode to create the workspace rather than hand-writing workspace data."
        if not args.dry_run:
            (root / "Apps").mkdir(parents=True, exist_ok=True)
            (root / "Packages").mkdir(exist_ok=True)
            if args.service != "none":
                (root / "Services").mkdir(exist_ok=True)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
