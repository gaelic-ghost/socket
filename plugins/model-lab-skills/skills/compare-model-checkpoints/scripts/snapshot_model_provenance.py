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


def validate_output_path(artifact: Path, output: Path | None) -> None:
    if output is None:
        return
    resolved_output = output.resolve()
    same_artifact_file = (
        output.exists() and artifact.is_file() and output.samefile(artifact)
    )
    if artifact.is_file() and (resolved_output == artifact or same_artifact_file):
        raise ValueError(
            f"Provenance output would overwrite the model artifact: {resolved_output}"
        )
    if artifact.is_dir() and (
        resolved_output == artifact or artifact in resolved_output.parents
    ):
        raise ValueError(
            "Provenance output must be outside the model artifact directory so the "
            f"snapshot cannot hash or overwrite itself: {resolved_output}"
        )
    if artifact.is_dir() and output.exists():
        for artifact_file in artifact.rglob("*"):
            if artifact_file.is_file() and output.samefile(artifact_file):
                raise ValueError(
                    "Provenance output is a hard-link alias of a file inside the model "
                    f"artifact directory: {artifact_file}"
                )


def write_output(path: Path, rendered: str) -> None:
    try:
        path.write_text(rendered, encoding="utf-8")
    except OSError as error:
        raise ValueError(
            f"Model provenance snapshot could not write output to {path}: {error}"
        ) from error


def build_snapshot(
    artifact: Path, model_id: str | None, revision: str | None
) -> dict[str, object]:
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
    return {
        "artifact": str(artifact),
        "kind": "file" if artifact.is_file() else "directory",
        "model_id": model_id,
        "revision": revision,
        "file_count": len(entries),
        "total_bytes": sum(path.stat().st_size for path in files),
        "inventory_sha256": aggregate.hexdigest(),
        "files": entries,
    }


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
    try:
        validate_output_path(artifact, arguments.output)
    except ValueError as error:
        print(
            f"Model provenance snapshot rejected its output path: {error}",
            file=sys.stderr,
        )
        return 2
    payload = build_snapshot(artifact, arguments.model_id, arguments.revision)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        try:
            write_output(arguments.output, rendered)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 2
        print(f"Wrote model provenance snapshot: {arguments.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
