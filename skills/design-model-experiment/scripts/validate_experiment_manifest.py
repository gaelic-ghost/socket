#!/usr/bin/env python3
"""Validate the required structure of a Model Lab experiment manifest."""

from __future__ import annotations

import argparse
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
    "provenance.tokenizer.id",
    "provenance.tokenizer.revision",
    "provenance.dataset.id",
    "provenance.dataset.revision",
    "method.controlled_variable",
    "method.baseline",
    "method.treatment",
    "method.seed",
    "evaluation.primary_metrics",
    "evaluation.guardrail_metrics",
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


def validate(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["The manifest root must be a YAML mapping."]
    errors = []
    for path in REQUIRED_PATHS:
        value = value_at(document, path)
        if value is None or value == "" or value == []:
            errors.append(f"Required field `{path}` is missing or empty.")
    if document.get("schema_version") != 1:
        errors.append("`schema_version` must be the integer 1.")
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
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Experiment manifest is structurally valid: {arguments.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
