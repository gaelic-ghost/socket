# Repo Shape Detection

Treat a repo as a plain Swift package when:
- `Package.swift` exists at the chosen root
- no `.xcodeproj`, `.xcworkspace`, or `.pbxproj` markers exist at that same root

Treat a repo as mixed when:
- `Package.swift` exists
- one or more `.xcodeproj`, `.xcworkspace`, or `.pbxproj` markers also exist at the same root

For mixed roots:
- prefer `swift-package-testing-workflow` when the request is ordinary SwiftPM testing work
- hand off to `xcode-testing-workflow` when the request needs Xcode session state, schemes, simulator or device flows, XCUITest, or `.xctestplan` execution
- hand off to `xcode-build-run-workflow` when the request instead needs guarded Xcode-managed mutation or file-membership follow-through
