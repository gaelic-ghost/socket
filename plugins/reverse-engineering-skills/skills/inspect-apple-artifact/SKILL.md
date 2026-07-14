---
name: inspect-apple-artifact
description: Inspect Apple application bundles, extensions, frameworks, dylibs, static archives, XCFrameworks, IPA files, Mach-O executables, dSYMs, crash artifacts, dyld caches, kernel collections, IPSW files, or restore images without changing the original. Use when Codex must identify Apple container structure, executable and architecture slices, Mach-O load commands, UUIDs, imports, exports, rpaths, encryption, signing context, or the next Apple-specific analysis workflow.
---

# Inspect Apple Artifact

## Overview

Map an Apple container and its executable evidence before opening it in a decompiler. Preserve the distinction between file offsets, unslid virtual addresses, and slid runtime addresses.

Read [references/apple-artifact-and-macho.md](references/apple-artifact-and-macho.md) when interpreting Mach-O structures, Apple container types, command output, or source limitations.

## Workflow

1. Preserve and identify the input.
   - Work from a copy when extraction or a mutable tool project is needed.
   - Record file or container type, size, SHA-256, acquisition source, and original path.

2. Inspect the outer container first.
   - For a bundle, read `Info.plist`, locate `CFBundleExecutable`, record bundle/version/build identifiers, and inventory extensions, frameworks, plug-ins, resources, provisioning data, and nested executables.
   - For an IPA or archive, list members before extracting and retain member paths.
   - For an XCFramework, map platform and architecture variants before choosing a library.
   - For firmware, caches, or kernel collections, record the manifest, platform, hardware identity, build, and container UUIDs before extracting images.

3. Select the executable and slice deliberately.
   - Record Mach-O file type, CPU type and subtype, UUID, minimum OS, linked SDK clues, and encryption state for every relevant slice.
   - Do not treat an `arm64` slice as evidence for `arm64e` or `x86_64`.

4. Map Mach-O structure.
   - Record headers and load commands, segments and sections, entry point, imports, exports, linked libraries, rpaths, code-signature command, function starts, unwind data, relocations or chained fixups, and Objective-C or Swift metadata clues.
   - Use the `macho-map` record from `evidence-notes-workflow`.

5. Establish address conventions.
   - Label each address as file offset, unslid VM address, image-relative offset, or slid runtime address.
   - Preserve image load address and ASLR slide when correlating runtime or crash evidence.

6. Inspect identity and protection context without mutation.
   - Record code-signing identity, entitlements, provisioning clues, and encryption commands.
   - Route deeper signature and containment interpretation to `audit-apple-signing-and-containment`.

7. Choose the next workflow.
   - Runtime names or language structure: `recover-apple-runtime-metadata`.
   - dSYM, crash, or address matching: `correlate-apple-symbols-and-crashes`.
   - AArch64, `arm64e`, or pointer authentication: `analyze-apple-silicon-arm64e`.
   - dyld cache, dynamic analysis, kernel/firmware, or tool-specific work: use the focused owning skill.

## Guardrails

- Do not thin, re-sign, patch, decrypt, or normalize the only copy.
- Do not infer successful runtime access from declared entitlements.
- Do not assume open-source dyld, XNU, or format code exactly matches a shipping build without UUID, build, symbol, or behavior correlation.
- Do not call a parser failure proof that a load command, fixup, symbol, or metadata record is absent.

## Output

Return an artifact manifest, container inventory, Mach-O map, address convention, confirmed observations, unresolved parser or version questions, and the smallest next workflow.
