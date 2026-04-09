from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/swift-package-workflow/scripts/run_workflow.py"


class SwiftPackageWorkflowTests(unittest.TestCase):
    def run_script(self, *args: str, env: dict | None = None) -> tuple[int, dict]:
        command_env = dict(env or os.environ)
        command_env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "apple-dev-skills-uv-cache"))
        proc = subprocess.run(
            [str(SCRIPT), *args],
            cwd="/tmp",
            env=command_env,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, json.loads(proc.stdout)

    def test_blocks_non_package_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--operation-type", "build", "--repo-root", tmpdir)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertEqual(payload["output"]["repo_shape"]["reason"], "package-swift-missing")

    def test_succeeds_for_plain_package_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            code, payload = self.run_script("--operation-type", "build", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["path_type"], "primary")
            self.assertEqual(payload["output"]["recommended_skill"], "swift-package-build-run-workflow")
            self.assertIn("build-run skill", payload["output"]["routing_summary"])
            self.assertFalse(payload["output"]["repo_shape"]["mixed_root"])

    def test_handoffs_mixed_root_without_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--operation-type", "build", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertTrue(payload["output"]["repo_shape"]["mixed_root"])
            self.assertEqual(payload["output"]["recommended_skill"], "xcode-build-run-workflow")
            self.assertIn("xcode-build-run-workflow", payload["output"]["next_step"])

    def test_allows_mixed_root_with_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script(
                "--operation-type",
                "build",
                "--repo-root",
                tmpdir,
                "--mixed-root-opt-in",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["output"]["recommended_skill"], "swift-package-build-run-workflow")
            self.assertTrue(payload["output"]["repo_shape"]["mixed_root"])

    def test_can_infer_test_operation_from_request(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            code, payload = self.run_script("--request", "run the package tests", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["output"]["operation_type"], "test")
            self.assertEqual(payload["output"]["operation_type_source"], "inferred")
            self.assertEqual(payload["output"]["recommended_skill"], "swift-package-testing-workflow")
            self.assertIn("testing skill", payload["output"]["routing_summary"])

    def test_resource_request_exposes_inferred_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            package_root = Path(tmpdir, "WorkspaceRoot", "Packages", "DemoPkg")
            (package_root / "Sources" / "DemoTool").mkdir(parents=True)
            (package_root / "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            code, payload = self.run_script(
                "--request",
                "verify package resources and Bundle.module access",
                "--repo-root",
                str(package_root / "Sources" / "DemoTool"),
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["output"]["repo_shape"]["reason"], "package-root-inferred")
            self.assertTrue(payload["output"]["inferred_context"]["resource_request"])
            self.assertEqual(payload["output"]["inferred_context"]["primary_target"], "DemoTool")
            self.assertEqual(payload["output"]["recommended_skill"], "swift-package-build-run-workflow")

    def test_resource_request_handoffs_to_xcode_when_bundle_integration_is_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script(
                "--request",
                "copy package resources into the app target build phase",
                "--repo-root",
                tmpdir,
                "--mixed-root-opt-in",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["output"]["recommended_skill"], "xcode-build-run-workflow")
            self.assertIn("bundle integration", payload["output"]["next_step"])

    def test_blocks_when_no_operation_or_request_is_provided(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            code, payload = self.run_script("--repo-root", tmpdir)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertEqual(payload["output"]["operation_type_source"], "missing")


if __name__ == "__main__":
    unittest.main()
