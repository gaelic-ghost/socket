---
name: python-tooling-style-workflow
description: Align Python formatting, linting, type checking, pytest configuration, dependency groups, local tooling, and CI validation around uv without overriding repo-local conventions.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients maintaining Python tooling with uv, Ruff, mypy, pytest, pyproject.toml, and optional CI integration.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-tooling
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*)
---

# Python Tooling And Style Workflow

## Purpose

Keep Python formatting, linting, type checking, and test tooling explicit.

The practical job is to respect existing repo conventions, use `uv` for commands and dependency groups, keep Ruff and mypy behavior understandable, and make local validation match CI.

## When To Use

- Use this skill when adding or changing Ruff, mypy, pytest, dependency groups, or Python tooling config.
- Use this skill when local validation and CI disagree.
- Use this skill when style drift causes noisy diffs.
- Use this skill when a repository needs one documented Python validation story.

## Source Check

Use repo-local files, checked-out dependency sources, Dash MCP or Dash HTTP for installed docsets, and then official project documentation when Dash/local coverage is missing or stale:

- [uv documentation](https://docs.astral.sh/uv/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Writing `pyproject.toml`](https://packaging.python.org/guides/writing-pyproject-toml/)

## Inspection Workflow

1. Inspect tooling files:
   ```bash
   rg --files -g 'pyproject.toml' -g 'uv.lock' -g 'ruff.toml' -g '.ruff.toml' -g 'mypy.ini' -g '.mypy.ini' -g 'pytest.ini' -g 'tox.ini' -g 'noxfile.py' -g '.pre-commit-config.yaml' -g '.github/workflows/*.yml' -g '.github/workflows/*.yaml'
   ```
2. Read existing repo guidance and CI.
3. Identify what is already enforced:
   - `uv sync`
   - `pytest`
   - Ruff lint
   - Ruff format
   - mypy
   - coverage
   - pre-commit
   - custom scripts
4. Decide the smallest alignment:
   - document existing commands
   - add missing dev dependency groups
   - add or adjust Ruff config
   - add or adjust mypy config
   - register pytest markers
   - align CI commands with local commands
5. Run validation.

## Ruff Guidance

Use Ruff lint checks for code-quality and style rules:

```bash
uv run ruff check .
```

Use Ruff formatting only when the repo has adopted it or the user asked for formatting:

```bash
uv run ruff format .
uv run ruff format --check .
```

Keep formatting-only sweeps separate from behavior changes when practical.

## mypy Guidance

Respect existing strictness first.

When adding type-checking:

- start with a clear package scope
- keep missing-stub decisions explicit
- avoid blanket ignores
- stage stricter settings when an existing codebase is noisy
- check Python-version settings against project metadata

Do not suppress type errors to make a check pass unless the suppression is narrow and documented.

## pytest Guidance

Keep pytest configuration close to the repo's existing pattern.

Use `pyproject.toml` for new configuration unless the repo already keeps pytest settings in a dedicated file.

Register custom marks to avoid marker warnings, and keep fixtures scoped narrowly unless expensive setup requires a wider scope.

## Dependency Groups

Keep maintainer tools in dependency groups rather than runtime dependencies:

```toml
[dependency-groups]
dev = [
  "pytest",
  "ruff",
  "mypy",
]
```

Use repo-local version bounds when the project already pins tooling. Do not introduce global-tool assumptions into docs or CI.

## Output Shape

Return:

1. `Existing tooling`: pytest, Ruff, mypy, dependency groups, CI, and custom scripts.
2. `Change`: documentation, dependency, config, formatting, linting, typing, or CI alignment.
3. `Commands`: exact `uv` commands.
4. `Validation`: results from relevant checks.
5. `Residual risk`: anything still manual or intentionally unenforced.

## Guardrails

- Do not make broad formatting sweeps inside unrelated behavior changes.
- Do not turn every lint or type suggestion into a blocking rule at once.
- Do not move maintainer tools into runtime dependencies.
- Do not depend on globally installed Python tools.
- Do not add pre-commit, tox, nox, or CI complexity unless the repo or user needs that surface.
