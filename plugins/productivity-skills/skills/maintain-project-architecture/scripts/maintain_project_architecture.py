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
IGNORED_PARTS = {".build", ".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".venv", "__pycache__", "node_modules"}


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


def load_json_file(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(read_text(path))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def relative_path(project_root: Path, path: Path) -> str:
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return path.as_posix()


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


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


def plugin_root_from_manifest(manifest_path: Path) -> Path:
    return manifest_path.parent.parent


def plugin_manifest_paths(project_root: Path) -> list[Path]:
    return sorted(path for path in project_root.rglob(".codex-plugin/plugin.json") if not is_ignored(path))


def skill_manifest_paths(plugin_root: Path) -> list[Path]:
    skills_root = plugin_root / "skills"
    if not skills_root.is_dir():
        return []
    return sorted(path for path in skills_root.glob("*/SKILL.md") if path.is_file())


def plugin_product_target_names(project_root: Path, plugin_root: Path, manifest: dict[str, Any]) -> list[str]:
    targets: list[str] = []
    skills_value = manifest.get("skills")
    if isinstance(skills_value, str) and (plugin_root / skills_value).exists():
        targets.append(f"skills:{relative_path(project_root, plugin_root / skills_value)}")
    mcp_value = manifest.get("mcpServers")
    if isinstance(mcp_value, str) and (plugin_root / mcp_value).exists():
        targets.append(f"mcp:{relative_path(project_root, plugin_root / mcp_value)}")
    return targets


def marketplace_paths(project_root: Path) -> list[Path]:
    marketplace_path = project_root / ".agents" / "plugins" / "marketplace.json"
    return [marketplace_path] if marketplace_path.is_file() else []


def marketplace_entry_name(entry: dict[str, Any]) -> str | None:
    name = entry.get("name")
    return name if isinstance(name, str) and name else None


def marketplace_source_path(entry: dict[str, Any]) -> str | None:
    source = entry.get("source")
    if not isinstance(source, dict):
        return None
    path = source.get("path")
    return path if isinstance(path, str) and path else None


def resolve_marketplace_source(marketplace_path: Path, source_path: str) -> Path:
    marketplace_root = marketplace_path.parent.parent.parent
    return (marketplace_root / source_path).resolve()


def detect_plugin_model(project_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    products: list[dict[str, Any]] = []
    targets: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    evidence: list[dict[str, str]] = []
    product_names: set[str] = set()
    target_names: set[str] = set()

    manifest_by_root: dict[Path, dict[str, Any]] = {}
    for manifest_path in plugin_manifest_paths(project_root):
        manifest = load_json_file(manifest_path)
        if not manifest:
            continue
        plugin_name = manifest.get("name")
        if not isinstance(plugin_name, str) or not plugin_name:
            continue
        plugin_root = plugin_root_from_manifest(manifest_path)
        manifest_by_root[plugin_root.resolve()] = manifest
        manifest_evidence = [{"kind": "codex-plugin-manifest", "path": relative_path(project_root, manifest_path)}]
        target_refs = plugin_product_target_names(project_root, plugin_root, manifest)
        if plugin_name not in product_names:
            products.append(
                {
                    "name": plugin_name,
                    "kind": "codex-plugin",
                    "targets": target_refs,
                    "path": relative_path(project_root, plugin_root),
                    "evidence": manifest_evidence,
                }
            )
            product_names.add(plugin_name)
        for skill_path in skill_manifest_paths(plugin_root):
            skill_name = skill_path.parent.name
            target_name = f"skill:{plugin_name}/{skill_name}"
            skill_evidence = [{"kind": "skill-manifest", "path": relative_path(project_root, skill_path)}]
            if target_name not in target_names:
                targets.append(
                    {
                        "name": target_name,
                        "kind": "codex-skill",
                        "dependencies": [],
                        "path": relative_path(project_root, skill_path),
                        "evidence": skill_evidence,
                    }
                )
                target_names.add(target_name)
                evidence.extend(skill_evidence)
            relationships.append(
                {
                    "kind": "exposes",
                    "from": f"product:{plugin_name}",
                    "to": f"target:{target_name}",
                    "label": "plugin exposes skill",
                    "evidence": [{"kind": "skill-directory", "path": relative_path(project_root, skill_path)}],
                }
            )
        mcp_value = manifest.get("mcpServers")
        if isinstance(mcp_value, str):
            mcp_path = plugin_root / mcp_value
            if mcp_path.is_file():
                target_name = f"mcp:{relative_path(project_root, mcp_path)}"
                mcp_evidence = [{"kind": "mcp-config", "path": relative_path(project_root, mcp_path)}]
                if target_name not in target_names:
                    targets.append(
                        {
                            "name": target_name,
                            "kind": "mcp-config",
                            "dependencies": [],
                            "path": relative_path(project_root, mcp_path),
                            "evidence": mcp_evidence,
                        }
                    )
                    target_names.add(target_name)
                    evidence.extend(mcp_evidence)
                relationships.append(
                    {
                        "kind": "exposes",
                        "from": f"product:{plugin_name}",
                        "to": f"target:{target_name}",
                        "label": "plugin declares MCP servers",
                        "evidence": manifest_evidence,
                    }
                )
        evidence.extend(manifest_evidence)

    for marketplace_path in marketplace_paths(project_root):
        marketplace = load_json_file(marketplace_path)
        if not marketplace:
            continue
        marketplace_name = marketplace.get("name")
        entries = marketplace.get("plugins")
        if not isinstance(marketplace_name, str) or not isinstance(entries, list):
            continue
        entry_names = [name for entry in entries if isinstance(entry, dict) for name in [marketplace_entry_name(entry)] if name]
        marketplace_evidence = [{"kind": "plugin-marketplace", "path": relative_path(project_root, marketplace_path)}]
        if marketplace_name not in product_names:
            products.append(
                {
                    "name": marketplace_name,
                    "kind": "codex-plugin-marketplace",
                    "targets": entry_names,
                    "path": relative_path(project_root, marketplace_path),
                    "evidence": marketplace_evidence,
                }
            )
            product_names.add(marketplace_name)
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            entry_name = marketplace_entry_name(entry)
            if not entry_name:
                continue
            source_path = marketplace_source_path(entry)
            source_root = resolve_marketplace_source(marketplace_path, source_path) if source_path else None
            if entry_name not in product_names:
                source = entry.get("source") if isinstance(entry.get("source"), dict) else {}
                source_kind = source.get("source") if isinstance(source, dict) else None
                products.append(
                    {
                        "name": entry_name,
                        "kind": "codex-plugin-entry" if source_kind == "local" else "remote-plugin-entry",
                        "targets": [],
                        "path": source_path,
                        "evidence": marketplace_evidence,
                    }
                )
                product_names.add(entry_name)
            relationships.append(
                {
                    "kind": "exposes",
                    "from": f"product:{marketplace_name}",
                    "to": f"product:{entry_name}",
                    "label": "marketplace exposes plugin entry",
                    "evidence": marketplace_evidence,
                }
            )
            if source_root and source_root in manifest_by_root:
                relationships.append(
                    {
                        "kind": "owns",
                        "from": f"product:{entry_name}",
                        "to": f"path:{source_path}",
                        "label": "marketplace entry points at local plugin root",
                        "evidence": marketplace_evidence,
                    }
                )
        evidence.extend(marketplace_evidence)

    return products, targets, relationships, evidence


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
    plugin_products, plugin_targets, plugin_relationships, plugin_evidence = detect_plugin_model(project_root)
    products.extend(plugin_products)
    targets.extend(plugin_targets)
    relationships.extend(plugin_relationships)
    if plugin_products or plugin_targets:
        source = f"{source}+plugin-repo" if source != "filesystem" else "plugin-repo"

    evidence = [{"kind": source, "path": "Package.swift"}] if (project_root / "Package.swift").is_file() else []
    evidence.extend(plugin_evidence)

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
        "evidence": evidence,
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
        kind = target.get("kind") or "target"
        lines.append(f"- `{target['name']}` ({kind}) at `{path}` depends on: {dependencies}.")
    return "\n".join(lines)


def evidence_inventory(model: dict[str, Any]) -> str:
    if not model.get("evidence"):
        return "- No architecture evidence has been recorded yet."
    lines = []
    seen: set[tuple[str, str]] = set()
    for item in model.get("evidence", []):
        kind = str(item.get("kind", "evidence"))
        path = str(item.get("path", "path not recorded"))
        key = (kind, path)
        if key in seen:
            continue
        lines.append(f"- `{kind}` evidence from `{path}`.")
        seen.add(key)
    return "\n".join(lines)


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
