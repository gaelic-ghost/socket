# App Extension Architecture Workflow Customization Contract

## Purpose

Preserve the repo-wide customization-file contract without turning extension-point, entitlement, or privacy decisions into persistent defaults.

## Knobs

The first version defines no runtime-enforced knobs.

## Runtime Behavior

- `scripts/customization_config.py` maintains the common configuration shape.
- The workflow ignores persisted settings because every extension-point and capability decision needs current Apple documentation and project evidence.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Add a setting only after its stable behavior and safety boundary are documented.
3. Validate the YAML before persisting it.
