from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "maintain_project_architecture.py"
SPEC = importlib.util.spec_from_file_location("maintain_project_architecture", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["maintain_project_architecture"] = MODULE
SPEC.loader.exec_module(MODULE)


def run(project_root: Path, run_mode: str = "check-only"):
    args = argparse.Namespace(project_root=str(project_root), run_mode=run_mode, architecture_dir=None, json_out=None, print_json=False)
    return MODULE.run(args)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def package_manifest() -> str:
    return """
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Demo",
    products: [
        .library(name: "DemoCore", targets: ["DemoCore"]),
        .executable(name: "demo-tool", targets: ["DemoTool"]),
    ],
    targets: [
        .target(name: "DemoCore"),
        .executableTarget(name: "DemoTool", dependencies: ["DemoCore"]),
    ]
)
""".strip()


def plugin_manifest(name: str = "demo-plugin") -> str:
    return f"""
{{
  "name": "{name}",
  "version": "1.0.0",
  "description": "Demo plugin.",
  "skills": "./skills/",
  "mcpServers": "./.mcp.json"
}}
""".strip()


def marketplace() -> str:
    return """
{
  "name": "demo-marketplace",
  "plugins": [
    {
      "name": "demo-plugin",
      "source": {
        "source": "local",
        "path": "./plugins/demo-plugin"
      }
    },
    {
      "name": "remote-plugin",
      "source": {
        "source": "url",
        "url": "https://github.com/example/remote-plugin.git",
        "ref": "main"
      }
    }
  ]
}
""".strip()


def test_check_only_reports_missing_architecture_files(tmp_path: Path) -> None:
    write(tmp_path / "Package.swift", package_manifest())
    report = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-architecture-md" in issue_ids
    assert "missing-slices-md" in issue_ids
    assert "missing-architecture-json" in issue_ids


def test_apply_creates_architecture_files_and_detects_products(tmp_path: Path) -> None:
    write(tmp_path / "Package.swift", package_manifest())
    report = run(tmp_path, run_mode="apply")
    architecture_dir = tmp_path / "docs" / "architecture"
    assert report["errors"] == []
    assert report["post_fix_status"] == []
    assert (architecture_dir / "ARCHITECTURE.md").is_file()
    assert (architecture_dir / "SLICES.md").is_file()
    assert (architecture_dir / "architecture.json").is_file()
    architecture = (architecture_dir / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "## Product Map" in architecture
    assert "`DemoCore`" in architecture
    assert "`demo-tool`" in architecture
    slices = (architecture_dir / "SLICES.md").read_text(encoding="utf-8")
    assert "No provable slices have been recorded yet." in slices


def test_stale_architecture_json_is_reported(tmp_path: Path) -> None:
    write(tmp_path / "Package.swift", package_manifest())
    run(tmp_path, run_mode="apply")
    write(tmp_path / "docs" / "architecture" / "architecture.json", '{"schemaVersion":1,"products":[{"name":"OldProduct"}],"targets":[{"name":"OldTarget"}]}')
    report = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["stale_claims"]}
    assert "stale-products" in issue_ids
    assert "stale-targets" in issue_ids


def test_apply_preserves_existing_slices_in_architecture_json(tmp_path: Path) -> None:
    write(tmp_path / "Package.swift", package_manifest())
    run(tmp_path, run_mode="apply")
    write(tmp_path / "docs" / "architecture" / "architecture.json", '{"schemaVersion":1,"products":[],"targets":[],"slices":[{"name":"Launch"}]}')
    run(tmp_path, run_mode="apply")
    model = (tmp_path / "docs" / "architecture" / "architecture.json").read_text(encoding="utf-8")
    assert '"name": "Launch"' in model


def test_apply_detects_plugin_manifest_skills_and_mcp_config(tmp_path: Path) -> None:
    plugin_root = tmp_path / "plugins" / "demo-plugin"
    write(plugin_root / ".codex-plugin" / "plugin.json", plugin_manifest())
    write(plugin_root / ".mcp.json", '{"mcpServers": {}}')
    write(plugin_root / "skills" / "demo-skill" / "SKILL.md", "---\nname: demo-skill\n---\n# Demo Skill\n")

    report = run(tmp_path, run_mode="apply")

    assert report["errors"] == []
    assert report["detected_model"]["detectionSource"] == "plugin-repo"
    product_names = {product["name"] for product in report["detected_model"]["products"]}
    target_names = {target["name"] for target in report["detected_model"]["targets"]}
    relationship_labels = {relationship["label"] for relationship in report["detected_model"]["relationships"]}
    assert "demo-plugin" in product_names
    assert "skill:demo-plugin/demo-skill" in target_names
    assert "mcp:plugins/demo-plugin/.mcp.json" in target_names
    assert "plugin exposes skill" in relationship_labels
    assert "plugin declares MCP servers" in relationship_labels

    architecture = (tmp_path / "docs" / "architecture" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "`demo-plugin`" in architecture
    assert "`skill:demo-plugin/demo-skill`" in architecture
    assert "`mcp-config` evidence from `plugins/demo-plugin/.mcp.json`" in architecture


def test_apply_detects_plugin_marketplace_entries(tmp_path: Path) -> None:
    plugin_root = tmp_path / "plugins" / "demo-plugin"
    write(plugin_root / ".codex-plugin" / "plugin.json", plugin_manifest())
    write(plugin_root / "skills" / "demo-skill" / "SKILL.md", "---\nname: demo-skill\n---\n# Demo Skill\n")
    write(tmp_path / ".agents" / "plugins" / "marketplace.json", marketplace())

    report = run(tmp_path, run_mode="apply")

    product_names = {product["name"] for product in report["detected_model"]["products"]}
    relationship_labels = {relationship["label"] for relationship in report["detected_model"]["relationships"]}
    assert {"demo-marketplace", "demo-plugin", "remote-plugin"}.issubset(product_names)
    assert "marketplace exposes plugin entry" in relationship_labels
    assert "marketplace entry points at local plugin root" in relationship_labels

    model = (tmp_path / "docs" / "architecture" / "architecture.json").read_text(encoding="utf-8")
    assert '"kind": "codex-plugin-marketplace"' in model
    assert '"kind": "remote-plugin-entry"' in model


def test_apply_detects_swift_and_plugin_repos_together(tmp_path: Path) -> None:
    write(tmp_path / "Package.swift", package_manifest())
    write(tmp_path / ".codex-plugin" / "plugin.json", plugin_manifest("demo-swift-plugin"))
    write(tmp_path / "skills" / "demo-skill" / "SKILL.md", "---\nname: demo-skill\n---\n# Demo Skill\n")

    report = run(tmp_path, run_mode="apply")

    product_names = {product["name"] for product in report["detected_model"]["products"]}
    assert "DemoCore" in product_names
    assert "demo-swift-plugin" in product_names
    assert report["detected_model"]["detectionSource"].endswith("+plugin-repo")
