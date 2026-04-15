from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SwiftCleanupSkillBoundaryTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_structure_skill_hands_docc_work_to_dedicated_skill(self) -> None:
        skill_text = self.read("skills/structure-swift-sources/SKILL.md")
        prompt_text = self.read("skills/structure-swift-sources/agents/openai.yaml")
        rules_text = self.read("skills/structure-swift-sources/references/source-organization-rules.md")

        self.assertIn("not the DocC authoring authority", skill_text)
        self.assertIn("author-swift-docc-docs", skill_text)
        self.assertNotIn("DocC coverage pass", skill_text)
        self.assertNotIn("DocC-compliant documentation comments", skill_text)
        self.assertIn("hand off to $author-swift-docc-docs", prompt_text)
        self.assertIn("Documentation Boundary", rules_text)
        self.assertNotIn("## DocC Rule", rules_text)

    def test_format_skill_routes_docc_work_to_dedicated_skill(self) -> None:
        skill_text = self.read("skills/format-swift-sources/SKILL.md")

        self.assertIn("Recommend `author-swift-docc-docs`", skill_text)
        self.assertNotIn("DocC coverage", skill_text)


if __name__ == "__main__":
    unittest.main()
