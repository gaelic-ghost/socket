---
name: python-ci-workflow
description: Design and maintain Python CI workflows around uv, pytest, Ruff, mypy, package build checks, dependency caching, Python version matrices, and local-command parity.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients maintaining Python CI for uv-managed projects, packages, services, FastAPI apps, FastMCP servers, and workspaces.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-ci
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*)
---

# Python CI Workflow

## Purpose

Make Python CI prove the same behavior maintainers care about locally.

The practical job is to choose Python setup, `uv` installation, dependency sync, pytest, Ruff, mypy, package-build checks, path filters, and matrix scope without making CI broader or noisier than the project needs.

## When To Use

- Use this skill when adding or changing CI for a Python repository.
- Use this skill when local Python validation and CI disagree.
- Use this skill when adding Python packages, services, FastAPI apps, FastMCP servers, or workspace members to an existing CI workflow.
- Use this skill before package or release workflows depend on CI results.

## Source Check

Use repo-local files, checked-out dependency sources, Dash MCP or Dash HTTP for installed docsets, and then official project documentation when Dash/local coverage is missing or stale:

- [GitHub Actions Python documentation](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [uv GitHub Actions integration](https://docs.astral.sh/uv/guides/integration/github/)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [Python packaging user guide](https://packaging.python.org/)

## CI Planning Workflow

1. Inspect local validation commands and project metadata:
   ```bash
   rg --files -g 'pyproject.toml' -g 'uv.lock' -g '.python-version' -g '.github/workflows/*.yml' -g '.github/workflows/*.yaml'
   ```
2. Inspect existing workflow files:
   ```bash
   rg --files .github/workflows -g '*.yml' -g '*.yaml'
   ```
3. Check Python version sources:
   - `requires-python`
   - `.python-version`
   - workflow `python-version`
   - repository docs
4. Decide job scope:
   - dependency sync
   - tests
   - lint
   - format check
   - type check
   - package build
5. Decide matrix scope:
   - one Python version for app/service CI unless compatibility is the point
   - multiple Python versions for public packages that promise a version range
   - one OS unless filesystem, process, path, native dependency, or user-facing CLI behavior requires cross-platform checks
6. Keep local and CI commands aligned.

## Baseline Command Order

Prefer a simple shape:

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run mypy .
```

Add formatting verification only when the repo enforces Ruff formatting:

```bash
uv run ruff format --check .
```

Add package validation only for package surfaces:

```bash
uv build
```

For workspaces, target package-specific jobs explicitly when the repo does not need a full workspace sweep:

```bash
uv run --package <package-name> pytest
uv run --package <package-name> mypy .
uv build --package <package-name>
```

## GitHub Actions Shape

Use the repo's existing workflow style first.

For new GitHub Actions workflows:

- install `uv` through the official setup action or documented installer path
- use `uv sync --dev` unless the repo documents a narrower sync command
- cache only when it measurably helps and the cache key includes lockfile state
- keep package build or publish steps separate from normal validation
- avoid CI secrets unless a workflow truly needs private package sources or publishing

## Output Shape

Return:

1. `Existing CI`: workflows, Python versions, uv setup, and checks.
2. `Local parity`: local commands CI should mirror.
3. `Change`: workflow, matrix, cache, package build, or docs update.
4. `Commands`: exact local commands and CI job commands.
5. `Residual risk`: checks still manual, secrets needed, or matrix not covered.

## Guardrails

- Do not publish packages from CI unless the user explicitly asked for release automation.
- Do not add broad OS or Python matrices without a concrete compatibility reason.
- Do not make CI depend on globally installed Python tools.
- Do not add machine-local paths, private checkout paths, or local package sources to workflows.
- Do not hide failing local validation by making CI narrower than the repo's documented checks.
