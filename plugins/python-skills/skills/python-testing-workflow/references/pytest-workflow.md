# Pytest Workflow for uv Projects

## Quick Start

1. Install pytest as a dev dependency.
- Root project: `uv add --dev pytest`
- Workspace member: `uv add --package <member-name> --dev pytest`

2. Run tests.
- Root project: `uv run pytest`
- Targeted path: `uv run pytest tests/unit`
- Expression filter: `uv run pytest -k "auth and not slow"`

3. Optional coverage guidance.
- Install plugin: `uv add --dev pytest-cov`
- Run with report: `uv run pytest --cov --cov-report=term-missing`

## Baseline pyproject.toml config

Use `tool.pytest.ini_options` for project defaults:

```toml
[tool.pytest.ini_options]
addopts = "-ra"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
```

Common optional fields:

```toml
[tool.pytest.ini_options]
markers = [
  "slow: marks tests as slow",
  "integration: marks tests as integration",
]
xfail_strict = true
```

## Test Organization

- Put unit tests in `tests/unit` and integration tests in `tests/integration` when useful.
- Keep test modules deterministic and independent.
- Prefer fixtures over repeated setup blocks.

## Fixtures, Parametrize, Monkeypatch

- Place shared fixtures in `tests/conftest.py`.
- Use `@pytest.mark.parametrize` for input/output matrices.
- Use `monkeypatch` for env vars and side-effectful dependencies.

## Troubleshooting

1. No tests collected:
- Confirm naming patterns (`test_*.py`, `*_test.py`) and path selection.

2. Marker warnings:
- Register custom markers under `tool.pytest.ini_options.markers`.

3. Import errors:
- Confirm package layout and current run context.
- Prefer running from repository root with uv to preserve expected module resolution.

## References

- https://docs.pytest.org/en/stable/getting-started.html#get-started
- https://docs.pytest.org/en/stable/example/simple.html
- https://docs.pytest.org/en/stable/how-to/index.html#how-to
- https://docs.pytest.org/en/stable/reference/index.html#reference
- https://docs.pytest.org/en/stable/explanation/index.html#explanation
