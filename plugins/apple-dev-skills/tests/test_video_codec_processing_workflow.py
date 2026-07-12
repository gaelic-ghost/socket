from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VideoCodecProcessingWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_covers_compression_decompression_properties_and_lifecycle(self) -> None:
        skill = self.read("skills/video-codec-processing-workflow/SKILL.md")
        lifecycle = self.read(
            "skills/video-codec-processing-workflow/references/compression-decompression-and-session-lifecycle.md"
        )
        for term in (
            "VTCompressionSession",
            "VTCompressionSessionCreate",
            "VTCompressionSessionPrepareToEncodeFrames",
            "VTCompressionSessionCompleteFrames",
            "VTDecompressionSession",
            "VTDecompressionSessionFinishDelayedFrames",
            "VTMultiPassStorage",
            "supported properties",
            "UsingHardwareAcceleratedVideoEncoder",
            "UsingHardwareAcceleratedVideoDecoder",
            "Invalidate",
            "OSStatus",
        ):
            self.assertIn(term.lower(), (skill + lifecycle).lower())

    def test_pixel_buffer_interop_color_and_hdr_are_preserved(self) -> None:
        skill = self.read("skills/video-codec-processing-workflow/SKILL.md")
        pixels = self.read(
            "skills/video-codec-processing-workflow/references/pixel-buffers-metal-color-and-hdr.md"
        )
        for term in (
            "CVPixelBuffer",
            "CVPixelBufferPool",
            "CVPixelBufferLockBaseAddress",
            "planes",
            "CVMetalTextureCacheCreateTextureFromImage",
            "CVMetalTexture",
            "IOSurface",
            "zero-copy",
            "color primaries",
            "transfer function",
            "YCbCr matrix",
            "clean aperture",
            "pixel aspect ratio",
            "HDR",
            "alpha",
        ):
            self.assertIn(term, skill + pixels)

    def test_compressed_samples_diagnostics_and_performance_are_explicit(self) -> None:
        skill = self.read("skills/video-codec-processing-workflow/SKILL.md")
        diagnostics = self.read(
            "skills/video-codec-processing-workflow/references/compressed-samples-diagnostics-and-performance.md"
        )
        for term in (
            "CMVideoFormatDescription",
            "parameter sets",
            "CMSampleBuffer",
            "presentation",
            "decode timestamps",
            "dependency flags",
            "callback status",
            "first-frame latency",
            "end-to-end frame age",
            "representative devices",
            "Bound in-flight frames",
        ):
            self.assertIn(term, skill + diagnostics)

    def test_avfoundation_preference_inventory_metadata_and_handoffs_are_aligned(self) -> None:
        skill = self.read("skills/video-codec-processing-workflow/SKILL.md")
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        name = "video-codec-processing-workflow"
        self.assertIn("prefer AVFoundation", skill)
        self.assertIn(f"`{name}`", readme)
        self.assertIn(f"./skills/{name}/SKILL.md", validator)
        self.assertIn(f"${name}", self.read(f"skills/{name}/agents/openai.yaml"))
        self.assertIn(
            f'SKILL_NAME = "{name}"',
            self.read(f"skills/{name}/scripts/customization_config.py"),
        )
        self.assertIn("VideoToolbox", plugin)
        self.assertIn("Core Video", plugin)
        self.assertIn("Expected exactly 43 active skills", validator)
        self.assertIn(name, self.read("skills/avfoundation-media-pipeline-workflow/SKILL.md"))
        self.assertIn(name, self.read("skills/coremedia-timing-samplebuffer-workflow/SKILL.md"))

    def test_shared_media_contract_includes_video_codec_types(self) -> None:
        media = self.read("shared/references/apple-media-type-ownership.md")
        for term in (
            "CVPixelBuffer",
            "CVPixelBufferPool",
            "CVMetalTextureCache",
            "VTCompressionSession",
            "VTDecompressionSession",
            "VTMultiPassStorage",
            "Choose VideoToolbox only when AVFoundation cannot express",
            "Do not replace `CVPixelBuffer`",
            "supported properties",
        ):
            self.assertIn(term, media)


if __name__ == "__main__":
    unittest.main()
