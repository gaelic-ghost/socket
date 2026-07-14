---
name: inspect-dotnet-assemblies
description: Inspect .NET and .NET Framework assemblies, managed PE files, CIL, manifests, metadata tables, resources, dependencies, target frameworks, runtimeconfig and deps files, portable or Windows PDBs, and generated decompiler output. Use when Codex must distinguish managed, mixed-mode, single-file, ReadyToRun, NativeAOT, or obfuscated artifacts; map types and members; compare IL with C# or another generated language view; or hand ordinary source repair and rebuilding to dotnet-skills.
---

# Inspect .NET Assemblies

## Overview

Establish whether the artifact contains inspectable managed metadata and IL before choosing a decompiler. Preserve manifest, runtime, dependency, symbol, and generated-output identity.

Read [references/dotnet-assembly-analysis.md](references/dotnet-assembly-analysis.md) for artifact shapes, metadata and symbol evidence, decompiler limits, and canonical sources.

## Workflow

1. Preserve and classify.
   - Record hash, PE architecture, CLI header and managed metadata presence, file version clues, signing or strong-name evidence, and supporting files.
   - Do not execute the assembly merely to learn its identity.

2. Inventory the deployment shape.
   - Record assembly manifest identity, modules, references, resources, target framework attributes, `.deps.json`, `.runtimeconfig.json`, config files, native libraries, and neighboring assemblies.
   - Distinguish framework-dependent, self-contained, single-file, ReadyToRun, NativeAOT, and mixed-mode clues without forcing every artifact into an IL workflow.

3. Match symbols.
   - Record portable or Windows PDB identity and source mapping evidence.
   - Keep embedded, adjacent, downloaded, or analyst-generated symbols distinct.

4. Inspect metadata before pseudocode.
   - Inventory assemblies, modules, namespaces, types, members, generic parameters, attributes, method signatures, resources, and references.
   - Record obfuscation, trimming, generated-code, async or iterator state-machine, and compiler-version clues.
   - If no safe non-executing metadata parser is available, stop after PE and CLI classification. Report which manifest, metadata, IL, strong-name, symbol, and dependency fields remain blocked rather than loading the assembly into the current process.

5. Compare IL and generated views.
   - Use CIL as the lower-level managed evidence and compare it with C#, F#, Visual Basic, or another decompiler rendering.
   - Route significant source-like conclusions through `review-decompiler-output`.

6. Map dependencies and behavior.
   - Trace calls, reflection strings, serialization names, P/Invoke entries, COM or native boundaries, and resource use.
   - Preserve unresolved assembly-binding and runtime-version questions.

7. Hand source projects, build failures, tests, package repair, or implementation changes to `dotnet-skills` after artifact analysis.

## Guardrails

- Do not load untrusted assemblies into the current process for metadata inspection when a non-executing parser is available.
- Do not claim NativeAOT or mixed-mode native code can be recovered through ordinary IL decompilation.
- Do not treat decompiler-generated C# as original source or assume generated state-machine names reflect source declarations.
- Do not resolve dependencies from unrelated local copies without recording the mismatch.

## Output

Return artifact and runtime shape, manifest and dependency map, symbol state, metadata observations, IL-versus-decompiler findings, native boundaries, uncertainty, and next workflow.
