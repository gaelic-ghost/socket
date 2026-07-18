---
name: sourcekit-lsp-workflow
description: Configure or diagnose SourceKit-LSP across SwiftPM, compilation databases, and build servers. Use for completion, navigation, refactoring, diagnostics, semantic tokens, indexing, generated files, or editor-client failures.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
  hermes:
    category: swift-language
    tags: [swift, sourcekit-lsp, lsp, editor, indexing]
---

# SourceKit-LSP Workflow

Treat SourceKit-LSP as an editor protocol server whose semantic quality depends on matching toolchain, build settings, modules, generated files, and index state.

## Workflow

1. Identify the client, workspace root, requested LSP feature, project model, and whether the failure is startup, build-settings, semantic, index, protocol, or client presentation.
2. Resolve the intended server and compiler together:
   - inspect Swiftly's selected location, `sourcekit-lsp`, and Swift version
   - inspect `xcode-select`, `xcrun --find sourcekit-lsp`, and `xcrun swiftc --version`
   - use Swiftly for Swift.org toolchains and cross-platform SwiftPM work
   - use Xcode's server for Apple SDK and Xcode-selected toolchain behavior
3. Confirm workspace integration:
   - native SwiftPM workspace
   - `compile_commands.json` or `compile_flags.txt`
   - Build Server Protocol provider
   - fallback settings only for intentionally unmanaged files
4. Confirm the client completed `initialize`, opened the document before document requests, preserved the process environment, and framed JSON-RPC messages correctly.
5. Check build settings, generated files, module preparation, last successful build, index-store production, index freshness, and background-indexing policy.
6. Reproduce with logging or the built-in `diagnose` bundle before clearing caches or changing configuration. Read [references/sourcekit-lsp-diagnostics.md](references/sourcekit-lsp-diagnostics.md) for the ordered diagnosis path.
7. Treat `.sourcekit-lsp/config.json` as version-sensitive. Verify options against the selected server before adding or changing them.
8. Report server, compiler, project model, failing request, logs, build/index state, correction, and remaining client-specific behavior.

## Toolchain Contract

- Keep SourceKit-LSP, `sourcekitd`, compiler, SDK, plugins, and built modules from one coherent toolchain selection.
- Record both Swiftly and Xcode resolution on macOS even when they currently report the same Swift version.
- When Swiftly selects `xcode`, confirm which Xcode is selected rather than treating the proxy as an independent toolchain.
- Do not hard-code an Xcode application or toolchain path; resolve it through the configured selection.
- Do not change the global toolchain merely to test a hypothesis without explicit user intent.

## Boundaries

- Use `swift-semantic-indexing-workflow` for direct SourceKit or IndexStoreDB application integrations that do not need LSP.
- Use `swift-compiler-inspection-workflow` for compiler phases and emitted artifacts.
- Hand Xcode-hosted coding-agent setup to `xcode-coding-intelligence-workflow` and Xcode build execution to `xcode-build-run-workflow`.

## Guardrails

- Do not blame the editor before checking server logs, build settings, generated files, and index freshness.
- Do not expect cross-module results from modules that have not been prepared or indexed.
- Do not run SourceKit-LSP inside a restricted application sandbox unless the host deliberately provides the required developer-tool access.
- Do not assume one stdout read equals one LSP packet; buffer and parse by protocol framing.
- Do not expose mirrored LSP traffic or diagnostic bundles without checking them for source and environment data.
