# Codex Hooks TTS Prototype

This worktree includes a small repo-local Codex hooks prototype for speaking
final assistant replies and inspecting Codex notification payloads.

## Files

- `.codex/config.toml`
  Enables `features.codex_hooks = true` for this trusted project and wires a
  `notify` probe command.
- `.codex/hooks.json`
  Registers one `Stop` hook handler.
- `.codex/hooks/stop-tts.mjs`
  Reads the Codex `Stop` payload from `stdin`, skips empty or duplicate turns,
  ignores continuation passes by default, and queues speech through the local
  `SpeakSwiftlyServer` HTTP route at `POST /speech/live`.
- `.codex/hooks/notify-dump.mjs`
  Records whatever Codex passes to the `notify` command so we can inspect the
  real payload shape. The probe captures both the documented JSON argument and
  any unexpected stdin payload so we can compare real behavior across Codex
  surfaces.
- `.codex/logs/stop-tts.jsonl`
  Runtime log for queued, skipped, and failed TTS attempts.
- `.codex/logs/notify-events.jsonl`
  Runtime log for `notify` payload inspection.
- `.codex/state/stop-tts-seen-turns.json`
  Dedupe state keyed by `session_id + turn_id`.

Both hook scripts now resolve their `.codex` state and log directories from the
script location itself instead of from `process.cwd()`. That matches the
official Codex hooks guidance to keep repo-local hook paths stable even when
Codex is started from a subdirectory.

## Environment Overrides

The `Stop` hook script accepts a few optional environment overrides:

- `CODEX_HOOK_TTS_BASE_URL`
  Override the default `http://127.0.0.1:7337`.
- `CODEX_HOOK_TTS_PROFILE_NAME`
  Override the default voice profile name `default-femme`.
- `CODEX_HOOK_TTS_SKIP_CONTINUATIONS`
  Defaults to `true`. Set to `false` if you want continued `Stop` turns read
  aloud too.
- `CODEX_HOOK_TTS_MAX_SEEN_TURNS`
  Controls how many dedupe keys are retained in the local state file.

## Validation Notes

The current prototype was rechecked against the current official Codex hooks
documentation:

- `Stop` receives one JSON object on `stdin`, including `turn_id`,
  `stop_hook_active`, and `last_assistant_message`.
- `Stop` must not emit plain text on `stdout`.
- repo-local hooks should resolve from the git root or another stable path, not
  by assuming the session `cwd` is the repository root.

The `Stop` hook script matches that current payload shape and was validated with
a synthetic `Stop` payload plus real runtime requests queued through the local
server.

Observed current behavior in this repo's live Codex TUI runs:

- the `Stop` hook payload arrives on `stdin`
- the `notify` command currently arrives as one JSON command-line argument
- the current notify runs observed here did not include any `stdin` payload

The `notify` probe still logs both the documented JSON argument and any `stdin`
payload so future Codex surfaces can be compared without rewriting the hook.
