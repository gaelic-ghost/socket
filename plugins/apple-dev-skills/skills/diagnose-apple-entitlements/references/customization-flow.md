# Diagnose Apple Entitlements Customization Contract

The first version defines no runtime-enforced knobs. `scripts/customization_config.py` preserves the shared Apple Dev Skills customization contract; the five-state comparison and final-artifact validation remain mandatory.

Inspect settings with `scripts/customization_config.py effective`, persist a documented change with `apply --input <yaml-file>`, and verify the effective result afterward.
