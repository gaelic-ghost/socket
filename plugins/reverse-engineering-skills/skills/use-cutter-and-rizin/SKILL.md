---
name: use-cutter-and-rizin
description: Use Cutter for interactive Rizin-backed binary analysis and Rizin CLI for repeatable inspection, queries, scripts, and exports. Use when Codex must open a binary or shellcode, choose a loader, image, architecture, base address, or analysis preset; navigate functions, graphs, strings, sections, imports, exports, and references; record types, comments, flags, or renames; compare disassembly with available decompiler output; or hand GUI findings into reproducible Rizin commands.
---

# Use Cutter And Rizin

## Overview

Use Cutter as an interactive interface around Rizin and use Rizin CLI as the repeatable evidence surface. Detect the installed capability set before assuming a decompiler, debugger, architecture, or script binding exists.

Read [references/cutter-rizin-workflow.md](references/cutter-rizin-workflow.md) for capability checks, Apple-specific limits, evidence fields, and canonical documentation.

## Workflow

1. Preserve and preflight the artifact.
   - Record hash, format, architecture or slices, signing or encryption clues, and the research question.
   - Use the owning domain skill for bundle, Mach-O, .NET, or Unity context before import.

2. Discover capabilities.
   - Record Cutter version, embedded Rizin libraries, any working standalone Rizin CLI, installed analysis and decompiler plugins, supported architecture, debugger availability, and scripting or `rzpipe` surfaces.
   - Test an app-bundled CLI before relying on it. The executable may be present but unusable outside Cutter because of packaging, loader-path, signing, or environment constraints.
   - Do not assume Cutter's website feature list matches a development build or custom package.

3. Open the correct view.
   - Record input URI or file, loader, selected image and architecture, base address, analysis options, and writable or read-only mode.
   - Analyze universal slices separately.

4. Run bounded analysis.
   - Start with enough analysis to establish sections, functions, imports, exports, strings, references, and control flow.
   - Increase analysis depth only when the question requires it and record the changed setting.

5. Navigate and annotate.
   - Use disassembly, graph, hex, strings, types, cross-references, and available decompiler views together.
   - Record comments, flags, types, and proposed renames with evidence and confidence.

6. Verify generated output.
   - Compare decompiler output with disassembly, metadata, references, and call sites.
   - Use `review-decompiler-output` when a source-level conclusion depends on generated pseudocode.

7. Hand repeatable questions to Rizin.
   - Record exact commands or scripts for queries that should be rerunnable or compared across builds.
   - Detect structured-output and binding availability instead of inventing a dependency.

8. Preserve the session.
   - Save project state separately from the original artifact.
   - Record Cutter/Rizin versions, plugins, analysis settings, selected slice, image base, exports, screenshots, and name changes.

9. Keep debugging separate.
   - Record launch or attach requirements and platform protections before using the debugger.
   - Route Apple runtime work to `perform-apple-dynamic-analysis`.

## Guardrails

- Do not enable write mode, patch bytes, or save over the original without an explicit transformation request.
- Do not claim complete Swift, Objective-C, `arm64e`, chained-fixup, or dyld-cache recovery from one Cutter view.
- Do not present a selected `arm64` slice as covering `arm64e` or `x86_64`.
- Preserve disagreements between Cutter, Rizin CLI, another tool, and runtime evidence.

## Output

Return artifact identity, capability inventory, loader and analysis context, direct observations, annotations and renames, reproducible Rizin evidence, tool disagreements, and the next check.
