---
name: swift-modernization-cleanup-workflow
description: Run complete modernization and repair passes over existing Swift code, sequencing formatting, source inventory, file splitting, API cleanup, functional pipeline cleanup, concurrency cleanup, tests, docs handoffs, and validation.
license: PolyForm-Noncommercial-1.0.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
---

# Swift Modernization Cleanup Workflow

## Purpose

Modernize existing Swift code without leaving cleanup half-done.

This is the top-level shared Swift repair workflow for poor-quality implementations, drifted source trees, unclear APIs, imperative pipeline tangles, old concurrency patterns, broad files, and weak validation.

## Ownership

- Use this skill for shared Swift language cleanup.
- Use `apple-dev-skills` for Apple framework behavior, Xcode execution, project membership, UI previews, signing, simulators, devices, and Apple docs gates.
- Use `server-side-swift` for Vapor, Hummingbird, SwiftNIO service hosting, persistence, Docker, Fly.io, auth, observability, and deployment.

## Workflow

1. Inspect before changing:
   - `AGENTS.md`
   - README or CONTRIBUTING
   - `Package.swift`
   - `.swiftformat`
   - `.swiftlint.yml`
   - Xcode or XcodeGen files when present
   - CI workflows
   - existing validation commands
2. Establish the formatting baseline through `swift-format-style-workflow`.
3. Inventory cleanup targets:
   - oversized files
   - mixed responsibilities
   - unclear public or internal APIs
   - callback-heavy or nested async code
   - mutable shared state
   - imperative parser, loader, or transform pipelines
   - weak error and log messages
   - duplicate helpers
   - stale TODO/FIXME comments
   - missing or weak tests around changed behavior
4. Plan coherent slices:
   - source organization
   - API shape and naming
   - functional data pipelines
   - concurrency boundaries
   - error and logging quality
   - tests
   - docs handoffs
5. Apply complete passes:
   - avoid tiny partial edits when adjacent cleanup is part of the same concern
   - split files when concern boundaries are real
   - remove duplicate paths and stale wrappers
   - keep behavior validation close to each slice
6. Format again after structural changes.
7. Validate serially with the narrowest useful commands.

## Modernization Defaults

- Prefer Swift concurrency over callback pyramids when the target platform and repository support it.
- Prefer value flow over hidden mutation.
- Prefer functional pipelines for transformation-heavy code.
- Prefer typed domain models over dictionaries, strings, or loosely coupled tuples.
- Prefer small support files with one clear job.
- Prefer tests around behavior before and after risky cleanup.
- Prefer human-readable errors that explain what operation failed and what to inspect next.

## Output Shape

Return:

1. `Cleanup state`: the current risks and code smells.
2. `Slice plan`: ordered cleanup slices and why each belongs.
3. `Changes`: files and responsibilities changed.
4. `Handoffs`: Apple, server-side, docs, project, or deployment owners.
5. `Validation`: commands run, results, and manual gaps.

## Guardrails

- Do not start with broad rewrites before reading repo guidance and validation commands.
- Do not leave compatibility shims, duplicate code paths, or transitional wrappers unless Gale explicitly approves.
- Do not silently change public API compatibility or deployment behavior.
- Do not run multiple SwiftPM or Xcode build/test commands concurrently.
- Do not claim runtime behavior is validated when only formatting or static checks ran.
