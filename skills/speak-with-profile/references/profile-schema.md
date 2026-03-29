# Profile Schema v1

Use this schema contract for profile files consumed by `speak-with-profile`.

## File formats
- JSON or YAML.
- Recommended path: `config/speech/profiles.yaml`.
- The preferred default path may be documented in `config/customization.yaml` or `config/customization.template.yaml`.

## Required top-level fields
- `version`: must be `"1"`.
- `profiles`: non-empty list of profile objects.

## Optional top-level fields
- `default_profile`: id of one profile in `profiles`.

## Profile object fields
- `id` (required): lowercase hyphen-case pattern `^[a-z0-9-]+$`.
- `description` (optional): short human-readable purpose.
- `voice` (required): one of
  - `alloy`, `ash`, `ballad`, `cedar`, `coral`, `echo`, `fable`, `marin`, `nova`, `onyx`, `sage`, `shimmer`, `verse`
- `instructions` (required): non-empty string.
- `speed` (required): number in `[0.25, 4.0]`.
- `response_format` (required): `mp3`, `wav`, `opus`, `aac`, or `flac`.
- `disclosure` (optional): disclosure text for downstream UX.
- `tags` (optional): list of strings.

## JSON Schema (authoritative)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SpeechProfiles",
  "type": "object",
  "required": ["version", "profiles"],
  "properties": {
    "version": { "type": "string", "const": "1" },
    "default_profile": { "type": "string" },
    "profiles": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "voice", "instructions", "speed", "response_format"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
          "description": { "type": "string" },
          "voice": {
            "type": "string",
            "enum": ["alloy", "ash", "ballad", "cedar", "coral", "echo", "fable", "marin", "nova", "onyx", "sage", "shimmer", "verse"]
          },
          "instructions": { "type": "string", "minLength": 1 },
          "speed": { "type": "number", "minimum": 0.25, "maximum": 4.0 },
          "response_format": { "type": "string", "enum": ["mp3", "wav", "opus", "aac", "flac"] },
          "disclosure": { "type": "string" },
          "tags": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```

## Validation rules
- Reject duplicate profile IDs.
- Reject `default_profile` if not found in `profiles`.
- Reject any out-of-range speed.
- Reject unknown voices/formats.
