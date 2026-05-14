---
name: build-python-project
description: Build or modify idiomatic Python projects using uv, explicit package layout, typed configuration, focused tests, Ruff, mypy, and repo-local validation without overriding established conventions.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients implementing Python changes in uv-managed projects, packages, CLIs, FastAPI services, FastMCP servers, and workspaces.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-implementation
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*)
---

# Build Python Project

## Purpose

Implement or modify a Python project in the repository's own shape.

The practical goal is clear package boundaries, readable data flow, typed configuration where the repo uses it, tests around changed behavior, and validation through the repo's `uv` commands.

## When To Use

- Use this skill when adding or changing Python source in an existing project.
- Use this skill when the project shape is already known or was chosen with `choose-python-project-shape`.
- Use this skill when implementation touches reusable package code, CLI code, FastAPI adapters, FastMCP adapters, or shared domain logic.
- Use a more specific workflow when the task is only test setup, packaging, diagnostics, tooling, or FastAPI/FastMCP integration.

## Source Check

Use official documentation first when implementation depends on package, tool, or framework behavior:

- [uv documentation](https://docs.astral.sh/uv/)
- [Python packaging user guide](https://packaging.python.org/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)

## Implementation Workflow

1. Inspect project shape:
   ```bash
   rg --files -g 'pyproject.toml' -g 'uv.lock' -g '*.py' -g 'tests/**/*.py' -g '.python-version'
   ```
2. Read the relevant `pyproject.toml` sections:
   - `[project]`
   - `[tool.uv]`
   - `[tool.uv.workspace]`
   - `[dependency-groups]`
   - `[tool.pytest.ini_options]`
   - `[tool.ruff]`
   - `[tool.mypy]`
3. Identify the behavior being changed and who calls it next.
4. Keep reusable logic separate from framework adapters when the behavior is not inherently tied to FastAPI, FastMCP, or a CLI parser.
5. Prefer explicit inputs and outputs for transformations.
6. Keep environment reads, network calls, file IO, process exits, and framework globals at the edge of the workflow.
7. Add or update tests around the changed behavior.
8. Run the narrowest useful validation first, then broaden before a checkpoint when risk warrants it.

## Package And Module Shape

Respect the existing layout first.

For `src/` layouts:

- import through the installed package name
- avoid test-only import hacks
- keep package-private modules clearly internal by name or documentation

For flat layouts:

- avoid introducing a second package root casually
- use local conventions for imports and tests
- consider a package layout only when packaging or import correctness is already part of the task

For workspaces:

- use `uv run --package <name>` when commands need a specific member
- keep local package dependencies expressed through workspace sources
- avoid copying shared code between members

## Configuration

When generated or existing projects use `pydantic-settings`, keep committed `.env` files limited to safe defaults and keep `.env.local` or real secret stores for machine-local and secret values.

For tests, override environment variables or settings dependencies rather than mutating committed `.env` files.

## Validation

Choose commands based on the changed surface:

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

Use package targeting for workspaces:

```bash
uv run --package <package-name> pytest
uv run --package <package-name> mypy .
```

Run `uv sync --dev` first when dependency resolution, lockfiles, or Python versions changed.

## Output Shape

Return:

1. `Changed behavior`: what user-visible or package-visible behavior changed.
2. `Files`: key files changed.
3. `Tests`: tests added or updated.
4. `Validation`: exact commands run and results.
5. `Residual risk`: anything not covered.

## Guardrails

- Do not add a new framework, queue, service object, repository layer, or dependency without naming the concrete need it solves.
- Do not mix broad formatting sweeps into behavior changes.
- Do not hide import errors with `sys.path` edits unless the repo already uses that pattern and the reason is documented.
- Do not add machine-local paths to `pyproject.toml`, lockfiles, CI, or docs.
- Do not silently skip tests when the changed behavior is testable.
