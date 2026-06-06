from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AppKitAppArchitectureWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_keeps_menu_bar_and_status_item_first_class(self) -> None:
        skill_text = self.read("skills/appkit-app-architecture-workflow/SKILL.md")
        status_text = self.read(
            "skills/appkit-app-architecture-workflow/references/menu-bar-status-item-and-activation.md"
        )

        self.assertIn("NSStatusItem", skill_text)
        self.assertIn("menu bar", skill_text)
        self.assertIn("activation policy", status_text)
        self.assertIn("SwiftUI `MenuBarExtra`", status_text)

    def test_skill_covers_restoration_archiving_and_observation(self) -> None:
        restoration_text = self.read(
            "skills/appkit-app-architecture-workflow/references/restoration-documents-and-workspaces.md"
        )
        archiving_text = self.read(
            "skills/appkit-app-architecture-workflow/references/archiving-persistence-and-migration.md"
        )
        observation_text = self.read(
            "skills/appkit-app-architecture-workflow/references/observation-and-appkit.md"
        )

        self.assertIn("NSWindowRestoration", restoration_text)
        self.assertIn("restoration identifiers", restoration_text)
        self.assertIn("NSSecureCoding", archiving_text)
        self.assertIn("NSKeyedArchiver", archiving_text)
        self.assertIn("@Observable", observation_text)
        self.assertIn("Do not assume AppKit controls automatically re-render", observation_text)

    def test_skill_handoffs_stay_explicit(self) -> None:
        skill_text = self.read("skills/appkit-app-architecture-workflow/SKILL.md")
        prompt_text = self.read("skills/appkit-app-architecture-workflow/agents/openai.yaml")

        self.assertIn("Recommend `swiftui-app-architecture-workflow`", skill_text)
        self.assertIn("Recommend `explore-apple-swift-docs`", skill_text)
        self.assertIn("Recommend `apple-ui-accessibility-workflow`", skill_text)
        self.assertIn("Recommend `xcode-build-run-workflow`", skill_text)
        self.assertIn("Recommend `xcode-testing-workflow`", skill_text)
        self.assertIn("$swiftui-app-architecture-workflow", prompt_text)
        self.assertIn("$explore-apple-swift-docs", prompt_text)
        self.assertIn("$xcode-build-run-workflow", prompt_text)
        self.assertIn("$xcode-testing-workflow", prompt_text)

    def test_mixed_appkit_swiftui_reference_names_single_owner(self) -> None:
        mixed_text = self.read(
            "skills/appkit-app-architecture-workflow/references/mixed-appkit-swiftui-composition.md"
        )
        anti_patterns_text = self.read(
            "skills/appkit-app-architecture-workflow/references/anti-patterns-and-corrections.md"
        )

        self.assertIn("Name the owner first", mixed_text)
        self.assertIn("NSHostingController", mixed_text)
        self.assertIn("NSHostingView", mixed_text)
        self.assertIn("Split Ownership Across Frameworks", anti_patterns_text)


if __name__ == "__main__":
    unittest.main()
