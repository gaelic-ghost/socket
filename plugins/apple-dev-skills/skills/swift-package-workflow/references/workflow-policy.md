# SwiftPM Workflow Policy

## Decision order

1. Resolve the repo root.
2. Confirm `Package.swift` is present.
3. Detect whether the root is plain SwiftPM or mixed with Xcode-managed markers.
4. Prefer the SwiftPM-first path for ordinary package work.
5. Hand off to `xcode-build-run-workflow` or `xcode-testing-workflow` only when Xcode-managed behavior is the primary concern.

## SwiftPM-first invariant

Use SwiftPM and ordinary filesystem edits first for:
- package inspection
- manifest and dependency work
- build, test, and run tasks
- package plugin flows
- terminal-first editor workflows

## Mixed-root invariant

When the repo root contains both `Package.swift` and Xcode-managed markers:
- default to a handoff instead of guessing
- keep the handoff concise and specific
- only stay on the SwiftPM-first path when the user explicitly wants that and the requested work does not cross into Xcode-managed scope
