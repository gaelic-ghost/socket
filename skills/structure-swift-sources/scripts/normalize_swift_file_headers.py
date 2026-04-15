#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
# ]
# ///
"""Audit and normalize structured block-comment headers in Swift source files."""

from __future__ import annotations

import argparse
from datetime import date
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

import yaml


SKIP_DIR_NAMES = {".build", ".swiftpm", "DerivedData"}
STRUCTURED_HEADER_RE = re.compile(r"\A/\*(?P<body>.*?)\*/", re.DOTALL)
COPYRIGHT_RE = re.compile(r"^© (?P<owner>.+) (?P<year>\d{4})$")


class HeaderFields(NamedTuple):
    project_name: str
    file_name: str
    copyright_owner: str
    copyright_year: int
    purpose: str
    concern: str
    key_types: tuple[str, ...]
    see_also: tuple[str, ...]


def fail(message: str) -> None:
    print(json.dumps({"status": "blocked", "message": message}, indent=2, sort_keys=True), file=sys.stderr)
    raise SystemExit(1)


def managed_swift_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.swift"):
        if path.name == "Package.swift":
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def parse_structured_header(block_text: str) -> HeaderFields | None:
    body = block_text.removeprefix("/*").removesuffix("*/")
    project_name = ""
    file_name = ""
    copyright_owner = ""
    copyright_year = 0
    purpose = ""
    concern = ""
    key_types: tuple[str, ...] = ()
    see_also: tuple[str, ...] = ()
    content_lines: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith("*"):
            line = line.removeprefix("*").strip()
        if line:
            content_lines.append(line)

    if len(content_lines) < 5:
        return None

    project_name = content_lines[0]
    file_name = content_lines[1]
    copyright_match = COPYRIGHT_RE.match(content_lines[2])
    if not copyright_match:
        return None
    copyright_owner = copyright_match.group("owner").strip()
    copyright_year = int(copyright_match.group("year"))

    for line in content_lines[3:]:
        if line.startswith("Concern:"):
            concern = line.partition(":")[2].strip()
        elif line.startswith("Purpose:"):
            purpose = line.partition(":")[2].strip()
        elif line.startswith("Key Types:"):
            value = line.partition(":")[2].strip()
            key_types = tuple(part.strip() for part in value.split(",") if part.strip())
        elif line.startswith("See Also:"):
            value = line.partition(":")[2].strip()
            see_also = tuple(part.strip() for part in value.split(",") if part.strip())
    if project_name and file_name and copyright_owner and copyright_year and purpose and concern:
        return HeaderFields(
            project_name=project_name,
            file_name=file_name,
            copyright_owner=copyright_owner,
            copyright_year=copyright_year,
            purpose=purpose,
            concern=concern,
            key_types=key_types,
            see_also=see_also,
        )
    return None


def first_block_comment(content: str) -> tuple[str | None, str]:
    stripped = content.lstrip()
    leading_gap = content[: len(content) - len(stripped)]
    if not stripped.startswith("/*"):
        return None, content
    match = STRUCTURED_HEADER_RE.match(stripped)
    if not match:
        return None, content
    block = stripped[: match.end()]
    remainder = stripped[match.end() :]
    return block, leading_gap + remainder


def first_preamble_segments(content: str) -> tuple[list[str], str]:
    lines = content.splitlines(keepends=True)
    index = 0
    segments: list[str] = []

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped == "":
            index += 1
            continue
        if stripped.startswith("//"):
            start = index
            index += 1
            while index < len(lines) and lines[index].strip().startswith("//"):
                index += 1
            segments.append("".join(lines[start:index]))
            continue
        if stripped.startswith("/*"):
            start = index
            index += 1
            while index < len(lines) and "*/" not in lines[index - 1]:
                index += 1
            segments.append("".join(lines[start:index]))
            continue
        break

    remainder = "".join(lines[index:])
    return segments, remainder


def first_structured_header_segment(content: str) -> HeaderFields | None:
    segments, _ = first_preamble_segments(content)
    for segment in segments:
        fields = parse_structured_header(segment.lstrip())
        if fields is not None:
            return fields
    return None


def header_issue_for_content(content: str) -> tuple[str, HeaderFields | None]:
    segments, _ = first_preamble_segments(content)
    saw_candidate = False
    for segment in segments:
        stripped = segment.lstrip()
        if not stripped.startswith("/*"):
            continue
        if "Concern:" in stripped or "Purpose:" in stripped or "© " in stripped:
            saw_candidate = True
        fields = parse_structured_header(stripped)
        if fields is not None:
            return "compliant", fields
    if saw_candidate:
        return "malformed-header", None
    return "missing-header", None


def report_headers(root: Path) -> dict:
    files = managed_swift_files(root)
    results = []
    counts = {"compliant": 0, "missing-header": 0, "malformed-header": 0}
    for path in files:
        content = path.read_text(encoding="utf-8")
        issue, fields = header_issue_for_content(content)
        counts[issue] += 1
        result = {"path": str(path.relative_to(root)), "status": issue}
        if fields is not None:
            result["project_name"] = fields.project_name
            result["file_name"] = fields.file_name
            result["copyright_owner"] = fields.copyright_owner
            result["copyright_year"] = fields.copyright_year
            result["purpose"] = fields.purpose
            result["concern"] = fields.concern
            if fields.key_types:
                result["key_types"] = list(fields.key_types)
            if fields.see_also:
                result["see_also"] = list(fields.see_also)
        results.append(result)
    return {
        "status": "success",
        "files_scanned": len(files),
        "counts": counts,
        "results": results,
    }


def load_inventory(path: Path) -> list[dict]:
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(f"Invalid YAML in inventory {path}: {exc}")
    if not isinstance(loaded, dict) or not isinstance(loaded.get("entries"), list):
        fail(f"Inventory {path} must be a mapping with an entries list.")
    entries = loaded["entries"]
    normalized: list[dict] = []
    for entry in entries:
        if not isinstance(entry, dict):
            fail("Each inventory entry must be a mapping.")
        path_value = str(entry.get("path", "")).strip()
        purpose = str(entry.get("purpose", "")).strip()
        concern = str(entry.get("concern", "")).strip()
        key_types_value = entry.get("key_types", [])
        see_also_value = entry.get("see_also", [])
        if not path_value or not purpose or not concern:
            fail("Each inventory entry must include non-empty path, purpose, and concern values.")
        if isinstance(key_types_value, str):
            key_types = [item.strip() for item in key_types_value.split(",") if item.strip()]
        elif isinstance(key_types_value, list):
            key_types = [str(item).strip() for item in key_types_value if str(item).strip()]
        else:
            fail("Inventory key_types must be a string or list of strings.")
        if isinstance(see_also_value, str):
            see_also = [item.strip() for item in see_also_value.split(",") if item.strip()]
        elif isinstance(see_also_value, list):
            see_also = [str(item).strip() for item in see_also_value if str(item).strip()]
        else:
            fail("Inventory see_also must be a string or list of strings.")
        normalized.append(
            {
                "path": path_value,
                "purpose": purpose,
                "concern": concern,
                "key_types": key_types,
                "see_also": see_also,
            }
        )
    return normalized


def render_header(
    *,
    project_name: str,
    file_name: str,
    copyright_owner: str,
    copyright_year: int,
    concern: str,
    purpose: str,
    key_types: list[str],
    see_also: list[str],
) -> str:
    lines = [
        "/*",
        project_name,
        file_name,
        f"© {copyright_owner} {copyright_year}",
        "",
        f"Concern: {concern}",
        f"Purpose: {purpose}",
    ]
    if key_types:
        lines.append(f"Key Types: {', '.join(key_types)}")
    if see_also:
        lines.append(f"See Also: {', '.join(see_also)}")
    lines.extend(["*/", ""])
    return "\n".join(lines)


def inferred_project_name(root: Path) -> str:
    return root.name


def inferred_file_name(target: Path) -> str:
    return target.name


def inferred_copyright_year(existing: HeaderFields | None) -> int:
    if existing is not None:
        return existing.copyright_year
    return date.today().year


def apply_header(
    *,
    root: Path,
    target: Path,
    content: str,
    purpose: str,
    concern: str,
    copyright_owner: str,
    key_types: list[str],
    see_also: list[str],
) -> str:
    segments, remainder = first_preamble_segments(content)
    existing = None
    preserved: list[str] = []
    for segment in segments:
        parsed = parse_structured_header(segment.lstrip()) if segment.lstrip().startswith("/*") else None
        if parsed is not None:
            existing = parsed
            continue
        preserved.append(segment.rstrip("\n"))

    parts = [segment for segment in preserved if segment]
    parts.append(
        render_header(
            project_name=inferred_project_name(root),
            file_name=inferred_file_name(target),
            copyright_owner=copyright_owner,
            copyright_year=inferred_copyright_year(existing),
            concern=concern,
            purpose=purpose,
            key_types=key_types,
            see_also=see_also,
        ).rstrip("\n")
    )

    rebuilt_prefix = "\n\n".join(parts)
    body = remainder.lstrip("\n")
    if body:
        return rebuilt_prefix + "\n\n" + body
    return rebuilt_prefix + "\n"


def apply_inventory(root: Path, inventory_path: Path, *, copyright_owner: str = "Gale Williams") -> dict:
    created = 0
    updated = 0
    normalized_paths: list[str] = []
    for entry in load_inventory(inventory_path):
        relative = Path(entry["path"])
        target = (root / relative).resolve()
        if not target.is_file():
            fail(f"Inventory target does not exist: {relative}")
        if target.suffix != ".swift" or target.name == "Package.swift":
            fail(f"Inventory target must be a managed Swift source file: {relative}")

        before = target.read_text(encoding="utf-8")
        status, _ = header_issue_for_content(before)
        after = apply_header(
            root=root,
            target=target,
            content=before,
            purpose=entry["purpose"],
            concern=entry["concern"],
            copyright_owner=copyright_owner,
            key_types=entry["key_types"],
            see_also=entry["see_also"],
        )
        target.write_text(after, encoding="utf-8")
        normalized_paths.append(str(relative))
        if status == "missing-header":
            created += 1
        else:
            updated += 1

    return {
        "status": "success",
        "created_headers": created,
        "updated_headers": updated,
        "normalized_paths": normalized_paths,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to scan")
    parser.add_argument("--apply", action="store_true", help="Apply header normalization from inventory")
    parser.add_argument("--inventory", help="YAML inventory file for --apply mode")
    parser.add_argument("--copyright-owner", default="Gale Williams", help="Copyright owner for rendered headers")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        fail(f"Root path does not exist: {root}")

    if args.apply:
        if not args.inventory:
            fail("--inventory is required when using --apply.")
        payload = apply_inventory(
            root,
            Path(args.inventory).expanduser().resolve(),
            copyright_owner=str(args.copyright_owner).strip() or "Gale Williams",
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    payload = report_headers(root)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
