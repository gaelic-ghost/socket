from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SafariExtensionControlWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_separates_safari_extension_shapes(self) -> None:
        skill_text = self.read("skills/safari-extension-control-workflow/SKILL.md")
        decision_text = self.read("skills/safari-extension-control-workflow/references/extension-shape-decision.md")

        self.assertIn("Safari Web Extension", skill_text)
        self.assertIn("Safari Web Inspector Extension", skill_text)
        self.assertIn("Safari App Extension", skill_text)
        self.assertIn("Content blocker", skill_text)
        self.assertIn("ASWebAuthenticationSession", decision_text)
        self.assertIn("Safari App Extensions are macOS-only", decision_text)
        self.assertIn(".safariextz", decision_text)
        self.assertIn("no JavaScript execution path", decision_text)

    def test_web_inspector_extension_path_is_first_class(self) -> None:
        skill_text = self.read("skills/safari-extension-control-workflow/SKILL.md")
        inspector_text = self.read("skills/safari-extension-control-workflow/references/web-inspector-extensions.md")
        prompt_text = self.read("skills/safari-extension-control-workflow/agents/openai.yaml")

        self.assertIn("web-inspector-extensions.md", skill_text)
        self.assertIn("developer tools", inspector_text)
        self.assertIn("Safari Web Inspector", inspector_text)
        self.assertIn("inspected-page", inspector_text)
        self.assertIn("Safari Web Inspector Extensions", prompt_text)

    def test_skill_keeps_control_surfaces_bounded(self) -> None:
        skill_text = self.read("skills/safari-extension-control-workflow/SKILL.md")
        control_text = self.read("skills/safari-extension-control-workflow/references/safari-services-control-surfaces.md")

        self.assertIn("Do not claim a Mac app can freely inspect or control arbitrary Safari", skill_text)
        self.assertIn("SFSafariApplication.openWindow", control_text)
        self.assertIn("SFSafariExtensionManager", control_text)
        self.assertIn("external automation", control_text)

    def test_messaging_reference_names_contexts_and_privacy(self) -> None:
        messaging_text = self.read("skills/safari-extension-control-workflow/references/messaging-shared-data-and-permissions.md")

        self.assertIn("containing macOS app", messaging_text)
        self.assertIn("native app extension", messaging_text)
        self.assertIn("WebExtension JavaScript", messaging_text)
        self.assertIn("app groups", messaging_text)
        self.assertIn("browsing history, cookies, tokens", messaging_text)

    def test_skill_handoffs_stay_explicit(self) -> None:
        skill_text = self.read("skills/safari-extension-control-workflow/SKILL.md")
        prompt_text = self.read("skills/safari-extension-control-workflow/agents/openai.yaml")

        self.assertIn("Recommend `explore-apple-swift-docs`", skill_text)
        self.assertIn("Recommend `xcode-build-run-workflow`", skill_text)
        self.assertIn("Recommend `xcode-testing-workflow`", skill_text)
        self.assertIn("Recommend `swiftui-app-architecture-workflow`", skill_text)
        self.assertIn("$explore-apple-swift-docs", prompt_text)
        self.assertIn("$xcode-build-run-workflow", prompt_text)
        self.assertIn("$xcode-testing-workflow", prompt_text)
        self.assertIn("$swiftui-app-architecture-workflow", prompt_text)


if __name__ == "__main__":
    unittest.main()
