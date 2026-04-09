# UV Command Recipes

Use these recipes when adapting or troubleshooting the bootstrap scripts.

## Project Init

```bash
uv init --package --lib --name my-lib --python 3.13 --vcs none ./my-lib
uv init --app --name my-service --python 3.13 --vcs none ./my-service
```

## Add Dependencies

```bash
uv add fastapi --extra standard
uv add pydantic-settings python-dotenv
uv add --group dev pytest ruff mypy
```

## Lock and Sync

```bash
uv lock
uv sync
```

## Run Commands

```bash
uv run fastapi dev app/main.py
uv run pytest
uv run ruff check .
uv run mypy .
```

## Workspace Root Setup

Add this to the workspace root `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["packages/*"]
```

## Workspace Member Bootstrap

```bash
uv init --package --lib --name core-lib --python 3.13 --vcs none ./packages/core-lib
uv init --app --name api-service --python 3.13 --vcs none ./packages/api-service
```

## Workspace Member Dependencies

```bash
uv add --package core-lib --group dev pytest ruff mypy
uv add --package api-service --group dev pytest ruff mypy
uv add --package core-lib pydantic-settings python-dotenv
uv add --package api-service pydantic-settings python-dotenv
uv add --package api-service fastapi --extra standard
```

## Workspace Local Linking

Create a dependency from one workspace member to another:

```bash
uv add --package api-service core-lib
```

This writes a `tool.uv.sources` entry with `workspace = true` in the dependent member.

## Workspace Lock, Sync, and Verification

```bash
uv lock
uv sync --all-packages
uv run --all-packages pytest
```
