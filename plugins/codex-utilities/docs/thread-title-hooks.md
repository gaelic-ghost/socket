# Codex Thread Title Hook Notes

Codex Utilities provides `SessionStart` and `Stop` hooks for prefixing generated
thread titles with the project directory name, plus a `PostToolUse` diagnostic
hook for timing research. By default, a trusted and enabled hook renames project
threads; disable the hook in Codex GUI settings to turn the behavior off.

## Name

The plugin is named `codex-utilities` because this work is about Codex runtime
behavior rather than a language, framework, app, or repository-maintenance
domain. It follows the Socket convention of hyphen-case plugin IDs with a
reader-facing display name in plugin metadata.

## Current Hooks

The current hooks listen for `SessionStart` with the `startup` matcher, `Stop`,
and `PostToolUse`. All three run:

```sh
sh ${PLUGIN_ROOT}/hooks/run-thread-title-hook.sh
```

This command path depends on Codex's plugin-bundled hook command expansion. It
has been verified in the installed Socket plugin cache after restarting the
Codex GUI and trusting the plugin hooks.

The script appends stdin to:

```text
~/.codex/codex-utilities/hooks/thread-title-payloads.jsonl
```

It also writes structured hook decisions to:

```text
~/.codex/codex-utilities/hooks/thread-title-decisions.jsonl
```

Per-thread rename state is written to:

```text
~/.codex/codex-utilities/hooks/thread-title-state.json
```

Post-tool-use summaries are written to:

```text
~/.codex/codex-utilities/hooks/tool-use-events.jsonl
```

Set `CODEX_UTILITIES_DATA_DIR` to redirect these paths during tests.

## Thread Title Modes

`CODEX_UTILITIES_THREAD_TITLE_MODE` controls the title behavior:

- `rename` is the default. It uses the `Stop` hook to read the generated title
  and then call App Server `thread/name/set` once per thread.
- `capture` records payloads and decisions without changing thread metadata.
- `dry-run` records the thread id candidate and proposed prefix without calling
  `thread/name/set`.

`SessionStart` never renames the thread because it runs before Codex creates the
generated title. By default, the first `Stop` for a thread also waits without
renaming because GUI tests showed Codex can generate or rewrite the title after
that hook fires. The second `Stop` reads the current generated title with App
Server `thread/read`, prefixes it, and records per-thread state so later turns
do not keep rewriting the title.

`CODEX_UTILITIES_THREAD_TITLE_MIN_STOP_COUNT` controls the Stop count threshold.
The default is `2`. Set it to `1` only when deliberately testing first-turn
renames.

The prefix is the last path component of `cwd`, truncated to
`CODEX_UTILITIES_THREAD_TITLE_MAX_PREFIX_LENGTH` characters. The default maximum
is `48`. The generated title is preserved after the prefix:

```text
socket: Implement Stop hook title prefixing
```

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
`sessionId`. Current Codex hook docs describe `session_id`.

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

The hook's rename mode starts a short-lived App Server JSONL stdio process:

```sh
codex app-server
```

Override the command with `CODEX_UTILITIES_APP_SERVER_COMMAND`. The hook sends
`initialize`, `initialized`, `thread/read`, and `thread/name/set` over stdio.
This path works with the regular CLI install and does not require the managed
app-server daemon or the standalone Codex installer.

`CODEX_UTILITIES_THREAD_TITLE_POLL_ATTEMPTS` and
`CODEX_UTILITIES_THREAD_TITLE_POLL_DELAY_MS` control the bounded wait for Codex's
generated title during the `Stop` hook. If the title is still missing when the
poll expires, the hook skips the rename and can try again on a later `Stop`.

An MCP tool can still be useful as an operator-facing helper, but it should be
implemented as a thin path to App Server metadata operations rather than as an
agent loop.

## Tool Timing Diagnostics

The `PostToolUse` hook records compact summaries in `tool-use-events.jsonl` and
the raw payload in `thread-title-payloads.jsonl`. The compact summary includes
the timestamp, thread id candidate, turn id, cwd, best-effort tool name, tool id,
status, and sorted payload keys.

This diagnostic hook is intentionally read-only. It exists to answer whether
Codex's title generation appears as a hook-visible tool event and to compare
that timing with `Stop` decisions.

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

## GUI Test Notes

Before testing, confirm the active Codex config uses the current feature keys:
`features.hooks = true` and the stable plugin feature. Removed keys such as
`features.plugin_hooks` are not required and should not appear in operator
guidance.

An installed `codex-utilities@socket` 6.16.0 probe initially did not expose the
plugin-bundled `SessionStart` hook until the Codex GUI was restarted. After the
restart, the hook appeared in settings, was trusted, and captured real
`SessionStart` payloads.

1. Install or refresh the Socket marketplace plugin locally.
2. Confirm the hook source is visible in Codex hook settings or `/hooks`.
3. Trust the `codex-utilities` `SessionStart`, `Stop`, and `PostToolUse` hooks
   if they appear.
4. Start a new thread in a known working directory.
5. Confirm `thread-title-decisions.jsonl` records `SessionStart` and `Stop`
   decisions for the new thread.
6. Confirm the first `Stop` records the wait-for-second-Stop decision.
7. Send a second turn, then confirm the generated title is prefixed after the
   second `Stop` event.
8. Inspect `tool-use-events.jsonl` to see whether title generation appears as a
   hook-visible tool event.
9. Use `CODEX_UTILITIES_THREAD_TITLE_MODE=capture` or `dry-run` only when
   debugging the hook without mutating thread metadata.
10. Keep the model-mediated prefix route as a comparison path if direct App
   Server renaming loses too much of Codex's generated-title quality.
