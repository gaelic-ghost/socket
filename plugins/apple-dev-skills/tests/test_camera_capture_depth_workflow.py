from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CameraCaptureDepthWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_covers_discovery_controls_rotation_and_capabilities(self) -> None:
        skill = self.read("skills/camera-capture-depth-workflow/SKILL.md")
        controls = self.read(
            "skills/camera-capture-depth-workflow/references/camera-discovery-controls-and-rotation.md"
        )
        capability = self.read("shared/references/apple-camera-capability-contract.md")
        for term in (
            "AVCaptureDevice.DiscoverySession",
            "AVCaptureDevice.Format",
            "supportedMultiCamDeviceSets",
            "AVCaptureMultiCamSession.isMultiCamSupported",
            "lockForConfiguration()",
            "focus",
            "exposure",
            "white balance",
            "zoom",
            "torch",
            "AVCaptureDevice.RotationCoordinator",
            "videoRotationAngle",
            "documented",
            "discovered",
            "device-verified",
        ):
            self.assertIn(term, skill + controls + capability)

    def test_skill_covers_photo_features_lifecycle_and_pressure(self) -> None:
        skill = self.read("skills/camera-capture-depth-workflow/SKILL.md")
        photo = self.read(
            "skills/camera-capture-depth-workflow/references/photo-computational-capture-and-lifecycle.md"
        )
        for term in (
            "AVCapturePhotoOutput",
            "AVCapturePhotoSettings",
            "RAW",
            "Live Photo",
            "quality prioritization",
            "responsive capture",
            "deferred photo delivery",
            "spatial video",
            "do not infer a spatial-photo API",
            "cinematic",
            "AVCapturePhoto",
            "interruptions",
            "media-services reset",
            "system pressure",
        ):
            self.assertIn(term, skill + photo)

    def test_skill_covers_depth_calibration_sync_mattes_and_drops(self) -> None:
        skill = self.read("skills/camera-capture-depth-workflow/SKILL.md")
        depth = self.read(
            "skills/camera-capture-depth-workflow/references/depth-calibration-and-synchronized-capture.md"
        )
        for term in (
            "AVDepthData",
            "activeDepthDataFormat",
            "depthDataAccuracy",
            "AVCameraCalibrationData",
            "intrinsic matrix",
            "lens-distortion",
            "AVCaptureDataOutputSynchronizer",
            "AVCaptureSynchronizedData",
            "wasDataDropped",
            "AVPortraitEffectsMatte",
            "AVSemanticSegmentationMatte",
        ):
            self.assertIn(term, skill + depth)

    def test_inventory_metadata_customization_and_handoffs_are_aligned(self) -> None:
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        skill = "camera-capture-depth-workflow"
        self.assertIn(f"`{skill}`", readme)
        self.assertIn(f"./skills/{skill}/SKILL.md", validator)
        self.assertIn(f"${skill}", self.read(f"skills/{skill}/agents/openai.yaml"))
        self.assertIn(
            f'SKILL_NAME = "{skill}"',
            self.read(f"skills/{skill}/scripts/customization_config.py"),
        )
        self.assertIn("camera", plugin.lower())
        self.assertIn("depth", plugin.lower())
        self.assertIn("Expected exactly 58 active skills", validator)
        self.assertIn(skill, self.read("skills/avfoundation-media-pipeline-workflow/SKILL.md"))
        self.assertIn(skill, self.read("skills/vision-image-analysis-workflow/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
