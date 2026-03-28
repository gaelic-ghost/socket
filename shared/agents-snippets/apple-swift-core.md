# Apple Swift Core AGENTS Snippet

Use this snippet in repository `AGENTS.md` files when you want cross-project Swift and Apple baseline standards.

## General Swift Baseline

- For any Swift, Apple-framework, Apple-platform, SwiftUI, SwiftData, Observation, AppKit, UIKit, Foundation-on-Apple, or Xcode-related task, read the relevant Apple documentation first before planning, proposing, or making changes.
- Use Dash or Xcode-local documentation first, then official Apple documentation when local docs are insufficient.
- Before proposing an architecture or implementation, state the documented API behavior, lifecycle rule, or workflow requirement being relied on.
- Do not rely on memory, habit, or analogy as the primary source when Apple documentation exists.
- If Apple documentation and the current code disagree, stop and report the conflict before continuing.
- If no relevant Apple documentation can be found, say that explicitly before proceeding.
- Prefer the simplest correct Swift that is easiest to read, reason about, and maintain.
- Treat idiomatic Swift, Cocoa conventions, and modern Swift features as tools in service of readability, not as goals by themselves.
- Do not add ceremony, abstraction, or boilerplate just to make code look more architectural, more generic, or more "Swifty".
- Strongly prefer synthesized, implicit, and framework-provided behavior over custom code.
- Prefer synthesized conformances (`Codable`, `Equatable`, `Hashable`, etc.) whenever they satisfy the actual requirements.
- Prefer memberwise and otherwise synthesized initializers, default property values, and framework defaults over handwritten setup code.
- Do not add `CodingKeys`, manual `Codable` methods, custom initializers, wrappers, helper types, protocols, coordinators, or extra layers unless they are required by a concrete constraint or they make the final code clearly easier to understand.
- Prefer stable, source-of-truth naming across layers when the data and meaning have not changed.
- Treat naming consistency as a reliability feature: if the same data still serves the same purpose, keep the same name.
- Do not rename fields just to match local style conventions when the external schema is already clear and stable.
- Do not use automatic case-conversion strategies such as `.convertFromSnakeCase` or `.convertToSnakeCase` unless the project explicitly wants that behavior and it clearly improves readability overall.
- When an API, cloud service, or wire format already provides clear names, preserve those names directly in Swift models and nearby code unless the meaning actually changes or a concrete collision must be resolved.
- Prefer explicit names that are consistent, unambiguous, and easy to scan at the call site.
- Prefer shorthand syntax, trailing closures, enums, `AsyncSequence`, `AsyncStream`, and `AsyncAlgorithms` when they make the code shorter and clearer.
- Do not force value types by default, protocols at seams, actors by default, or other pattern slogans when a plainer concrete implementation is easier to reason about.
- Keep code compliant with Swift 6 language mode.
- Keep strict concurrency checking enabled.
- Prefer modern structured concurrency (`async`/`await`, task groups, actors) over legacy async patterns when it keeps the flow clearer and more direct.
- Prefer Swift Testing (`import Testing`) as the default test framework, and use XCTest only when a dependency or platform constraint requires it.
- Prefer first-party and top-tier Swift ecosystem packages from Apple, `swiftlang`, the Swift Server Work Group, and similar trusted core Swift projects when they simplify the code and make it easier to reason about.
- Commonly approved examples include `swift-configuration` and `swift-async-algorithms` when they reduce bespoke code and improve readability.
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
