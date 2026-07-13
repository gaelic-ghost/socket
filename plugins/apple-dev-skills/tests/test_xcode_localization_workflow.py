from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class XcodeLocalizationWorkflowTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_catalog_first_workflow_covers_source_translation_and_validation(self) -> None:
        skill = self.read("skills/xcode-localization-workflow/SKILL.md")
        foundations = self.read("skills/xcode-localization-workflow/references/string-catalog-foundations.md")
        source = self.read("skills/xcode-localization-workflow/references/source-apis-and-translator-context.md")
        validation = self.read("skills/xcode-localization-workflow/references/translation-review-and-validation.md")

        for term in (
            "String Catalogs (`.xcstrings`)",
            "String(localized:table:bundle:locale:comment:)",
            "LocalizedStringResource",
            "Vary by Plural",
            "XLIFF",
            "right-to-left",
            "human-review",
        ):
            self.assertIn(term, skill + foundations + source + validation)

        self.assertIn("xcode-build-run-workflow", skill)
        self.assertIn("xcode-testing-workflow", skill)
        self.assertIn("xcode-device-hub-workflow", skill)
        self.assertIn("apple-ui-accessibility-workflow", skill)
        self.assertIn("xcode-coding-intelligence-workflow", skill)

    def test_agent_translation_is_optional_and_beta_scoped(self) -> None:
        skill = self.read("skills/xcode-localization-workflow/SKILL.md")
        agent = self.read("skills/xcode-localization-workflow/references/agent-assisted-translation.md")

        self.assertIn("optional beta-era acceleration", skill)
        self.assertIn("Do not present agent output as human-reviewed translation.", skill)
        self.assertIn("optional beta-era workflow", agent)
        self.assertIn("machine-translation provenance", agent)

    def test_inventory_metadata_and_roadmap_name_the_shipped_skill(self) -> None:
        readme = self.read("README.md")
        manifest = self.read(".codex-plugin/plugin.json")
        roadmap = self.read("ROADMAP.md")
        validator = self.read(".github/scripts/validate_repo_docs.sh")

        for text in (readme, roadmap, validator):
            self.assertIn("xcode-localization-workflow", text)
        self.assertIn("String Catalog localization", manifest)
        self.assertIn('"string-catalog"', manifest)
        self.assertIn("Expected exactly 50 active skills", validator)


if __name__ == "__main__":
    unittest.main()
