from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CoreAnimationTypographyWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_core_animation_workflow_covers_layer_boundaries_and_handoffs(self) -> None:
        skill_text = self.read("skills/core-animation-layer-workflow/SKILL.md")
        ownership_text = self.read(
            "skills/core-animation-layer-workflow/references/layer-ownership-and-animation-rules.md"
        )
        performance_text = self.read(
            "skills/core-animation-layer-workflow/references/model-presentation-and-performance.md"
        )
        prompt_text = self.read("skills/core-animation-layer-workflow/agents/openai.yaml")

        for term in [
            "Apply the Apple docs gate",
            "CALayer",
            "CAAnimation",
            "CATransaction",
            "presentationLayer",
            "swiftui-animation-workflow",
            "xcode-build-run-workflow",
            "references/snippets/apple-xcode-project-core.md",
        ]:
            self.assertIn(term, skill_text)

        for term in [
            "UIKit views own their backing layer",
            "Do not replace the layer delegate",
            "Update the model layer to the final value",
            "CAShapeLayer",
            "CAGradientLayer",
        ]:
            self.assertIn(term, ownership_text)

        for term in [
            "Treat the model layer as durable state",
            "Treat the presentation layer as an in-flight visual snapshot",
            "Screenshots can show final layout",
            "Hand off to `xcode-build-run-workflow`",
        ]:
            self.assertIn(term, performance_text)

        self.assertIn("$core-animation-layer-workflow", prompt_text)

    def test_apple_typography_workflow_covers_dynamic_type_and_font_boundaries(self) -> None:
        skill_text = self.read("skills/apple-typography-workflow/SKILL.md")
        system_text = self.read("skills/apple-typography-workflow/references/system-typography-and-dynamic-type.md")
        custom_text = self.read("skills/apple-typography-workflow/references/custom-fonts-and-licensing.md")
        prompt_text = self.read("skills/apple-typography-workflow/agents/openai.yaml")

        for term in [
            "Apply the Apple docs gate",
            "San Francisco",
            "New York",
            "Dynamic Type",
            "UIFontMetrics",
            "UIAppFonts",
            "ATSApplicationFontsPath",
            "xcode-build-run-workflow",
            "references/snippets/apple-xcode-project-core.md",
        ]:
            self.assertIn(term, skill_text)

        for term in [
            "Treat San Francisco as the system default family",
            "Use UIKit `UIFont.preferredFont(forTextStyle:)`",
            "Use `UIFontDescriptor.SystemDesign`",
            "Prefer semantic text styles",
        ]:
            self.assertIn(term, system_text)

        for term in [
            "Confirm the font license allows app embedding",
            "Do not extract or bundle Apple system font files",
            "state the licensing or redistribution concern once",
        ]:
            self.assertIn(term, custom_text)

        self.assertIn("$apple-typography-workflow", prompt_text)

    def test_second_slice_inventory_is_wired_into_metadata_and_validation(self) -> None:
        readme = self.read("README.md")
        roadmap = self.read("ROADMAP.md")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        plugin = self.read(".codex-plugin/plugin.json")

        for skill in ["core-animation-layer-workflow", "apple-typography-workflow"]:
            with self.subTest(skill=skill):
                self.assertIn(f"`{skill}`", readme)
                self.assertIn(skill, roadmap)
                self.assertIn(f"./skills/{skill}/SKILL.md", validator)

        self.assertIn("Core Animation", plugin)
        self.assertIn("Apple typography", plugin)
        self.assertIn("core-animation", plugin)
        self.assertIn("typography", plugin)


if __name__ == "__main__":
    unittest.main()
