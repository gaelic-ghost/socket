---
name: choose-swift-language-tooling
description: Choose between SwiftSyntax, swiftc and swift-driver, SourceKit or SourceKitten, IndexStoreDB, and SourceKit-LSP by required information model and project shape. Use before building, debugging, or automating Swift language tooling, especially when Swiftly and Xcode toolchains may resolve different binaries.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
  hermes:
    category: swift-language
    tags: [swift, tooling, sourcekit, swiftsyntax, lsp]
---

# Choose Swift Language Tooling

Route Swift tooling by the information the task needs. Resolve toolchain ownership before interpreting output.

## Workflow

1. Inspect repository guidance, `Package.swift`, Xcode project markers, build configuration, generated sources, and existing tooling dependencies.
2. Resolve the active toolchain without changing it:
   - record `command -v swift`, `command -v swiftc`, and `swift --version`
   - record `swiftly use --print-location` when Swiftly is installed
   - record `xcode-select -p`, `xcrun --find swiftc`, and `xcrun swiftc --version` on macOS
   - label each command and artifact as `Swiftly`, `Xcode`, or another explicitly named toolchain
3. Choose one primary information model:
   - source-accurate syntax and rewriting: `swift-syntax-tooling-workflow`
   - compilation, diagnostics, AST, SIL, IR, modules, or driver jobs: `swift-compiler-inspection-workflow`
   - types, USRs, documentation, occurrences, or symbol relationships: `swift-semantic-indexing-workflow`
   - editor protocol, completion, navigation, refactoring, or language-service diagnosis: `sourcekit-lsp-workflow`
4. Resolve the project model:
   - SwiftPM package
   - Xcode project or workspace
   - compilation database
   - build server
   - loose source file with explicit compiler arguments
5. State why the selected surface answers the question and why the nearest alternative does not.
6. Hand build, test, package-plugin, macro-package, signing, simulator, or device execution to the owning Apple Dev or server-side workflow.

## Toolchain Contract

- Treat Swiftly and Xcode as separate first-class Swift toolchain owners.
- Use Swiftly-resolved tools for cross-platform Swift.org packages, CLI work, explicit `.swift-version` selection, and toolchain-version matrices unless repository guidance selects Xcode.
- Use `xcrun`-resolved tools when the task depends on an Apple SDK, selected Xcode, Xcode build settings, or Xcode-bundled SourceKit behavior.
- Recognize that `swiftly use xcode` makes Swiftly proxy the currently selected Xcode toolchain; still record both the Swiftly selection and `xcode-select` result.
- Do not mix a compiler from one toolchain with `sourcekitd`, SourceKit-LSP, SDKs, plugins, or SwiftSyntax libraries from another and call the result valid.
- Do not change `swiftly use`, `.swift-version`, `xcode-select`, Xcode settings, or `DEVELOPER_DIR` merely to inspect state.

## Output

Return:

1. `Toolchain ownership`: Swiftly, Xcode, or another named owner for every selected binary.
2. `Information model`: syntax, compiler artifact, semantic query, index, or LSP.
3. `Project model`: SwiftPM, Xcode, compilation database, build server, or loose file.
4. `Selected workflow`: one primary skill and any required handoff.
5. `Evidence`: versions, resolved paths, build settings, and freshness of generated modules or indexes.

## Guardrails

- Do not use SwiftSyntax to claim inferred types or project-wide references.
- Do not parse unstable compiler dumps when a supported library or protocol answers the question.
- Do not use raw SourceKit when LSP or SourceKitten already supplies the required contract with acceptable fidelity.
- Do not treat SourceKitten as a replacement for SwiftSyntax, SourceKit-LSP, or the compiler.
- Do not diagnose semantic or LSP failures before checking compiler arguments and build-state freshness.

Read [references/tool-selection-matrix.md](references/tool-selection-matrix.md) for the detailed routing matrix and stability classes.
