from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/swift-package-testing-workflow/scripts/run_workflow.py"


class SwiftPackageTestingWorkflowTests(unittest.TestCase):
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

    def test_succeeds_for_plain_package_tests(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            code, payload = self.run_script("--operation-type", "test", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["output"]["planned_commands"][0], "swift test")

    def test_handoffs_build_requests_to_build_run_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            code, payload = self.run_script("--request", "build the release artifact", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertIn("swift-package-build-run-workflow", payload["output"]["next_step"])

    def test_handoffs_mixed_root_without_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--operation-type", "test", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertIn("xcode-testing-workflow", payload["output"]["next_step"])

    def test_infers_test_plan_and_scheme_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            package_root = Path(tmpdir)
            (package_root / "Tests" / "DemoPkgTests").mkdir(parents=True)
            (package_root / "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            (package_root / "DemoPkg.xctestplan").write_text("{}", encoding="utf-8")
            code, payload = self.run_script("--operation-type", "test", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertTrue(payload["output"]["inferred_context"]["has_xcode_test_plan"])
            self.assertEqual(payload["output"]["inferred_context"]["xcode_scheme_hint"], "DemoPkg")
            joined = "\n".join(payload["output"]["planned_commands"])
            self.assertIn("-showTestPlans", joined)
            self.assertIn("-testPlan DemoPkg", joined)

    def test_blocks_when_no_operation_or_request_is_provided(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            code, payload = self.run_script("--repo-root", tmpdir)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
