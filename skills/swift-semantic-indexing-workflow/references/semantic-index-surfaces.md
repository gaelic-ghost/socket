# Swift Semantic And Index Surfaces

## Raw SourceKit

Use for live compiler-backed requests such as completion, cursor information, documentation, generated interfaces, structure, types, and indexing. Supply the source snapshot, correct byte position, and the compiler arguments required to resolve every dependency.

Raw SourceKit is a low-level integration. Isolate request dictionaries and response keys behind typed adapters, enforce timeouts and cancellation, and keep crash or service-restart behavior visible to the caller.

## SourceKitten

Use when a Swift framework or CLI that emits JSON materially simplifies an accepted integration. Its commands cover completion, documentation, indexing, module information, raw requests, structure, and syntax. It resolves SourceKit from the surrounding toolchain, so verify that resolution before trusting results.

SourceKitten is not bundled with Swiftly or Xcode and is not a substitute for a source-accurate SwiftSyntax rewrite or a standards-based LSP client.

## Compiler Index Store And IndexStoreDB

The compiler writes raw index data while building. IndexStoreDB reads that data and maintains acceleration tables for symbol, occurrence, and relation queries.

Use it for project-wide questions only after verifying:

- every relevant target produced index data
- generated files were present
- path prefix mappings match the current checkout
- the database processed current units
- configuration and conditional flags match the question

An absent occurrence means only that the inspected index does not contain it. It is not proof of whole-program absence.

## Position Discipline

- SourceKit commonly uses UTF-8 byte offsets tied to one source snapshot.
- Index data uses compiler-recorded locations and paths.
- LSP uses negotiated position encodings and document versions.

Convert positions once at a named boundary and test Unicode scalars, extended grapheme clusters, and edits before the query position.

## Authoritative Sources

- [SourceKit protocol](https://github.com/swiftlang/swift/blob/main/tools/SourceKit/docs/Protocol.md)
- [IndexStoreDB](https://github.com/swiftlang/indexstore-db)
- [SourceKitten](https://github.com/jpsim/SourceKitten)
