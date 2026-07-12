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
        self.assertIn("Xcode plug-in import inspection", skill_text)
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
        self.assertIn("Observed beta Xcode version: Xcode 27.0, build 27A5194q.", evidence_text)
        self.assertIn("Earlier default-developer-dir check observed Xcode 26.5, build 17F42.", evidence_text)
        self.assertIn("Local Xcode 27 Beta Plug-in Import Probe", evidence_text)

    def test_beta_path_guidance_uses_system_wide_app_locations(self) -> None:
        skill_text = self.read("skills/xcode-coding-intelligence-workflow/SKILL.md")
        bridge_text = self.read("skills/xcode-coding-intelligence-workflow/references/mcpbridge-and-external-agents.md")
        setup_text = self.read("skills/xcode-coding-intelligence-workflow/references/setup-and-agent-surfaces.md")
        evidence_text = self.read("skills/xcode-coding-intelligence-workflow/references/source-evidence.md")

        for text in (bridge_text, setup_text):
            self.assertIn("do not override it with `DEVELOPER_DIR`", text)
            self.assertNotIn("/Users/galew/Applications/Betas", text)

        self.assertIn("use the Xcode CLI toolchain Gale selected through `xcode-select`", skill_text)
        self.assertIn("Do not set `DEVELOPER_DIR` unless", skill_text)

        self.assertIn("Current path note", evidence_text)
        self.assertIn("Observed beta Xcode version: Xcode 27.0, build 27A5209h.", evidence_text)
        self.assertIn("historical evidence, not current guidance", evidence_text)
        self.assertIn("Historical evidence only", evidence_text)

    def test_external_agent_reference_documents_mcpbridge_preconditions(self) -> None:
        bridge_text = self.read("skills/xcode-coding-intelligence-workflow/references/mcpbridge-and-external-agents.md")

        self.assertIn("codex mcp add xcode -- xcrun mcpbridge", bridge_text)
        self.assertIn("MCP_XCODE_PID", bridge_text)
        self.assertIn("xcrun mcpbridge run-agent --dry-run <agent-name>", bridge_text)
        self.assertIn("Plug-in Import Is Not A Bridge Subcommand", bridge_text)
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
        self.assertIn("Add from URL", evidence_text)

    def test_permissions_reference_requires_reviewable_artifacts(self) -> None:
        permissions_text = self.read("skills/xcode-coding-intelligence-workflow/references/permissions-and-artifacts.md")

        self.assertIn("Do not grant broader permissions to work around unclear setup.", permissions_text)
        self.assertIn("Plan-First Bias", permissions_text)
        self.assertIn("Reviewable Artifacts", permissions_text)
        self.assertIn("Do not store provider API keys", permissions_text)


if __name__ == "__main__":
    unittest.main()
