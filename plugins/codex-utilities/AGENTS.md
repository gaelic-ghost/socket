# AGENTS.md

Use this file for durable guidance inside the Codex Utilities Socket plugin.

## Scope

- This plugin is for local Codex runtime utilities that are not specific to one programming language, Apple platform workflow, external app, or skill-repository maintainer task.
- Keep utilities small, explicit, and independently removable.
- Do not add broad convenience tooling here when the behavior clearly belongs in `productivity-skills`, `agent-plugin-skills`, a language-specific `*-skills` plugin, or an app integration plugin.

## Current Utility

- The first utility is a `SessionStart` hook that records the real hook payload to a local JSONL file.
- Capture mode is the default and must remain safe for normal installs.
- `dry-run` and `rename` modes are test levers for thread-title prefixing, enabled with `CODEX_UTILITIES_THREAD_TITLE_MODE`.
- Do not enable `rename` by default until the payload and target thread identity have been confirmed against a real new-thread test.

## Planned Desktop Bridge Utility

- Keep the desktop bridge MCP and skill plan in `docs/desktop-bridge-mcp-skill-plan.md`.
- The MCP and skill belong in this plugin because they are local Codex runtime utilities.
- The signed macOS runtime belongs in the separate `UtilitiesForCodex` app repository, not inside this plugin payload.
- Do not bundle a `.app` inside `codex-utilities`; the plugin should detect and talk to the installed app through a local transport.

## Runtime Data

- Default runtime data path: `~/.codex/codex-utilities/hooks/session-start.jsonl`
- Thread title decisions are recorded in `~/.codex/codex-utilities/hooks/thread-title-decisions.jsonl`
- Override with `CODEX_UTILITIES_DATA_DIR` when testing.
- Do not store captured hook payloads in the Socket repository.

## Thread Naming Direction

- Prefer the Codex App Server `thread/name/set` operation for thread renaming once the hook can identify the target thread.
- Avoid using `codex exec` for automatic thread renaming because it starts a separate Codex run instead of performing a direct metadata update.
- The hook's App Server path connects to the local control socket and sends JSON-RPC directly; it should not start a new Codex thread or turn.
- Treat any MCP tool for thread naming as an operator-facing helper unless it can call App Server metadata operations without creating or steering another thread.
