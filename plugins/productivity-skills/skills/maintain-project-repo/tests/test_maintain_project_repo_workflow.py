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
        self.assertIn("wait_for_initial_pr_checks", release_script)
        self.assertIn("wait_for_remote_branch", release_script)
        self.assertIn("wait_for_remote_tag", release_script)
        self.assertIn("wait_for_pr_review_state", release_script)
        self.assertIn("wait_for_github_release", release_script)
        self.assertIn("REPO_MAINTENANCE_INITIAL_CHECK_TIMEOUT_SECONDS", release_script)
        self.assertIn("push_release_branch", release_script)
        self.assertIn("push_release_tag", release_script)
        self.assertIn('rev-list -n 1 "$RELEASE_TAG"', release_script)
        self.assertIn('gh pr checks "$pr_number" --watch', release_script)
        self.assertIn('select(.state == "COMMENTED")', release_script)
        self.assertIn("valid concerns in code, or add out-of-scope concerns to ROADMAP.md", release_script)
        self.assertIn('gh pr merge "$pr_number" --merge --delete-branch', release_script)
        self.assertIn('pull --ff-only origin "$base_branch"', release_script)
        self.assertIn("Last observed state:", release_script)
        self.assertNotIn("release tag `$RELEASE_TAG` was created locally before this PR", release_script)
        standard_flow = release_script[release_script.index("run_standard_release()") :]
        self.assertLess(standard_flow.index("watch_ci \"$pr_number\""), standard_flow.index("create_release_tag"))
        self.assertLess(standard_flow.index("check_pr_comments \"$pr_number\""), standard_flow.index("create_release_tag"))
        self.assertLess(standard_flow.index("fast_forward_base_branch"), standard_flow.index("create_release_tag"))

    def test_common_release_helpers_cover_delayed_github_state(self) -> None:
        common_script = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/lib/common.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("wait_for_remote_branch", common_script)
        self.assertIn("wait_for_remote_tag", common_script)
        self.assertIn("wait_for_github_release", common_script)
        self.assertIn("REPO_MAINTENANCE_GH_WAIT_TIMEOUT_SECONDS", common_script)
        self.assertIn("REPO_MAINTENANCE_GH_WAIT_POLL_SECONDS", common_script)
        self.assertIn("REPO_MAINTENANCE_REMOTE_BRANCH_TIMEOUT_SECONDS", common_script)
        self.assertIn("REPO_MAINTENANCE_REMOTE_TAG_TIMEOUT_SECONDS", common_script)
        self.assertIn("REPO_MAINTENANCE_GH_RELEASE_TIMEOUT_SECONDS", common_script)
        self.assertIn("positive_integer_or_default", common_script)

        push_step = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/release/30-push-release.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn('wait_for_remote_branch "$branch_name"', push_step)
        self.assertIn('wait_for_remote_tag "$RELEASE_TAG"', push_step)

        release_step = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/release/40-github-release.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn('wait_for_github_release "$RELEASE_TAG"', release_step)

    def test_release_env_documents_github_wait_defaults(self) -> None:
        release_env = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/config/release.env").read_text(
            encoding="utf-8"
        )
        self.assertIn("REPO_MAINTENANCE_GH_WAIT_TIMEOUT_SECONDS=120", release_env)
        self.assertIn("REPO_MAINTENANCE_GH_WAIT_POLL_SECONDS=5", release_env)
        self.assertIn("transient indexing gaps", release_env)

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
