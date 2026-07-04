---
name: uv-pytest-unit-testing
description: Set up and run unit tests for Python uv projects and uv workspaces with pytest. Use when creating or updating pytest configuration in pyproject.toml, installing pytest dev dependencies with uv, running tests in a workspace member package via `uv run --package`, customizing pytest workflow defaults through layered YAML profiles, organizing tests with fixtures/markers/parametrize, or troubleshooting test discovery and import failures.
license: Apache-2.0
compatibility: Designed for Codex and compatible Agent Skills clients on macOS with uv-managed Python projects, pytest, and shell access for the bundled scripts.
metadata:
  owner: gaelic-ghost
  repo: python-skills
  category: python-testing
allowed-tools: Bash(uv:*) Read
---

# Uv Pytest Unit Testing

## Purpose

Use this skill to standardize pytest setup and execution for uv-managed Python repositories, including single-project repos and uv workspaces.

## When To Use

- Use this skill for pytest setup, execution, and troubleshooting in `uv`-managed repositories.
- Use this skill when the user wants package-targeted pytest runs for a workspace member.
- Keep scope on test setup and execution; do not use this as a generic repo bootstrap skill.

## Primary Workflow

1. Detect repository mode.
   - Treat the repo as a workspace when `pyproject.toml` defines `[tool.uv.workspace]`.
   - Treat it as a single project otherwise.
2. Bootstrap pytest dependencies and baseline config:
   - `scripts/bootstrap_pytest_uv.sh --workspace-root <repo>`
   - add `--package <member-name>` for workspace-member setup
   - add `--with-cov` when the task explicitly wants `pytest-cov`
   - add `--dry-run` when previewing changes
3. Run tests:
   - `scripts/run_pytest_uv.sh --workspace-root <repo>`
   - `scripts/run_pytest_uv.sh --workspace-root <repo> --package <member-name>`
4. Troubleshoot failures in this order:
   - command context
   - test discovery layout
   - marker registration
   - import-path assumptions

## Test Authoring Guidance

- Keep fast unit tests under `tests/unit` and integration-heavy tests under `tests/integration` when repo size warrants separation.
- Use fixtures for setup reuse, and keep fixture scope minimal (`function` by default).
- Use `@pytest.mark.parametrize` for matrix-style cases instead of hand-written loops.
- Use `monkeypatch` for environment variables and runtime dependency replacement.
- When generated projects use `pydantic-settings`, prefer overriding environment variables or the settings dependency rather than mutating committed `.env` files in tests.
- Register custom marks in config to avoid marker warnings.

## Automation Suitability

- Codex App automation: High. Strong recurring fit for test health checks, failure triage, and drift detection.
- Codex CLI automation: High. Strong fit for non-interactive test setup and targeted test sweeps.

## Codex App Automation Prompt Template

```markdown
Use $uv-pytest-unit-testing.

Scope boundaries:
- Work only inside <REPO_PATH>.
- Operate only on pytest setup and test execution tasks.
- Do not perform unrelated code refactors.

Task:
1. Detect repository mode from <WORKSPACE_ROOT>/pyproject.toml.
2. If <DRY_RUN_BOOTSTRAP:TRUE|FALSE> is TRUE, run:
   `scripts/bootstrap_pytest_uv.sh --workspace-root <WORKSPACE_ROOT> <PACKAGE_FLAG> <WITH_COV_FLAG> --dry-run`
3. If <DRY_RUN_BOOTSTRAP:TRUE|FALSE> is FALSE, run:
   `scripts/bootstrap_pytest_uv.sh --workspace-root <WORKSPACE_ROOT> <PACKAGE_FLAG> <WITH_COV_FLAG>`
4. Run tests with:
   `scripts/run_pytest_uv.sh --workspace-root <WORKSPACE_ROOT> <PACKAGE_FLAG> <TEST_PATH_FLAG> -- <PYTEST_ARGS>`
5. Keep package-targeted runs explicit when <PACKAGE_NAME_OR_EMPTY> is set.

Output contract:
1. STATUS: PASS or FAIL
2. SETUP: what bootstrap actions ran
3. TEST_RESULTS: concise pass/fail summary
4. FAILURES: grouped likely causes
5. NEXT_STEPS: minimal remediation actions
```

## Codex CLI Automation Prompt Template

```bash
codex exec --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

`<PROMPT_BODY>` template:

```markdown
Use $uv-pytest-unit-testing.
Limit scope to pytest setup and execution in <WORKSPACE_ROOT>.
Run bootstrap in dry-run or real mode based on <DRY_RUN_BOOTSTRAP:TRUE|FALSE>.
Run tests with explicit package targeting when <PACKAGE_NAME_OR_EMPTY> is set.
Return STATUS, setup actions, concise test summary, grouped likely causes for failures, and minimal next steps.
```

## Customization Placeholders

- `<REPO_PATH>`
- `<WORKSPACE_ROOT>`
- `<PACKAGE_NAME_OR_EMPTY>`
- `<PACKAGE_FLAG>`
- `<TEST_PATH_OR_EMPTY>`
- `<TEST_PATH_FLAG>`
- `<PYTEST_ARGS>`
- `<WITH_COV_FLAG:--with-cov|EMPTY>`
- `<DRY_RUN_BOOTSTRAP:TRUE|FALSE>`

## Interactive Customization Workflow

1. Ask whether users want bootstrap mode or run mode.
2. Gather workspace root and optional package target.
3. For bootstrap mode, gather `with_cov` and `dry_run`.
4. For run mode, gather optional test path and optional pytest args.
5. Return both:
- A YAML profile for durable reuse.
- The exact command to run.
6. Use this precedence order:
- CLI flags
- `--config` profile file
- `.codex/profiles/uv-pytest-unit-testing/customization.yaml`
- `~/.config/gaelic-ghost/python-skills/uv-pytest-unit-testing/customization.yaml`
- Script defaults
7. If users want temporary reset behavior:
- `--bypassing-all-profiles`
- `--bypassing-repo-profile`
- `--deleting-repo-profile`
8. If users provide no customization or profile files, keep existing script defaults unchanged.
9. See [`references/interactive-customization.md`](references/interactive-customization.md) for schema and examples.

## Outputs

- `status`
  - `success`: setup or test execution completed
  - `blocked`: repo shape or prerequisites prevented the run
  - `failed`: bootstrap or test execution ran but did not complete cleanly
- `path_type`
  - `primary`: canonical shell entrypoints completed
- `output`
  - setup actions taken
  - exact run command used
  - concise failure grouping when applicable

## Guardrails

- Require `uv` for all installation and execution paths.
- Require an existing `pyproject.toml` under `--workspace-root`.
- Keep package targeting explicit when operating on a workspace member.

## References

- `references/pytest-workflow.md`
- `references/uv-workspace-testing.md`
- `references/customization.md`
- `references/interactive-customization.md`

## Script Inventory

- `scripts/bootstrap_pytest_uv.sh`
- `scripts/run_pytest_uv.sh`
