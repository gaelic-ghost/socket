#!/usr/bin/env python3
"""Validate the required structure of a Model Lab experiment manifest."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as error:
    raise SystemExit(
        "Experiment manifest validation requires PyYAML. Install the repository development dependencies with `uv sync --dev`."
    ) from error

REQUIRED_PATHS = (
    "schema_version",
    "experiment.id",
    "experiment.title",
    "experiment.hypothesis",
    "experiment.decision",
    "experiment.owner",
    "provenance.code_revision",
    "provenance.model.id",
    "provenance.model.revision",
    "provenance.model.license",
    "provenance.tokenizer.id",
    "provenance.tokenizer.revision",
    "provenance.dataset.id",
    "provenance.dataset.revision",
    "provenance.environment.lockfile",
    "provenance.environment.hardware",
    "method.controlled_variable",
    "method.baseline",
    "method.treatment",
    "method.seed",
    "method.generation_parameters",
    "evaluation.primary_metrics",
    "evaluation.guardrail_metrics",
    "evaluation.failure_thresholds",
    "budget.smoke_run",
    "budget.full_run",
    "budget.maximum_cost_usd",
    "budget.stop_conditions",
    "artifacts.raw_results",
    "artifacts.derived_results",
    "artifacts.report",
    "artifacts.sensitive_data",
)


def value_at(document: dict[str, Any], dotted_path: str) -> Any:
    value: Any = document
    for component in dotted_path.split("."):
        if not isinstance(value, dict) or component not in value:
            return None
        value = value[component]
    return value


def contains_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        normalized = value.lower()
        return normalized.startswith("replace with") or normalized.startswith(
            "replace-with"
        )
    if isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(
            contains_placeholder(key) or contains_placeholder(item)
            for key, item in value.items()
        )
    return False


def validate(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["The manifest root must be a YAML mapping."]
    errors = []
    for path in REQUIRED_PATHS:
        value = value_at(document, path)
        if value is None or value == "" or value == []:
            errors.append(f"Required field `{path}` is missing or empty.")
        elif contains_placeholder(value):
            errors.append(
                f"Required field `{path}` still contains a template placeholder."
            )
    if document.get("schema_version") != 1:
        errors.append("`schema_version` must be the integer 1.")
    for path in (
        "evaluation.primary_metrics",
        "evaluation.guardrail_metrics",
        "budget.stop_conditions",
    ):
        value = value_at(document, path)
        if (
            not isinstance(value, list)
            or not value
            or not all(isinstance(item, str) and item.strip() for item in value)
        ):
            errors.append(f"`{path}` must be a non-empty list of strings.")
    if not isinstance(value_at(document, "method.generation_parameters"), dict):
        errors.append("`method.generation_parameters` must be a mapping.")
    thresholds = value_at(document, "evaluation.failure_thresholds")
    if not isinstance(thresholds, dict) or not thresholds:
        errors.append("`evaluation.failure_thresholds` must be a non-empty mapping.")
    seed = value_at(document, "method.seed")
    if not isinstance(seed, int) or isinstance(seed, bool):
        errors.append("`method.seed` must be an integer.")
    maximum_cost = value_at(document, "budget.maximum_cost_usd")
    if (
        not isinstance(maximum_cost, (int, float))
        or isinstance(maximum_cost, bool)
        or not math.isfinite(maximum_cost)
        or maximum_cost < 0
    ):
        errors.append("`budget.maximum_cost_usd` must be a finite non-negative number.")
    if not isinstance(value_at(document, "artifacts.sensitive_data"), bool):
        errors.append("`artifacts.sensitive_data` must be a boolean.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    arguments = parser.parse_args()
    try:
        document = yaml.safe_load(arguments.manifest.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(
            f"Experiment manifest does not exist: {arguments.manifest}", file=sys.stderr
        )
        return 2
    except yaml.YAMLError as error:
        print(f"Experiment manifest is not valid YAML: {error}", file=sys.stderr)
        return 2
    errors = validate(document)
    if errors:
        for validation_error in errors:
            print(validation_error, file=sys.stderr)
        return 1
    print(f"Experiment manifest is structurally valid: {arguments.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
