# macOS Sandbox File Access Customization Contract

The first version defines no runtime-enforced knobs. `scripts/customization_config.py` preserves the shared Apple Dev Skills customization contract; access scope must be selected from the concrete resource, process, operation, distribution, and persistence need.

Inspect settings with `scripts/customization_config.py effective`, persist a documented change with `apply --input <yaml-file>`, and verify the effective result afterward.
