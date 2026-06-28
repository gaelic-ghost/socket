from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


MEDIA_SKILLS = {
    "avfaudio-session-workflow": [
        "AVAudioSession",
        "AVAudioApplication.requestRecordPermission",
        "AVAudioSession.RouteSharingPolicy",
        "notifyOthersOnDeactivation",
        "route changes",
        "apple-media-type-ownership.md",
        "xcode-build-run-workflow",
    ],
    "avaudio-engine-workflow": [
        "AVAudioEngine",
        "AVAudioFormat",
        "AVAudioPCMBuffer",
        "manual rendering",
        "real-time render callbacks",
        "apple-media-type-ownership.md",
        "coreaudio-modernization-repair-workflow",
    ],
    "avfoundation-media-pipeline-workflow": [
        "AVCaptureSession.startRunning()",
        "AVAsyncProperty",
        "loadValuesAsynchronously(forKeys:)",
        "isReadyForMoreMediaData",
        "AVAssetWriterInput",
        "apple-media-type-ownership.md",
        "coremedia-timing-samplebuffer-workflow",
    ],
    "coremedia-timing-samplebuffer-workflow": [
        "CMTime",
        "CMClock",
        "CMTimebase",
        "CMFormatDescription",
        "CMSampleBuffer",
        "CMSampleTimingInfo",
        "presentation timestamp",
        "apple-media-type-ownership.md",
        "AVSampleBufferRenderSynchronizer",
    ],
    "coreaudio-modernization-repair-workflow": [
        "AudioStreamBasicDescription",
        "AudioComponentDescription",
        "AudioBufferList",
        "AudioQueue",
        "AudioUnit",
        "OSStatus",
        "apple-media-type-ownership.md",
        "archive docs only",
    ],
}


class MediaAudioWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_media_audio_skills_have_required_structure_and_prompts(self) -> None:
        for skill, expected_terms in MEDIA_SKILLS.items():
            with self.subTest(skill=skill):
                skill_text = self.read(f"skills/{skill}/SKILL.md")
                prompt_text = self.read(f"skills/{skill}/agents/openai.yaml")

                self.assertIn(f"name: {skill}", skill_text)
                self.assertIn("Apply the Apple docs gate", skill_text)
                self.assertIn("repair", skill_text.lower())
                self.assertIn("references/snippets/apple-xcode-project-core.md", skill_text)
                self.assertIn(f"${skill}", prompt_text)
                for term in expected_terms:
                    self.assertIn(term, skill_text)

    def test_reference_files_cover_repair_boundaries(self) -> None:
        references = {
            "skills/avfaudio-session-workflow/references/session-policy-and-repair.md": [
                "headphones disconnect",
                "AVCaptureSession",
                "AVAudioSession.RouteSharingPolicy",
                "operation, category, mode, route, permission state",
            ],
            "skills/avaudio-engine-workflow/references/engine-graph-and-repair.md": [
                "AVAudioPCMBuffer",
                "AudioStreamBasicDescription",
                "conversion back to AVFAudio explicit",
            ],
            "skills/avaudio-engine-workflow/references/realtime-rendering-safety.md": [
                "allocation",
                "await",
                "main-actor hops",
            ],
            "skills/avfoundation-media-pipeline-workflow/references/media-pipeline-and-repair.md": [
                "AVAssetReaderOutput",
                "AVAssetWriterInput",
                "Use Core Media types for timing",
            ],
            "skills/avfoundation-media-pipeline-workflow/references/async-loading-and-backpressure.md": [
                "try await asset.load(.duration)",
                "keep durations as `CMTime`",
                "loadValuesAsynchronously(forKeys:)",
                "isReadyForMoreMediaData",
            ],
            "skills/coremedia-timing-samplebuffer-workflow/references/diagnostics-and-handoffs.md": [
                "Keep diagnostics typed",
                "CMSampleTimingInfo",
                "CMFormatDescription",
            ],
            "skills/coremedia-timing-samplebuffer-workflow/references/time-samplebuffer-and-repair.md": [
                "presentation timestamp",
                "decode timestamp",
                "CMTime",
                "CMTimebase",
                "CMSampleTimingInfo",
            ],
            "skills/coreaudio-modernization-repair-workflow/references/coreaudio-modernization-and-repair.md": [
                "Framework choice",
                "AudioConverterRef",
                "OSStatus",
            ],
            "skills/coreaudio-modernization-repair-workflow/references/legacy-archive-boundary.md": [
                "historical or migration context",
                "current AVFAudio documentation",
                "Archive context does not justify replacing Apple media types",
                "Audio Unit Programming Guide",
            ],
        }

        for path, terms in references.items():
            with self.subTest(path=path):
                text = self.read(path)
                for term in terms:
                    self.assertIn(term, text)

    def test_readme_and_validator_include_active_media_audio_skills(self) -> None:
        readme = self.read("README.md")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        roadmap = self.read("ROADMAP.md")

        for skill in MEDIA_SKILLS:
            self.assertIn(f"`{skill}`", readme)
            self.assertIn(f"./skills/{skill}/SKILL.md", validator)
            self.assertIn(skill, roadmap)

    def test_shared_media_type_ownership_contract_is_strict(self) -> None:
        text = self.read("shared/references/apple-media-type-ownership.md")

        for term in [
            "Use Apple and Swift media types as the default representation",
            "only after naming the concrete reason",
            "AVAudioSession.Category",
            "AVAudioFormat",
            "AVAssetWriterInput",
            "CMTime",
            "CMSampleBuffer",
            "CMFormatDescription",
            "AudioStreamBasicDescription",
            "AudioBufferList",
            "OSStatus",
            "Do not convert `CMTime`",
            "Do not model media type, route, category, mode",
            "Do not keep duplicate AVFAudio and Core Audio codepaths",
        ]:
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
