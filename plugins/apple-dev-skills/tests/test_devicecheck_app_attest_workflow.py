from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeviceCheckAppAttestWorkflowTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_separates_devicecheck_and_app_attest_paths(self) -> None:
        skill_text = self.read("skills/devicecheck-app-attest-workflow/SKILL.md")
        device_text = self.read("skills/devicecheck-app-attest-workflow/references/devicecheck-device-state.md")
        client_text = self.read("skills/devicecheck-app-attest-workflow/references/app-attest-client-flow.md")

        self.assertIn("DeviceCheck two-bit state with `DCDevice`", skill_text)
        self.assertIn("App Attest app-instance integrity with `DCAppAttestService`", skill_text)
        self.assertIn("query, update, or validate the two bits", device_text)
        self.assertIn("Do not use DeviceCheck as account identity", device_text)
        self.assertIn("generateKey(completionHandler:)", client_text)
        self.assertIn("attestKey(_:clientDataHash:completionHandler:)", client_text)
        self.assertIn("generateAssertion(_:clientDataHash:completionHandler:)", client_text)

    def test_skill_requires_docs_gate_and_supported_apple_behavior(self) -> None:
        skill_text = self.read("skills/devicecheck-app-attest-workflow/SKILL.md")
        client_text = self.read("skills/devicecheck-app-attest-workflow/references/app-attest-client-flow.md")
        entitlement_text = self.read("skills/devicecheck-app-attest-workflow/references/entitlements-app-id-and-validation.md")

        self.assertIn("Apply the Apple docs gate", skill_text)
        self.assertIn("state the documented Apple behavior being relied on", skill_text)
        self.assertIn("Action, extensible SSO, and watchOS extensions", client_text)
        self.assertIn("sandbox and production", entitlement_text)
        self.assertIn("macOS-specific App Attest validation", entitlement_text)

    def test_server_validation_stays_a_handoff_not_app_local_trust(self) -> None:
        skill_text = self.read("skills/devicecheck-app-attest-workflow/SKILL.md")
        server_text = self.read("skills/devicecheck-app-attest-workflow/references/app-attest-server-validation.md")

        self.assertIn("Do not pretend the app can validate its own integrity locally", skill_text)
        self.assertIn("The server owns trust", server_text)
        self.assertIn("decode the attestation object as CBOR", server_text)
        self.assertIn("verify the assertion counter is greater than the previous stored counter", server_text)
        self.assertIn("server-side Swift, OpenAPI, RPC, or backend-specific workflows", server_text)

    def test_skill_handoffs_and_metadata_are_explicit(self) -> None:
        skill_text = self.read("skills/devicecheck-app-attest-workflow/SKILL.md")
        prompt_text = self.read("skills/devicecheck-app-attest-workflow/agents/openai.yaml")

        self.assertIn("Recommend `explore-apple-swift-docs`", skill_text)
        self.assertIn("Recommend `xcode-build-run-workflow`", skill_text)
        self.assertIn("Recommend `xcode-testing-workflow`", skill_text)
        self.assertIn("Recommend `swift-openapi-client-workflow`", skill_text)
        self.assertIn("broader client auth and app-sync workflow", skill_text)
        self.assertIn("references/snippets/apple-xcode-project-core.md", skill_text)
        self.assertIn("$devicecheck-app-attest-workflow", prompt_text)
        self.assertIn("$xcode-build-run-workflow", prompt_text)
        self.assertIn("$xcode-testing-workflow", prompt_text)
        self.assertIn("$swift-openapi-client-workflow", prompt_text)
        self.assertIn("$explore-apple-swift-docs", prompt_text)

    def test_plugin_inventory_includes_devicecheck_workflow(self) -> None:
        readme = self.read("README.md")
        plugin = self.read(".codex-plugin/plugin.json")
        validator = self.read(".github/scripts/validate_repo_docs.sh")
        roadmap = self.read("ROADMAP.md")

        self.assertIn("devicecheck-app-attest-workflow", readme)
        self.assertIn("DeviceCheck", plugin)
        self.assertIn("App Attest", plugin)
        self.assertIn("./skills/devicecheck-app-attest-workflow/SKILL.md", validator)
        self.assertIn("Expected exactly 31 active skills", validator)
        self.assertIn("Milestone 53: DeviceCheck and App Attest Workflow - Completed", roadmap)


if __name__ == "__main__":
    unittest.main()
