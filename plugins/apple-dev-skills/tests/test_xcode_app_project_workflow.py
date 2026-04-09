from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/xcode-app-project-workflow/scripts/run_workflow.py"


class XcodeWorkflowTests(unittest.TestCase):
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

    def test_routes_build_requests_to_xcode_build_run_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--operation-type", "build", "--workspace-path", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["output"]["recommended_skill"], "xcode-build-run-workflow")

    def test_routes_test_requests_to_xcode_testing_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--request", "run the UI tests with the test plan", "--workspace-path", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["output"]["recommended_skill"], "xcode-testing-workflow")

    def test_exposes_workspace_context_for_nested_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "App" / "Demo.xcodeproj").mkdir(parents=True)
            (repo_root / "App" / "Demo.xctestplan").write_text("{}", encoding="utf-8")
            code, payload = self.run_script("--operation-type", "build", "--workspace-path", str(repo_root / "App" / "Sources"))
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["output"]["inferred_context"]["scheme_hint"], "Demo")
            self.assertTrue(payload["output"]["inferred_context"]["has_xcode_test_plan"])
            self.assertTrue(payload["output"]["workspace_state"]["project"].endswith("Demo.xcodeproj"))

    def test_direct_pbxproj_edit_requires_explicit_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "project.pbxproj").write_text("// !$*UTF8*$!\n", encoding="utf-8")
            code, payload = self.run_script(
                "--operation-type",
                "mutation",
                "--workspace-path",
                tmpdir,
                "--direct-pbxproj-edit",
            )
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertEqual(payload["path_type"], "primary")
            self.assertTrue(payload["output"]["guard_result"]["direct_pbxproj_edit_warning_required"])
            self.assertIn("Warn the user", payload["output"]["next_step"])

    def test_direct_pbxproj_edit_can_proceed_after_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "project.pbxproj").write_text("// !$*UTF8*$!\n", encoding="utf-8")
            code, payload = self.run_script(
                "--operation-type",
                "mutation",
                "--workspace-path",
                tmpdir,
                "--direct-pbxproj-edit",
                "--direct-pbxproj-edit-opt-in",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertTrue(payload["output"]["guard_result"]["direct_pbxproj_edit_warning_required"])
            self.assertEqual(payload["output"]["recommended_skill"], "xcode-build-run-workflow")

    def test_blocks_when_no_operation_or_request_is_provided(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--workspace-path", tmpdir)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertEqual(payload["output"]["operation_type_source"], "missing")


if __name__ == "__main__":
    unittest.main()
