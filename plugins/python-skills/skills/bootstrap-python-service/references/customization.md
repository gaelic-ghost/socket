# Customization Guide

Use this reference when you need to change the defaults shipped by `bootstrap-python-service`.

## High-Impact Knobs

- Python version default
- FastAPI app layout and generated test shape
- workspace member defaults and profile-map examples
- quality command stack (`pytest`, `ruff`, `mypy`)
- guardrail strictness around `--force`, `--no-git-init`, and `--initial-commit`

## Audit Checklist After Changes

- `SKILL.md` examples match script help text
- generated scaffold layout matches the documented paths
- generated next-step commands actually run
- repo-level docs still describe the active public surface correctly
