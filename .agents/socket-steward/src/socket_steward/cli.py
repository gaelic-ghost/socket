from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from socket_steward.agent import ask_socket_steward
from socket_steward.audit import run_audit
from socket_steward.plan import plan_docs_sync


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root)

    if args.command == "audit":
        report = run_audit(repo_root, args.audit_name)
        print(report.as_json() if args.json else report.as_text())
        return 1 if report.status == "FAIL" else 0

    if args.command == "ask":
        if "OPENAI_API_KEY" not in os.environ:
            print(
                "Socket Steward cannot run the Agents SDK without OPENAI_API_KEY. "
                "Set the variable for this command, or use `audit` for offline checks.",
                file=sys.stderr,
            )
            return 2
        print(asyncio.run(ask_socket_steward(args.question, repo_root)))
        return 0

    if args.command == "plan":
        plan = plan_docs_sync(repo_root)
        print(plan.as_json() if args.json else plan.as_text())
        return 0

    parser.print_help()
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="socket-steward",
        description="Repo-local OpenAI Agents SDK steward for Socket maintainer audits.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to the Socket repository root. Defaults to the current directory.",
    )
    subparsers = parser.add_subparsers(dest="command")

    audit_parser = subparsers.add_parser("audit", help="Run a deterministic read-only audit.")
    audit_parser.add_argument("audit_name", choices=("docs", "guidance", "marketplace"))
    audit_parser.add_argument("--json", action="store_true", help="Print the audit report as JSON.")

    ask_parser = subparsers.add_parser("ask", help="Ask the OpenAI Agents SDK steward.")
    ask_parser.add_argument("question")

    plan_parser = subparsers.add_parser("plan", help="Create a deterministic read-only plan.")
    plan_parser.add_argument("plan_name", choices=("docs-sync",))
    plan_parser.add_argument("--json", action="store_true", help="Print the plan as JSON.")

    return parser


if __name__ == "__main__":
    raise SystemExit(main())
