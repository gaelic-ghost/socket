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
        command_env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "repository-skills-uv-cache"))
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
            self.assertIn("runs-on: macos-26", workflow_text)
            self.assertIn("actions/checkout@v6.0.2", workflow_text)
            self.assertIn("xcode-select --print-path", workflow_text)
            self.assertNotIn("actions/checkout@v4", workflow_text)
            self.assertNotIn("maxim-lobanov/setup-xcode@v1", workflow_text)
            self.assertIn("xcrun swift --version", workflow_text)
            self.assertIn("brew install swiftformat swiftlint", workflow_text)

    def test_xcode_profile_uses_standard_capital_scripts_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "install", "--profile", "xcode-app")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertIn("Scripts/repo-maintenance/validate-all.sh", payload["managed_files"])
            self.assertIn("Scripts/repo-maintenance/config/profile.env", payload["managed_files"])
            self.assertTrue(Path(tmpdir, "Scripts/repo-maintenance/validate-all.sh").is_file())
            self.assertTrue(Path(tmpdir, "Scripts/repo-maintenance/release.sh").is_file())
            self.assertTrue(Path(tmpdir, "Scripts/repo-maintenance/config/profile.env").is_file())
            Path(tmpdir, "case-probe").touch()
            if not Path(tmpdir, "CASE-PROBE").exists():
                self.assertFalse(Path(tmpdir, "scripts/repo-maintenance/validate-all.sh").exists())
            self.assertIn(
                'REPO_MAINTENANCE_PROFILE="xcode-app"',
                Path(tmpdir, "Scripts/repo-maintenance/config/profile.env").read_text(encoding="utf-8"),
            )
            workflow_text = Path(tmpdir, ".github/workflows/validate-repo-maintenance.yml").read_text(encoding="utf-8")
            self.assertIn("bash Scripts/repo-maintenance/validate-all.sh", workflow_text)
            self.assertNotIn("scripts/repo-maintenance", workflow_text)

    def test_xcode_profile_migrates_legacy_lowercase_toolkit_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "case-probe").touch()
            if Path(tmpdir, "CASE-PROBE").exists():
                self.skipTest("legacy lowercase-to-capital migration requires a case-sensitive filesystem")

            legacy_custom = Path(tmpdir, "scripts/repo-maintenance/validations/90-custom.sh")
            legacy_custom.parent.mkdir(parents=True)
            legacy_custom.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")

            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "refresh", "--profile", "xcode-app")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertIn(
                "migrated legacy scripts/repo-maintenance to Scripts/repo-maintenance for xcode-app profile",
                payload["actions"],
            )
            self.assertFalse(Path(tmpdir, "scripts/repo-maintenance").exists())
            self.assertTrue(Path(tmpdir, "Scripts/repo-maintenance/validations/90-custom.sh").is_file())
            self.assertTrue(Path(tmpdir, "Scripts/repo-maintenance/validate-all.sh").is_file())

    def test_generic_profile_uses_generic_macos_latest_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script("--repo-root", tmpdir, "--operation", "install")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            workflow_text = Path(tmpdir, ".github/workflows/validate-repo-maintenance.yml").read_text(encoding="utf-8")
            self.assertIn("runs-on: macos-latest", workflow_text)
            self.assertIn("actions/checkout@v6.0.2", workflow_text)
            self.assertNotIn("actions/checkout@v4", workflow_text)
            self.assertNotIn("maxim-lobanov/setup-xcode@v1", workflow_text)

    def test_managed_workflows_avoid_node20_action_versions(self) -> None:
        workflow_assets = [
            ROOT / "skills/maintain-project-repo/assets/github/repo-maintenance-workflows/validate-repo-maintenance.yml",
            ROOT
            / "skills/maintain-project-repo/assets/profiles/apple/github/repo-maintenance-workflows/validate-repo-maintenance.yml",
        ]
        for workflow_asset in workflow_assets:
            with self.subTest(workflow=workflow_asset.name):
                workflow_text = workflow_asset.read_text(encoding="utf-8")
                self.assertIn("actions/checkout@v6.0.2", workflow_text)
                self.assertNotIn("actions/checkout@v4", workflow_text)
                self.assertNotIn("maxim-lobanov/setup-xcode@v1", workflow_text)

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
        self.assertIn("ensure_operation", release_script)
        self.assertIn("--operation prepare|inspect|advance", release_script)
        self.assertIn("Version bump commit for $RELEASE_TAG is already at HEAD", release_script)
        self.assertIn("emit_continuation_packet", release_script)
        self.assertIn("minimum_delay_minutes", release_script)
        self.assertIn("reuse a live matching host-native continuation", release_script)
        self.assertIn("inspect_pr_gate", release_script)
        self.assertIn("--json name,bucket", release_script)
        self.assertIn("REPO_MAINTENANCE_MIN_REQUIRED_CHECKS", release_script)
        self.assertIn("gh pr checks exits 8 while pending", release_script)
        self.assertIn('not-started|awaiting-branch-visibility', release_script)
        self.assertIn("remote_branch_is_visible", release_script)
        self.assertIn("remote_tag_is_visible", release_script)
        self.assertIn("github_release_is_visible", release_script)
        self.assertIn("push_release_branch", release_script)
        self.assertIn("push_release_tag", release_script)
        self.assertIn('rev-list -n 1 "$RELEASE_TAG"', release_script)
        self.assertNotIn('gh pr checks "$pr_number" --watch', release_script)
        self.assertNotIn('sleep "$poll_seconds"', release_script)
        self.assertIn('select(.state == "COMMENTED")', release_script)
        self.assertIn("valid concerns in code, or add out-of-scope concerns to ROADMAP.md", release_script)
        self.assertIn('gh pr merge "$pr_number" --merge --delete-branch', release_script)
        self.assertIn('pull --ff-only origin "$base_branch"', release_script)
        self.assertNotIn("release tag `$RELEASE_TAG` was created locally before this PR", release_script)
        standard_flow = release_script[release_script.index("run_standard_release()") :]
        self.assertLess(standard_flow.index("inspect_pr_gate \"$pr_number\""), standard_flow.index("create_release_tag"))
        self.assertLess(standard_flow.index("check_pr_comments \"$pr_number\""), standard_flow.index("create_release_tag"))
        self.assertLess(standard_flow.index("fast_forward_base_branch"), standard_flow.index("create_release_tag"))

    def test_common_release_helpers_cover_delayed_github_state(self) -> None:
        common_script = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/lib/common.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("remote_branch_is_visible", common_script)
        self.assertIn("remote_tag_is_visible", common_script)
        self.assertIn("github_release_is_visible", common_script)
        self.assertNotIn("github_wait_timeout", common_script)
        self.assertNotIn("sleep", common_script)

        push_step = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/release/30-push-release.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn('remote_branch_is_visible "$branch_name"', push_step)
        self.assertIn('remote_tag_is_visible "$RELEASE_TAG"', push_step)

        release_step = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/release/40-github-release.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn('github_release_is_visible "$RELEASE_TAG"', release_step)

    def test_release_helpers_preserve_prerelease_github_metadata(self) -> None:
        common_script = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/lib/common.sh").read_text(
            encoding="utf-8"
        )
        release_script = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/release.sh").read_text(
            encoding="utf-8"
        )
        release_step = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/release/40-github-release.sh").read_text(
            encoding="utf-8"
        )

        self.assertIn("is_semver_prerelease_tag", common_script)
        self.assertIn("expected_github_prerelease_value", common_script)
        self.assertIn("github_release_create_prerelease_flag", common_script)
        self.assertIn("verify_github_release_prerelease_metadata", common_script)
        self.assertIn("--json isPrerelease --jq .isPrerelease", common_script)
        self.assertIn("prerelease metadata mismatch", common_script)

        for release_text in (release_script, release_step):
            with self.subTest(surface=release_text[:32]):
                self.assertIn('prerelease_flag="$(github_release_create_prerelease_flag "$RELEASE_TAG")"', release_text)
                self.assertIn('create_github_release_from_notes_or_generated "$RELEASE_TAG" "$prerelease_flag"', release_text)
                self.assertIn('verify_github_release_prerelease_metadata "$RELEASE_TAG"', release_text)

    def test_release_notes_helper_prefers_checked_in_notes_then_falls_back(self) -> None:
        common_script = ROOT / "skills/maintain-project-repo/assets/repo-maintenance/lib/common.sh"
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            notes_dir = repo_root / "docs/releases"
            notes_dir.mkdir(parents=True)
            tagged_notes = notes_dir / "v1.2.3.md"
            versioned_notes = notes_dir / "1.2.3.md"
            tagged_notes.write_text("# Tagged notes\n", encoding="utf-8")
            versioned_notes.write_text("# Versioned notes\n", encoding="utf-8")
            fake_bin = repo_root / "bin"
            fake_bin.mkdir()
            fake_gh = fake_bin / "gh"
            fake_gh.write_text('#!/usr/bin/env sh\nprintf "%s\\n" "$*" >> "$GH_LOG"\n', encoding="utf-8")
            fake_gh.chmod(0o755)
            log_path = repo_root / "gh.log"

            script = '\n'.join(
                [
                    f'. "{common_script}"',
                    f'REPO_ROOT="{repo_root}"',
                    'create_github_release_from_notes_or_generated v1.2.3 ""',
                ]
            )
            env = dict(os.environ, PATH=f"{fake_bin}:{os.environ['PATH']}", GH_LOG=str(log_path))
            subprocess.run(["sh", "-c", script], check=True, capture_output=True, text=True, env=env)
            self.assertIn(f"--notes-file {tagged_notes}", log_path.read_text(encoding="utf-8"))

            tagged_notes.unlink()
            log_path.unlink()
            subprocess.run(["sh", "-c", script], check=True, capture_output=True, text=True, env=env)
            self.assertIn(f"--notes-file {versioned_notes}", log_path.read_text(encoding="utf-8"))

            versioned_notes.unlink()
            log_path.unlink()
            subprocess.run(["sh", "-c", script], check=True, capture_output=True, text=True, env=env)
            self.assertIn("--generate-notes", log_path.read_text(encoding="utf-8"))

    def test_coderabbit_review_unavailable_fixtures_are_narrow(self) -> None:
        helper = ROOT / "skills/maintain-project-repo/assets/repo-maintenance/lib/coderabbit.sh"
        fixtures = [
            ("CodeRabbit", "Review unavailable: monthly quota reached.", 0),
            ("coderabbitai", "Rate limit reached; no review was produced.", 0),
            ("CodeRabbit", "Found a potential nil dereference.", 1),
            ("GitHub Actions", "Rate limit reached.", 1),
        ]
        for source, message, expected_returncode in fixtures:
            with self.subTest(source=source, message=message):
                proc = subprocess.run(
                    ["sh", "-c", f'. "{helper}"; coderabbit_review_is_unavailable "$1" "$2"', "sh", source, message],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(proc.returncode, expected_returncode, proc.stderr)

    def test_release_gate_only_exempts_explicit_coderabbit_unavailability(self) -> None:
        release_script = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/release.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("detect_coderabbit_review_unavailable", release_script)
        self.assertIn("repos/$repo_name/commits/$head_sha/check-runs", release_script)
        self.assertIn("CODERABBIT_UNAVAILABLE_COMMENT_COUNT", release_script)
        self.assertIn('contains("coderabbit")', release_script)
        self.assertIn("ignoring only its pending review context and diagnostic comments", release_script)

    def test_release_env_documents_scheduled_continuation_default(self) -> None:
        release_env = (ROOT / "skills/maintain-project-repo/assets/repo-maintenance/config/release.env").read_text(
            encoding="utf-8"
        )
        self.assertIn("REPO_MAINTENANCE_RELEASE_OPERATION=prepare", release_env)
        self.assertIn("REPO_MAINTENANCE_MIN_REQUIRED_CHECKS=1", release_env)
        self.assertIn("host-native continuation", release_env)
        self.assertIn("five", release_env)
        self.assertIn("Never add a shell poll loop", release_env)
        self.assertIn("do not delete/recreate it after an unchanged snapshot", release_env)

    def test_release_guidance_reuses_healthy_pending_continuations(self) -> None:
        skill_text = (ROOT / "skills/maintain-project-repo/SKILL.md").read_text(encoding="utf-8")
        release_modes = (ROOT / "skills/maintain-project-repo/references/release-modes.md").read_text(
            encoding="utf-8"
        )
        prompts = (ROOT / "skills/maintain-project-repo/references/automation-prompts.md").read_text(
            encoding="utf-8"
        )

        for text in (skill_text, release_modes, prompts):
            with self.subTest(surface=text[:32]):
                self.assertIn("matching", text)
                self.assertIn("pending and healthy", text)
                self.assertIn("do not delete/recreate", text)

    def test_continuation_plan_matches_emitted_packet_schema(self) -> None:
        socket_root = ROOT.parents[1]
        plan = (socket_root / "docs/maintainers/deferred-work-wakeup-policy-plan.md").read_text(
            encoding="utf-8"
        )
        self.assertIn('"minimum_delay_minutes": 5', plan)
        self.assertIn('"pr_number": "123"', plan)
        self.assertNotIn('"not_before"', plan)
        self.assertNotIn('"observed_at"', plan)
        self.assertIn("Superseded by the live", plan)

        live_policy = (socket_root / "docs/maintainers/deferred-work-wakeup-policy.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Reuse that item unchanged", live_policy)
        self.assertIn("minimum delay is five minutes", live_policy)

    def test_branch_accounting_guidance_is_documented(self) -> None:
        skill_text = (ROOT / "skills/maintain-project-repo/SKILL.md").read_text(encoding="utf-8")
        release_modes = (ROOT / "skills/maintain-project-repo/references/release-modes.md").read_text(
            encoding="utf-8"
        )
        automation_prompts = (ROOT / "skills/maintain-project-repo/references/automation-prompts.md").read_text(
            encoding="utf-8"
        )

        for text in (skill_text, release_modes):
            with self.subTest(surface=text[:32]):
                self.assertIn("branch accounting", text)
                self.assertIn("git branch --no-merged <base>", text)
                self.assertIn("commit reachability", text)
                self.assertIn("temporary rescue refs", text)
                self.assertIn("explicit archive ref", text)

        self.assertIn("accounts for every local branch not contained by `main`", automation_prompts)
        self.assertIn("do not delete local branches, remote branches, worktrees, archive refs", automation_prompts)

    def test_release_and_publish_triggers_are_documented(self) -> None:
        skill_text = (ROOT / "skills/maintain-project-repo/SKILL.md").read_text(encoding="utf-8")
        trigger_reference = (ROOT / "skills/maintain-project-repo/references/trigger-eval.md").read_text(
            encoding="utf-8"
        )
        openai_yaml = (ROOT / "skills/maintain-project-repo/agents/openai.yaml").read_text(encoding="utf-8")

        self.assertIn("references/trigger-eval.md", skill_text)
        self.assertIn("maintain-github-repository", skill_text)

        for expected in (
            "release or publish a version",
            "bump and tag a release",
            "create the GitHub release",
            "protected-main release",
            "release cleanup and branch accounting",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, skill_text)

        for expected in (
            "Release version 1.4.0.",
            "Publish this package.",
            "Tag this commit and create the GitHub release.",
            "Prepare this branch for a protected-main release.",
            "Apply my normal GitHub repository settings.",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, trigger_reference)

        self.assertIn("protected-main release, publish, tag, GitHub release", openai_yaml)

    def test_prerelease_release_metadata_guidance_is_documented(self) -> None:
        skill_text = (ROOT / "skills/maintain-project-repo/SKILL.md").read_text(encoding="utf-8")
        release_modes = (ROOT / "skills/maintain-project-repo/references/release-modes.md").read_text(
            encoding="utf-8"
        )

        for text in (skill_text, release_modes):
            with self.subTest(surface=text[:32]):
                self.assertIn("SemVer prerelease", text)
                self.assertIn("--prerelease", text)
                self.assertIn("prerelease metadata", text)

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
            self.assertIn("Scripts/repo-maintenance/validate-all.sh", payload["managed_files"])
            joined = "\n".join(payload["actions"])
            self.assertIn("profile.env", joined)
            self.assertIn("xcode-app profile", joined)


if __name__ == "__main__":
    unittest.main()
