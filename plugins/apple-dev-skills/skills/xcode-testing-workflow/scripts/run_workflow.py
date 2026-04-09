#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Runtime workflow policy engine for xcode-testing-workflow."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

import customization_config


VALID_OPERATION_TYPES = {
    "workspace-inspection",
    "session-inspection",
    "read-search-diagnostics",
    "test",
    "mutation",
}


def normalize_request_text(text: str | None) -> str:
    return " ".join((text or "").strip().lower().split())


def infer_operation_type_from_request(request: str | None) -> str | None:
    text = normalize_request_text(request)
    if not text:
        return None

    padded = f" {text} "
    if any(
        needle in padded
        for needle in (
            " build",
            " compile",
            " archive",
            " release build",
            " debug build",
            " artifact",
            " run",
            " launch",
            " preview",
            " simulator",
            " device",
            " xcrun",
            " toolchain",
            " xcode-select",
            " metal toolchain",
            " sdk",
            " package resolve",
        )
    ):
        return "build"

    checks: list[tuple[str, tuple[str, ...]]] = [
        ("test", (" test", " tests", "testing", "xctest", "xcuitest", "ui test", "ui tests", "xctestplan")),
        ("read-search-diagnostics", ("diagnostic", "diagnostics", "error", "warning", "issue", "issues", "grep", "search", "find", "read", "navigator", "flake")),
        ("workspace-inspection", ("workspace", "scheme list", "inspect project", "inspect workspace", "session")),
        ("mutation", ("edit test", "change test", "modify test", "rewrite test", "refactor test", "rename test", "move test", "add test", "fix test", "pbxproj")),
    ]
    for operation_type, needles in checks:
        if any(needle in padded for needle in needles):
            return operation_type
    return None


def load_effective_config() -> dict:
    return customization_config.merge_configs(
        customization_config.load_template(),
        customization_config.load_durable(),
    )


def detect_managed_scope(workspace_path: str | None) -> dict:
    if not workspace_path:
        return {"managed": False, "path": None, "markers": [], "reason": "workspace-path-missing"}

    script_path = Path(__file__).with_name("detect_xcode_managed_scope.sh")
    proc = subprocess.run(
        [str(script_path), workspace_path],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        payload = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        payload = {
            "managed": False,
            "path": workspace_path,
            "markers": [],
            "reason": "scope-detection-json-error",
        }
    if proc.returncode != 0 and "reason" not in payload:
        payload["reason"] = "scope-detection-failed"
    return payload


def discover_workspace_state(workspace_path: str | None) -> dict:
    if not workspace_path:
        return {
            "workspace": None,
            "project": None,
            "swift_package": False,
            "requested_root": None,
            "resolved_root": None,
            "xctestplans": [],
            "scheme_hints": [],
            "test_targets": [],
            "ui_test_targets": [],
        }

    requested = Path(workspace_path).expanduser().resolve()
    existing = requested
    while not existing.exists() and existing != existing.parent:
        existing = existing.parent
    if not existing.exists():
        return {
            "workspace": None,
            "project": None,
            "swift_package": False,
            "requested_root": str(requested),
            "resolved_root": None,
            "xctestplans": [],
            "scheme_hints": [],
            "test_targets": [],
            "ui_test_targets": [],
        }

    candidate = existing if existing.is_dir() else existing.parent
    direct_workspace = requested if requested.suffix == ".xcworkspace" else None
    direct_project = requested if requested.suffix == ".xcodeproj" else None

    parent_workspace = None
    parent_project = None
    for current in (candidate, *candidate.parents):
        if not parent_workspace:
            matches = sorted(current.glob("*.xcworkspace"))
            if matches:
                parent_workspace = matches[0]
        if not parent_project:
            matches = sorted(current.glob("*.xcodeproj"))
            if matches:
                parent_project = matches[0]
        if parent_workspace or parent_project:
            break

    scan_root = candidate
    workspace = direct_workspace or parent_workspace
    project = direct_project or parent_project
    if workspace:
        scan_root = workspace.parent
    elif project:
        scan_root = project.parent

    if not workspace:
        descendants = sorted(scan_root.rglob("*.xcworkspace"), key=str)
        if descendants:
            workspace = descendants[0]
            scan_root = workspace.parent
    if not project:
        descendants = sorted(scan_root.rglob("*.xcodeproj"), key=str)
        if descendants:
            project = descendants[0]
            if not workspace:
                scan_root = project.parent

    xctestplans = sorted(str(path) for path in scan_root.rglob("*.xctestplan"))
    test_root = scan_root / "Tests"
    test_targets = sorted(path.name for path in test_root.iterdir() if path.is_dir()) if test_root.exists() else []
    ui_test_targets = sorted(name for name in test_targets if "UI" in name or "UITest" in name)
    scheme_hints = []
    if workspace:
        scheme_hints.append(workspace.stem)
    if project:
        scheme_hints.append(project.stem)
    scheme_hints.extend(Path(path).stem for path in xctestplans)
    scheme_hints = sorted(dict.fromkeys(scheme_hints))
    swift_package = any((current / "Package.swift").exists() for current in (scan_root, *scan_root.parents))
    return {
        "requested_root": str(requested),
        "resolved_root": str(scan_root),
        "workspace": str(workspace) if workspace else None,
        "project": str(project) if project else None,
        "swift_package": swift_package,
        "xctestplans": xctestplans,
        "scheme_hints": scheme_hints,
        "test_targets": test_targets,
        "ui_test_targets": ui_test_targets,
    }


def shell_join(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def inferred_scheme(state: dict) -> str:
    hints = state.get("scheme_hints", [])
    return hints[0] if hints else "<scheme>"


def build_fallback_commands(operation_type: str, workspace_path: str | None, mapping_profile: str) -> list[str]:
    state = discover_workspace_state(workspace_path)
    commands: list[str] = []
    include_swift_package = mapping_profile != "xcode-only"
    scheme = inferred_scheme(state)

    if operation_type in {"workspace-inspection", "session-inspection", "read-search-diagnostics"}:
        if state["workspace"]:
            commands.append(shell_join(["xcodebuild", "-workspace", state["workspace"], "-list"]))
            commands.append(shell_join(["xcodebuild", "-workspace", state["workspace"], "-showTestPlans", "-scheme", scheme]))
        if state["project"]:
            commands.append(shell_join(["xcodebuild", "-project", state["project"], "-list"]))
        if include_swift_package and state["swift_package"]:
            commands.append("swift package describe")
    elif operation_type == "test":
        if state["workspace"]:
            commands.append(shell_join(["xcodebuild", "-workspace", state["workspace"], "-showTestPlans", "-scheme", scheme]))
            commands.append(
                shell_join(
                    [
                        "xcodebuild",
                        "test",
                        "-workspace",
                        state["workspace"],
                        "-scheme",
                        scheme,
                        "-destination",
                        "<destination>",
                    ]
                )
            )
            if state["xctestplans"]:
                commands.append(
                    shell_join(
                        [
                            "xcodebuild",
                            "test",
                            "-workspace",
                            state["workspace"],
                            "-scheme",
                            scheme,
                            "-testPlan",
                            Path(state["xctestplans"][0]).stem,
                            "-destination",
                            "<destination>",
                        ]
                    )
                )
        if state["project"]:
            commands.append(
                shell_join(
                    [
                        "xcodebuild",
                        "test",
                        "-project",
                        state["project"],
                        "-scheme",
                        scheme,
                        "-destination",
                        "<destination>",
                    ]
                )
            )
        if include_swift_package and state["swift_package"]:
            commands.append("swift test")
    elif operation_type == "mutation":
        commands.append("Verify the affected test target, test plan, and target membership after filesystem edits.")
        if state["workspace"]:
            commands.append(
                shell_join(
                    [
                        "xcodebuild",
                        "test",
                        "-workspace",
                        state["workspace"],
                        "-scheme",
                        scheme,
                        "-destination",
                        "<destination>",
                    ]
                )
            )
    return commands


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation-type", choices=sorted(VALID_OPERATION_TYPES))
    parser.add_argument("--request")
    parser.add_argument("--workspace-path")
    parser.add_argument("--tab-identifier")
    parser.add_argument("--mcp-failure-reason")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--direct-pbxproj-edit", action="store_true")
    parser.add_argument("--direct-pbxproj-edit-opt-in", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_effective_config()
    settings = config["settings"]
    inferred_operation_type = infer_operation_type_from_request(args.request)
    operation_type = args.operation_type or inferred_operation_type

    if operation_type is None:
        payload = {
            "status": "blocked",
            "path_type": "primary",
            "output": {
                "operation_type": None,
                "operation_type_source": "missing",
                "workspace_path": args.workspace_path,
                "tab_identifier": args.tab_identifier,
                "mcp_failure_reason": args.mcp_failure_reason,
                "guard_result": {
                    "applied": False,
                    "managed_scope": False,
                    "reason": "not-applicable",
                },
                "fallback_commands": [],
                "retry_count": int(settings.get("mcpRetryCount", 1)),
                "next_step": "Pass --operation-type explicitly or provide --request text that makes the intended Xcode testing workflow obvious.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if operation_type == "build":
        payload = {
            "status": "handoff",
            "path_type": "primary",
            "output": {
                "operation_type": "build-or-run",
                "operation_type_source": "explicit" if args.operation_type else "inferred",
                "workspace_path": args.workspace_path,
                "tab_identifier": args.tab_identifier,
                "mcp_failure_reason": args.mcp_failure_reason,
                "guard_result": {
                    "applied": False,
                    "managed_scope": False,
                    "reason": "build-run-handoff",
                },
                "fallback_commands": [],
                "retry_count": int(settings.get("mcpRetryCount", 1)),
                "next_step": "Use xcode-build-run-workflow because this request is primarily about build, run, previews, toolchain, or project-integrity work.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    workspace_state = discover_workspace_state(args.workspace_path)
    fallback_commands = build_fallback_commands(
        operation_type,
        args.workspace_path,
        str(settings.get("fallbackCommandMappingProfile", "official-default")),
    )

    guard_result = {
        "applied": False,
        "managed_scope": False,
        "direct_edits_allowed": True,
        "direct_pbxproj_edit_warning_required": False,
        "reason": "not-applicable",
    }
    status = "success"
    path_type = "primary"
    next_step = "Proceed with the agent-side MCP path."

    if operation_type == "mutation":
        scope = detect_managed_scope(args.workspace_path)
        markers = scope.get("markers", [])
        has_pbxproj_marker = any(str(marker).endswith(".pbxproj") for marker in markers)
        guard_result = {
            "applied": True,
            "managed_scope": bool(scope.get("managed")),
            "direct_edits_allowed": True,
            "direct_pbxproj_edit_warning_required": False,
            "reason": "ordinary-direct-edits-allowed",
            "markers": markers,
        }
        if args.direct_pbxproj_edit or has_pbxproj_marker:
            guard_result["direct_pbxproj_edit_warning_required"] = True
            guard_result["reason"] = "direct-pbxproj-edit-warning-required"
            if args.direct_pbxproj_edit and not args.direct_pbxproj_edit_opt_in:
                status = "blocked"
                next_step = "Warn the user about direct .pbxproj edit risks and rerun with --direct-pbxproj-edit-opt-in only if they explicitly approve that path."

    if args.mcp_failure_reason and status != "blocked":
        path_type = "fallback"
        next_step = (
            f"Use the first documented fallback command because MCP reported {args.mcp_failure_reason}."
            if fallback_commands
            else "No documented CLI fallback is available for this operation type."
        )

    payload = {
        "status": status,
        "path_type": path_type,
        "output": {
            "operation_type": operation_type,
            "operation_type_source": "explicit" if args.operation_type else "inferred",
            "workspace_path": args.workspace_path,
            "workspace_state": workspace_state,
            "tab_identifier": args.tab_identifier,
            "mcp_failure_reason": args.mcp_failure_reason,
            "guard_result": guard_result,
            "fallback_commands": fallback_commands,
            "inferred_context": {
                "scheme_hint": inferred_scheme(workspace_state),
                "has_xcode_test_plan": bool(workspace_state.get("xctestplans")),
                "ui_test_targets": workspace_state.get("ui_test_targets"),
                "primary_test_target": (
                    workspace_state.get("test_targets", [None])[0]
                    if len(workspace_state.get("test_targets", [])) == 1
                    else None
                ),
            },
            "retry_count": int(settings.get("mcpRetryCount", 1)),
            "next_step": next_step,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status != "blocked" else 1


if __name__ == "__main__":
    sys.exit(main())
