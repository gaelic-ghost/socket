from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TVOSWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_app_experience_workflow_owns_focus_without_overclaiming_ai(self) -> None:
        skill = self.read("skills/tvos-app-experience-workflow/SKILL.md")
        platform = self.read("skills/tvos-app-experience-workflow/references/platform-beta-and-migration.md")

        for term in (
            "SwiftUI is the primary implementation path",
            "directional focus remains under user control",
            "UIFocusGuide",
            "TVMLKit has been deprecated since tvOS 18",
            "Do not claim direct Core AI",
            "model-lab-skills:choose-apple-model-runtime",
            "xcode-testing-workflow",
        ):
            with self.subTest(term=term):
                self.assertIn(term, skill)
        self.assertIn("do not name tvOS as a direct app runtime target", platform)

    def test_app_experience_references_cover_remote_large_text_and_device_evidence(self) -> None:
        focus = self.read("skills/tvos-app-experience-workflow/references/focus-layout-and-input.md")
        validation = self.read("skills/tvos-app-experience-workflow/references/validation-expectations.md")

        for term in ("Siri Remote", "focusSection()", "Large Text", "Preserve `Menu`/Back"):
            self.assertIn(term, focus)
        for term in ("VoiceOver", "Apple TV model", "real Apple TV", "xcode-testing-workflow"):
            self.assertIn(term, validation)

    def test_media_workflow_keeps_system_player_and_command_matrix_explicit(self) -> None:
        skill = self.read("skills/tvos-media-playback-workflow/SKILL.md")
        commands = self.read("skills/tvos-media-playback-workflow/references/system-player-and-remote-commands.md")
        validation = self.read("skills/tvos-media-playback-workflow/references/playback-validation-and-handoffs.md")

        for term in (
            "AVPlayerViewController",
            "MPRemoteCommandCenter",
            "MPNowPlayingInfoCenter",
            "custom-player justification",
            "tvos-app-experience-workflow",
            "avfoundation-media-pipeline-workflow",
        ):
            with self.subTest(term=term):
                self.assertIn(term, skill)
        for term in ("Menu/Back", "previous/next", "focus to an intentional browse control"):
            self.assertIn(term, validation)
        self.assertIn("A visual preference alone is not a", commands)
        self.assertIn("sufficient custom-player justification", commands)

    def test_discovery_and_portability_surfaces_list_both_workflows(self) -> None:
        readme = self.read("README.md")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        roadmap = self.read("ROADMAP.md")

        for skill in ("tvos-app-experience-workflow", "tvos-media-playback-workflow"):
            with self.subTest(skill=skill):
                self.assertIn(f"`{skill}`", readme)
                self.assertIn(f"./skills/{skill}/SKILL.md", validator)
                self.assertIn(skill, roadmap)


if __name__ == "__main__":
    unittest.main()
