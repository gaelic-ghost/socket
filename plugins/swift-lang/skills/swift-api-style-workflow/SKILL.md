---
name: swift-api-style-workflow
description: Review, design, or repair Swift APIs for Swifty naming, call-site ergonomics, access control, typed result shapes, human-friendly errors, and consistency across sibling symbols. Use for shared Swift API style before Apple-platform or server-framework details.
license: PolyForm-Noncommercial-1.0.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
---

# Swift API Style Workflow

## Purpose

Make Swift APIs feel Swifty, ergonomic, intuitive, and human-friendly at the call site.

This skill owns language-level API style. Hand off to `apple-dev-skills` for Apple framework or Xcode project behavior, and to `server-side-swift` for Vapor, Hummingbird, SwiftNIO, deployment, persistence, observability, or auth behavior.

## Source Check

Use repo-local guidance first. When general Swift API behavior needs a source, prefer the official Swift API Design Guidelines and current Swift documentation before community style guides.

## Workflow

1. Inspect the current API surface:
   - public and internal symbols
   - call sites
   - result and error shapes
   - overloads, default arguments, and options structs
   - access control
   - naming consistency across sibling APIs
2. Classify the work:
   - new API design
   - API cleanup
   - call-site ergonomics review
   - error and result-shape repair
   - access-control tightening
3. Optimize for the caller:
   - prefer names that read naturally at the use site
   - keep labels meaningful instead of decorative
   - prefer domain values over ambiguous tuples, dictionaries, or strings
   - prefer defaulted parameters for small option sets
   - prefer request or options structs when public APIs reach four or more meaningful parameters
   - prefer enum-backed choices over boolean soups or stringly-typed modes
4. Tighten result and failure behavior:
   - use `throws`, typed domain errors, `Result`, or optional returns according to caller recovery needs
   - make invalid states hard to construct
   - include operation, source, likely cause, and next inspection point in operator-facing errors and logs
5. Remove accidental API weight:
   - collapse needless overloads
   - remove compatibility shims unless explicitly approved
   - replace broad managers with small support types when the current type owns unrelated jobs
   - keep dependency injection unidirectional and data flow straight

## Style Defaults

- Prefer compact Swifty syntax when it is obvious.
- Prefer trailing closures, key paths, shorthand closure arguments, and fluent calls when they improve readability.
- Prefer named intermediate values when a chain needs a diagnostic boundary or the next reader would have to mentally execute it.
- Prefer small composable values, functions, and extensions over stateful orchestration types.
- Prefer complete cleanup passes over leaving duplicate long-term APIs behind.

## Output Shape

Return:

1. `API state`: the current shape and main pain points.
2. `Recommended surface`: the target symbols, names, labels, and result shape.
3. `Call-site examples`: compact examples showing the intended feel.
4. `Migration`: compatibility impact and whether shims are being avoided or deliberately approved.
5. `Validation`: compile, test, or review checks needed.

## Guardrails

- Do not rename public APIs casually when the repo has release or compatibility constraints.
- Do not add wrappers, managers, or service layers without a concrete near-term use case.
- Do not expand readable fluent Swift into verbose ceremony just to satisfy a generic style guide.
- Do not hide recoverable errors in logs or `nil` when the caller can do something useful.
- Do not keep duplicate old and new paths unless Gale explicitly approves that compromise.
