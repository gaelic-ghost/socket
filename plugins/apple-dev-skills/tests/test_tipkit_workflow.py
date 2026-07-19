from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TipKitWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_owns_tipkit_setup_and_presentations(self) -> None:
        skill = self.read("skills/tipkit-workflow/SKILL.md")
        presentation = self.read("skills/tipkit-workflow/references/presentation-and-platform-patterns.md")

        for term in ("Tips.configure", "TipView", "popoverTip", "TipUIView", "TipUIPopoverViewController", "TipNSView", "TipNSPopover"):
            self.assertIn(term, skill + presentation)
        self.assertIn("Prefer an inline tip whenever practical", presentation)
        self.assertIn("attach `popoverTip` to the exact feature", presentation)

    def test_skill_covers_eligibility_lifecycle_testing_and_diagnosis(self) -> None:
        skill = self.read("skills/tipkit-workflow/SKILL.md")
        lifecycle = self.read("skills/tipkit-workflow/references/eligibility-lifecycle-and-testing.md")

        for term in ("@Parameter", "Tips.Event", "#Rule", "donate()", "sendDonation", "invalidate(reason:)", "showAllTipsForTesting", "hideAllTipsForTesting", "resetDatastore"):
            self.assertIn(term, skill + lifecycle)
        self.assertIn("Multiple entries in `rules` combine with logical AND", lifecycle)
        self.assertIn("Call `Tips.resetDatastore()` before `Tips.configure()`", lifecycle)
        self.assertIn("Never leave unconditional datastore resets", lifecycle)

    def test_skill_requires_docs_and_explicit_handoffs(self) -> None:
        skill = self.read("skills/tipkit-workflow/SKILL.md")
        prompt = self.read("skills/tipkit-workflow/agents/openai.yaml")
        customization = self.read("skills/tipkit-workflow/scripts/customization_config.py")

        self.assertIn("Apply the Apple docs gate", skill)
        self.assertIn("State the documented TipKit behavior", skill)
        self.assertIn("Recommend `explore-apple-swift-docs`", skill)
        self.assertIn("Recommend `xcode-build-run-workflow`", skill)
        self.assertIn("Recommend `xcode-testing-workflow`", skill)
        self.assertIn("$tipkit-workflow", prompt)
        self.assertIn('SKILL_NAME = "tipkit-workflow"', customization)

    def test_inventory_and_metadata_include_tipkit(self) -> None:
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        roadmap = self.read("ROADMAP.md")

        self.assertIn("tipkit-workflow", readme)
        self.assertIn("TipKit", plugin)
        self.assertIn("./skills/tipkit-workflow/SKILL.md", validator)
        self.assertIn("Expected exactly 59 active skills", validator)
        self.assertIn("Milestone 55: TipKit Workflow", roadmap)


if __name__ == "__main__":
    unittest.main()
