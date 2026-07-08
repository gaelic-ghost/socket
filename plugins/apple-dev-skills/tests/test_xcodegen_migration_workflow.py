from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/migrate-xcode-project-to-xcodegen/scripts/run_workflow.py"


PBXPROJ_WITH_SETTINGS = """
// !$*UTF8*$!
{
  objects = {
    111111111111111111111111 = {
      isa = PBXNativeTarget;
      name = DemoApp;
      buildConfigurationList = 222222222222222222222222;
    };
    333333333333333333333333 = {
      isa = XCBuildConfiguration;
      buildSettings = {
        MARKETING_VERSION = 0.0.7;
        CURRENT_PROJECT_VERSION = 14;
        SWIFT_VERSION = 6.0;
        CODE_SIGN_ENTITLEMENTS = DemoApp/DemoApp.entitlements;
        ENABLE_APP_SANDBOX = YES;
        DEAD_CODE_STRIPPING = YES;
      };
      name = Debug;
    };
  };
}
"""


class XcodeGenMigrationWorkflowTests(unittest.TestCase):
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
        payload = json.loads(proc.stdout)
        return proc.returncode, payload

    def make_xcode_project(self, repo: Path) -> None:
        project_dir = repo / "DemoApp.xcodeproj"
        project_dir.mkdir()
        (project_dir / "project.pbxproj").write_text(PBXPROJ_WITH_SETTINGS, encoding="utf-8")

    def test_audits_xcode_managed_project_before_xcodegen_conversion(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            self.make_xcode_project(repo)

            code, payload = self.run_script("--repo-root", str(repo))

            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            output = payload["output"]
            self.assertEqual(output["migration_path"], "xcode-managed-to-xcodegen")
            self.assertIn("DemoApp.xcodeproj", output["discovered"]["projects"])
            self.assertIn("MARKETING_VERSION", output["pbxproj_audit"]["settings_to_promote"])
            self.assertIn("CODE_SIGN_ENTITLEMENTS", output["pbxproj_audit"]["settings_to_promote"])
            self.assertIn("DEAD_CODE_STRIPPING", output["pbxproj_audit"]["settings_to_promote"])
            self.assertTrue(any("Promote pbxproj build settings" in phase for phase in output["recommended_phases"]))
            self.assertEqual(output["file_audit"]["expected_app_entitlements"], "Sources/Support/DemoApp.entitlements")
            self.assertTrue(any("Sources/Support/DemoApp.entitlements" in phase for phase in output["recommended_phases"]))

    def test_audits_existing_xcodegen_project_for_current_baseline_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            self.make_xcode_project(repo)
            (repo / "project.yml").write_text(
                """
name: DemoApp
targets:
  DemoApp:
    type: application
    platform: macOS
    sources:
      - path: Sources/App
        type: syncedFolder
      - path: Sources/Resources
        type: syncedFolder
  DemoAppTests:
    type: bundle.unit-test
    sources:
      - path: Tests/DemoAppTests
        type: syncedFolder
""",
                encoding="utf-8",
            )
            app_sources = repo / "Sources" / "App"
            app_sources.mkdir(parents=True)
            (app_sources / "DemoApp.swift").write_text(
                """
import SwiftUI

@main
struct DemoApp: App {
    var body: some Scene {
        WindowGroup { Text("Demo") }
    }
}
""",
                encoding="utf-8",
            )
            (app_sources / "DemoAppBeta.swift").write_text(
                """
import SwiftUI

@main
struct DemoAppBeta: App {
    var body: some Scene {
        WindowGroup { Text("Demo") }
    }
}
""",
                encoding="utf-8",
            )

            code, payload = self.run_script("--repo-root", str(repo))

            self.assertEqual(code, 0)
            output = payload["output"]
            self.assertEqual(output["migration_path"], "modernize-xcodegen")
            self.assertIn("default_source_directory_type", output["project_yml_audit"]["baseline_gaps"])
            self.assertIn("config_files", output["project_yml_audit"]["baseline_gaps"])
            self.assertIn("sources_root", output["project_yml_audit"]["baseline_gaps"])
            self.assertIn("shared_root", output["project_yml_audit"]["baseline_gaps"])
            self.assertIn("tests_root", output["project_yml_audit"]["baseline_gaps"])
            self.assertIn("Shared", output["file_audit"]["missing_standard_directories"])
            self.assertIn("Extensions", output["file_audit"]["missing_standard_directories"])
            self.assertIn("Scripts", output["file_audit"]["missing_standard_directories"])
            self.assertIn("Packages", output["file_audit"]["missing_standard_directories"])
            self.assertIn("Sources/App", output["project_yml_audit"]["fragmented_source_entries"])
            self.assertIn("Sources/Resources", output["project_yml_audit"]["fragmented_source_entries"])
            self.assertIn("Tests/DemoAppTests", output["project_yml_audit"]["fragmented_source_entries"])
            self.assertIn("Sources/App/DemoApp.swift", output["file_audit"]["app_entry_points"])
            self.assertIn("Sources/App/DemoAppBeta.swift", output["file_audit"]["app_entry_points"])
            self.assertTrue(any("current baseline gaps" in phase for phase in output["recommended_phases"]))
            self.assertTrue(any("Collapse fragmented XcodeGen source entries" in phase for phase in output["recommended_phases"]))
            self.assertTrue(any("Add missing standard top-level Xcode app directories" in phase for phase in output["recommended_phases"]))
            self.assertTrue(any("Collapse multiple app lifecycle entry points" in phase for phase in output["recommended_phases"]))

    def test_blocks_when_requested_modernization_has_no_project_yml(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            self.make_xcode_project(repo)

            code, payload = self.run_script("--repo-root", str(repo), "--mode", "xcodegen-modernize")

            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn("no project.yml", payload["output"]["reason"])

    def test_skill_metadata_and_reference_contracts_are_wired(self) -> None:
        skill_text = (ROOT / "skills/migrate-xcode-project-to-xcodegen/SKILL.md").read_text(encoding="utf-8")
        reference_text = (
            ROOT / "skills/migrate-xcode-project-to-xcodegen/references/migration-audit-and-promotion.md"
        ).read_text(encoding="utf-8")
        prompt_text = (
            ROOT / "skills/migrate-xcode-project-to-xcodegen/agents/openai.yaml"
        ).read_text(encoding="utf-8")
        validator_text = (ROOT / ".github/scripts/validate_repo_docs.sh").read_text(encoding="utf-8")
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        plugin_text = (ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8")

        self.assertIn("migration-audit-and-promotion.md", skill_text)
        self.assertIn("references/snippets/apple-xcode-project-core.md", skill_text)
        self.assertIn("xcode-managed-to-xcodegen", reference_text)
        self.assertIn("modernize XcodeGen", reference_text)
        self.assertIn("$migrate-xcode-project-to-xcodegen", prompt_text)
        self.assertIn("./skills/migrate-xcode-project-to-xcodegen/SKILL.md", validator_text)
        self.assertIn("`migrate-xcode-project-to-xcodegen`", readme_text)
        self.assertIn("XcodeGen migration", plugin_text)


if __name__ == "__main__":
    unittest.main()
