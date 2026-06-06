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

This command path is intentionally provisional. The live Codex hook docs do not
document `${PLUGIN_ROOT}` expansion for plugin-bundled hook commands, and the
managed-hook guidance recommends absolute script paths for managed hooks. Before
enabling `rename` mode, confirm how Codex resolves plugin-relative hook commands
in an installed plugin cache.

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

Projectless Codex chat directories are treated specially. If `cwd` appears under
the default Codex chat root:

```text
~/Documents/Codex/YYYY-MM-DD/<thread-directory>
```

the hook skips prefixing by default so projectless chats keep Codex's generated
title. Override the root with `CODEX_UTILITIES_PROJECTLESS_ROOT`. To opt into a
shared projectless prefix such as `Chat`, set
`CODEX_UTILITIES_PROJECTLESS_THREAD_PREFIX`.

The thread id candidate is read from `thread_id`, `threadId`, `session_id`, then
`sessionId`. Current Codex hook docs describe `session_id`; keep rename mode
disabled by default until a live GUI new-thread test confirms that value is the
same id accepted by `thread/name/set`.

A live projectless thread created after trusting the plugin hook produced this
`SessionStart` payload shape:

```json
{
  "session_id": "019e9e4e-e0c5-7591-ac1d-51c09ef83faa",
  "transcript_path": "~/.codex/sessions/2026/06/06/rollout-2026-06-06T15-00-30-019e9e4e-e0c5-7591-ac1d-51c09ef83faa.jsonl",
  "cwd": "~/Documents/Codex/2026-06-06/codex-utilities-projectless-hook-test",
  "hook_event_name": "SessionStart",
  "model": "gpt-5.5",
  "permission_mode": "default",
  "source": "startup"
}
```

The payload did not include an explicit saved-project or projectless marker, so
the projectless rule is path-based until Codex exposes richer thread metadata to
hooks.

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

## Tested Alternate Route

An adjacent thread tested a more model-mediated route for prefixing thread
names. A `SessionStart` hook injected developer context that asked the new
thread itself to call its rename tool. That successfully renamed a generated
title to:

```text
heya-codex-i-d-like-to: Inspect thread naming controls
```

This route is worth keeping as a future refinement option because it preserves
Codex's generated title and only adds the project prefix around it. The tradeoff
is that it depends on model and tool compliance, and the instruction is more
visible inside the new thread than the direct App Server hook route.

## Next Test

Before testing, confirm the active Codex config uses the current feature keys:
`features.hooks = true` and the stable plugin feature. Removed keys such as
`features.plugin_hooks` are not required and should not appear in operator
guidance.

An installed `codex-utilities@socket` 6.16.0 probe did not expose or run the
plugin-bundled `SessionStart` hook in the Codex GUI settings or in
`codex exec --dangerously-bypass-hook-trust`. Current Codex docs say
plugin-bundled hooks load alongside other hook sources and do not document a
`SessionStart` exclusion, so treat that result as a product behavior mismatch or
loading-order limitation until confirmed upstream. A user-level or project-local
hook is the better live test surface for the thread-title flow.

1. Install or refresh the Socket marketplace plugin locally.
2. Confirm the hook source is visible in Codex hook settings or `/hooks`.
3. Trust the `codex-utilities` `SessionStart` hook if it appears.
4. Start a new thread in a known working directory with the default `capture`
   mode.
5. Compare the captured `session_id` with the new thread id.
6. Repeat with `CODEX_UTILITIES_THREAD_TITLE_MODE=dry-run` and inspect
   `thread-title-decisions.jsonl`.
7. Only after that identity is confirmed, repeat with
   `CODEX_UTILITIES_THREAD_TITLE_MODE=rename`.
8. Keep the model-mediated prefix route as a comparison path if direct App
   Server renaming loses too much of Codex's generated-title quality.
