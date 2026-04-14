#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Runtime workflow policy engine for docc-workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import customization_config


VALID_REPO_SHAPES = {"swift-package", "xcode-app-framework"}
VALID_TASK_TYPES = {
    "symbol-docs",
    "article",
    "structure",
    "review",
    "tutorial-aware-review",
}
VALID_TUTORIAL_LEVELS = {"light-review", "defer"}


def normalize_request_text(text: str | None) -> str:
    return " ".join((text or "").strip().lower().split())


def request_implies_docs_lookup(text: str) -> bool:
    needles = (
        "search docs",
        "look up docs",
        "find docs",
        "wwdc",
        "apple docs",
        "swift.org docs",
        "directive reference",
        "which directive",
        "documentationsearch",
    )
    return any(needle in text for needle in needles)


def request_implies_execution(text: str) -> bool:
    needles = (
        "docbuild",
        "xcodebuild",
        "build documentation",
        "generate archive",
        "doccarchive",
        "export docs",
        "publish docs",
        "host docs",
        "archive export",
    )
    return any(needle in text for needle in needles)


def infer_task_type_from_request(request: str | None) -> str | None:
    text = normalize_request_text(request)
    if not text:
        return None

    if "tutorial" in text or "guided learning" in text or "walkthrough" in text:
        return "tutorial-aware-review"
    if "topic group" in text or "landing page" in text or "extension file" in text or "catalog structure" in text:
        return "structure"
    if "article" in text or "overview page" in text or "conceptual page" in text:
        return "article"
    if "symbol" in text or "doc comment" in text or "parameter docs" in text or "return docs" in text or "inline comments" in text:
        return "symbol-docs"
    if "review" in text or "accuracy" in text or "correctness" in text or "clarity" in text:
        return "review"
    return None


def detect_repo_state(repo_path: str | None) -> dict:
    if not repo_path:
        return {
            "requested_root": None,
            "resolved_root": None,
            "package_manifest": None,
            "workspace": None,
            "project": None,
            "docc_catalogs": [],
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
            "docc_catalogs": [],
            "mixed_root": False,
        }

    candidate = existing if existing.is_dir() else existing.parent
    package_manifest = candidate / "Package.swift"
    workspaces = sorted(candidate.rglob("*.xcworkspace"), key=str)
    projects = sorted(candidate.rglob("*.xcodeproj"), key=str)
    docc_catalogs = sorted(str(path) for path in candidate.rglob("*.docc"))
    return {
        "requested_root": str(requested),
        "resolved_root": str(candidate),
        "package_manifest": str(package_manifest) if package_manifest.exists() else None,
        "workspace": str(workspaces[0]) if workspaces else None,
        "project": str(projects[0]) if projects else None,
        "docc_catalogs": docc_catalogs,
        "mixed_root": bool(package_manifest.exists() and (workspaces or projects)),
    }


def infer_repo_shape(repo_state: dict, request: str | None) -> str | None:
    if repo_state.get("workspace") or repo_state.get("project"):
        return "xcode-app-framework"
    if repo_state.get("package_manifest"):
        return "swift-package"

    text = normalize_request_text(request)
    if "package.swift" in text or "swift package" in text or "swiftpm" in text:
        return "swift-package"
    if "xcode" in text or "workspace" in text or "scheme" in text or ".xcodeproj" in text:
        return "xcode-app-framework"
    return None


def load_effective_config() -> dict:
    return customization_config.merge_configs(
        customization_config.load_template(),
        customization_config.load_durable(),
    )


def recommended_execution_skill(repo_shape: str | None) -> str | None:
    if repo_shape == "swift-package":
        return "swift-package-build-run-workflow"
    if repo_shape == "xcode-app-framework":
        return "xcode-build-run-workflow"
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-path")
    parser.add_argument("--repo-shape", choices=sorted(VALID_REPO_SHAPES))
    parser.add_argument("--task-type", choices=sorted(VALID_TASK_TYPES))
    parser.add_argument("--request")
    parser.add_argument("--needs-generation", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    settings = load_effective_config().get("settings", {})
    tutorial_support_level = str(settings.get("tutorialSupportLevel", "light-review"))
    if tutorial_support_level not in VALID_TUTORIAL_LEVELS:
        tutorial_support_level = "light-review"

    repo_state = detect_repo_state(args.repo_path)
    repo_shape = args.repo_shape or infer_repo_shape(repo_state, args.request)
    repo_shape_source = "explicit" if args.repo_shape else ("inferred" if repo_shape else "missing")
    task_type = args.task_type or infer_task_type_from_request(args.request)
    task_type_source = "explicit" if args.task_type else ("inferred" if task_type else "missing")
    text = normalize_request_text(args.request)

    if request_implies_docs_lookup(text):
        payload = {
            "status": "handoff",
            "path_type": "primary",
            "output": {
                "repo_shape": repo_shape,
                "repo_shape_source": repo_shape_source,
                "task_type": task_type,
                "task_type_source": task_type_source,
                "repo_state": repo_state,
                "tutorial_support_level": tutorial_support_level,
                "correctness_model": ["content", "docc", "project"],
                "recommended_skill": "explore-apple-swift-docs",
                "next_step": "Use explore-apple-swift-docs because this request is primarily about finding DocC or Apple documentation rather than authoring or reviewing DocC content.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.needs_generation or request_implies_execution(text):
        recommended = recommended_execution_skill(repo_shape)
        if not recommended:
            payload = {
                "status": "blocked",
                "path_type": "fallback",
                "output": {
                    "repo_shape": repo_shape,
                    "repo_shape_source": repo_shape_source,
                    "task_type": task_type,
                    "task_type_source": task_type_source,
                    "repo_state": repo_state,
                    "tutorial_support_level": tutorial_support_level,
                    "correctness_model": ["content", "docc", "project"],
                    "recommended_skill": None,
                    "next_step": "Provide --repo-shape explicitly or point --repo-path at the package or Xcode repo before handing DocC generation or export work to a build-run workflow.",
                },
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

        payload = {
            "status": "handoff",
            "path_type": "primary" if repo_shape_source != "missing" else "fallback",
            "output": {
                "repo_shape": repo_shape,
                "repo_shape_source": repo_shape_source,
                "task_type": task_type,
                "task_type_source": task_type_source,
                "repo_state": repo_state,
                "tutorial_support_level": tutorial_support_level,
                "correctness_model": ["content", "docc", "project"],
                "recommended_skill": recommended,
                "next_step": f"Use {recommended} because the next step is DocC generation, export, archive, hosting, or other execution-heavy follow-through.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if task_type is None:
        payload = {
            "status": "blocked",
            "path_type": "fallback" if repo_shape_source != "missing" else "primary",
            "output": {
                "repo_shape": repo_shape,
                "repo_shape_source": repo_shape_source,
                "task_type": None,
                "task_type_source": "missing",
                "repo_state": repo_state,
                "tutorial_support_level": tutorial_support_level,
                "correctness_model": ["content", "docc", "project"],
                "recommended_skill": None,
                "next_step": "Pass --task-type explicitly or describe whether you need symbol docs, article work, structure work, review, or tutorial-aware review.",
            },
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    next_step = "Stay in docc-workflow and revise or review the DocC content locally."
    if task_type == "tutorial-aware-review" and tutorial_support_level == "defer":
        next_step = "Keep the tutorial request recognized, but use the fuller DocC references before making directive-specific claims."
    elif task_type == "tutorial-aware-review":
        next_step = "Stay in docc-workflow for a light first-pass tutorial review focused on conceptual flow, and use the fuller DocC references before making directive-specific claims."

    payload = {
        "status": "success",
        "path_type": "primary" if repo_shape_source != "missing" else "fallback",
        "output": {
            "repo_shape": repo_shape,
            "repo_shape_source": repo_shape_source,
            "task_type": task_type,
            "task_type_source": task_type_source,
            "repo_state": repo_state,
            "tutorial_support_level": tutorial_support_level,
            "correctness_model": ["content", "docc", "project"],
            "recommended_skill": None,
            "next_step": next_step,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
