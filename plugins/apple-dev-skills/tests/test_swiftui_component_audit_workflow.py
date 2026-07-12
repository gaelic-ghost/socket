from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SwiftUIComponentAuditWorkflowTests(unittest.TestCase):
    def test_audit_requires_declarative_component_boundaries(self) -> None:
        skill_text = (ROOT / "skills/swiftui-component-audit-workflow/SKILL.md").read_text(encoding="utf-8")
        examples_text = (
            ROOT / "skills/swiftui-component-audit-workflow/references/component-rules-and-examples.md"
        ).read_text(encoding="utf-8")

        self.assertIn("external ViewModels", skill_text)
        self.assertIn("memberwise initializer", skill_text)
        self.assertIn("custom environment value or action", skill_text)
        self.assertIn("preference keys", skill_text)
        self.assertIn("@Query", skill_text)
        self.assertIn("GEAItemRowViewModel", examples_text)
        self.assertIn("onToggle", examples_text)


if __name__ == "__main__":
    unittest.main()
