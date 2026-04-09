#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Normalize Swift and Objective-C TODO/FIXME comments into repo ledger files."""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


SUPPORTED_SUFFIXES = (".swift", ".h", ".m", ".mm")
COMMENT_PATTERNS = (
    (
        "line-comment",
        re.compile(
            r"^(?P<indent>\s*)//\s*(?P<kind>TODO|FIXME):\s*(?P<body>.*?)\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        "objc-warning",
        re.compile(
            r"^(?P<indent>\s*)#warning\s+(?P<kind>TODO|FIXME):\s*(?P<body>.*?)\s*$",
            re.IGNORECASE,
        ),
    ),
    (
        "swift-warning",
        re.compile(
            r'^(?P<indent>\s*)#warning\(\s*"(?P<kind>TODO|FIXME):\s*(?P<body>.*?)"\s*\)\s*$',
            re.IGNORECASE,
        ),
    ),
)
TICKET_RE = re.compile(r"^(?P<ticket>(TODO|FIXME)-(?P<number>\d{4}))(?:\s+(?P<rest>.*))?$", re.IGNORECASE)
ENTRY_HEADER_RE = re.compile(r"^## (?P<ticket>(TODO|FIXME)-\d{4}): (?P<title>.+?)$", re.MULTILINE)
MILESTONE_HEADING_RE = re.compile(r"^## Milestone (?P<number>\d+): (?P<title>.+?)$", re.MULTILINE)
ROADMAP_TOKEN_RE = re.compile(r"\[(?:ROADMAP:)?M(?P<milestone>\d+)(?:-T(?P<ticket>\d+))?\]", re.IGNORECASE)
PLAN_TOKEN_RE = re.compile(r"\[(?:PLAN|DOC):(?P<path>[^\]]+)\]", re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"\[(?P<label>[^\]]+)\]\((?P<target>[^)]+)\)")
LEDGER_HEADERS = {
    "TODO": "# TODO Ledger\n\nTrack normalized TODO tickets extracted from Swift and Objective-C sources.\n",
    "FIXME": "# FIXME Ledger\n\nTrack normalized FIXME tickets extracted from Swift and Objective-C sources.\n",
}
FIELD_ORDER = ("Status", "File", "Line", "Source", "Detail", "Roadmap", "Plans")
SOURCE_LABELS = {
    "line-comment": "line-comment",
    "objc-warning": "objc-warning",
    "swift-warning": "swift-warning",
}


@dataclass
class CommentOccurrence:
    kind: str
    file_path: Path
    line_number: int
    indent: str
    raw_body: str
    detail: str
    ticket_id: str | None
    source_kind: str
    roadmap_links: list[str] = field(default_factory=list)
    plan_links: list[str] = field(default_factory=list)


@dataclass
class LedgerEntry:
    ticket_id: str
    kind: str
    status: str
    file: str
    line: int
    title: str
    detail: str
    source: str
    roadmap_links: list[str] = field(default_factory=list)
    plan_links: list[str] = field(default_factory=list)


@dataclass
class ReferenceIssue:
    file: str
    line: int
    token: str
    reason: str


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalize_kind(kind: str) -> str:
    return kind.upper()


def normalize_ticket(ticket_id: str) -> str:
    return ticket_id.upper()


def iter_source_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def slugify_heading(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def build_roadmap_index(root: Path) -> dict[int, tuple[str, str]]:
    roadmap_path = root / "ROADMAP.md"
    if not roadmap_path.exists():
        return {}

    index: dict[int, tuple[str, str]] = {}
    text = roadmap_path.read_text(encoding="utf-8")
    for match in MILESTONE_HEADING_RE.finditer(text):
        number = int(match.group("number"))
        title = match.group("title").strip()
        heading = f"Milestone {number}: {title}"
        index[number] = (title, f"ROADMAP.md#{slugify_heading(heading)}")
    return index


def parse_link_list(value: str) -> list[str]:
    stripped = value.strip()
    if not stripped or stripped.lower() == "none":
        return []
    return [match.group(0) for match in MARKDOWN_LINK_RE.finditer(stripped)]


def render_link_list(links: list[str]) -> str:
    return ", ".join(links) if links else "none"


def clean_detail(text: str) -> str:
    return " ".join(text.split())


def derive_title(detail: str) -> str:
    stripped = clean_detail(detail)
    if not stripped:
        return "Backfill ledger entry"
    return stripped[:77] + "..." if len(stripped) > 80 else stripped


def merge_links(*link_groups: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for link_group in link_groups:
        for link in link_group:
            if link in seen:
                continue
            seen.add(link)
            merged.append(link)
    return merged


def resolve_roadmap_links(body: str, roadmap_index: dict[int, tuple[str, str]]) -> tuple[list[str], list[ReferenceIssue]]:
    links: list[str] = []
    issues: list[ReferenceIssue] = []
    for match in ROADMAP_TOKEN_RE.finditer(body):
        milestone_number = int(match.group("milestone"))
        ticket_number = match.group("ticket")
        token = match.group(0)
        milestone = roadmap_index.get(milestone_number)
        if milestone is None:
            issues.append(ReferenceIssue(file="", line=0, token=token, reason="Roadmap milestone was not found."))
            continue
        _, target = milestone
        if ticket_number:
            label = f"M{milestone_number}-T{ticket_number}"
        else:
            label = f"Milestone {milestone_number}"
        links.append(f"[{label}]({target})")
    return links, issues


def resolve_plan_links(body: str, root: Path) -> tuple[list[str], list[ReferenceIssue]]:
    links: list[str] = []
    issues: list[ReferenceIssue] = []
    for match in PLAN_TOKEN_RE.finditer(body):
        raw_path = match.group("path").strip()
        token = match.group(0)
        if not raw_path:
            issues.append(ReferenceIssue(file="", line=0, token=token, reason="Plan-doc reference did not include a path."))
            continue
        if raw_path.startswith("/"):
            issues.append(ReferenceIssue(file="", line=0, token=token, reason="Plan-doc reference must stay repo-relative."))
            continue
        candidate = (root / raw_path).resolve()
        try:
            relative = candidate.relative_to(root.resolve())
        except ValueError:
            issues.append(
                ReferenceIssue(
                    file="",
                    line=0,
                    token=token,
                    reason="Plan-doc reference escaped the repository root.",
                )
            )
            continue
        if not candidate.exists():
            issues.append(
                ReferenceIssue(
                    file="",
                    line=0,
                    token=token,
                    reason=f"Plan-doc reference does not exist: {relative.as_posix()}",
                )
            )
            continue
        relative_path = relative.as_posix()
        links.append(f"[{relative_path}]({relative_path})")
    return links, issues


def parse_body_metadata(
    *,
    kind: str,
    body: str,
    root: Path,
    roadmap_index: dict[int, tuple[str, str]],
) -> tuple[str | None, str, list[str], list[str], list[ReferenceIssue]]:
    stripped = body.strip()
    ticket_id: str | None = None
    metadata_body = stripped

    ticket_match = TICKET_RE.match(stripped)
    if ticket_match:
        candidate = normalize_ticket(ticket_match.group("ticket"))
        if candidate.startswith(f"{kind}-"):
            ticket_id = candidate
            metadata_body = (ticket_match.group("rest") or "").strip()

    roadmap_links, roadmap_issues = resolve_roadmap_links(metadata_body, roadmap_index)
    plan_links, plan_issues = resolve_plan_links(metadata_body, root)
    detail = clean_detail(ROADMAP_TOKEN_RE.sub("", PLAN_TOKEN_RE.sub("", metadata_body)))
    return ticket_id, detail, roadmap_links, plan_links, roadmap_issues + plan_issues


def rewrite_line(source_kind: str, indent: str, kind: str, ticket_id: str) -> str:
    if source_kind == "line-comment":
        return f"{indent}// {kind}: {ticket_id}"
    if source_kind == "objc-warning":
        return f"{indent}#warning {kind}: {ticket_id}"
    if source_kind == "swift-warning":
        return f'{indent}#warning("{kind}: {ticket_id}")'
    fail(f"Unsupported source kind for rewrite: {source_kind}")
    return ""


def scan_comments(
    root: Path,
    roadmap_index: dict[int, tuple[str, str]],
) -> tuple[list[CommentOccurrence], list[ReferenceIssue]]:
    occurrences: list[CommentOccurrence] = []
    issues: list[ReferenceIssue] = []

    for file_path in iter_source_files(root):
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            matched_pattern = None
            match = None
            for source_kind, pattern in COMMENT_PATTERNS:
                candidate = pattern.match(line)
                if candidate:
                    matched_pattern = source_kind
                    match = candidate
                    break
            if match is None or matched_pattern is None:
                continue

            kind = normalize_kind(match.group("kind"))
            ticket_id, detail, roadmap_links, plan_links, reference_issues = parse_body_metadata(
                kind=kind,
                body=match.group("body"),
                root=root,
                roadmap_index=roadmap_index,
            )
            relative_file = file_path.relative_to(root).as_posix()
            for issue in reference_issues:
                issues.append(
                    ReferenceIssue(
                        file=relative_file,
                        line=line_number,
                        token=issue.token,
                        reason=issue.reason,
                    )
                )

            occurrences.append(
                CommentOccurrence(
                    kind=kind,
                    file_path=file_path,
                    line_number=line_number,
                    indent=match.group("indent"),
                    raw_body=match.group("body").strip(),
                    detail=detail,
                    ticket_id=ticket_id,
                    source_kind=matched_pattern,
                    roadmap_links=roadmap_links,
                    plan_links=plan_links,
                )
            )
    return occurrences, issues


def ledger_path(root: Path, kind: str) -> Path:
    return root / f"{kind}.md"


def parse_ledger(root: Path, kind: str) -> dict[str, LedgerEntry]:
    path = ledger_path(root, kind)
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    matches = list(ENTRY_HEADER_RE.finditer(text))
    entries: dict[str, LedgerEntry] = {}

    for index, match in enumerate(matches):
        ticket_id = normalize_ticket(match.group("ticket"))
        if not ticket_id.startswith(f"{kind}-"):
            continue
        block_start = match.end()
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[block_start:block_end]
        fields: dict[str, str] = {}
        for raw_line in block.splitlines():
            if not raw_line.startswith("- "):
                continue
            key, separator, value = raw_line[2:].partition(":")
            if not separator:
                continue
            fields[key.strip().lower()] = value.strip()

        file_value = fields.get("file", "`unknown`").strip("`")
        line_value = fields.get("line", "`0`").strip("`")
        try:
            line_number = int(line_value)
        except ValueError:
            line_number = 0

        entries[ticket_id] = LedgerEntry(
            ticket_id=ticket_id,
            kind=kind,
            status=fields.get("status", "open"),
            file=file_value,
            line=line_number,
            title=match.group("title").strip(),
            detail=fields.get("detail", f"Backfill detail for {ticket_id}."),
            source=fields.get("source", "line-comment").strip("`"),
            roadmap_links=parse_link_list(fields.get("roadmap", "none")),
            plan_links=parse_link_list(fields.get("plans", "none")),
        )
    return entries


def next_ticket_id(kind: str, used_ids: set[str]) -> str:
    prefix = f"{kind}-"
    numbers = [
        int(ticket_id.split("-")[1])
        for ticket_id in used_ids
        if ticket_id.startswith(prefix) and TICKET_RE.match(ticket_id)
    ]
    next_number = (max(numbers) if numbers else 0) + 1
    return f"{kind}-{next_number:04d}"


def render_ledger(entries: dict[str, LedgerEntry], kind: str) -> str:
    header = LEDGER_HEADERS[kind]
    ordered = sorted(entries.values(), key=lambda entry: entry.ticket_id)
    body: list[str] = []
    for entry in ordered:
        fields = {
            "Status": entry.status,
            "File": f"`{entry.file}`",
            "Line": f"`{entry.line}`",
            "Source": f"`{entry.source}`",
            "Detail": entry.detail,
            "Roadmap": render_link_list(entry.roadmap_links),
            "Plans": render_link_list(entry.plan_links),
        }
        body.append(
            "\n".join(
                [f"## {entry.ticket_id}: {entry.title}"]
                + [f"- {field}: {fields[field]}" for field in FIELD_ORDER]
            )
        )
    if not body:
        return header + "\n"
    return header + "\n\n" + "\n\n".join(body) + "\n"


def format_reference_issues(issues: list[ReferenceIssue]) -> str:
    formatted = [
        f"{issue.file}:{issue.line}: {issue.token} -> {issue.reason}"
        for issue in issues
    ]
    return "\n".join(formatted)


def apply_normalization(root: Path) -> dict:
    roadmap_index = build_roadmap_index(root)
    occurrences, issues = scan_comments(root, roadmap_index)
    if issues:
        fail(
            "Cannot apply TODO/FIXME normalization until all explicit roadmap and plan-doc "
            "references resolve cleanly:\n"
            f"{format_reference_issues(issues)}"
        )

    ledgers = {kind: parse_ledger(root, kind) for kind in ("TODO", "FIXME")}
    used_ids = set()
    for entries in ledgers.values():
        used_ids.update(entries.keys())
    for occurrence in occurrences:
        if occurrence.ticket_id:
            used_ids.add(occurrence.ticket_id)

    rewrites_by_file: dict[Path, dict[int, str]] = {}
    created_entries: list[str] = []
    refreshed_entries: list[str] = []
    source_counts = {label: 0 for label in SOURCE_LABELS.values()}

    for occurrence in occurrences:
        kind = occurrence.kind
        relative_file = occurrence.file_path.relative_to(root).as_posix()
        ticket_id = occurrence.ticket_id
        existing_entry = ledgers[kind].get(ticket_id) if ticket_id else None

        if ticket_id is None:
            ticket_id = next_ticket_id(kind, used_ids)
            used_ids.add(ticket_id)
            detail = occurrence.detail or occurrence.raw_body
            entry = LedgerEntry(
                ticket_id=ticket_id,
                kind=kind,
                status="open",
                file=relative_file,
                line=occurrence.line_number,
                title=derive_title(detail),
                detail=detail,
                source=occurrence.source_kind,
                roadmap_links=occurrence.roadmap_links,
                plan_links=occurrence.plan_links,
            )
            ledgers[kind][ticket_id] = entry
            created_entries.append(ticket_id)
        else:
            entry = existing_entry or LedgerEntry(
                ticket_id=ticket_id,
                kind=kind,
                status="open",
                file=relative_file,
                line=occurrence.line_number,
                title="Backfill ledger entry",
                detail=f"Backfill detail for {ticket_id}.",
                source=occurrence.source_kind,
            )
            ledgers[kind][ticket_id] = entry
            refreshed_entries.append(ticket_id)
            if occurrence.detail:
                entry.detail = occurrence.detail
                entry.title = derive_title(occurrence.detail)

        entry.file = relative_file
        entry.line = occurrence.line_number
        entry.source = occurrence.source_kind
        entry.roadmap_links = merge_links(entry.roadmap_links, occurrence.roadmap_links)
        entry.plan_links = merge_links(entry.plan_links, occurrence.plan_links)

        rewrites_by_file.setdefault(occurrence.file_path, {})[occurrence.line_number] = rewrite_line(
            occurrence.source_kind,
            occurrence.indent,
            kind,
            ticket_id,
        )
        source_counts[occurrence.source_kind] += 1

    for file_path, rewrites in rewrites_by_file.items():
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, replacement in rewrites.items():
            lines[line_number - 1] = replacement
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for kind in ("TODO", "FIXME"):
        ledger_path(root, kind).write_text(render_ledger(ledgers[kind], kind), encoding="utf-8")

    return {
        "status": "success",
        "files_scanned": len(iter_source_files(root)),
        "comment_count": len(occurrences),
        "created_entries": sorted(created_entries),
        "refreshed_entries": sorted(set(refreshed_entries)),
        "ledger_files": [f"{kind}.md" for kind in ("TODO", "FIXME")],
        "source_counts": source_counts,
    }


def report_normalization(root: Path) -> dict:
    roadmap_index = build_roadmap_index(root)
    occurrences, issues = scan_comments(root, roadmap_index)
    counts = {"TODO": 0, "FIXME": 0}
    existing_ids = {"TODO": 0, "FIXME": 0}
    textual_comments = {"TODO": 0, "FIXME": 0}
    source_counts = {label: 0 for label in SOURCE_LABELS.values()}
    linked_roadmap = 0
    linked_plans = 0

    for occurrence in occurrences:
        counts[occurrence.kind] += 1
        source_counts[occurrence.source_kind] += 1
        if occurrence.ticket_id:
            existing_ids[occurrence.kind] += 1
        else:
            textual_comments[occurrence.kind] += 1
        if occurrence.roadmap_links:
            linked_roadmap += 1
        if occurrence.plan_links:
            linked_plans += 1

    return {
        "status": "success",
        "files_scanned": len(iter_source_files(root)),
        "comment_count": len(occurrences),
        "counts": counts,
        "existing_ids": existing_ids,
        "textual_comments": textual_comments,
        "ledger_files": [f"{kind}.md" for kind in ("TODO", "FIXME")],
        "source_counts": source_counts,
        "linked_roadmap_comments": linked_roadmap,
        "linked_plan_comments": linked_plans,
        "unresolved_references": [
            {
                "file": issue.file,
                "line": issue.line,
                "token": issue.token,
                "reason": issue.reason,
            }
            for issue in issues
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to normalize.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Rewrite Swift and Objective-C comments and refresh TODO.md / FIXME.md. Defaults to report-only mode.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        fail(f"Expected --root to be a directory: {root}")

    payload = apply_normalization(root) if args.apply else report_normalization(root)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
