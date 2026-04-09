from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/xcode-build-run-workflow/scripts/run_workflow.py"


def write_config(tmpdir: str, skill: str, settings: dict) -> None:
    target = Path(tmpdir) / skill / "customization.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schemaVersion: 1", "isCustomized: true", "settings:"]
    for key, value in settings.items():
        raw = str(value) if isinstance(value, int) else f'"{value}"'
        lines.append(f"  {key}: {raw}")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


class XcodeBuildRunWorkflowTests(unittest.TestCase):
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

    def test_handoffs_test_requests_to_xcode_testing_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--request", "run the UI tests", "--workspace-path", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertIn("xcode-testing-workflow", payload["output"]["next_step"])

    def test_build_fallback_includes_swift_build_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// test\n", encoding="utf-8")
            code, payload = self.run_script(
                "--operation-type",
                "build",
                "--workspace-path",
                tmpdir,
                "--mcp-failure-reason",
                "timeout",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["path_type"], "fallback")
            self.assertIn("swift build", payload["output"]["fallback_commands"])

    def test_customization_can_use_xcode_only_fallback_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// test\n", encoding="utf-8")
            write_config(
                tmpdir,
                "xcode-build-run-workflow",
                {"mcpRetryCount": 2, "fallbackCommandMappingProfile": "xcode-only"},
            )
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script(
                "--operation-type",
                "build",
                "--workspace-path",
                tmpdir,
                "--mcp-failure-reason",
                "xcode-mcp-unavailable",
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["output"]["retry_count"], 2)
            self.assertNotIn("swift build", payload["output"]["fallback_commands"])

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
            self.assertTrue(payload["output"]["guard_result"]["direct_pbxproj_edit_warning_required"])

    def test_infers_workspace_state_and_scheme_hint_from_nested_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "App" / "Demo.xcodeproj").mkdir(parents=True)
            (repo_root / "App" / "Demo.xctestplan").write_text("{}", encoding="utf-8")
            code, payload = self.run_script(
                "--operation-type",
                "build",
                "--workspace-path",
                str(repo_root / "App" / "Sources"),
                "--mcp-failure-reason",
                "timeout",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["path_type"], "fallback")
            self.assertEqual(payload["output"]["inferred_context"]["scheme_hint"], "Demo")
            self.assertTrue(payload["output"]["inferred_context"]["has_xcode_test_plan"])
            self.assertTrue(payload["output"]["workspace_state"]["project"].endswith("Demo.xcodeproj"))
            joined = "\n".join(payload["output"]["fallback_commands"])
            self.assertIn("-scheme Demo", joined)


if __name__ == "__main__":
    unittest.main()
