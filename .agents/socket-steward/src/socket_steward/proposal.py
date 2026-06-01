from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from socket_steward.plan import DocsSyncPlan, plan_docs_sync


DEFAULT_DOCS_SYNC_REPORT = Path("docs/agents/socket-steward-docs-sync.md")


@dataclass(frozen=True)
class ProposalReport:
    name: str
    plan: DocsSyncPlan
    validation_commands: tuple[str, ...]

    def as_markdown(self) -> str:
        lines = [
            f"# {self.name}",
            "",
            "## Status",
            "",
            self.plan.status,
            "",
            "## Scope",
            "",
            "This report proposes documentation synchronization work only. It does not "
            "apply file edits, run git commands, publish releases, or change background "
            "service state.",
            "",
            "## Proposed Work",
            "",
        ]

        if not self.plan.items:
            lines.append("No docs-sync work is currently suggested.")
        else:
            for index, item in enumerate(self.plan.items, start=1):
                lines.extend(
                    [
                        f"### {index}. {item.target}",
                        "",
                        f"- Action: {item.action}",
                        f"- Reason: {item.reason}",
                        f"- Source: {item.source}",
                        "",
                    ]
                )

        lines.extend(
            [
                "",
                "## Validation",
                "",
                "Run these commands after any accepted documentation edits:",
                "",
            ]
        )
        lines.extend(f"- `{command}`" for command in self.validation_commands)
        lines.append("")
        return "\n".join(lines)


def build_docs_sync_proposal(repo_root: Path) -> ProposalReport:
    return ProposalReport(
        name="Socket Steward Docs Sync Proposal",
        plan=plan_docs_sync(repo_root),
        validation_commands=(
            "uv run --directory .agents/socket-steward pytest",
            "uv run --directory .agents/socket-steward ruff check .",
            "uv run --directory .agents/socket-steward mypy .",
            "uv run scripts/validate_socket_metadata.py",
            "uv run mypy",
        ),
    )


def write_report(repo_root: Path, output_path: Path, report: ProposalReport) -> Path:
    root = repo_root.resolve()
    resolved_output = (root / output_path).resolve() if not output_path.is_absolute() else output_path
    reports_root = (root / "docs" / "agents").resolve()

    try:
        resolved_output.relative_to(reports_root)
    except ValueError as error:
        raise ValueError(
            "Socket Steward only writes proposal reports under docs/agents. "
            f"Requested output was {resolved_output}."
        ) from error

    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(report.as_markdown(), encoding="utf-8")
    return resolved_output
