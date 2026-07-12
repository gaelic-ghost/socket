from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class XcodeDeviceWindowTelemetryDebuggerWorkflowTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_device_hub_preserves_native_device_and_agentdeck_boundaries(self) -> None:
        skill = self.read("skills/xcode-device-hub-workflow/SKILL.md")
        evidence = self.read("skills/xcode-device-hub-workflow/references/device-hub-scope-and-evidence.md")
        prompt = self.read("skills/xcode-device-hub-workflow/agents/openai.yaml")

        for term in ("simulated and physical", "Liquid Glass", "Text Size", "screenshots", "diagnostics"):
            self.assertIn(term, skill + evidence)
        self.assertIn("future AgentDeck runtime", skill)
        self.assertIn("Do not erase, remove, unpair, or reset", skill)
        self.assertIn("$xcode-device-hub-workflow", prompt)

    def test_window_workflow_keeps_native_chrome_and_restoration_contracts(self) -> None:
        skill = self.read("skills/macos-window-management-workflow/SKILL.md")
        reference = self.read("skills/macos-window-management-workflow/references/window-scene-and-chrome-rules.md")

        for term in ("WindowGroup", "WindowDragGesture", "allowsWindowActivationEvents", "restoration", "Window-menu"):
            self.assertIn(term, skill + reference)
        self.assertIn("Do not use borderless or hidden-title-bar styling", skill)
        self.assertIn("appkit-app-architecture-workflow", skill)

    def test_runtime_telemetry_is_private_and_evidence_oriented(self) -> None:
        skill = self.read("skills/apple-runtime-telemetry-workflow/SKILL.md")
        logger_reference = self.read("skills/apple-runtime-telemetry-workflow/references/logger-privacy-and-evidence.md")
        signpost_reference = self.read("skills/apple-runtime-telemetry-workflow/references/signposts-and-runtime-capture.md")

        for term in ("Logger", "OSSignposter", "private by default", "com.apple.logging.local-store", "Instruments"):
            self.assertIn(term, skill + logger_reference + signpost_reference)
        self.assertIn("Do not create a logging manager", skill)
        self.assertIn("ios-runtime-forensics-workflow", skill)

    def test_debugger_workflow_records_beta3_loader_boundary(self) -> None:
        skill = self.read("skills/xcode-debugger-mcp-workflow/SKILL.md")
        evidence = self.read("skills/xcode-debugger-mcp-workflow/references/beta3-capability-evidence.md")
        contract = self.read("skills/xcode-debugger-mcp-workflow/references/active-session-debugging-contract.md")

        for term in ("Xcode 27.0 Beta 3", "27A5218g", "lib_CompilerSwiftIDEUtils.dylib", "InvokeDebuggerCommand", "active debugging session", "mcpbridge", "lldb_command", "does not document a way to select"):
            self.assertIn(term, skill + evidence + contract)
        self.assertIn("Do not work around this", skill)
        self.assertIn("xcode-build-run-workflow", skill)


if __name__ == "__main__":
    unittest.main()
