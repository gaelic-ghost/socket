---
name: diagnose-python-project
description: Diagnose Python uv sync, lock, import, test, Ruff, mypy, FastAPI, FastMCP, packaging, and CI failures with concrete phase classification and next checks.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients diagnosing Python projects that use uv, pytest, Ruff, mypy, FastAPI, FastMCP, and Python package metadata.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-diagnostics
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*)
---

# Diagnose Python Project

## Purpose

Find the first meaningful cause of a Python failure and explain it in human terms.

The useful answer is not "tests failed." It is what command failed, which project or package failed, which phase failed, why it most likely failed, and the smallest next check or fix.

## When To Use

- Use this skill when `uv sync`, `uv run pytest`, `uv run ruff`, `uv run mypy`, package build checks, FastAPI startup, or FastMCP startup fails.
- Use this skill when Python version selection, dependency groups, lockfiles, package layout, imports, test discovery, or type checking are unclear.
- Use this skill before widening into refactors after a vague Python error.

## Source Check

Use official documentation first:

- [uv documentation](https://docs.astral.sh/uv/)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [Python packaging user guide](https://packaging.python.org/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)

## Diagnostic Workflow

1. Capture repository shape:
   ```bash
   rg --files -g 'pyproject.toml' -g 'uv.lock' -g '.python-version' -g 'requirements*.txt' -g 'setup.py' -g 'setup.cfg' -g 'tox.ini' -g 'noxfile.py' -g '*.py'
   ```
2. Identify the exact failing command.
3. Re-run only the narrowest failing command when reproduction is needed.
4. Classify the failure phase:
   - Python version
   - dependency resolution
   - lockfile sync
   - import or package layout
   - test discovery
   - test execution
   - lint
   - format
   - type check
   - FastAPI startup
   - FastMCP startup
   - package build
   - CI environment
5. Identify the first meaningful error.
6. Explain the likely cause and smallest next check.

## Common Failure Classes

### Python Version

Look for `requires-python`, `.python-version`, CI setup, and `uv` interpreter selection.

Report when the repo asks for a Python version that local or CI does not provide.

### Dependency Resolution

Look for dependency groups, optional dependencies, extras, index configuration, lockfile drift, and private package sources.

Do not turn authenticated index failures into generic network diagnoses. Name the package source or credential surface when visible.

### Imports And Package Layout

Separate installed-package import failures from test-context import failures.

For `src/` layouts, check whether commands run through `uv` with the package installed. For workspaces, check whether the command targets the intended package member.

### Test Discovery And Execution

Discovery failures usually point at package imports, pytest configuration, plugin availability, markers, or test file naming.

Execution failures usually point at behavior, fixtures, environment, timing, async boundaries, or external dependencies.

### Ruff

Separate lint failures from format failures.

Use `uv run ruff check .` for lint and `uv run ruff format --check .` only when the repo enforces formatting.

### mypy

Check configuration scope, missing stubs, optional dependencies, package exports, and Python-version settings before suppressing errors.

### FastAPI And FastMCP

Check import paths, app object names, lifespan handling, settings loading, dependency initialization, and environment variables.

For combined FastAPI/FastMCP apps, verify that mounted app lifespan behavior was preserved.

## Output Shape

Return:

1. `Command`: exact failing command.
2. `Phase`: failure phase.
3. `Project`: package, workspace member, app, or workflow involved.
4. `First meaningful error`: short quoted or paraphrased error.
5. `Likely cause`: concrete explanation.
6. `Next check`: one or two smallest useful commands or edits.

## Guardrails

- Do not bury the first meaningful error under a long transcript.
- Do not rerun broad commands repeatedly before narrowing the phase.
- Do not delete lockfiles, virtual environments, caches, or generated artifacts without explaining why and getting approval when destructive.
- Do not add `sys.path` hacks to hide package-layout problems.
- Do not suppress Ruff or mypy findings to make checks pass unless the suppression is intentional and documented.
