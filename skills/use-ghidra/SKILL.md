---
name: use-ghidra
description: Create Ghidra projects for compiled artifacts. Use for import, loader and analyzer choices, listings, functions, symbols, types, references, graphs, decompiler review, scripts, headless analysis, PyGhidra, comparisons, and archives.
metadata:
  hermes:
    category: reverse-engineering
    tags: [ghidra, decompilation, static-analysis]
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

5. Choose the execution surface.
   - Use CodeBrowser when the work needs visual navigation, graph review, annotations, types, or a saved analyst checkpoint.
   - Use `analyzeHeadless` when import, analyzer selection, scripts, and exports must be repeatable in a batch or CI-like run. Keep the input, project directory, script, arguments, and emitted files together.
   - Use PyGhidra only when Python is the narrowest way to query or transform a direct Ghidra program. Record the Python environment and exact API calls.
   - Do not treat a headless or PyGhidra run as equivalent to a reviewed GUI project until its generated state has been opened or otherwise verified.

6. Review multiple views.
   - Compare memory map, listing, functions, symbols, references, data types, graphs, and decompiler output.
   - Track manual function creation, types, comments, bookmarks, and renames with evidence.

7. Automate repeatable work.
   - Use supported scripts, PyGhidra, or headless analysis when the task benefits from deterministic queries or batch processing.
   - Record script source, parameters, Ghidra version, project, and outputs.

8. Preserve and hand off.
   - Save or archive project state with the artifact and tool context.
   - Export only the evidence needed for notes and preserve generated pseudocode attribution.

## Guardrails

- Do not run an outdated Ghidra release without checking current advisories.
- Do not accept an auto-selected language, base address, or analyzer set without verifying it against the artifact.
- Do not mix a direct Ghidra project with a tool that happens to invoke Ghidra internally; their retained state, analyzer controls, and evidence differ.
- Do not make batch scripts modify the only project copy. Preserve a known checkpoint before transformations.
- Do not attribute Malimite output to a persistent Ghidra project unless the project was actually opened and preserved.
- Do not present decompiler output as original source.

## Output

Return installation identity, project and import context, analyzer set, observations, analyst transformations, automation evidence, archived state, and unresolved loader or decompiler questions. When the task stops at capability discovery, explicitly report `preflight only; no project created` and leave loader, language, analyzer, and decompiler results unverified.
