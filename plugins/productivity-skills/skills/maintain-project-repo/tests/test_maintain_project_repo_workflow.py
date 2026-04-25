from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/maintain-project-repo/scripts/run_workflow.py"


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
            self.assertIn("scripts/repo-maintenance/config/profile.env", payload["managed_files"])
            self.assertEqual(payload["profile"], "generic")

    def test_install_writes_toolkit_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "install", "--profile", "swift-package")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertTrue(Path(tmpdir, "scripts/repo-maintenance/validate-all.sh").is_file())
            self.assertTrue(Path(tmpdir, "scripts/repo-maintenance/release.sh").is_file())
            self.assertTrue(Path(tmpdir, "scripts/repo-maintenance/config/profile.env").is_file())
            self.assertTrue(Path(tmpdir, ".swiftformat").is_file())
            self.assertTrue(Path(tmpdir, ".swiftlint.yml").is_file())
            self.assertIn('REPO_MAINTENANCE_PROFILE="swift-package"', Path(tmpdir, "scripts/repo-maintenance/config/profile.env").read_text(encoding="utf-8"))
            swiftlint_text = Path(tmpdir, ".swiftlint.yml").read_text(encoding="utf-8")
            self.assertIn("SwiftFormat owns visual shape", swiftlint_text)
            self.assertIn("fatal_error_message", swiftlint_text)
            hook_text = Path(tmpdir, "scripts/repo-maintenance/hooks/pre-commit.sample").read_text(encoding="utf-8")
            self.assertIn("swiftformat --lint", hook_text)
            self.assertTrue(Path(tmpdir, ".github/workflows/validate-repo-maintenance.yml").is_file())
            workflow_text = Path(tmpdir, ".github/workflows/validate-repo-maintenance.yml").read_text(encoding="utf-8")
            self.assertIn("Branch protection should require the Actions check context `validate`.", workflow_text)
            self.assertIn("  validate:\n    name: validate\n", workflow_text)
            self.assertIn("brew install swiftformat swiftlint", workflow_text)

    def test_generic_profile_keeps_generic_pre_commit_hook(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "install")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertFalse(Path(tmpdir, ".swiftformat").exists())
            self.assertFalse(Path(tmpdir, ".swiftlint.yml").exists())
            hook_text = Path(tmpdir, "scripts/repo-maintenance/hooks/pre-commit.sample").read_text(encoding="utf-8")
            self.assertNotIn("swiftformat --lint", hook_text)
            self.assertIn('exec "$repo_root/scripts/repo-maintenance/validate-all.sh"', hook_text)

    def test_generated_validation_uses_repo_maintenance_self_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "install")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")

            Path(tmpdir, "AGENTS.md").write_text(
                "\n".join(
                    [
                        "# AGENTS.md",
                        "",
                        "- scripts/repo-maintenance/validate-all.sh",
                        "- scripts/repo-maintenance/sync-shared.sh",
                        "- scripts/repo-maintenance/release.sh",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True, text=True)

            proc = subprocess.run(
                ["sh", "scripts/repo-maintenance/validate-all.sh"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            self.assertIn("Repo-maintenance validation completed successfully.", proc.stdout)

    def test_release_script_encodes_protected_main_standard_flow(self) -> None:
        release_script = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/release.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("Standard release mode must run from a release branch or worktree", release_script)
        self.assertIn("version-bump.sh", release_script)
        self.assertIn('gh pr checks "$pr_number" --watch', release_script)
        self.assertIn("valid concerns in code, or add out-of-scope concerns to ROADMAP.md", release_script)
        self.assertIn('gh pr merge "$pr_number" --merge --delete-branch', release_script)
        self.assertIn('pull --ff-only origin "$base_branch"', release_script)

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

    def test_report_only_can_select_xcode_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "report-only", "--profile", "xcode-app")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["profile"], "xcode-app")
            joined = "\n".join(payload["actions"])
            self.assertIn("profile.env", joined)
            self.assertIn("xcode-app profile", joined)


if __name__ == "__main__":
    unittest.main()
