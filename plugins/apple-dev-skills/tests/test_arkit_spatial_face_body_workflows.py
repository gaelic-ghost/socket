from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ARKitSpatialFaceBodyWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_spatial_skill_covers_world_depth_mesh_maps_and_raycasting(self) -> None:
        skill = self.read("skills/arkit-spatial-sensing-workflow/SKILL.md")
        world = self.read(
            "skills/arkit-spatial-sensing-workflow/references/world-tracking-depth-meshes-and-maps.md"
        )
        for term in (
            "ARSession",
            "ARWorldTrackingConfiguration",
            "ARCamera.TrackingState",
            "ray casting",
            "sceneDepth",
            "smoothedSceneDepth",
            "supportsSceneReconstruction",
            "ARMeshAnchor",
            "ARMeshGeometry",
            "ARWorldMap",
            "relocalization",
            "ARReferenceObject",
            "geographic anchors",
        ):
            self.assertIn(term, skill + world)

    def test_spatial_skill_distinguishes_visionos_and_framework_handoffs(self) -> None:
        skill = self.read("skills/arkit-spatial-sensing-workflow/SKILL.md")
        providers = self.read(
            "skills/arkit-spatial-sensing-workflow/references/visionos-providers-rendering-and-diagnostics.md"
        )
        for term in (
            "ARKitSession",
            "authorization",
            "providers",
            "Do not translate an iOS",
            "RealityKit",
            "RoomCaptureSession",
            "RoomCaptureView",
            "RoomBuilder",
            "CapturedRoom",
            "SceneKit",
            "Metal",
        ):
            self.assertIn(term, skill + providers)

    def test_face_body_skill_covers_tracking_skeleton_and_authentication_boundary(self) -> None:
        skill = self.read("skills/arkit-face-body-tracking-workflow/SKILL.md")
        face = self.read(
            "skills/arkit-face-body-tracking-workflow/references/face-geometry-blend-shapes-and-authentication-boundary.md"
        )
        body = self.read(
            "skills/arkit-face-body-tracking-workflow/references/body-skeleton-scale-rendering-and-diagnostics.md"
        )
        for term in (
            "ARFaceTrackingConfiguration",
            "ARFaceAnchor",
            "ARFaceGeometry",
            "blend shapes",
            "eye transforms",
            "supportsWorldTracking",
            "LAContext",
            "LAPolicy",
            "not Face ID",
            "ARBodyTrackingConfiguration",
            "ARBodyAnchor",
            "ARSkeleton3D",
            "estimatedScaleFactor",
        ):
            self.assertIn(term, skill + face + body)

    def test_shared_privacy_inventory_and_evidence_boundaries_are_explicit(self) -> None:
        privacy = self.read("shared/references/apple-spatial-data-privacy-contract.md")
        for term in (
            "world maps",
            "room structure",
            "face geometry",
            "body skeletons",
            "ARKitSession",
            "in-memory, session-scoped",
            "retention",
            "deletion",
            "estimates",
            "Do not describe them as exact",
            "bystander",
        ):
            self.assertIn(term, privacy)

    def test_inventory_metadata_customization_and_cross_skill_handoffs_are_aligned(self) -> None:
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        for skill in ("arkit-spatial-sensing-workflow", "arkit-face-body-tracking-workflow"):
            self.assertIn(f"`{skill}`", readme)
            self.assertIn(f"./skills/{skill}/SKILL.md", validator)
            self.assertIn(f"${skill}", self.read(f"skills/{skill}/agents/openai.yaml"))
            self.assertIn(
                f'SKILL_NAME = "{skill}"',
                self.read(f"skills/{skill}/scripts/customization_config.py"),
            )
        self.assertIn("ARKit", plugin)
        self.assertIn("LiDAR", plugin)
        self.assertIn("Expected exactly 50 active skills", validator)
        self.assertIn("arkit-spatial-sensing-workflow", self.read("skills/camera-capture-depth-workflow/SKILL.md"))
        self.assertIn("arkit-face-body-tracking-workflow", self.read("skills/vision-image-analysis-workflow/SKILL.md"))
        self.assertIn("arkit-spatial-sensing-workflow", self.read("skills/apple-ui-accessibility-workflow/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
