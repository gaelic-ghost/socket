# Swift Checks

## Detection

Treat repository as Swift when any is present:
- `Package.swift`
- `*.xcodeproj`
- `*.xcworkspace`

## Alignment Expectations

- Docs should include Swift command usage for package-based repos:
  - `swift build`
  - `swift test`
- If repository docs require `swiftly` for toolchain management, docs should not direct users to unrelated toolchain managers.

## Safe Fix Scope

- Replace clearly wrong language command snippets in docs quickstart/test lines when the replacement is deterministic.
- Add concise quickstart block if missing and repo is clearly Swift package-based.
