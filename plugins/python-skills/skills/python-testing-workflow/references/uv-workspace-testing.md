# uv Workspace Testing

## Detect Context

- Single project: one package, run tests with `uv run pytest`.
- Workspace: repository defines `[tool.uv.workspace]`, run member tests with `uv run --package <member-name> pytest`.

## Command Patterns

1. Run all tests for root project:
- `uv run pytest`

2. Run tests for one workspace member package:
- `uv run --package <member-name> pytest`

3. Run only a path in one workspace member package:
- `uv run --package <member-name> pytest tests/unit`

4. Forward selectors/options:
- `uv run --package <member-name> pytest -k "api and not slow" -m "not integration"`

## Dependency Setup Patterns

- Root project dev dependency:
- `uv add --dev pytest`

- Workspace member dev dependency:
- `uv add --package <member-name> --dev pytest`

- Optional coverage plugin:
- `uv add --dev pytest-cov`
- `uv add --package <member-name> --dev pytest-cov`

## Practical Guardrails

- Install dependencies in the same context used to run tests (root vs package).
- Use `--package` consistently when the target is a workspace member.
- Keep package-specific test commands explicit in automation scripts to avoid accidental root-only execution.

## References

- https://docs.astral.sh/uv/concepts/projects/workspaces/
- https://docs.astral.sh/uv/reference/cli/#uv-run
- https://pydevtools.com/handbook/how-to/how-to-run-tests-using-uv/
- https://pydevtools.com/handbook/tutorial/setting-up-testing-with-pytest-and-uv/
