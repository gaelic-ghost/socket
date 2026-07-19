#!/usr/bin/env python3
"""Create a deterministic provenance snapshot for a local model artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--model-id")
    parser.add_argument("--revision")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    artifact = arguments.artifact.resolve()
    if not artifact.exists():
        print(f"Model artifact does not exist: {artifact}", file=sys.stderr)
        return 2
    files = (
        [artifact]
        if artifact.is_file()
        else sorted(path for path in artifact.rglob("*") if path.is_file())
    )
    entries = [
        {
            "path": path.name
            if artifact.is_file()
            else str(path.relative_to(artifact)),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        }
        for path in files
    ]
    aggregate = hashlib.sha256()
    for entry in entries:
        aggregate.update(f"{entry['path']}\0{entry['sha256']}\n".encode())
    payload = {
        "artifact": str(artifact),
        "kind": "file" if artifact.is_file() else "directory",
        "model_id": arguments.model_id,
        "revision": arguments.revision,
        "file_count": len(entries),
        "total_bytes": sum(entry["bytes"] for entry in entries),
        "inventory_sha256": aggregate.hexdigest(),
        "files": entries,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote model provenance snapshot: {arguments.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
