from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MediaExpansionAuditTests(unittest.TestCase):
    skills = (
        "core-image-processing-workflow",
        "apple-image-representation-workflow",
        "vision-image-analysis-workflow",
        "vision-coreml-recognition-workflow",
        "camera-capture-depth-workflow",
        "arkit-spatial-sensing-workflow",
        "arkit-face-body-tracking-workflow",
        "video-codec-processing-workflow",
        "photos-library-editing-workflow",
    )

    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_every_media_skill_has_the_complete_workflow_contract(self) -> None:
        required_headings = (
            "## Purpose",
            "## When To Use",
            "## Single-Path Workflow",
            "## Inputs",
            "## Outputs",
            "## Guards and Stop Conditions",
            "## Fallbacks and Handoffs",
            "## Customization",
            "## References",
        )
        for name in self.skills:
            skill = self.read(f"skills/{name}/SKILL.md")
            references = "\n".join(
                path.read_text(encoding="utf-8")
                for path in (ROOT / "skills" / name / "references").glob("*.md")
            )
            for heading in required_headings:
                self.assertIn(heading, skill, f"{name} is missing {heading}")
            self.assertIn("Apple docs", skill)
            self.assertTrue(
                "availability" in (skill + references).lower()
                or "capability" in (skill + references).lower(),
                f"{name} must gate availability or capability claims",
            )

    def test_framework_owners_and_handoffs_remain_distinct(self) -> None:
        contracts = {
            "core-image-processing-workflow": ("CIImage", "CIFilter", "CIContext"),
            "apple-image-representation-workflow": ("CGImageSource", "CGImageDestination", "NSImage"),
            "vision-image-analysis-workflow": ("Vision", "observations", "coordinates"),
            "vision-coreml-recognition-workflow": ("Core ML", "model", "Vision"),
            "camera-capture-depth-workflow": ("AVCapture", "AVDepthData", "calibration"),
            "arkit-spatial-sensing-workflow": ("ARKit", "scene depth", "mesh"),
            "arkit-face-body-tracking-workflow": ("Face ID", "face tracking", "body"),
            "video-codec-processing-workflow": ("VideoToolbox", "CVPixelBuffer", "compressed"),
            "photos-library-editing-workflow": ("PhotosUI", "PhotoKit", "nondestructive"),
        }
        for name, terms in contracts.items():
            content = self.read(f"skills/{name}/SKILL.md")
            references = "\n".join(
                path.read_text(encoding="utf-8")
                for path in (ROOT / "skills" / name / "references").glob("*.md")
            )
            for term in terms:
                self.assertIn(term, content + references, f"{name} lost ownership term {term}")

    def test_privacy_device_evidence_and_direct_framework_paths_are_explicit(self) -> None:
        combined = "\n".join(
            self.read(f"skills/{name}/SKILL.md") for name in self.skills
        )
        for term in (
            "physical device",
            "runtime evidence",
            "privacy",
            "permission",
            "bystander",
            "Face ID",
            "limited",
            "Do not mirror",
            "generic image managers",
            "generic tracking manager",
            "Photos repository",
        ):
            self.assertIn(term, combined)

    def test_public_inventory_and_plugin_metadata_cover_the_shipped_family(self) -> None:
        readme = self.read("README.md")
        plugin = json.loads(self.read(".codex-plugin/plugin.json"))
        manifest_text = json.dumps(plugin)
        for name in self.skills:
            self.assertIn(f"`{name}`", readme)
        for term in (
            "Core Image",
            "Image I/O",
            "Vision",
            "Core ML",
            "camera",
            "depth",
            "ARKit",
            "VideoToolbox",
            "Core Video",
            "PhotosUI",
            "PhotoKit",
        ):
            self.assertIn(term, manifest_text)


if __name__ == "__main__":
    unittest.main()
