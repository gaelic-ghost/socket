from __future__ import annotations

from datetime import date
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills/structure-swift-sources/scripts/normalize_swift_file_headers.py"
TEMPLATE_PATH = ROOT / "skills/structure-swift-sources/references/file-header-inventory.template.yaml"


def load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructureSwiftSourcesFileHeaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module(MODULE_PATH)

    def test_report_counts_compliant_missing_and_malformed_headers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Sources").mkdir()
            (root / "Sources" / "Compliant.swift").write_text(
                "/*\nSampleProject\nCompliant.swift\n© Gale Williams 2026\n\nConcern: Entry-point state and setup.\nPurpose: Explains the feature entry point.\nKey Types: FeatureView, FeatureState\nSee Also: FeatureView+Model.swift\n*/\n\nimport Foundation\n",
                encoding="utf-8",
            )
            (root / "Sources" / "Missing.swift").write_text("import Foundation\n", encoding="utf-8")
            (root / "Sources" / "Malformed.swift").write_text(
                "/*\nSampleProject\nMalformed.swift\n© Gale Williams 2026\n\nPurpose: Missing the concern field.\n*/\n\nimport Foundation\n",
                encoding="utf-8",
            )

            payload = self.module.report_headers(root)

        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["files_scanned"], 3)
        self.assertEqual(payload["counts"]["compliant"], 1)
        self.assertEqual(payload["counts"]["missing-header"], 1)
        self.assertEqual(payload["counts"]["malformed-header"], 1)

    def test_apply_inventory_preserves_license_block_and_adds_structured_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "Sources"
            source_dir.mkdir()
            target = source_dir / "Feature.swift"
            target.write_text(
                "/*\nCopyright 2026 Example.\n*/\n\nimport Foundation\n",
                encoding="utf-8",
            )
            inventory = root / "headers.yaml"
            inventory.write_text(
                "\n".join(
                    [
                        "entries:",
                        "  - path: Sources/Feature.swift",
                        '    purpose: "Defines the feature entry point in plain terms."',
                        '    concern: "Feature startup state and setup."',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = self.module.apply_inventory(root, inventory)
            rewritten = target.read_text(encoding="utf-8")

        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["created_headers"], 1)
        self.assertIn("Copyright 2026 Example.", rewritten)
        self.assertIn(root.name, rewritten)
        self.assertIn("Feature.swift", rewritten)
        self.assertIn(f"© Gale Williams {date.today().year}", rewritten)
        self.assertIn("Concern: Feature startup state and setup.", rewritten)
        self.assertIn("Purpose: Defines the feature entry point in plain terms.", rewritten)

    def test_apply_inventory_replaces_existing_structured_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "Sources"
            source_dir.mkdir()
            target = source_dir / "Feature.swift"
            target.write_text(
                "/*\nOldProject\nFeature.swift\n© Gale Williams 2022\n\nConcern: Old concern.\nPurpose: Old purpose.\n*/\n\nimport Foundation\n",
                encoding="utf-8",
            )
            inventory = root / "headers.yaml"
            inventory.write_text(
                "\n".join(
                    [
                        "entries:",
                        "  - path: Sources/Feature.swift",
                        '    purpose: "Defines the new feature entry point."',
                        '    concern: "Feature state and wiring."',
                        '    key_types: "FeatureView, FeatureState"',
                        '    see_also: "FeatureView+Model.swift, FeatureView+Modifier.swift"',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = self.module.apply_inventory(root, inventory)
            rewritten = target.read_text(encoding="utf-8")

        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["updated_headers"], 1)
        self.assertIn(root.name, rewritten)
        self.assertIn("© Gale Williams 2022", rewritten)
        self.assertIn("Concern: Feature state and wiring.", rewritten)
        self.assertIn("Purpose: Defines the new feature entry point.", rewritten)
        self.assertIn("Key Types: FeatureView, FeatureState", rewritten)
        self.assertIn("See Also: FeatureView+Model.swift, FeatureView+Modifier.swift", rewritten)
        self.assertNotIn("Old purpose", rewritten)

    def test_checked_in_inventory_template_matches_loader_contract(self) -> None:
        entries = self.module.load_inventory(TEMPLATE_PATH)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["path"], "Sources/Feature.swift")
        self.assertTrue(entries[0]["concern"])
        self.assertTrue(entries[0]["purpose"])
        self.assertEqual(entries[0]["key_types"], ["FeatureView", "FeatureState"])
        self.assertEqual(
            entries[0]["see_also"],
            ["FeatureView+Model.swift", "FeatureView+Modifier.swift"],
        )


if __name__ == "__main__":
    unittest.main()
