# Conventions

## Platform and tooling

- Target macOS development workflows.
- Use `uv` for initialization, dependency management, lock/sync, and command execution.
- Use `git` for repository initialization unless explicitly disabled.

## Modes

- `project`: scaffold one FastAPI service.
- `workspace`: scaffold a uv workspace with package/service members.

## FastAPI defaults

- Use uv FastAPI integration style:

```bash
uv add fastapi --extra standard
uv add pydantic-settings python-dotenv
uv run fastapi dev app/main.py
```

- Keep optional production-style local command:

```bash
uv run fastapi run app/main.py
```

## Quality defaults

- Always include `pytest`, `ruff`, and `mypy`.
- Verify with:

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

- In workspace mode, run `uv run --all-packages pytest` plus per-member lint/type checks.

## Project structure defaults

- Service profile: `app/main.py`, `app/config.py`, committed `.env`, ignored `.env.local`, `tests/test_service.py`, `pyproject.toml`.
- Workspace root: `[tool.uv.workspace]` with members under `packages/`.
