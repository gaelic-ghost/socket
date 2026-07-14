#!/usr/bin/env python3
"""Generate Socket's checked-in Hermes skill-tap export from its authored skills."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "plugins" / "agent-portability-skills" / "skills"
MESSAGING_SOURCE_ROOT = REPO_ROOT / "plugins" / "messaging-collaboration-skills" / "skills"
APPLE_SOURCE_ROOT = REPO_ROOT / "plugins" / "apple-dev-skills" / "skills"
CYBERSECURITY_SOURCE_ROOT = REPO_ROOT / "plugins" / "cybersecurity-skills" / "skills"
REVERSE_ENGINEERING_SOURCE_ROOT = REPO_ROOT / "plugins" / "reverse-engineering-skills" / "skills"
EXPORT_ROOT = REPO_ROOT / "skills"
AGENT_PORTABILITY_SKILLS = (
    "bootstrap-skills-plugin-repo",
    "hermes-agent-compatibility",
    "sync-skills-repo-guidance",
)
MESSAGING_SKILLS = (
    "apple-communication-workflow",
    "choose-platform-integration",
    "communication-notifications-workflow",
    "conversation-state-human-handoff",
    "default-communication-app-workflow",
    "discord-app-workflow",
    "google-meet-collaboration-workflow",
    "imessage-app-and-collaboration-workflow",
    "push-to-talk-workflow",
    "slack-app-workflow",
    "sms-mms-rcs-workflow",
    "teams-agent-workflow",
    "telegram-bot-workflow",
    "voip-sip-calling-workflow",
    "webhook-and-event-lifecycle",
    "whatsapp-business-workflow",
)
APPLE_SKILLS = (
    "app-extension-architecture-workflow",
    "mailkit-workflow",
    "file-provider-and-finder-sync-workflow",
)
CYBERSECURITY_SKILLS = (
    "analyze-suspicious-script-or-document",
    "assess-and-explain-threat",
    "assess-exposure-and-impact",
    "assess-macos-threat",
    "author-detection-content",
    "author-yara-x-rules",
    "check-artifact-reputation",
    "contain-and-recover-macos",
    "contain-security-incident",
    "harden-macos",
    "hunt-security-indicators",
    "inspect-macos-persistence",
    "inspect-macos-runtime-activity",
    "map-malware-behavior",
    "operate-agentic-security-tools",
    "perform-dynamic-malware-analysis",
    "perform-static-malware-analysis",
    "preserve-security-evidence",
    "recover-security-incident",
    "report-security-assessment",
    "route-security-work",
    "scope-authorized-security-test",
    "select-analysis-isolation",
    "test-network-services",
    "test-web-and-api-security",
    "triage-security-incident",
    "triage-suspicious-content",
    "triage-vulnerability-report",
    "use-objective-see-tools",
    "validate-vulnerability",
)
REVERSE_ENGINEERING_SKILLS = (
    "connect-hopper-mcp",
    "script-hopper-analysis",
    "use-ghidra",
    "use-hopper",
)
EXPORTED_SKILLS = (
    AGENT_PORTABILITY_SKILLS
    + MESSAGING_SKILLS
    + APPLE_SKILLS
    + CYBERSECURITY_SKILLS
    + REVERSE_ENGINEERING_SKILLS
)


class ExportError(RuntimeError):
    """Raised when the Hermes skill export cannot be created or verified."""


def source_paths(source_root: Path | None = None) -> dict[str, Path]:
    if source_root is not None:
        return {skill_name: source_root / skill_name for skill_name in EXPORTED_SKILLS}
    roots = {
        **{skill_name: SOURCE_ROOT for skill_name in AGENT_PORTABILITY_SKILLS},
        **{skill_name: MESSAGING_SOURCE_ROOT for skill_name in MESSAGING_SKILLS},
        **{skill_name: APPLE_SOURCE_ROOT for skill_name in APPLE_SKILLS},
        **{skill_name: CYBERSECURITY_SOURCE_ROOT for skill_name in CYBERSECURITY_SKILLS},
        **{skill_name: REVERSE_ENGINEERING_SOURCE_ROOT for skill_name in REVERSE_ENGINEERING_SKILLS},
    }
    return {skill_name: roots[skill_name] / skill_name for skill_name in EXPORTED_SKILLS}


def validate_sources(source_root: Path | None = None) -> None:
    sources = source_paths(source_root)
    for skill_name in EXPORTED_SKILLS:
        skill_path = sources[skill_name] / "SKILL.md"
        if not skill_path.is_file():
            raise ExportError(
                f"Hermes export source is missing {skill_name}/SKILL.md at {sources[skill_name]}."
            )


def write_export(
    source_root: Path | None = None,
    export_root: Path | None = None,
) -> None:
    export_root = EXPORT_ROOT if export_root is None else export_root
    validate_sources(source_root)
    sources = source_paths(source_root)
    with tempfile.TemporaryDirectory(prefix="socket-hermes-skills.", dir=export_root.parent) as temp_dir:
        staged_root = Path(temp_dir) / "skills"
        staged_root.mkdir()
        for skill_name in EXPORTED_SKILLS:
            shutil.copytree(sources[skill_name], staged_root / skill_name)
        if export_root.exists():
            shutil.rmtree(export_root)
        staged_root.replace(export_root)


def has_exact_export(
    source_root: Path | None = None,
    export_root: Path | None = None,
) -> bool:
    export_root = EXPORT_ROOT if export_root is None else export_root
    if not export_root.is_dir():
        return False
    sources = source_paths(source_root)
    export_names = {path.name for path in export_root.iterdir()}
    if set(sources) != set(EXPORTED_SKILLS) or export_names != set(EXPORTED_SKILLS):
        return False
    for skill_name in EXPORTED_SKILLS:
        comparison = filecmp.dircmp(sources[skill_name], export_root / skill_name)
        if comparison.left_only or comparison.right_only or comparison.funny_files:
            return False
        for _, mismatches, errors in _walk_comparison(comparison):
            if mismatches or errors:
                return False
    return True


def _walk_comparison(comparison: filecmp.dircmp) -> list[tuple[list[str], list[str], list[str]]]:
    results = [(comparison.left_only, comparison.diff_files, comparison.funny_files)]
    for child in comparison.subdirs.values():
        results.extend(_walk_comparison(child))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify the checked-in Socket Hermes skill-tap export."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the checked-in export differs from its authored source.",
    )
    args = parser.parse_args(argv)
    if args.check:
        validate_sources()
        if not has_exact_export():
            raise ExportError(
                "Root skills/ is stale or incomplete. Run `uv run scripts/export_hermes_skills.py` "
                "and commit the refreshed export."
            )
        print("Hermes skill-tap export matches its authored source.")
        return 0
    write_export()
    print("Generated the checked-in Hermes skill-tap export at skills/.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ExportError as error:
        print(f"export-hermes-skills: {error}")
        raise SystemExit(1)
