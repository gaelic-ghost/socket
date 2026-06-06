# Desktop Bridge MCP and Skill Plan

## Summary

`codex-utilities` should own the agent-facing MCP and skill surfaces for a future desktop automation bridge, while the separate `Utilities for Codex` macOS app owns the stable installed runtime.

The plugin should feel familiar to agents trained on first-party Computer Use: a small set of explicit UI-action tools, a read-first app-state tool, and a clear confirmation policy. It should not ship or cache the signed macOS app bundle.

## Repository Split

- `gaelic-ghost/UtilitiesForCodex`: stable macOS app, signing identity, permission flow, local transport endpoint, Socket installer/status UI, and runtime diagnostics.
- `socket/plugins/codex-utilities`: MCP shim, skill guidance, confirmation policy, install/troubleshooting docs, and lightweight plugin metadata.

This split keeps the macOS trust boundary stable while preserving a hot-swappable agent-facing plugin adapter.

## Why This Belongs Here

`codex-utilities` is already the Socket plugin for local Codex runtime utilities that are not language-specific, app-specific, or repository-maintenance workflows. A desktop bridge for Codex is a local Codex runtime utility.

It does not belong in:

- `apple-dev-skills`, because the MCP/skill is for using the desktop, not building Apple apps.
- `swiftasb-skills`, because the initial runtime should not make SwiftASB own the macOS trust boundary.
- `productivity-skills`, because this is a concrete local utility, not general automation-design guidance.
- A standalone plugin payload, because Socket should expose the Codex-facing adapter and keep the installed app separate.

## Planned MCP Surface

The initial MCP server should be a stdio adapter that talks to the installed `Utilities for Codex` app over a local transport. Unix domain sockets are the preferred first transport to evaluate.

Planned tools:

- `get_bridge_status()`: report app installation, app reachability, runtime version, transport state, and permission status.
- `get_app_state(app)`: return app identity, focused window, compact Accessibility tree, focused element, and screenshot metadata.
- `click(app, element_index | x/y)`: click an indexed element or coordinates.
- `type_text(app, text)`: type literal text.
- `set_value(app, element_index, value)`: set an Accessibility value when supported.
- `select_text(app, element_index, text, prefix, suffix, selection)`: select text or place the cursor before/after a text range.
- `perform_secondary_action(app, element_index, action)`: invoke a named secondary Accessibility action exposed by an element.

The first implementation slice should ship `get_bridge_status()` only. UI action tools should wait until the app reports stable permission state and the skill policy is in place.

## Planned Skill Surface

Add a `desktop-bridge` skill under `plugins/codex-utilities/skills/desktop-bridge/`.

The skill should tell agents:

- Use dedicated app or browser plugins first when they can complete the task.
- Use the desktop bridge only when the task requires reading or operating local macOS app UI.
- Call `get_bridge_status()` before any app interaction.
- Call `get_app_state(app)` once per assistant turn before interacting with an app.
- Prefer element-index actions over raw pixel coordinates when the Accessibility tree contains a usable target.
- Treat screenshot-only actions as more fragile than Accessibility-indexed actions.
- Stop and report clear diagnostics when the app is not installed, not running, or missing permissions.

The skill should mirror the useful shape of first-party Computer Use without copying its app-bundle packaging model.

## Confirmation Policy

The skill should require action-time confirmation before risky UI actions, including:

- Deleting local or cloud data through a UI.
- Submitting messages, forms, comments, applications, purchases, or other third-party communications.
- Changing local security, privacy, account, password, VPN, or system settings.
- Installing or running newly acquired software through UI automation.
- Uploading files or transmitting sensitive data into another app or website.
- Accepting browser or OS permission prompts that grant durable access.

Normal read-only app-state inspection should not require confirmation, but it should still avoid collecting more screenshot or Accessibility content than needed for the task.

## Runtime Contract

The MCP shim should fail closed with descriptive messages:

- App not installed: name the missing app and link the public repository or install instructions.
- App not running: say how to launch it and whether auto-launch is planned.
- Transport unavailable: name the expected Unix socket path or discovery mechanism.
- Permission missing: name the missing macOS permission and point to the app's permission status view.
- Unsupported action: name the target app, element, and requested action.

The MCP shim should not silently start broad UI automation or bypass permission prompts.

## Transport Plan

Evaluate Unix domain sockets first:

- Keep the endpoint local-only.
- Let the app own socket creation and lifecycle.
- Let the plugin own a small stdio MCP shim.
- Use request/response JSON messages that can evolve toward JSON-RPC if useful.

Open questions:

- Whether Codex plugin execution can always access the user-scoped socket path.
- Whether a signed command-line helper inside the app bundle is needed later.
- Whether XPC becomes preferable once helper registration or login item behavior is needed.
- Whether localhost is worth supporting only as a diagnostic fallback.

## Implementation Slices

### Slice 1: Plan and App Baseline

- Add this plan.
- Keep `codex-utilities` metadata hook-only until a real MCP server exists.
- Bootstrap `UtilitiesForCodex` as the separate macOS runtime app.

### Slice 2: Bridge Status MCP

- Add a small MCP server under `plugins/codex-utilities/mcp/desktop-bridge/`.
- Implement `get_bridge_status()` only.
- Return useful missing-app and missing-transport diagnostics.
- Add plugin metadata only when the server is runnable.

### Slice 3: Skill

- Add `skills/desktop-bridge/SKILL.md`.
- Include the confirmation policy and per-turn `get_app_state` rule.
- Keep wording narrow and operational.

### Slice 4: Read-Only App State

- Add `get_app_state(app)` once the app service can return Accessibility tree and screenshot metadata.
- Avoid UI action tools until read-only state has been validated against Finder and at least one non-Apple app.

### Slice 5: Guarded UI Actions

- Add click, type, set-value, select-text, and secondary-action tools.
- Keep action tools behind clear skill policy and descriptive app diagnostics.

## Current Decision

Plan the MCP and skill inside `codex-utilities`, but keep the actual app runtime in the public `gaelic-ghost/UtilitiesForCodex` repository.
