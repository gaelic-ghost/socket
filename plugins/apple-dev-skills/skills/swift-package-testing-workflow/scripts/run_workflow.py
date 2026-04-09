#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Runtime workflow policy engine for swift-package-testing-workflow."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

import customization_config


VALID_OPERATION_TYPES = {
    "package-inspection",
    "read-search",
    "test",
    "mutation",
}


def normalize_request_text(text: str | None) -> str:
    return " ".join((text or "").strip().lower().split())


def infer_operation_type_from_request(request: str | None) -> str | None:
    text = normalize_request_text(request)
    if not text:
        return None

    checks: list[tuple[str, tuple[str, ...]]] = [
        ("test", (" test", " tests", "testing", "xctest", "swift testing", "xctestplan", "spec")),
        ("package-inspection", ("describe", "dump-package", "show dependencies", "inspect package", "inspect the package", "package graph")),
        ("read-search", ("read", "search", "grep", "find", "lookup", "trace")),
        ("mutation", ("edit test", "change test", "modify test", "rewrite test", "refactor test", "rename test", "move test", "add test", "fix test")),
    ]

    padded = f" {text} "
    if any(
        needle in padded
        for needle in (
            " build",
            " compile",
            " release build",
            " debug build",
            " artifact",
            " run",
            " launch",
            " execute",
            " start",
            " plugin",
            " plugins",
            " package.swift",
            " manifest",
            " dependency",
            " dependencies",
            " add package",
            " add target",
            " resolve",
            " update package",
            " package resource",
            " bundle.module",
            " metallib",
            " resource.",
        )
    ):
        return "build"
    for operation_type, needles in checks:
        if any(needle in padded for needle in needles):
            return operation_type
    return None


def load_effective_config() -> dict:
    return customization_config.merge_configs(
        customization_config.load_template(),
        customization_config.load_durable(),
    )


def shell_join(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def first_matching_file(root: Path, pattern: str) -> list[str]:
    return sorted(str(path) for path in root.rglob(pattern))


def infer_package_root(repo_root: str | None) -> tuple[Path, Path | None]:
    requested = Path(repo_root or ".").expanduser().resolve()
    candidate = requested if requested.is_dir() else requested.parent

    for current in (candidate, *candidate.parents):
        if (current / "Package.swift").exists():
            return requested, current

    descendants = sorted(
        requested.rglob("Package.swift"),
        key=lambda path: (len(path.relative_to(requested).parts), str(path)),
    )
    if descendants:
        return requested, descendants[0].parent
    return requested, None


def discover_repo_shape(repo_root: str | None) -> dict:
    requested_root, package_root = infer_package_root(repo_root)
    if not requested_root.exists():
        return {
            "requested_root": str(requested_root),
            "repo_root": str(requested_root),
            "exists": False,
            "has_package": False,
            "xcode_markers": [],
            "xctestplans": [],
            "test_targets": [],
            "ui_test_targets": [],
            "metal_sources": [],
            "mixed_root": False,
            "reason": "repo-root-missing",
        }

    scan_root = package_root or requested_root
    has_package = package_root is not None
    markers: list[str] = []
    for suffix in ("*.xcodeproj", "*.xcworkspace", "*.pbxproj"):
        markers.extend(first_matching_file(scan_root, suffix))
    tests_dir = scan_root / "Tests"
    test_targets = sorted(path.name for path in tests_dir.iterdir() if path.is_dir()) if tests_dir.exists() else []
    ui_test_targets = sorted(name for name in test_targets if "UI" in name or "UITest" in name)
    xctestplans = first_matching_file(scan_root, "*.xctestplan")
    metal_sources = first_matching_file(scan_root, "*.metal")

    return {
        "requested_root": str(requested_root),
        "repo_root": str(scan_root),
        "exists": True,
        "has_package": has_package,
        "xcode_markers": markers,
        "xctestplans": xctestplans,
        "test_targets": test_targets,
        "ui_test_targets": ui_test_targets,
        "metal_sources": metal_sources,
        "mixed_root": has_package and bool(markers),
        "reason": (
            "package-root-inferred"
            if has_package and scan_root != requested_root
            else "ok"
            if has_package
            else "package-swift-missing"
        ),
    }


def inferred_package_name(repo_shape: dict) -> str | None:
    root = repo_shape.get("repo_root")
    return Path(root).name if root else None


def inferred_xcode_scheme(repo_shape: dict) -> str:
    plans = repo_shape.get("xctestplans", [])
    if len(plans) == 1:
        return Path(plans[0]).stem
    package_name = inferred_package_name(repo_shape)
    return package_name or "<package-scheme>"


def build_commands(operation_type: str, repo_shape: dict) -> list[str]:
    if operation_type == "package-inspection":
        return ["swift package describe", "swift package dump-package"]
    if operation_type == "read-search":
        return ["swift package describe"]
    if operation_type == "test":
        commands = ["swift test", "swift test --filter <pattern>"]
        if repo_shape["xctestplans"]:
            commands.append(f"xcodebuild -scheme {inferred_xcode_scheme(repo_shape)} -showTestPlans")
            commands.append(
                f"xcodebuild -scheme {inferred_xcode_scheme(repo_shape)} -testPlan {Path(repo_shape['xctestplans'][0]).stem} test"
            )
        return commands
    if operation_type == "mutation":
        return [
            "Edit package test sources or test fixtures directly when the change stays inside SwiftPM-managed scope.",
            shell_join(["swift", "test", "--filter", "<pattern>"]),
        ]
    return []


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation-type", choices=sorted(VALID_OPERATION_TYPES))
    parser.add_argument("--request")
    parser.add_argument("--repo-root")
    parser.add_argument("--mixed-root-opt-in", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    load_effective_config()

    inferred_operation_type = infer_operation_type_from_request(args.request)
    operation_type = args.operation_type or inferred_operation_type

    if operation_type is None:
        payload = {
            "status": "blocked",
            "path_type": "primary",
            "output": {
                "operation_type": None,
                "operation_type_source": "missing",
                "repo_shape": discover_repo_shape(args.repo_root),
                "planned_commands": [],
                "next_step": "Pass --operation-type explicitly or provide --request text that makes the intended SwiftPM workflow obvious.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if operation_type == "build":
        payload = {
            "status": "handoff",
            "path_type": "fallback",
            "output": {
                "operation_type": "build-or-run",
                "operation_type_source": "explicit" if args.operation_type else "inferred",
                "repo_shape": discover_repo_shape(args.repo_root),
                "planned_commands": [],
                "next_step": "Use swift-package-build-run-workflow because this request is primarily about package build, run, manifest, dependency, plugin, resource, or Metal-distribution work.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    repo_shape = discover_repo_shape(args.repo_root)
    status = "success"
    path_type = "primary"
    next_step = "Proceed with the SwiftPM-first path."

    if not repo_shape["exists"]:
        status = "blocked"
        next_step = "Resolve the repo root before continuing."
    elif not repo_shape["has_package"]:
        status = "blocked"
        next_step = "Use a Swift package repo with Package.swift at the selected root."
    elif repo_shape["mixed_root"] and not args.mixed_root_opt_in:
        status = "handoff"
        next_step = "Use xcode-testing-workflow because this repo root is mixed and Xcode-managed test behavior may matter."

    payload = {
        "status": status,
        "path_type": path_type,
        "output": {
            "operation_type": operation_type,
            "operation_type_source": "explicit" if args.operation_type else "inferred",
            "repo_shape": repo_shape,
            "planned_commands": build_commands(operation_type, repo_shape),
            "inferred_context": {
                "package_name": inferred_package_name(repo_shape),
                "primary_test_target": repo_shape["test_targets"][0] if len(repo_shape["test_targets"]) == 1 else None,
                "ui_test_targets": repo_shape["ui_test_targets"],
                "has_xcode_test_plan": bool(repo_shape["xctestplans"]),
                "xcode_scheme_hint": inferred_xcode_scheme(repo_shape) if repo_shape["xctestplans"] else None,
                "has_metal_sources": bool(repo_shape["metal_sources"]),
            },
            "next_step": next_step,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status != "blocked" else 1


if __name__ == "__main__":
    sys.exit(main())
