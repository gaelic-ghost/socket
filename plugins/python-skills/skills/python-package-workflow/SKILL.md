---
name: python-package-workflow
description: Validate Python package surfaces with pyproject metadata, uv-managed builds, dependency boundaries, local smoke checks, semantic versioning, and release-boundary guidance.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients maintaining Python packages with uv, pyproject.toml, build metadata, tests, and package release preparation.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-packaging
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(uv:*)
---

# Python Package Workflow

## Purpose

Validate a Python package before release or publication.

The practical job is to make package metadata explicit, build and test the package, inspect the generated artifact when needed, and keep publishing as an explicit release step rather than an accidental side effect.

## When To Use

- Use this skill when a Python library is intended to become an installable package.
- Use this skill when `pyproject.toml` package metadata, versioning, dependencies, optional dependencies, or release notes change.
- Use this skill when adding package validation to CI.
- Use this skill before package publication, but do not publish unless the user asks for that release step.

## Source Check

Use official documentation first:

- [Python packaging user guide](https://packaging.python.org/)
- [Writing `pyproject.toml`](https://packaging.python.org/guides/writing-pyproject-toml/)
- [uv build documentation](https://docs.astral.sh/uv/concepts/projects/build/)
- [Python package version specifiers](https://packaging.python.org/specifications/version-specifiers/)

Translate documentation into the specific package, metadata, and release decision in front of you.

## Inspection Workflow

1. Identify package-bearing projects:
   ```bash
   rg --files -g 'pyproject.toml' -g 'uv.lock' -g 'README*' -g 'LICENSE*' -g 'src/**/*.py' -g '*.py'
   ```
2. Confirm the intended package boundary:
   - one package per public library project
   - no accidental service-only package release
   - no hidden machine-local dependencies
   - workspace members packaged only when they are intended package surfaces
3. Check metadata:
   - `name`
   - `version` or repository-owned version source
   - `description`
   - `readme`
   - `requires-python`
   - `license`
   - `authors` or maintainers
   - `classifiers`
   - `dependencies`
   - optional dependencies
   - project URLs
   - build system
4. Check dependency boundaries:
   - runtime dependencies in `[project].dependencies`
   - optional feature dependencies in `[project.optional-dependencies]`
   - maintainer tools in `[dependency-groups]`
   - workspace sources in `[tool.uv.sources]`
5. Run validation:
   ```bash
   uv sync --dev
   uv run pytest
   uv run ruff check .
   uv run mypy .
   uv build
   ```
6. Inspect generated package output when metadata or package contents changed.

## Workspace Notes

For workspaces, validate package members deliberately:

```bash
uv run --package <package-name> pytest
uv build --package <package-name>
```

Do not assume every workspace member should publish. Services, examples, internal tools, and test fixtures are often intentionally unpublished.

## Local Smoke Checks

When package behavior is public or packaging changed materially, create a temporary consumer outside the package tree and install the built artifact there.

Keep the smoke check small:

- install the built wheel
- import the public package
- call one tiny public function or CLI entry point
- confirm package metadata when relevant

Do not commit temporary consumer directories or generated artifacts unless the repo intentionally tracks release evidence.

## Output Shape

Return:

1. `Package boundary`: package name and path.
2. `Metadata`: changed or verified package metadata.
3. `Artifacts`: built wheel or sdist path if created.
4. `Validation`: exact commands run and results.
5. `Publish status`: not published, blocked, or explicitly published by user request.
6. `Residual risk`: missing smoke checks, external index state, or release notes still needed.

## Guardrails

- Do not publish to PyPI or another index unless the user explicitly asks for publication.
- Do not add machine-local paths to package metadata, dependencies, lockfiles, docs, examples, or CI.
- Do not move maintainer tools into runtime dependencies.
- Do not package app-only or service-only code accidentally.
- Do not change semantic versioning without checking repo-local release policy.
