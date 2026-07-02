# ErrorHandles Package Plan

Use this plan when deciding whether to create a small Swift helper package for
Gale's house error-handling style and how that package should relate to Socket.

## Decision

Create `ErrorHandles` as a separate Swift package repository if the helper API
graduates beyond guidance.

Do not vendor the package source into `socket`. Socket is the Codex plugin and
skills superproject; it should own the agent-facing skills, docs, and workflow
guidance that describe the house style. A reusable Swift package should live in
its own fetchable repository so Gale's apps, services, packages, and libraries
can depend on it through Swift Package Manager without depending on Socket.

Keep the skills located here in Socket:

- `plugins/swift-lang/skills/swift-error-handling-style-workflow` should own the
  general style decision tree.
- A future `swift-lang` skill may own `ErrorHandles` package usage, migration,
  and API review after the package exists.
- Apple-platform and server-side framework skills should hand off shared
  language-level decisions to `swift-lang` instead of duplicating package
  guidance.

## Fit

### Belongs In `ErrorHandles`

- Small typed wrappers or helpers that compile as ordinary Swift.
- `ErrorContext<Failure>` or a similar generic context value.
- A `DiagnosticError`-style protocol if repeated packages need one common
  human-facing shape.
- `Result` and typed-throws bridge helpers that remove real boilerplate.
- Optional macros only after the manual API proves stable.
- Tests, DocC, examples, and semantic-versioned releases for the package.

### Belongs In Socket

- Skills explaining when to use typed throws, untyped throws, `Result`,
  `Optional`, framework errors, or custom domain errors.
- Migration guidance from ad hoc local helpers to the package.
- Agent workflow guidance for package adoption, review, and validation.
- Root roadmap and maintainer notes that track the package's relationship to
  Swift Lang.

### Does Not Belong In Socket

- The package's Swift source as a local dependency.
- Machine-local package paths in manifests, examples, CI, or docs.
- App-specific error domains that only make sense inside one product.
- Macro implementation experiments before the underlying helper API is proven.

## Initial Package Shape

Start with a deliberately small Swift package:

- library target: `ErrorHandles`
- test target: `ErrorHandlesTests`
- Swift language mode: Swift 6
- minimum platform: choose when the first real consumer appears
- dependencies: none for the first slice

Prefer ordinary Swift before macros:

1. `ErrorContext<Failure: Error>`
2. `DiagnosticError` protocol or similarly small diagnostic shape
3. typed `throws` helpers for adding context at a real boundary
4. `Result` helpers for batch and pipeline work
5. examples that preserve existing framework errors until a custom boundary is
   useful

Only add a macro target after repeated boilerplate proves that generated
conformance would be clearer than handwritten Swift.

## API Design Questions

Discuss these before creating the repository:

- Should `ErrorContext` be the concrete root type, or should the package start
  with protocols and extensions only?
- Should context facts be plain values, key-value pairs, or typed fact values?
- Should human-facing descriptions be modeled through `LocalizedError`, a
  package protocol, or both?
- Should the package include `CustomNSError` support in the first slice, or keep
  Cocoa bridging as a later adapter?
- Should helper functions prefer direct typed throws, `Result`, or both from the
  first release?
- What is the minimum Swift tools version and platform floor for Gale's likely
  first consumers?

## Validation And Release

For the package repository:

1. Run `swift test`.
2. Add tests for typed throws propagation, context preservation, framework-error
   pass-through, and `Result` composition.
3. Avoid local path dependencies in committed manifests.
4. Tag semantic versions once the package is used by another repository.

For Socket:

1. Keep `plugins/swift-lang` guidance in sync with the package API after it
   exists.
2. Run `uv run scripts/validate_socket_metadata.py` when skills or plugin
   metadata change.
3. Do not claim the package exists until the standalone repository and fetchable
   Swift package are created.
