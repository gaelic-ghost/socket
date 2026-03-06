# Apple Swift Core AGENTS Snippet

Use this snippet in repository `AGENTS.md` files when you want cross-project Swift and Apple baseline standards.

## General Swift Baseline

- Keep code compliant with Swift 6 language mode.
- Keep strict concurrency checking enabled.
- Prefer modern structured concurrency (`async`/`await`, task groups, actors) over legacy async patterns.
- Prefer Swift Testing (`import Testing`) as the default test framework, and use XCTest only when a dependency or platform constraint requires it.
- Prefer idiomatic Swift APIs, value types by default, and explicit names that stay clear in call sites and generated docs.
- Keep automation and CI commands deterministic, non-interactive, and explicit about toolchain, platform, and configuration assumptions.

## Xcode Workspace and Project Baseline

- Treat the `.xcworkspace` or `.xcodeproj` as the source of truth for Apple platform app integration, schemes, build settings, and destinations.
- Prefer edits through Xcode-aware project structure and keep project file changes intentional and reviewed closely.
- Use `xcodebuild` for Apple platform integration validation, including scheme, destination or SDK, and configuration-specific build or test runs.
- Keep `xcodebuild` invocations reproducible in automation by passing explicit schemes, destinations or SDKs, and configurations when relevant.
- Prefer direct filesystem edits in Xcode-managed scope only when the workflow already accounts for project-file and scheme integrity.

## Swift Tooling Outside Xcode

- Use Swift Package Manager as the source of truth for package structure and dependencies outside Xcode-managed app workflows.
- Prefer `swift package` subcommands for dependency, target, and manifest-adjacent changes before hand-editing `Package.swift`.
- Keep package graph updates cohesive across `Package.swift`, `Package.resolved`, and related source or test targets.
- Run `swift build` and `swift test` as the default validation checks after package-level changes.
- Keep toolchain selection explicit and reproducible across local development and CI when supporting multiple Swift versions or platforms.
- Prefer portable SwiftPM and CLI workflows for server-side or cross-platform Swift code, and avoid assuming Apple-only SDKs or Xcode-only behavior unless the project explicitly requires them.
