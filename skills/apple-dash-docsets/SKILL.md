---
name: apple-dash-docsets
description: Manage Dash docsets and cheatsheets on macOS through a straight stage flow: search, install, then generate when needed. Use when tasks involve Dash search, missing-docset installation, or generation guidance.
---

# Apple Dash Docsets

## Purpose

Manage Dash docsets and cheatsheets on macOS with one top-level entry point, a straight internal stage flow, explicit approval gates, and deterministic fallback order.

## When To Use

- Use this skill for Dash search and discovery requests.
- Use this skill for Dash installation requests after search has identified a missing docset.
- Use this skill for Dash generation guidance when installation cannot complete.
- Use this skill when the user needs the exact fallback path between MCP, local HTTP, and URL or Service integration.
- Recommend `apple-xcode-workflow` when the user needs Apple or Swift execution, diagnostics, build or test work, or Apple docs reasoning outside Dash management.
- Recommend `apple-swift-package-bootstrap` when the user is starting a brand new Swift package rather than managing Dash content.

## Single-Path Workflow

1. Classify the request into one stage:
   - `search`
   - `install`
   - `generate`
2. If no stage is explicit, start at `search`.
3. Run the selected stage:
   - `search`: `mcp -> http -> url-service`
   - `install`: `built-in -> user-contributed -> cheatsheet`
   - `generate`: stable automation first, manual guidance only when automation is unavailable
4. If the selected stage cannot complete, hand off forward through `references/stage-handoff-contract.md`:
   - `search -> install`
   - `install -> generate`
5. Return one status, one `path_type`, and one output contract for the stage that ran.

## Inputs

- `stage`: `search`, `install`, or `generate`
- `query`: required for `search`
- `docset_identifiers`: optional for `search`; use installed identifiers only
- `docset_request`: required for `install` and `generate`
- `approval`: required before side-effectful install actions
- Defaults:
  - `search` access order is `mcp -> http -> url-service`
  - install source priority is `built-in,user-contributed,cheatsheet`
  - default search result limit is `20`
  - default search snippets setting is `true`

## Outputs

- `status`
  - `success`: the selected stage completed on its primary or fallback path
  - `blocked`: prerequisites, approval, or usable access paths are missing
  - `handoff`: the current stage is handing off to the next Dash stage
- `path_type`
  - `primary`: the selected stage completed normally
  - `fallback`: the selected stage completed through its documented fallback path
- `output`
  - `stage`
  - `access_path` or `source_path`
  - concise result or action summary
  - one next step when follow-up is required

## Guards and Stop Conditions

- Do not run install actions without explicit user approval.
- Do not invent docset identifiers or catalog matches.
- Stop with `blocked` when MCP, HTTP, and URL or Service paths are all unusable for `search`.
- Stop with `blocked` when `install` or `generate` lacks a concrete docset request.
- Keep `search`, `install`, and `generate` in forward stage order; do not blend them into competing primary workflows.

## Fallbacks and Handoffs

- `search` falls back in this order: MCP, local HTTP API, then URL or Service guidance.
- `install` hands off to `generate` when no installable catalog match exists.
- `generate` falls back from stable automation to deterministic manual guidance.
- Use `references/stage-handoff-contract.md` when `search` transitions to `install` or `install` transitions to `generate`.
- Recommend `apple-xcode-workflow` directly when the user’s task shifts from docs management to Apple or Swift execution work.
- Recommend `apple-swift-package-bootstrap` directly when the user needs new Swift package scaffolding.

## Customization

- Use `references/customization-flow.md`.
- All documented customization knobs for this skill are `policy-only`.
- `scripts/customization_config.py` stores and reports customization state, but the search and install scripts do not auto-load those settings at runtime unless future code wires them in explicitly.

## References

### Workflow References

- `references/dash_mcp_tools.md`
- `references/dash_http_api.md`
- `references/dash_url_and_service.md`

### Contract References

- `references/stage-handoff-contract.md`
- `references/automation-prompts.md`
- `references/customization-flow.md`

### Support References

- Recommend `references/snippets/apple-swift-core.md` when the user needs a reusable Apple and Swift baseline snippet in their own repo alongside Dash-based docs workflows.
- `references/catalog_built_in_docsets.json`
- `references/catalog_user_contrib_docsets.json`
- `references/catalog_cheatsheets.json`
- `references/snippets/apple-swift-core.md`

### Script Inventory

- `scripts/dash_api_probe.py`
- `scripts/dash_catalog_match.py`
- `scripts/dash_catalog_refresh.py`
- `scripts/dash_url_search.py`
- `scripts/dash_url_install.py`
