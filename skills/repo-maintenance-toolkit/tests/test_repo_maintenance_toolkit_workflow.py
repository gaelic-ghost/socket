from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/repo-maintenance-toolkit/scripts/run_workflow.py"


class RepoMaintenanceToolkitWorkflowTests(unittest.TestCase):
    def run_script(self, *args: str, env: dict | None = None) -> tuple[int, dict]:
        command_env = dict(env or os.environ)
        command_env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "productivity-skills-uv-cache"))
        proc = subprocess.run(
            [str(SCRIPT), *args],
            cwd="/tmp",
            env=command_env,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, json.loads(proc.stdout)

    def test_report_only_lists_managed_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "report-only")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["path_type"], "fallback")
            self.assertIn("scripts/repo-maintenance/validate-all.sh", payload["managed_files"])
            self.assertIn(".github/workflows/validate-repo-maintenance.yml", payload["managed_files"])

    def test_install_writes_toolkit_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "install")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertTrue(Path(tmpdir, "scripts/repo-maintenance/validate-all.sh").is_file())
            self.assertTrue(Path(tmpdir, "scripts/repo-maintenance/release.sh").is_file())
            self.assertTrue(Path(tmpdir, ".github/workflows/validate-repo-maintenance.yml").is_file())

    def test_refresh_preserves_repo_specific_extra_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "install")
            self.assertEqual(code, 0)

            custom_script = Path(tmpdir, "scripts/repo-maintenance/validations/90-custom.sh")
            custom_script.parent.mkdir(parents=True, exist_ok=True)
            custom_script.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")

            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "refresh")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertTrue(custom_script.is_file())


if __name__ == "__main__":
    unittest.main()
