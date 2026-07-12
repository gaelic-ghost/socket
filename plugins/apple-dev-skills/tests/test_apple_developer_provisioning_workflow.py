from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AppleDeveloperProvisioningWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_distinguishes_supported_and_portal_only_operations(self) -> None:
        skill = self.read("skills/apple-developer-provisioning-workflow/SKILL.md")
        portal = self.read("skills/apple-developer-provisioning-workflow/references/portal-only-configuration.md")

        self.assertIn("registered bundle IDs, supported capabilities, certificates, devices, and provisioning profiles", skill)
        self.assertIn("App Group registration or assignment", skill)
        self.assertIn("CloudKit container registration or assignment", skill)
        self.assertIn("Service ID registration", skill)
        self.assertIn("not an invitation to reverse engineer the website", portal)

    def test_skill_requires_safe_credentials_planning_and_confirmation(self) -> None:
        skill = self.read("skills/apple-developer-provisioning-workflow/SKILL.md")
        provisioning = self.read("skills/apple-developer-provisioning-workflow/references/app-store-connect-provisioning.md")

        self.assertIn("individual API keys cannot use provisioning endpoints", skill)
        self.assertIn("Enterprise Program accounts use Apple’s separate Enterprise Program API", skill)
        self.assertIn("short-lived JWT", skill)
        self.assertIn("requires an explicit confirmation immediately before every", skill)
        self.assertIn("never place them in the repo", skill)
        self.assertIn("team API key", provisioning)
        self.assertIn("team API keys are unavailable in that program", provisioning)

    def test_cloudkit_paths_remain_local_and_token_safe(self) -> None:
        skill = self.read("skills/apple-developer-provisioning-workflow/SKILL.md")
        cloudkit = self.read("skills/apple-developer-provisioning-workflow/references/cloudkit-automation.md")

        self.assertIn("xcrun cktool save-token --type management", skill)
        self.assertIn("@apple/cktool.database", skill)
        self.assertIn("@apple/cktool.target.nodejs", cloudkit)
        self.assertIn("pnpm add", cloudkit)
        self.assertIn("never put the token in source", cloudkit)

    def test_inventory_metadata_and_roadmap_are_updated(self) -> None:
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        roadmap = self.read("ROADMAP.md")

        self.assertIn("apple-developer-provisioning-workflow", readme)
        self.assertIn("Apple Developer provisioning", plugin)
        self.assertIn("./skills/apple-developer-provisioning-workflow/SKILL.md", validator)
        self.assertIn("Expected exactly 38 active skills", validator)
        self.assertIn("Milestone 54: Apple Developer Provisioning and CloudKit Workflow - Completed", roadmap)

    def test_customization_cli_preserves_shared_apply_and_reset_verbs(self) -> None:
        script = ROOT / "skills/apple-developer-provisioning-workflow/scripts/customization_config.py"
        with tempfile.TemporaryDirectory() as tmpdir:
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            env["UV_CACHE_DIR"] = str(Path(tempfile.gettempdir()) / "apple-dev-skills-uv-cache")
            override = Path(tmpdir) / "override.yaml"
            override.write_text(
                "schemaVersion: 1\nisCustomized: true\nsettings:\n  preferredDiscoveryMode: rest-first\n",
                encoding="utf-8",
            )

            apply = subprocess.run([str(script), "apply", "--input", str(override)], env=env, capture_output=True, text=True)
            self.assertEqual(apply.returncode, 0, apply.stderr)
            expected = Path(tmpdir) / "apple-developer-provisioning-workflow/customization.yaml"
            self.assertEqual(Path(apply.stdout.strip()), expected)
            self.assertTrue(expected.is_file())

            effective = subprocess.run([str(script), "effective"], env=env, capture_output=True, text=True)
            self.assertEqual(effective.returncode, 0, effective.stderr)
            self.assertIn("preferredDiscoveryMode: rest-first", effective.stdout)

            reset = subprocess.run([str(script), "reset"], env=env, capture_output=True, text=True)
            self.assertEqual(reset.returncode, 0, reset.stderr)
            self.assertEqual(Path(reset.stdout.strip()), expected)
            self.assertFalse(expected.exists())


if __name__ == "__main__":
    unittest.main()
