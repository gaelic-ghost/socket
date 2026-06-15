---
name: triage-artifact
description: Classify compiled artifacts before deeper reverse engineering. Use when Codex needs to inspect an unknown or mixed artifact set such as binaries, app bundles, frameworks, dylibs, DLLs, EXEs, Unity build outputs, IL2CPP metadata, archives, symbol files, crash logs, decompiler output, or disassembler output and choose the next technical workflow without mutating original inputs.
---

# Triage Artifact

## Overview

Use this skill to make the first technical pass over unknown compiled artifacts. The output should identify what the artifact appears to be, which supporting files matter, what can be inspected next, and which owner skill should take over.

## Workflow

1. Preserve the input shape.
   - Do not edit original artifacts during triage.
   - If a working area is needed, copy artifacts into a clearly named scratch or analysis directory and keep the original path visible in notes.
   - Record stable identifiers when useful: file names, sizes, timestamps from the filesystem, bundle identifiers, UUIDs, versions, checksums, or archive member paths.

2. Identify containers before internals.
   - Check whether the input is a single file, directory tree, app bundle, framework, package, archive, symbol bundle, crash log, metadata file, or generated decompiler output.
   - For archives, inspect the member list before extracting broadly.
   - For app or framework bundles, inspect metadata files before jumping into the main executable.

3. Classify runtime and platform clues.
   - Apple: look for `.app`, `.framework`, `.dylib`, `.appex`, `Info.plist`, entitlements, Mach-O slices, dSYM bundles, crash logs, Swift symbols, Objective-C class names, linked frameworks, and UUID matches.
   - .NET: look for `.dll`, `.exe`, `.deps.json`, `.runtimeconfig.json`, target framework metadata, PDB files, NuGet package clues, and managed assembly metadata.
   - Unity: look for `UnityPlayer`, `GameAssembly`, `global-metadata.dat`, `Managed/`, `Assembly-CSharp.dll`, `Data/`, `Resources/`, and platform-specific player layouts.
   - Native or mixed binaries: look for architecture, debug sections, symbol tables, strings, linked libraries, imports/exports, resources, and packed or nested payloads.

4. Choose the next workflow by artifact shape.
   - Use `reverse-engineering:evidence-notes-workflow` when the user needs a durable analysis log or handoff.
   - Use future .NET, Unity, Apple binary, tool-selection, or decompiler-output skills when those surfaces exist and the artifact clearly fits them.
   - Use `dotnet-skills` for ordinary .NET project repair, rebuild, test, or package work after source/project files are available.
   - Use `apple-dev-skills` for ordinary Swift, Objective-C, Xcode, signing, simulator, or package work after the task stops being artifact analysis.

5. Report with uncertainty intact.
   - Separate observed facts from likely inferences.
   - Name the command or tool that produced each important observation.
   - Prefer "appears to be," "contains," "exports," "links," or "matches" over source-level claims that triage cannot prove.
   - End with the smallest useful next inspection step.

## Useful Local Checks

Use the narrowest checks that fit the host and artifact. Do not run every command by default.

```bash
file <artifact>
ls -la <path>
find <path> -maxdepth 3 -type f | sort
shasum -a 256 <artifact>
strings <artifact> | head
```

Apple-focused checks when the artifact is Mach-O or an Apple bundle:

```bash
plutil -p <bundle>/Info.plist
lipo -info <binary>
otool -L <binary>
otool -l <binary>
codesign -dvvv <bundle-or-binary>
dwarfdump --uuid <binary-or-dsym>
```

.NET-focused checks when the artifact is a managed assembly or .NET app:

```bash
dotnet --info
dotnet <assembly>.dll --help
```

Use dedicated decompilers or disassemblers only after the artifact shape justifies them. Record the tool name and version when possible.

## Output Shape

Return a concise triage note:

```markdown
## Artifact
- Path:
- Original preserved: yes/no
- Type:
- Size/checksum:

## Observations
- ...

## Inferences
- ...

## Useful Supporting Files
- ...

## Recommended Next Step
...
```
