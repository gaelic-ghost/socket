---
name: choose-python-project-shape
description: Choose the right Python project shape before implementation, including uv project versus workspace layout, package, CLI, FastAPI, FastMCP, testing, packaging, tooling, and validation boundaries.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with Python, uv-managed projects, FastAPI, FastMCP, pytest, Ruff, mypy, and Python packaging workflows.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-planning
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*)
---

# Choose Python Project Shape

## Purpose

Pick the smallest correct Python project shape before code changes begin.

The practical decision is what kind of Python surface the user needs, whether it should be a single `uv` project or workspace, which package or service owns the behavior, which validation commands should prove the work, and where package, API, MCP, test, or tooling boundaries should sit.

## When To Use

- Use this skill when the user wants a new Python project but has not chosen package, app, service, MCP server, workspace, or tooling shape.
- Use this skill before scaffolding with `bootstrap-uv-python-workspace`, `bootstrap-python-service`, or `bootstrap-python-mcp-service`.
- Use this skill when an existing repository has Python files and the next change could cross package, service, test, or tooling boundaries.
- Use this skill when the user asks whether Python, FastAPI, FastMCP, a CLI, or a package is the right shape for the work.

## Source Check

Use repo-local Python files, checked-out dependency sources, Dash MCP or Dash HTTP for installed Python docsets, and then official project documentation when Dash/local coverage is missing or stale. Check one of those source-specific paths before making claims about Python packaging, `uv`, FastAPI, FastMCP, tests, linting, or typing:

- [uv documentation](https://docs.astral.sh/uv/)
- [Python packaging user guide](https://packaging.python.org/)
- [Writing `pyproject.toml`](https://packaging.python.org/guides/writing-pyproject-toml/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)

Translate any documentation rule into the concrete repository decision it changes.

## Classification Workflow

1. Inspect the repository shape:
   ```bash
   rg --files -g 'pyproject.toml' -g 'uv.lock' -g 'requirements*.txt' -g 'setup.py' -g 'setup.cfg' -g 'tox.ini' -g 'noxfile.py' -g '.python-version' -g '.github/workflows/*.yml' -g '.github/workflows/*.yaml'
   ```
2. Identify the user-visible job:
   - reusable package
   - command-line app
   - FastAPI service
   - FastMCP server
   - combined FastAPI and FastMCP app
   - test or tooling setup
   - package maintenance
   - CI maintenance
   - dependency or Python-version upgrade
   - Python member inside a mixed-language repository
3. Choose the project layout:
   - single `uv` project for one small package, CLI, service, or MCP server
   - `uv` workspace when multiple packages or services need shared local dependencies
   - package plus tests when the repo exposes reusable logic
   - service plus shared package when API or MCP adapters should stay thin around reusable behavior
   - tooling-only change when the code shape already fits
4. Choose the validation path:
   - `uv sync --dev` when dependency resolution matters
   - `uv run pytest` for behavior
   - `uv run ruff check .` for lint
   - `uv run ruff format --check .` only when formatting is enforced
   - `uv run mypy .` when type checking is configured
   - package build checks only when package metadata or release surfaces changed
5. Choose the next skill:
   - scaffold: `bootstrap-uv-python-workspace`, `bootstrap-python-service`, or `bootstrap-python-mcp-service`
   - implementation: `build-python-project`
   - test work: `uv-pytest-unit-testing`
   - FastAPI/FastMCP integration: `integrate-fastapi-fastmcp`
   - diagnosis: `diagnose-python-project`
   - package validation: `python-package-workflow`
   - tooling alignment: `python-tooling-style-workflow`

## Recommendations

Prefer `uv` as the command and dependency surface.

Prefer `pyproject.toml` as the project metadata and tool configuration home unless the repository already uses dedicated config files for a clear reason.

Use a `src/` layout when creating reusable packages or packages that need import behavior to match installed use. Preserve an existing flat layout unless the requested work already requires a package-structure cleanup.

Keep FastAPI and FastMCP adapter code thin around shared logic when the behavior should be reusable outside the web or MCP transport.

Use a workspace only when multiple packages or services need a real local package relationship. Do not add a workspace for a single small project that can stay simpler.

## Output Shape

Return:

1. `Shape`: selected package, CLI, service, MCP server, workspace, tooling, package, CI, or upgrade shape.
2. `Why`: concrete user-visible reason.
3. `Layout`: expected files or package members.
4. `Next skill`: the skill that should handle implementation.
5. `Validation`: exact `uv` commands to prove the next change.
6. `Docs`: docs or repo guidance that should change.

## Guardrails

- Do not scaffold before the project shape is clear.
- Do not create a workspace just to look organized.
- Do not introduce machine-local dependency paths into shared project files.
- Do not publish packages, open releases, or change CI secrets from this planning skill.
- Do not replace established repo conventions unless the current shape blocks the requested work.
