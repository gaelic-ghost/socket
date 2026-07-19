from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SafariMCPWorkflowTests(unittest.TestCase):
    def text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_skill_owns_runtime_validation_not_extension_architecture(self) -> None:
        skill = self.text("skills/safari-mcp-workflow/SKILL.md")
        self.assertIn("Safari Technology Preview", skill)
        self.assertIn("safari-extension-control-workflow", skill)
        self.assertIn("not Safari extension architecture", skill)
        self.assertIn("Safari-specific claims only", skill)

    def test_skill_requires_scoped_authorized_evidence(self) -> None:
        skill = self.text("skills/safari-mcp-workflow/SKILL.md")
        reference = self.text("skills/safari-mcp-workflow/references/evidence-and-validation.md")
        self.assertIn("Do not inspect unrelated tabs", skill)
        self.assertIn("fresh user confirmation", skill)
        self.assertIn("screenshot alone", skill)
        self.assertIn("get_page_content", skill)
        self.assertIn("page_interactions", skill)
        self.assertIn("observed facts from inference", reference)

    def test_setup_reference_keeps_registration_and_data_boundaries_explicit(self) -> None:
        setup = self.text("skills/safari-mcp-workflow/references/setup-and-privacy.md")
        prompt = self.text("skills/safari-mcp-workflow/agents/openai.yaml")
        customization = self.text("skills/safari-mcp-workflow/scripts/customization_config.py")
        self.assertIn("codex mcp add safari-mcp-stp", setup)
        self.assertIn("explicit approval", setup)
        self.assertIn("Allow remote automation", setup)
        self.assertIn("uid", setup)
        self.assertIn("expression", setup)
        self.assertIn("close_tab", setup)
        self.assertIn("AutoFill", setup)
        self.assertIn("$safari-mcp-workflow", prompt)
        self.assertIn('SKILL_NAME = "safari-mcp-workflow"', customization)


if __name__ == "__main__":
    unittest.main()
