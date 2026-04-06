from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills/structure-swift-sources/scripts/normalize_todo_fixme_ledgers.py"


def load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructureSwiftSourcesTodoFixmeLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module(MODULE_PATH)

    def test_report_mode_counts_textual_and_existing_ticket_comments(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Example.swift").write_text(
                "\n".join(
                    [
                        "struct Example {",
                        "    // TODO: add caching",
                        "    // FIXME: FIXME-0002",
                        "}",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "FIXME.md").write_text(
                "\n".join(
                    [
                        "# FIXME Ledger",
                        "",
                        "Track normalized FIXME tickets extracted from Swift sources.",
                        "",
                        "## FIXME-0002: Existing fix",
                        "- Status: open",
                        "- File: `Old.swift`",
                        "- Line: `2`",
                        "- Detail: Existing fix detail",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = self.module.report_normalization(root)

        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["counts"]["TODO"], 1)
        self.assertEqual(payload["counts"]["FIXME"], 1)
        self.assertEqual(payload["textual_comments"]["TODO"], 1)
        self.assertEqual(payload["existing_ids"]["FIXME"], 1)

    def test_apply_mode_rewrites_comments_and_refreshes_ledgers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "Sources" / "Feature.swift"
            source.parent.mkdir(parents=True)
            source.write_text(
                "\n".join(
                    [
                        "struct Feature {",
                        "    // TODO: add telemetry around retries",
                        "    // FIXME: FIXME-0002",
                        "}",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "FIXME.md").write_text(
                "\n".join(
                    [
                        "# FIXME Ledger",
                        "",
                        "Track normalized FIXME tickets extracted from Swift sources.",
                        "",
                        "## FIXME-0002: Existing fix",
                        "- Status: open",
                        "- File: `Legacy.swift`",
                        "- Line: `9`",
                        "- Detail: Existing fix detail",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = self.module.apply_normalization(root)

            rewritten = source.read_text(encoding="utf-8")
            todo_ledger = (root / "TODO.md").read_text(encoding="utf-8")
            fixme_ledger = (root / "FIXME.md").read_text(encoding="utf-8")

        self.assertEqual(payload["status"], "success")
        self.assertIn("TODO-0001", payload["created_entries"])
        self.assertIn("FIXME-0002", payload["refreshed_entries"])
        self.assertIn("// TODO: TODO-0001", rewritten)
        self.assertIn("// FIXME: FIXME-0002", rewritten)
        self.assertIn("## TODO-0001: add telemetry around retries", todo_ledger)
        self.assertIn("- File: `Sources/Feature.swift`", todo_ledger)
        self.assertIn("- Line: `2`", todo_ledger)
        self.assertIn("- Detail: add telemetry around retries", todo_ledger)
        self.assertIn("- File: `Sources/Feature.swift`", fixme_ledger)
        self.assertIn("- Line: `3`", fixme_ledger)
        self.assertIn("- Detail: Existing fix detail", fixme_ledger)

    def test_cli_apply_prints_json_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Example.swift").write_text(
                "\n".join(
                    [
                        "enum Example {",
                        "    // TODO: wire analytics",
                        "}",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            proc = subprocess.run(
                [str(MODULE_PATH), "--root", str(root), "--apply"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            payload = json.loads(proc.stdout)

        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["comment_count"], 1)
        self.assertIn("TODO-0001", payload["created_entries"])


if __name__ == "__main__":
    unittest.main()
