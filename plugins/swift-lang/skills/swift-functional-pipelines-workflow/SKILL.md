---
name: swift-functional-pipelines-workflow
description: Design or repair Swift data modeling and data pipelines using functional, composable, monadic flows with Optional, Result, throws, async throws, AsyncSequence, map, flatMap, compactMap, filter, reduce, and clear imperative fallbacks when needed. Use swift-error-handling-style-workflow for deeper error carrier and diagnostic decisions.
license: PolyForm-Noncommercial-1.0.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
---

# Swift Functional Pipelines Workflow

## Purpose

Shape Swift data flow as readable functional pipelines whenever that makes the code easier to reason about, test, and compose.

The preferred feel is railway-oriented Swift: values move through named transforms, optional or fallible branches stay explicit, and each stage has one job.

## When To Use

- Use this skill for Swift data modeling, parser, loader, transformer, validation, normalization, or export flows.
- Use this skill when code has sprawling loops, nested `if let`, duplicated guard ladders, mutable scratch state, callback pyramids, or unclear failure handling.
- Use this skill when the user asks for functional Swift, monadic flow, railway-oriented programming, pipelines, `map`, `flatMap`, `compactMap`, `filter`, `reduce`, `Result`, `Optional`, or `AsyncSequence`.

## Workflow

1. Identify the pipeline boundary:
   - input values
   - output values
   - recoverable failures
   - side effects
   - async boundaries
2. Choose the carrier:
   - `Optional` for absence when absence is expected and not diagnostic
   - `throws` or `async throws` for straightforward fallible operations
   - `Result` when failures must be stored, combined, or passed as values
   - `AsyncSequence` when values arrive over time
   - a small domain pipeline type only when standard carriers cannot express the flow clearly
   - hand deeper error carrier, typed throws, domain error, Cocoa bridging, or diagnostics decisions to `swift-error-handling-style-workflow`
3. Refactor toward composable stages:
   - parse
   - validate
   - normalize
   - enrich
   - transform
   - persist or emit
4. Use fluent transforms where they read left-to-right:
   - `map`
   - `flatMap`
   - `compactMap`
   - `filter`
   - `reduce`
   - `zip`
   - `forEach`
   - key-path mapping
5. Name intermediate values when needed:
   - before important diagnostics
   - before side effects
   - before async boundaries
   - when a chain wraps past the point where it remains readable
6. Keep side effects at the edge:
   - isolate I/O, logging, database writes, UI updates, and network calls
   - keep pure transforms independently testable
   - keep MainActor and event-loop boundaries explicit

## Monadic Defaults

- Keep data modeling and pipelines monadic unless it is genuinely infeasible or harmful.
- Prefer binding fallible stages through `flatMap`, `throws`, `Result.flatMap`, or `async throws` rather than scattering state mutation across branches.
- Prefer small transformations that can be composed, reordered, and tested.
- Prefer a narrow domain type over a loose dictionary when stages need shared meaning.
- Prefer a boring `for` loop when mutation is local, performance-sensitive, or more readable than a forced chain.

## Output Shape

Return:

1. `Pipeline state`: current inputs, outputs, failures, and side effects.
2. `Carrier choice`: why `Optional`, `Result`, `throws`, `async throws`, `AsyncSequence`, or an imperative fallback fits.
3. `Refactor plan`: stages and files to change.
4. `Example shape`: a compact code sketch or call-site sketch.
5. `Validation`: tests or compile checks that prove the flow still works.

## Guardrails

- Do not force point-free or overly abstract style when named functions would be clearer.
- Do not hide side effects inside innocent-looking transforms.
- Do not turn a simple local loop into a chain if the loop is more readable.
- Do not erase useful failure information to fit `Optional`.
- Do not add a custom monad or pipeline framework unless standard Swift tools are materially insufficient.
