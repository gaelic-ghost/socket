# Codex Thread Title Hook Notes

Codex Utilities starts with a capture-only `SessionStart` hook. The hook records
the actual payload that Codex provides when a thread starts so later thread-name
automation can be designed from real data instead of guessing.

## Name

The plugin is named `codex-utilities` because this work is about Codex runtime
behavior rather than a language, framework, app, or repository-maintenance
domain. It follows the Socket convention of hyphen-case plugin IDs with a
reader-facing display name in plugin metadata.

## Current Hook

The current hook listens for `SessionStart` with the `startup` matcher and runs:

```sh
sh ${PLUGIN_ROOT}/hooks/capture-session-start.sh
```

The script appends stdin to:

```text
~/.codex/codex-utilities/hooks/session-start.jsonl
```

Set `CODEX_UTILITIES_DATA_DIR` to redirect this path during tests.

## Rename Transport

The preferred next transport is Codex App Server `thread/name/set`. The
[App Server API overview](https://developers.openai.com/codex/app-server#api-overview)
describes it as setting or updating a thread's user-facing name for a loaded
thread or persisted rollout. The same API overview describes `command/exec` as
running a command without starting a thread or turn, which makes App Server
calls a better fit than launching `codex exec`.

`codex exec` is a poorer fit for automatic thread naming because it starts a
new agent run. That makes a metadata-only update depend on another model turn
and risks making the naming utility visible as its own thread activity.

An MCP tool can still be useful as an operator-facing helper, but it should be
implemented as a thin path to App Server metadata operations rather than as an
agent loop.

## Next Test

1. Install or refresh the Socket marketplace plugin locally.
2. Trust the `codex-utilities` `SessionStart` hook.
3. Start a new thread in a known working directory.
4. Compare the captured `session_id` with the new thread id.
5. Only after that identity is confirmed, add a rename script that derives a
   prefix from `cwd` and calls `thread/name/set`.
