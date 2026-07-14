---
name: script-hopper-analysis
description: Automate repeatable Hopper analysis with its installed Python SDK or extension APIs. Use for deterministic queries, controlled annotations, structured exports, or a scriptable document operation with a checkpointed evidence trail.
metadata:
  hermes:
    category: reverse-engineering
    tags: [hopper, python, automation]
---

# Script Hopper Analysis

## Overview

Use Hopper's installed Python SDK for narrow, repeatable document operations. Keep the script, its inputs, the document checkpoint, and its output together so another analyst can reproduce or review the transformation.

Read [references/hopper-automation-and-mcp.md](references/hopper-automation-and-mcp.md) for SDK discovery, mutation controls, MCP separation, and canonical sources.

## Workflow

1. Establish a document checkpoint.
   - Hash the input, save the Hopper document, and record the selected image, architecture, cursor or procedure scope, and Hopper version.
   - Do not let the first script run be the only copy of analyst work.

2. Discover the local SDK rather than guessing imports.
   - Use the installed Hopper help and resource bundle to locate the shipped Python API modules and examples.
   - Verify the active Python runtime can import the discovered API before writing an analysis script.

3. Write the smallest operation.
   - Prefer a query or structured export first.
   - Limit any transformation to an explicit procedure, address range, or selected document; do not sweep every procedure by default.

4. Run with an explicit mode.
   - Label the run `read-only`, `proposed-edit`, or `applied-edit`.
   - For an applied edit, preserve the pre-edit checkpoint and record each mutation class: comment, name, type, procedure, bookmark, or patch.

5. Verify in Hopper.
   - Reopen or refresh the affected document view and compare a sample of output with the assembly and pre-run state.
   - Report failed imports, unavailable APIs, and unsupported operations as calibration findings rather than substituting guessed output.

6. Preserve the evidence package.
   - Keep script source, dependency/runtime identity, parameters, stdout or logs, structured output, affected addresses, and final document checkpoint.

## Guardrails

- Do not overwrite the only Hopper document or original artifact.
- Do not treat SDK imports observed in another Hopper version as a contract for the installed version.
- Do not combine remote-model calls with a script without explicit approval for the selected artifact data.
- Use `$connect-hopper-mcp` instead of inventing an MCP transport in a Python script.

## Output

Return the Hopper and Python identities, document checkpoint, script purpose and mode, exact scope, observed output, mutations if any, verification sample, and retained evidence paths. For SDK discovery only, state `preflight only; no script or document mutation performed`.
