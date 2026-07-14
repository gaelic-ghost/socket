# Unity Artifact Analysis Reference

## Backend Decision

### Managed Or Mono

Look for managed assemblies, engine assemblies, runtime configuration, PDBs, and a `Managed` directory. Inspect assembly metadata and IL before high-level decompiler output.

### IL2CPP

Look for the platform's native player and generated-code library, commonly named `GameAssembly`, plus `global-metadata.dat`, Unity player data, symbols, and platform-specific native libraries. The exact layout and names vary by platform and Unity version.

IL2CPP converts managed assemblies through generated C++ into native binaries. Analysis therefore requires both native-code evidence and matching metadata. Generated function or type names produced by analysis tools are not original symbols unless verified.

## Build Manifest

- Platform, architecture, executable, and player library.
- Unity version clues and build timestamps.
- Scripting backend and stripping or optimization clues.
- Managed assembly hashes and references.
- Native library hashes, UUIDs or build IDs, and symbols.
- `global-metadata.dat` hash and version clues.
- Data directory, scenes, assets, resource archives, streaming assets, and plug-ins.
- Signing, bundle, or package identity for the target platform.

## Common Failure Modes

- Metadata and native library come from different builds.
- Tool supports an older metadata layout but silently produces partial names.
- Managed stripping removes expected members.
- Obfuscation changes identifiers before IL2CPP conversion.
- Architecture slice or platform loader is wrong.
- Asset parser version does not match serialized data.

## Official Sources

- [Unity IL2CPP scripting backend](https://docs.unity3d.com/Manual/scripting-backends-il2cpp.html)
- [Unity scripting backend overview](https://docs.unity3d.com/Manual/scripting-backends.html)
- [Unity managed code stripping](https://docs.unity3d.com/Manual/managed-code-stripping.html)
- [Unity documentation](https://docs.unity3d.com/)

Use the documentation version matching the identified Unity editor or player build when available.
