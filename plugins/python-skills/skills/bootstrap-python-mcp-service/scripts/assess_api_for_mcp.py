#!/usr/bin/env -S uv run
"""Assess OpenAPI/FastAPI endpoints for MCP mapping guidance."""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}
ACTION_HINTS = {
    "search",
    "sync",
    "refresh",
    "execute",
    "run",
    "submit",
    "approve",
    "reject",
    "create",
    "update",
    "delete",
    "import",
    "export",
    "generate",
    "send",
}


@dataclass
class Endpoint:
    method: str
    path: str
    operation_id: str
    summary: str


def load_openapi(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix == ".json":
        return json.loads(text)

    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "YAML OpenAPI parsing requires PyYAML. Run this script in a uv project with "
            "PyYAML available, or add it with: uv add pyyaml"
        ) from exc

    return yaml.safe_load(text)


def endpoints_from_openapi(spec: dict[str, Any]) -> list[Endpoint]:
    endpoints: list[Endpoint] = []
    for path, operations in (spec.get("paths") or {}).items():
        if not isinstance(operations, dict):
            continue
        for method, operation in operations.items():
            if method.lower() not in HTTP_METHODS:
                continue
            if not isinstance(operation, dict):
                operation = {}
            endpoints.append(
                Endpoint(
                    method=method.upper(),
                    path=str(path),
                    operation_id=str(operation.get("operationId") or ""),
                    summary=str(operation.get("summary") or operation.get("description") or ""),
                )
            )
    return endpoints


def endpoints_from_fastapi(import_path: str) -> list[Endpoint]:
    if ":" not in import_path:
        raise SystemExit("--fastapi must be in format module:app")

    module_name, app_name = import_path.split(":", 1)
    module = importlib.import_module(module_name)
    app = getattr(module, app_name, None)
    if app is None:
        raise SystemExit(f"Could not find '{app_name}' in module '{module_name}'")

    endpoints: list[Endpoint] = []
    for route in getattr(app, "routes", []):
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)
        if not path or not methods:
            continue

        for method in sorted(methods):
            upper = str(method).upper()
            if upper in {"HEAD", "OPTIONS"}:
                continue
            endpoints.append(
                Endpoint(
                    method=upper,
                    path=str(path),
                    operation_id=str(getattr(route, "name", "") or ""),
                    summary=str(getattr(route, "summary", "") or ""),
                )
            )
    return endpoints


def classify(endpoint: Endpoint) -> tuple[str, str]:
    path = endpoint.path.lower()
    opid = endpoint.operation_id.lower()
    method = endpoint.method.upper()

    has_action_hint = any(f"/{hint}" in path for hint in ACTION_HINTS) or any(
        hint in opid for hint in ACTION_HINTS
    )

    if method in {"POST", "PUT", "PATCH", "DELETE"} or has_action_hint:
        return (
            "Tool",
            "State-changing or action-oriented endpoint; expose as an MCP tool.",
        )

    if method == "GET":
        if re.search(r"\{[^}]+\}", path):
            return (
                "Resource",
                "Read endpoint with path parameters; model as a resource fetch.",
            )
        return (
            "Resource",
            "Read endpoint; model as a resource list/query where practical.",
        )

    return ("Tool", "Non-standard method; default to tool with explicit input schema.")


def route_map_suggestion(endpoint: Endpoint) -> str | None:
    if re.search(r"^/api/v\d+", endpoint.path):
        return "Strip versioned prefix (e.g., /api/v1) in RouteMap naming."
    if endpoint.path.count("/") >= 4:
        return "Use RouteMap alias to shorten deeply nested paths for MCP ergonomics."
    return None


def transform_suggestion(endpoint: Endpoint) -> str | None:
    if endpoint.method.upper() == "GET" and endpoint.path.endswith("s"):
        return "Consider response transform to normalize list envelopes and pagination fields."
    if endpoint.method.upper() in {"POST", "PUT", "PATCH"}:
        return "Consider request transform to flatten nested payload wrappers into tool args."
    return None


def build_findings(endpoints: list[Endpoint]) -> list[str]:
    findings: list[str] = []
    if not endpoints:
        findings.append("No endpoints discovered. Verify source path/import and try again.")
        return findings

    mutation_count = sum(e.method in {"POST", "PUT", "PATCH", "DELETE"} for e in endpoints)
    if mutation_count / len(endpoints) > 0.6:
        findings.append(
            "API is mutation-heavy. Prioritize tool design with clear side-effect descriptions and confirmations."
        )

    if any(e.path.startswith("/admin") or "/internal" in e.path for e in endpoints):
        findings.append(
            "Sensitive/internal routes detected. Apply strict auth boundaries before exposing to MCP clients."
        )

    if any("/search" in e.path or "query" in e.operation_id.lower() for e in endpoints):
        findings.append(
            "Search/query patterns detected. Prefer read-oriented resources when side effects are absent."
        )

    return findings


def render_report(source_label: str, endpoints: list[Endpoint]) -> str:
    lines: list[str] = []
    lines.append("# MCP Mapping Report")
    lines.append("")
    lines.append(f"Source: `{source_label}`")
    lines.append(f"Endpoints analyzed: **{len(endpoints)}**")
    lines.append("")
    lines.append("## Proposed Endpoint Mapping")
    lines.append("")
    lines.append("| Method | Path | Suggested MCP Primitive | Rationale |")
    lines.append("|---|---|---|---|")

    route_map_notes: list[str] = []
    transform_notes: list[str] = []

    for endpoint in endpoints:
        primitive, rationale = classify(endpoint)
        lines.append(
            f"| {endpoint.method} | `{endpoint.path}` | {primitive} | {rationale} |"
        )

        route_note = route_map_suggestion(endpoint)
        if route_note:
            route_map_notes.append(f"- `{endpoint.method} {endpoint.path}`: {route_note}")

        transform_note = transform_suggestion(endpoint)
        if transform_note:
            transform_notes.append(f"- `{endpoint.method} {endpoint.path}`: {transform_note}")

    lines.append("")
    lines.append("## MCP Best-Practice Findings")
    lines.append("")
    findings = build_findings(endpoints)
    for finding in findings:
        lines.append(f"- {finding}")

    lines.append("")
    lines.append("## Suggested RouteMap Strategy")
    lines.append("")
    if route_map_notes:
        lines.extend(route_map_notes)
    else:
        lines.append("- Default route naming appears acceptable; custom RouteMaps can be deferred.")

    lines.append("")
    lines.append("## Suggested Transform Strategy")
    lines.append("")
    if transform_notes:
        lines.extend(transform_notes)
    else:
        lines.append("- No immediate transform requirements detected; start with native schemas.")

    lines.append("")
    lines.append("## Recommended Bootstrap Follow-up")
    lines.append("")
    lines.append("1. Keep bootstrap mapping simple and ship a minimal MCP surface first.")
    lines.append("2. Add RouteMaps for naming clarity after first client feedback.")
    lines.append("3. Add Transforms where payload shape harms usability or consistency.")
    lines.append("4. Validate exposed tools/resources with representative prompt flows.")
    lines.append("")

    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--openapi", help="Path to OpenAPI file (.json/.yaml/.yml)")
    source.add_argument("--fastapi", help="FastAPI import in form module:app")
    parser.add_argument("--out", default="mcp_mapping_report.md", help="Output markdown path")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if args.openapi:
        source_path = Path(args.openapi)
        spec = load_openapi(source_path)
        endpoints = endpoints_from_openapi(spec)
        source_label = str(source_path)
    else:
        endpoints = endpoints_from_fastapi(args.fastapi)
        source_label = args.fastapi

    report = render_report(source_label, endpoints)
    out_path = Path(args.out)
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote MCP mapping report: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
