# Swift Language Tool Selection Matrix

## Information Models

| Required answer | Primary surface | Avoid as primary |
| --- | --- | --- |
| Tokens, trivia, declarations, structural rewrite | SwiftParser and SwiftSyntax | Compiler AST dumps, raw text replacement |
| Parse or type-check diagnostics, lowering, emitted artifacts | `swiftc` and swift-driver | SourceKitten structure output |
| Live inferred type, completion, cursor info, documentation | SourceKit or SourceKit-LSP | SwiftSyntax |
| Project-wide definitions, references, occurrences, relations | Compiler index store and IndexStoreDB | One-file SourceKit structure request |
| Editor-neutral completion, navigation, refactoring, diagnostics | SourceKit-LSP | Custom raw SourceKit protocol client |
| JSON convenience over SourceKit | SourceKitten | Treating its schema as compiler-stable |

## Stability Classes

- `Supported library or protocol`: SwiftSyntax package APIs, LSP, documented compiler-driver options, and IndexStoreDB public APIs within their supported versions.
- `Version-sensitive integration`: SourceKit request keys, SourceKit-LSP configuration, SourceKitten JSON, symbol and index schemas, and SwiftSyntax release alignment.
- `Compiler internal`: direct `swift-frontend` invocation, debug-only flags, and AST or lowering dumps without a documented compatibility promise.

## Toolchain Resolution

Use Swiftly when a `.swift-version`, `swiftly use`, Swift.org release, snapshot, or cross-platform package owns the task. Use Xcode through `xcrun` when Apple SDKs, selected Xcode build settings, or Xcode-bundled SourceKit own it.

On macOS, collect both sets of evidence before choosing:

```text
command -v swift
swift --version
swiftly use --print-location
xcode-select -p
xcrun --find swiftc
xcrun swiftc --version
xcrun --find sourcekit-lsp
```

Do not interpret matching version strings as proof that resolved libraries, SDKs, plugins, and modules are interchangeable.

## Authoritative Sources

- [Swift compiler](https://www.swift.org/documentation/swift-compiler/)
- [SwiftSyntax](https://github.com/swiftlang/swift-syntax)
- [SourceKit protocol](https://github.com/swiftlang/swift/blob/main/tools/SourceKit/docs/Protocol.md)
- [SourceKit-LSP](https://github.com/swiftlang/sourcekit-lsp)
- [IndexStoreDB](https://github.com/swiftlang/indexstore-db)
- [Swift compiler driver](https://github.com/swiftlang/swift-driver)
- [SourceKitten](https://github.com/jpsim/SourceKitten)
- [Swiftly](https://github.com/swiftlang/swiftly)
