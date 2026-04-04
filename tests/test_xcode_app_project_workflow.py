from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/xcode-app-project-workflow/scripts/run_workflow.py"


def write_config(tmpdir: str, skill: str, settings: dict) -> None:
    target = Path(tmpdir) / skill / "customization.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schemaVersion: 1", "isCustomized: true", "settings:"]
    for key, value in settings.items():
        if isinstance(value, bool):
            raw = "true" if value else "false"
        elif isinstance(value, int):
            raw = str(value)
        else:
            raw = f'"{value}"'
        lines.append(f"  {key}: {raw}")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


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

    def test_mutation_guard_blocks_managed_scope_without_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            env = dict(os.environ)
            code, payload = self.run_script(
                "--operation-type",
                "mutation",
                "--workspace-path",
                tmpdir,
                env=env,
            )
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertTrue(payload["guard_result"]["managed_scope"])

    def test_mutation_guard_allows_non_managed_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script(
                "--operation-type",
                "mutation",
                "--workspace-path",
                tmpdir,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertFalse(payload["guard_result"]["managed_scope"])

    def test_advisory_cooldown_and_retry_count_follow_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            write_config(
                tmpdir,
                "xcode-app-project-workflow",
                {
                    "advisoryCooldownDays": 30,
                    "mcpRetryCount": 2,
                },
            )
            state_file = Path(tmpdir) / "cooldown.json"
            state_file.write_text('{"mcp-fallback-advisory":"2999-01-01T00:00:00Z"}\n', encoding="utf-8")
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script(
                "--operation-type",
                "build",
                "--advisory-state-file",
                str(state_file),
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["retry_count"], 2)
            self.assertEqual(payload["advisory"]["cooldown_days"], 30)
            self.assertFalse(payload["advisory"]["should_emit"])

    def test_fallback_commands_follow_mapping_profile(self) -> None:
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
            self.assertIn("swift build", payload["fallback_commands"])

    def test_test_operation_prefers_workspace_and_project_fallbacks(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcworkspace").mkdir()
            Path(tmpdir, "Demo.xcodeproj").mkdir()
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
            joined = "\n".join(payload["fallback_commands"])
            self.assertIn("xcodebuild test -workspace", joined)
            self.assertIn("xcodebuild test -project", joined)

    def test_package_toolchain_management_lists_swift_and_xcode_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Package.swift").write_text("// test\n", encoding="utf-8")
            code, payload = self.run_script(
                "--operation-type",
                "package-toolchain-management",
                "--workspace-path",
                tmpdir,
                "--mcp-failure-reason",
                "session-missing",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["path_type"], "fallback")
            self.assertIn("swift package describe", payload["fallback_commands"])
            self.assertIn("xcrun --find swift", payload["fallback_commands"])
            self.assertIn("xcrun --find xcodebuild", payload["fallback_commands"])

    def test_blocked_mutation_does_not_switch_to_cli_fallback_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script(
                "--operation-type",
                "mutation",
                "--workspace-path",
                tmpdir,
                "--mcp-failure-reason",
                "timeout",
            )
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertEqual(payload["path_type"], "primary")
            self.assertIn("MCP mutation tools", payload["next_step"])


if __name__ == "__main__":
    unittest.main()
