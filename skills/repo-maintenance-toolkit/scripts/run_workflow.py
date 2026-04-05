#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Unified runtime entrypoint for repo-maintenance-toolkit."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root")
    parser.add_argument("--operation", choices=("install", "refresh", "report-only"))
    parser.add_argument("--skip-github-workflow", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = str(Path(args.repo_root or ".").expanduser().resolve())
    operation = args.operation or "install"
    normalized_inputs = {
        "repo_root": repo_root,
        "operation": operation,
        "skip_github_workflow": args.skip_github_workflow,
        "dry_run": args.dry_run,
    }

    helper_path = Path(__file__).with_name("install_repo_maintenance_toolkit.py")
    command = [
        str(helper_path),
        "--repo-root",
        repo_root,
        "--operation",
        operation,
    ]
    if args.skip_github_workflow:
        command.append("--skip-github-workflow")
    if args.dry_run:
        command.append("--dry-run")

    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    payload = json.loads(proc.stdout) if proc.stdout.strip() else {
        "status": "failed",
        "path_type": "primary",
        "repo_root": repo_root,
        "normalized_inputs": normalized_inputs,
        "managed_files": [],
        "actions": [],
        "validation_result": None,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "next_step": "Fix the repo-maintenance toolkit workflow error and rerun the workflow.",
    }
    payload.setdefault("normalized_inputs", normalized_inputs)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
