---
name: swift-syntax-tooling-workflow
description: Parse, inspect, generate, or transform source with SwiftParser and SwiftSyntax while preserving fidelity. Use for Swift codemods, structural linting, generators, syntax-aware edits, or macro trees without inferred types.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
  hermes:
    category: swift-language
    tags: [swift, swiftsyntax, parser, codemod, source-generation]
---

# Swift Syntax Tooling Workflow

Build source-accurate Swift tooling without confusing a syntax tree with the compiler's type-checked AST.

## Workflow

1. Inspect repository guidance, manifest dependencies, Swift language mode, formatting policy, and existing SwiftSyntax version.
2. Resolve whether Swiftly or Xcode owns the compiler used to build the tooling. Record both resolvers on macOS when they are available.
3. Classify the task:
   - parse or inspect
   - visit and collect
   - rewrite or migrate
   - generate declarations or files
   - emit syntax diagnostics
   - implement macro expansion syntax
4. Select only the needed products. Use [references/swift-syntax-components.md](references/swift-syntax-components.md) for product responsibilities and version alignment.
5. Preserve source fidelity:
   - operate on syntax nodes instead of text ranges when structure matters
   - retain trivia and untouched subtrees
   - make malformed-source recovery explicit
   - account for `#if` regions and generated source
6. Design transformations as pure input-tree to output-tree operations where practical. Isolate filesystem writes, formatting, and reporting at the edge.
7. Test with fixtures covering matching input, non-matching input, malformed syntax, trivia, idempotence, and the active Swift version.
8. Run the repository's serialized SwiftPM or Xcode validation through its owning workflow.

## Toolchain Contract

- Align the SwiftSyntax release with the Swift language and tooling release selected by the repository.
- Prefer the repository's SwiftPM dependency for a distributable tool; do not link against machine-local Xcode libraries in shared package manifests.
- Use Swiftly for explicit Swift.org toolchain matrices and cross-platform package validation.
- Use Xcode through `xcrun` when the tool must match an Apple SDK, selected Xcode compiler, or Xcode macro behavior.
- Report a mismatch instead of silently rebuilding against whichever `swift` appears first on `PATH`.

## Boundaries

- Use `swift-semantic-indexing-workflow` when the task needs inferred types, USRs, overload resolution, documentation from compiled modules, or project-wide references.
- Use `swift-compiler-inspection-workflow` when the task needs the compiler AST, SIL, IR, module interfaces, or driver jobs.
- Hand macro target shape, compiler-plugin dependencies, permissions, generated build products, and Xcode package-plugin execution to the Apple Dev package-extension workflow.

## Output

Return the selected toolchain, SwiftSyntax products, transformation contract, preservation rules, changed artifacts, and fixture or build validation.

## Guardrails

- Do not present a SwiftSyntax tree as type-checked semantic truth.
- Do not replace structured rewriting with regular expressions for grammar-sensitive changes.
- Do not discard comments, whitespace, source locations, or inactive conditional regions accidentally.
- Do not pin a SwiftSyntax release without checking compatibility with the selected Swift toolchain.
- Do not introduce a macro when an ordinary library or build-time tool is simpler.
