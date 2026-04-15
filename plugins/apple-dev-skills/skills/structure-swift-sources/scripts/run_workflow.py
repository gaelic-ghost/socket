#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Runtime workflow policy engine for structure-swift-sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import customization_config


VALID_REPOSITORY_KINDS = {"swift-package", "xcode-app-project", "mixed"}
VALID_CLEANUP_KINDS = {
    "repo-layout-cleanup",
    "large-file-split",
    "section-and-mark-normalization",
    "file-header-normalization",
    "todo-fixme-ledger-extraction",
    "combined-source-hygiene-pass",
}
VALID_SPLIT_MODES = {"advisory", "required", "full-pass"}
VALID_TODO_FIXME_MODES = {"report-only", "rewrite-ledgers", "normalize-existing"}
VALID_FILE_HEADER_MODES = {"advisory", "required"}
VALID_FILE_HEADER_STYLES = {"plain-block"}


def normalize_request_text(text: str | None) -> str:
    return " ".join((text or "").strip().lower().split())


def request_implies_docc_work(text: str) -> bool:
    needles = (
        "docc",
        "symbol docs",
        "symbol documentation",
        "doc comments",
        "parameter docs",
        "landing page",
        "topic group",
        "docc review",
    )
    return any(needle in text for needle in needles)


def request_implies_xcode_execution_handoff(text: str) -> bool:
    needles = (
        "target membership",
        "add to target",
        "remove from target",
        "xcode target",
        "pbxproj",
        "project membership",
        "file membership",
        "scheme validation",
    )
    return any(needle in text for needle in needles)


def infer_cleanup_kind(request: str | None) -> str | None:
    text = normalize_request_text(request)
    if not text:
        return None

    hits: list[str] = []

    if any(token in text for token in ("layout", "reorganize", "move files", "directory shape", "repo shape")):
        hits.append("repo-layout-cleanup")
    if any(token in text for token in ("split", "oversized file", "too large", "extension file")):
        hits.append("large-file-split")
    if any(token in text for token in ("mark", "// mark", "section group", "declaration grouping")):
        hits.append("section-and-mark-normalization")
    if any(token in text for token in ("file header", "header comment", "block-comment header", "purpose header", "concern header")):
        hits.append("file-header-normalization")
    if "todo" in text or "fixme" in text or "ledger" in text:
        hits.append("todo-fixme-ledger-extraction")

    unique_hits = sorted(set(hits))
    if not unique_hits:
        return None
    if len(unique_hits) > 1:
        return "combined-source-hygiene-pass"
    return unique_hits[0]


def detect_repo_state(repo_path: str | None) -> dict:
    if not repo_path:
        return {
            "requested_root": None,
            "resolved_root": None,
            "package_manifest": None,
            "workspace": None,
            "project": None,
            "swift_files": 0,
            "mixed_root": False,
        }

    requested = Path(repo_path).expanduser().resolve()
    existing = requested
    while not existing.exists() and existing != existing.parent:
        existing = existing.parent
    if not existing.exists():
        return {
            "requested_root": str(requested),
            "resolved_root": None,
            "package_manifest": None,
            "workspace": None,
            "project": None,
            "swift_files": 0,
            "mixed_root": False,
        }

    candidate = existing if existing.is_dir() else existing.parent
    package_manifest = candidate / "Package.swift"
    workspaces = sorted(candidate.rglob("*.xcworkspace"), key=str)
    projects = sorted(candidate.rglob("*.xcodeproj"), key=str)
    swift_files = [
        path for path in candidate.rglob("*.swift") if path.name != "Package.swift" and ".build" not in path.parts
    ]
    return {
        "requested_root": str(requested),
        "resolved_root": str(candidate),
        "package_manifest": str(package_manifest) if package_manifest.exists() else None,
        "workspace": str(workspaces[0]) if workspaces else None,
        "project": str(projects[0]) if projects else None,
        "swift_files": len(swift_files),
        "mixed_root": bool(package_manifest.exists() and (workspaces or projects)),
    }


def infer_repository_kind(repo_state: dict, request: str | None) -> str | None:
    if repo_state.get("mixed_root"):
        return "mixed"
    if repo_state.get("workspace") or repo_state.get("project"):
        return "xcode-app-project"
    if repo_state.get("package_manifest"):
        return "swift-package"

    text = normalize_request_text(request)
    if "swift package" in text or "package.swift" in text or "swiftpm" in text:
        return "swift-package"
    if "xcode" in text or ".xcodeproj" in text or "workspace" in text:
        return "xcode-app-project"
    return None


def load_effective_config() -> dict:
    effective = customization_config.merge_configs(
        customization_config.load_template(),
        customization_config.load_durable(),
    )
    customization_config.validate_config(effective, allow_partial=False)
    return effective


def validated_runtime_settings() -> dict:
    settings = load_effective_config().get("settings", {})
    file_header_mode = str(settings.get("fileHeaderMode", "advisory"))
    file_header_style = str(settings.get("fileHeaderStyle", "plain-block"))
    try:
        split_soft_limit = int(settings.get("splitSoftLimit", 400))
        split_hard_limit = int(settings.get("splitHardLimit", 800))
    except (TypeError, ValueError):
        split_soft_limit = 400
        split_hard_limit = 800

    if file_header_mode not in VALID_FILE_HEADER_MODES:
        file_header_mode = "advisory"
    if file_header_style not in VALID_FILE_HEADER_STYLES:
        file_header_style = "plain-block"
    if split_soft_limit < 1:
        split_soft_limit = 400
    if split_hard_limit <= split_soft_limit:
        split_hard_limit = max(split_soft_limit + 1, 800)

    return {
        "fileHeaderMode": file_header_mode,
        "fileHeaderStyle": file_header_style,
        "splitSoftLimit": split_soft_limit,
        "splitHardLimit": split_hard_limit,
    }


def helper_scripts_for(cleanup_kind: str) -> list[str]:
    helpers = ["scripts/run_workflow.py"]
    if cleanup_kind in {"file-header-normalization", "combined-source-hygiene-pass"}:
        helpers.append("scripts/normalize_swift_file_headers.py")
    if cleanup_kind in {"todo-fixme-ledger-extraction", "combined-source-hygiene-pass"}:
        helpers.append("scripts/normalize_todo_fixme_ledgers.py")
    return helpers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-path")
    parser.add_argument("--repository-kind", choices=sorted(VALID_REPOSITORY_KINDS))
    parser.add_argument("--cleanup-kind", choices=sorted(VALID_CLEANUP_KINDS))
    parser.add_argument("--target-scope")
    parser.add_argument("--split-mode", choices=sorted(VALID_SPLIT_MODES))
    parser.add_argument("--todo-fixme-mode", choices=sorted(VALID_TODO_FIXME_MODES))
    parser.add_argument("--request")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    settings = validated_runtime_settings()
    repo_state = detect_repo_state(args.repo_path)
    repository_kind = args.repository_kind or infer_repository_kind(repo_state, args.request)
    repository_kind_source = "explicit" if args.repository_kind else ("inferred" if repository_kind else "missing")
    cleanup_kind = args.cleanup_kind or infer_cleanup_kind(args.request)
    cleanup_kind_source = "explicit" if args.cleanup_kind else ("inferred" if cleanup_kind else "missing")
    request_text = normalize_request_text(args.request)

    if request_implies_docc_work(request_text):
        payload = {
            "status": "handoff",
            "path_type": "primary",
            "output": {
                "repository_kind": repository_kind,
                "repository_kind_source": repository_kind_source,
                "cleanup_kind": cleanup_kind,
                "cleanup_kind_source": cleanup_kind_source,
                "repo_state": repo_state,
                "header_policy": {
                    "mode": settings["fileHeaderMode"],
                    "style": settings["fileHeaderStyle"],
                },
                "split_thresholds": {
                    "soft_limit": settings["splitSoftLimit"],
                    "hard_limit": settings["splitHardLimit"],
                },
                "helper_scripts": helper_scripts_for(cleanup_kind or "combined-source-hygiene-pass"),
                "recommended_skill": "author-swift-docc-docs",
                "next_step": "Use author-swift-docc-docs because this request is about symbol docs or DocC content rather than file layout and source-structure cleanup.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if request_implies_xcode_execution_handoff(request_text):
        payload = {
            "status": "handoff",
            "path_type": "primary" if repository_kind_source != "missing" else "fallback",
            "output": {
                "repository_kind": repository_kind,
                "repository_kind_source": repository_kind_source,
                "cleanup_kind": cleanup_kind,
                "cleanup_kind_source": cleanup_kind_source,
                "repo_state": repo_state,
                "header_policy": {
                    "mode": settings["fileHeaderMode"],
                    "style": settings["fileHeaderStyle"],
                },
                "split_thresholds": {
                    "soft_limit": settings["splitSoftLimit"],
                    "hard_limit": settings["splitHardLimit"],
                },
                "helper_scripts": helper_scripts_for(cleanup_kind or "combined-source-hygiene-pass"),
                "recommended_skill": "xcode-build-run-workflow",
                "next_step": "Use xcode-build-run-workflow because this request touches target membership, project membership, or other Xcode-managed project-integrity follow-through.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if cleanup_kind is None:
        payload = {
            "status": "blocked",
            "path_type": "fallback" if repository_kind_source != "missing" else "primary",
            "output": {
                "repository_kind": repository_kind,
                "repository_kind_source": repository_kind_source,
                "cleanup_kind": cleanup_kind,
                "cleanup_kind_source": cleanup_kind_source,
                "repo_state": repo_state,
                "header_policy": {
                    "mode": settings["fileHeaderMode"],
                    "style": settings["fileHeaderStyle"],
                },
                "split_thresholds": {
                    "soft_limit": settings["splitSoftLimit"],
                    "hard_limit": settings["splitHardLimit"],
                },
                "helper_scripts": ["scripts/run_workflow.py"],
                "recommended_skill": None,
                "next_step": "Pass --cleanup-kind explicitly or describe whether you need repo layout cleanup, large-file splitting, MARK normalization, file-header normalization, TODO/FIXME ledger extraction, or a combined hygiene pass.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if repository_kind is None:
        payload = {
            "status": "blocked",
            "path_type": "fallback",
            "output": {
                "repository_kind": repository_kind,
                "repository_kind_source": repository_kind_source,
                "cleanup_kind": cleanup_kind,
                "cleanup_kind_source": cleanup_kind_source,
                "repo_state": repo_state,
                "header_policy": {
                    "mode": settings["fileHeaderMode"],
                    "style": settings["fileHeaderStyle"],
                },
                "split_thresholds": {
                    "soft_limit": settings["splitSoftLimit"],
                    "hard_limit": settings["splitHardLimit"],
                },
                "helper_scripts": helper_scripts_for(cleanup_kind),
                "recommended_skill": None,
                "next_step": "Provide --repository-kind explicitly or point --repo-path at the package or Xcode repository before running a structural-cleanup workflow that depends on repo shape.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    target_scope = args.target_scope or "repo-root"
    split_mode = args.split_mode or ("full-pass" if cleanup_kind == "combined-source-hygiene-pass" else "advisory")
    todo_fixme_mode = args.todo_fixme_mode or (
        "report-only" if cleanup_kind != "todo-fixme-ledger-extraction" else "normalize-existing"
    )
    recommended_path = (
        "Use format-swift-sources first, then apply the structure references for the resolved cleanup kind, "
        "use deterministic helpers only where the skill documents them, and finish by returning to format-swift-sources."
    )
    next_step = "Stay in structure-swift-sources and apply the resolved structure rules locally."
    if cleanup_kind == "file-header-normalization":
        next_step = (
            "Audit headers with scripts/normalize_swift_file_headers.py first, then apply header normalization "
            "with an explicit inventory when you already have trusted purpose and concern text."
        )
    elif cleanup_kind == "todo-fixme-ledger-extraction":
        next_step = "Run scripts/normalize_todo_fixme_ledgers.py in report mode first, then apply when the references are clean."

    payload = {
        "status": "success",
        "path_type": "primary" if repository_kind_source != "missing" else "fallback",
        "output": {
            "repository_kind": repository_kind,
            "repository_kind_source": repository_kind_source,
            "cleanup_kind": cleanup_kind,
            "cleanup_kind_source": cleanup_kind_source,
            "repo_state": repo_state,
            "target_scope": target_scope,
            "split_mode": split_mode,
            "todo_fixme_mode": todo_fixme_mode,
            "recommended_path": recommended_path,
            "header_policy": {
                "mode": settings["fileHeaderMode"],
                "style": settings["fileHeaderStyle"],
            },
            "split_thresholds": {
                "soft_limit": settings["splitSoftLimit"],
                "hard_limit": settings["splitHardLimit"],
            },
            "helper_scripts": helper_scripts_for(cleanup_kind),
            "verification": "Finish by returning to format-swift-sources so the moved, split, or header-normalized files end in a clean formatting state.",
            "next_step": next_step,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
