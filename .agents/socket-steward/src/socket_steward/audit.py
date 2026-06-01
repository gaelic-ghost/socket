from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


REQUIRED_ROOT_DOCS = (
    "README.md",
    "CONTRIBUTING.md",
    "ROADMAP.md",
    "AGENTS.md",
    "TODO.md",
)


@dataclass(frozen=True)
class AuditFinding:
    code: str
    severity: str
    message: str
    path: str


@dataclass(frozen=True)
class AuditReport:
    audit: str
    status: str
    findings: tuple[AuditFinding, ...]

    def as_text(self) -> str:
        if not self.findings:
            return f"{self.audit}: PASS"

        lines = [f"{self.audit}: {self.status}"]
        for finding in self.findings:
            lines.append(
                f"- [{finding.severity}] {finding.code}: {finding.message} ({finding.path})"
            )
        return "\n".join(lines)

    def as_json(self) -> str:
        return json.dumps(
            {
                "audit": self.audit,
                "status": self.status,
                "findings": [
                    {
                        "code": finding.code,
                        "severity": finding.severity,
                        "message": finding.message,
                        "path": finding.path,
                    }
                    for finding in self.findings
                ],
            },
            indent=2,
            sort_keys=True,
        )


def run_audit(repo_root: Path, audit_name: str) -> AuditReport:
    root = repo_root.resolve()
    if audit_name == "docs":
        return _audit_docs(root)
    if audit_name == "guidance":
        return _audit_guidance(root)
    if audit_name == "marketplace":
        return _audit_marketplace(root)

    return AuditReport(
        audit=audit_name,
        status="FAIL",
        findings=(
            AuditFinding(
                code="unknown-audit",
                severity="error",
                message=(
                    "Socket Steward does not know this audit name. "
                    "Use one of: docs, guidance, marketplace."
                ),
                path=str(root),
            ),
        ),
    )


def _audit_docs(repo_root: Path) -> AuditReport:
    findings: list[AuditFinding] = []
    for relative_path in REQUIRED_ROOT_DOCS:
        path = repo_root / relative_path
        if not path.is_file():
            findings.append(
                AuditFinding(
                    code="missing-root-doc",
                    severity="error",
                    message=f"Expected root maintainer document {relative_path} to exist.",
                    path=relative_path,
                )
            )

    roadmap = repo_root / "ROADMAP.md"
    if roadmap.is_file():
        text = roadmap.read_text(encoding="utf-8")
        for heading in ("## Vision", "## Product Principles", "## Backlog Candidates"):
            if heading not in text:
                findings.append(
                    AuditFinding(
                        code="roadmap-missing-section",
                        severity="warning",
                        message=f"ROADMAP.md is missing the expected {heading} section.",
                        path="ROADMAP.md",
                    )
                )

    return _report("docs", findings)


def _audit_guidance(repo_root: Path) -> AuditReport:
    findings: list[AuditFinding] = []
    root_agents = repo_root / "AGENTS.md"
    if not root_agents.is_file():
        findings.append(
            AuditFinding(
                code="missing-root-agents",
                severity="error",
                message="Socket needs root AGENTS.md guidance before repo-local agents run.",
                path="AGENTS.md",
            )
        )
    else:
        text = root_agents.read_text(encoding="utf-8")
        for phrase in (
            "Treat Gale's local `socket` checkout as the normal day-to-day working checkout on `main`.",
            "Root docs and marketplace wiring are updated together when packaging or policy changed.",
            "Do not assume every child surface exposes `.codex-plugin/plugin.json` at its directory root.",
        ):
            if phrase not in text:
                findings.append(
                    AuditFinding(
                        code="guidance-anchor-missing",
                        severity="warning",
                        message=f"Root AGENTS.md is missing expected guidance anchor: {phrase}",
                        path="AGENTS.md",
                    )
                )

    for child_agents in sorted((repo_root / "plugins").glob("*/AGENTS.md")):
        plugin_root = child_agents.parent
        if not (plugin_root / ".codex-plugin" / "plugin.json").exists():
            findings.append(
                AuditFinding(
                    code="child-guidance-without-plugin-manifest",
                    severity="info",
                    message=(
                        "Child guidance exists without a packaged plugin manifest. "
                        "Confirm this is still a placeholder or non-installable child."
                    ),
                    path=str(child_agents.relative_to(repo_root)),
                )
            )

    return _report("guidance", findings)


def _audit_marketplace(repo_root: Path) -> AuditReport:
    findings: list[AuditFinding] = []
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    if not marketplace_path.is_file():
        return _report(
            "marketplace",
            [
                AuditFinding(
                    code="missing-marketplace",
                    severity="error",
                    message="Socket root marketplace metadata is missing.",
                    path=".agents/plugins/marketplace.json",
                )
            ],
        )

    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return _report(
            "marketplace",
            [
                AuditFinding(
                    code="invalid-marketplace-json",
                    severity="error",
                    message=f"Socket marketplace JSON could not be parsed: {error}",
                    path=".agents/plugins/marketplace.json",
                )
            ],
        )

    plugin_entries = _plugin_entries(marketplace)
    if not plugin_entries:
        findings.append(
            AuditFinding(
                code="marketplace-has-no-plugins",
                severity="error",
                message="Socket marketplace metadata did not expose any plugin entries.",
                path=".agents/plugins/marketplace.json",
            )
        )

    for plugin_id, entry in plugin_entries:
        source_path = _entry_source_path(entry)
        if source_path is None:
            findings.append(
                AuditFinding(
                    code="marketplace-entry-without-local-path",
                    severity="info",
                    message=(
                        f"Marketplace entry {plugin_id} is not a local plugin path. "
                        "If it is Git-backed, confirm root docs explain that ownership."
                    ),
                    path=".agents/plugins/marketplace.json",
                )
            )
            continue

        manifest_path = repo_root / source_path / ".codex-plugin" / "plugin.json"
        if not manifest_path.is_file():
            findings.append(
                AuditFinding(
                    code="marketplace-path-missing-manifest",
                    severity="error",
                    message=(
                        f"Marketplace entry {plugin_id} points at {source_path}, "
                        "but no .codex-plugin/plugin.json exists there."
                    ),
                    path=str(Path(source_path) / ".codex-plugin" / "plugin.json"),
                )
            )

    return _report("marketplace", findings)


def _plugin_entries(marketplace: object) -> tuple[tuple[str, dict[str, object]], ...]:
    if not isinstance(marketplace, dict):
        return ()

    plugins = marketplace.get("plugins")
    if isinstance(plugins, dict):
        return tuple(
            (str(plugin_id), entry)
            for plugin_id, entry in plugins.items()
            if isinstance(entry, dict)
        )

    if isinstance(plugins, list):
        entries: list[tuple[str, dict[str, object]]] = []
        for index, entry in enumerate(plugins):
            if not isinstance(entry, dict):
                continue
            plugin_id = entry.get("id") or entry.get("name") or f"plugin-{index}"
            entries.append((str(plugin_id), entry))
        return tuple(entries)

    return ()


def _entry_source_path(entry: dict[str, object]) -> str | None:
    for key in ("path", "source", "root"):
        value = entry.get(key)
        if isinstance(value, str) and value.startswith("./"):
            return value.removeprefix("./")

    source = entry.get("source")
    if isinstance(source, dict):
        for key in ("path", "root"):
            value = source.get(key)
            if isinstance(value, str) and value.startswith("./"):
                return value.removeprefix("./")

    return None


def _report(audit_name: str, findings: list[AuditFinding]) -> AuditReport:
    status = "PASS" if not any(finding.severity in {"error", "warning"} for finding in findings) else "WARN"
    if any(finding.severity == "error" for finding in findings):
        status = "FAIL"
    return AuditReport(audit=audit_name, status=status, findings=tuple(findings))
