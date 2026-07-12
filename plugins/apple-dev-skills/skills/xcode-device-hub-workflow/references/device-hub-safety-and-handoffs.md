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
