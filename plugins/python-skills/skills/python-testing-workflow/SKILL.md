---
name: python-testing-workflow
description: Set up, run, and improve Python tests in uv projects and workspaces. Use for pytest configuration, focused and package-targeted runs, fixtures, parametrization, async and integration tests, coverage, CI parity, or failure triage.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients with uv-managed Python projects and pytest.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-testing
allowed-tools: Bash(uv:*) Read
---

# Python Testing Workflow

## Purpose

Make Python tests describe behavior, run through `uv`, and give a focused
failure signal. Preserve the repository's existing test framework and markers;
use the repository's own checked-in commands for setup and execution.

## Workflow

1. Inspect `pyproject.toml`, existing tests, CI, markers, fixtures, package
   layout, and workspace members before changing test configuration.
2. Choose the smallest useful test boundary:
   - unit tests for pure behavior and fakeable dependencies;
   - integration tests for framework, database, filesystem, network, or
     process boundaries;
   - a client test for public HTTP or MCP behavior;
   - a package-artifact smoke test when package contents changed.
3. Run a focused check first:
   ```bash
   uv run pytest tests/unit
   uv run pytest -k "auth and not slow"
   uv run --package <member-name> pytest
   ```
4. Add fixtures for reusable setup, keep their scope minimal, and use
   `@pytest.mark.parametrize` for input/output matrices.
5. Use `monkeypatch`, dependency overrides, fakes, or disposable services at
   the boundary rather than mutating committed configuration or calling a live
   dependency during every test.
6. Use async tests only when the code under test is async. Configure the
   repository's async test support explicitly and verify lifespan behavior when
   the app owns startup or shutdown resources.
7. Run the relevant complete test selection, then the project's CI-equivalent
   validation commands. Add coverage only when the user or repository has a
   concrete coverage threshold or reporting need.

## FastAPI And FastMCP Boundaries

For FastAPI, override external dependencies with
`app.dependency_overrides`, reset them after the test, and use an async client
when the test itself needs async behavior. Ensure lifespan events run when the
application depends on them.

For FastMCP, prefer an in-memory `Client(mcp)` test for deterministic server
behavior, then add transport or authorization integration tests only for the
configured deployment shape. Test listed and callable tools, readable
resources, and rendered prompts separately when each surface is public.

## Failure Triage

Classify the first failure before changing code:

- collection or import failure: package layout, test path, missing dependency,
  or environment;
- fixture or marker failure: configuration, scope, registration, or setup;
- async/lifespan failure: event-loop ownership, startup, shutdown, or client
  configuration;
- assertion failure: behavior, test data, or an intentionally changed public
  contract;
- integration failure: isolate the external boundary before widening the test
  suite.

Hand general environment, lockfile, lint, type-check, packaging, or CI failures
to `diagnose-python-project`, `python-package-workflow`, or
`python-ci-workflow` rather than turning this into a generic maintenance skill.

## Output Shape

Return:

1. `Test boundary`: unit, integration, client, artifact, or full suite.
2. `Command`: exact `uv` command and package or path scope.
3. `Configuration`: markers, fixtures, async support, or no change.
4. `Evidence`: tests added or run and concise results.
5. `Residual risk`: live dependency, unrun integration lane, coverage, or CI
   limitation.

## Guardrails

- Do not add coverage tooling or thresholds without a concrete need.
- Do not make unit tests depend on a live network, production service, or
  machine-local secret.
- Do not use `sys.path` edits to hide a package-layout problem.
- Do not leave the old `uv-pytest-unit-testing` skill name, profile path, or
  routing surface behind after this rename.

## References

- `references/pytest-workflow.md`
- `references/uv-workspace-testing.md`
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [FastAPI async tests](https://fastapi.tiangolo.com/advanced/async-tests/)
- [FastAPI dependency overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [FastMCP server testing](https://gofastmcp.com/servers/testing)
