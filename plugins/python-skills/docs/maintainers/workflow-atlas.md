# Workflow Atlas

## Active Surface

`python-skills` now ships with five bundled skills under root `skills/` and thin packaged plugin manifests under `plugins/python-skills/`:

- `bootstrap-python-mcp-service`
- `bootstrap-python-service`
- `integrate-fastapi-fastmcp`
- `bootstrap-uv-python-workspace`
- `uv-pytest-unit-testing`

These are the only active bundled skill surfaces that root docs, plugin metadata, and marketplace metadata should present.

OpenAI packaging is the live release surface today. Claude Code compatibility and packaging should stay additive over the same shared skill bodies rather than creating a second authored surface.

The repository should still support both user-facing install paths:

- direct skill installation from `skills/` into standard `.agents/skills` locations
- plugin installation through `plugins/python-skills/` plus marketplace metadata

## Skill Roles

### `bootstrap-uv-python-workspace`

This is the shared scaffolding base for generic `uv` project and workspace creation. It owns:

- package and service scaffold layout
- default Python/tooling versions
- README template rendering for generated projects
- shared workspace-member conventions

### `bootstrap-python-service`

This skill is the FastAPI-specialized layer on top of the shared `uv` bootstrap surface. It owns:

- FastAPI-oriented app and run-command guidance
- project-versus-workspace entrypoint selection for service creation
- handoff guidance to the shared workspace bootstrap scripts

### `bootstrap-python-mcp-service`

This skill is the FastMCP-specialized layer. It owns:

- FastMCP overlay behavior for generated projects or service members
- OpenAPI and FastAPI mapping-analysis guidance
- the `fastmcp_docs` documentation dependency callout

### `uv-pytest-unit-testing`

This skill owns repo-shape detection and pytest workflow guidance for `uv` repositories. It owns:

- bootstrap guidance for `tool.pytest.ini_options`
- package-targeted `uv run --package ... pytest` patterns
- test troubleshooting order and execution examples

## Contract Shape

Each active skill should maintain the full repo contract:

- frontmatter `name` matches the directory name
- frontmatter includes the repo-required open-standard fields: `license`, `compatibility`, `metadata`, and `allowed-tools`
- `SKILL.md` clearly states when to use the skill and its primary workflow
- script references in `SKILL.md` resolve to real files
- `agents/openai.yaml` presents the same public surface as `SKILL.md`, including interface metadata and invocation policy
- assets and references called out in docs actually exist

## Repo-Level Sources Of Truth

- Root `README.md`: install surface and discovery guidance
- `skills/`: canonical workflow-authoring surface
- `plugins/python-skills/.codex-plugin/plugin.json`: Codex plugin distribution contract
- `plugins/python-skills/.claude-plugin/plugin.json`: Claude plugin distribution contract
- `.agents/plugins/marketplace.json`: repo-local Codex plugin install and smoke-test contract
- `.claude-plugin/marketplace.json`: repo-shared Claude marketplace contract
- `ROADMAP.md`: milestone history and near-term intent
- `AGENTS.md`: repo-local authoring and validation policy
- `docs/maintainers/reality-audit.md`: audit checklist for shipped reality
- `scripts/validate_repo_metadata.py`: mechanical validation for basic integrity

Future vendor surfaces should follow the same split:

- shared skill content stays under `skills/`
- OpenAI-specific packaging stays under `plugins/python-skills/.codex-plugin/` with repo-root marketplace catalogs
- Claude-specific packaging stays under `plugins/python-skills/.claude-plugin/` and the repo-root `.claude-plugin/marketplace.json`
- discovery mirrors stay explicit through `.agents/skills`, `.claude/skills`, and `plugins/python-skills/skills`

## Validation Ownership

Maintainers should validate three layers together whenever the skill surface changes:

1. Root docs:
   - inventory, install commands, and layout
2. Skill contracts:
   - `SKILL.md`, script inventory, references, and metadata
3. Validation path:
   - metadata validator and associated tests

Do not treat one of these layers as authoritative if the others disagree; update all of them in the same pass.

## Scaffold Defaults

Across the bootstrap skills, generated outputs should stay aligned on:

- `pydantic-settings` for typed config loading
- a committed `.env` for safe defaults
- an ignored `.env.local` for machine-local or secret overrides
- validation via `uv run pytest`, `uv run ruff check .`, and `uv run mypy .`
