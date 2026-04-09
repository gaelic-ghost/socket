#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Runtime workflow policy engine for swift-package-workflow."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import customization_config


VALID_OPERATION_TYPES = {
    "package-inspection",
    "read-search",
    "manifest-dependencies",
    "build",
    "test",
    "run",
    "plugin",
    "toolchain-management",
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
        ("run", (" run", "launch", "execute", "start")),
        ("plugin", ("plugin", "plugins")),
        ("toolchain-management", ("toolchain", "swift version", "xcrun", "xcodebuild", "metal toolchain", "sdk")),
        ("manifest-dependencies", ("package.swift", "manifest", "dependency", "dependencies", "add package", "add target", "resolve", "update package", "package resource", "bundle.module", "metallib", "resource.")),
        ("package-inspection", ("describe", "dump-package", "show dependencies", "inspect package", "inspect the package", "package graph")),
        ("read-search", ("read", "search", "grep", "find", "lookup", "trace")),
        ("build", ("build", "compile", "release build", "debug build", "artifact")),
        ("mutation", ("edit", "change", "modify", "rewrite", "refactor", "rename", "move", "add file")),
    ]

    padded = f" {text} "
    for operation_type, needles in checks:
        if any(needle in padded for needle in needles):
            return operation_type
    return None


def load_effective_config() -> dict:
    return customization_config.merge_configs(
        customization_config.load_template(),
        customization_config.load_durable(),
    )


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
            "metal_sources": [],
            "metal_libraries": [],
            "source_targets": [],
            "test_targets": [],
            "mixed_root": False,
            "reason": "repo-root-missing",
        }

    scan_root = package_root or requested_root
    has_package = package_root is not None
    markers: list[str] = []
    for suffix in ("*.xcodeproj", "*.xcworkspace", "*.pbxproj"):
        markers.extend(first_matching_file(scan_root, suffix))
    sources_dir = scan_root / "Sources"
    tests_dir = scan_root / "Tests"
    source_targets = sorted(path.name for path in sources_dir.iterdir() if path.is_dir()) if sources_dir.exists() else []
    test_targets = sorted(path.name for path in tests_dir.iterdir() if path.is_dir()) if tests_dir.exists() else []
    xctestplans = first_matching_file(scan_root, "*.xctestplan")
    metal_sources = first_matching_file(scan_root, "*.metal")
    metal_libraries = first_matching_file(scan_root, "*.metallib")

    return {
        "requested_root": str(requested_root),
        "repo_root": str(scan_root),
        "exists": True,
        "has_package": has_package,
        "xcode_markers": markers,
        "xctestplans": xctestplans,
        "metal_sources": metal_sources,
        "metal_libraries": metal_libraries,
        "source_targets": source_targets,
        "test_targets": test_targets,
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


def request_mentions_resources(request: str | None) -> bool:
    text = normalize_request_text(request)
    padded = f" {text} "
    return any(
        needle in padded
        for needle in (
            " resource",
            " resources",
            " bundle.module",
            " process(",
            " copy(",
            " embedincode",
            " asset",
            " assets",
            " fixture",
            " fixtures",
            " metallib",
        )
    )


def specialized_handoff(operation_type: str, repo_shape: dict, request: str | None, mixed_root_opt_in: bool) -> tuple[str | None, str | None]:
    text = normalize_request_text(request)
    if repo_shape["mixed_root"] and not mixed_root_opt_in:
        skill = "xcode-build-run-workflow" if operation_type != "test" else "xcode-testing-workflow"
        return skill, f"Use {skill} because this repo root is mixed and Xcode-managed behavior may matter."
    if operation_type != "test":
        if repo_shape["metal_sources"] and any(
            token in text
            for token in (" metal ", " shader", " compile metal", " build metal", " metal toolchain", " metallib")
        ):
            return "xcode-build-run-workflow", "Use xcode-build-run-workflow because this request touches Metal compilation or Apple-managed Metal toolchain behavior."
        if repo_shape["xcode_markers"] and any(
            token in text
            for token in (" xcode target", " target membership", " build phase", " resource inclusion", " copy into app", " bundle in app")
        ):
            return "xcode-build-run-workflow", "Use xcode-build-run-workflow because this package-resource request is crossing into Xcode-managed target or bundle integration."
    if operation_type == "test" and repo_shape["xctestplans"] and "test plan" in text:
        return "xcode-testing-workflow", "Use xcode-testing-workflow because this package repo already carries .xctestplan coverage and the request is crossing into Xcode-managed test-plan behavior."
    return None, None


def recommended_skill(operation_type: str) -> str:
    if operation_type == "test":
        return "swift-package-testing-workflow"
    return "swift-package-build-run-workflow"


def routing_summary(operation_type: str, repo_shape: dict, request: str | None) -> str:
    resource_focused = request_mentions_resources(request)
    target = repo_shape["source_targets"][0] if len(repo_shape["source_targets"]) == 1 else None
    if operation_type == "test":
        if repo_shape["xctestplans"]:
            return "Package testing request with existing .xctestplan context; prefer the narrower testing skill so it can decide whether plain swift test or Xcode-native test-plan handling is the better fit."
        return "Package testing request; prefer the narrower testing skill so Swift Testing, XCTest holdouts, fixtures, and flake diagnosis stay in one place."
    if operation_type in {"build", "run", "manifest-dependencies", "plugin", "toolchain-management", "mutation"}:
        if resource_focused and repo_shape["xcode_markers"]:
            return "Package resource request with nearby Xcode markers; prefer the narrower build-run skill so it can either stay on SwiftPM or escalate cleanly into Xcode-managed bundle integration."
        if resource_focused:
            return "Package resource request; prefer the narrower build-run skill so Bundle.module, Package.swift resources, fixtures, and Metal-distribution checks stay with the real execution owner."
        if repo_shape["metal_sources"] or repo_shape["metal_libraries"]:
            return "Package build-run request with Metal-related signals; prefer the narrower build-run skill so SwiftPM-first behavior and Xcode-aware Metal escalation stay consistent."
        if target:
            return f"Package execution request with a single inferred source target `{target}`; prefer the narrower build-run skill so target-aware planning happens in the long-term owner."
        return "Package build-run request; prefer the narrower build-run skill so manifest, dependency, plugin, and execution guidance stays in the long-term owner."
    return "Broad package request; prefer the narrower package skill that owns the actual execution path."


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
                "routing_summary": None,
                "next_step": "Pass --operation-type explicitly or provide --request text that makes the intended SwiftPM workflow obvious.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    repo_shape = discover_repo_shape(args.repo_root)
    status = "handoff"
    path_type = "primary"
    recommended = recommended_skill(operation_type)
    next_step = f"Use {recommended} because the package execution surface is now split by build/run versus testing."

    if not repo_shape["exists"]:
        status = "blocked"
        recommended = None
        next_step = "Resolve the repo root before continuing."
    elif not repo_shape["has_package"]:
        status = "blocked"
        recommended = None
        next_step = "Use a Swift package repo with Package.swift at the selected root."
    else:
        specialized_skill, specialized_next_step = specialized_handoff(
            operation_type,
            repo_shape,
            args.request,
            args.mixed_root_opt_in,
        )
        if specialized_skill:
            recommended = specialized_skill
            next_step = specialized_next_step

    payload = {
        "status": status,
        "path_type": path_type,
        "output": {
            "operation_type": operation_type,
            "operation_type_source": "explicit" if args.operation_type else "inferred",
            "repo_shape": repo_shape,
            "routing_summary": routing_summary(operation_type, repo_shape, args.request),
            "inferred_context": {
                "package_name": inferred_package_name(repo_shape),
                "primary_target": repo_shape["source_targets"][0] if len(repo_shape["source_targets"]) == 1 else None,
                "has_xcode_test_plan": bool(repo_shape["xctestplans"]),
                "has_metal_sources": bool(repo_shape["metal_sources"]),
                "has_bundled_metallib": bool(repo_shape["metal_libraries"]),
                "resource_request": request_mentions_resources(args.request),
            },
            "recommended_skill": recommended,
            "next_step": next_step,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status != "blocked" else 1


if __name__ == "__main__":
    sys.exit(main())
