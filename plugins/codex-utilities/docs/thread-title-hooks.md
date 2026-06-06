# Codex Thread Title Hook Notes

Codex Utilities starts with a safe `SessionStart` hook. By default, the hook
records the actual payload that Codex provides when a thread starts so
thread-name automation can be designed from real data instead of guessing.

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

It also writes structured hook decisions to:

```text
~/.codex/codex-utilities/hooks/thread-title-decisions.jsonl
```

Set `CODEX_UTILITIES_DATA_DIR` to redirect both paths during tests.

## Thread Title Modes

`CODEX_UTILITIES_THREAD_TITLE_MODE` controls the title behavior:

- `capture` is the default. It records payloads and decisions without changing
  thread metadata.
- `dry-run` records the thread id candidate and proposed prefix without calling
  App Server.
- `rename` calls App Server `thread/name/set` with the proposed name.

The proposed name is currently the last path component of `cwd`, truncated to
`CODEX_UTILITIES_THREAD_TITLE_MAX_PREFIX_LENGTH` characters. The default maximum
is `48`.

The thread id candidate is read from `thread_id`, `threadId`, `session_id`, then
`sessionId`. Current Codex hook docs describe `session_id`; keep rename mode
disabled by default until a live GUI new-thread test confirms that value is the
same id accepted by `thread/name/set`.

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

The hook's rename mode connects directly to the Codex App Server unix control
socket:

```text
~/.codex/app-server-control/app-server-control.sock
```

Override that path with `CODEX_UTILITIES_APP_SERVER_SOCKET`. The control socket
uses WebSocket frames over a unix socket, so the hook uses a small Node stdlib
client instead of sending plain JSONL to `codex app-server proxy`.

An MCP tool can still be useful as an operator-facing helper, but it should be
implemented as a thin path to App Server metadata operations rather than as an
agent loop.

## Next Test

1. Install or refresh the Socket marketplace plugin locally.
2. Trust the `codex-utilities` `SessionStart` hook.
3. Start a new thread in a known working directory with the default `capture`
   mode.
4. Compare the captured `session_id` with the new thread id.
5. Repeat with `CODEX_UTILITIES_THREAD_TITLE_MODE=dry-run` and inspect
   `thread-title-decisions.jsonl`.
6. Only after that identity is confirmed, repeat with
   `CODEX_UTILITIES_THREAD_TITLE_MODE=rename`.
