# AGENTS.md

## Baseline Provenance

- This template is the full bootstrap `AGENTS.md` used for new Swift package repositories.
- It intentionally incorporates the shared Swift/Apple baseline from `shared/agents-snippets/apple-swift-core.md`.
- Keep baseline guidance aligned with the shared snippet and use this template for deterministic scaffold output.

## Repository Expectations

- Use Swift Package Manager (SPM) as the source of truth for package structure and dependencies.
- Prefer `swift package` CLI commands for structural changes whenever the command exists.
- Use `swift package add-dependency` to add dependencies instead of hand-editing package graphs.
- Use `swift package add-target` to add library, executable, or test targets.
- For package configuration not covered by CLI commands, update `Package.swift` intentionally and keep edits minimal.
- Keep package graph updates together in the same change (`Package.swift`, `Package.resolved`, and target/test layout when applicable).
- Validate package changes with:
  - `swift build`
  - `swift test`

## Swift Coding Preferences

- Prefer the simplest correct Swift that is easiest to read, reason about, and maintain.
- Treat idiomatic Swift and Cocoa-style naming conventions as tools in service of readability, not goals by themselves.
- Prefer explicit, consistent, and unambiguous names.
- Prefer compact and concise code; use shorthand syntax and trailing-closure syntax when readability improves.
- Do not add boilerplate, helper types, or extra layers just to make code look more architectural or more "Swifty".
- Strongly prefer synthesized, implicit, and framework-provided behavior over handwritten setup code.
- Prefer stable, source-of-truth naming across layers when the data and meaning have not changed.
- Treat naming consistency as a reliability feature: if the same data still serves the same purpose, keep the same name.
- Do not rename fields just to match local style conventions when the external schema is already clear and stable.
- Do not use automatic case-conversion strategies such as `.convertFromSnakeCase` or `.convertToSnakeCase` unless the project explicitly wants that behavior and it clearly improves readability overall.

## Types and Architecture

- Prefer concrete, straightforward types and data flow that keep the code easy to follow.
- Use `struct`, `enum`, `class`, `actor`, and protocols only when each one is the clearest fit for the actual problem.
- Mark classes as `final` by default.
- Prefer synthesized conformances (`Codable`, `Equatable`, `Hashable`, etc.) whenever they satisfy the actual requirements.
- Prefer memberwise and otherwise synthesized initializers, default property values, and framework defaults over handwritten setup code.
- Do not add `CodingKeys`, manual `Codable`, custom initializers, wrappers, helper types, protocols, coordinators, or extra layers unless they are required by a concrete constraint or make the final code clearly easier to understand.
- When an API, cloud service, or wire format already provides clear names, preserve those names directly in Swift models and nearby code unless the meaning actually changes or a concrete collision must be resolved.
- Use enums as namespaces only when they genuinely reduce clutter instead of adding indirection.
- Keep code modular and cohesive without fragmenting simple logic across unnecessary files or types.
- Prefer pure Swift solutions where practical.

## Concurrency and Language Mode

- Keep code compliant with Swift 6 language mode.
- Keep strict concurrency checking enabled.
- Use modern structured concurrency (`async`/`await`, task groups, actors, `AsyncSequence`) instead of legacy async patterns when it keeps the flow clearer and more direct.
- For app-facing packages, prefer approachable concurrency defaults with main-actor isolation by default.
- Introduce parallelism where it produces clear performance gains.

## State, Frameworks, and Dependencies

- Prefer `@Observation` over Combine for observation/state propagation.
- Prefer frameworks and packages from Swift.org, Swift on Server, Apple, and Apple Open Source ecosystems when they simplify the code and make it easier to reason about.
- Commonly approved examples include packages such as `swift-configuration`, `swift-async-algorithms`, and `swift-algorithms`.

## Testing and Tooling Baseline

- Use Swift Testing (`import Testing`) as the default test framework.
- Avoid XCTest unless an external constraint requires it.
- Keep formatting consistent with `swift-format` conventions.
- Keep linting clean against `swiftlint` with clear, maintainable rule intent.

## CLI Tooling Preferences

- Prefer `swift package` for package-focused workflows (dependency graph, targets, manifest intent, and local package validation).
- Prefer `swift package` subcommands for structural package edits before manually editing `Package.swift`.
- Use `swift build` and `swift test` as the default first-pass validation commands.
- Use `xcodebuild` when validating Apple platform integration details that `swift package` does not cover well (schemes, destinations, SDK-specific behavior, and configuration-specific builds/tests).
- Keep `xcodebuild` invocations explicit and reproducible (always pass scheme, destination or SDK, and configuration when relevant).
- Prefer deterministic non-interactive CLI usage in automation/CI for both `swift package` and `xcodebuild`.
