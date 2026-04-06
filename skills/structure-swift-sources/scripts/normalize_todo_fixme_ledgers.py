#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Normalize Swift TODO/FIXME comments into repo ledger files."""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


COMMENT_RE = re.compile(r"^(?P<indent>\s*)//\s*(?P<kind>TODO|FIXME):\s*(?P<body>.*?)\s*$")
ID_RE = re.compile(r"^(TODO|FIXME)-(?P<number>\d{4})$")
LEDGER_ENTRY_RE = re.compile(
    r"^## (?P<ticket>(TODO|FIXME)-\d{4}): (?P<title>.+?)\n"
    r"- Status: (?P<status>.+?)\n"
    r"- File: `(?P<file>.+?)`\n"
    r"- Line: `(?P<line>\d+)`\n"
    r"- Detail: (?P<detail>.+?)\n"
    r"(?:\n|$)",
    re.MULTILINE,
)
SWIFT_SUFFIX = ".swift"
LEDGER_HEADERS = {
    "TODO": "# TODO Ledger\n\nTrack normalized TODO tickets extracted from Swift sources.\n",
    "FIXME": "# FIXME Ledger\n\nTrack normalized FIXME tickets extracted from Swift sources.\n",
}


@dataclass
class CommentOccurrence:
    kind: str
    file_path: Path
    line_number: int
    indent: str
    body: str
    ticket_id: str | None


@dataclass
class LedgerEntry:
    ticket_id: str
    kind: str
    status: str
    file: str
    line: int
    title: str
    detail: str


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def iter_swift_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob(f"*{SWIFT_SUFFIX}") if path.is_file())


def scan_comments(root: Path) -> list[CommentOccurrence]:
    occurrences: list[CommentOccurrence] = []
    for file_path in iter_swift_files(root):
        for line_number, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            match = COMMENT_RE.match(line)
            if not match:
                continue
            body = match.group("body").strip()
            ticket_match = ID_RE.match(body)
            ticket_id = body if ticket_match and body.startswith(match.group("kind")) else None
            occurrences.append(
                CommentOccurrence(
                    kind=match.group("kind"),
                    file_path=file_path,
                    line_number=line_number,
                    indent=match.group("indent"),
                    body=body,
                    ticket_id=ticket_id,
                )
            )
    return occurrences


def ledger_path(root: Path, kind: str) -> Path:
    return root / f"{kind}.md"


def parse_ledger(root: Path, kind: str) -> dict[str, LedgerEntry]:
    path = ledger_path(root, kind)
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    entries: dict[str, LedgerEntry] = {}
    for match in LEDGER_ENTRY_RE.finditer(text):
        ticket_id = match.group("ticket")
        entries[ticket_id] = LedgerEntry(
            ticket_id=ticket_id,
            kind=kind,
            status=match.group("status").strip(),
            file=match.group("file").strip(),
            line=int(match.group("line")),
            title=match.group("title").strip(),
            detail=match.group("detail").strip(),
        )
    return entries


def next_ticket_id(kind: str, used_ids: set[str]) -> str:
    prefix = f"{kind}-"
    numbers = [
        int(ticket_id.split("-")[1])
        for ticket_id in used_ids
        if ticket_id.startswith(prefix) and ID_RE.match(ticket_id)
    ]
    next_number = (max(numbers) if numbers else 0) + 1
    return f"{kind}-{next_number:04d}"


def derive_title(detail: str) -> str:
    stripped = " ".join(detail.split())
    if not stripped:
        return "Backfill ledger entry"
    return stripped[:77] + "..." if len(stripped) > 80 else stripped


def render_ledger(entries: dict[str, LedgerEntry], kind: str) -> str:
    header = LEDGER_HEADERS[kind]
    ordered = sorted(entries.values(), key=lambda entry: entry.ticket_id)
    body = []
    for entry in ordered:
        body.append(
            "\n".join(
                [
                    f"## {entry.ticket_id}: {entry.title}",
                    f"- Status: {entry.status}",
                    f"- File: `{entry.file}`",
                    f"- Line: `{entry.line}`",
                    f"- Detail: {entry.detail}",
                ]
            )
        )
    if not body:
        return header + "\n"
    return header + "\n\n" + "\n\n".join(body) + "\n"


def apply_normalization(root: Path) -> dict:
    occurrences = scan_comments(root)
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

    for occurrence in occurrences:
        kind = occurrence.kind
        relative_file = occurrence.file_path.relative_to(root).as_posix()
        ticket_id = occurrence.ticket_id
        existing_entry = ledgers[kind].get(ticket_id) if ticket_id else None

        if ticket_id is None:
            ticket_id = next_ticket_id(kind, used_ids)
            used_ids.add(ticket_id)
            detail = occurrence.body
            entry = LedgerEntry(
                ticket_id=ticket_id,
                kind=kind,
                status="open",
                file=relative_file,
                line=occurrence.line_number,
                title=derive_title(detail),
                detail=detail,
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
            )
            ledgers[kind][ticket_id] = entry
            refreshed_entries.append(ticket_id)

        entry.file = relative_file
        entry.line = occurrence.line_number

        rewrites_by_file.setdefault(occurrence.file_path, {})[occurrence.line_number] = (
            f"{occurrence.indent}// {kind}: {ticket_id}"
        )

    for file_path, rewrites in rewrites_by_file.items():
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, replacement in rewrites.items():
            lines[line_number - 1] = replacement
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for kind in ("TODO", "FIXME"):
        ledger_path(root, kind).write_text(render_ledger(ledgers[kind], kind), encoding="utf-8")

    return {
        "status": "success",
        "files_scanned": len(iter_swift_files(root)),
        "comment_count": len(occurrences),
        "created_entries": sorted(created_entries),
        "refreshed_entries": sorted(set(refreshed_entries)),
        "ledger_files": [f"{kind}.md" for kind in ("TODO", "FIXME")],
    }


def report_normalization(root: Path) -> dict:
    occurrences = scan_comments(root)
    counts = {"TODO": 0, "FIXME": 0}
    existing_ids = {"TODO": 0, "FIXME": 0}
    textual_comments = {"TODO": 0, "FIXME": 0}
    for occurrence in occurrences:
        counts[occurrence.kind] += 1
        if occurrence.ticket_id:
            existing_ids[occurrence.kind] += 1
        else:
            textual_comments[occurrence.kind] += 1
    return {
        "status": "success",
        "files_scanned": len(iter_swift_files(root)),
        "comment_count": len(occurrences),
        "counts": counts,
        "existing_ids": existing_ids,
        "textual_comments": textual_comments,
        "ledger_files": [f"{kind}.md" for kind in ("TODO", "FIXME")],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to normalize.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Rewrite Swift comments and refresh TODO.md / FIXME.md. Defaults to report-only mode.",
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
