---
name: correlate-apple-symbols-and-crashes
description: Match Apple binaries, dSYMs, BCSymbolMaps when applicable, crash reports, IPS logs, panic excerpts, and static-analysis databases by UUID, architecture, load address, and exact build. Use when Codex must symbolicate or assess partial symbolication, translate crash addresses, correlate runtime frames with Mach-O functions, validate archived symbols, or hand a supported finding into Xcode or deeper reverse engineering.
---

# Correlate Apple Symbols And Crashes

## Overview

Prove binary and symbol identity before translating addresses. Preserve every address convention and the source of each recovered name.

Read [references/apple-symbol-and-crash-correlation.md](references/apple-symbol-and-crash-correlation.md) when interpreting crash fields, UUID matching, ASLR arithmetic, symbol sources, or Apple symbolication tools.

## Workflow

1. Preserve the report and binaries.
   - Record crash or IPS file hash, timestamp, incident identifier, process, OS build, device model, architecture, and report source.
   - Preserve candidate binaries and symbol bundles unchanged.

2. Identify the crashed image.
   - Record binary name, bundle identifier and version, UUID, architecture, load address, image range, and path from the report.
   - Do not assume the main executable owns a frame from a framework, extension, dyld cache, or translated image.

3. Match symbols by identity.
   - Compare the report image UUID to the binary and dSYM DWARF UUID for the same architecture.
   - Reject same-name or same-version candidates with a different UUID.
   - Record whether names come from the binary, dSYM, runtime metadata, system symbols, or an analyst database.

4. Establish address arithmetic.
   - Preserve reported runtime address, image load address, preferred image address when needed, ASLR slide, and image-relative offset.
   - Confirm which address form the selected tool expects before symbolication.

5. Symbolicate narrowly.
   - Start with the relevant frame or image rather than rewriting the complete report blindly.
   - Record exact commands, Xcode archive or symbol source, architecture, and output.
   - Preserve unsymbolicated and partially symbolicated frames.

6. Correlate with static analysis.
   - Translate the verified image-relative location into the analysis database's address convention.
   - Compare function boundaries, symbols, disassembly, and runtime metadata.
   - Record an analyst rename separately from a symbolicated name.

7. Assess confidence.
   - Confirmed: UUID, architecture, address convention, and symbol source match.
   - Partial: image match is sound but symbol, inline, or optimization evidence is incomplete.
   - Unresolved: candidate binary, dSYM, slide, system symbol, or address convention remains uncertain.

8. Hand off ordinary Xcode crash debugging or source fixes to `apple-dev-skills` after the artifact correlation is complete.

## Guardrails

- Do not force symbolication with a UUID-mismatched dSYM.
- Do not subtract a slide twice or mix image-relative and absolute runtime addresses.
- Do not treat the nearest symbol as proof that the instruction belongs to that source line or inlined function.
- Do not present a system-framework name recovered from a different OS build as exact evidence.

## Output

Return matched artifact identities, address translation, symbol sources, correlated frames, confidence, unresolved images, and the next verification step.
