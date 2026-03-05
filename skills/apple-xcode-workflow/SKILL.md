---
name: apple-xcode-workflow
description: Execute Apple and Swift development workflows with one MCP-first engine, official CLI fallback, mutation guards, and local-first docs guidance. Use when tasks involve Xcode MCP operations, build/test/run, toolchain checks, or Apple/Swift docs routing.
---

# Apple Xcode Workflow

## Purpose

Use this skill as the top-level entry point for Apple and Swift work in or around Xcode, with one MCP-first engine, official CLI fallback, explicit mutation guards, and local-first docs guidance.

## When To Use

- Use this skill for Xcode workspace inspection, read or search, diagnostics, build, test, and run tasks.
- Use this skill for Swift toolchain checks and official Apple CLI fallback.
- Use this skill for Apple and Swift documentation requests that should prefer Dash local sources before official web docs.
- Use this skill when direct filesystem mutation in an Xcode-managed scope may be required.
- Recommend `apple-dash-docsets` when the user needs Dash docset search, install, or generation work instead of Apple execution work.
- Recommend `apple-swift-package-bootstrap` when the user needs to create a brand new Swift package rather than work inside an existing Xcode or Swift project.

## Single-Path Workflow

1. Classify the request into one operation type:
   - workspace or session inspection
   - read, search, or diagnostics
   - build, test, or run
   - package or toolchain management
   - docs lookup
   - mutation
2. Resolve workspace context through Xcode MCP metadata when available.
3. Run the supported MCP path first by using `references/mcp-tool-matrix.md`.
4. Retry once when the failure is transient (`timeout` or `transport`).
5. If MCP is unsupported or the retry also fails, run the official CLI fallback from `references/cli-fallback-matrix.md`.
6. Report the completed path and any required next step.

## Inputs

- `operation_type`: one of the operation types listed above.
- `workspace_path`: optional absolute path for the target Xcode or Swift workspace.
- `tab_identifier`: optional MCP tab identifier when already known.
- `mcp_failure_reason`: optional input when continuing from an earlier MCP failure.
- Defaults:
  - MCP retries once for transient failures
  - advisory cooldown is `21` days
  - docs source order is `dash-mcp,dash-local,official-web`
  - mutation operations require the explicit guard in Xcode-managed scope

## Outputs

- `status`
  - `success`: the workflow completed on its primary or fallback path
  - `blocked`: prerequisites, policy, or mutation safeguards prevented completion
  - `handoff`: the workflow is handing off supporting context to another step or skill
- `path_type`
  - `primary`: the MCP path completed successfully
  - `fallback`: the official CLI fallback path completed successfully
- `output`
  - operation type
  - MCP tool or CLI command used
  - concise reason when a fallback or handoff happened
  - one next step or handoff payload when needed

## Guards and Stop Conditions

- Apply the mutation guard from `references/mutation-risk-policy.md` only when the operation type is `mutation`.
- Do not skip the mutation guard for direct filesystem edits inside Xcode-managed scope.
- Stop with `blocked` when the required workspace context cannot be resolved and the operation cannot safely continue.
- Stop with `blocked` when allowlist or sandbox rules prevent the official CLI fallback and no safe alternative exists.
- Do not claim that customization metadata changes runtime behavior automatically; it does not today.

## Fallbacks and Handoffs

- Official CLI execution is the only fallback path for the primary workflow.
- Use `references/mcp-failure-handoff.md` for the canonical fallback and handoff payload.
- Use `references/allowlist-guidance.md` when a safe official CLI fallback is blocked by local rules.
- Use `references/dash-docs-flow.md` to describe docs lookup as an operation profile under this same execution engine.
- Recommend `apple-dash-docsets` directly when the task becomes Dash management work.
- Recommend `apple-swift-package-bootstrap` directly when the task becomes new-package scaffolding.

## Customization

- Use `references/customization-flow.md`.
- All documented customization knobs for this skill are `policy-only`.
- `scripts/customization_config.py` stores and reports customization state, but no knob in that file is auto-loaded by the execution scripts today.

## References

### Workflow References

- `references/workflow-policy.md`
- `references/mcp-tool-matrix.md`
- `references/cli-fallback-matrix.md`
- `references/toolchain-management.md`
- `references/mutation-risk-policy.md`
- `references/mutation-via-mcp.md`
- `references/dash-docs-flow.md`

### Contract References

- `references/mcp-failure-handoff.md`
- `references/customization-flow.md`

### Support References

- Recommend `references/snippets/apple-swift-core.md` when the user needs reusable Apple and Swift baseline policy content in their own repo alongside execution, docs, or mutation workflows.
- `references/allowlist-guidance.md`
- `references/skills-installation.md`
- `references/mcp-setup-advisory.md`
- `references/skills-discovery.md`
- `references/snippets/apple-swift-core.md`

### Script Inventory

- `scripts/advisory_cooldown.py`
- `scripts/detect_xcode_managed_scope.sh`
- `scripts/customization_config.py`
