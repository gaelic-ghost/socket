from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/bootstrap-swift-package/scripts/run_workflow.py"


def write_config(tmpdir: str, skill: str, settings: dict) -> None:
    target = Path(tmpdir) / skill / "customization.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schemaVersion: 1", "isCustomized: true", "settings:"]
    for key, value in settings.items():
        if isinstance(value, bool):
            raw = "true" if value else "false"
        elif isinstance(value, int):
            raw = str(value)
        else:
            raw = f'"{value}"'
        lines.append(f"  {key}: {raw}")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


@contextmanager
def fake_swift_in_path(script_body: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        bin_dir = Path(tmpdir) / "bin"
        bin_dir.mkdir()
        swift_path = bin_dir / "swift"
        swift_path.write_text(script_body, encoding="utf-8")
        swift_path.chmod(0o755)
        env = dict(os.environ)
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        yield env


class BootstrapWorkflowTests(unittest.TestCase):
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
                "bootstrap-swift-package",
                {
                    "defaultVersionProfile": "latest-major",
                    "defaultTestingMode": "xctest",
                    "initializeGit": False,
                    "copyAgentsMd": False,
                },
            )
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script("--name", "DemoPkg", "--dry-run", env=env)
            self.assertEqual(code, 0)
            self.assertEqual(payload["normalized_inputs"]["type"], "library")
            self.assertEqual(payload["normalized_inputs"]["platform"], "multiplatform")
            self.assertEqual(payload["normalized_inputs"]["version_profile"], "latest-major")
            self.assertEqual(payload["normalized_inputs"]["testing_mode"], "xctest")
            self.assertFalse(payload["normalized_inputs"]["initialize_git"])
            self.assertFalse(payload["normalized_inputs"]["copy_agents_md"])
            self.assertEqual(payload["testing_strategy"], "init-flags")
            self.assertIn("--testing-mode", payload["command"])
            self.assertIn("xctest", payload["command"])
            self.assertIn("--skip-git-init", payload["command"])
            self.assertIn("--skip-copy-agents", payload["command"])

    def test_explicit_args_override_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            write_config(
                tmpdir,
                "bootstrap-swift-package",
                {
                    "defaultVersionProfile": "current-minus-one",
                },
            )
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--type",
                "tool",
                "--platform",
                "mobile",
                "--version-profile",
                "current-minus-two",
                "--testing-mode",
                "swift-testing",
                "--dry-run",
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["normalized_inputs"]["type"], "tool")
            self.assertEqual(payload["normalized_inputs"]["platform"], "mobile")
            self.assertEqual(payload["normalized_inputs"]["version_profile"], "current-minus-two")
            self.assertEqual(payload["normalized_inputs"]["testing_mode"], "swift-testing")
            self.assertEqual(payload["testing_strategy"], "init-flags")

    def test_wrapper_normalizes_shell_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            blocking_file = Path(tmpdir) / "not-a-directory"
            blocking_file.write_text("x", encoding="utf-8")
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--destination",
                str(blocking_file),
                "--skip-validation",
            )
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn("Resolve the bootstrap prerequisite", payload["next_step"])

    def test_dry_run_rejects_invalid_testing_mode(self) -> None:
        code, payload = self.run_script(
            "--name",
            "DemoPkg",
            "--testing-mode",
            "unsupported",
            "--dry-run",
        )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("supported testing mode", payload["next_step"])

    def test_dry_run_rejects_invalid_package_type(self) -> None:
        code, payload = self.run_script(
            "--name",
            "DemoPkg",
            "--type",
            "bogus",
            "--dry-run",
        )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("input validation issue", payload["next_step"])
        self.assertIn("--type must be", payload["stderr"])

    def test_dry_run_rejects_invalid_version_profile(self) -> None:
        code, payload = self.run_script(
            "--name",
            "DemoPkg",
            "--version-profile",
            "bogus",
            "--dry-run",
        )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("input validation issue", payload["next_step"])
        self.assertIn("--version-profile must be", payload["stderr"])

    @unittest.skipUnless(shutil.which("swift"), "swift is required for testing strategy coverage")
    def test_dry_run_uses_default_template_strategy_for_xctest_without_selection_flags(self) -> None:
        real_swift = shutil.which("swift")
        assert real_swift is not None
        script_body = f"""#!/bin/sh
if [ "$1" = "--version" ]; then
  cat <<'EOF'
Apple Swift version 5.10 (swift-5.10-RELEASE)
Target: arm64-apple-macosx14.0
EOF
  exit 0
fi
if [ "$1" = "package" ] && [ "$2" = "init" ] && [ "$3" = "--help" ]; then
  cat <<'EOF'
OVERVIEW: Initialize a new package.

USAGE: swift package init [--type <type>] [--name <name>]
EOF
  exit 0
fi
exec "{real_swift}" "$@"
"""
        with fake_swift_in_path(script_body) as env:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--testing-mode",
                "xctest",
                "--dry-run",
                env=env,
            )
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["testing_strategy"], "default-template")

    @unittest.skipUnless(shutil.which("swift"), "swift is required for testing strategy coverage")
    def test_dry_run_blocks_xctest_when_partial_selection_flags_cannot_force_it(self) -> None:
        real_swift = shutil.which("swift")
        assert real_swift is not None
        script_body = f"""#!/bin/sh
if [ "$1" = "--version" ]; then
  cat <<'EOF'
Apple Swift version 6.0 (swift-6.0-RELEASE)
Target: arm64-apple-macosx15.0
EOF
  exit 0
fi
if [ "$1" = "package" ] && [ "$2" = "init" ] && [ "$3" = "--help" ]; then
  cat <<'EOF'
OVERVIEW: Initialize a new package.

USAGE: swift package init [--type <type>] [--enable-swift-testing] [--name <name>]
EOF
  exit 0
fi
exec "{real_swift}" "$@"
"""
        with fake_swift_in_path(script_body) as env:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--testing-mode",
                "xctest",
                "--dry-run",
                env=env,
            )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("cannot force XCTest mode", payload["stderr"])

    @unittest.skipUnless(shutil.which("swift"), "swift is required for toolchain compatibility coverage")
    def test_dry_run_rejects_unsupported_swift_testing_selection(self) -> None:
        real_swift = shutil.which("swift")
        assert real_swift is not None
        script_body = f"""#!/bin/sh
if [ "$1" = "--version" ]; then
  exec "{real_swift}" "$@"
fi
if [ "$1" = "package" ] && [ "$2" = "init" ] && [ "$3" = "--help" ]; then
  cat <<'EOF'
OVERVIEW: Initialize a new package.

USAGE: swift package init [--type <type>] [--enable-xctest] [--disable-xctest] [--name <name>]
EOF
  exit 0
fi
exec "{real_swift}" "$@"
"""
        with fake_swift_in_path(script_body) as env:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--testing-mode",
                "swift-testing",
                "--dry-run",
                env=env,
            )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("toolchain selection issue", payload["next_step"])
        self.assertIn("does not support Swift Testing", payload["stderr"])

    @unittest.skipUnless(shutil.which("swift"), "swift is required for toolchain floor coverage")
    def test_dry_run_accepts_swift_5_10_floor(self) -> None:
        real_swift = shutil.which("swift")
        assert real_swift is not None
        script_body = f"""#!/bin/sh
if [ "$1" = "--version" ]; then
  cat <<'EOF'
Apple Swift version 5.10 (swift-5.10-RELEASE)
Target: arm64-apple-macosx14.0
EOF
  exit 0
fi
if [ "$1" = "package" ] && [ "$2" = "init" ] && [ "$3" = "--help" ]; then
  exec "{real_swift}" "$@"
fi
exec "{real_swift}" "$@"
"""
        with fake_swift_in_path(script_body) as env:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--testing-mode",
                "xctest",
                "--dry-run",
                env=env,
            )
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "success")

    @unittest.skipUnless(shutil.which("swift"), "swift is required for toolchain floor coverage")
    def test_dry_run_blocks_swift_5_9_toolchain(self) -> None:
        real_swift = shutil.which("swift")
        assert real_swift is not None
        script_body = f"""#!/bin/sh
if [ "$1" = "--version" ]; then
  cat <<'EOF'
Apple Swift version 5.9.2 (swift-5.9.2-RELEASE)
Target: arm64-apple-macosx14.0
EOF
  exit 0
fi
if [ "$1" = "package" ] && [ "$2" = "init" ] && [ "$3" = "--help" ]; then
  exec "{real_swift}" "$@"
fi
exec "{real_swift}" "$@"
"""
        with fake_swift_in_path(script_body) as env:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--dry-run",
                env=env,
            )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("Swift 5.10+", payload["stderr"])

    @unittest.skipUnless(shutil.which("swift"), "swift is required for toolchain floor coverage")
    def test_dry_run_blocks_unparseable_swift_version(self) -> None:
        real_swift = shutil.which("swift")
        assert real_swift is not None
        script_body = f"""#!/bin/sh
if [ "$1" = "--version" ]; then
  echo "mystery toolchain output"
  exit 0
fi
if [ "$1" = "package" ] && [ "$2" = "init" ] && [ "$3" = "--help" ]; then
  exec "{real_swift}" "$@"
fi
exec "{real_swift}" "$@"
"""
        with fake_swift_in_path(script_body) as env:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--dry-run",
                env=env,
            )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("Unable to parse", payload["stderr"])

    @unittest.skipUnless(shutil.which("swift"), "swift is required for failure-path coverage")
    def test_runtime_reports_failed_when_package_init_fails(self) -> None:
        real_swift = shutil.which("swift")
        assert real_swift is not None
        script_body = f"""#!/bin/sh
if [ "$1" = "package" ] && [ "$2" = "init" ] && [ "$3" = "--help" ]; then
  exec "{real_swift}" "$@"
fi
if [ "$1" = "package" ] && [ "$2" = "init" ]; then
  echo "Simulated swift package init failure." >&2
  exit 1
fi
exec "{real_swift}" "$@"
"""
        with tempfile.TemporaryDirectory() as tmpdir, fake_swift_in_path(script_body) as env:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--destination",
                tmpdir,
                "--skip-validation",
                env=env,
            )
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "failed")
        self.assertIn("Fix the bootstrap error", payload["next_step"])

    @unittest.skipUnless(shutil.which("swift"), "swift is required for XCTest bootstrap coverage")
    def test_executable_bootstrap_creates_xctest_test_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--type",
                "executable",
                "--testing-mode",
                "xctest",
                "--destination",
                tmpdir,
                "--skip-validation",
            )
            self.assertEqual(code, 0)
            package_dir = Path(payload["resolved_path"])
            test_file = package_dir / "Tests" / "DemoPkgTests" / "DemoPkgTests.swift"
            self.assertTrue(test_file.is_file())
            test_text = test_file.read_text(encoding="utf-8")
            self.assertIn("import XCTest", test_text)
            self.assertIn("XCTestCase", test_text)
            manifest_text = (package_dir / "Package.swift").read_text(encoding="utf-8")
            self.assertIn(".executableTarget(", manifest_text)
            self.assertIn(".testTarget(", manifest_text)
            self.assertIn("swiftLanguageModes: [.v6]", manifest_text)

    @unittest.skipUnless(shutil.which("swift"), "swift is required for end-to-end bootstrap success")
    def test_wrapper_normalizes_shell_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--destination",
                tmpdir,
                "--skip-validation",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertTrue(payload["resolved_path"].endswith("DemoPkg"))
            manifest_text = (Path(payload["resolved_path"]) / "Package.swift").read_text(encoding="utf-8")
            self.assertIn("swiftLanguageModes: [.v6]", manifest_text)
            self.assertEqual(payload["testing_mode"], "swift-testing")
            self.assertEqual(payload["testing_strategy"], "init-flags")
            self.assertEqual(payload["swift_toolchain"], "6.3")
            package_dir = Path(payload["resolved_path"])
            self.assertTrue((package_dir / ".swiftformat").is_file())
            self.assertTrue((package_dir / "scripts" / "repo-maintenance" / "validate-all.sh").is_file())
            self.assertTrue((package_dir / "scripts" / "repo-maintenance" / "release.sh").is_file())
            self.assertTrue((package_dir / "scripts" / "repo-maintenance" / "hooks" / "pre-commit.sample").is_file())
            self.assertTrue((package_dir / "scripts" / "repo-maintenance" / "config" / "profile.env").is_file())
            self.assertIn(
                'REPO_MAINTENANCE_PROFILE="swift-package"',
                (package_dir / "scripts" / "repo-maintenance" / "config" / "profile.env").read_text(encoding="utf-8"),
            )
            self.assertTrue((package_dir / ".github" / "workflows" / "validate-repo-maintenance.yml").is_file())

    @unittest.skipUnless(shutil.which("swift"), "swift is required for executable bootstrap coverage")
    def test_executable_bootstrap_creates_swift_testing_test_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script(
                "--name",
                "DemoPkg",
                "--type",
                "executable",
                "--destination",
                tmpdir,
                "--skip-validation",
            )
            self.assertEqual(code, 0)
            package_dir = Path(payload["resolved_path"])
            test_file = package_dir / "Tests" / "DemoPkgTests" / "DemoPkgTests.swift"
            self.assertTrue(test_file.is_file())
            test_text = test_file.read_text(encoding="utf-8")
            self.assertIn("import Testing", test_text)
            self.assertIn("@Test", test_text)

    @unittest.skipUnless(shutil.which("swift"), "swift is required for tool bootstrap coverage")
    def test_tool_bootstrap_captures_argument_parser_and_platforms(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = self.run_script(
                "--name",
                "DemoTool",
                "--type",
                "tool",
                "--platform",
                "mac",
                "--version-profile",
                "latest-major",
                "--destination",
                tmpdir,
                "--skip-validation",
            )
            self.assertEqual(code, 0)
            package_dir = Path(payload["resolved_path"])
            manifest_text = (package_dir / "Package.swift").read_text(encoding="utf-8")
            self.assertIn("swift-argument-parser", manifest_text)
            self.assertIn('.macOS("26.0")', manifest_text)
            self.assertNotIn('.iOS("26.0")', manifest_text)
            self.assertTrue((package_dir / ".git").is_dir())
            self.assertTrue((package_dir / "AGENTS.md").is_file())
            agents_text = (package_dir / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("swift-package-build-run-workflow", agents_text)
            self.assertIn("swift-package-testing-workflow", agents_text)
            self.assertIn("Bundle.module", agents_text)
            self.assertIn(".xctestplan", agents_text)
            self.assertIn(".metallib", agents_text)
            self.assertIn("Debug and Release", agents_text)
            self.assertIn("GitHub URL, or other real remote repository requirements", agents_text)
            self.assertIn("do not commit machine-local dependency paths", agents_text)
            self.assertIn("Package.resolved", agents_text)
            self.assertIn("one change when possible", agents_text)
            self.assertTrue((package_dir / "scripts" / "repo-maintenance" / "sync-shared.sh").is_file())


if __name__ == "__main__":
    unittest.main()
