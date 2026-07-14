# .NET Assembly Analysis Reference

## Supporting Artifact Inventory

- Managed `.dll` or `.exe` plus PE and CLI metadata identity.
- Assembly manifest name, version, culture, public-key or strong-name token.
- Referenced assemblies and native libraries.
- Target framework and runtime configuration.
- `.deps.json`, `.runtimeconfig.json`, app config, and NuGet package clues.
- Portable, embedded, or Windows PDB identity.
- ReadyToRun, single-file, NativeAOT, mixed-mode, trimming, or obfuscation clues.

## Evidence Order

1. PE and CLI headers.
2. Assembly manifest and metadata tables.
3. CIL and exception regions.
4. Symbols and source mapping.
5. Generated high-level code.
6. Runtime observation when static evidence is insufficient.

MetadataLoadContext can inspect assembly metadata without ordinary execution semantics, but dedicated parsers and decompilers can be safer for untrusted inputs. Record the exact tool and whether dependency resolution loaded external files.

## Decompiler Limits

- Async and iterator state machines may be rewritten into source-like constructs.
- Closures, anonymous types, records, interpolated strings, and pattern matching can be reconstructed differently by tools.
- Nullable annotations, tuple names, and parameter names depend on metadata and symbols.
- Obfuscation and trimming can destroy names or relationships.
- ReadyToRun can contain both IL and native code; NativeAOT may require native analysis.

## Canonical Sources

- [.NET assemblies](https://learn.microsoft.com/dotnet/standard/assembly/)
- [.NET metadata and self-description](https://learn.microsoft.com/dotnet/standard/metadata-and-self-describing-components)
- [MetadataLoadContext](https://learn.microsoft.com/dotnet/standard/assembly/inspect-contents-using-metadataloadcontext)
- [ECMA-335 Common Language Infrastructure](https://ecma-international.org/publications-and-standards/standards/ecma-335/)
- [ILSpy](https://github.com/icsharpcode/ILSpy)

Use the runtime and tool documentation that matches the artifact generation when format or symbol behavior changed across .NET versions.
