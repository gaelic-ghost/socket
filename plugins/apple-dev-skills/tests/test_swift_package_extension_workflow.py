from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/swift-package-extension-workflow"
SCRIPT = SKILL / "scripts/run_workflow.py"


class SwiftPackageExtensionWorkflowTests(unittest.TestCase):
    def run_script(self, *args: str) -> tuple[int, dict]:
        env = dict(os.environ)
        env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "apple-dev-skills-uv-cache"))
        proc = subprocess.run(
            [str(SCRIPT), *args],
            cwd="/tmp",
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, json.loads(proc.stdout)

    def package(self, root: str) -> None:
        Path(root, "Package.swift").write_text("// swift-tools-version: 6.2\n", encoding="utf-8")

    def test_trait_plan_covers_both_toolchains_and_support_floor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            self.package(tmpdir)
            code, payload = self.run_script("--extension-type", "traits", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            commands = "\n".join(payload["output"]["planned_commands"])
            self.assertIn("swiftly use --print-location", commands)
            self.assertIn("xcrun swift --version", commands)
            self.assertIn("swift package show-traits --format json", commands)
            self.assertIn("xcrun swift test --disable-default-traits", commands)
            self.assertEqual(payload["output"]["support_window"]["minimum"], "6.2")

    def test_infers_macro_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            self.package(tmpdir)
            code, payload = self.run_script("--request", "diagnose this macro expansion", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["output"]["extension_type"], "macro")
            self.assertIn("swift package init --type macro", payload["output"]["planned_commands"])

    def test_mixed_root_hands_off_to_xcode(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            self.package(tmpdir)
            Path(tmpdir, "Demo.xcodeproj").mkdir()
            code, payload = self.run_script("--extension-type", "command-plugin", "--repo-root", tmpdir)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertIn("xcode-build-run-workflow", payload["output"]["next_step"])

    def test_skill_contains_planned_reference_set_and_toolchain_boundary(self) -> None:
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        references = {
            "package-plugins-build-command-and-xcode.md",
            "plugin-permissions-sandbox-and-outputs.md",
            "swift-macros-package-shape.md",
            "package-traits-feature-flags.md",
            "generated-source-and-build-products.md",
            "xcode-handoff-conditions.md",
            "cli-command-matrix.md",
        }
        for reference in references:
            self.assertTrue((SKILL / "references" / reference).is_file())
            self.assertIn(reference, skill_text)
        self.assertIn("swiftly use --print-location", skill_text)
        self.assertIn("xcrun swift --version", skill_text)

    def test_existing_package_skills_route_extension_work(self) -> None:
        for name in (
            "swift-package-build-run-workflow",
            "swift-package-testing-workflow",
            "swift-package-workflow",
        ):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("swift-package-extension-workflow", text)

    def test_roadmap_marks_milestone_complete(self) -> None:
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("Milestone 41: Swift Package Extension Workflow - Completed", roadmap)
        self.assertIn("Completed Milestone 41", roadmap)


if __name__ == "__main__":
    unittest.main()
