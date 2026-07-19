# Safari MCP Workflow Customization Contract

## Purpose

Preserve the repo-wide customization-file contract without making origin, interaction, or privacy decisions persistent defaults.

## Knobs

The first version defines no runtime-enforced knobs.

## Runtime Behavior

- `scripts/customization_config.py` maintains the common configuration shape.
- The workflow ignores persisted settings because each browser session requires its own approved target and interaction boundary.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Add a setting only after its stable behavior and safety boundary are documented.
3. Validate YAML before persisting it.
