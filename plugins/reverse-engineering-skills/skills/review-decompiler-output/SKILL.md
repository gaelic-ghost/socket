---
name: review-decompiler-output
description: Review generated pseudocode or disassembly without presenting it as original source. Use when Codex must interpret, compare, annotate, validate, or summarize output from Cutter, Rizin, Malimite, Ghidra, Hopper, ILSpy, or another decompiler or disassembler; assess recovered types and control flow; track analyst renames; or reconcile disagreements between generated output and binary or runtime evidence.
---

# Review Decompiler Output

## Overview

Turn generated output into bounded findings. Preserve which tool produced each name, type, expression, and control-flow shape.

## Workflow

1. Record the input context.
   - Identify the artifact hash, architecture or managed runtime, selected image, base address, tool and version, analysis settings, and function or address range.
   - Note whether symbols, debug information, signatures, runtime metadata, or prior analyst names were loaded.
   - If no actual generated view and no tool, version, and load context are available, stop with `no generated output reviewed` and request those inputs. Do not emit an empty review or infer source-level behavior from capability discovery alone.

2. Classify every important name.
   - Original exported or debug symbol.
   - Runtime-derived name such as an Objective-C selector or managed metadata name.
   - Tool-generated placeholder.
   - Analyst-proposed rename.
   - Demangled or normalized presentation of another recorded name.

3. Inspect decompiler artifacts.
   - Look for invented temporaries, merged variables, missing signedness, guessed structures, incorrect calling conventions, flattened control flow, synthetic gotos, hidden exception edges, and elided reference counting or runtime calls.
   - Treat casts, field layouts, loop shapes, and high-level operators as hypotheses until supported by lower-level evidence.

4. Cross-check the important claim.
   - Compare relevant instructions, references, imports, constants, strings, metadata, and call sites.
   - Check more than one caller or callee when a type or responsibility inference depends on context.
   - Use a second tool or runtime observation when the claim is consequential and the first tool's output is ambiguous.

5. Preserve transformations.
   - Record original name, proposed name, reason, evidence source, and confidence.
   - Keep tool output, analyst edits, and inferred source structure separate.

6. Report uncertainty.
   - Say `the decompiler represents` for generated constructs.
   - Say `the artifact contains`, `loads`, `exports`, or `references` only for directly supported observations.
   - Say `appears consistent with` for reconstructed behavior.
   - Say `not observed in this pass` instead of `does not exist` when analysis coverage is incomplete.

## Comparison Checklist

- Same artifact hash and architecture slice.
- Same load address or a documented address translation.
- Same symbol and type inputs.
- Same analysis scope and function boundaries.
- Tool-specific renames remain attributed.
- Differences are preserved rather than averaged into false agreement.

## Output

```markdown
## Generated View
- Tool/version:
- Artifact/function:
- Analysis context:

## Direct Observations
- ...

## Decompiler Artifacts Or Uncertainty
- ...

## Inferences
- Claim:
  - Supporting evidence:
  - Contradicting evidence:
  - Confidence:

## Renames
| Original | Proposed | Evidence | Confidence |
| --- | --- | --- | --- |

## Next Verification
...
```
