from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VisionRecognitionWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_builtin_vision_workflow_covers_requests_sequences_and_analysis(self) -> None:
        skill = self.read("skills/vision-image-analysis-workflow/SKILL.md")
        requests = self.read(
            "skills/vision-image-analysis-workflow/references/vision-requests-observations-and-sequences.md"
        )
        live = self.read(
            "skills/vision-image-analysis-workflow/references/vision-coordinates-live-frames-and-diagnostics.md"
        )
        for term in (
            "ImageRequestHandler",
            "VNImageRequestHandler",
            "VNSequenceRequestHandler",
            "request revisions",
            "text",
            "barcode",
            "face",
            "pose",
            "segmentation",
            "feature prints",
            "bounded newest-frame",
            "source frame identity",
        ):
            self.assertIn(term, skill + requests + live)

    def test_coreml_workflow_covers_provenance_models_outputs_and_evaluation(self) -> None:
        skill = self.read("skills/vision-coreml-recognition-workflow/SKILL.md")
        integration = self.read(
            "skills/vision-coreml-recognition-workflow/references/vision-coreml-model-integration.md"
        )
        evaluation = self.read(
            "skills/vision-coreml-recognition-workflow/references/model-evaluation-performance-and-diagnostics.md"
        )
        for term in (
            "CoreMLRequest",
            "VNCoreMLModel",
            "VNCoreMLRequest",
            "MLModelDescription",
            "MLModelConfiguration",
            "computeUnits",
            "classification",
            "object detection",
            "segmentation",
            "immutable provenance",
            "regression",
            "representative devices",
        ):
            self.assertIn(term, skill + integration + evaluation)

    def test_shared_contract_covers_coordinates_confidence_identity_and_staleness(self) -> None:
        contract = self.read("shared/references/apple-vision-analysis-contract.md")
        for term in (
            "source identity",
            "source orientation",
            "preprocessing transform",
            "observation coordinate space",
            "normalized coordinates",
            "It is not automatically a calibrated probability",
            "TrueDepth face geometry is ARKit sensing",
            "Face ID and Touch ID authentication belong to Local Authentication",
            "Bound in-flight work",
            "older result",
        ):
            self.assertIn(term, contract)

    def test_inventory_metadata_customization_and_handoffs_are_aligned(self) -> None:
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        for skill in ("vision-image-analysis-workflow", "vision-coreml-recognition-workflow"):
            self.assertIn(f"`{skill}`", readme)
            self.assertIn(f"./skills/{skill}/SKILL.md", validator)
            self.assertIn(f"${skill}", self.read(f"skills/{skill}/agents/openai.yaml"))
            self.assertIn(
                f'SKILL_NAME = "{skill}"',
                self.read(f"skills/{skill}/scripts/customization_config.py"),
            )
        self.assertIn("Apple Vision", plugin)
        self.assertIn("Core ML", plugin)
        self.assertIn("Expected exactly 64 active skills", validator)


if __name__ == "__main__":
    unittest.main()
