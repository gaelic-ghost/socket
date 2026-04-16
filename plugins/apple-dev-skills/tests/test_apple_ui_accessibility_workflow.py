from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AppleUIAccessibilityWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_keeps_swiftui_first_but_framework_broad(self) -> None:
        skill_text = self.read("skills/apple-ui-accessibility-workflow/SKILL.md")
        bridge_text = self.read("skills/apple-ui-accessibility-workflow/references/framework-bridging-uikit-appkit.md")
        examples_text = self.read("skills/apple-ui-accessibility-workflow/references/worked-swiftui-accessibility-examples.md")

        self.assertIn("SwiftUI-first", skill_text)
        self.assertIn("UIKit", skill_text)
        self.assertIn("AppKit", skill_text)
        self.assertIn("UIViewRepresentable", bridge_text)
        self.assertIn("NSViewRepresentable", bridge_text)
        self.assertIn("StepsBars", examples_text)
        self.assertIn("RingView", examples_text)

    def test_skill_handoffs_stay_explicit(self) -> None:
        skill_text = self.read("skills/apple-ui-accessibility-workflow/SKILL.md")
        prompt_text = self.read("skills/apple-ui-accessibility-workflow/agents/openai.yaml")

        self.assertIn("Recommend `explore-apple-swift-docs`", skill_text)
        self.assertIn("Recommend `xcode-testing-workflow`", skill_text)
        self.assertIn("Recommend `swiftui-app-architecture-workflow`", skill_text)
        self.assertIn("$explore-apple-swift-docs", prompt_text)
        self.assertIn("$xcode-testing-workflow", prompt_text)
        self.assertIn("$swiftui-app-architecture-workflow", prompt_text)

    def test_verification_reference_draws_the_boundary_clearly(self) -> None:
        verification_text = self.read("skills/apple-ui-accessibility-workflow/references/verification-expectations.md")

        self.assertIn("VoiceOver", verification_text)
        self.assertIn("Dynamic Type", verification_text)
        self.assertIn("reduced motion", verification_text)
        self.assertIn("xcode-testing-workflow", verification_text)

    def test_semantics_and_tree_shaping_references_include_worked_examples(self) -> None:
        semantics_text = self.read("skills/apple-ui-accessibility-workflow/references/swiftui-accessibility-semantics.md")
        tree_text = self.read("skills/apple-ui-accessibility-workflow/references/swiftui-accessibility-tree-shaping.md")

        self.assertIn("FavoriteButton", semantics_text)
        self.assertIn("accessibilityValue", semantics_text)
        self.assertIn("SettingsCard", tree_text)
        self.assertIn("accessibilityElement(children: .combine)", tree_text)


if __name__ == "__main__":
    unittest.main()
