#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Install or refresh repository tooling and canonical project documentation."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root")
    parser.add_argument("--operation", choices=("install", "refresh", "report-only"))
    parser.add_argument("--profile", choices=("generic", "xcode-workspace"))
    parser.add_argument("--skip-github-workflow", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def decode_payload(proc: subprocess.CompletedProcess[str], fallback: dict[str, Any]) -> dict[str, Any]:
    if not proc.stdout.strip():
        return fallback
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            **fallback,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    return payload if isinstance(payload, dict) else fallback


def run_documentation(repo_root: str, run_mode: str) -> tuple[int, dict[str, Any], str]:
    helper_path = Path(__file__).with_name("maintain_project_docs.py")
    command = [
        sys.executable,
        str(helper_path),
        "--project-root",
        repo_root,
        "--run-mode",
        run_mode,
        "--print-json",
    ]
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    fallback = {
        "run_context": {"project_root": repo_root, "run_mode": run_mode},
        "document_order": [],
        "document_reports": [],
        "responsibility_issues": [],
        "fixes_applied": [],
        "post_fix_status": [],
        "errors": ["The integrated documentation workflow did not return JSON output."],
    }
    return proc.returncode, decode_payload(proc, fallback), proc.stderr.strip()


def main() -> int:
    args = build_parser().parse_args()
    repo_root = str(Path(args.repo_root or ".").expanduser().resolve())
    operation = args.operation or "install"
    profile = args.profile or "generic"
    normalized_inputs = {
        "repo_root": repo_root,
        "operation": operation,
        "profile": profile,
        "skip_github_workflow": args.skip_github_workflow,
        "dry_run": args.dry_run,
    }

    helper_path = Path(__file__).with_name("install_maintain_project_repo.py")
    command = [
        str(helper_path),
        "--repo-root",
        repo_root,
        "--operation",
        operation,
        "--profile",
        profile,
    ]
    if args.skip_github_workflow:
        command.append("--skip-github-workflow")
    if args.dry_run:
        command.append("--dry-run")

    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    return_code = proc.returncode
    payload = decode_payload(proc, {
        "status": "failed",
        "path_type": "primary",
        "repo_root": repo_root,
        "normalized_inputs": normalized_inputs,
        "managed_files": [],
        "actions": [],
        "validation_result": None,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "next_step": "Fix the maintain-project-repo workflow error and rerun the workflow.",
    })
    payload.setdefault("normalized_inputs", normalized_inputs)
    if proc.returncode == 0:
        documentation_mode = (
            "check-only"
            if operation == "report-only" or args.dry_run
            else "apply"
        )
        docs_code, docs_payload, docs_stderr = run_documentation(
            repo_root, documentation_mode
        )
        payload["documentation"] = docs_payload
        payload["documentation_result"] = (
            "checked (no writes)"
            if documentation_mode == "check-only"
            else "canonical documents created or refreshed"
        )
        if docs_code != 0:
            payload["status"] = "failed"
            payload["documentation_result"] = "failed after toolkit update"
            existing_stderr = str(payload.get("stderr", "")).strip()
            details = docs_stderr or "The integrated documentation workflow failed."
            payload["stderr"] = "\n".join(
                part for part in (existing_stderr, details) if part
            )
            payload["next_step"] = (
                "Fix the reported documentation workflow error and rerun "
                "maintain-project-repo so tooling and canonical docs agree."
            )
            return_code = 1
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if return_code == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
