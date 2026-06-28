# AGENTS.md

This file is the Swift Lang child-plugin override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `swift-lang` is a monorepo-owned Socket child and the canonical source of truth for shared Swift language workflow skills.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Treat `swift-lang` as the shared language layer for Swift API style, error handling, formatting, source organization, modernization cleanup, and functional data-flow guidance.
- Treat `apple-dev-skills` as the Apple-platform specialist layer. Do not put Xcode project mutation, SwiftUI, AppKit, UIKit, AVFoundation, AVFAudio, Core Media, Core Audio, DocC, Safari, SPI, signing, simulator, or device execution guidance here unless it is only a handoff.
- Treat `server-side-swift` as the server-side specialist layer. Do not put Vapor, Hummingbird, SwiftNIO service hosting, persistence, Docker, Fly.io, observability, auth, or deployment guidance here unless it is only a handoff.

## Local Rules

- Match the `socket` shared semantic version exactly; use the Socket root release workflow for version inventory and bumps.
- Prefer Swift Package Manager as the source of truth for plain Swift packages, libraries, command-line tools, and package-level validation.
- Use repo-local files, checked-out dependency sources, and Dash MCP or Dash HTTP for installed Swift, SwiftPM, SwiftFormat, SwiftLint, and Swift ecosystem docsets before reaching for web docs. Use official Swift project documentation when Dash/local coverage is missing, stale, or a public latest-release citation is needed.
- Keep Swift examples Swifty, ergonomic, compact, and functional when that improves clarity.
- Prefer explicit inputs and outputs, value types, immutable local bindings, composable transforms, and straight data flow over hidden mutation or broad manager types.
- Keep data modeling and pipelines monadic where practical: model stages as values flowing through `Optional`, `Result`, `throws`, `async throws`, `AsyncSequence`, or small domain pipeline types. Do not force this style when it hides effects, fights Swift concurrency, or makes the code harder to test.
- Prefer `throws` for ordinary fallible operations, typed throws for small closed domain failure sets that callers can usefully exhaust, `Result` when failure must be stored or composed as a value, and `Optional` only for ordinary absence that is not diagnostic.
- Prefer `map`, `flatMap`, `compactMap`, `filter`, `reduce`, `zip`, `forEach`, key paths, trailing closures, and fluent chains when the resulting code reads left-to-right as a real data flow.
- Split long chains into named intermediate values when debugging, error reporting, or readability would improve.
- Prefer small files and single-purpose support types. Split Swift files earlier than broad default style guides when a real concern boundary exists.
- Keep public APIs human-friendly at call sites: clear labels, concrete domain values, typed errors or actionable thrown errors, and consistent naming across sibling APIs.
- Keep operator-facing error, warning, and log messages concrete, readable, and actionable.
- Do not leave duplicate compatibility paths, stringly-typed fallback surfaces, or transitional wrappers behind unless Gale explicitly approves that compromise.

## Validation

Use the narrowest validation that proves the changed surface. For plugin metadata changes, run from the Socket root:

```bash
uv run scripts/validate_socket_metadata.py
```

For future Swift helper scripts or tested contracts added under this plugin, add child-plugin validation commands here in the same pass.
