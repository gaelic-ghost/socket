from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from socket_steward.audit import run_audit


@dataclass(frozen=True)
class PlanItem:
    target: str
    action: str
    reason: str
    source: str


@dataclass(frozen=True)
class DocsSyncPlan:
    name: str
    status: str
    items: tuple[PlanItem, ...]

    def as_text(self) -> str:
        if not self.items:
            return f"{self.name}: PASS\nNo docs-sync work is currently suggested."

        lines = [f"{self.name}: {self.status}"]
        for item in self.items:
            lines.append(f"- {item.target}: {item.action}")
            lines.append(f"  Reason: {item.reason}")
            lines.append(f"  Source: {item.source}")
        return "\n".join(lines)

    def as_json(self) -> str:
        return json.dumps(
            {
                "name": self.name,
                "status": self.status,
                "items": [
                    {
                        "target": item.target,
                        "action": item.action,
                        "reason": item.reason,
                        "source": item.source,
                    }
                    for item in self.items
                ],
            },
            indent=2,
            sort_keys=True,
        )


def plan_docs_sync(repo_root: Path) -> DocsSyncPlan:
    root = repo_root.resolve()
    items: list[PlanItem] = []

    for audit_name in ("docs", "guidance", "marketplace"):
        report = run_audit(root, audit_name)
        for finding in report.findings:
            if finding.severity in {"warning", "error"}:
                items.append(
                    PlanItem(
                        target=finding.path,
                        action=f"Resolve {finding.code}: {finding.message}",
                        reason=f"The {audit_name} audit reported {finding.severity}.",
                        source=f"audit:{audit_name}",
                    )
                )
            elif finding.code == "marketplace-entry-without-local-path":
                packaging_strategy = _read_text(
                    root / "docs" / "maintainers" / "plugin-packaging-strategy.md"
                )
                if not (
                    "Git-backed" in packaging_strategy
                    and "SpeakSwiftlyServer" in packaging_strategy
                ):
                    items.append(
                        PlanItem(
                            target="docs/maintainers/plugin-packaging-strategy.md",
                            action=(
                                "Document the Git-backed marketplace entry and explain "
                                "why it is not a local plugin path."
                            ),
                            reason=(
                                "Socket allows Git-backed entries such as Speak Swiftly, "
                                "but the docs should explain why that entry is not local."
                            ),
                            source="audit:marketplace",
                        )
                    )

    marketplace_names = _marketplace_names(root)
    if marketplace_names:
        readme = _read_text(root / "README.md")
        for plugin_name in marketplace_names.available:
            if plugin_name not in readme:
                items.append(
                    PlanItem(
                        target="README.md",
                        action=f"Add {plugin_name} to the currently available catalog list.",
                        reason=(
                            "The root README should stay aligned with installable "
                            "Socket marketplace entries."
                        ),
                        source=".agents/plugins/marketplace.json",
                    )
                )
        for plugin_name in marketplace_names.placeholders:
            if plugin_name not in readme:
                items.append(
                    PlanItem(
                        target="README.md",
                        action=f"Add {plugin_name} to the placeholder plugin list.",
                        reason=(
                            "The root README should make non-installable placeholder "
                            "entries visible when they remain in the marketplace catalog."
                        ),
                        source=".agents/plugins/marketplace.json",
                    )
                )

    if (root / ".agents" / "socket-steward").exists():
        contributing = _read_text(root / "CONTRIBUTING.md")
        if "Repo-Local Steward" not in contributing:
            items.append(
                PlanItem(
                    target="CONTRIBUTING.md",
                    action="Document Socket Steward commands and validation expectations.",
                    reason=(
                        "Repo-local maintainer tooling should be discoverable from "
                        "contributor workflow docs."
                    ),
                    source=".agents/socket-steward",
                )
            )

        roadmap = _read_text(root / "ROADMAP.md")
        if "Socket Steward" not in roadmap:
            items.append(
                PlanItem(
                    target="ROADMAP.md",
                    action="Track shipped and future Socket Steward slices.",
                    reason=(
                        "The steward changes Socket's maintainer tooling surface and "
                        "future write-mode boundary."
                    ),
                    source=".agents/socket-steward",
                )
            )

    unique_items = tuple(dict.fromkeys(items))
    status = "PASS" if not unique_items else "TODO"
    return DocsSyncPlan(name="docs-sync", status=status, items=unique_items)


@dataclass(frozen=True)
class _MarketplaceNames:
    available: tuple[str, ...]
    placeholders: tuple[str, ...]


def _marketplace_names(repo_root: Path) -> _MarketplaceNames | None:
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    if not marketplace_path.is_file():
        return None

    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None

    plugins = marketplace.get("plugins") if isinstance(marketplace, dict) else None
    if not isinstance(plugins, list):
        return None

    available: list[str] = []
    placeholders: list[str] = []
    for entry in plugins:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        policy = entry.get("policy")
        if not isinstance(name, str) or not isinstance(policy, dict):
            continue
        installation = policy.get("installation")
        if installation == "AVAILABLE":
            available.append(name)
        elif installation == "NOT_AVAILABLE":
            placeholders.append(name)

    return _MarketplaceNames(available=tuple(available), placeholders=tuple(placeholders))


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")
