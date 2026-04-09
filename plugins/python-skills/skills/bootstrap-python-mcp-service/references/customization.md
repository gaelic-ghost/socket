# Customization Guide

Use this reference when you need to change the defaults shipped by `bootstrap-python-mcp-service`.

## High-Impact Knobs

- Python version default
- workspace member defaults and profile-map behavior
- generated FastMCP overlay files and dependencies
- mapping-report strictness in `scripts/assess_api_for_mcp.py`
- quality command stack (`pytest`, `ruff`, `mypy`)

## Audit Checklist After Changes

- `SKILL.md` examples match script help text
- project and workspace output both reflect the documented FastMCP overlay
- mapping-report commands use the current `uv run python ...` form
- `agents/openai.yaml` still describes the shipped scope accurately
