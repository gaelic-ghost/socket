from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class XcodeToolchainSelectionGuidanceTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_xcode_workflows_document_global_and_command_scoped_toolchain_selection(self) -> None:
        references = [
            "skills/xcode-build-run-workflow/references/toolchain-management.md",
            "skills/xcode-testing-workflow/references/toolchain-management.md",
            "skills/xcode-app-project-workflow/references/toolchain-management.md",
        ]

        for reference in references:
            with self.subTest(reference=reference):
                text = self.read(reference)

                self.assertIn("DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer", text)
                self.assertIn("DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer", text)
                self.assertIn("DEVELOPER_DIR=/Applications/Betas/Xcode-beta.app/Contents/Developer", text)
                self.assertIn("sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer", text)
                self.assertIn("sudo xcode-select --switch /Applications/Xcode-beta.app/Contents/Developer", text)
                self.assertIn("sudo xcode-select --switch /Applications/Betas/Xcode-beta.app/Contents/Developer", text)
                self.assertIn("record the current value first with `xcode-select -p`", text)
                self.assertIn("restore the previous path", text)
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


if __name__ == "__main__":
    unittest.main()
