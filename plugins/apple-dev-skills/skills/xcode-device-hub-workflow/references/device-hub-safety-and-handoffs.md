# Device Hub Safety and Handoffs

Use the smallest surface that proves the question:

| Need | Owner |
| --- | --- |
| Scheme, build, install, launch, normal logs | `xcode-build-run-workflow` |
| Test filtering, XCTest, Swift Testing, XCUITest | `xcode-testing-workflow` |
| Breakpoints, variables, stack frames, debugger commands | `xcode-debugger-mcp-workflow` |
| Simulator ETTrace, memgraph, leak ownership | `ios-runtime-forensics-workflow` |
| Device capability, profiles, certificates, CloudKit | `apple-developer-provisioning-workflow` |
| Browser-visible mirror or package preview host | future AgentDeck runtime; unavailable until its bridge status says ready |

Pairing, unpairing, Developer Mode, device removal, erase/reset, and environment changes affect user-owned device state. Read the state first and require an explicit requested action before changing it. A screenshot or diagnostic should identify the exact device and app state that produced it.

For a physical-device UI-test failure, preserve the XCUITest result and `.xcresult` first. Use Device Hub for the visible state and a relevant diagnostic, `xcrun devicectl` for a bounded scripted device-management or diagnostic action, and `xcode-debugger-mcp-workflow` for an active Xcode source-level debugging session. These artifacts complement one another; none replaces the test result.
