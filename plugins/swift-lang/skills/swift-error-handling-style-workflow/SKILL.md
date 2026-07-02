---
name: swift-error-handling-style-workflow
description: Design or repair Swift error handling style using throws, typed throws, Result, Optional, AsyncSequence failure types, domain errors, Cocoa bridging, and concise functional recovery paths.
license: PolyForm-Noncommercial-1.0.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
---

# Swift Error Handling Style Workflow

## Purpose

Make Swift failure behavior clear at the call site and useful when something
breaks.

The house style is concise, typed by default for Swift-owned failure surfaces,
and functional in feel: fallible values should move through explicit carriers,
error messages should explain the failed operation, and recovery should happen
at the boundary that can actually choose a next step.

## Source Check

Use repo-local guidance first. For general language behavior, prefer the Swift
Book, Swift Standard Library docs, Swift Evolution, and Apple Foundation docs:

- [Error Handling in The Swift Programming Language](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/)
- [SE-0413: Typed throws](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0413-typed-throws.md)
- [Result](https://developer.apple.com/documentation/swift/result)
- [About Imported Cocoa Error Parameters](https://developer.apple.com/documentation/swift/about-imported-cocoa-error-parameters)
- [Handling Cocoa Errors in Swift](https://developer.apple.com/documentation/swift/handling-cocoa-errors-in-swift)
- [LocalizedError](https://developer.apple.com/documentation/foundation/localizederror)
- [CustomNSError](https://developer.apple.com/documentation/foundation/customnserror)
- [RecoverableError](https://developer.apple.com/documentation/foundation/recoverableerror)

## When To Use

- Use this skill when designing or reviewing Swift error surfaces.
- Use this skill when code hides recoverable failures in `nil`, strings, logs, or
  broad catch-all wrappers.
- Use this skill when deciding between `throws`, typed throws, `Result`,
  `Optional`, `AsyncSequence` failure types, framework errors, or domain errors.
- Use this skill when modernizing nested `do`/`catch`, callback-era
  `Result`-passing, weak diagnostics, or awkward Objective-C/Cocoa error
  bridging.

## Workflow

1. Identify the failure boundary:
   - operation
   - inputs
   - success value
   - expected absence
   - recoverable failures
   - programmer errors
   - framework or transport errors
   - async or streaming boundary
2. Choose the carrier:
   - nonoptional value when failure is impossible after construction
   - `Optional` when absence is expected and not diagnostic
   - typed throws for Swift-owned fallible operations when the error type can be
     named clearly
   - untyped `throws` or `async throws` when the operation forwards broad,
     open-ended framework, filesystem, networking, database, plugin, or
     dependency failures without adding a useful typed boundary
   - `Result` when success or failure must be stored, combined, cached, tested,
     or delivered through a non-throwing callback
   - `AsyncSequence` failure types when values arrive over time and iteration can
     fail
   - existing framework errors when the platform already gives a precise error
     domain
3. Model domain failures:
   - prefer existing framework errors until a concrete custom domain, extension,
     or call-site recovery need appears
   - prefer small `enum` errors with associated values when the cases are closed
     and meaningful
   - preserve underlying errors when they help diagnosis
   - use `LocalizedError` for user-visible or operator-facing descriptions
   - use `CustomNSError` when Cocoa interop, error domains, codes, or user-info
     keys matter
   - use `RecoverableError` only when the caller can present concrete recovery
     choices
4. Keep flow concise:
   - use `try` and `try await` for straight-line fallible work
   - use `map`, `flatMap`, `mapError`, `Result.get()`, and typed transforms when
     the failure value is intentionally part of the pipeline
   - prefer functional composition over imperative branching whenever it stays
     accurate and readable
   - split long chains at diagnostic, side-effect, actor, or async boundaries
   - catch narrowly where recovery happens
   - let errors propagate when the current layer has no useful recovery decision
5. Improve diagnostics:
   - include operation, source, important input identity, likely cause, and next
     inspection point when the error reaches a human
   - keep low-level details available without dumping secrets or raw payloads
   - log at the boundary that has context, not at every propagation hop
   - avoid vague messages such as `failed`, `invalid`, or `unknown error`

## House Defaults

- Prefer typed throws for Swift-owned synchronous and structured-concurrency
  APIs when the error type can be named clearly.
- Prefer untyped `throws` when forwarding broad framework, filesystem,
  networking, database, plugin, or dependency failures without changing their
  meaning.
- Prefer `Result` for value-level composition, storage, callback interop, batch
  outcomes, and tests that need to assert failure as data.
- Prefer `Optional` only for ordinary absence. Do not erase useful failure
  information to make a pipeline look tidy.
- Prefer existing Foundation, Cocoa, SwiftPM, SwiftNIO, Vapor, Hummingbird, or
  framework error types until a concrete custom domain, extension, or recovery
  need appears.
- Prefer small domain error enums over broad wrapper hierarchies when custom
  errors are needed.
- Prefer preserving underlying errors over stringifying them.
- Prefer direct propagation over local catch-and-rethrow wrappers that add no new
  context.
- Prefer functional transforms, narrow recovery helpers, and value-level error
  composition over broad imperative branching.
- Prefer assertions, preconditions, or non-throwing validation for programmer
  mistakes only when recovery is not part of the API contract.

## Typed Throws Guidance

Typed throws is the preferred house style for Swift-owned error surfaces, while
untyped `throws` remains the right tool for open-ended failure domains.

Use typed throws when:

- the operation has a closed domain error set
- the operation is Swift-owned and the error type can be named clearly
- callers benefit from exhaustive `catch` handling
- tests should assert every domain case
- a generic API should preserve its caller's failure type
- embedded, performance-sensitive, or allocation-sensitive code benefits from
  carrying a concrete error type

Avoid typed throws when:

- the operation mostly forwards framework, filesystem, networking, database, or
  plugin errors without adding a meaningful typed boundary
- the API boundary is public and the error set is likely to grow
- callers would immediately erase the type to `any Error`
- the type annotation makes simple code noisier without changing recovery

## Error Helper Direction

A small shared helper package could become useful if several repositories start
needing the same concise diagnostic, wrapping, or recovery helpers.

Treat that as a separate design decision. A future package might explore generic
helpers, variadic generics or parameter packs, and macros, but do not invent a
local helper framework inside one app or skill unless the repeated call sites
already exist and the package design has been discussed.

Use the root Socket maintainer plan at
`docs/maintainers/errorhandles-package-plan.md` when deciding whether that helper
belongs in Socket or in a separate Swift package repository.

## Example Shapes

Straight-line fallible work:

```swift
func loadManifest(at url: URL) async throws -> Manifest {
    let data = try await fetch(url)
    return try ManifestDecoder().decode(data)
}
```

Closed domain failures:

```swift
enum ManifestError: Error, Equatable {
    case missingName(URL)
    case unsupportedVersion(String)
}

func validate(_ manifest: Manifest) throws(ManifestError) -> Manifest {
    guard let name = manifest.name else {
        throw .missingName(manifest.sourceURL)
    }

    guard manifest.version.isSupported else {
        throw .unsupportedVersion(manifest.version.rawValue)
    }

    return manifest
}
```

Stored or batched failures:

```swift
let results: [Result<Package, PackageLoadError>] = urls.map { url in
    Result { try loadPackage(at: url) }
}

let packages = results.compactMap { try? $0.get() }
let failures = results.compactMap { result -> PackageLoadError? in
    guard case let .failure(error) = result else { return nil }
    return error
}
```

Operator-facing error context:

```swift
enum PackageLoadError: LocalizedError {
    case unreadableManifest(url: URL, underlying: any Error)

    var errorDescription: String? {
        switch self {
        case let .unreadableManifest(url, underlying):
            "Could not read Package.swift at \(url.path). Check that the file exists, is readable, and contains valid Swift package syntax. Underlying error: \(underlying)"
        }
    }
}
```

## Output Shape

Return:

1. `Failure state`: current operation, success value, absence, recoverable
   failures, and programmer errors.
2. `Carrier choice`: why `throws`, typed throws, `Result`, `Optional`,
   `AsyncSequence`, existing framework errors, or domain errors fit.
3. `House-style changes`: API signatures, error types, propagation, recovery,
   and diagnostics to change.
4. `Examples`: compact call-site or implementation sketch.
5. `Validation`: compile, tests, and failure-case checks needed.

## Guardrails

- Do not add error abstraction layers without a real caller, recovery path, or
  interop need.
- Do not wrap every underlying error just to make a local enum exhaustive.
- Do not force typed throws onto APIs whose failures are still genuinely
  open-ended.
- Do not hide recoverable failures in logs, `nil`, default values, or comments.
- Do not over-functionalize error handling when a narrow `do`/`catch` is clearer.
- Do not catch only to print or log and then continue with corrupted state.
