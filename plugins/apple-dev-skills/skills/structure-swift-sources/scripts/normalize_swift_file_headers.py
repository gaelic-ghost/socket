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
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

import yaml


SKIP_DIR_NAMES = {".build", ".swiftpm", "DerivedData"}
STRUCTURED_HEADER_RE = re.compile(r"\A/\*(?P<body>.*?)\*/", re.DOTALL)


class HeaderFields(NamedTuple):
    purpose: str
    concern: str


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
    purpose = ""
    concern = ""
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith("*"):
            line = line.removeprefix("*").strip()
        if line.startswith("Purpose:"):
            purpose = line.partition(":")[2].strip()
        elif line.startswith("Concern:"):
            concern = line.partition(":")[2].strip()
    if purpose and concern:
        return HeaderFields(purpose=purpose, concern=concern)
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


def header_issue_for_content(content: str) -> tuple[str, HeaderFields | None]:
    block, _ = first_block_comment(content)
    if block is None:
        return "missing-header", None
    if "Purpose:" not in block and "Concern:" not in block:
        return "missing-header", None
    fields = parse_structured_header(block)
    if fields is None:
        return "malformed-header", None
    return "compliant", fields


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
            result["purpose"] = fields.purpose
            result["concern"] = fields.concern
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
        if not path_value or not purpose or not concern:
            fail("Each inventory entry must include non-empty path, purpose, and concern values.")
        normalized.append({"path": path_value, "purpose": purpose, "concern": concern})
    return normalized


def render_header(purpose: str, concern: str) -> str:
    return "\n".join(
        [
            "/*",
            f"Purpose: {purpose}",
            f"Concern: {concern}",
            "*/",
            "",
        ]
    )


def apply_header(content: str, purpose: str, concern: str) -> str:
    segments, remainder = first_preamble_segments(content)
    preserved: list[str] = []
    for segment in segments:
        if segment.lstrip().startswith("/*") and parse_structured_header(segment.lstrip()) is not None:
            continue
        preserved.append(segment.rstrip("\n"))

    parts = [segment for segment in preserved if segment]
    parts.append(render_header(purpose, concern).rstrip("\n"))

    rebuilt_prefix = "\n\n".join(parts)
    body = remainder.lstrip("\n")
    if body:
        return rebuilt_prefix + "\n\n" + body
    return rebuilt_prefix + "\n"


def apply_inventory(root: Path, inventory_path: Path) -> dict:
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
        after = apply_header(before, entry["purpose"], entry["concern"])
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
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        fail(f"Root path does not exist: {root}")

    if args.apply:
        if not args.inventory:
            fail("--inventory is required when using --apply.")
        payload = apply_inventory(root, Path(args.inventory).expanduser().resolve())
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    payload = report_headers(root)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
