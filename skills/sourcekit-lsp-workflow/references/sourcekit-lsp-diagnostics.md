# SourceKit-LSP Diagnosis Order

## 1. Process And Toolchain

- Resolve the exact `sourcekit-lsp` executable.
- Resolve its sibling compiler and SourceKit libraries.
- Record Swiftly selection and Xcode selection separately.
- Confirm the server starts with the environment it needs.

## 2. Protocol Lifecycle

- Confirm `initialize` and `initialized` completed.
- Confirm the client opened a document before document requests.
- Confirm document versions and position encodings remain coherent.
- Confirm JSON-RPC headers and content lengths are parsed from a stream rather than assumed to align with stdout reads.
- Confirm cancellation and shutdown are handled.

## 3. Build System

- SwiftPM: confirm package root, resolved dependencies, selected traits and configuration, scratch path, target triple, SDK, and extra flags.
- Compilation database: confirm search path, absolute file coverage, and current commands.
- Build server: confirm target discovery, source membership, build settings, and response timeouts.
- Fallback settings: use only for files intentionally outside a managed target.

## 4. Modules, Generated Files, And Index

- Confirm dependencies and generated sources exist.
- Confirm the project was built or prepared for indexing with matching settings.
- Confirm index data is current and paths map to the active checkout.
- Distinguish file-local semantic success from missing cross-module results.

## 5. Logs And Diagnostic Bundle

Use SourceKit-LSP logging and its `diagnose` subcommand before deleting caches. Record the failing method, request position, workspace, server version, and relevant response or timeout. Inspect bundles and mirrored traffic for source text, paths, environment data, and other sensitive content before sharing.

## 6. Configuration

Verify every `.sourcekit-lsp/config.json` option against the selected server. The configuration structure is explicitly version-sensitive; unknown keys may be ignored, and renamed settings can create convincing but ineffective configurations.

## 7. Correction And Proof

Apply the smallest correction, restart only the affected server when required, reproduce the original request, and verify both file-local and cross-module behavior relevant to the failure.

## Authoritative Sources

- [SourceKit-LSP repository](https://github.com/swiftlang/sourcekit-lsp)
- [SourceKit-LSP documentation](https://github.com/swiftlang/sourcekit-lsp/tree/main/Documentation)
- [Language Server Protocol 3.17](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/)
