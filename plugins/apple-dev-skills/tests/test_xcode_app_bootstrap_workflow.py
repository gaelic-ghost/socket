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
XCODEGEN_TEMPLATE_DIR = ROOT / "templates/xcodegen/swiftui-app"


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
            code, payload = self.run_script("--name", "DemoApp", "--dry-run", env=env)
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
            project_yml = (target / "project.yml").read_text(encoding="utf-8")
            self.assertIn("minimumXcodeGenVersion: 2.45.4", project_yml)
            self.assertIn("projectFormat: xcode16_0", project_yml)
            self.assertIn("defaultSourceDirectoryType: syncedFolder", project_yml)
            self.assertIn("configs:", project_yml)
            self.assertIn("schemes:", project_yml)
            self.assertIn("configFiles:", project_yml)
            self.assertIn("type: syncedFolder", project_yml)
            self.assertIn("- path: Sources", project_yml)
            self.assertIn("- path: Shared", project_yml)
            self.assertIn("- path: Tests", project_yml)
            self.assertNotIn("- path: Sources/App", project_yml)
            self.assertNotIn("- path: Sources/Resources", project_yml)
            self.assertNotIn("- path: Sources/Support", project_yml)
            self.assertNotIn("- path: Tests/DemoAppTests", project_yml)
            self.assertIn("CFBundleShortVersionString: $(MARKETING_VERSION)", project_yml)
            self.assertIn("CFBundleVersion: $(CURRENT_PROJECT_VERSION)", project_yml)
            self.assertIn("Configurations/App-Debug.xcconfig", project_yml)
            self.assertIn("Configurations/Tests-Debug.xcconfig", project_yml)
            self.assertIn("parallelizable: true", project_yml)
            for top_level_dir in ("Sources", "Tests", "Shared", "Extensions", "Configurations", "Scripts", "Packages"):
                self.assertTrue((target / top_level_dir).is_dir(), top_level_dir)
            for source_dir in (
                "Sources/Views/Shared",
                "Sources/Views/macOS",
                "Sources/Views/iOS",
                "Sources/Models",
                "Sources/Services/Consumed",
                "Sources/Services/Internal",
                "Sources/Services/Provided",
            ):
                self.assertTrue((target / source_dir).is_dir(), source_dir)
            for placeholder in ("Shared/.gitkeep", "Extensions/.gitkeep", "Scripts/.gitkeep", "Packages/.gitkeep"):
                self.assertTrue((target / placeholder).exists(), placeholder)
            self.assertTrue((target / "Sources" / "DemoApp.swift").exists())
            self.assertTrue((target / "Sources" / "DemoApp+ViewModel.swift").exists())
            self.assertTrue((target / "Sources" / "Views" / "Shared" / "ContentView.swift").exists())
            self.assertTrue((target / "Sources" / "Views" / "Shared" / "ContentView+Model.swift").exists())
            self.assertTrue((target / "Sources" / "Services" / "Internal" / "DemoAppService.swift").exists())
            self.assertFalse((target / "Sources" / "Controllers").exists())
            self.assertTrue((target / "Sources" / "Support" / "DemoApp.entitlements").exists())
            self.assertTrue((target / "Sources" / "Resources" / "Assets.xcassets" / "Contents.json").exists())
            self.assertTrue(
                (target / "Sources" / "Resources" / "Assets.xcassets" / "AppIcon.appiconset" / "Contents.json").exists()
            )
            self.assertTrue(
                (target / "Sources" / "Resources" / "Assets.xcassets" / "AccentColor.colorset" / "Contents.json").exists()
            )
            self.assertTrue((target / "Configurations" / "Shared.xcconfig").exists())
            self.assertTrue((target / "Configurations" / "App.xcconfig").exists())
            self.assertTrue((target / "Configurations" / "App-Debug.xcconfig").exists())
            self.assertTrue((target / "Configurations" / "App-Release.xcconfig").exists())
            self.assertTrue((target / "Configurations" / "Tests.xcconfig").exists())
            self.assertTrue((target / "Configurations" / "Tests-Debug.xcconfig").exists())
            self.assertTrue((target / "Configurations" / "Tests-Release.xcconfig").exists())
            self.assertIn(
                "PRODUCT_BUNDLE_IDENTIFIER = com.example.DemoApp",
                (target / "Configurations" / "App.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "MARKETING_VERSION = 0.0.1",
                (target / "Configurations" / "App.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "CURRENT_PROJECT_VERSION = 1",
                (target / "Configurations" / "App.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "CODE_SIGN_ENTITLEMENTS = Sources/Support/DemoApp.entitlements",
                (target / "Configurations" / "App.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon",
                (target / "Configurations" / "App.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "ENABLE_APP_SANDBOX[sdk=macosx*] = NO",
                (target / "Configurations" / "App.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "ENABLE_HARDENED_RUNTIME[sdk=macosx*] = NO",
                (target / "Configurations" / "App.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "SWIFT_VERSION = 6.0",
                (target / "Configurations" / "Shared.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "SWIFT_APPROACHABLE_CONCURRENCY = YES",
                (target / "Configurations" / "Shared.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "SWIFT_STRICT_CONCURRENCY = complete",
                (target / "Configurations" / "Shared.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "ENABLE_USER_SCRIPT_SANDBOXING = YES",
                (target / "Configurations" / "Shared.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES",
                (target / "Configurations" / "Shared.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "DEAD_CODE_STRIPPING = YES",
                (target / "Configurations" / "Shared.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                '#include "App.xcconfig"',
                (target / "Configurations" / "App-Debug.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "PRODUCT_BUNDLE_IDENTIFIER = com.example.DemoApp.tests",
                (target / "Configurations" / "Tests.xcconfig").read_text(encoding="utf-8"),
            )
            self.assertIn("xcodegen_template_paths", payload)
            self.assertIn("standard_directory_paths", payload)
            self.assertTrue((target / "AGENTS.md").exists())
            local_environment_path = target / ".codex" / "environments" / "xcode-project.toml"
            self.assertTrue(local_environment_path.exists())
            local_environment_text = local_environment_path.read_text(encoding="utf-8")
            self.assertIn("xcodebuild -scheme DemoApp -derivedDataPath ./DerivedData build", local_environment_text)
            self.assertEqual(payload["local_environment_path"], str(local_environment_path))
            agents_text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("xcode-build-run-workflow", agents_text)
            self.assertIn("xcode-testing-workflow", agents_text)
            self.assertIn("XcodeGen plus synced source folders", agents_text)
            self.assertIn("Use the standard top-level Xcode app repository layout", agents_text)
            self.assertIn("`Shared/` owns reusable source intended to be compiled into the app and extension targets", agents_text)
            self.assertIn("Sources/Views/Shared", agents_text)
            self.assertIn("Sources/Services/Internal", agents_text)
            self.assertIn("WhateverNameApp+ViewModel.swift", agents_text)
            self.assertIn("<ViewName>+Controller.swift", agents_text)
            self.assertIn("A standard app target gets one `Sources` source entry", agents_text)
            self.assertIn("Every native app target must have exactly one app lifecycle entry point", agents_text)
            self.assertIn("Keep XcodeGen specs readable as project structure", agents_text)
            self.assertIn("Keep `.xcconfig` layering explicit", agents_text)
            self.assertIn("CODE_SIGN_ENTITLEMENTS", agents_text)
            self.assertIn("Build Settings UI", agents_text)
            self.assertIn("Before running `xcodegen generate`", agents_text)
            self.assertIn("promote intentional values into the owning tracked source files", agents_text)
            self.assertIn(".xctestplan", agents_text)
            self.assertIn("project membership, target membership, build phases, and resource inclusion", agents_text)
            self.assertIn("Never edit `.pbxproj` files directly.", agents_text)
            self.assertIn("treat that diff as critical project state", agents_text)
            self.assertTrue((target / "DemoApp.xcodeproj").exists())
            self.assertTrue((target / ".swiftformat").exists())
            self.assertTrue((target / "Scripts" / "repo-maintenance" / "validate-all.sh").exists())
            self.assertTrue((target / "Scripts" / "repo-maintenance" / "release.sh").exists())
            self.assertTrue((target / "Scripts" / "repo-maintenance" / "hooks" / "pre-commit.sample").exists())
            self.assertTrue((target / "Scripts" / "repo-maintenance" / "config" / "profile.env").exists())
            self.assertIn(
                'REPO_MAINTENANCE_PROFILE="xcode-app"',
                (target / "Scripts" / "repo-maintenance" / "config" / "profile.env").read_text(encoding="utf-8"),
            )
            self.assertTrue((target / ".github" / "workflows" / "validate-repo-maintenance.yml").exists())
            self.assertEqual(payload["validation_result"], "passed (xcodebuild -list)")

    def test_xcodegen_templates_are_checked_in_as_bootstrap_sources(self) -> None:
        expected_templates = {
            "project.yml.tmpl",
            "Sources/Support/App.entitlements.tmpl",
            "Sources/Resources/Assets.xcassets/Contents.json.tmpl",
            "Sources/Resources/Assets.xcassets/AppIcon.appiconset/Contents.json.tmpl",
            "Sources/Resources/Assets.xcassets/AccentColor.colorset/Contents.json.tmpl",
            "Configurations/Shared.xcconfig.tmpl",
            "Configurations/App.xcconfig.tmpl",
            "Configurations/App-Debug.xcconfig.tmpl",
            "Configurations/App-Release.xcconfig.tmpl",
            "Configurations/Tests.xcconfig.tmpl",
            "Configurations/Tests-Debug.xcconfig.tmpl",
            "Configurations/Tests-Release.xcconfig.tmpl",
        }

        for relative_path in expected_templates:
            self.assertTrue((XCODEGEN_TEMPLATE_DIR / relative_path).is_file(), relative_path)

        project_template = (XCODEGEN_TEMPLATE_DIR / "project.yml.tmpl").read_text(encoding="utf-8")
        self.assertIn("minimumXcodeGenVersion: 2.45.4", project_template)
        self.assertIn("defaultSourceDirectoryType: syncedFolder", project_template)
        self.assertIn("type: syncedFolder", project_template)
        self.assertIn("- path: Sources", project_template)
        self.assertIn("- path: Shared", project_template)
        self.assertIn("- path: Tests", project_template)
        self.assertNotIn("- path: Sources/App", project_template)
        self.assertNotIn("- path: Sources/Resources", project_template)
        self.assertNotIn("- path: Sources/Support", project_template)
        self.assertNotIn("- path: Tests/__APP_NAME__Tests", project_template)
        self.assertIn("CFBundleShortVersionString: $(MARKETING_VERSION)", project_template)
        self.assertIn("CFBundleVersion: $(CURRENT_PROJECT_VERSION)", project_template)
        self.assertIn("schemes:", project_template)
        self.assertIn("configFiles:", project_template)
        self.assertNotIn("/Users/", project_template)
