# Customization Flow

This skill has no runtime customization knobs. Keep the audit contract stable and make repository-specific exceptions explicit in the audit result rather than persisting hidden policy changes.

## Validation

Run `scripts/customization_config.py effective` after changing the shared customization contract, and verify that the workflow text still describes the same behavior.
