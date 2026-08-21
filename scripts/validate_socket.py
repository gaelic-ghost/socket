#!/usr/bin/env python3
"""Run Socket validation profiles without duplicating child-suite ownership."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Check:
    name: str
    command: tuple[str, ...]
    cwd: Path = REPO_ROOT


def root_python(script_name: str) -> tuple[str, ...]:
    return (sys.executable, f"scripts/{script_name}")


CORE_CHECKS = (
    Check("root marketplace metadata", root_python("validate_socket_metadata.py")),
    Check("shared skill metadata", root_python("validate_socket_skill_metadata.py")),
    Check("root tests", (sys.executable, "-m", "pytest")),
    Check("root type checks", (sys.executable, "-m", "mypy")),
    Check("root lint", (sys.executable, "-m", "ruff", "check", "scripts", "tests")),
)
COMPATIBILITY_CHECKS = (
    Check("Hermes compatibility", root_python("validate_hermes_compatibility.py")),
    Check("Claude compatibility", root_python("validate_claude_compatibility.py")),
)
CHILD_CHECKS = (
    Check(
        "Agent Engineering Skills tests",
        ("uv", "run", "pytest"),
        REPO_ROOT / "plugins" / "agent-engineering-skills",
    ),
    Check(
        "Agent Portability Skills tests",
        ("uv", "run", "pytest"),
        REPO_ROOT / "plugins" / "agent-portability-skills",
    ),
    Check(
        "Agent Portability Skills lint",
        ("uv", "run", "ruff", "check", "."),
        REPO_ROOT / "plugins" / "agent-portability-skills",
    ),
    Check(
        "Agent Portability Skills type checks",
        ("uv", "run", "mypy", "."),
        REPO_ROOT / "plugins" / "agent-portability-skills",
    ),
    Check(
        "Apple Dev Skills docs",
        ("bash", ".github/scripts/validate_repo_docs.sh"),
        REPO_ROOT / "plugins" / "apple-dev-skills",
    ),
    Check(
        "Apple Dev Skills tests",
        ("uv", "run", "pytest"),
        REPO_ROOT / "plugins" / "apple-dev-skills",
    ),
    Check(
        "Professional Skills tests",
        ("uv", "run", "pytest"),
        REPO_ROOT / "plugins" / "professional-skills",
    ),
    Check(
        "Python Skills metadata",
        ("uv", "run", "scripts/validate_repo_metadata.py"),
        REPO_ROOT / "plugins" / "python-skills",
    ),
    Check(
        "Python Skills tests",
        ("uv", "run", "pytest"),
        REPO_ROOT / "plugins" / "python-skills",
    ),
    Check(
        "Python Skills lint",
        ("uv", "run", "ruff", "check", "."),
        REPO_ROOT / "plugins" / "python-skills",
    ),
    Check(
        "Python Skills type checks",
        ("uv", "run", "mypy", "."),
        REPO_ROOT / "plugins" / "python-skills",
    ),
    Check(
        "Cybersecurity Skills metadata",
        ("uv", "run", "scripts/validate_repo_metadata.py"),
        REPO_ROOT / "plugins" / "cybersecurity-skills",
    ),
    Check(
        "Cybersecurity Skills tests",
        ("uv", "run", "pytest", "tests"),
        REPO_ROOT / "plugins" / "cybersecurity-skills",
    ),
    Check(
        "Reverse Engineering Skills metadata",
        ("uv", "run", "scripts/validate_repo_metadata.py"),
        REPO_ROOT / "plugins" / "reverse-engineering-skills",
    ),
    Check(
        "Reverse Engineering Skills tests",
        ("uv", "run", "pytest", "tests"),
        REPO_ROOT / "plugins" / "reverse-engineering-skills",
    ),
)


def checks_for_profile(profile: str) -> tuple[Check, ...]:
    checks: tuple[Check, ...] = CORE_CHECKS
    if profile in {"compatibility", "full"}:
        checks += COMPATIBILITY_CHECKS
    if profile == "full":
        checks += CHILD_CHECKS
    return checks


def run_check(check: Check, *, dry_run: bool) -> None:
    rendered_command = " ".join(check.command)
    relative_cwd = check.cwd.relative_to(REPO_ROOT)
    print(f"\n==> {check.name}\n    cwd: {relative_cwd or '.'}\n    {rendered_command}")
    if not dry_run:
        environment = None
        if check.cwd != REPO_ROOT:
            environment = os.environ.copy()
            environment.pop("VIRTUAL_ENV", None)
        subprocess.run(check.command, cwd=check.cwd, check=True, env=environment)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        choices=("core", "compatibility", "full"),
        default="core",
        help="Validation breadth; defaults to the fast PR-safe core profile.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print checks without running them.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        checks = checks_for_profile(args.profile)
    except ValueError as error:
        raise SystemExit(f"validate-socket: {error}") from error
    for check in checks:
        run_check(check, dry_run=args.dry_run)
    print(f"\nSocket validation profile `{args.profile}` passed ({len(checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
