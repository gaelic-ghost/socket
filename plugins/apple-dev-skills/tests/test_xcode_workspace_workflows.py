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

    def test_extension_is_an_apps_peer_with_explicit_host_embedding(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(BOOTSTRAP, "--name", "Product", "--file-prefix", "PRD", "--destination", tmpdir, "--skip-validation")
            self.assertEqual(code, 0, payload)
            root = Path(payload["workspace_root"])
            code, payload = run_script(
                BOOTSTRAP,
                "--operation", "add-component",
                "--repo-root", str(root),
                "--component-kind", "extension",
                "--component-name", "ProductShareExtension",
                "--platform", "ios",
                "--host-target", "ProductiOS",
                "--extension-product-type", "app-extension",
                "--extension-point-identifier", "com.apple.share-services",
            )
            self.assertEqual(code, 0, payload)
            self.assertTrue((root / "Apps/ProductShareExtension/target.yml").is_file())
            self.assertFalse((root / "Extensions").exists())
            host_spec = (root / "Apps/ProductiOS/target.yml").read_text(encoding="utf-8")
            self.assertIn("- target: ProductShareExtension", host_spec)
            self.assertIn("embed: true", host_spec)
            extension_spec = (root / "Apps/ProductShareExtension/target.yml").read_text(encoding="utf-8")
            self.assertIn("type: app-extension", extension_spec)
            self.assertIn("Apps/ProductShareExtension/Sources", extension_spec)

    def test_extension_addition_blocks_without_explicit_host_and_extension_point(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, payload = run_script(BOOTSTRAP, "--name", "Product", "--destination", tmpdir, "--skip-validation")
            self.assertEqual(code, 0, payload)
            code, payload = run_script(
                BOOTSTRAP,
                "--operation", "add-component",
                "--repo-root", payload["workspace_root"],
                "--component-kind", "extension",
                "--component-name", "ProductShareExtension",
                "--platform", "ios",
            )
            self.assertEqual(code, 1)
            self.assertIn("--host-target", payload["stderr"])

    def test_adopt_inventories_swiftpm_library_without_xcode_prerequisites(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Sources/Library").mkdir(parents=True)
            (root / "Sources/Library/Library.swift").write_text("public enum Library {}\n", encoding="utf-8")
            (root / "Package.swift").write_text(
                '// swift-tools-version: 6.2\nimport PackageDescription\nlet package = Package(name: "Library", products: [.library(name: "Library", targets: ["Library"])], targets: [.target(name: "Library")])\n',
                encoding="utf-8",
            )
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir)
            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["components"][0]["kind"], "library")
            self.assertEqual(payload["components"][0]["proposed_destination"], "Packages/Library")
            self.assertFalse((root / "project.yml").exists(), "inventory must not mutate")
            self.assertNotIn("repo_shape", json.dumps(payload))

    def test_adopt_stages_reviewed_library_map_without_deleting_original_project_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Sources/Library").mkdir(parents=True)
            (root / "Sources/Library/Library.swift").write_text("public enum Library {}\n", encoding="utf-8")
            (root / "Package.swift").write_text(
                '// swift-tools-version: 6.2\nimport PackageDescription\nlet package = Package(name: "Library", products: [.library(name: "Library", targets: ["Library"])], targets: [.target(name: "Library")])\n',
                encoding="utf-8",
            )
            code, inventory = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir)
            self.assertEqual(code, 0, inventory)
            mapping_path = root / "reviewed-adoption.json"
            mapping_path.write_text(json.dumps(inventory["adoption_map"]), encoding="utf-8")
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir, "--adoption-map", str(mapping_path), "--apply")
            self.assertEqual(code, 0, payload)
            self.assertTrue((root / "Packages/Library/Package.swift").is_file())
            self.assertTrue((root / "Packages/Library/Sources/Library/Library.swift").is_file())
            self.assertTrue((root / ".socket/adoption/original-inventory.json").is_file())
            self.assertTrue((root / ".socket/adoption/equivalence-report.json").is_file())
            self.assertTrue((root / ".socket/adoption-candidate/Library.xcodeproj/project.pbxproj").is_file())

    def test_adopt_discovers_hummingbird_and_vapor_services_independently(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            for name, dependency in (("API", "Hummingbird"), ("Worker", "Vapor")):
                package = root / name
                (package / f"Sources/{name}").mkdir(parents=True)
                (package / f"Sources/{name}/main.swift").write_text("print(\"service\")\n", encoding="utf-8")
                (package / "Package.swift").write_text(
                    f'// swift-tools-version: 6.2\nimport PackageDescription\n// {dependency}\nlet package = Package(name: "{name}", products: [.executable(name: "{name}", targets: ["{name}"])], targets: [.executableTarget(name: "{name}")])\n',
                    encoding="utf-8",
                )
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir)
            self.assertEqual(code, 0, payload)
            services = {item["name"]: item for item in payload["components"]}
            self.assertEqual(services["API"]["proposed_destination"], "Services/API")
            self.assertEqual(services["API"]["product_type"], "hummingbird")
            self.assertEqual(services["Worker"]["product_type"], "vapor")

    def test_adopt_blocks_ambiguous_extension_host_before_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            project = root / "Legacy.xcodeproj"
            project.mkdir()
            project.joinpath("project.pbxproj").write_text(
                """A = { isa = PBXNativeTarget; name = FirstApp; productType = \"com.apple.product-type.application\"; };
B = { isa = PBXNativeTarget; name = SecondApp; productType = \"com.apple.product-type.application\"; };
C = { isa = PBXNativeTarget; name = ShareExtension; productType = \"com.apple.product-type.app-extension\"; };
SDKROOT = iphoneos;
""",
                encoding="utf-8",
            )
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir)
            self.assertEqual(code, 1)
            self.assertIn("extension host target", " ".join(payload["unresolved"]))
            self.assertFalse((root / "project.yml").exists())

    def test_adopt_inventories_hand_managed_app_settings_resources_and_schemes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            project = root / "Legacy.xcodeproj"
            (project / "xcshareddata/xcschemes").mkdir(parents=True)
            project.joinpath("project.pbxproj").write_text(
                """A = {
  isa = PBXNativeTarget;
  name = LegacyApp;
  productType = "com.apple.product-type.application";
};
SDKROOT = iphoneos;
PRODUCT_BUNDLE_IDENTIFIER = com.example.legacy;
CODE_SIGN_ENTITLEMENTS = Sources/Legacy.entitlements;
SWIFT_VERSION = 6.0;
""",
                encoding="utf-8",
            )
            (project / "xcshareddata/xcschemes/LegacyApp.xcscheme").write_text("<Scheme/>\n", encoding="utf-8")
            (root / "Sources/Resources/Assets.xcassets").mkdir(parents=True)
            (root / "Sources/Resources/Info.plist").write_text("<plist/>\n", encoding="utf-8")
            (root / "Sources/Legacy.entitlements").write_text("<plist/>\n", encoding="utf-8")
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir)
            self.assertEqual(code, 0, payload)
            app = next(item for item in payload["components"] if item["name"] == "LegacyApp")
            self.assertEqual(app["proposed_destination"], "Apps/LegacyApp")
            self.assertEqual(app["platform"], "ios")
            self.assertIn("PRODUCT_BUNDLE_IDENTIFIER", payload["inventory"]["pbx_settings_to_promote"])
            self.assertIn("Sources/Resources/Assets.xcassets", payload["inventory"]["asset_catalogs"])
            self.assertIn("Legacy.xcodeproj/xcshareddata/xcschemes/LegacyApp.xcscheme", payload["inventory"]["schemes"])

    def test_adopt_inventories_old_xcodegen_flat_app_without_repo_classification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "Sources").mkdir()
            (root / "Sources/App.swift").write_text("import SwiftUI\n", encoding="utf-8")
            (root / "project.yml").write_text(
                """name: Legacy
targets:
  LegacyApp:
    type: application
    platform: iOS
    sources:
      - Sources
""",
                encoding="utf-8",
            )
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir)
            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["components"][0]["name"], "LegacyApp")
            self.assertEqual(payload["components"][0]["owned_paths"], ["Sources"])
            serialized = json.dumps(payload)
            self.assertNotIn("repo_shape", serialized)
            self.assertNotIn("migration_path", serialized)
            self.assertFalse((root / "Apps").exists())

    def test_adopt_inventories_mixed_components_independently(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            project = root / "Product.xcodeproj"
            project.mkdir()
            project.joinpath("project.pbxproj").write_text(
                """A = { isa = PBXNativeTarget; name = ProductApp; productType = "com.apple.product-type.application"; };
SDKROOT = macosx;
""",
                encoding="utf-8",
            )
            for name, executable in (("ProductCore", False), ("ProductAPI", True)):
                package = root / "LegacyComponents" / name
                (package / f"Sources/{name}").mkdir(parents=True)
                product = f'.executable(name: "{name}", targets: ["{name}"])' if executable else f'.library(name: "{name}", targets: ["{name}"])'
                target = f'.executableTarget(name: "{name}")' if executable else f'.target(name: "{name}")'
                (package / "Package.swift").write_text(
                    f'// swift-tools-version: 6.2\nimport PackageDescription\nlet package = Package(name: "{name}", products: [{product}], targets: [{target}])\n',
                    encoding="utf-8",
                )
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir)
            self.assertEqual(code, 0, payload)
            destinations = {item["name"]: item["proposed_destination"] for item in payload["components"]}
            self.assertEqual(destinations["ProductApp"], "Apps/ProductApp")
            self.assertEqual(destinations["ProductCore"], "Packages/ProductCore")
            self.assertEqual(destinations["ProductAPI"], "Services/ProductAPI")

    def test_adopt_preserves_test_target_and_test_plan_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            project = root / "Product.xcodeproj"
            project.mkdir()
            project.joinpath("project.pbxproj").write_text(
                """A = { isa = PBXNativeTarget; name = ProductApp; productType = "com.apple.product-type.application"; };
B = { isa = PBXNativeTarget; name = ProductAppTests; productType = "com.apple.product-type.bundle.unit-test"; };
SDKROOT = iphoneos;
""",
                encoding="utf-8",
            )
            (root / "Product.xctestplan").write_text('{"testTargets": []}\n', encoding="utf-8")
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", tmpdir)
            self.assertEqual(code, 0, payload)
            tests = next(item for item in payload["components"] if item["kind"] == "test")
            self.assertEqual(tests["proposed_destination"], "Apps/ProductAppTests")
            self.assertIn("Product.xctestplan", payload["inventory"]["test_plans"])

    def test_adopt_reports_already_canonical_workspace_without_migration(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            code, created = run_script(BOOTSTRAP, "--name", "Product", "--destination", tmpdir, "--skip-validation")
            self.assertEqual(code, 0, created)
            code, payload = run_script(BOOTSTRAP, "--operation", "adopt", "--repo-root", created["workspace_root"])
            self.assertEqual(code, 0, payload)
            self.assertFalse(payload["migration_required"])

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
