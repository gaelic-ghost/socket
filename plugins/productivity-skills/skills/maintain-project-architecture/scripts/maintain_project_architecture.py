#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Maintain docs/architecture files from repo evidence."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_ARCHITECTURE_SECTIONS = [
    "Summary",
    "Product Map",
    "Module Architecture",
    "Construction And Ownership",
    "Visual Model",
    "Architecture Evidence",
    "Staleness Checks",
]
REQUIRED_SLICES_SECTIONS = ["Summary", "Slice Index", "Slices"]


@dataclass
class Issue:
    issue_id: str
    category: str
    severity: str
    file: str
    evidence: str
    recommended_fix: str
    auto_fixable: bool
    fixed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "category": self.category,
            "severity": self.severity,
            "file": self.file,
            "evidence": self.evidence,
            "recommended_fix": self.recommended_fix,
            "auto_fixable": self.auto_fixable,
            "fixed": self.fixed,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--run-mode", required=True, choices=["check-only", "apply"])
    parser.add_argument("--architecture-dir")
    parser.add_argument("--json-out")
    parser.add_argument("--print-json", action="store_true")
    return parser.parse_args()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def render_template(name: str) -> str:
    return read_text(skill_root() / "assets" / name)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def h2_headings(markdown: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"^##\s+(.+?)\s*$", markdown, re.MULTILINE)]


def run_dump_package(project_root: Path) -> dict[str, Any] | None:
    if not (project_root / "Package.swift").is_file():
        return None
    proc = subprocess.run(
        ["swift", "package", "dump-package"],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def fallback_parse_package(project_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = project_root / "Package.swift"
    if not manifest.is_file():
        return [], []
    text = read_text(manifest)
    products = [
        {
            "name": match.group(2),
            "kind": match.group(1),
            "targets": [],
            "evidence": [{"kind": "manifest-regex", "path": "Package.swift"}],
        }
        for match in re.finditer(r"\.(library|executable)\s*\(\s*name:\s*\"([^\"]+)\"", text)
    ]
    targets = []
    for match in re.finditer(r"\.(target|executableTarget|testTarget)\s*\(\s*name:\s*\"([^\"]+)\"", text):
        name = match.group(2)
        targets.append(
            {
                "name": name,
                "kind": match.group(1),
                "dependencies": [],
                "path": f"Sources/{name}" if (project_root / "Sources" / name).exists() else None,
                "evidence": [{"kind": "manifest-regex", "path": "Package.swift"}],
            }
        )
    return products, targets


def normalize_dump_package(project_root: Path, data: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    products = []
    for product in data.get("products", []):
        if not isinstance(product, dict):
            continue
        product_type = product.get("type")
        kind = product_type.get("executable") if isinstance(product_type, dict) and "executable" in product_type else product_type
        if isinstance(kind, dict):
            kind = next(iter(kind.keys()), "library")
        products.append(
            {
                "name": product.get("name"),
                "kind": kind or "product",
                "targets": product.get("targets", []),
                "evidence": [{"kind": "swift-package-dump", "path": "Package.swift"}],
            }
        )

    targets = []
    for target in data.get("targets", []):
        if not isinstance(target, dict):
            continue
        name = target.get("name")
        path = target.get("path")
        if not path and isinstance(name, str) and (project_root / "Sources" / name).exists():
            path = f"Sources/{name}"
        dependencies = []
        for dependency in target.get("dependencies", []):
            if isinstance(dependency, str):
                dependencies.append(dependency)
            elif isinstance(dependency, dict):
                dependencies.extend(str(value) for value in dependency.values() if isinstance(value, str))
        targets.append(
            {
                "name": name,
                "kind": target.get("type", "target"),
                "dependencies": dependencies,
                "path": path,
                "evidence": [{"kind": "swift-package-dump", "path": "Package.swift"}],
            }
        )
    return products, targets


def detect_model(project_root: Path) -> dict[str, Any]:
    package_data = run_dump_package(project_root)
    if package_data:
        products, targets = normalize_dump_package(project_root, package_data)
        source = "swift-package-dump"
    else:
        products, targets = fallback_parse_package(project_root)
        source = "package-swift-regex" if (project_root / "Package.swift").is_file() else "filesystem"

    relationships = []
    for target in targets:
        for dependency in target.get("dependencies", []):
            relationships.append(
                {
                    "kind": "depends-on",
                    "from": f"target:{target['name']}",
                    "to": f"target-or-product:{dependency}",
                    "label": "declared target dependency",
                    "evidence": target.get("evidence", []),
                }
            )

    return {
        "schemaVersion": 1,
        "generatedBy": "maintain-project-architecture",
        "projectRoot": str(project_root),
        "detectedAt": datetime.now(timezone.utc).isoformat(),
        "detectionSource": source,
        "products": [item for item in products if item.get("name")],
        "targets": [item for item in targets if item.get("name")],
        "relationships": relationships,
        "slices": [],
        "evidence": [{"kind": source, "path": "Package.swift"}] if (project_root / "Package.swift").is_file() else [],
    }


def product_inventory(model: dict[str, Any]) -> str:
    products = model.get("products", [])
    if not products:
        return "No products have been recorded yet."
    lines = []
    for product in products:
        targets = ", ".join(product.get("targets", [])) or "no targets recorded"
        kind = product.get("kind") or "product"
        lines.append(f"- `{product['name']}` ({kind}) uses targets: {targets}.")
    return "\n".join(lines)


def target_inventory(model: dict[str, Any]) -> str:
    targets = model.get("targets", [])
    if not targets:
        return "No modules have been recorded yet."
    lines = []
    for target in targets:
        dependencies = ", ".join(target.get("dependencies", [])) or "no declared dependencies"
        path = target.get("path") or "path not recorded"
        lines.append(f"- `{target['name']}` at `{path}` depends on: {dependencies}.")
    return "\n".join(lines)


def evidence_inventory(model: dict[str, Any]) -> str:
    source = model.get("detectionSource", "unknown")
    if not model.get("evidence"):
        return "- No architecture evidence has been recorded yet."
    return f"- Product and target inventory detected with `{source}` from `Package.swift`."


def replace_generated_block(text: str, start: str, end: str, body: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n\n{body.strip()}\n\n{end}"
    if pattern.search(text):
        return pattern.sub(replacement, text)
    return text.rstrip() + f"\n\n{replacement}\n"


def render_architecture(model: dict[str, Any]) -> str:
    text = render_template("ARCHITECTURE.template.md")
    text = replace_generated_block(text, "<!-- Generated product inventory starts here. -->", "<!-- Generated product inventory ends here. -->", product_inventory(model))
    text = replace_generated_block(text, "<!-- Generated target inventory starts here. -->", "<!-- Generated target inventory ends here. -->", target_inventory(model))
    text = replace_generated_block(text, "<!-- Generated evidence starts here. -->", "<!-- Generated evidence ends here. -->", evidence_inventory(model))
    return text


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def names(items: list[dict[str, Any]]) -> set[str]:
    return {str(item.get("name")) for item in items if item.get("name")}


def audit(architecture_dir: Path, model: dict[str, Any]) -> tuple[list[Issue], list[Issue], list[str]]:
    architecture_path = architecture_dir / "ARCHITECTURE.md"
    slices_path = architecture_dir / "SLICES.md"
    json_path = architecture_dir / "architecture.json"
    schema_violations: list[Issue] = []
    stale_claims: list[Issue] = []
    errors: list[str] = []

    for path, issue_id in [(architecture_path, "missing-architecture-md"), (slices_path, "missing-slices-md"), (json_path, "missing-architecture-json")]:
        if not path.is_file():
            schema_violations.append(Issue(issue_id, "schema", "high", str(path), f"{path.name} is missing.", f"Create {path.name} from the architecture template.", True))

    if architecture_path.is_file():
        headings = set(h2_headings(read_text(architecture_path)))
        for section in REQUIRED_ARCHITECTURE_SECTIONS:
            if section not in headings:
                schema_violations.append(Issue(f"missing-architecture-section-{slugify(section)}", "schema", "high", str(architecture_path), f"ARCHITECTURE.md is missing '## {section}'.", f"Add '## {section}'.", True))

    if slices_path.is_file():
        headings = set(h2_headings(read_text(slices_path)))
        for section in REQUIRED_SLICES_SECTIONS:
            if section not in headings:
                schema_violations.append(Issue(f"missing-slices-section-{slugify(section)}", "schema", "high", str(slices_path), f"SLICES.md is missing '## {section}'.", f"Add '## {section}'.", True))

    existing_model = load_json(json_path)
    if json_path.is_file() and existing_model is None:
        errors.append(f"{json_path} is not valid JSON.")
    if existing_model:
        for kind in ["products", "targets"]:
            existing_names = names(existing_model.get(kind, []))
            current_names = names(model.get(kind, []))
            stale = existing_names - current_names
            missing = current_names - existing_names
            if stale:
                stale_claims.append(Issue(f"stale-{kind}", "stale-claim", "high", str(json_path), f"architecture.json records stale {kind}: {', '.join(sorted(stale))}.", "Refresh architecture.json from current repo evidence.", True))
            if missing:
                stale_claims.append(Issue(f"missing-current-{kind}", "stale-claim", "medium", str(json_path), f"architecture.json is missing current {kind}: {', '.join(sorted(missing))}.", "Refresh architecture.json from current repo evidence.", True))

    return schema_violations, stale_claims, errors


def apply_fixes(architecture_dir: Path, model: dict[str, Any]) -> list[dict[str, str]]:
    fixes = []
    architecture_path = architecture_dir / "ARCHITECTURE.md"
    slices_path = architecture_dir / "SLICES.md"
    json_path = architecture_dir / "architecture.json"
    write_text(architecture_path, render_architecture(model))
    fixes.append({"action": "refresh-architecture-md", "file": str(architecture_path)})
    if not slices_path.exists():
        write_text(slices_path, render_template("SLICES.template.md"))
        fixes.append({"action": "create-slices-md", "file": str(slices_path)})
    existing_model = load_json(json_path) or {}
    model["slices"] = existing_model.get("slices", [])
    write_text(json_path, json.dumps(model, indent=2, sort_keys=True))
    fixes.append({"action": "refresh-architecture-json", "file": str(json_path)})
    return fixes


def run(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).expanduser().resolve()
    architecture_dir = Path(args.architecture_dir).expanduser().resolve() if args.architecture_dir else project_root / "docs" / "architecture"
    model = detect_model(project_root)
    fixes: list[dict[str, str]] = []
    errors: list[str] = []
    if not project_root.is_dir():
        errors.append(f"Project root does not exist or is not a directory: {project_root}")
    elif args.run_mode == "apply":
        fixes = apply_fixes(architecture_dir, model)
    schema_violations, stale_claims, audit_errors = audit(architecture_dir, model)
    errors.extend(audit_errors)
    post_fix_status = []
    if args.run_mode == "apply":
        post_schema, post_stale, post_errors = audit(architecture_dir, model)
        post_fix_status = [issue.to_dict() for issue in [*post_schema, *post_stale]]
        errors.extend(post_errors)
    return {
        "run_context": {"project_root": str(project_root), "architecture_dir": str(architecture_dir), "run_mode": args.run_mode},
        "detected_model": model,
        "schema_violations": [issue.to_dict() for issue in schema_violations],
        "stale_claims": [issue.to_dict() for issue in stale_claims],
        "fixes_applied": fixes,
        "post_fix_status": post_fix_status,
        "errors": errors,
    }


def main() -> int:
    args = parse_args()
    report = run(args)
    if args.json_out:
        write_text(Path(args.json_out), json.dumps(report, indent=2, sort_keys=True))
    if args.print_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif not report["schema_violations"] and not report["stale_claims"] and not report["errors"]:
        print("No findings.")
    else:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
