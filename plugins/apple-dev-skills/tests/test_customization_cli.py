from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = {
    "xcode-app-project-workflow": ROOT / "skills/xcode-app-project-workflow/scripts/customization_config.py",
    "xcode-build-run-workflow": ROOT / "skills/xcode-build-run-workflow/scripts/customization_config.py",
    "xcode-testing-workflow": ROOT / "skills/xcode-testing-workflow/scripts/customization_config.py",
    "explore-apple-swift-docs": ROOT / "skills/explore-apple-swift-docs/scripts/customization_config.py",
    "bootstrap-swift-package": ROOT / "skills/bootstrap-swift-package/scripts/customization_config.py",
    "swift-package-build-run-workflow": ROOT / "skills/swift-package-build-run-workflow/scripts/customization_config.py",
    "swift-package-testing-workflow": ROOT / "skills/swift-package-testing-workflow/scripts/customization_config.py",
}


class CustomizationCliTests(unittest.TestCase):
    def run_cli(self, script: Path, *args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
        command_env = dict(env or os.environ)
        command_env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "apple-dev-skills-uv-cache"))
        return subprocess.run(
            [str(script), *args],
            cwd="/tmp",
            env=command_env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_effective_apply_and_reset_roundtrip(self) -> None:
        override_text = 'isCustomized: true\nsettings:\n  sampleKey: "sampleValue"\n'

        for skill_name, script in SKILL_SCRIPTS.items():
            with self.subTest(skill=skill_name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    env = dict(os.environ)
                    env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir

                    initial = self.run_cli(script, "effective", env=env)
                    self.assertEqual(initial.returncode, 0)
                    self.assertIn("schemaVersion: 1", initial.stdout)
                    self.assertIn("settings:", initial.stdout)

                    override_path = Path(tmpdir) / "override.yaml"
                    override_path.write_text(override_text, encoding="utf-8")

                    apply = self.run_cli(script, "apply", "--input", str(override_path), env=env)
                    self.assertEqual(apply.returncode, 0)
                    expected_path = Path(tmpdir) / skill_name / "customization.yaml"
                    self.assertEqual(Path(apply.stdout.strip()), expected_path)
                    self.assertTrue(expected_path.is_file())

                    updated = self.run_cli(script, "effective", env=env)
                    self.assertEqual(updated.returncode, 0)
                    self.assertIn("sampleKey: \"sampleValue\"", updated.stdout)

                    reset = self.run_cli(script, "reset", env=env)
                    self.assertEqual(reset.returncode, 0)
                    self.assertEqual(Path(reset.stdout.strip()), expected_path)
                    self.assertFalse(expected_path.exists())

    def test_apply_rejects_invalid_override_yaml(self) -> None:
        invalid_text = "settings:\n  nested:\n    child: true\n"

        for skill_name, script in SKILL_SCRIPTS.items():
            with self.subTest(skill=skill_name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    env = dict(os.environ)
                    env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
                    override_path = Path(tmpdir) / "invalid.yaml"
                    override_path.write_text(invalid_text, encoding="utf-8")

                    proc = self.run_cli(script, "apply", "--input", str(override_path), env=env)
                    self.assertEqual(proc.returncode, 1)
                    self.assertIn("settings values must be scalar", proc.stderr)


if __name__ == "__main__":
    unittest.main()
