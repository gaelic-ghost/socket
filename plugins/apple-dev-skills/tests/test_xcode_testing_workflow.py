from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/xcode-testing-workflow/scripts/run_workflow.py"


class XcodeTestingWorkflowTests(unittest.TestCase):
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

    def test_handoffs_build_requests_to_xcode_build_run_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--request", "build the release artifact", "--workspace-path", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertIn("xcode-build-run-workflow", payload["output"]["next_step"])

    def test_test_fallback_prefers_workspace_commands_and_test_plans(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcworkspace").mkdir()
            code, payload = self.run_script(
                "--operation-type",
                "test",
                "--workspace-path",
                tmpdir,
                "--mcp-failure-reason",
                "timeout",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["path_type"], "fallback")
            joined = "\n".join(payload["output"]["fallback_commands"])
            self.assertIn("xcodebuild test -workspace", joined)
            self.assertIn("-showTestPlans", joined)

    def test_mutation_still_warns_for_direct_pbxproj_edit(self) -> None:
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
            self.assertTrue(payload["output"]["guard_result"]["direct_pbxproj_edit_warning_required"])

    def test_infers_test_plan_and_ui_test_context_from_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "Demo.xcworkspace").mkdir()
            (repo_root / "Demo.xctestplan").write_text("{}", encoding="utf-8")
            (repo_root / "Tests" / "DemoUITests").mkdir(parents=True)
            code, payload = self.run_script(
                "--operation-type",
                "test",
                "--workspace-path",
                tmpdir,
                "--mcp-failure-reason",
                "timeout",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["path_type"], "fallback")
            self.assertEqual(payload["output"]["inferred_context"]["scheme_hint"], "Demo")
            self.assertTrue(payload["output"]["inferred_context"]["has_xcode_test_plan"])
            self.assertIn("DemoUITests", payload["output"]["inferred_context"]["ui_test_targets"])
            joined = "\n".join(payload["output"]["fallback_commands"])
            self.assertIn("-testPlan Demo", joined)
            self.assertIn("-scheme Demo", joined)


if __name__ == "__main__":
    unittest.main()
