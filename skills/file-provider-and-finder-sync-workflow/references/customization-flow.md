# File Provider and Finder Sync Workflow Customization Contract

## Purpose

Preserve the common customization-file contract without hiding synchronization authority, conflict policy, or monitored-folder scope in unmanaged defaults.

## Knobs

The first version defines no runtime-enforced knobs.

## Runtime Behavior

- `scripts/customization_config.py` provides the shared configuration shape.
- The workflow ignores persisted settings because remote identity, destructive behavior, and Finder scope require product-specific validation.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Add a setting only after documenting its synchronization and privacy effects.
3. Validate YAML before applying it.
