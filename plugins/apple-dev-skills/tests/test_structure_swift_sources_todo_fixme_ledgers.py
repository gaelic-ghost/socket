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

    def write_roadmap(self, root: Path) -> None:
        (root / "ROADMAP.md").write_text(
            "\n".join(
                [
                    "## Milestone 29: Swift Cleanup Automation Exploration",
                    "",
                    "Tickets:",
                    "",
                    "- [ ] Evaluate a `codex exec`-friendly maintainer wrapper for sequential formatting and structure passes.",
                    "",
                    "## Milestone 30: Expand TODO and FIXME Ledger Normalization",
                    "",
                    "Tickets:",
                    "",
                    "- [ ] Extend source discovery beyond `.swift` to include Objective-C source files such as `.h`, `.m`, and `.mm`.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    def test_report_mode_counts_supported_syntaxes_and_unresolved_plan_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_roadmap(root)

            (root / "Feature.swift").write_text(
                "\n".join(
                    [
                        "struct Feature {",
                        "    // TODO: [M30] add caching",
                        "}",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "Legacy.h").write_text(
                "\n".join(
                    [
                        "#warning FIXME: [PLAN:docs/maintainers/missing-plan.md] patch legacy API",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "Compiler.swift").write_text(
                '#warning("FIXME: FIXME-0002")\n',
                encoding="utf-8",
            )

            payload = self.module.report_normalization(root)

        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["files_scanned"], 3)
        self.assertEqual(payload["counts"]["TODO"], 1)
        self.assertEqual(payload["counts"]["FIXME"], 2)
        self.assertEqual(payload["textual_comments"]["TODO"], 1)
        self.assertEqual(payload["existing_ids"]["FIXME"], 1)
        self.assertEqual(payload["source_counts"]["line-comment"], 1)
        self.assertEqual(payload["source_counts"]["objc-warning"], 1)
        self.assertEqual(payload["source_counts"]["swift-warning"], 1)
        self.assertEqual(payload["linked_roadmap_comments"], 1)
        self.assertEqual(payload["linked_plan_comments"], 0)
        self.assertEqual(len(payload["unresolved_references"]), 1)
        self.assertIn("missing-plan.md", payload["unresolved_references"][0]["reason"])

    def test_apply_mode_rewrites_swift_and_objc_and_renders_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_roadmap(root)

            plan_dir = root / "docs" / "maintainers"
            plan_dir.mkdir(parents=True)
            (plan_dir / "todo-plan.md").write_text("# Todo plan\n", encoding="utf-8")
            (plan_dir / "fix-plan.md").write_text("# Fix plan\n", encoding="utf-8")

            swift_source = root / "Sources" / "Feature.swift"
            swift_source.parent.mkdir(parents=True)
            swift_source.write_text(
                "\n".join(
                    [
                        "struct Feature {",
                        "    // TODO: [M30] [PLAN:docs/maintainers/todo-plan.md] add telemetry around retries",
                        "}",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            objc_source = root / "Sources" / "Legacy.m"
            objc_source.write_text(
                "#warning FIXME: [M29-T2] [PLAN:docs/maintainers/fix-plan.md] replace unsafe pointer dance\n",
                encoding="utf-8",
            )
            compiler_source = root / "Headers" / "Legacy.h"
            compiler_source.parent.mkdir(parents=True)
            compiler_source.write_text(
                '#warning("FIXME: FIXME-0002")\n',
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

            rewritten_swift = swift_source.read_text(encoding="utf-8")
            rewritten_objc = objc_source.read_text(encoding="utf-8")
            rewritten_warning = compiler_source.read_text(encoding="utf-8")
            todo_ledger = (root / "TODO.md").read_text(encoding="utf-8")
            fixme_ledger = (root / "FIXME.md").read_text(encoding="utf-8")

        self.assertEqual(payload["status"], "success")
        self.assertIn("TODO-0001", payload["created_entries"])
        self.assertIn("FIXME-0003", payload["created_entries"])
        self.assertIn("FIXME-0002", payload["refreshed_entries"])
        self.assertEqual(payload["source_counts"]["line-comment"], 1)
        self.assertEqual(payload["source_counts"]["objc-warning"], 1)
        self.assertEqual(payload["source_counts"]["swift-warning"], 1)

        self.assertIn("// TODO: TODO-0001", rewritten_swift)
        self.assertIn("#warning FIXME: FIXME-0003", rewritten_objc)
        self.assertIn('#warning("FIXME: FIXME-0002")', rewritten_warning)

        self.assertIn("## TODO-0001: add telemetry around retries", todo_ledger)
        self.assertIn("- File: `Sources/Feature.swift`", todo_ledger)
        self.assertIn("- Line: `2`", todo_ledger)
        self.assertIn("- Source: `line-comment`", todo_ledger)
        self.assertIn("- Detail: add telemetry around retries", todo_ledger)
        self.assertIn(
            "- Roadmap: [Milestone 30](ROADMAP.md#milestone-30-expand-todo-and-fixme-ledger-normalization)",
            todo_ledger,
        )
        self.assertIn(
            "- Plans: [docs/maintainers/todo-plan.md](docs/maintainers/todo-plan.md)",
            todo_ledger,
        )

        self.assertIn("## FIXME-0003: replace unsafe pointer dance", fixme_ledger)
        self.assertIn("- Source: `objc-warning`", fixme_ledger)
        self.assertIn("- Detail: replace unsafe pointer dance", fixme_ledger)
        self.assertIn(
            "- Roadmap: [M29-T2](ROADMAP.md#milestone-29-swift-cleanup-automation-exploration)",
            fixme_ledger,
        )
        self.assertIn(
            "- Plans: [docs/maintainers/fix-plan.md](docs/maintainers/fix-plan.md)",
            fixme_ledger,
        )
        self.assertIn("## FIXME-0002: Existing fix", fixme_ledger)
        self.assertIn("- File: `Headers/Legacy.h`", fixme_ledger)
        self.assertIn("- Line: `1`", fixme_ledger)
        self.assertIn("- Source: `swift-warning`", fixme_ledger)
        self.assertIn("- Detail: Existing fix detail", fixme_ledger)
        self.assertIn("- Roadmap: none", fixme_ledger)
        self.assertIn("- Plans: none", fixme_ledger)

    def test_cli_apply_prints_json_summary_for_objective_cplusplus(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_roadmap(root)
            (root / "Mixed.mm").write_text(
                "// TODO: [M30] wire analytics bridge\n",
                encoding="utf-8",
            )

            proc = subprocess.run(
                ["uv", "run", str(MODULE_PATH), "--root", str(root), "--apply"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            payload = json.loads(proc.stdout)

        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["comment_count"], 1)
        self.assertEqual(payload["files_scanned"], 1)
        self.assertIn("TODO-0001", payload["created_entries"])


if __name__ == "__main__":
    unittest.main()
