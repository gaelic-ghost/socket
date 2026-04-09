# Customization Guide

Use this reference when you need to change the defaults shipped by `bootstrap-uv-python-workspace`.

## High-Impact Knobs

- Python version default
- package versus service profile behavior
- default workspace members and first-package linking behavior
- generated README template content
- quality command stack (`pytest`, `ruff`, `mypy`)

## Audit Checklist After Changes

- single-project and workspace examples match the scripts
- generated layout and README content reflect the documented defaults
- service-member linking still matches the narrative in `SKILL.md`
- downstream skills that delegate here remain aligned
