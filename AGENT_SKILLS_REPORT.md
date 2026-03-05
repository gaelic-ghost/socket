# Agent Skills Workflow Report

## Overview

This report describes the active skills in this repository after the router-removal cleanup completed on 2026-03-05.

Maintainer-facing workflow diagrams, path maps, and Agent ↔ User UX descriptions now live in `WORKFLOWS.md`.

Active skills:

1. `apple-xcode-workflow`
2. `apple-dash-docsets`
3. `apple-swift-package-bootstrap`

Migration map:

| Historical ID | Current State |
| --- | --- |
| `apple-skills-router-advise-install` | removed |
| `apple-skills-router` | removed |
| `apple-xcode-workflow-execute` | `apple-xcode-workflow` |
| `apple-dash-docset-manage` | `apple-dash-docsets` |

## Canonical Path Model

Every active skill now uses the same path vocabulary:

- `primary workflow`: the only numbered top-level path in `SKILL.md`
- `guard`: a condition that must be satisfied before the primary path continues
- `fallback`: a supported secondary path when the primary path cannot run
- `handoff`: a transfer to another skill or later stage
- `blocked`: no valid path remains

Every active skill now documents:

- `status`
- `path_type`
- `output`

Canonical `path_type` values:

- `primary`
- `fallback`

Canonical status policy:

- `success` for completed primary or fallback paths
- `handoff` for directed transfers
- `blocked` when no valid path remains
- `failed` only where an operation can start and then fail mid-run

## Skill Summaries

### `apple-xcode-workflow`

Purpose:

- Provide the canonical Apple and Swift execution workflow with one MCP-first execution engine.

Primary workflow:

1. Classify the operation.
2. Resolve workspace context.
3. Attempt the MCP path.
4. Retry once for transient failures.
5. Use official CLI fallback when MCP cannot complete.
6. Report the completed path.

Straightened behavior:

- Mutation handling is now a `guard`, not a peer workflow.
- Docs lookup is now an operation profile under the same execution engine, not a separate top-level track.
- The skill is a top-level entry point and may recommend `apple-dash-docsets` or `apple-swift-package-bootstrap` directly when the user has shifted tasks.

Contract notes:

- `status`: `success`, `handoff`, `blocked`
- `path_type`: `primary`, `fallback`
- Handoff contract: `skills/apple-xcode-workflow/references/mcp-failure-handoff.md`

### `apple-dash-docsets`

Purpose:

- Manage Dash docsets through a straight stage flow.

Primary workflow:

1. Classify the request into a stage.
2. Start at `search` unless another stage is explicit.
3. Run the selected stage.
4. Hand off forward when needed.
5. Return one status and one path type.

Straightened behavior:

- Default flow is now `search -> install -> generate`.
- `generate` is terminal guidance, not a peer top-level workflow in practice.
- The skill is a top-level entry point and may recommend `apple-xcode-workflow` for Apple execution work or `apple-swift-package-bootstrap` for new package creation.

Contract notes:

- `status`: `success`, `handoff`, `blocked`
- `path_type`: `primary`, `fallback`
- Handoff contract: `skills/apple-dash-docsets/references/stage-handoff-contract.md`

### `apple-swift-package-bootstrap`

Purpose:

- Create one deterministic Swift package scaffold path grounded in the bundled bootstrap script.

Primary workflow:

1. Collect inputs.
2. Normalize aliases.
3. Run the bundled script.
4. Verify the generated repository.
5. Report the result.

Straightened behavior:

- Manual `swift package init` is fallback-only guidance.
- `tool` remains supported but is documented as an advanced explicit passthrough, not a default branch.
- The skill is a top-level entry point for new Swift packages only and may recommend `apple-xcode-workflow` or `apple-dash-docsets` directly when the user moves into execution or docs work.

Contract notes:

- `status`: `success`, `blocked`, `failed`
- `path_type`: `primary`, `fallback`

## Repo-Level Alignment

This pass aligned:

- the public skill surface back to three top-level skills
- install commands and maintainer docs to the three-skill surface
- `WORKFLOWS.md` to maintainer-only documentation
- cross-skill recommendation language inside each remaining skill
- per-skill local end-user AGENTS guidance references

## Follow-Up

The remaining maintenance work is routine:

- preserve one top-level entry point per skill
- keep skill-local operational resources self-contained
- avoid reintroducing a repo-level Apple orchestrator layer
