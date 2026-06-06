# AGENTS.md

Use this file for durable guidance inside the Codex Utilities Socket plugin.

## Scope

- This plugin is for local Codex runtime utilities that are not specific to one programming language, Apple platform workflow, external app, or skill-repository maintainer task.
- Keep utilities small, explicit, and independently removable.
- Do not add broad convenience tooling here when the behavior clearly belongs in `productivity-skills`, `agent-plugin-skills`, a language-specific `*-skills` plugin, or an app integration plugin.

## Current Utility

- The first utility is a `SessionStart` hook that records the real hook payload to a local JSONL file.
- Treat this as an evidence-gathering step before implementing title mutation.
- Do not rename threads from this hook until the payload and target thread identity have been confirmed against a real new-thread test.

## Runtime Data

- Default runtime data path: `~/.codex/codex-utilities/hooks/session-start.jsonl`
- Override with `CODEX_UTILITIES_DATA_DIR` when testing.
- Do not store captured hook payloads in the Socket repository.

## Thread Naming Direction

- Prefer the Codex App Server `thread/name/set` operation for thread renaming once the hook can identify the target thread.
- Avoid using `codex exec` for automatic thread renaming because it starts a separate Codex run instead of performing a direct metadata update.
- Treat any MCP tool for thread naming as an operator-facing helper unless it can call App Server metadata operations without creating or steering another thread.
