---
name: use-malimite
description: Use Malimite as a Ghidra-backed Apple app-package exploration front end for supported IPA files and copied ZIP or application-bundle inputs. Use when Codex must inspect bundle metadata, resources, provisioning data, classes, functions, strings, entry points, cross-references, reconstructed Swift or Objective-C views, or optional generated method translations while preserving Malimite, Java, Ghidra, project-database, privacy, and unsupported-format evidence.
---

# Use Malimite

## Overview

Use Malimite for supported Apple app-package navigation, not as a general standalone Mach-O decompiler. Preflight encryption, container shape, universal slices, prerequisites, network exposure, and Ghidra compatibility before analysis.

Read [references/malimite-workflow.md](references/malimite-workflow.md) for the currently verified capability and limitation baseline, privacy boundaries, and canonical sources.

## Workflow

1. Preserve and preflight.
   - Copy and hash the input.
   - Record bundle executable, architecture slices and subtypes, UUID, signing, provisioning, and encryption state.
   - Route encrypted code, unsupported bare Mach-O, or unsupported universal formats before import.

2. Verify the toolchain.
   - Record exact Malimite, Java, and Ghidra versions.
   - Verify the release bundle and its Ghidra bridge remain together and that the configured Ghidra headless analyzer is available.
   - Do not mutate a Ghidra installation or elevate privileges without explaining the exact operation and obtaining approval.

3. Isolate untrusted analysis.
   - Use a dedicated working area and consider offline or firewall-isolated execution.
   - Inspect listener exposure before analyzing hostile input.

4. Import a supported package.
   - Prefer IPA or copied ZIP input.
   - If direct `.app` selection fails, try drag and drop or a copied ZIP wrapper and record the workaround.
   - Choose a universal slice explicitly and record library-filter and analysis options.

5. Navigate generated results.
   - Inspect bundle and provisioning metadata, resources, classes, functions, strings, entry points, search results, cross-references, and supported nested executables.
   - Attribute C-like pseudocode to Ghidra and reconstructed names or grouping to Malimite.

6. Review interpretation layers.
   - Keep direct metadata, Ghidra output, Malimite heuristics, manual edits, and LLM-generated translations separate.
   - Verify important conclusions in disassembly or a second tool.

7. Preserve generated state.
   - Record adjacent project files, `project.json`, SQLite database, screenshots, snippets, and any manual edits.
   - Do not promise bulk decompiled-source export.

8. Route failures.
   - Use Cutter, Ghidra, or Hopper for bare Mach-O, richer analyzer control, graphs, symbols, persistent project state, patching, or deep instruction work.

## Guardrails

- Do not claim Malimite decrypts App Store executables.
- Do not describe heuristic Swift recovery or LLM output as recovered source.
- Do not claim iOS/macOS 26, beta, `arm64e`, PAC, or chained-fixup support without artifact-level verification.
- Do not transmit selected decompiled code to a hosted model without explicit destination and data approval.
- Do not store a sensitive long-lived API key in Malimite's built-in storage.

## Output

Return artifact preflight, toolchain versions, isolation state, import options, direct metadata, generated analysis layers, preserved project artifacts, failures, and handoffs.
