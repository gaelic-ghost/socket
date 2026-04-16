from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SwiftUIAppArchitectureWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_keeps_focus_as_first_class_architecture_surface(self) -> None:
        skill_text = self.read("skills/swiftui-app-architecture-workflow/SKILL.md")
        focus_text = self.read("skills/swiftui-app-architecture-workflow/references/focus-and-focused-context.md")

        self.assertIn("focus and focused context", skill_text)
        self.assertIn("focused object", skill_text)
        self.assertIn("FocusState", focus_text)
        self.assertIn("focusedSceneObject", focus_text)
        self.assertIn("focusScope", focus_text)

    def test_skill_handoffs_stay_explicit(self) -> None:
        skill_text = self.read("skills/swiftui-app-architecture-workflow/SKILL.md")
        prompt_text = self.read("skills/swiftui-app-architecture-workflow/agents/openai.yaml")

        self.assertIn("Recommend `explore-apple-swift-docs`", skill_text)
        self.assertIn("Recommend `xcode-build-run-workflow`", skill_text)
        self.assertIn("Recommend `xcode-testing-workflow`", skill_text)
        self.assertIn("$explore-apple-swift-docs", prompt_text)
        self.assertIn("$xcode-build-run-workflow", prompt_text)
        self.assertIn("$xcode-testing-workflow", prompt_text)


if __name__ == "__main__":
    unittest.main()
