from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ImagingFoundationWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_core_image_skill_owns_processing_and_rendering(self) -> None:
        skill = self.read("skills/core-image-processing-workflow/SKILL.md")
        processing = self.read(
            "skills/core-image-processing-workflow/references/core-image-processing-and-rendering.md"
        )
        diagnostics = self.read(
            "skills/core-image-processing-workflow/references/core-image-diagnostics-and-handoffs.md"
        )

        for term in (
            "CIImage",
            "CIContext",
            "CIFilter",
            "CIRAWFilter",
            "CIKernel",
            "CVPixelBuffer",
            "IOSurface",
            "Metal",
            "lazy",
            "working color space",
            "premultiplication",
            "representative devices",
        ):
            self.assertIn(term, skill + processing + diagnostics)

    def test_representation_skill_preserves_source_meaning(self) -> None:
        skill = self.read("skills/apple-image-representation-workflow/SKILL.md")
        image_io = self.read(
            "skills/apple-image-representation-workflow/references/image-io-decoding-encoding-and-metadata.md"
        )
        bridging = self.read(
            "skills/apple-image-representation-workflow/references/apple-image-representations-and-bridging.md"
        )

        for term in (
            "CGImageSource",
            "CGImageDestination",
            "CGImageDestinationFinalize",
            "CGImageMetadata",
            "NSImage",
            "NSImageRep",
            "NSBitmapImageRep",
            "UIImage",
            "orientation",
            "scale",
            "auxiliary data",
            "incremental",
        ):
            self.assertIn(term, skill + image_io + bridging)

    def test_shared_type_ownership_requires_conversion_ledger(self) -> None:
        ownership = self.read("shared/references/apple-image-type-ownership.md")
        for term in (
            "Do not normalize Apple image values",
            "Required Conversion Ledger",
            "Name every intentional loss",
            "CGImageSource",
            "CIImage",
            "NSImage",
            "UIImage",
            "CVPixelBuffer",
            "Do not keep parallel framework and wrapper codepaths",
        ):
            self.assertIn(term, ownership)

    def test_inventory_metadata_and_customization_are_aligned(self) -> None:
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")

        for skill in (
            "core-image-processing-workflow",
            "apple-image-representation-workflow",
        ):
            self.assertIn(f"`{skill}`", readme)
            self.assertIn(f"./skills/{skill}/SKILL.md", validator)
            self.assertIn(f"${skill}", self.read(f"skills/{skill}/agents/openai.yaml"))
            self.assertIn(
                f'SKILL_NAME = "{skill}"',
                self.read(f"skills/{skill}/scripts/customization_config.py"),
            )

        self.assertIn("Core Image", plugin)
        self.assertIn("Image I/O", plugin)
        self.assertIn("Expected exactly 54 active skills", validator)


if __name__ == "__main__":
    unittest.main()
