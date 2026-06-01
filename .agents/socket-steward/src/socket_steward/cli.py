from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from socket_steward.agent import ask_socket_steward
from socket_steward.audit import run_audit
from socket_steward.plan import plan_docs_sync
from socket_steward.proposal import DEFAULT_DOCS_SYNC_REPORT, build_docs_sync_proposal, write_report
from socket_steward.workflow import apply_docs_sync, prepare_docs_sync


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root)

    if args.command == "audit":
        audit_report = run_audit(repo_root, args.audit_name)
        print(audit_report.as_json() if args.json else audit_report.as_text())
        return 1 if audit_report.status == "FAIL" else 0

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

    if args.command == "propose":
        proposal_report = build_docs_sync_proposal(repo_root)
        if args.output is None:
            print(proposal_report.as_markdown())
        else:
            try:
                written_path = write_report(repo_root, args.output, proposal_report)
            except ValueError as error:
                print(error, file=sys.stderr)
                return 2
            print(f"Socket Steward wrote proposal report to {written_path}")
        return 0

    if args.command == "prepare":
        output_path = DEFAULT_DOCS_SYNC_REPORT if args.output else None
        prepared = prepare_docs_sync(repo_root, output_path=output_path)
        print(prepared.as_json() if args.json else prepared.as_text())
        return 1 if prepared.status == "FAIL" else 0

    if args.command == "apply":
        try:
            result = apply_docs_sync(
                repo_root,
                confirm=args.confirm,
                output_path=args.output,
            )
        except ValueError as error:
            print(error, file=sys.stderr)
            return 2
        print(result.as_text())
        return 1 if result.status == "NEEDS-REVIEW" else 0

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

    propose_parser = subparsers.add_parser(
        "propose",
        help="Create a Markdown proposal report without applying documentation edits.",
    )
    propose_parser.add_argument("proposal_name", choices=("docs-sync",))
    propose_parser.add_argument(
        "--output",
        type=Path,
        nargs="?",
        const=DEFAULT_DOCS_SYNC_REPORT,
        help=(
            "Write the proposal under docs/agents. Defaults to "
            "docs/agents/socket-steward-docs-sync.md when no path is provided."
        ),
    )

    prepare_parser = subparsers.add_parser(
        "prepare",
        help="Run audits, docs-sync planning, and proposal generation in order.",
    )
    prepare_parser.add_argument("workflow_name", choices=("docs-sync",))
    prepare_parser.add_argument(
        "--output",
        action="store_true",
        help="Write the proposal report to docs/agents/socket-steward-docs-sync.md.",
    )
    prepare_parser.add_argument("--json", action="store_true", help="Print the run as JSON.")

    apply_parser = subparsers.add_parser(
        "apply",
        help="Run guarded docs-sync apply behavior.",
    )
    apply_parser.add_argument("apply_name", choices=("docs-sync",))
    apply_parser.add_argument(
        "--confirm",
        action="store_true",
        help="Required. Confirms that guarded apply behavior may write the proposal report.",
    )
    apply_parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_DOCS_SYNC_REPORT,
        help="Proposal report path under docs/agents.",
    )

    return parser


if __name__ == "__main__":
    raise SystemExit(main())
