# SwiftPM Workflow Policy

## Decision order

1. Resolve the nearest package root.
2. Confirm `Package.swift` is present.
3. Use SwiftPM for package operations regardless of co-located Xcode files.
4. Hand off only the operation that requires Xcode-owned state.

## SwiftPM-first invariant

Use SwiftPM and ordinary filesystem edits first for:
- package inspection
- manifest and dependency work
- build, test, and run tasks
- package plugin flows
- terminal-first editor workflows

## Workspace invariant

Co-located `Package.swift`, `.xcworkspace`, and `.xcodeproj` files are the normal product shape. Never classify the repository or require an opt-in.
