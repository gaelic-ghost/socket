---
name: python-upgrade-workflow
description: Plan and validate Python version, dependency, uv lockfile, FastAPI, FastMCP, Pydantic, Ruff, mypy, pytest, and package metadata upgrades with staged checks.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients upgrading Python, uv-managed dependencies, package metadata, frameworks, and maintainer tooling.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-upgrade
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*)
---

# Python Upgrade Workflow

## Purpose

Upgrade Python projects without losing track of compatibility, validation, or package-consumer impact.

The practical job is to inventory Python requirements, dependency groups, lockfile state, framework versions, tooling strictness, and public package promises; apply one coherent upgrade slice; then run staged validation and document migration notes when users or contributors need them.

## When To Use

- Use this skill when changing `requires-python`, `.python-version`, or CI Python versions.
- Use this skill when changing `uv.lock`.
- Use this skill when upgrading runtime dependencies, optional dependencies, or dependency groups.
- Use this skill when upgrading FastAPI, FastMCP, Pydantic, Ruff, mypy, pytest, or other workflow-shaping tools.
- Use this skill when package consumers, service operators, or contributors may need migration notes.

## Source Check

Use repo-local files, checked-out dependency sources, Dash MCP or Dash HTTP for installed docsets, and then official project documentation when Dash/local coverage is missing or stale:

- [uv documentation](https://docs.astral.sh/uv/)
- [Python packaging user guide](https://packaging.python.org/)
- [Python package version specifiers](https://packaging.python.org/specifications/version-specifiers/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)

## Upgrade Workflow

1. Inventory current state:
   ```bash
   rg -n "requires-python|dependencies|optional-dependencies|dependency-groups|tool.uv|tool.pytest|tool.ruff|tool.mypy|fastapi|fastmcp|pydantic|pytest|ruff|mypy"
   rg --files -g 'pyproject.toml' -g 'uv.lock' -g '.python-version' -g '.github/workflows/*.yml' -g '.github/workflows/*.yaml'
   ```
2. Decide upgrade boundary:
   - Python version only
   - runtime dependencies only
   - maintainer tools only
   - framework major or minor upgrade
   - package metadata and compatibility range
   - lockfile refresh without requirement changes
3. Read release notes or migration docs for version jumps that may change behavior.
4. Apply one coherent upgrade slice.
5. Run staged validation:
   ```bash
   uv sync --dev
   uv run pytest
   uv run ruff check .
   uv run mypy .
   ```
6. Add package build validation when package surfaces exist:
   ```bash
   uv build
   ```
7. Update docs, CI, release notes, or migration guidance when contributor setup, package requirements, or runtime behavior changes.

## Dependency Boundary Notes

Keep dependency changes in the right place:

- runtime imports belong in `[project].dependencies`
- optional user-facing features belong in `[project.optional-dependencies]`
- maintainer tools belong in `[dependency-groups]`
- local workspace relationships belong in `[tool.uv.sources]`

Do not move tools into runtime dependencies to make CI easier.

## Python Version Notes

When changing Python version support:

- update `requires-python`
- update `.python-version` when present
- update CI matrices or setup versions
- check lockfile compatibility
- check package classifiers when the repo ships them
- mention migration impact for contributors or package consumers

For public packages, do not narrow supported Python versions without treating it as a compatibility decision.

## Framework Notes

For FastAPI, FastMCP, and Pydantic upgrades:

- check startup and lifespan behavior
- check settings and validation behavior
- check generated or mounted MCP surfaces
- run tests that cover app construction and representative endpoints or tools
- update integration guidance when the public app shape changes

For Ruff, mypy, and pytest upgrades:

- separate new tool findings from behavior changes
- avoid broad suppressions
- update config only when the new version requires or justifies it

## Output Shape

Return:

1. `Upgrade boundary`: Python, runtime dependencies, tooling, framework, package metadata, or lockfile.
2. `Changed versions`: before and after.
3. `Compatibility impact`: contributors, package consumers, service operators, or none.
4. `Validation`: exact commands run and results.
5. `Docs`: migration notes, CI changes, release notes, or none.
6. `Residual risk`: checks still missing or behavior not covered.

## Guardrails

- Do not combine unrelated upgrade families unless the repo already requires one coherent migration.
- Do not refresh lockfiles casually inside unrelated behavior changes.
- Do not narrow Python version support silently.
- Do not suppress new lint or type errors broadly after tool upgrades.
- Do not publish packages or create releases unless the user explicitly asks for that release step.
