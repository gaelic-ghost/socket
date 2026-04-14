from __future__ import annotations

import importlib.util
import plistlib
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills/format-swift-sources/scripts/export_swiftformat_xcode_config.py"


def load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FormatSwiftSourcesExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module(MODULE_PATH)

    def test_infer_options_export_keeps_rules_and_explicit_swift_version(self) -> None:
        payload = {
            "infer-options": True,
            "rules": {
                "blankLinesBetweenScopes": True,
                "redundantSelf": False,
                "wrapArguments": True,
            },
            "format-options": {
                "indent": "4",
                "swiftversion": "6.0",
                "languagemode": "0",
            },
        }

        lines = self.module.serialize_lines(payload)
        rendered = "\n".join(lines)

        self.assertIn("--rules blankLinesBetweenScopes,wrapArguments", rendered)
        self.assertIn("--swiftversion 6.0", rendered)
        self.assertNotIn("--indent 4", rendered)

    def test_explicit_options_export_writes_sorted_option_lines(self) -> None:
        payload = {
            "infer-options": False,
            "rules": {"wrap": True},
            "format-options": {
                "indent": "2",
                "allman": False,
                "header": "",
            },
        }

        lines = self.module.serialize_lines(payload)

        self.assertIn("--rules wrap", lines)
        self.assertIn("--allman false", lines)
        self.assertIn("--indent 2", lines)
        self.assertNotIn("--header ", "\n".join(lines))
        self.assertLess(lines.index("--allman false"), lines.index("--indent 2"))

    def test_plist_input_path_loads_dictionary_payload(self) -> None:
        payload = {
            "infer-options": True,
            "rules": {"wrap": True},
            "format-options": {"swiftversion": "5.10"},
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            plist_path = Path(tmpdir) / "swiftformat.plist"
            with plist_path.open("wb") as handle:
                plistlib.dump(payload, handle)

            loaded = self.module.load_plist(plist_path)

        self.assertEqual(loaded["rules"]["wrap"], True)
        self.assertEqual(loaded["format-options"]["swiftversion"], "5.10")


if __name__ == "__main__":
    unittest.main()
