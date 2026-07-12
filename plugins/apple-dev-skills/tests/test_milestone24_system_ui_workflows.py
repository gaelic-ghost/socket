from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Milestone24SystemUIWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_app_intents_workflow_preserves_narrow_domain_and_system_boundaries(self) -> None:
        skill = self.read("skills/app-intents-workflow/SKILL.md")
        references = self.read("skills/app-intents-workflow/references/intent-entity-and-shortcut-shapes.md")
        prompt = self.read("skills/app-intents-workflow/agents/openai.yaml")
        customization = self.read("skills/app-intents-workflow/scripts/customization_config.py")

        for term in ("AppIntent", "AppEntity", "AppShortcutsProvider", "Spotlight", "widgets", "controls", "Live Activities"):
            self.assertIn(term, skill + references)
        self.assertIn("do not invent a parallel intent-only repository", skill)
        self.assertIn("xcode-build-run-workflow", skill)
        self.assertIn("$app-intents-workflow", prompt)
        self.assertIn('SKILL_NAME = "app-intents-workflow"', customization)

    def test_liquid_glass_workflow_requires_native_composition_and_fallbacks(self) -> None:
        skill = self.read("skills/swiftui-liquid-glass/SKILL.md")
        references = self.read("skills/swiftui-liquid-glass/references/glass-composition-and-fallbacks.md")
        prompt = self.read("skills/swiftui-liquid-glass/agents/openai.yaml")
        customization = self.read("skills/swiftui-liquid-glass/scripts/customization_config.py")

        for term in ("glassEffect", "GlassEffectContainer", "glassEffectID", "interactive glass", "availability"):
            self.assertIn(term, skill + references)
        self.assertIn("Do not substitute custom blur stacks", skill)
        self.assertIn("oldest supported OS fallback", skill)
        self.assertIn("$swiftui-liquid-glass", prompt)
        self.assertIn('SKILL_NAME = "swiftui-liquid-glass"', customization)


if __name__ == "__main__":
    unittest.main()
