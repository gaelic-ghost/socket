# Swift Lang Plugin Plan

Use this plan for the first implementation pass of a Socket-hosted `swift-lang`
plugin. The plugin should own shared Swift language guidance that is useful for
Apple apps, server-side Swift services, Swift packages, command-line tools, and
library code without absorbing Apple-platform or server-framework workflows.

## Decision

Create `plugins/swift-lang` as a first-class Socket marketplace plugin.

Do not treat `swift-lang` as a hidden include layer for `apple-dev-skills` or
`server-side-swift`. Socket's documented install model exposes plugins through
marketplace entries, so the shared Swift guidance should be a normal plugin with
its own manifest, skills, metadata, validation, and release surface.

Keep `apple-dev-skills` and `server-side-swift` as specialist plugins. They
should hand off to `swift-lang` for language-level style, structure,
modernization, and cleanup work, while retaining their own domain-specific
documentation and execution workflows.

## Product Shape

`swift-lang` should be the shared language layer for:

- Swift API design, naming, ergonomics, and call-site readability.
- Swift error handling style, carrier choice, typed throws, domain errors, and
  diagnostics.
- Swift writing, style, formatting, and linting policy.
- Swift source organization, file splitting, declaration grouping, and cleanup.
- Swift modernization passes across packages, apps, services, and libraries.
- Functional, composable data modeling and data-flow guidance.
- SwiftPM-first project structure when no narrower Apple or server framework
  skill owns the repository.

`swift-lang` should not own:

- Xcode project mutation, schemes, previews, simulators, signing, or target
  membership. Use `apple-dev-skills`.
- SwiftUI, AppKit, UIKit, AVFoundation, AVFAudio, Core Media, Core Audio, DocC,
  Safari extensions, or Apple developer app workflows. Use `apple-dev-skills`.
- Vapor, Hummingbird, SwiftNIO service hosting, persistence, Docker, Fly.io,
  auth, observability, app sync, or server deployment. Use `server-side-swift`.

## Style Policy

Swift code should feel Swifty, ergonomic, human-friendly, and unsurprising at
the call site. Prefer APIs that read naturally when used, with names that make
the operation, data shape, and failure behavior clear without ceremony.

Default toward functional Swift when it fits the problem:

- Prefer explicit inputs and outputs over hidden mutation.
- Prefer value types and immutable local bindings where practical.
- Prefer small composable transformations over sprawling imperative branches.
- Prefer `map`, `flatMap`, `compactMap`, `filter`, `reduce`, `zip`,
  `forEach`, `Result`, `Optional`, `AsyncSequence`, and throwing transforms when
  they make the pipeline clearer.
- Prefer chaining when the chain reads left-to-right as a real data flow.
- Prefer splitting a long chain into named intermediate values when the chain
  stops being readable, debuggable, or easy to test.
- Keep data modeling and pipelines monadic where practical: model stages as
  values flowing through transformations, bind optional or fallible work through
  `Optional`, `Result`, `throws`, `async throws`, or domain-specific pipeline
  types, and keep error paths explicit.
- Do not force monadic style when it hides important effects, requires awkward
  type gymnastics, fights Swift concurrency, or makes the code harder for the
  next maintainer to change.

Readable Swift in this style may use shorthand syntax, trailing closures,
key-path expressions, chained transforms, and compact closure arguments when the
meaning stays obvious. Do not expand fluent code into verbose ceremony merely to
look more conventional.

Human-friendly APIs should:

- Make invalid states hard to construct.
- Keep labels and names consistent across sibling APIs.
- Return clear domain values instead of ambiguous tuples or stringly-typed
  dictionaries.
- Use typed errors, meaningful thrown errors, or result values where callers can
  recover.
- Keep operator-facing error and log messages concrete, readable, and actionable.
- Avoid compatibility shims, duplicate paths, broad managers, and wrapper layers
  unless a real near-term use case requires them.

## Initial Skill Set

### `swift-api-style-workflow`

Own API naming, call-site ergonomics, access control, typed result shapes,
consistency across sibling APIs, and human-friendly errors.

### `swift-functional-pipelines-workflow`

Own functional data modeling, pipeline design, `Optional` and `Result` flows,
throwing and async transformations, `AsyncSequence`, monadic composition, and
the boundary where imperative code is clearer.

### `swift-error-handling-style-workflow`

Own language-level failure-shape decisions: `throws`, typed throws, `Result`,
`Optional`, `AsyncSequence` failure types, small domain error enums, Cocoa
bridging, `LocalizedError`, `CustomNSError`, recoverable errors, and concise
diagnostic style.

### `swift-format-style-workflow`

Own SwiftFormat and SwiftLint setup, formatter/linter responsibility split,
configuration policy, Git hook or CI enforcement, and personal style defaults.
This skill should absorb or supersede the shared-language parts of
`apple-dev-skills:format-swift-sources`.

### `swift-source-organization-workflow`

Own file splitting, feature/layer directory shape, extension-file extraction,
`// MARK:` discipline, file headers, TODO/FIXME ledger handling, and stronger
split thresholds. This skill should absorb or supersede the shared-language
parts of `apple-dev-skills:structure-swift-sources`.

### `swift-modernization-cleanup-workflow`

Own complete modernization passes over existing Swift code. It should sequence
formatting, source inventory, file splitting, API cleanup, concurrency cleanup,
testability cleanup, documentation handoffs, and final validation.

## Modernization Workflow

The modernization skill should use this default order:

1. Inspect repo guidance, package or project shape, Swift toolchain, formatter
   and linter config, and validation commands.
2. Establish or confirm the formatting baseline before structural edits.
3. Inventory large files, mixed concerns, unclear APIs, callback-heavy code,
   duplicated helpers, weak error messages, mutable shared state, and stale
   TODO/FIXME comments.
4. Split files by concern more readily than the current Apple-local defaults.
   Prefer a soft split threshold around `250` to `300` lines and a hard split
   threshold around `500` to `600` lines, while still requiring a real concern
   boundary for the split.
5. Modernize in coherent slices: API surface, data modeling and pipelines,
   concurrency, source organization, tests, and documentation.
6. Run formatting again after moves and splits.
7. Validate with the narrowest useful SwiftPM or Xcode check, serialized with no
   concurrent Swift build or test processes.

## Compatibility And Migration

First release:

- Add `swift-lang` as a new Socket marketplace entry.
- Keep Apple Dev's existing `format-swift-sources` and
  `structure-swift-sources` skills available for Apple-only installs.
- Update Apple Dev and Server-Side Swift guidance to hand off to `swift-lang`
  when the user has the Socket marketplace or `swift-lang` installed.
- Avoid breaking standalone `apple-dev-skills` users in the first release.

Later release:

- Decide whether Apple Dev should keep thin Apple-flavored wrappers around the
  shared Swift skills or deprecate its local copies.
- If deprecating, provide a clear release note and migration path through the
  Socket marketplace.

## Implementation Slices

1. Scaffold `plugins/swift-lang` with manifest, `AGENTS.md`, first skill
   metadata, and root marketplace wiring.
2. Add `swift-api-style-workflow` and `swift-functional-pipelines-workflow`.
3. Port and tune formatting and source-organization guidance from Apple Dev into
   `swift-format-style-workflow` and `swift-source-organization-workflow`.
4. Add `swift-modernization-cleanup-workflow` as the top-level repair workflow.
5. Add `swift-error-handling-style-workflow` for the house error-handling style.
6. Update Apple Dev and Server-Side Swift handoff guidance.
7. Add focused tests or metadata validation coverage for the new plugin.
8. Run root metadata validation and any new child-plugin validation.

## Exit Criteria

- Socket exposes `swift-lang` as an installable marketplace plugin.
- The plugin gives agents clear Swift language guidance without duplicating
  Apple-platform or server-framework ownership.
- The functional Swift style policy is explicit enough to guide implementation
  choices, review comments, and modernization passes.
- Apple Dev and Server-Side Swift guidance can route shared Swift cleanup work
  to `swift-lang` while preserving standalone Apple-only behavior for the first
  release.
