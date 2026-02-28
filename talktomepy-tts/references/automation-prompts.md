# Automation Prompt Templates

Use this section order in this file: Suitability, App template, CLI template, Placeholders, Customization Points.

## Suitability

- Codex App: `Conditional` - works for recurring narration tasks, but only when text source and local service availability are explicit.
- Codex CLI: `Conditional` - `codex exec` works if local TalkToMePy service is reachable and write/network permissions are configured.

## Codex App Automation Prompt Template

```markdown
Use $talktomepy-tts.

Scope:
- Service base URL: <TALKTOMEPY_BASE_URL>
- Output directory: <TTS_OUTPUT_DIR_ABS_PATH>
- Text source mode: <TEXT_SOURCE_MODE_LITERAL_OR_FILE>
- Literal text: <TEXT_TO_SPEAK_OR_NONE>
- Text file path: <TEXT_FILE_PATH_OR_NONE>
- Playback enabled: <PLAYBACK_ENABLED_TRUE_FALSE>

Execution policy:
- Require explicit text source for unattended runs (literal or file).
- Default to generation-only mode (`--no-play`) unless playback is explicitly enabled.
- Run service health and model readiness checks before synthesis.
- Keep writes limited to <TTS_OUTPUT_DIR_ABS_PATH>.
- Do not modify unrelated files.

Output contract:
- Report synthesis status, output WAV path, selected style, language, and playback mode.
- If synthesis succeeds, include generated file path and timestamp.

No-findings handling:
- If no valid text source is provided, output exactly `No findings.` and archive the run.
- If text is provided and synthesis runs, keep output in inbox triage with artifact path.

Failure handling:
- If service/model is unavailable, report endpoint checked, failing step (`/health`, `/model/load`, `/model/status`), and suggested next check.
```

## Codex CLI Automation Prompt Template (codex exec)

- Recommended sandbox: `workspace-write` (writes WAV output)
- Network note: local HTTP access to `<TALKTOMEPY_BASE_URL>` must be permitted for this run.

Prompt template:

```markdown
Use $talktomepy-tts.

Synthesize speech with explicit inputs:
- Base URL: <TALKTOMEPY_BASE_URL>
- Output path: <OUTPUT_WAV_PATH>
- Language: <LANGUAGE>
- Style: <STYLE_ENERGETIC_SOFT_NEUTRAL_OR_CUSTOM>
- Playback enabled: <PLAYBACK_ENABLED_TRUE_FALSE>

Text input:
- Literal: <TEXT_TO_SPEAK_OR_NONE>
- File: <TEXT_FILE_PATH_OR_NONE>

Rules:
- If playback is not explicitly enabled, run in --no-play mode.
- If both text inputs are missing, output exactly `No findings.`.
- If service checks fail, report which endpoint failed and stop without retries beyond configured limits.
- Do not modify files outside the output location.
```

Optional command wrapper:

```bash
codex exec --sandbox workspace-write --output-last-message <FINAL_MESSAGE_PATH> "<PASTE_PROMPT_TEXT>"
```

Optional machine-readable mode:

```bash
codex exec --sandbox workspace-write --json "<PASTE_PROMPT_TEXT>"
```

## Placeholders

- `<TALKTOMEPY_BASE_URL>`: TalkToMePy HTTP base URL.
- `<TTS_OUTPUT_DIR_ABS_PATH>`: Directory for generated WAV files.
- `<TEXT_SOURCE_MODE_LITERAL_OR_FILE>`: `literal` or `file`.
- `<TEXT_TO_SPEAK_OR_NONE>`: Inline text payload, or `none`.
- `<TEXT_FILE_PATH_OR_NONE>`: Path to UTF-8 text file, or `none`.
- `<PLAYBACK_ENABLED_TRUE_FALSE>`: `true` to play audio, `false` for unattended generation.
- `<OUTPUT_WAV_PATH>`: Final WAV output path.
- `<LANGUAGE>`: Synthesis language value.
- `<STYLE_ENERGETIC_SOFT_NEUTRAL_OR_CUSTOM>`: `energetic`, `soft`, `neutral`, or explicit instruction label.
- `<FINAL_MESSAGE_PATH>`: File path for final assistant message.
- `<PASTE_PROMPT_TEXT>`: Fully expanded prompt text for `codex exec`.

## Customization Points

- Text source policy (literal/file, fallback behavior).
- Playback policy (`--no-play` default vs opt-in playback).
- Voice style and language defaults.
- Service endpoint and retry/wait thresholds.
- Output path and file naming conventions.
