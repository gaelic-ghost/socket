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
- `request_codex_gui_restart(mode, requesting_thread_id, observed_active_thread_ids, delay_seconds, reason)`: ask the installed app to schedule a user-requested Codex GUI restart.
- `cancel_codex_gui_restart(request_id)`: cancel a pending restart before the app executes it.
- `get_codex_gui_restart_status(request_id?)`: report pending, waiting, cancelled, blocked, failed, or completed restart state.

The first implementation slice should ship `get_bridge_status()` only. UI action tools should wait until the app reports stable permission state and the skill policy is in place.

Codex GUI restart tools can ship as their own small surface after the app exposes a restart coordinator endpoint. They do not need to wait for desktop UI action tools because they use a different safety model: explicit user restart intent plus thread-state checks.

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

Add a separate `codex-gui-restart` skill under `plugins/codex-utilities/skills/codex-gui-restart/`.

That skill should tell agents:

- Use it only when the user explicitly asks to restart Codex GUI.
- Inspect current GUI thread status before requesting `if-idle`.
- Exclude the requesting thread from the set of other active threads.
- Use `if-idle` when the user wants a restart only if no other threads are active.
- Use `when-idle` only when the user explicitly wants the app to wait for other active threads.
- Treat `when-idle` as blocked unless `UtilitiesForCodex` reports that it has a supported app-side thread-status source.
- Report the scheduled restart status before ending the assistant turn.
- Do not use restart tools as a generic cache refresh, plugin update, or troubleshooting step without user intent.

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
- Restart blocked: name the active thread count, the observed thread ids when available, or the missing supported thread-status source.
- Restart scheduled: report the mode, delay, requesting thread id when available, and cancellation/status path.

The MCP shim should not silently start broad UI automation or bypass permission prompts.

The MCP shim should not decide thread idleness by looking only at process state. A running Codex process does not prove another assistant turn is active, and a quiet process does not prove all GUI threads have finished.

The restart coordinator should fail closed when it cannot confirm idleness from a supported thread-status source immediately before the final quit/reopen step. Assistant-supplied `observed_active_thread_ids` can explain the request, but they must not be treated as authoritative after a delay.

## Codex GUI Restart Plan

The restart workflow belongs in `codex-utilities` because it is a local Codex runtime utility. It is not an Apple development workflow, a general productivity workflow, or a repo-maintenance skill.

The app/plugin split should be:

- `UtilitiesForCodex`: owns pending restart requests, cancellation, status, waiting behavior, and final macOS quit/reopen execution.
- `codex-utilities` MCP shim: exposes request, cancel, and status tools that talk to the app over the local transport.
- `codex-gui-restart` skill: tells agents when it is safe to call those tools and how to report the result.

The first restart implementation should support `if-idle` before `when-idle`.

For `if-idle`, the assistant can call Codex GUI thread-listing tools during the current turn, pass the observed active-thread set into the MCP request, and let the app schedule a delayed restart only when no other active threads were observed. Before it actually quits and reopens Codex, the app must re-check supported thread state and cancel or block the restart if another thread became active or the supported thread-status source is unavailable.

For `when-idle`, the app needs a supported way to observe GUI thread state after the assistant turn ends. Until that exists, the MCP tool should return a blocked status that says automatic waiting is unavailable instead of pretending process polling is equivalent to thread idleness.

The restart request payload should stay small and explicit:

- `mode`: `if-idle` or `when-idle`.
- `requesting_thread_id`: the GUI thread that asked for the restart, when known.
- `observed_active_thread_ids`: other active thread ids observed before the request.
- `delay_seconds`: short delay before quit/reopen.
- `reason`: short user-visible explanation.

The skill should ask the app for status after scheduling. If a restart is pending, the final assistant response should tell the user that Codex may quit and reopen after the configured delay.

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
- Whether a supported Codex App Server or GUI endpoint can report thread status outside the current assistant turn.
- Whether `when-idle` should use persistent app state or remain memory-only until the coordinator is proven.

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

### Slice 6: Codex GUI Restart Tools

- Add restart request, cancellation, and status tools once `UtilitiesForCodex` exposes the coordinator endpoint.
- Implement `if-idle` first using assistant-provided observed thread state.
- Return blocked diagnostics for `when-idle` until a supported app-side thread-status source exists.
- Add `skills/codex-gui-restart/SKILL.md` with the explicit user-intent, active-thread inspection, and final-status reporting rules.

## Current Decision

Plan the MCP and skill inside `codex-utilities`, but keep the actual app runtime in the public `gaelic-ghost/UtilitiesForCodex` repository.

For Codex GUI restart coordination, keep the waiting and restart execution in `UtilitiesForCodex`; keep the agent-facing request/cancel/status tools and operational skill in `codex-utilities`. Do not claim automatic `when-idle` support until the installed app has a supported thread-status source outside the current assistant turn.
