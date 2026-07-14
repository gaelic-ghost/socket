---
name: use-hopper
description: Use Hopper on macOS for interactive disassembly, control-flow graphs, C-like pseudocode, Objective-C and Swift presentation, procedure and type editing, Python automation, supported extensions, and optional LLDB or GDB debugging. Use when Codex must create a Hopper document, choose a loader or architecture, navigate or annotate a binary, preserve analyst changes, compare Hopper output with another tool, or assess installed MCP, AI, debugger, and SDK capabilities before use.
---

# Use Hopper

## Overview

Use Hopper as a Mac-native interactive analysis document. Discover the installed edition and capabilities before relying on decompiler, debugger, scripting, SDK, AI, or MCP features.

Read [references/hopper-workflow.md](references/hopper-workflow.md) for capability and project records, Apple handoffs, and official sources.

## Workflow

1. Preserve and preflight.
   - Record artifact hash, format, architecture or slice, UUID or build ID, signing or encryption clues, and question.
   - Use the owning domain skill for Apple bundle, Mach-O, runtime, or symbol context.

2. Discover capabilities.
   - Record Hopper version, edition and license context, installed loaders and CPU backends, decompiler, debugger, Python, SDK extensions, and any AI or MCP surface.
   - Record whether a feature is present, configured, or merely documented for another release.

3. Create the analysis document.
   - Record loader, selected architecture and image, base address, analysis options, and document path.
   - Analyze universal slices separately.

4. Navigate and annotate.
   - Compare assembly, control-flow graph, pseudocode, strings, references, procedures, types, Objective-C and Swift views, and file metadata.
   - Record comments, procedure changes, types, and renames with evidence and confidence.

5. Automate narrowly.
   - Use Python or extension APIs for repeatable tasks only after verifying installed API behavior.
   - Record script, inputs, Hopper version, document state, and outputs.

6. Keep external and dynamic features explicit.
   - Treat LLDB or GDB debugging as a separate runtime stage.
   - Treat AI or MCP use as a separate data-flow decision; record what leaves the document and where it goes.

7. Preserve and compare.
   - Save the Hopper document separately from the original.
   - Preserve screenshots or minimal exports and compare important pseudocode claims with assembly or another tool.

## Guardrails

- Do not enable patching or overwrite the original without an explicit transformation request.
- Do not claim Hopper's Swift or Objective-C presentation is complete source recovery.
- Do not assume an MCP, AI, debugger, loader, or Python surface exists in the installed build.
- Do not transmit artifact data through an external integration without explicit approval.

## Output

Return artifact identity, Hopper capability inventory, document and analysis context, observations, annotations, automation or integration data flow, preserved state, and next verification. When the task stops at capability discovery, explicitly report `preflight only; no document created` and leave loader, analysis, decompiler, debugger, and integration behavior unverified.
