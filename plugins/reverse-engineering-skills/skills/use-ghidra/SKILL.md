---
name: use-ghidra
description: Create and maintain reproducible Ghidra analysis projects for compiled artifacts. Use when Codex must import a binary, select a format, language, compiler specification, image base, or analyzer set; inspect listings, functions, symbols, types, references, graphs, memory maps, or decompiler output; apply scripts or headless analysis; compare programs; archive project state; or distinguish direct Ghidra work from Ghidra-backed output produced by another tool.
---

# Use Ghidra

## Overview

Use a copied artifact and a recorded project configuration. Treat the loader, language, analyzer set, symbol inputs, and Ghidra version as part of the evidence.

Read [references/ghidra-workflow.md](references/ghidra-workflow.md) for project records, analyzer and headless boundaries, security checks, and canonical sources.

## Workflow

1. Verify the installation.
   - Record Ghidra version, release source, Java runtime, installed extensions, processor modules, and relevant security advisories.
   - Do not extract a new release over an existing installation.

2. Preserve and classify the artifact.
   - Record hash, format, architecture, runtime, symbols, and the research question.
   - Use the owning domain skill before choosing specialized loader options.

3. Create project state.
   - Record project type and path, imported filename, loader, language and compiler specification, image base, selected segments or overlays, and symbol inputs.
   - Keep project files separate from original inputs.

4. Configure analysis deliberately.
   - Record enabled and disabled analyzers and any non-default options.
   - Start with a bounded baseline and rerun only the analyses needed for the question.

5. Review multiple views.
   - Compare memory map, listing, functions, symbols, references, data types, graphs, and decompiler output.
   - Track manual function creation, types, comments, bookmarks, and renames with evidence.

6. Automate repeatable work.
   - Use supported scripts, PyGhidra, or headless analysis when the task benefits from deterministic queries or batch processing.
   - Record script source, parameters, Ghidra version, project, and outputs.

7. Preserve and hand off.
   - Save or archive project state with the artifact and tool context.
   - Export only the evidence needed for notes and preserve generated pseudocode attribution.

## Guardrails

- Do not run an outdated Ghidra release without checking current advisories.
- Do not accept an auto-selected language, base address, or analyzer set without verifying it against the artifact.
- Do not attribute Malimite output to a persistent Ghidra project unless the project was actually opened and preserved.
- Do not present decompiler output as original source.

## Output

Return installation identity, project and import context, analyzer set, observations, analyst transformations, automation evidence, archived state, and unresolved loader or decompiler questions. When the task stops at capability discovery, explicitly report `preflight only; no project created` and leave loader, language, analyzer, and decompiler results unverified.
