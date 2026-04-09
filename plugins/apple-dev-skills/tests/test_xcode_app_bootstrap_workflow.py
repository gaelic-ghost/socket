from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/bootstrap-xcode-app-project/scripts/run_workflow.py"


def write_config(tmpdir: str, skill: str, settings: dict) -> None:
    target = Path(tmpdir) / skill / "customization.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schemaVersion: 1", "isCustomized: true", "settings:"]
    for key, value in settings.items():
        if isinstance(value, bool):
            raw = "true" if value else "false"
        else:
            raw = f'"{value}"'
        lines.append(f"  {key}: {raw}")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


@contextmanager
def fake_tools_in_path(*entries: tuple[str, str]):
    with tempfile.TemporaryDirectory() as tmpdir:
        bin_dir = Path(tmpdir) / "bin"
        bin_dir.mkdir()
        for name, body in entries:
            tool = bin_dir / name
            tool.write_text(body, encoding="utf-8")
            tool.chmod(0o755)
        env = dict(os.environ)
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        yield env


class XcodeAppBootstrapWorkflowTests(unittest.TestCase):
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

    def test_wrapper_injects_runtime_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            write_config(
                tmpdir,
                "bootstrap-xcode-app-project",
                {
                    "defaultPlatform": "macos",
                    "defaultOrgIdentifier": "dev.example",
                    "copyAgentsMd": False,
                },
            )
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script("--name", "DemoApp", "--project-generator", "xcodegen", "--dry-run", env=env)
            self.assertEqual(code, 0)
            self.assertEqual(payload["normalized_inputs"]["platform"], "macos")
            self.assertEqual(payload["normalized_inputs"]["ui_stack"], "swiftui")
            self.assertEqual(payload["normalized_inputs"]["project_generator"], "xcodegen")
            self.assertEqual(payload["bundle_identifier"], "dev.example.DemoApp")
            self.assertFalse(payload["normalized_inputs"]["copy_agents_md"])

    def test_blocks_non_app_project_kind(self) -> None:
        code, payload = self.run_script(
            "--name",
            "DemoPkg",
            "--project-kind",
            "package",
            "--platform",
            "macos",
            "--project-generator",
            "xcodegen",
            "--dry-run",
        )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("bootstrap-swift-package", payload["next_step"])

    def test_blocks_when_platform_is_unresolved(self) -> None:
        code, payload = self.run_script(
            "--name",
            "DemoApp",
            "--project-generator",
            "xcodegen",
            "--dry-run",
        )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("supported platform", payload["next_step"])

    def test_blocks_when_generator_is_ask(self) -> None:
        code, payload = self.run_script(
            "--name",
            "DemoApp",
            "--platform",
            "macos",
            "--project-generator",
            "ask",
        )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("Choose --project-generator", payload["next_step"])

    def test_xcode_path_is_guided_only(self) -> None:
        code, payload = self.run_script(
            "--name",
            "DemoApp",
            "--platform",
            "macos",
            "--project-generator",
            "xcode",
        )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("standard Xcode GUI creation path", payload["stderr"])

    def test_xcodegen_path_blocks_when_xcodegen_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env = dict(os.environ)
            env["XCODEGEN_BIN"] = "/definitely-missing-xcodegen"
            code, payload = self.run_script(
                "--name",
                "DemoApp",
                "--destination",
                tmpdir,
                "--platform",
                "macos",
                "--project-generator",
                "xcodegen",
                env=env,
            )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("Install XcodeGen", payload["next_step"])

    def test_xcodegen_path_can_succeed_with_fake_tools(self) -> None:
        xcodegen_body = """#!/bin/sh
if [ "$1" = "generate" ]; then
  spec="project.yml"
  while [ "$#" -gt 0 ]; do
    if [ "$1" = "--spec" ]; then
      shift
      spec="$1"
    fi
    shift
  done
  name="$(sed -n 's/^name: //p' "$spec" | head -n1)"
  mkdir -p "$name.xcodeproj"
  exit 0
fi
exit 1
"""
        xcodebuild_body = """#!/bin/sh
if [ "$1" = "-list" ]; then
  echo "Information about project"
  exit 0
fi
exit 1
"""
        with tempfile.TemporaryDirectory() as tmpdir, fake_tools_in_path(("xcodegen", xcodegen_body), ("xcodebuild", xcodebuild_body)) as env:
            code, payload = self.run_script(
                "--name",
                "DemoApp",
                "--destination",
                tmpdir,
                "--platform",
                "macos",
                "--project-generator",
                "xcodegen",
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            target = Path(payload["resolved_path"])
            self.assertTrue((target / "project.yml").exists())
            self.assertTrue((target / "AGENTS.md").exists())
            agents_text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("xcode-build-run-workflow", agents_text)
            self.assertIn("xcode-testing-workflow", agents_text)
            self.assertIn(".xctestplan", agents_text)
            self.assertIn("project membership, target membership, build phases, and resource inclusion", agents_text)
            self.assertIn("Never edit `.pbxproj` files directly.", agents_text)
            self.assertTrue((target / "DemoApp.xcodeproj").exists())
            self.assertTrue((target / "scripts" / "repo-maintenance" / "validate-all.sh").exists())
            self.assertTrue((target / "scripts" / "repo-maintenance" / "release.sh").exists())
            self.assertTrue((target / "scripts" / "repo-maintenance" / "config" / "profile.env").exists())
            self.assertIn(
                'REPO_MAINTENANCE_PROFILE="xcode-app"',
                (target / "scripts" / "repo-maintenance" / "config" / "profile.env").read_text(encoding="utf-8"),
            )
            self.assertTrue((target / ".github" / "workflows" / "validate-repo-maintenance.yml").exists())
            self.assertEqual(payload["validation_result"], "passed (xcodebuild -list)")
