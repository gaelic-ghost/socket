---
name: code-slice-explainer
description: Explain a bounded code slice end to end with data shape first, then full execution flow, boundaries, branch points, transformations, and final output. Use when users ask for a pipeline, execution flow, request lifecycle, data flow, trace, walkthrough, or how a part of a codebase works.
license: Apache-2.0
compatibility:
  platforms:
    - codex
metadata:
  version: 1.0.0
  owner: gaelic-ghost
  source_repo: https://github.com/gaelic-ghost/productivity-skills
  category: code
  domain: explanation
---

# Code Slice Explainer

Use this skill when the user wants one bounded walkthrough of how part of a system works from start to finish. The canonical term is `slice`.

## Purpose

- Explain one slice end to end without dropping meaningful steps.
- Start with the incoming data shape, what it represents, who sends it, and why it enters the flow.
- Walk the execution path in order, including boundaries, branch points, shared versus specialized steps, and data transformations.
- End with the final output shape, who receives it, and what purpose it serves.
- Let the user control explanation density with a detail level, not by silently skipping steps.

## Canonical vocabulary

- `slice`: one bounded end-to-end walkthrough of a request, event, feature action, job, or data item.
- `data shape`: the meaningful structure of the data at a point in the slice, what it represents, and why it has that shape.
- `boundary`: a meaningful crossing such as caller/callee, module, package, process, service, client/server, queue, storage, or external API.
- `branch point`: any step that can route execution down different paths.

Treat `pipeline`, `execution flow`, `request lifecycle`, `data flow`, `trace`, and `walkthrough` as compatibility language for the same underlying workflow unless the user clearly means something else.

## Inputs

- The slice subject:
  - a feature
  - a request or event
  - a job or workflow
  - a specific datum moving through code
  - a code entrypoint or path to follow
- Optional detail level:
  - `quick`
  - `standard`
  - `thorough`
- Optional focus:
  - branch-heavy
  - data-shape-heavy
  - boundary-heavy
  - debugging-oriented
- Optional comparison target for `compare slices`

Use `standard` when no detail level is specified.

## Primary workflow: explain a slice

1. Identify the slice trigger or entrypoint.
2. Explain the incoming data first:
   - what shape it has
   - what it represents
   - who is sending or constructing it
   - why it is entering the slice
3. Walk the slice in strict execution order from start to finish.
4. For each meaningful step, explain:
   - where it happens
   - what responsibility it has
   - whether it is shared or specialized
   - whether it crosses a boundary
   - whether it branches
   - whether the data shape changes
   - why any transformation exists
5. End with the output or return path:
   - final shape
   - final destination
   - why that result is consumed there
6. Include a simple step diagram with markers for branch points and data-shape changes.
7. Add short notes for those markers so the diagram stays readable.

## Variant workflow: compare slices

Use this when the user wants to compare:

- two related slices
- two implementations of the same slice
- old versus new behavior
- two branches within one slice

First explain each slice clearly enough to stand on its own. Then compare:

- trigger differences
- data-shape differences
- execution-order differences
- boundary differences
- branch differences
- output differences
- why the two paths diverge

## Detail levels

- `quick`: keep each step brief, but still include every meaningful step in order.
- `standard`: default density for most walkthroughs.
- `thorough`: add fuller commentary for branch behavior, boundaries, contracts, and why each transformation exists.

The detail level changes explanation density only. It must not remove meaningful steps from the slice.

## Output contract

Return a structured narrative in this order:

1. `Slice summary`
2. `Walkthrough`
3. `Diagram`
4. `Notes`

The writing should stay conversational and narrative-first. Avoid sterile dumps, but do not skip steps for brevity.

## Guardrails

- Never silently collapse or omit meaningful steps in the requested slice.
- Do not replace the end-to-end walkthrough with only a component map or only a high-level summary.
- If the path is ambiguous, say where the ambiguity starts and explain the most likely path plus the alternate branch.
- If a step cannot be proven from the code, say that plainly instead of guessing.
- Prefer concrete file/function references when available.
- Keep branch and data-shape notes short and move clutter out of the main narrative when a marker note will do.

## References

- Output contract: `references/output-contract.md`
- Detail levels: `references/detail-levels.md`
- Diagram rules: `references/diagram-format.md`
- Comparison workflow: `references/comparison-workflow.md`
- Example prompts: `references/example-prompts.md`
