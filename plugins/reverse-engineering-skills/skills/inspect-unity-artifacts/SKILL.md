---
name: inspect-unity-artifacts
description: Inspect compiled Unity player, package, data, managed Mono, and IL2CPP artifacts across supported platforms. Use when Codex must identify Unity version and scripting backend; inventory player executables, UnityPlayer, managed assemblies, Assembly-CSharp, GameAssembly, global-metadata.dat, native libraries, symbols, resources, assets, scenes, or package clues; choose managed decompilation versus native IL2CPP analysis; or hand project authoring, profiling, builds, and source changes to game-dev-skills.
---

# Inspect Unity Artifacts

## Overview

Classify the player platform, Unity version, and scripting backend before selecting managed or native analysis. Preserve relationships among the player, data directory, metadata, libraries, symbols, and assets.

Read [references/unity-artifact-analysis.md](references/unity-artifact-analysis.md) for common layouts, backend decisions, IL2CPP evidence, asset boundaries, and official sources.

## Workflow

1. Preserve the complete build shape.
   - Record container and member hashes, platform, architecture, executable, data directory, Unity version clues, timestamps, symbols, and acquisition source.
   - Keep file relationships and relative paths intact in the working copy.
   - Classify the input as original player material, copied build content, extracted content, or a reconstructed/exported project. Record the extraction or reconstruction tool and version when known.

2. Identify the scripting backend.
   - Managed or Mono clues: `Managed/`, runtime libraries, and assemblies such as `Assembly-CSharp.dll`.
   - IL2CPP clues: native `GameAssembly` or platform equivalent plus `global-metadata.dat` and Unity player data.
   - Record mixed, stripped, obfuscated, or incomplete cases instead of forcing a choice.

3. Inventory code artifacts.
   - Managed: assembly identities, references, PDBs, target/runtime clues, generated code, and engine assemblies.
   - IL2CPP: player and native-library identity, metadata identity and version clues, symbols, architecture, exports, registration and metadata relationships, and platform-specific signing or Mach-O context.

4. Inventory data and resources.
   - Record scenes, serialized assets, resource archives, streaming assets, plug-ins, bundles, and package or catalog clues.
   - Keep asset parsing separate from code-behavior claims.

5. Choose the analysis path.
   - Use `inspect-dotnet-assemblies` for managed assemblies.
   - Use native and platform workflows for IL2CPP-generated code and the player.
   - Correlate metadata and native functions with exact tool versions and record generated names as tool output.

6. Preserve cross-artifact mappings.
   - Record which metadata record, managed identity, generated name, symbol, native function, asset, or scene supports each relationship.

7. Hand Unity project authoring, builds, profiling, package repair, or source changes to `game-dev-skills`.

## Guardrails

- Do not analyze one managed assembly without preserving its dependency and build context.
- Do not promote a reconstructed project's `ProjectVersion.txt`, managed directory, or generated project layout into a claim about the original player unless it is corroborated against original build artifacts.
- Do not treat IL2CPP-generated pseudocode as recovered C# source.
- Do not assume metadata and native libraries from different builds can be combined.
- Do not run an untrusted player as an implied inspection step.
- Do not conflate asset extraction with permission to redistribute the assets.

## Output

Return build manifest, platform and Unity version clues, scripting-backend classification, code and asset inventories, symbol state, chosen workflow, cross-artifact mappings, uncertainty, and next check.
