#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Report token-efficiency and drift hotspots across Socket skill surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPEATED_PHRASES = (
    "When the user explicitly requests subagents",
    "Use official documentation first",
    "Use official docs first",
    "Do not run multiple SwiftPM or Xcode build/test commands concurrently",
    "Run the repository's documented validation path",
    "Report the intended edit scope",
)
VERSION_SENSITIVE_RE = re.compile(r"\bAs of\b.*?\bv?\d+\.\d+\.\d+\b")
HANDOFF_EXPECTATIONS = {
    "plugins/swiftasb-skills/skills/build-appkit-app/SKILL.md": (
        ("swiftasb:explain-swiftasb",),
        ("apple-dev-skills:explore-apple-swift-docs", "Apple Dev Skills"),
    ),
    "plugins/swiftasb-skills/skills/build-swift-package/SKILL.md": (
        ("swiftasb:explain-swiftasb",),
        ("apple-dev-skills:sync-swift-package-guidance", "Apple Swift package workflow skills"),
    ),
    "plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md": (
        ("swiftasb:explain-swiftasb",),
        ("apple-dev-skills:explore-apple-swift-docs", "Apple Dev Skills"),
    ),
    "plugins/swiftasb-skills/skills/choose-integration-shape/SKILL.md": (
        ("Apple Dev Skills", "apple-dev-skills"),
    ),
    "plugins/web-dev-skills/skills/expo-inline-native-modules-workflow/SKILL.md": (
        ("Apple Dev Skills", "apple-dev-skills"),
    ),
}


@dataclass(frozen=True)
class TextSurface:
    plugin: str
    path: Path
    relative_path: str
    line_count: int
    text: str


@dataclass(frozen=True)
class DuplicateGroup:
    digest: str
    line_count: int
    paths: tuple[str, ...]


@dataclass(frozen=True)
class PhraseHit:
    phrase: str
    file_count: int
    total_count: int
    paths: tuple[str, ...]


@dataclass(frozen=True)
class VersionHit:
    path: str
    line: int
    text: str


@dataclass(frozen=True)
class MissingHandoff:
    plugin: str
    path: str
    expected: str


@dataclass(frozen=True)
class AuditReport:
    skill_count: int
    skill_lines: int
    reference_count: int
    reference_lines: int
    skill_lines_by_plugin: dict[str, int]
    largest_skills: tuple[TextSurface, ...]
    largest_references: tuple[TextSurface, ...]
    duplicate_references: tuple[DuplicateGroup, ...]
    phrase_hits: tuple[PhraseHit, ...]
    version_hits: tuple[VersionHit, ...]
    missing_handoffs: tuple[MissingHandoff, ...]


def plugin_name_for(path: Path) -> str:
    parts = path.parts
    try:
        plugins_index = parts.index("plugins")
    except ValueError:
        return "(unknown)"
    if len(parts) <= plugins_index + 1:
        return "(unknown)"
    return parts[plugins_index + 1]


def read_text_surface(repo_root: Path, path: Path) -> TextSurface:
    text = path.read_text(encoding="utf-8")
    return TextSurface(
        plugin=plugin_name_for(path.relative_to(repo_root)),
        path=path,
        relative_path=path.relative_to(repo_root).as_posix(),
        line_count=len(text.splitlines()),
        text=text,
    )


def discover_surfaces(repo_root: Path, pattern: str) -> tuple[TextSurface, ...]:
    paths = sorted(repo_root.glob(pattern))
    return tuple(read_text_surface(repo_root, path) for path in paths if path.is_file())


def find_duplicate_references(references: tuple[TextSurface, ...]) -> tuple[DuplicateGroup, ...]:
    by_digest: dict[str, list[TextSurface]] = {}
    for surface in references:
        digest = hashlib.sha256(surface.text.encode("utf-8")).hexdigest()
        by_digest.setdefault(digest, []).append(surface)

    groups: list[DuplicateGroup] = []
    for digest, surfaces in by_digest.items():
        if len(surfaces) < 2:
            continue
        first = surfaces[0]
        groups.append(
            DuplicateGroup(
                digest=digest,
                line_count=first.line_count,
                paths=tuple(surface.relative_path for surface in sorted(surfaces, key=lambda item: item.relative_path)),
            )
        )

    return tuple(sorted(groups, key=lambda group: (-len(group.paths), -group.line_count, group.digest)))


def find_phrase_hits(surfaces: tuple[TextSurface, ...], phrases: tuple[str, ...]) -> tuple[PhraseHit, ...]:
    hits: list[PhraseHit] = []
    for phrase in phrases:
        paths: list[str] = []
        total_count = 0
        for surface in surfaces:
            count = surface.text.count(phrase)
            if count == 0:
                continue
            total_count += count
            paths.append(surface.relative_path)
        if total_count > 0:
            hits.append(
                PhraseHit(
                    phrase=phrase,
                    file_count=len(paths),
                    total_count=total_count,
                    paths=tuple(paths),
                )
            )
    return tuple(sorted(hits, key=lambda hit: (-hit.total_count, hit.phrase)))


def find_version_hits(surfaces: tuple[TextSurface, ...]) -> tuple[VersionHit, ...]:
    hits: list[VersionHit] = []
    for surface in surfaces:
        for line_number, line in enumerate(surface.text.splitlines(), start=1):
            if VERSION_SENSITIVE_RE.search(line):
                hits.append(VersionHit(path=surface.relative_path, line=line_number, text=line.strip()))
    return tuple(hits)


def find_missing_handoffs(skills: tuple[TextSurface, ...]) -> tuple[MissingHandoff, ...]:
    missing: list[MissingHandoff] = []
    for surface in skills:
        expectations = HANDOFF_EXPECTATIONS.get(surface.relative_path)
        if not expectations:
            continue
        for alternatives in expectations:
            if not any(expected in surface.text for expected in alternatives):
                missing.append(
                    MissingHandoff(
                        plugin=surface.plugin,
                        path=surface.relative_path,
                        expected=" or ".join(alternatives),
                    )
                )
    return tuple(sorted(missing, key=lambda item: (item.plugin, item.path, item.expected)))


def build_report(repo_root: Path, *, top: int = 10) -> AuditReport:
    skills = discover_surfaces(repo_root, "plugins/*/skills/*/SKILL.md")
    references = discover_surfaces(repo_root, "plugins/*/skills/*/references/**/*.md")

    skill_lines_by_plugin: dict[str, int] = {}
    for skill in skills:
        skill_lines_by_plugin[skill.plugin] = skill_lines_by_plugin.get(skill.plugin, 0) + skill.line_count

    return AuditReport(
        skill_count=len(skills),
        skill_lines=sum(skill.line_count for skill in skills),
        reference_count=len(references),
        reference_lines=sum(reference.line_count for reference in references),
        skill_lines_by_plugin=dict(sorted(skill_lines_by_plugin.items())),
        largest_skills=tuple(sorted(skills, key=lambda item: (-item.line_count, item.relative_path))[:top]),
        largest_references=tuple(sorted(references, key=lambda item: (-item.line_count, item.relative_path))[:top]),
        duplicate_references=find_duplicate_references(references),
        phrase_hits=find_phrase_hits(skills, DEFAULT_REPEATED_PHRASES),
        version_hits=find_version_hits(skills),
        missing_handoffs=find_missing_handoffs(skills),
    )


def surface_to_json(surface: TextSurface) -> dict[str, object]:
    return {
        "plugin": surface.plugin,
        "path": surface.relative_path,
        "line_count": surface.line_count,
    }


def report_to_json(report: AuditReport) -> dict[str, object]:
    return {
        "skill_count": report.skill_count,
        "skill_lines": report.skill_lines,
        "reference_count": report.reference_count,
        "reference_lines": report.reference_lines,
        "skill_lines_by_plugin": report.skill_lines_by_plugin,
        "largest_skills": [surface_to_json(surface) for surface in report.largest_skills],
        "largest_references": [surface_to_json(surface) for surface in report.largest_references],
        "duplicate_references": [
            {
                "digest": group.digest,
                "line_count": group.line_count,
                "paths": list(group.paths),
            }
            for group in report.duplicate_references
        ],
        "phrase_hits": [
            {
                "phrase": hit.phrase,
                "file_count": hit.file_count,
                "total_count": hit.total_count,
                "paths": list(hit.paths),
            }
            for hit in report.phrase_hits
        ],
        "version_hits": [
            {
                "path": hit.path,
                "line": hit.line,
                "text": hit.text,
            }
            for hit in report.version_hits
        ],
        "missing_handoffs": [
            {
                "plugin": missing.plugin,
                "path": missing.path,
                "expected": missing.expected,
            }
            for missing in report.missing_handoffs
        ],
    }


def markdown_table(rows: list[tuple[object, ...]], headers: tuple[str, ...]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)


def render_markdown(report: AuditReport) -> str:
    sections = [
        "# Socket Skill Surface Audit",
        "",
        "## Summary",
        "",
        f"- Skills: {report.skill_count} files, {report.skill_lines} lines",
        f"- References: {report.reference_count} files, {report.reference_lines} lines",
        f"- Exact duplicate reference groups: {len(report.duplicate_references)}",
        f"- Version-sensitive lines: {len(report.version_hits)}",
        f"- Missing expected handoffs: {len(report.missing_handoffs)}",
        "",
        "## Skill Lines By Plugin",
        "",
        markdown_table(
            [(plugin, lines) for plugin, lines in sorted(report.skill_lines_by_plugin.items(), key=lambda item: (-item[1], item[0]))],
            ("Plugin", "Skill lines"),
        ),
        "",
        "## Largest Skills",
        "",
        markdown_table(
            [(surface.relative_path, surface.line_count) for surface in report.largest_skills],
            ("Path", "Lines"),
        ),
        "",
        "## Largest References",
        "",
        markdown_table(
            [(surface.relative_path, surface.line_count) for surface in report.largest_references],
            ("Path", "Lines"),
        ),
        "",
        "## Exact Duplicate References",
        "",
    ]

    if report.duplicate_references:
        for group in report.duplicate_references:
            sections.append(f"- {len(group.paths)} files, {group.line_count} lines, sha256 `{group.digest[:12]}`")
            sections.extend(f"  - `{path}`" for path in group.paths)
    else:
        sections.append("No duplicate reference groups found.")

    sections.extend(["", "## Repeated Phrase Hits", ""])
    if report.phrase_hits:
        sections.append(
            markdown_table(
                [(hit.phrase, hit.file_count, hit.total_count) for hit in report.phrase_hits],
                ("Phrase", "Files", "Total hits"),
            )
        )
    else:
        sections.append("No configured repeated phrase hits found.")

    sections.extend(["", "## Version-Sensitive Lines", ""])
    if report.version_hits:
        for hit in report.version_hits:
            sections.append(f"- `{hit.path}:{hit.line}`: {hit.text}")
    else:
        sections.append("No version-sensitive lines found.")

    sections.extend(["", "## Missing Expected Handoffs", ""])
    if report.missing_handoffs:
        for missing in report.missing_handoffs:
            sections.append(f"- `{missing.path}` does not mention `{missing.expected}`")
    else:
        sections.append("No missing expected handoffs found.")

    sections.append("")
    return "\n".join(sections)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report token-efficiency hotspots across Socket skill surfaces.")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT, help="Socket repository root to audit.")
    parser.add_argument("--top", type=int, default=10, help="Number of largest skills and references to show.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_format: Literal["markdown", "json"] = args.format
    report = build_report(args.repo_root.resolve(), top=args.top)
    if output_format == "json":
        print(json.dumps(report_to_json(report), indent=2, sort_keys=True))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
