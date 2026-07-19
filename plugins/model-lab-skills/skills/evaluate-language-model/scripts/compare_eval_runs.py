#!/usr/bin/env python3
"""Compare paired Model Lab JSONL evaluation results."""

from __future__ import annotations

import argparse
import json
import math
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
        if (
            not isinstance(score, (int, float))
            or isinstance(score, bool)
            or not math.isfinite(score)
        ):
            raise ValueError(f"{path}:{line_number} requires a finite numeric `score`.")
        results[identifier] = item
    if not results:
        raise ValueError(f"{path} contains no evaluation results.")
    return results


def paired_ids(
    baseline: dict[str, dict[str, Any]],
    treatment: dict[str, dict[str, Any]],
    allow_partial: bool,
) -> list[str]:
    baseline_ids = set(baseline)
    treatment_ids = set(treatment)
    if baseline_ids != treatment_ids and not allow_partial:
        baseline_only = sorted(baseline_ids - treatment_ids)
        treatment_only = sorted(treatment_ids - baseline_ids)
        raise ValueError(
            "Evaluation runs must contain identical case ids for a paired comparison. "
            f"Baseline-only ids: {baseline_only}; treatment-only ids: {treatment_only}. "
            "Use --allow-partial only for an explicitly labeled diagnostic comparison."
        )
    shared = sorted(baseline_ids & treatment_ids)
    if not shared:
        raise ValueError("Evaluation comparison found no shared case ids.")
    return shared


def validate_output_path(output: Path | None, *inputs: Path) -> None:
    if output is None:
        return
    resolved_output = output.resolve()
    for input_path in inputs:
        same_existing_file = output.exists() and output.samefile(input_path)
        if resolved_output == input_path.resolve() or same_existing_file:
            raise ValueError(
                f"Evaluation comparison output would overwrite an input file: {resolved_output}"
            )


def write_output(path: Path, rendered: str) -> None:
    try:
        path.write_text(rendered, encoding="utf-8")
    except OSError as error:
        raise ValueError(
            f"Evaluation comparison could not write output to {path}: {error}"
        ) from error


def build_comparison(
    baseline: dict[str, dict[str, Any]],
    treatment: dict[str, dict[str, Any]],
    allow_partial: bool = False,
) -> dict[str, Any]:
    shared = paired_ids(baseline, treatment, allow_partial)
    deltas = [
        float(treatment[key]["score"]) - float(baseline[key]["score"]) for key in shared
    ]
    return {
        "baseline_count": len(baseline),
        "treatment_count": len(treatment),
        "paired_count": len(shared),
        "partial_comparison": set(baseline) != set(treatment),
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("treatment", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Compare only shared ids and retain missing-id lists for diagnostic use.",
    )
    arguments = parser.parse_args()
    try:
        validate_output_path(arguments.output, arguments.baseline, arguments.treatment)
        baseline = load_results(arguments.baseline)
        treatment = load_results(arguments.treatment)
        payload = build_comparison(baseline, treatment, arguments.allow_partial)
    except (OSError, ValueError) as error:
        print(
            f"Evaluation comparison could not load its inputs: {error}", file=sys.stderr
        )
        return 2
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        try:
            write_output(arguments.output, rendered)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 2
        print(f"Wrote paired evaluation comparison: {arguments.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
