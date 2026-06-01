from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from socket_steward.audit import AuditReport, run_audit
from socket_steward.plan import DocsSyncPlan, plan_docs_sync
from socket_steward.proposal import DEFAULT_DOCS_SYNC_REPORT, ProposalReport, build_docs_sync_proposal, write_report


DOCS_SYNC_AUDITS = ("docs", "guidance", "marketplace")


@dataclass(frozen=True)
class PreparedDocsSync:
    audits: tuple[AuditReport, ...]
    plan: DocsSyncPlan
    proposal: ProposalReport
    report_path: Path | None

    @property
    def status(self) -> str:
        if any(audit.status == "FAIL" for audit in self.audits):
            return "FAIL"
        if self.plan.status == "TODO":
            return "TODO"
        return "PASS"

    def as_text(self) -> str:
        lines = ["docs-sync prepare: " + self.status, "", "Audits:"]
        lines.extend(f"- {audit.audit}: {audit.status}" for audit in self.audits)
        lines.extend(["", "Plan:", self.plan.as_text()])
        if self.report_path is not None:
            lines.extend(["", f"Proposal report: {self.report_path}"])
        else:
            lines.extend(["", "Proposal:", self.proposal.as_markdown()])
        return "\n".join(lines)

    def as_json(self) -> str:
        return json.dumps(
            {
                "status": self.status,
                "audits": [
                    {
                        "audit": audit.audit,
                        "status": audit.status,
                        "findings": [
                            {
                                "code": finding.code,
                                "severity": finding.severity,
                                "message": finding.message,
                                "path": finding.path,
                            }
                            for finding in audit.findings
                        ],
                    }
                    for audit in self.audits
                ],
                "plan": {
                    "name": self.plan.name,
                    "status": self.plan.status,
                    "items": [
                        {
                            "target": item.target,
                            "action": item.action,
                            "reason": item.reason,
                            "source": item.source,
                        }
                        for item in self.plan.items
                    ],
                },
                "report_path": str(self.report_path) if self.report_path else None,
            },
            indent=2,
            sort_keys=True,
        )


@dataclass(frozen=True)
class ApplyResult:
    status: str
    message: str
    report_path: Path

    def as_text(self) -> str:
        return "\n".join(
            [
                f"docs-sync apply: {self.status}",
                self.message,
                f"Proposal report: {self.report_path}",
            ]
        )


def prepare_docs_sync(
    repo_root: Path,
    *,
    output_path: Path | None = None,
) -> PreparedDocsSync:
    root = repo_root.resolve()
    audits = tuple(run_audit(root, audit_name) for audit_name in DOCS_SYNC_AUDITS)
    plan = plan_docs_sync(root)
    proposal = build_docs_sync_proposal(root)
    report_path = write_report(root, output_path, proposal) if output_path else None
    return PreparedDocsSync(
        audits=audits,
        plan=plan,
        proposal=proposal,
        report_path=report_path,
    )


def apply_docs_sync(
    repo_root: Path,
    *,
    confirm: bool,
    output_path: Path = DEFAULT_DOCS_SYNC_REPORT,
) -> ApplyResult:
    if not confirm:
        raise ValueError("Socket Steward apply requires --confirm.")

    root = repo_root.resolve()
    proposal = build_docs_sync_proposal(root)
    report_path = write_report(root, output_path, proposal)

    if proposal.plan.items:
        return ApplyResult(
            status="NEEDS-REVIEW",
            message=(
                "Socket Steward refreshed the proposal report, but this guarded apply "
                "mode does not mutate durable docs for TODO plans yet."
            ),
            report_path=report_path,
        )

    return ApplyResult(
        status="PASS",
        message=(
            "Socket Steward refreshed the proposal report. No durable docs-sync edits "
            "are currently suggested."
        ),
        report_path=report_path,
    )
