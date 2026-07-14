---
name: recover-apple-runtime-metadata
description: Recover and validate Objective-C and Swift runtime structure from Apple binaries and generated analysis output. Use when Codex must inspect classes, categories, protocols, selectors, methods, properties, ivars, mangled Swift names, metadata, conformances, witness tables, generic specialization, async state machines, closure thunks, or Swift and Objective-C interoperability without presenting recovered metadata or decompiler guesses as original source declarations.
---

# Recover Apple Runtime Metadata

## Overview

Recover names and structural relationships from runtime metadata, symbols, references, and call sites. Keep runtime facts, tool guesses, and analyst reconstructions distinct.

Read [references/apple-runtime-recovery.md](references/apple-runtime-recovery.md) when interpreting Objective-C sections, Swift ABI clues, common generated functions, or evidence limits.

## Workflow

1. Fix the artifact context.
   - Record artifact hash, selected slice, UUID, tool and version, loader, base address, and symbol inputs.
   - Confirm whether the artifact is stripped, optimized, encrypted, or extracted from a cache.

2. Recover Objective-C structure.
   - Inventory classes, metaclasses, categories, protocols, selectors, method lists, properties, ivars, and class references.
   - Trace selector and class references to call sites instead of inferring behavior from names alone.
   - Preserve category ownership and inherited-versus-declared distinctions when the metadata supports them.

3. Recover Swift identities.
   - Record original mangled names and the demangler and version used.
   - Inventory nominal type descriptors, field metadata, protocol conformances, witness tables, method descriptors, and accessible reflection or replacement metadata.
   - Recognize specializations, thunks, closures, async continuations, and synthesized helpers as generated implementation units rather than source declarations.

4. Reconcile interoperability.
   - Map `@objc` names, selectors, bridging thunks, Objective-C entry points, and Swift implementations only when references support the relationship.
   - Preserve multiple possible owners when stripped or optimized output is ambiguous.

5. Validate recovered types and names.
   - Compare metadata with disassembly, callers, callees, constants, strings, and memory access patterns.
   - Use `review-decompiler-output` for high-level type and control-flow claims.

6. Record provenance.
   - Use the symbol-map shape from `evidence-notes-workflow`.
   - Classify each name as binary symbol, runtime metadata, demangled presentation, tool-generated placeholder, or analyst proposal.

7. Route the next step.
   - Use `correlate-apple-symbols-and-crashes` for dSYM and address evidence.
   - Use `analyze-apple-silicon-arm64e` for calling convention, PAC, or low-level instruction questions.
   - Hand ordinary Swift or Objective-C source changes to `apple-dev-skills`.

## Guardrails

- Do not convert metadata presence into proof that a source declaration had the same spelling or shape.
- Do not treat a demangled name as an original debug symbol.
- Do not infer complete conformance, generic, or field structure from one tool's partial rendering.
- Do not erase tool disagreement about function boundaries, types, or ownership.

## Output

Return the artifact and tool context, recovered runtime observations, symbol map, supported relationships, uncertain reconstructions, and the next verification target.
