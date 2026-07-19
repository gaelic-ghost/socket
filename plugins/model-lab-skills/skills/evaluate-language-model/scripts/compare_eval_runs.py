#!/usr/bin/env python3
"""Compare paired Model Lab JSONL evaluation results."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any


def load_results(path: Path) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"{path}:{line_number} is not valid JSON: {error}"
            ) from error
        identifier = item.get("id")
        score = item.get("score")
        if not isinstance(identifier, str) or not identifier:
            raise ValueError(f"{path}:{line_number} requires a non-empty string `id`.")
        if identifier in results:
            raise ValueError(
                f"{path}:{line_number} repeats evaluation id `{identifier}`."
            )
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            raise ValueError(f"{path}:{line_number} requires a numeric `score`.")
        results[identifier] = item
    if not results:
        raise ValueError(f"{path} contains no evaluation results.")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("treatment", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    try:
        baseline = load_results(arguments.baseline)
        treatment = load_results(arguments.treatment)
    except (OSError, ValueError) as error:
        print(
            f"Evaluation comparison could not load its inputs: {error}", file=sys.stderr
        )
        return 2
    shared = sorted(set(baseline) & set(treatment))
    if not shared:
        print("Evaluation comparison found no shared case ids.", file=sys.stderr)
        return 1
    deltas = [
        float(treatment[key]["score"]) - float(baseline[key]["score"]) for key in shared
    ]
    payload = {
        "baseline_count": len(baseline),
        "treatment_count": len(treatment),
        "paired_count": len(shared),
        "baseline_only": sorted(set(baseline) - set(treatment)),
        "treatment_only": sorted(set(treatment) - set(baseline)),
        "mean_paired_delta": statistics.fmean(deltas),
        "improved": sum(delta > 0 for delta in deltas),
        "unchanged": sum(delta == 0 for delta in deltas),
        "regressed": sum(delta < 0 for delta in deltas),
        "cases": [
            {
                "id": key,
                "baseline": baseline[key]["score"],
                "treatment": treatment[key]["score"],
                "delta": delta,
            }
            for key, delta in zip(shared, deltas)
        ],
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote paired evaluation comparison: {arguments.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
