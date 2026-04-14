from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/author-swift-docc-docs/scripts/run_workflow.py"


def write_config(tmpdir: str, skill: str, settings: dict) -> None:
    target = Path(tmpdir) / skill / "customization.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schemaVersion: 1", "isCustomized: true", "settings:"]
    for key, value in settings.items():
        lines.append(f'  {key}: "{value}"')
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


class DoccWorkflowTests(unittest.TestCase):
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

    def test_infers_symbol_docs_for_swift_package_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            (repo / "Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            (repo / "Sources" / "MyLib").mkdir(parents=True)
            code, payload = self.run_script(
                "--repo-path",
                tmpdir,
                "--request",
                "Please write the symbol docs and parameter docs for this API",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["output"]["repo_shape"], "swift-package")
            self.assertEqual(payload["output"]["task_type"], "symbol-docs")

    def test_handoffs_docs_lookup_to_explore_skill(self) -> None:
        code, payload = self.run_script("--request", "Search docs for the right DocC tutorial directive")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "handoff")
        self.assertEqual(payload["output"]["recommended_skill"], "explore-apple-swift-docs")

    def test_handoffs_generation_work_for_xcode_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            (repo / "Demo.xcodeproj").mkdir()
            code, payload = self.run_script(
                "--repo-path",
                tmpdir,
                "--request",
                "Build documentation and export the doccarchive",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "handoff")
            self.assertEqual(payload["output"]["recommended_skill"], "xcode-build-run-workflow")

    def test_tutorial_review_respects_defer_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            write_config(tmpdir, "author-swift-docc-docs", {"tutorialSupportLevel": "defer"})
            code, payload = self.run_script(
                "--request",
                "Review this DocC tutorial flow for clarity",
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["output"]["task_type"], "tutorial-aware-review")
            self.assertEqual(payload["output"]["tutorial_support_level"], "defer")
            self.assertIn("fuller DocC references", payload["output"]["next_step"])

    def test_blocks_when_task_cannot_be_inferred(self) -> None:
        code, payload = self.run_script("--request", "Help with this")
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["output"]["task_type_source"], "missing")


if __name__ == "__main__":
    unittest.main()
