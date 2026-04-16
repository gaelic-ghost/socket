from __future__ import annotations

import io
import importlib.util
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_MODULES = {
    "xcode-app-project-workflow": ROOT / "skills/xcode-app-project-workflow/scripts/customization_config.py",
    "xcode-build-run-workflow": ROOT / "skills/xcode-build-run-workflow/scripts/customization_config.py",
    "xcode-testing-workflow": ROOT / "skills/xcode-testing-workflow/scripts/customization_config.py",
    "author-swift-docc-docs": ROOT / "skills/author-swift-docc-docs/scripts/customization_config.py",
    "swiftui-app-architecture-workflow": ROOT / "skills/swiftui-app-architecture-workflow/scripts/customization_config.py",
    "explore-apple-swift-docs": ROOT / "skills/explore-apple-swift-docs/scripts/customization_config.py",
    "format-swift-sources": ROOT / "skills/format-swift-sources/scripts/customization_config.py",
    "structure-swift-sources": ROOT / "skills/structure-swift-sources/scripts/customization_config.py",
    "bootstrap-swift-package": ROOT / "skills/bootstrap-swift-package/scripts/customization_config.py",
    "bootstrap-xcode-app-project": ROOT / "skills/bootstrap-xcode-app-project/scripts/customization_config.py",
    "sync-xcode-project-guidance": ROOT / "skills/sync-xcode-project-guidance/scripts/customization_config.py",
    "sync-swift-package-guidance": ROOT / "skills/sync-swift-package-guidance/scripts/customization_config.py",
    "swift-package-build-run-workflow": ROOT / "skills/swift-package-build-run-workflow/scripts/customization_config.py",
    "swift-package-testing-workflow": ROOT / "skills/swift-package-testing-workflow/scripts/customization_config.py",
}


def load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CustomizationTemplatePathTests(unittest.TestCase):
    def test_customization_templates_live_under_references(self) -> None:
        for skill_name, module_path in SKILL_MODULES.items():
            with self.subTest(skill=skill_name):
                module = load_module(module_path)
                template_path = module.template_path()
                expected = module_path.parents[1] / "references" / "customization.template.yaml"
                self.assertEqual(template_path, expected)
                self.assertTrue(template_path.is_file())
                loaded = module.load_template()
                self.assertEqual(loaded["schemaVersion"], 1)
                self.assertIn("settings", loaded)

    def test_partial_override_yaml_loads_and_merges(self) -> None:
        override_text = 'isCustomized: true\nsettings:\n  fallbackOrder: "url-service,http,mcp"\n'
        for skill_name, module_path in SKILL_MODULES.items():
            with self.subTest(skill=skill_name):
                module = load_module(module_path)
                with tempfile.TemporaryDirectory() as tmpdir:
                    override_path = Path(tmpdir) / "override.yaml"
                    override_path.write_text(override_text, encoding="utf-8")
                    loaded = module.parse_yaml(override_path)
                    module.validate_config(loaded, allow_partial=True)
                    merged = module.merge_configs(module.load_template(), loaded)
                    self.assertEqual(merged["isCustomized"], True)
                    self.assertIn("settings", merged)

    def test_invalid_yaml_is_rejected(self) -> None:
        invalid_text = "schemaVersion: [1\n"
        for skill_name, module_path in SKILL_MODULES.items():
            with self.subTest(skill=skill_name):
                module = load_module(module_path)
                with tempfile.TemporaryDirectory() as tmpdir:
                    invalid_path = Path(tmpdir) / "invalid.yaml"
                    invalid_path.write_text(invalid_text, encoding="utf-8")
                    stderr = io.StringIO()
                    with self.assertRaises(SystemExit):
                        with redirect_stderr(stderr):
                            module.parse_yaml(invalid_path)
                    self.assertIn("Invalid YAML", stderr.getvalue())

    def test_unknown_top_level_key_is_rejected(self) -> None:
        for skill_name, module_path in SKILL_MODULES.items():
            with self.subTest(skill=skill_name):
                module = load_module(module_path)
                config = {
                    "schemaVersion": 1,
                    "isCustomized": True,
                    "settings": {},
                    "unexpected": "value",
                }
                with self.assertRaises(SystemExit):
                    module.validate_config(config, allow_partial=False)

    def test_settings_must_be_a_mapping(self) -> None:
        invalid_text = "schemaVersion: 1\nisCustomized: true\nsettings:\n  - bad\n"
        for skill_name, module_path in SKILL_MODULES.items():
            with self.subTest(skill=skill_name):
                module = load_module(module_path)
                with tempfile.TemporaryDirectory() as tmpdir:
                    invalid_path = Path(tmpdir) / "invalid.yaml"
                    invalid_path.write_text(invalid_text, encoding="utf-8")
                    loaded = module.parse_yaml(invalid_path)
                    with self.assertRaises(SystemExit):
                        module.validate_config(loaded, allow_partial=False)

    def test_nested_settings_values_are_rejected(self) -> None:
        invalid_text = "schemaVersion: 1\nisCustomized: true\nsettings:\n  nested:\n    child: true\n"
        for skill_name, module_path in SKILL_MODULES.items():
            with self.subTest(skill=skill_name):
                module = load_module(module_path)
                with tempfile.TemporaryDirectory() as tmpdir:
                    invalid_path = Path(tmpdir) / "invalid.yaml"
                    invalid_path.write_text(invalid_text, encoding="utf-8")
                    loaded = module.parse_yaml(invalid_path)
                    with self.assertRaises(SystemExit):
                        module.validate_config(loaded, allow_partial=False)


if __name__ == "__main__":
    unittest.main()
