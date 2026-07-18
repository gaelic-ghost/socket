from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AppExtensionWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_architecture_skill_keeps_process_and_product_boundaries_explicit(self) -> None:
        skill = self.read("skills/app-extension-architecture-workflow/SKILL.md")

        self.assertIn("separate process", skill)
        self.assertIn("App Group", skill)
        self.assertIn("MailKit", skill)
        self.assertIn("File Provider", skill)
        self.assertIn("Messages/iMessage collaboration", skill)
        self.assertIn("Do not add a generic coordinator", skill)
        self.assertIn("xcode-build-run-workflow", skill)
        self.assertIn("xcode-testing-workflow", skill)

    def test_mailkit_skill_covers_each_handler_and_private_mail_boundary(self) -> None:
        skill = self.read("skills/mailkit-workflow/SKILL.md")
        reference = self.read("skills/mailkit-workflow/references/mailkit-capabilities-and-handler-boundaries.md")

        for handler in (
            "MEContentBlocker",
            "MEMessageActionHandler",
            "MEComposeSessionHandler",
            "MEMessageSecurityHandler",
        ):
            self.assertIn(handler, skill)
            self.assertIn(handler, reference)
        self.assertIn("Do not retain or log raw message data", skill)
        self.assertIn("enabled extensions", reference)

    def test_file_provider_and_finder_sync_have_non_overlapping_ownership(self) -> None:
        skill = self.read("skills/file-provider-and-finder-sync-workflow/SKILL.md")
        finder = self.read("skills/file-provider-and-finder-sync-workflow/references/finder-sync-boundaries.md")

        self.assertIn("File Provider for remote storage synchronization", skill)
        self.assertIn("Finder Sync only", skill)
        self.assertIn("Do not recommend Finder Sync as the implementation of remote storage synchronization", skill)
        self.assertIn("does not provide a remote storage domain", finder)
        self.assertIn("FIFinderSyncController", finder)

    def test_inventory_and_metadata_include_the_new_skills(self) -> None:
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        readme = self.read("README.md")
        manifest = self.read(".codex-plugin/plugin.json")

        for skill in (
            "app-extension-architecture-workflow",
            "mailkit-workflow",
            "file-provider-and-finder-sync-workflow",
        ):
            self.assertIn(f"./skills/{skill}/SKILL.md", validator)
            self.assertIn(f"`{skill}`", readme)
        self.assertIn("mailkit", manifest)
        self.assertIn("file-provider", manifest)
        self.assertIn("Expected exactly 54 active skills", validator)


if __name__ == "__main__":
    unittest.main()
