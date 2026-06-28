from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DesignAnimationSymbolWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_sf_symbols_workflow_covers_app_rendering_and_custom_symbols(self) -> None:
        skill_text = self.read("skills/sf-symbols-workflow/SKILL.md")
        selection_text = self.read("skills/sf-symbols-workflow/references/symbol-selection-and-rendering.md")
        app_text = self.read("skills/sf-symbols-workflow/references/custom-symbols-and-app-inspection.md")
        prompt_text = self.read("skills/sf-symbols-workflow/agents/openai.yaml")

        for term in [
            "Apply the Apple docs gate",
            "SF Symbols 7.2 build 119",
            "symbolRenderingMode",
            "variableValue",
            "symbolEffect",
            "custom symbol",
            "icon-composer-app-icon-workflow",
            "xcode-build-run-workflow",
            "references/snippets/apple-xcode-project-core.md",
        ]:
            self.assertIn(term, skill_text)

        for term in [
            "monochrome",
            "hierarchical",
            "palette",
            "multicolor",
            "variable value",
            "Do not use color alone",
        ]:
            self.assertIn(term, selection_text)

        for term in [
            "/Applications/SF Symbols.app",
            "Info, Format, and Animation",
            "Do not save, overwrite, export, or mutate user collections",
        ]:
            self.assertIn(term, app_text)

        self.assertIn("$sf-symbols-workflow", prompt_text)

    def test_swiftui_animation_workflow_covers_motion_and_accessibility_boundaries(self) -> None:
        skill_text = self.read("skills/swiftui-animation-workflow/SKILL.md")
        decision_text = self.read("skills/swiftui-animation-workflow/references/animation-decision-rules.md")
        accessibility_text = self.read(
            "skills/swiftui-animation-workflow/references/transitions-effects-and-accessibility.md"
        )
        prompt_text = self.read("skills/swiftui-animation-workflow/agents/openai.yaml")

        for term in [
            "Apply the Apple docs gate",
            "withAnimation",
            "animation(_:value:)",
            "PhaseAnimator",
            "KeyframeAnimator",
            "reduce-motion",
            "sf-symbols-workflow",
            "swiftui-app-architecture-workflow",
            "xcode-build-run-workflow",
            "references/snippets/apple-xcode-project-core.md",
        ]:
            self.assertIn(term, skill_text)

        for term in [
            "Use `withAnimation`",
            "Use `animation(_:value:)`",
            "Use `PhaseAnimator`",
            "Use `KeyframeAnimator`",
            "If too much animates",
        ]:
            self.assertIn(term, decision_text)

        for term in [
            "Use insertion/removal transitions",
            "Treat symbol effects as SwiftUI motion",
            "Respect reduce-motion expectations",
            "Screenshots cannot prove motion quality",
        ]:
            self.assertIn(term, accessibility_text)

        self.assertIn("$swiftui-animation-workflow", prompt_text)

    def test_design_animation_inventory_is_wired_into_metadata_and_validation(self) -> None:
        readme = self.read("README.md")
        roadmap = self.read("ROADMAP.md")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        plugin = self.read(".codex-plugin/plugin.json")

        for skill in ["sf-symbols-workflow", "swiftui-animation-workflow"]:
            with self.subTest(skill=skill):
                self.assertIn(f"`{skill}`", readme)
                self.assertIn(skill, roadmap)
                self.assertIn(f"./skills/{skill}/SKILL.md", validator)

        self.assertIn("SF Symbols", plugin)
        self.assertIn("SwiftUI animation", plugin)
        self.assertIn("sf-symbols", plugin)
        self.assertIn("animation", plugin)


if __name__ == "__main__":
    unittest.main()
