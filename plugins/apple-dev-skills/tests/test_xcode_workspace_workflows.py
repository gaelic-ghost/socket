from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "skills/bootstrap-xcode-workspace/scripts/run_workflow.py"


def run_script(script: Path, *args: str) -> tuple[int, dict]:
    env = dict(os.environ)
    env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "apple-dev-skills-uv-cache"))
    process = subprocess.run(["uv", "run", str(script), *args], capture_output=True, check=False, env=env, text=True)
    return process.returncode, json.loads(process.stdout)


class XcodeWorkspaceWorkflowTests(unittest.TestCase):
    def test_bootstrap_defaults_to_one_root_project_and_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(BOOTSTRAP, "--name", "Product", "--destination", tmpdir, "--dry-run")
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["normalized_inputs"]["platforms"], ["ios", "macos"])
            self.assertIn("root XcodeGen project", " ".join(payload["actions"]))
            self.assertTrue(payload["workspace_path"].endswith("Product.xcworkspace"))
            self.assertTrue(payload["project_path"].endswith("Product.xcodeproj"))

    def test_bootstrap_supports_package_first_without_a_second_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(
                BOOTSTRAP,
                "--name", "Product",
                "--destination", tmpdir,
                "--component-kind", "library",
                "--component-name", "ProductAnalytics",
                "--dry-run",
            )
            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["normalized_inputs"]["platforms"], [])
            self.assertIn("Packages/ProductAnalytics", " ".join(payload["actions"]))

    def test_bootstrap_creates_one_project_target_specs_shared_layers_and_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(BOOTSTRAP, "--name", "Product", "--file-prefix", "PRD", "--destination", tmpdir, "--skip-validation")
            self.assertEqual(code, 0, payload)
            root = Path(payload["workspace_root"])
            self.assertTrue((root / "Product.xcworkspace/contents.xcworkspacedata").is_file())
            self.assertTrue((root / "Product.xcodeproj/project.pbxproj").is_file())
            self.assertTrue((root / "project.yml").is_file())
            self.assertTrue((root / "Apps/apps-shared.yml").is_file())
            self.assertTrue((root / "Apps/Apps-shared.xcconfig").is_file())
            self.assertTrue((root / "Apps/AGENTS.md").is_file())
            self.assertTrue((root / "Packages/packages-shared.yml").is_file())
            self.assertTrue((root / "Packages/AGENTS.md").is_file())
            self.assertTrue((root / "Packages/ProductCore/Package.swift").is_file())
            self.assertTrue((root / "Services/services-shared.yml").is_file())
            self.assertTrue((root / "Services/AGENTS.md").is_file())
            self.assertTrue((root / "AGENTS.md").is_file())
            self.assertTrue((root / "CONTRIBUTING.md").is_file())
            self.assertTrue((root / "Justfile").is_file())
            self.assertTrue((root / ".githooks/pre-commit").is_file())
            root_spec = (root / "project.yml").read_text(encoding="utf-8")
            self.assertIn("Apps/apps-shared.yml", root_spec)
            self.assertIn("Packages/packages-shared.yml", root_spec)
            self.assertIn("Services/services-shared.yml", root_spec)
            self.assertIn("projectFormat: xcode16_3", root_spec)
            self.assertIn("AppStore: release", root_spec)
            self.assertIn('iOS: "26.1"', root_spec)
            for target in ("ProductiOS", "ProductmacOS"):
                self.assertTrue((root / f"Apps/{target}/target.yml").is_file())
                self.assertTrue((root / f"Apps/{target}/Configurations/App.xcconfig").is_file())
                self.assertTrue((root / f"Apps/{target}/Configurations/Version.xcconfig").is_file())
                self.assertTrue((root / f"Apps/{target}/Resources/Info.plist").is_file())
                self.assertTrue((root / f"Apps/{target}/Resources/{target}.entitlements").is_file())
                self.assertTrue((root / f"Apps/{target}Tests/Sources/{target}Tests.swift").is_file())
                self.assertTrue((root / f"Apps/{target}UITests/Sources/{target}UITests.swift").is_file())
                self.assertFalse((root / f"Apps/{target}Tests/Configurations").exists())
                target_spec = (root / f"Apps/{target}/target.yml").read_text(encoding="utf-8")
                self.assertIn(f"{target} All Tests", target_spec)
                self.assertIn("SWIFT_DEFAULT_ACTOR_ISOLATION: MainActor", target_spec)
            manifest = (root / "Packages/ProductCore/Package.swift").read_text(encoding="utf-8")
            self.assertIn("swift-tools-version: 6.2", manifest)
            self.assertIn("ProductDomain", manifest)
            self.assertIn("ProductServices", manifest)
            self.assertTrue((root / "Scripts/repo-maintenance/validate-all.sh").is_file())

    def test_bootstrap_discovers_repository_runner_from_versioned_plugin_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_root = Path(tmpdir) / "cache" / "socket"
            apple_root = cache_root / "apple-dev-skills" / "9.34.0"
            repository_root = cache_root / "repository-skills" / "9.34.0"
            shutil.copytree(
                ROOT / "skills/bootstrap-xcode-workspace",
                apple_root / "skills/bootstrap-xcode-workspace",
            )
            shutil.copytree(
                ROOT.parent / "repository-skills",
                repository_root,
                ignore=shutil.ignore_patterns(".venv", ".pytest_cache", ".ruff_cache", "__pycache__"),
            )
            cache_script = apple_root / "skills/bootstrap-xcode-workspace/scripts/run_workflow.py"
            destination = Path(tmpdir) / "products"
            code, payload = run_script(
                cache_script,
                "--name",
                "CachedProduct",
                "--file-prefix",
                "CCH",
                "--destination",
                str(destination),
                "--skip-validation",
            )
            self.assertEqual(code, 0, payload)
            self.assertTrue((destination / "CachedProduct/Scripts/repo-maintenance/validate-all.sh").is_file())

    def test_bootstrap_rejects_existing_file_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "Product").write_text("occupied", encoding="utf-8")
            code, payload = run_script(BOOTSTRAP, "--name", "Product", "--destination", tmpdir)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn("already contains files", payload["stderr"])

    def test_bootstrap_rejects_noncanonical_platform_or_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(BOOTSTRAP, "--name", "Product", "--destination", tmpdir, "--platforms", "watchos", "--dry-run")
            self.assertEqual(code, 0)
            self.assertEqual(payload["normalized_inputs"]["platforms"], ["watchos"])
            code, payload = run_script(BOOTSTRAP, "--name", "Product", "--destination", tmpdir, "--file-prefix", "no")
            self.assertEqual(code, 1)
            self.assertIn("three uppercase", payload["stderr"])

    def test_existing_workspace_alignment_preserves_local_content_and_adds_just_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Product.xcworkspace").mkdir()
            (root / "Product.xcodeproj").mkdir()
            (root / "project.yml").write_text("name: Product\ninclude:\noptions:\n  createIntermediateGroups: true\n", encoding="utf-8")
            (root / "Apps/ProductiOS").mkdir(parents=True)
            (root / "Apps/apps-shared.yml").write_text("targetTemplates: {}\n", encoding="utf-8")
            (root / "Apps/Apps-shared.xcconfig").write_text("SWIFT_VERSION = 6.0\n", encoding="utf-8")
            (root / "Apps/ProductiOS/target.yml").write_text("targets: {}\n", encoding="utf-8")
            (root / "Packages/ProductCore").mkdir(parents=True)
            (root / "Packages/packages-shared.yml").write_text("packages: {}\n", encoding="utf-8")
            (root / "Packages/ProductCore/Package.swift").write_text("// swift-tools-version: 6.0\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Local\n\nKeep this.\n", encoding="utf-8")
            (root / "Justfile").write_text("local:\n  echo local\n", encoding="utf-8")
            code, payload = run_script(BOOTSTRAP, "--operation", "align", "--repo-root", tmpdir)
            self.assertEqual(code, 0, payload)
            self.assertIn("Justfile", " ".join(payload["actions"]))
            self.assertIn(".socket/managed/align.sh", " ".join(payload["actions"]))
            self.assertIn("Keep this.", (root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("socket-managed:begin", (root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("local:", (root / "Justfile").read_text(encoding="utf-8"))
            self.assertIn("socket-managed:begin just-recipes", (root / "Justfile").read_text(encoding="utf-8"))
            self.assertTrue((root / ".socket/managed/align.sh").is_file())
            self.assertTrue((root / ".githooks/pre-commit").is_file())
            self.assertTrue((root / "Services/services-shared.yml").is_file())
            self.assertIn("Services/services-shared.yml", (root / "project.yml").read_text(encoding="utf-8"))
            aligned = {
                path: (root / path).read_text(encoding="utf-8")
                for path in ("project.yml", "AGENTS.md", "Justfile", "Services/services-shared.yml")
            }
            code, payload = run_script(BOOTSTRAP, "--operation", "align", "--repo-root", tmpdir)
            self.assertEqual(code, 0, payload)
            self.assertEqual(
                aligned,
                {
                    path: (root / path).read_text(encoding="utf-8")
                    for path in aligned
                },
            )

    def test_docs_record_single_root_project_contract(self) -> None:
        bootstrap = (ROOT / "skills/bootstrap-xcode-workspace/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("one root XcodeGen project", bootstrap)
        self.assertIn("Apps-shared.xcconfig", bootstrap)
        self.assertIn("packages-shared.yml", bootstrap)
        self.assertIn("--operation align", bootstrap)
        self.assertIn("--operation add-component", bootstrap)
        self.assertIn("Services/services-shared.yml", bootstrap)

    def test_add_component_does_not_require_repo_conversion(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(BOOTSTRAP, "--name", "Product", "--file-prefix", "PRD", "--destination", tmpdir, "--skip-validation")
            self.assertEqual(code, 0, payload)
            root = Path(payload["workspace_root"])
            code, payload = run_script(
                BOOTSTRAP,
                "--operation", "add-component",
                "--repo-root", str(root),
                "--component-kind", "library",
                "--component-name", "ProductAnalytics",
            )
            self.assertEqual(code, 0, payload)
            self.assertTrue((root / "Packages/ProductAnalytics/Package.swift").is_file())
            self.assertIn("ProductAnalytics", (root / "Packages/packages-shared.yml").read_text(encoding="utf-8"))

    def test_service_component_routes_through_server_adapter(self) -> None:
        adapter = ROOT.parent / "server-side-swift/skills/workspace-service-component/scripts/run_workflow.py"
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Services").mkdir()
            (root / "project.yml").write_text("name: Product\n", encoding="utf-8")
            (root / "Services/services-shared.yml").write_text("packages: {}\n", encoding="utf-8")
            code, payload = run_script(adapter, "--repo-root", tmpdir, "--name", "ProductAPI", "--framework", "hummingbird", "--dry-run")
            self.assertEqual(code, 0, payload)
            self.assertIn("brew", payload["output"]["next_step"].lower() if payload["output"]["next_step"] else "")

    def test_service_package_is_visible_from_permanent_workspace(self) -> None:
        if not shutil.which("xcodegen") or not shutil.which("xcodebuild"):
            self.skipTest("xcodegen and xcodebuild are required")
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(
                BOOTSTRAP,
                "--name", "Product",
                "--file-prefix", "PRD",
                "--destination", tmpdir,
                "--component-kind", "library",
                "--skip-validation",
            )
            self.assertEqual(code, 0, payload)
            root = Path(payload["workspace_root"])
            service = root / "Services/ProductAPI"
            (service / "Sources/ProductAPI").mkdir(parents=True)
            (service / "Package.swift").write_text(
                "// swift-tools-version: 6.2\n"
                "import PackageDescription\n"
                "let package = Package(name: \"ProductAPI\", products: [.executable(name: \"ProductAPI\", targets: [\"ProductAPI\"])], targets: [.executableTarget(name: \"ProductAPI\")])\n",
                encoding="utf-8",
            )
            (service / "Sources/ProductAPI/main.swift").write_text("print(\"ProductAPI\")\n", encoding="utf-8")
            (root / "Services/services-shared.yml").write_text(
                "packages:\n  ProductAPI:\n    path: Services/ProductAPI\n",
                encoding="utf-8",
            )
            generated = subprocess.run(
                ["xcodegen", "generate"], cwd=root, capture_output=True, text=True, check=False
            )
            self.assertEqual(generated.returncode, 0, generated.stderr or generated.stdout)
            listed = subprocess.run(
                ["xcodebuild", "-list", "-workspace", str(root / "Product.xcworkspace")],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(listed.returncode, 0, listed.stderr or listed.stdout)
            self.assertIn("ProductAPI", listed.stdout)
            service_manifest = (service / "Package.swift").read_text(encoding="utf-8")
            code, payload = run_script(
                BOOTSTRAP,
                "--operation", "add-component",
                "--repo-root", str(root),
                "--component-kind", "app",
                "--component-name", "Product",
                "--platform", "ios",
                "--file-prefix", "PRD",
            )
            self.assertEqual(code, 0, payload)
            self.assertTrue((root / "Apps/ProductiOS/target.yml").is_file())
            self.assertEqual(service_manifest, (service / "Package.swift").read_text(encoding="utf-8"))
