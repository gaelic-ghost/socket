# Shared Python Bootstrap Contract

Use this contract for every generated Python project, FastAPI service, and
FastMCP service. It owns the policy common to the three bootstrap entry points;
framework-specific overlays remain with their own skills.

## Command And Dependency Policy

- Use `uv` for project creation, dependency changes, locking, syncing, and
  command execution.
- Keep runtime imports in `[project].dependencies`, optional user-facing
  features in `[project.optional-dependencies]`, and maintainer tooling in
  `[dependency-groups]`.
- Install and run `pytest`, Ruff, and mypy through `uv`; do not rely on a
  globally installed Python tool.
- Use a single project for one package or service. Use a workspace only when
  multiple members have a real local package relationship.

## Configuration And Secret Policy

- Commit only safe, non-secret defaults in `.env` when the selected scaffold
  uses environment-backed settings.
- Keep machine-local or secret values in ignored `.env.local` or the target
  deployment's secret store.
- Keep typed configuration in a dedicated settings module. Tests override
  environment values or a settings dependency rather than modifying committed
  defaults.

## Validation And Cleanup

Run the scaffold's emitted commands first, then use the narrowest configured
checks for the changed member or project:

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

Run `uv run ruff format --check .` only when the generated or target project
enforces formatting. For a workspace, target the intended member with
`uv run --package <member> ...` when a full workspace sweep is unnecessary.

Do not overwrite a non-empty target or existing `pyproject.toml` without the
entrypoint's explicit force flag. Initialize git only when requested by the
entrypoint defaults, and remove temporary scaffold output only after reporting
the validation result.

## Handoff Matrix

| Need | Owning skill |
| --- | --- |
| Generic package or service scaffold | `bootstrap-uv-python-workspace` |
| New FastAPI service | `bootstrap-python-service` |
| New FastMCP server | `bootstrap-python-mcp-service` |
| Existing FastAPI and FastMCP integration | `integrate-fastapi-fastmcp` |
| Existing-project implementation | `build-python-project` |
| Test setup or testing workflow | `python-testing-workflow` |
| Tooling, package, CI, or upgrade maintenance | The corresponding `python-*-workflow` skill |
