# AGENTS.md

Use this file for durable guidance inside the Codex Utilities Socket plugin.

## Scope

- This plugin is for local Codex runtime utilities that are not specific to one programming language, Apple platform workflow, external app, or skill-repository maintainer task.
- Keep utilities small, explicit, and independently removable.
- Do not add broad convenience tooling here when the behavior clearly belongs in `productivity-skills`, `agent-plugin-skills`, a language-specific `*-skills` plugin, or an app integration plugin.

## Current Utility

- The first utility is a thread-title hook pair that records `SessionStart` and
  `Stop` payloads to local JSONL files.
- `rename` mode is the default because Codex GUI hook settings already provide
  the operator-facing enable/disable toggle for this behavior.
- `capture` and `dry-run` modes are explicit test levers for thread-title
  prefixing, enabled with `CODEX_UTILITIES_THREAD_TITLE_MODE`.
- `Stop` is the only hook event that may prefix generated titles because
  `SessionStart` runs before Codex creates the generated thread title.

## Planned Desktop Bridge Utility

- Keep the desktop bridge MCP and skill plan in `docs/desktop-bridge-mcp-skill-plan.md`.
- The MCP and skill belong in this plugin because they are local Codex runtime utilities.
- The signed macOS runtime belongs in the separate `UtilitiesForCodex` app repository, not inside this plugin payload.
- Do not bundle a `.app` inside `codex-utilities`; the plugin should detect and talk to the installed app through a local transport.
- Codex GUI restart coordination should follow the same split: the installed app owns pending restart requests, waiting, cancellation, status, and final quit/reopen execution; this plugin owns the MCP request/cancel/status tools and the agent-facing skill policy.
- Do not implement `when-idle` by polling Codex process state alone. Treat automatic waiting as blocked until `UtilitiesForCodex` has a supported GUI thread-status source outside the current assistant turn.

## Runtime Data

- Default runtime payload path: `~/.codex/codex-utilities/hooks/thread-title-payloads.jsonl`
- Thread title decisions are recorded in `~/.codex/codex-utilities/hooks/thread-title-decisions.jsonl`
- Per-thread rename state is recorded in `~/.codex/codex-utilities/hooks/thread-title-state.json`
- Override with `CODEX_UTILITIES_DATA_DIR` when testing.
- Do not store captured hook payloads in the Socket repository.

## Thread Naming Direction

- Prefer the Codex App Server `thread/read` and `thread/name/set` operations for thread renaming once the hook can identify the target thread.
- Avoid using `codex exec` for automatic thread renaming because it starts a separate Codex run instead of performing a direct metadata update.
- The hook's App Server path starts `codex app-server` as a short-lived stdio
  JSON-RPC process; it should not start a new Codex thread or turn.
- Treat any MCP tool for thread naming as an operator-facing helper unless it can call App Server metadata operations without creating or steering another thread.
