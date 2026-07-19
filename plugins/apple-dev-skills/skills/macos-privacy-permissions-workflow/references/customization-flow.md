# macOS Privacy Permissions Customization Contract

The first version defines no runtime-enforced knobs. `scripts/customization_config.py` preserves the shared Apple Dev Skills customization contract; permission conclusions must remain derived from current documentation, stable code identity, exact host state, and the recorded user or managed decision.

Inspect settings with `scripts/customization_config.py effective`, persist a documented change with `apply --input <yaml-file>`, and verify the effective result afterward.
