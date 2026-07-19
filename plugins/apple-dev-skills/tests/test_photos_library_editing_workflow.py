from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PhotosLibraryEditingWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_picker_first_and_authorization_matrix_are_explicit(self) -> None:
        skill = self.read("skills/photos-library-editing-workflow/SKILL.md")
        selection = self.read(
            "skills/photos-library-editing-workflow/references/photosui-selection-and-authorization.md"
        )
        for term in (
            "PhotosPicker",
            "PHPickerViewController",
            "PhotosPickerItem",
            "loadTransferable",
            "privacy-preserving",
            "PHAccessLevel.addOnly",
            ".readWrite",
            ".notDetermined",
            ".restricted",
            ".denied",
            ".limited",
            ".authorized",
            "narrowest access",
            "full-library album",
        ):
            self.assertIn(term, skill + selection)

    def test_assets_requests_resources_changes_and_cloud_delivery_are_typed(self) -> None:
        skill = self.read("skills/photos-library-editing-workflow/SKILL.md")
        assets = self.read(
            "skills/photos-library-editing-workflow/references/assets-fetches-requests-resources-and-changes.md"
        )
        for term in (
            "PHAsset",
            "PHAssetCollection",
            "PHFetchResult",
            "PHPhotoLibraryChangeObserver",
            "PHChange",
            "fetchResultAfterChanges",
            "PHImageManager",
            "PHCachingImageManager",
            "PHImageRequestID",
            "degraded",
            "iCloud",
            "PHAssetResource",
            "PHAssetResourceManager",
            "Live Photo",
            "RAW-plus-processed",
        ):
            self.assertIn(term, skill + assets)

    def test_creation_and_nondestructive_editing_are_transactional(self) -> None:
        skill = self.read("skills/photos-library-editing-workflow/SKILL.md")
        editing = self.read(
            "skills/photos-library-editing-workflow/references/creation-collections-and-nondestructive-editing.md"
        )
        for term in (
            "PHPhotoLibrary.performChanges",
            "PHAssetCreationRequest",
            "PHAssetCollectionChangeRequest",
            "placeholders",
            "PHContentEditingInput",
            "PHContentEditingOutput",
            "PHAdjustmentData",
            "nondestructive",
            "transaction",
            "adjustment-version",
            "authorizationStatus(for: .readWrite) == .authorized",
        ):
            self.assertIn(term, skill + editing)

    def test_no_repository_inventory_metadata_customization_and_handoffs_are_aligned(self) -> None:
        skill = self.read("skills/photos-library-editing-workflow/SKILL.md")
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        name = "photos-library-editing-workflow"
        self.assertIn("Do not mirror the entire library", skill)
        self.assertIn("Photos repository", skill)
        self.assertIn(f"`{name}`", readme)
        self.assertIn(f"./skills/{name}/SKILL.md", validator)
        self.assertIn(f"${name}", self.read(f"skills/{name}/agents/openai.yaml"))
        self.assertIn(
            f'SKILL_NAME = "{name}"',
            self.read(f"skills/{name}/scripts/customization_config.py"),
        )
        self.assertIn("PhotosUI", plugin)
        self.assertIn("PhotoKit", plugin)
        self.assertIn("Expected exactly 59 active skills", validator)
        self.assertIn(name, self.read("skills/apple-image-representation-workflow/SKILL.md"))
        self.assertIn(name, self.read("skills/core-image-processing-workflow/SKILL.md"))
        self.assertIn(name, self.read("skills/avfoundation-media-pipeline-workflow/SKILL.md"))
        self.assertIn(name, self.read("skills/swiftui-app-architecture-workflow/SKILL.md"))
        self.assertIn(name, self.read("skills/appkit-app-architecture-workflow/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
