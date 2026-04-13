# Apple Swift Package Core AGENTS Snippet

Use this snippet in repository `AGENTS.md` files when you want baseline standards for a Swift Package Manager repository that is not itself a native Apple app project.

## General Swift Baseline

- For any Swift, Apple-framework, Apple-platform, SwiftUI, SwiftData, Observation, AppKit, UIKit, Foundation-on-Apple, or Xcode-related task, read the relevant Apple documentation first before planning, proposing, or making changes.
- Use Dash or local Apple documentation first, then official Apple documentation when local docs are insufficient.
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
- Prefer applicable existing framework or platform error types before inventing custom error wrappers or error hierarchies.
- Prefer direct, simple error flows and small focused error enums only when they materially improve understanding.
- Prefer stable, source-of-truth naming across layers when the data and meaning have not changed.
- Treat naming consistency as a reliability feature: if the same data still serves the same purpose, keep the same name.
- Do not rename fields just to match local style conventions when the external schema is already clear and stable.
- Do not use automatic case-conversion strategies such as `.convertFromSnakeCase` or `.convertToSnakeCase` unless the project explicitly wants that behavior and it clearly improves readability overall.
- When an API, cloud service, or wire format already provides clear names, preserve those names directly in Swift models and nearby code unless the meaning actually changes or a concrete collision must be resolved.
- Preserve raw wire and persistence shapes by default; do not add DTO, domain, or view-model conversion layers unless meaning actually changes or a concrete boundary requires it.
- Treat redundant wrappers, rename-and-copy layers, and duplicated logic as anti-patterns by default.
- This guidance is optimized for an advanced Swift reader and may prefer dense but readable modern Swift over beginner-style explicitness.
- Prefer explicit names that are consistent, unambiguous, and easy to scan at the call site.
- Prefer compact syntax when it improves local reasoning, including shorthand syntax, ternary expressions, trailing closures, enums, `switch`, `map`, `filter`, `forEach`, async iteration, `AsyncSequence`, `AsyncStream`, and `AsyncAlgorithms`.
- Prefer explicit default values at initialization when they reduce optional-handling clutter and keep the code easier to follow.
- When lines, chains, or expressions get long, prefer chopping them down into a clean vertical, top-down structure with straight visual flow.
- Do not force value types by default, protocols at seams, actors by default, or other pattern slogans when a plainer concrete implementation is easier to reason about.
- Keep code compliant with Swift 6 language mode.
- Keep strict concurrency checking enabled.
- Prefer modern structured concurrency (`async`/`await`, task groups, actors) over legacy async patterns when it keeps the flow clearer and more direct.
- Make async APIs cancellation-aware, propagate cancellation promptly, and avoid detached tasks unless severing actor, priority, and task-local context is the explicit goal.
- Prefer clear `Sendable` boundaries for values crossing task or actor isolation, and treat unchecked sendability as a last resort that must be justified locally.
- Prefer direct async tests over expectation-heavy indirection when the code already exposes async entry points.
- Prefer Swift Testing (`import Testing`) as the default test framework, and use XCTest only when a dependency or platform constraint requires it.
- Use Swift Testing suites, tags, parameterized tests, and `@Test` functions as the default package-testing surface on current toolchains.
- For asynchronous event-driven tests in Swift Testing, prefer `confirmation(...)` with an explicit expected count or count range instead of ad hoc sleeps or polling loops.
- Keep XCTest for integration points that still require it, for legacy package surfaces that have not migrated yet, or when a dependency or platform toolchain still expects XCTest.
- Prefer first-party and top-tier Swift ecosystem packages from Apple, `swiftlang`, the Swift Server Work Group, and similarly trusted core Swift projects when they simplify the code and make it easier to reason about.
- Commonly approved examples include `swift-configuration` and `swift-async-algorithms` when they reduce bespoke code and improve readability.
- For packages, server-side, or cross-platform Swift, prefer Swift Logging as the primary logging API.
- Prefer Swift OpenTelemetry for telemetry and instrumentation when telemetry is needed, and prefer existing ecosystem integrations over bespoke wrappers.
- Prefer Nick Lockwood's SwiftFormat and/or SwiftLint as the default Swift formatting and linting tools; at least one should be configured and used in any Swift project.
- Keep automation and CI commands deterministic, non-interactive, and explicit about toolchain, platform, and configuration assumptions.

## Swift Package and Tooling Baseline

- Use Swift Package Manager as the source of truth for package structure and dependencies outside Xcode-managed app workflows.
- Prefer `swift package` subcommands for dependency, target, and manifest-adjacent changes before hand-editing `Package.swift`.
- Edit `Package.swift` intentionally and keep it readable; agents may modify it when package structure, targets, products, or dependencies need to change, and should try to keep package graph updates consolidated in one change when possible.
- Avoid adding unnecessary dependency-provenance detail or switching to branch/revision-based requirements unless the user explicitly asks for that level of control.
- Treat `Package.resolved` and similar package-manager outputs as generated files; do not hand-edit them.
- Keep package resources under the owning target directory, typically below `Sources/<TargetName>/Resources` or `Tests/<TargetName>Tests/Resources`, so target membership stays obvious.
- Declare non-automatic resources intentionally with `Resource.process(...)`, `Resource.copy(...)`, or `Resource.embedInCode(...)` according to the distribution need.
- Prefer `Resource.process(...)` when platform-aware processing or optimization is desired, and prefer `Resource.copy(...)` when the bytes or directory layout must be preserved exactly.
- Use `exclude` intentionally when files live under a target tree but should not be bundled as package resources.
- Load bundled package resources through `Bundle.module`, and expose higher-level typed accessors when that makes downstream use easier to read.
- Keep test fixtures as test-target resources instead of relying on unstable working-directory assumptions.
- Bundle precompiled Metal artifacts such as `.metallib` files as explicit package resources, and prefer `.copy(...)` when exact distribution matters more than resource processing.
- When the requested work requires compiling Metal shaders, validating Apple-platform bundle integration, or inspecting Apple-managed components such as the Metal toolchain, hand off to the Xcode-aware workflow instead of assuming plain `swift build` is sufficient.
- Run `swift build` and `swift test` as the default validation checks after package-level changes.
- Use `xcodebuild` for package validation when configuration-specific Apple-platform behavior matters, when test plans must be exercised, or when package builds depend on Xcode-managed SDK or Metal-toolchain behavior.
- When package test plans are part of the contract, keep `.xctestplan` files versioned alongside the package-facing Xcode integration and exercise them explicitly with `xcodebuild -showTestPlans` and `xcodebuild -testPlan ...`.
- Validate both Debug and Release paths when behavior or optimization differences matter, and treat tagged releases as a signal to verify both the everyday Debug developer path and the Release artifact path before publishing.
- Keep toolchain selection explicit and reproducible across local development and CI when supporting multiple Swift versions or platforms.
- Prefer portable SwiftPM and CLI workflows for server-side or cross-platform Swift code, and avoid assuming Apple-only SDKs or Xcode-only behavior unless the project explicitly requires them.
