from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "skills/bootstrap-xcode-workspace/scripts/run_workflow.py"
SYNC = ROOT / "skills/sync-xcode-workspace-guidance/scripts/run_workflow.py"
APP_SYNC = ROOT / "skills/sync-xcode-project-guidance/scripts/run_workflow.py"


def run_script(script: Path, *args: str) -> tuple[int, dict]:
    env = dict(os.environ)
    env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "apple-dev-skills-uv-cache"))
    process = subprocess.run(
        ["uv", "run", str(script), *args],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )
    return process.returncode, json.loads(process.stdout)


class XcodeWorkspaceWorkflowTests(unittest.TestCase):
    def test_bootstrap_defaults_to_separate_projects(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(
                BOOTSTRAP,
                "--name",
                "Product",
                "--destination",
                tmpdir,
                "--dry-run",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["normalized_inputs"]["app_topology"], "separate-projects")
            self.assertEqual(payload["normalized_inputs"]["platforms"], ["ios", "macos"])
            self.assertIn("create the .xcworkspace through Xcode", " ".join(payload["actions"]))

    def test_bootstrap_rejects_watchos_multiplatform_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(
                BOOTSTRAP,
                "--name",
                "Product",
                "--destination",
                tmpdir,
                "--app-topology",
                "multiplatform-target",
                "--platforms",
                "ios,watchos",
            )
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn("watchOS requires", payload["stderr"])

    def test_sync_writes_bounded_workspace_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Product.xcworkspace").mkdir()
            (root / "Apps/ProductiOS/ProductiOS.xcodeproj").mkdir(parents=True)
            (root / "Apps/ProductiOS/project.yml").write_text("name: ProductiOS\n", encoding="utf-8")
            (root / "Packages/ProductCore").mkdir(parents=True)
            (root / "Packages/ProductCore/Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            code, payload = run_script(SYNC, "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(len(payload["detected_state"]["app_projects"]), 1)
            self.assertEqual(len(payload["detected_state"]["packages"]), 1)
            agents = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("## Apple / Xcode Workspace Workflow", agents)
            self.assertIn("schemePathPrefix", agents)

    def test_app_sync_redirects_workspace_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Product.xcworkspace").mkdir()
            (root / "Apps" / "Product.xcodeproj").mkdir(parents=True)
            (root / "Packages").mkdir()
            code, payload = run_script(APP_SYNC, "--repo-root", tmpdir)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn("sync-xcode-workspace-guidance", payload["next_step"])

    def test_docs_record_current_xcodegen_workspace_contract(self) -> None:
        bootstrap = (ROOT / "skills/bootstrap-xcode-workspace/SKILL.md").read_text(encoding="utf-8")
        xcodegen = (ROOT / "skills/xcode-build-run-workflow/references/xcodegen-project-maintenance.md").read_text(encoding="utf-8")
        self.assertIn("separate-projects", bootstrap)
        self.assertIn("multiplatform-target", bootstrap)
        self.assertIn("schemePathPrefix", bootstrap)
        self.assertIn("XcodeGen `2.46.0`", xcodegen)
