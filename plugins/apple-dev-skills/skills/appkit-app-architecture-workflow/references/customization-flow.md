# Customization Flow

Preserve the repo-wide customization-file contract without pretending the first
version of `appkit-app-architecture-workflow` already has runtime-tunable
behavior.

## Current Behavior

- `references/customization.template.yaml` is the default persisted shape.
- `scripts/customization_config.py` can show, apply, and reset customization
  state for consistency with the rest of Apple Dev Skills.
- The workflow currently ignores persisted settings at runtime because no
  runtime-enforced knobs are documented yet.

## Future Knobs

Only add runtime behavior after documenting:

- the exact setting key
- the allowed values
- which recommendation changes when the setting is present
- how tests prove the change is applied
