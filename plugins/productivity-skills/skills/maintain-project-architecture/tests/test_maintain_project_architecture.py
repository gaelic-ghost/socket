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
