---
name: compare-binary-versions
description: Compare exact compiled-artifact builds and record reproducible structural, metadata, symbol, dependency, signing, resource, or control-flow differences. Use when Codex must diff binaries, bundles, frameworks, firmware, assemblies, dyld caches, releases, security updates, or beta builds without assuming that marketing versions, filenames, or tool-generated names uniquely identify the compared inputs.
---

# Compare Binary Versions

## Overview

Build a matched comparison before interpreting a delta. Attribute what changed to exact artifacts and environments, not to filenames or `latest` labels.

## Workflow

1. Define the comparison question.
   - Name the suspected behavior, component, mitigation, dependency, symbol, or resource change.
   - Decide whether the result needs to locate an introducing build or only show a difference between two endpoints.

2. Match the inputs.
   - Record hashes, build numbers, platform and hardware class, architecture or runtime, binary UUID or build ID, signing identity, container path, and acquisition source.
   - Record extraction, decryption, thinning, normalization, or symbol-application steps.
   - Reject comparisons that silently mix Simulator and device, translated and native, debug and release, or different architecture slices.

3. Match the analysis environment.
   - Record tool versions, loaders, analysis presets, symbol inputs, base addresses, and scripts.
   - Re-run both sides with the same method when a prior result lacks equivalent context.

4. Compare from stable structure outward.
   - Container and metadata identity.
   - Dependencies, imports, exports, sections, resources, entitlements, and signatures.
   - Symbols, functions, types, constants, strings, and references.
   - Control-flow or pseudocode only after address and function correspondence is established.

5. Track correspondence.
   - Match by stable symbol or metadata identity when possible.
   - Otherwise record the evidence used for a proposed match: call graph, constants, strings, type shape, relative position, or binary similarity.
   - Keep unmatched and ambiguous items visible.

6. Report temporal bounds honestly.
   - Use `changed between A and B` for endpoint comparisons.
   - Use `first observed in B` only when earlier checked builds are listed.
   - Do not equate a security advisory's named component with the full patch boundary without artifact evidence.

7. Preserve the comparison record.
   - Use the `version-diff` shape from `evidence-notes-workflow`.
   - Record unchanged observations that constrain interpretation, not only differences.

## Output

```markdown
## Comparison Question
...

## Matched Inputs
| Field | Build A | Build B |
| --- | --- | --- |

## Method
- Tooling:
- Symbols/loaders:
- Normalization:

## Confirmed Differences
- ...

## Confirmed Unchanged Context
- ...

## Ambiguous Matches
- ...

## Temporal Claim
...

## Next Intermediate Build Or Runtime Check
...
```
