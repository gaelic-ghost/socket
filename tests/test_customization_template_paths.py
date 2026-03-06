from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_MODULES = {
    "apple-dash-docsets": ROOT / "skills/apple-dash-docsets/scripts/customization_config.py",
    "apple-xcode-workflow": ROOT / "skills/apple-xcode-workflow/scripts/customization_config.py",
    "apple-swift-package-bootstrap": ROOT / "skills/apple-swift-package-bootstrap/scripts/customization_config.py",
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


if __name__ == "__main__":
    unittest.main()
