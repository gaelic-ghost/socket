#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0.2,<7"]
# ///
"""Plan SwiftPM plugin, macro, trait, and generated-source work."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import customization_config

EXTENSION_TYPES = {
    "build-tool-plugin",
    "command-plugin",
    "macro",
    "traits",
    "generated-source",
}
TOOLCHAIN_SCOPES = {"swiftly", "xcode", "both"}


def normalize(text: str | None) -> str:
    return " ".join((text or "").strip().lower().split())


def infer_extension_type(request: str | None) -> str | None:
    text = normalize(request)
    if not text:
        return None
    if "macro" in text or "expansion" in text:
        return "macro"
    if "trait" in text or "feature flag" in text:
        return "traits"
    if "command plugin" in text or "plugin command" in text or "format plugin" in text:
        return "command-plugin"
    if "generated" in text or "codegen" in text or "code generation" in text:
        return "generated-source"
    if "build tool plugin" in text or "build plugin" in text or "plugin" in text:
        return "build-tool-plugin"
    return None


def resolve_package_root(repo_root: str | None) -> tuple[Path, Path | None]:
    requested = Path(repo_root or ".").expanduser().resolve()
    candidate = requested if requested.is_dir() else requested.parent
    for current in (candidate, *candidate.parents):
        if (current / "Package.swift").exists():
            return requested, current
    if requested.exists() and requested.is_dir():
        manifests = sorted(requested.rglob("Package.swift"), key=lambda path: (len(path.parts), str(path)))
        if manifests:
            return requested, manifests[0].parent
    return requested, None


def package_context(repo_root: str | None) -> dict:
    requested, package_root = resolve_package_root(repo_root)
    scan_root = package_root or requested
    plugin_sources = []
    if scan_root.exists():
        plugin_dir = scan_root / "Plugins"
        if plugin_dir.exists():
            plugin_sources = sorted(str(path) for path in plugin_dir.rglob("*.swift"))
    return {
        "requested_root": str(requested),
        "package_root": str(scan_root) if package_root is not None else None,
        "exists": requested.exists(),
        "has_package": package_root is not None,
        "plugin_sources": plugin_sources,
    }


def identity_commands(scope: str) -> list[str]:
    commands: list[str] = []
    if scope in {"swiftly", "both"}:
        commands.extend(["swiftly use --print-location", "swift --version"])
    if scope in {"xcode", "both"}:
        commands.extend(["xcode-select -p", "xcrun --find swift", "xcrun swift --version"])
    return commands


def prefixed_commands(scope: str, commands: list[str]) -> list[str]:
    planned: list[str] = []
    if scope in {"swiftly", "both"}:
        planned.extend(commands)
    if scope in {"xcode", "both"}:
        planned.extend(f"xcrun {command}" for command in commands)
    return planned


def extension_commands(extension_type: str, scope: str) -> list[str]:
    if extension_type == "build-tool-plugin":
        commands = ["swift package plugin --list", "swift package init --type build-tool-plugin"]
    elif extension_type == "command-plugin":
        commands = ["swift package plugin --list", "swift package plugin --help", "swift package init --type command-plugin"]
    elif extension_type == "macro":
        commands = ["swift package init --type macro", "swift build", "swift test"]
    elif extension_type == "traits":
        commands = [
            "swift package show-traits --format json",
            "swift build",
            "swift test",
            "swift build --disable-default-traits",
            "swift test --disable-default-traits",
            "swift build --enable-all-traits",
            "swift test --enable-all-traits",
        ]
    else:
        commands = ["swift package dump-package", "swift build", "swift build -v"]
    return identity_commands(scope) + prefixed_commands(scope, commands)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extension-type", choices=sorted(EXTENSION_TYPES))
    parser.add_argument("--request")
    parser.add_argument("--repo-root")
    parser.add_argument("--toolchain-scope", choices=sorted(TOOLCHAIN_SCOPES), default="both")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    customization_config.merge_configs(
        customization_config.load_template(),
        customization_config.load_durable(),
    )

    extension_type = args.extension_type or infer_extension_type(args.request)
    context = package_context(args.repo_root)
    status = "success"
    next_step = "Proceed with the package-first extension plan."
    if extension_type is None:
        status = "blocked"
        next_step = "Pass --extension-type or provide a request that identifies plugin, macro, trait, or generated-source work."
    elif not context["exists"]:
        status = "blocked"
        next_step = "Resolve the requested repository path before continuing."
    elif not context["has_package"]:
        status = "blocked"
        next_step = "Use a Swift package repository containing Package.swift."
    commands = extension_commands(extension_type, args.toolchain_scope) if extension_type else []
    payload = {
        "status": status,
        "path_type": "primary",
        "output": {
            "extension_type": extension_type,
            "extension_type_source": "explicit" if args.extension_type else "inferred" if extension_type else "missing",
            "package_context": context,
            "toolchain_scope": args.toolchain_scope,
            "planned_commands": commands,
            "support_window": {"minimum": "6.2", "policy": "latest stable minor plus previous stable minor"},
            "next_step": next_step,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if status == "blocked" else 0


if __name__ == "__main__":
    sys.exit(main())
