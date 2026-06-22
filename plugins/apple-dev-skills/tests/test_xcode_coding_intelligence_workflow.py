from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class XcodeCodingIntelligenceWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_owns_setup_not_execution(self) -> None:
        skill_text = self.read("skills/xcode-coding-intelligence-workflow/SKILL.md")
        prompt_text = self.read("skills/xcode-coding-intelligence-workflow/agents/openai.yaml")

        self.assertIn("Xcode Intelligence setup", skill_text)
        self.assertIn("xcrun mcpbridge", skill_text)
        self.assertIn("command and tool permissions", skill_text)
        self.assertIn("Recommend `xcode-build-run-workflow`", skill_text)
        self.assertIn("Recommend `xcode-testing-workflow`", skill_text)
        self.assertIn("$xcode-build-run-workflow", prompt_text)
        self.assertIn("$xcode-testing-workflow", prompt_text)

    def test_beta_claims_are_dated_and_bounded(self) -> None:
        skill_text = self.read("skills/xcode-coding-intelligence-workflow/SKILL.md")
        evidence_text = self.read("skills/xcode-coding-intelligence-workflow/references/source-evidence.md")

        self.assertIn("checked against Apple developer pages and WWDC26 transcripts on 2026-06-22", skill_text)
        self.assertIn("Do not claim Xcode 27 beta behavior is stable Xcode behavior.", skill_text)
        self.assertIn("Observed local Xcode version: Xcode 26.5, build 17F42.", evidence_text)
        self.assertIn("Xcode 27 beta behavior on Gale's machine", evidence_text)

    def test_external_agent_reference_documents_mcpbridge_preconditions(self) -> None:
        bridge_text = self.read("skills/xcode-coding-intelligence-workflow/references/mcpbridge-and-external-agents.md")

        self.assertIn("codex mcp add xcode -- xcrun mcpbridge", bridge_text)
        self.assertIn("MCP_XCODE_PID", bridge_text)
        self.assertIn("xcrun mcpbridge run-agent --dry-run <agent-name>", bridge_text)
        self.assertIn("External-agent access must be enabled", bridge_text)
        self.assertIn("The relevant project or workspace should be open in Xcode", bridge_text)

    def test_agent_surface_reference_keeps_acp_and_plugins_research_first(self) -> None:
        setup_text = self.read("skills/xcode-coding-intelligence-workflow/references/setup-and-agent-surfaces.md")
        evidence_text = self.read("skills/xcode-coding-intelligence-workflow/references/source-evidence.md")

        self.assertIn("xcode-hosted", setup_text)
        self.assertIn("external-mcp", setup_text)
        self.assertIn("plugin", setup_text)
        self.assertIn("acp", setup_text)
        self.assertIn("Do not claim Apple-documented ACP setup", setup_text)
        self.assertIn("Xcode plug-in package shape: keep blocked", evidence_text)

    def test_permissions_reference_requires_reviewable_artifacts(self) -> None:
        permissions_text = self.read("skills/xcode-coding-intelligence-workflow/references/permissions-and-artifacts.md")

        self.assertIn("Do not grant broader permissions to work around unclear setup.", permissions_text)
        self.assertIn("Plan-First Bias", permissions_text)
        self.assertIn("Reviewable Artifacts", permissions_text)
        self.assertIn("Do not store provider API keys", permissions_text)


if __name__ == "__main__":
    unittest.main()
