# Python Skills Plugin Expansion Plan

This plan records the next durable shape for the Socket-hosted `python-skills` plugin.

The plugin already has a useful scaffold and integration surface. The next job is to make it help agents keep working after the first project exists: choose the right Python project shape, write idiomatic Python, diagnose failures, validate package surfaces, align tooling, and keep CI and upgrades grounded in the same `uv` command vocabulary.

## Intent

The `python-skills` plugin should help agents do seven things:

- choose a Python project shape before scaffolding or implementation starts
- bootstrap reproducible `uv` projects, services, workspaces, tests, FastAPI apps, and FastMCP servers
- write idiomatic Python that respects the repository's package layout, type-checking strictness, configuration model, and test boundaries
- run and explain Python test, lint, format, type-check, package, and diagnostics workflows
- maintain Python packaging metadata without accidentally publishing or relying on machine-local paths
- align local commands, CI checks, and upgrade work around `uv`
- keep FastAPI and FastMCP guidance grounded in official documentation and curated MCP ergonomics

This remains a companion guidance plugin, not a runtime plugin. Do not add an MCP server, daemon, custom package registry, private template feed, or machine-local interpreter state unless a later plan explicitly approves that scope.

## Packaging Direction

Keep the guidance as a monorepo-owned child plugin under:

```text
plugins/python-skills/
```

The child plugin owns:

- `.codex-plugin/plugin.json`
- `skills/`
- per-skill `agents/openai.yaml`
- child `AGENTS.md`
- child-local validation scripts and tests for plugin metadata, skill metadata, scaffold smoke tests, and exported workflow contracts

Do not reintroduce a child `README.md` or per-skill `README.md` files by default. Socket's root README remains the user-facing catalog surface, child `AGENTS.md` remains the child operating contract, and this maintainer plan records expansion decisions.

## Naming Convention

Use names that describe what the skill asks the agent to do.

Prefer action-first names when the skill is primarily a directed action:

- `choose-python-project-shape`
- `build-python-project`
- `diagnose-python-project`

Prefer subject-workflow names when the skill is primarily an ongoing maintenance or operating surface:

- `python-package-workflow`
- `python-tooling-style-workflow`
- `python-ci-workflow`
- `python-upgrade-workflow`
- `python-testing-workflow`

Keep existing names unless a cleanup slice explicitly renames the skill and removes the old duplicate surface in the same pass. Do not leave compatibility shims or duplicate overlapping skill paths behind unless Gale explicitly approves that compromise.

## Documentation Sources

Use official documentation first for Python behavior:

- [uv documentation](https://docs.astral.sh/uv/)
- [Python packaging user guide](https://packaging.python.org/)
- [Writing `pyproject.toml`](https://packaging.python.org/guides/writing-pyproject-toml/)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)
- [GitHub Actions Python documentation](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

When a skill relies on documentation, translate the relevant rule into practical workflow guidance. Explain what the doc changes about command choice, package layout, validation scope, configuration, CI, or upgrade risk.

## Current Skill Inventory

The shipped inventory has thirteen skills. The original expansion plan below
predates the later local-first agent-service addition, so this list is the
current source of truth for the audit rather than the older twelve-skill
summary in generated architecture metadata.

### `python-skills:bootstrap-uv-python-workspace`

Keep this as the shared `uv` scaffolding basis.

It should continue to own deterministic project and workspace generation, profile-driven scaffolding, initial `pytest`/`ruff`/`mypy` setup, safe `.env` defaults, and generated next-step commands.

### `python-skills:bootstrap-python-service`

Keep this as the FastAPI-first scaffold path.

It should stay focused on creating new services. Ongoing endpoint, dependency, configuration, and deployment changes belong in a future service workflow rather than making this bootstrap skill too broad.

### `python-skills:bootstrap-python-mcp-service`

Keep this as the FastMCP-first scaffold path.

It should stay focused on creating new MCP server projects and mapping existing APIs into MCP review reports. Ongoing MCP surface design can grow later if repeated FastMCP maintenance work needs its own skill.

### `python-skills:integrate-fastapi-fastmcp`

Keep this as the existing integration bridge.

It should continue to cover mounted FastMCP apps, FastAPI-derived MCP surfaces, combined app shapes, lifespan boundaries, and promotion from generated MCP surfaces to curated MCP tools and resources.

### `python-skills:build-python-agent-service`

Keep this as the local-first Python agent-service implementation workflow.

It owns framework selection, exact-model capability gates, typed tool and
result contracts, evaluation fixtures, and the draft-to-approved-write
promotion boundary. It is intentionally not a generic FastAPI/FastMCP service
maintenance skill, a local-model benchmark, or a multi-agent framework survey.

### `python-skills:uv-pytest-unit-testing`

Keep this for now as the tested pytest setup and execution surface.

Consider renaming or replacing it with `python-testing-workflow` only in a cleanup slice that broadens the skill to cover test selection, failure explanation, coverage, async tests, integration tests, and CI parity. Do not keep both names as long-term duplicates.

## Proposed Skill Inventory

### `python-skills:choose-python-project-shape`

Help an agent decide how Python should fit into a user's project before implementation starts.

This skill should classify the requested work:

- single-package library
- command-line app
- FastAPI service
- FastMCP server
- combined FastAPI and FastMCP surface
- `uv` workspace
- test-only or tooling-only change
- packaging, CI, or upgrade pass
- mixed-language repository where Python is only one project member

The output should recommend project shape, package layout, validation commands, dependency group strategy, generated files, and documentation updates. It should hand off to existing bootstrap skills when scaffolding is the next step.

### `python-skills:build-python-project`

Guide agents through implementation in an existing Python project.

This skill should cover:

- reading `pyproject.toml`, package layout, tests, and existing style before editing
- choosing module boundaries that keep imports straightforward
- preserving typed configuration and environment boundaries
- using small composable functions and explicit inputs/outputs where practical
- keeping framework adapters thin around reusable project logic
- adding focused tests around changed behavior
- running the narrowest useful `uv run` validation command first

This is the general implementation skill, not a replacement for specialized FastAPI, FastMCP, package, test, or CI workflows.

### `python-skills:diagnose-python-project`

Help agents find the first meaningful cause of Python failures.

This skill should cover:

- missing or mismatched Python versions
- `uv` sync, lock, and dependency-group issues
- import path and package layout problems
- test discovery and fixture failures
- Ruff lint or format failures
- mypy configuration, missing stubs, and type-check failures
- FastAPI app import or lifespan failures
- FastMCP server startup and tool-registration failures
- packaging metadata and build failures

Diagnostics should report what command failed, which phase failed, the likely cause, and the smallest useful next check.

### `python-skills:python-package-workflow`

Validate Python package surfaces before release or publication.

This skill should cover:

- package metadata in `pyproject.toml`
- build-system selection and package discovery
- dependency versus optional dependency versus dependency-group boundaries
- README, license, classifiers, project URLs, and package description expectations
- local build validation
- local package smoke checks
- semantic versioning and release notes
- PyPI or private index publication as an explicit release step only

It should not publish packages unless the user explicitly asks for that release step or repo-local release automation owns it.

### `python-skills:python-tooling-style-workflow`

Align Python formatting, linting, type checking, and local tooling.

This skill should cover:

- Ruff formatter and linter setup
- mypy configuration and staged strictness
- `pytest` configuration when it intersects with tooling
- `pyproject.toml` versus dedicated config file choices
- dependency groups for maintainer tools
- pre-commit or editor integration only when the repo already uses it or the user asks
- keeping formatting-only sweeps separate from behavior changes when practical

The workflow should preserve repo-local conventions and avoid forcing strictness upgrades into unrelated feature work.

### `python-skills:python-ci-workflow`

Guide agents through Python CI setup and maintenance.

This skill should cover:

- GitHub Actions setup for Python and `uv`
- dependency caching choices
- `uv sync --dev` or equivalent repo-local install commands
- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format --check .` when formatting is enforced
- `uv run mypy .`
- package build checks when package surfaces exist
- matrix decisions for Python versions and operating systems

CI should prove the same behavior maintainers care about locally and avoid publishing as a side effect.

### `python-skills:python-upgrade-workflow`

Guide agents through Python, dependency, framework, and tooling upgrades.

This skill should cover:

- current Python version requirements
- `uv.lock`
- dependency groups and optional dependencies
- FastAPI, FastMCP, Pydantic, Ruff, mypy, and pytest upgrade notes
- staged validation
- contributor setup or package-consumer migration notes when requirements change

Use this when changing Python version support, package versions, lockfiles, or framework major versions.

## First Implementation Slice

The first slice should repair the current child contract and add the core missing operating skills:

- [x] Fix `plugins/python-skills/scripts/validate_repo_metadata.py` so it validates the child `AGENTS.md`, plugin manifest, and skill metadata without expecting a removed child `README.md`.
- [x] Update child tests so they assert the current no-child-README contract.
- [x] Record this expansion plan.
- [x] Add `python-skills:choose-python-project-shape`.
- [x] Add `python-skills:build-python-project`.
- [x] Add `python-skills:diagnose-python-project`.
- [x] Add `python-skills:python-package-workflow`.
- [x] Add `python-skills:python-tooling-style-workflow`.
- [x] Update `plugins/python-skills/.codex-plugin/plugin.json` default prompts and long description after the new skills exist.
- [x] Run child validation with `uv run scripts/validate_repo_metadata.py`, `uv run pytest`, `uv run ruff check .`, and `uv run mypy .`.
- [x] Run root Socket metadata validation with `uv run scripts/validate_socket_metadata.py`.

## Second Implementation Slice

The second slice should cover repeated project operations that become more valuable after the core skill set lands:

- [x] Add `python-skills:python-ci-workflow`.
- [x] Add `python-skills:python-upgrade-workflow`.
- [x] Decide whether to broaden `uv-pytest-unit-testing` into `python-testing-workflow`; keep `uv-pytest-unit-testing` for this release so existing prompts and routing remain compatible.
- [ ] Decide whether ongoing FastAPI service maintenance needs a dedicated `fastapi-service-workflow`.
- [ ] Decide whether ongoing FastMCP server maintenance needs a dedicated `fastmcp-service-workflow`.
- [x] Add install testing with a temporary `CODEX_HOME` if the exported skill surface or plugin metadata changes enough to need plugin-install verification.

## Deferred Scope

After the first two slices prove useful, consider deeper specialized workflows:

- data science and notebook workflows
- Django workflows
- Typer or Click CLI workflows
- async service performance diagnostics
- package publishing automation
- Python MCP server runtime diagnostics beyond FastMCP guidance
- generated project-template maintenance beyond the current shell scaffold scripts
- bundled MCP servers or app connectors

## Open Decisions Before Implementation

### Testing Skill Name

Decision for now: keep `uv-pytest-unit-testing`.

A future cleanup can rename or replace it with `python-testing-workflow` when the scope grows beyond unit-test setup and `uv`-targeted pytest execution. If that cleanup happens, remove the old duplicate skill path in the same pass unless Gale explicitly approves a compatibility period.

### Service Workflow Timing

Decision for the first slice: defer ongoing FastAPI and FastMCP service workflows.

The existing bootstrap and integration skills already cover new service creation and combined FastAPI/FastMCP architecture. Add service-maintenance workflows only after the general `build-python-project` and `diagnose-python-project` skills prove where specialized service guidance should branch.

### Script Depth

Decision for the first slice: keep the new operating skills as guidance-first.

The existing bootstrap and pytest skills already own deterministic shell entrypoints. Add scripts to new skills only when repeated command generation or validation behavior becomes mechanical enough to test directly.

### Versioning And Marketplace Timing

Decision for this expansion: treat the full first implementation slice as a likely Socket minor release candidate.

The validator repair alone is a maintenance fix. Adding the new skill inventory is user-facing plugin capability and should likely publish as a minor release when the branch is ready.

## Follow-Up Audit: 2026-07-29

### Audit Result

The plugin has a coherent general Python path now: choose a shape, bootstrap
it, build it, diagnose failures, test it, align tooling, validate packaging,
maintain CI, and plan upgrades. The next pass should be a focused cleanup and
service-maintenance expansion, not another broad scaffold expansion.

The existing bootstrap skills remain distinct user-facing entry points:

- `bootstrap-uv-python-workspace` owns generic package or service scaffolds.
- `bootstrap-python-service` owns FastAPI-first scaffolds.
- `bootstrap-python-mcp-service` owns FastMCP-first scaffolds.

Do not merge or rename those three installed skill names. They express three
different starting intents and already share their actual scaffold mechanics.
Instead, consolidate their repeated prose, validation vocabulary, configuration
policy, and handoff matrix through shared references or a small common
bootstrap-contract asset. That preserves clear discovery without maintaining
three copies of the same policy.

### Immediate Contract Repairs

Complete these in one small maintenance slice before adding a new workflow:

- [ ] Correct the maintainer inventory to include
  `build-python-agent-service`, then refresh the root architecture model in a
  dedicated cross-plugin architecture pass. Do not hand-edit only the Python
  entries: the current architecture audit reports stale targets in other
  plugins too.
- [ ] Remove the packaged dependency claim for `fastmcp_docs`, or add a
  deliberately approved bundled MCP declaration plus its required Hermes
  translation. The current plugin has two skills that require that server in
  their metadata, but it does not ship the corresponding `.mcp.json` source.
  The preferred narrow repair is to say “use `fastmcp_docs` when the host has
  configured it; otherwise use the official FastMCP documentation,” and make
  that dependency optional in the skill metadata.
- [ ] Update `python-ci-workflow` to distinguish local development checks from
  reproducible locked CI. For a repository that commits `uv.lock`, the default
  CI example should use `uv sync --locked --all-extras --dev` only when those
  extras and development groups are part of the tested contract; it should not
  imply that every project needs all extras.
- [ ] Add a concrete isolated wheel and sdist smoke-check recipe to
  `python-package-workflow`, while keeping publication explicitly outside the
  workflow. The current prose asks for a temporary consumer but leaves the
  most important artifact-install proof underspecified.
- [ ] Make all agent-service Python execution examples `uv`-based and remove
  the unused unrestricted `Bash(python:*)` tool allowance from
  `build-python-agent-service` unless a tested workflow truly needs it.

### Consolidation Slice

Create one shared bootstrap contract reference used by all three bootstrap
skills. It should own only the common policy:

- `uv` command and dependency-group vocabulary;
- safe configuration defaults, secret boundaries, and typed settings;
- `pytest`, Ruff, mypy, and optional formatting-check command selection;
- project versus workspace decision and handoff rules;
- generated-artifact, git-initialization, and temporary-scaffold cleanup
  boundaries.

Each existing skill should retain only its special behavior: generic profile
selection, FastAPI overlay, or FastMCP overlay and API-mapping review. This is
a durable documentation building block, not a runtime abstraction or another
scaffold layer.

### Next New Workflows

Prioritize these two workflows after the contract repairs. They answer the two
open decisions from the original expansion plan and cover real work that the
current bootstrap and integration skills intentionally stop before.

1. `fastapi-service-workflow`
   - Own existing-service route composition, typed settings and dependency
     overrides, lifespan, async and integration testing, OpenAPI boundary
     review, deployment-readiness handoff, and service-specific diagnostics.
   - Hand package, CI, general tooling, and FastMCP work back to their current
     owners instead of duplicating them.
2. `fastmcp-service-workflow`
   - Own existing-server transport and lifespan behavior, tool/resource/prompt
     curation, authorization and input boundaries, client integration tests,
     generated-surface review, and upgrade diagnostics.
   - Pin implementation decisions to the installed FastMCP version and its
     release documentation; the public FastMCP docs track `main` and can
     describe unreleased behavior.

### Testing Workflow Decision

Replace `uv-pytest-unit-testing` with `python-testing-workflow` in one
deliberate cleanup release. The new skill should cover test selection,
fixtures, parametrization, async tests, integration boundaries, coverage when
requested, workspace-member targeting, failure triage, and local-to-CI parity.
Remove the old skill in that same pass and update every routing, prompt,
Hermes-export, architecture, and compatibility surface. Do not keep two
overlapping testing skills or add a compatibility shim unless Gale explicitly
approves a temporary migration window.

### Deliberately Deferred Expansions

These are useful only after evidence of repeated demand; they should not be
folded into the general implementation skill:

- a CLI workflow for Typer or Click;
- a data and notebook workflow, preferably including reproducibility and
  environment/kernel boundaries;
- a Django workflow;
- a background-job and task-queue workflow;
- a persistence workflow for SQLAlchemy and migration ownership;
- publishing automation, which remains an explicit release decision rather
  than a normal package-validation feature.

### Definition Of Done For The Follow-Up

- [ ] Every shipped Python skill appears in the child plan, plugin discovery
  metadata, portable export decision, and regenerated architecture inventory.
- [ ] Each declared MCP dependency is packaged and translated, explicitly
  host-provided, or removed.
- [ ] Bootstrap policies have one shared source while each entry point keeps a
  narrow, distinct purpose.
- [ ] CI guidance demonstrates both fast local iteration and locked,
  reproducible verification without overgeneralizing either command.
- [ ] FastAPI and FastMCP maintenance each have a clear owning workflow.
- [ ] The renamed testing workflow replaces, rather than shadows, the current
  unit-testing skill.

## Definition Of Done

The expansion is ready when:

- [x] The child validator passes without requiring a child `README.md`.
- [x] The plugin has a documented skill naming convention and expansion plan.
- [x] The first new skill set covers project choice, implementation, diagnostics, packaging, and tooling/style alignment.
- [x] The second new skill set covers CI and upgrade workflows.
- [x] The guidance consistently uses `uv` for Python command examples.
- [x] The guidance uses official documentation as the source of truth for Python packaging, `uv`, pytest, Ruff, mypy, FastAPI, FastMCP, and CI behavior.
- [x] Root Socket docs, plugin metadata, child validation, and root validation agree on the exported Python skill surface.
