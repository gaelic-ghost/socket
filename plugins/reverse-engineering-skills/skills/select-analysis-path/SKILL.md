---
name: select-analysis-path
description: Choose the smallest useful reverse-engineering workflow from an artifact's format, runtime, platform, available evidence, and research question. Use when Codex must decide between metadata inspection, static analysis, decompilation, disassembly, symbol or crash correlation, resource inspection, dynamic analysis, version comparison, or a tool-specific workflow for binaries, bundles, assemblies, firmware, or generated analysis output.
---

# Select Analysis Path

## Overview

Route an artifact to the least invasive workflow that can answer the stated question. Choose from evidence needs rather than tool preference.

## Workflow

1. Establish the question.
   - State the behavior, identity, relationship, or difference being investigated.
   - Separate a request for facts from a request to patch, execute, debug, or transform an artifact.

2. Establish artifact identity.
   - Use `triage-artifact` when format, container, architecture, runtime, or supporting files are uncertain.
   - Preserve the original and record a hash before extraction, thinning, re-signing, or import into a mutable project.

3. Choose the evidence class.
   - Metadata inspection: identity, architecture, dependencies, signing, sections, resources, or build clues.
   - Static analysis: control flow, references, strings, types, algorithms, or recovered runtime metadata.
   - Symbol correlation: dSYMs, PDBs, crash logs, addresses, or analyst databases.
   - Dynamic analysis: runtime-only state, generated data, environment-dependent behavior, or a static hypothesis requiring observation.
   - Version comparison: an exact-build delta rather than a single-artifact conclusion.
   - Preservation: acquisition, authenticity, provenance, and durable research records.

4. Choose the domain workflow.
   - Use Apple workflows for Mach-O, Apple bundles, Swift or Objective-C metadata, Apple signing, dyld caches, Apple Silicon, or Apple runtime evidence.
   - Use .NET or Unity workflows for managed assemblies, PDBs, IL2CPP metadata, and compiled Unity layouts.
   - Keep ordinary source development, builds, tests, Xcode work, or Unity authoring with the owning development plugin.

5. Choose a tool adapter only after the domain need is clear.
   - Use Cutter and Rizin for interactive plus repeatable general binary analysis.
   - Use Malimite for supported Apple app-package exploration.
   - Use Ghidra or Hopper when their project, loader, analyzer, or platform presentation fits better.
   - Detect installed capabilities and versions instead of assuming a decompiler, debugger, loader, or plugin exists.

6. Define the stopping condition.
   - Name the observation that would answer the question.
   - Name the smallest useful fallback if the chosen tool cannot parse, analyze, or verify the artifact.

7. Start or update `evidence-notes-workflow` when the work will span tools, sessions, renames, or exact-build claims.

## Selection Rules

- Prefer read-only metadata before expensive or mutable analysis.
- Prefer disassembly and format metadata over decompiler output when they disagree.
- Treat a debugger as a separate optional stage, not an automatic continuation of static analysis.
- Do not treat a Simulator, VM, translated process, or re-signed copy as equivalent to the original environment.
- Do not claim absence when a parser, selected slice, analysis preset, or stripped artifact may have hidden the evidence.

## Output

Return:

```markdown
## Question
...

## Artifact Identity
- Type:
- Stable identifier:
- Original preserved:

## Chosen Path
- Evidence class:
- Domain workflow:
- Tool adapter, if needed:

## Why This Path
...

## Stop Condition
...

## Fallback
...
```
