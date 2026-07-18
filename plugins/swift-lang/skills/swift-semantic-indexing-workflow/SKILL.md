---
name: swift-semantic-indexing-workflow
description: Query Swift types, USRs, cursor information, documentation, symbol occurrences, references, and relationships with SourceKit, SourceKitten, compiler index stores, and IndexStoreDB. Use when syntax alone cannot answer a file-local semantic or project-wide symbol question.
license: Apache-2.0
metadata:
  owner: gaelic-ghost
  repo: socket
  category: swift-language
  hermes:
    category: swift-language
    tags: [swift, sourcekit, sourcekitten, indexstore, semantics]
---

# Swift Semantic Indexing Workflow

Choose between live file semantics and persisted project-wide index data without substituting syntax shape for type-checked meaning.

## Workflow

1. State the semantic question and required scope:
   - one source snapshot at a byte position
   - one file or module
   - project-wide occurrences and relations
   - documentation or generated interface
2. Resolve the toolchain that produced or should interpret the source:
   - use Swiftly for matching Swift.org toolchains and cross-platform SwiftPM builds
   - use Xcode's `xcrun` tools and `sourcekitd` for Apple SDK or Xcode build settings
   - never load `sourcekitd` from one toolchain while passing compiler or plugin paths from another
3. Choose the surface using [references/semantic-index-surfaces.md](references/semantic-index-surfaces.md):
   - raw SourceKit for precise live semantic requests
   - SourceKitten for an accepted Swift or JSON convenience layer
   - compiler index store plus IndexStoreDB for project-wide symbols, occurrences, and relations
   - SourceKit-LSP when a standard editor-facing protocol already covers the request
4. Reconstruct exact compiler arguments from the real build. Include target, SDK, module search paths, language mode, conditional flags, generated sources, bridging inputs, and plugins when applicable.
5. Keep the source text and position representation paired. Record whether positions are UTF-8 byte offsets, line and column pairs, or LSP positions.
6. Verify build and index freshness before interpreting missing results.
7. Normalize output into typed domain records at the integration boundary instead of spreading SourceKit keys or loose JSON dictionaries through the application.
8. Test absent symbols, overloads, extensions, generated code, conditional compilation, and stale-index behavior.

## SourceKitten Policy

- Treat SourceKitten as a third-party wrapper and CLI around SourceKit, not as the source of semantic truth.
- Use it when its `structure`, `syntax`, `doc`, `index`, `complete`, or raw-request JSON contract matches a concrete integration need.
- Check installation and toolchain resolution before use; do not assume SourceKitten is bundled with Swiftly or Xcode.
- Prefer a direct supported library or LSP contract when adding SourceKitten would only translate one unstable representation into another.

## Output

Return semantic scope, selected toolchain, selected surface, compiler-argument source, position encoding, index freshness, query result, and uncertainty.

## Guardrails

- Do not answer inferred-type or reference questions from SwiftSyntax alone.
- Do not treat a missing index result as proof that a symbol is unused before verifying every relevant target was indexed.
- Do not reuse byte offsets after source text changes.
- Do not pass machine-local SourceKit or SDK paths into shared package manifests.
- Do not let raw SourceKit dictionaries become a public application API.
