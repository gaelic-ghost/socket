# MailKit Workflow Customization Contract

## Purpose

Preserve the repo-wide customization-file contract without persisting mail-access, action, header, or message-security policy as hidden defaults.

## Knobs

The first version defines no runtime-enforced knobs.

## Runtime Behavior

- `scripts/customization_config.py` provides the shared configuration shape.
- The workflow ignores persisted settings because handler declarations and mail-data policy must be explicit for each product.

## Update Flow

1. Inspect current settings with `scripts/customization_config.py effective`.
2. Add a setting only after documenting its MailKit capability, user impact, and privacy boundary.
3. Validate YAML before applying it.
