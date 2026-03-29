# Starter Profiles

These baseline profiles cover general productivity use, accessibility-friendly listening, and deterministic prompt playback.

## Example YAML
```yaml
version: "1"
default_profile: default-general
profiles:
  - id: default-general
    description: General purpose default speech profile.
    voice: cedar
    instructions: |
      Voice Affect: Natural and clear.
      Tone: Neutral and professional.
      Pacing: Steady.
    speed: 1.0
    response_format: mp3

  - id: a11y-slow-clear
    description: Slower pacing with high enunciation for accessibility reads.
    voice: cedar
    instructions: |
      Voice Affect: Calm and focused.
      Tone: Supportive and direct.
      Pacing: Slightly slow.
      Pronunciation: Enunciate acronyms and numbers clearly.
    speed: 0.9
    response_format: wav

  - id: a11y-plain-language
    description: Optimized for simple wording and manageable cognitive load.
    voice: marin
    instructions: |
      Voice Affect: Warm and patient.
      Tone: Plain-language delivery.
      Pacing: Slightly slow with short sentence breaks.
    speed: 0.92
    response_format: wav

  - id: ivr-precise
    description: Precision-oriented prompt profile for phone/menu flows.
    voice: alloy
    instructions: |
      Voice Affect: Crisp and efficient.
      Tone: Neutral.
      Pacing: Controlled and consistent.
      Emphasis: Stress menu numbers and action words.
    speed: 0.95
    response_format: mp3
```

## Usage notes
- Prefer `default-general` for narrated notes, spoken drafts, or general audio summaries.
- For long informational reads or hands-free review, start with `a11y-slow-clear`.
- For lower reading complexity requirements, use `a11y-plain-language`.
- For deterministic telephone prompts or concise procedural cues, use `ivr-precise`.
