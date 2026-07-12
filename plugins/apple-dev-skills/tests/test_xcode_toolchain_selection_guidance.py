from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class XcodeToolchainSelectionGuidanceTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_xcode_workflows_require_xcode_select_and_permission_for_exceptions(self) -> None:
        references = [
            "skills/xcode-build-run-workflow/references/toolchain-management.md",
            "skills/xcode-testing-workflow/references/toolchain-management.md",
            "skills/xcode-app-project-workflow/references/toolchain-management.md",
        ]

        for reference in references:
            with self.subTest(reference=reference):
                text = self.read(reference)

                self.assertIn("currently selected by `xcode-select`", text)
                self.assertIn("Do not override it per command", text)
                self.assertIn("Never set `DEVELOPER_DIR` by default", text)
                self.assertIn("obtain Gale's explicit permission", text)
                self.assertNotIn("DEVELOPER_DIR=", text)
                self.assertIn("sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer", text)
                self.assertIn("sudo xcode-select --switch /Applications/Xcode-beta.app/Contents/Developer", text)
                self.assertIn("sudo xcode-select --switch /Applications/Betas/Xcode-beta.app/Contents/Developer", text)
                self.assertIn("record the current value first with `xcode-select -p`", text)
                self.assertIn("restore a previous path only when the user asked for a temporary switch", text)
                self.assertIn("Do not use `xcode-select --install` as an Xcode app switch", text)

    def test_icon_composer_checks_system_wide_beta_paths(self) -> None:
        text = self.read("skills/icon-composer-app-icon-workflow/SKILL.md")

        self.assertIn("/Applications/Xcode-beta.app/Contents/Applications/Icon Composer.app", text)
        self.assertIn("/Applications/Betas/Xcode-beta.app/Contents/Applications/Icon Composer.app", text)
        self.assertIn("/Applications/Xcode-beta.app/Contents/Applications/Icon Composer.app/Contents/Executables/ictool", text)
        self.assertIn(
            "/Applications/Betas/Xcode-beta.app/Contents/Applications/Icon Composer.app/Contents/Executables/ictool",
            text,
        )
        self.assertNotIn("/Users/galew/Applications/Betas", text)

    def test_icon_composer_documents_stable_1_6_and_beta_2_0_boundaries(self) -> None:
        text = self.read("skills/icon-composer-app-icon-workflow/SKILL.md")

        for term in [
            "Icon Composer 1.6",
            "bundle-version` `99.1",
            "Icon Composer 2.0",
            "Do not mix stable and beta behavior",
            "--light-angle",
            "--tint-color",
            "--tint-strength",
            "--design-generation",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
