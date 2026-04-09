from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/sync-xcode-project-guidance/scripts/run_workflow.py"


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


class XcodeGuidanceSyncWorkflowTests(unittest.TestCase):
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

    def test_blocks_non_xcode_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn(".xcodeproj", payload["stderr"])

    def test_dry_run_plans_agents_creation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--repo-root", tmpdir, "--dry-run")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["path_type"], "fallback")
            self.assertIn("create AGENTS.md from assets/AGENTS.md", payload["actions"])

    def test_sync_creates_agents_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            agents_text = Path(tmpdir, "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("xcode-build-run-workflow", agents_text)
            self.assertIn("xcode-testing-workflow", agents_text)
            self.assertIn("sync-xcode-project-guidance", agents_text)
            self.assertIn(".xctestplan", agents_text)
            self.assertIn("project membership, target membership, build phases, and resource inclusion", agents_text)
            self.assertIn("Debug and Release", agents_text)
            self.assertIn("Never edit `.pbxproj` files directly.", agents_text)
            self.assertTrue(Path(tmpdir, "scripts/repo-maintenance/validate-all.sh").is_file())
            self.assertTrue(Path(tmpdir, "scripts/repo-maintenance/config/profile.env").is_file())
            self.assertIn(
                'REPO_MAINTENANCE_PROFILE="xcode-app"',
                Path(tmpdir, "scripts/repo-maintenance/config/profile.env").read_text(encoding="utf-8"),
            )
            self.assertTrue(Path(tmpdir, ".github/workflows/validate-repo-maintenance.yml").is_file())

    def test_sync_appends_section_to_existing_agents(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            agents_path = Path(tmpdir, "AGENTS.md")
            agents_path.write_text("# AGENTS.md\n\n## Existing Section\n\n- Keep this content.\n", encoding="utf-8")
            code, payload = self.run_script("--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            agents_text = agents_path.read_text(encoding="utf-8")
            self.assertIn("## Existing Section", agents_text)
            self.assertIn("## Apple / Xcode Project Workflow", agents_text)
            self.assertIn(".xctestplan", agents_text)
            self.assertIn("project membership, target membership, build phases, and resource inclusion", agents_text)
            self.assertTrue(Path(tmpdir, "scripts/repo-maintenance/release.sh").is_file())
            self.assertIn(
                'REPO_MAINTENANCE_PROFILE="xcode-app"',
                Path(tmpdir, "scripts/repo-maintenance/config/profile.env").read_text(encoding="utf-8"),
            )

    def test_write_mode_can_disable_append_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            Path(tmpdir, "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
            write_config(
                tmpdir,
                "sync-xcode-project-guidance",
                {"writeMode": "create-missing-only"},
            )
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script("--repo-root", tmpdir, env=env)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn("append behavior is disabled", payload["stderr"])

    def test_report_only_mode_returns_non_mutating_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            write_config(
                tmpdir,
                "sync-xcode-project-guidance",
                {"writeMode": "report-only"},
            )
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script("--repo-root", tmpdir, env=env)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["path_type"], "fallback")
            self.assertIn("report that AGENTS.md is missing", payload["actions"][0])


if __name__ == "__main__":
    unittest.main()
