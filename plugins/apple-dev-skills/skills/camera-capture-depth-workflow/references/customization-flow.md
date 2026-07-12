# Camera Capture and Depth Workflow Customization Contract

The first version defines no runtime-enforced knobs. `scripts/customization_config.py` preserves the shared Apple Dev Skills customization contract; future settings must be documented here and in `SKILL.md` before runtime behavior depends on them.

Inspect settings with `scripts/customization_config.py effective`, persist a documented change with `apply --input <yaml-file>`, and verify the effective result afterward.
