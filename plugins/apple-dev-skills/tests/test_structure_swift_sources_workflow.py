from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/structure-swift-sources/scripts/run_workflow.py"


def write_config(tmpdir: str, settings: dict) -> None:
    target = Path(tmpdir) / "structure-swift-sources" / "customization.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schemaVersion: 1", "isCustomized: true", "settings:"]
    for key, value in settings.items():
        if isinstance(value, int):
            lines.append(f"  {key}: {value}")
        else:
            lines.append(f'  {key}: "{value}"')
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


class StructureWorkflowTests(unittest.TestCase):
    def run_script(self, *args: str, env: dict | None = None) -> tuple[int, dict]:
        command_env = dict(env or os.environ)
        command_env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "apple-dev-skills-uv-cache"))
        proc = subprocess.run(
            [str(SCRIPT), *args],
            cwd="/tmp",
            env=command_env,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, json.loads(proc.stdout)

    def test_infers_header_cleanup_for_swift_package_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            (repo / "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            (repo / "Sources" / "Demo").mkdir(parents=True)
            (repo / "Sources" / "Demo" / "Feature.swift").write_text("import Foundation\n", encoding="utf-8")

            code, payload = self.run_script(
                "--repo-path",
                tmpdir,
                "--request",
                "Normalize the block-comment file headers for these Swift files",
            )

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["output"]["repository_kind"], "swift-package")
        self.assertEqual(payload["output"]["cleanup_kind"], "file-header-normalization")
        self.assertIn("scripts/normalize_swift_file_headers.py", payload["output"]["helper_scripts"])

    def test_handoffs_docc_requests_to_dedicated_skill(self) -> None:
        code, payload = self.run_script("--request", "Add DocC symbol docs to these files")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "handoff")
        self.assertEqual(payload["output"]["recommended_skill"], "author-swift-docc-docs")

    def test_handoffs_xcode_membership_requests(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            (repo / "App.xcodeproj").mkdir()
            code, payload = self.run_script(
                "--repo-path",
                tmpdir,
                "--request",
                "Move these files and update target membership afterward",
            )

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "handoff")
        self.assertEqual(payload["output"]["recommended_skill"], "xcode-build-run-workflow")

    def test_runtime_customization_changes_header_policy_and_thresholds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            write_config(
                tmpdir,
                {
                    "fileHeaderMode": "required",
                    "fileHeaderStyle": "project-banner",
                    "fileHeaderCopyrightOwner": "Gale Williams",
                    "splitSoftLimit": 250,
                    "splitHardLimit": 600,
                },
            )
            code, payload = self.run_script(
                "--repository-kind",
                "swift-package",
                "--request",
                "Split this oversized file and normalize the file headers",
                env=env,
            )

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["output"]["header_policy"]["mode"], "required")
        self.assertEqual(payload["output"]["header_policy"]["style"], "project-banner")
        self.assertEqual(payload["output"]["header_policy"]["copyright_owner"], "Gale Williams")
        self.assertEqual(payload["output"]["split_thresholds"]["soft_limit"], 250)
        self.assertEqual(payload["output"]["split_thresholds"]["hard_limit"], 600)

    def test_swiftui_structure_requires_one_view_and_preview_per_file(self) -> None:
        skill_text = (ROOT / "skills/structure-swift-sources/SKILL.md").read_text(encoding="utf-8")
        source_rules_text = (ROOT / "skills/structure-swift-sources/references/source-organization-rules.md").read_text(
            encoding="utf-8"
        )
        layout_rules_text = (ROOT / "skills/structure-swift-sources/references/layout-rules.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("require exactly one SwiftUI `View` component per file", skill_text)
        self.assertIn("keep that component's Xcode SwiftUI preview in the same file", skill_text)
        self.assertIn("Hand SwiftUI component", source_rules_text)
        self.assertIn("swiftui-app-architecture-workflow", layout_rules_text)

    def test_swiftui_view_model_structure_is_per_view_only(self) -> None:
        skill_text = (ROOT / "skills/structure-swift-sources/SKILL.md").read_text(encoding="utf-8")
        source_rules_text = (ROOT / "skills/structure-swift-sources/references/source-organization-rules.md").read_text(
            encoding="utf-8"
        )
        layout_rules_text = (ROOT / "skills/structure-swift-sources/references/layout-rules.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("do not use `+` filenames", skill_text)
        self.assertIn("concatenated filename grammar", source_rules_text)
        self.assertIn("GEASettingsSheetToggleCard.swift", layout_rules_text)
        self.assertIn("GEAWhateverModel.swift", layout_rules_text)


if __name__ == "__main__":
    unittest.main()
