from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/apple-swift-package-bootstrap/scripts/run_workflow.py"


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


class BootstrapWorkflowTests(unittest.TestCase):
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

    def test_wrapper_injects_runtime_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            write_config(
                tmpdir,
                "apple-swift-package-bootstrap",
                {
                    "defaultPackageType": "executable",
                    "defaultPlatformPreset": "mac",
                    "defaultVersionProfile": "latest-major",
                    "defaultTestingMode": "xctest",
                    "initializeGit": False,
                    "copyAgentsMd": False,
                },
            )
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script("--name", "DemoPkg", "--dry-run", env=env)
            self.assertEqual(code, 0)
            self.assertEqual(payload["normalized_inputs"]["type"], "executable")
            self.assertEqual(payload["normalized_inputs"]["platform"], "mac")
            self.assertEqual(payload["normalized_inputs"]["version_profile"], "latest-major")
            self.assertEqual(payload["normalized_inputs"]["testing_mode"], "xctest")
            self.assertFalse(payload["normalized_inputs"]["initialize_git"])
            self.assertFalse(payload["normalized_inputs"]["copy_agents_md"])
            self.assertIn("--testing-mode", payload["command"])
            self.assertIn("xctest", payload["command"])
            self.assertIn("--skip-git-init", payload["command"])
            self.assertIn("--skip-copy-agents", payload["command"])

    def test_explicit_args_override_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            write_config(
                tmpdir,
                "apple-swift-package-bootstrap",
                {
                    "defaultPackageType": "library",
                    "defaultPlatformPreset": "multiplatform",
                    "defaultVersionProfile": "current-minus-one",
                },
            )
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--type",
                "tool",
                "--platform",
                "mobile",
                "--version-profile",
                "current-minus-two",
                "--testing-mode",
                "swift-testing",
                "--dry-run",
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["normalized_inputs"]["type"], "tool")
            self.assertEqual(payload["normalized_inputs"]["platform"], "mobile")
            self.assertEqual(payload["normalized_inputs"]["version_profile"], "current-minus-two")
            self.assertEqual(payload["normalized_inputs"]["testing_mode"], "swift-testing")

    def test_wrapper_normalizes_shell_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            blocking_file = Path(tmpdir) / "not-a-directory"
            blocking_file.write_text("x", encoding="utf-8")
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--destination",
                str(blocking_file),
                "--skip-validation",
            )
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "failed")
            self.assertIn("Fix the bootstrap error", payload["next_step"])

    @unittest.skipUnless(shutil.which("swift"), "swift is required for end-to-end bootstrap success")
    def test_wrapper_normalizes_shell_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--destination",
                tmpdir,
                "--skip-validation",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertTrue(payload["resolved_path"].endswith("DemoPkg"))
            self.assertEqual(payload["testing_mode"], "swift-testing")

    @unittest.skipUnless(shutil.which("swift"), "swift is required for executable bootstrap coverage")
    def test_executable_bootstrap_creates_swift_testing_test_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--type",
                "executable",
                "--destination",
                tmpdir,
                "--skip-validation",
            )
            self.assertEqual(code, 0)
            package_dir = Path(payload["resolved_path"])
            test_file = package_dir / "Tests" / "DemoPkgTests" / "DemoPkgTests.swift"
            self.assertTrue(test_file.is_file())
            test_text = test_file.read_text(encoding="utf-8")
            self.assertIn("import Testing", test_text)
            self.assertIn("@Test", test_text)


if __name__ == "__main__":
    unittest.main()
