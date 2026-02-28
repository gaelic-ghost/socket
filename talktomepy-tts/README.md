# TalkToMePy TTS Customization Guide

> Deprecated: This skill is retained for backward compatibility. For new speech workflows, use the maintained successor path in `a11y-skills`.

## What To Customize First

- Service endpoint (`--base-url` / `TALKTOMEPY_BASE_URL`).
- Voice style default (`energetic`, `soft`, `neutral`) or custom `--instruct`.
- Language default (`--language`, default `English`).
- Retry and wait controls (`TALKTOMEPY_MAX_WAIT_SECONDS`, retry count/backoff).
- Output location (`TALKTOMEPY_OUTPUT_DIR` or `--save`).
- Playback behavior (`--no-play` for generation-only workflows).

## Personalization Points

- Service location and startup behavior
  - Default: local service at `http://127.0.0.1:8000` with model load polling.
  - Why customize: users may run the service remotely or on alternate ports.
  - Where to change: [`scripts/speak_with_talktomepy.sh`](./scripts/speak_with_talktomepy.sh) defaults and env vars documented in [`SKILL.md`](./SKILL.md).
- Voice and tone profile
  - Default: `energetic` preset with a warm/friendly/brisk voice instruction.
  - Why customize: users may need narration, neutral support voice, or domain-specific delivery.
  - Where to change: `STYLE`/`set_style` and `INSTRUCT` in [`scripts/speak_with_talktomepy.sh`](./scripts/speak_with_talktomepy.sh).
- Language and content behavior
  - Default: language `English`; custom text passed via `--text`.
  - Why customize: multilingual workflows or strict pronunciation/style requirements.
  - Where to change: `LANGUAGE` default + command flags in [`scripts/speak_with_talktomepy.sh`](./scripts/speak_with_talktomepy.sh).
- Reliability and operational controls
  - Default: wait 180s, up to 12 synthesis retries, retry-after fallback 5s.
  - Why customize: slower hardware may need longer waits; CI pipelines may need faster failure.
  - Where to change: env var defaults in [`scripts/speak_with_talktomepy.sh`](./scripts/speak_with_talktomepy.sh).

## Common Customization Profiles

- Local interactive playback
  - Keep `afplay`, energetic/soft styles, default output folder.
- Batch generation pipeline
  - Use `--no-play`, custom output path, and tighter retry/fail-fast settings.
- Remote service client
  - Set custom `TALKTOMEPY_BASE_URL`, longer wait timeout, and explicit save paths.
- Neutral narration mode
  - Set neutral style as default and add custom narration instruction text.

## Example Prompts For Codex

### Adjust Defaults

- "Make `neutral` the default style in `speak_with_talktomepy.sh` and update docs accordingly."
- "Set default output directory to `./audio/tts` instead of `./tts_outputs`."

### Change Behavior

- "Add a new `narrator` style preset with slower pacing and clear enunciation."
- "Reduce max synth retries to 6 and fail faster when model status is not ready."

### Adapt For My Environment

- "Adapt this script to use my remote TalkToMePy endpoint and increase load wait to 300 seconds."
- "Configure the skill for non-macOS use where playback is disabled by default."

### Validate My Customization

- "Review the script and confirm all environment variable overrides still work after my edits."
- "Run a no-play synthesis test and verify the output file path and style metadata."

## Validation Checklist

- Verify `/health` succeeds for your configured base URL.
- Verify `/model/load` succeeds using a mode-aware payload:
  - `{"mode":"voice_design","strict_load":false}`
- Verify `/model/status` reaches `loaded=true` for VoiceDesign mode.
- Run one `--no-play` synthesis and confirm output file path.
- Run one playback synthesis (if supported) and confirm audio plays correctly.
- Confirm retry/wait env vars are honored in logs/output behavior.
- Confirm style presets and custom `--instruct` produce expected voice behavior.

## Notes And Compatibility

- Current script expects `bash`, `curl`, and `python3`.
- Skill targets TalkToMePy v0.5+ API contract (`/synthesize/voice-design`, mode-aware `/model/load`).
- Playback uses `afplay` (macOS); use `--no-play` when playback is unavailable.
