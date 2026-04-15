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
                    "fileHeaderStyle": "plain-block",
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
        self.assertEqual(payload["output"]["split_thresholds"]["soft_limit"], 250)
        self.assertEqual(payload["output"]["split_thresholds"]["hard_limit"], 600)


if __name__ == "__main__":
    unittest.main()
