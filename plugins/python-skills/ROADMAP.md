# Project Roadmap

## Vision

- Keep `python-skills` as a focused, durable skills repository with one shared `skills/` surface, deterministic local helpers, OpenAI-first packaging today, and a clean path to Claude Code support without duplicating the skills themselves.

## Product principles

- Keep the active public surface constrained to one shared `skills/` tree with thin vendor packaging layers on top.
- Prefer deterministic local scripts and validation over implied behavior.
- Keep skill docs, metadata, and script behavior synchronized.
- Keep plugin packaging, marketplace metadata, and maintainer tooling simple and repo-local rather than adding new abstraction layers.
- Prefer portable Agent Skills content first, then add vendor-specific optimizations only where they are materially useful.

## Milestone Progress

- [x] Milestone 1: Initial Python skill bundle
- [x] Milestone 2: FastAPI and FastMCP bootstrap coverage
- [x] Milestone 3: `uv` pytest workflow coverage
- [x] Milestone 4: Standards alignment and maintainer contract
- [x] Milestone 5: Validation expansion and release hardening
- [x] Milestone 6: Codex plugin packaging
- [ ] Milestone 7: Claude Code skill optimizations
- [x] Milestone 8: Claude plugin and marketplace support
- [x] Milestone 9: Use `Agent Plugin Skills` plugin to align repo with skills/plugin repo standards
- [x] Milestone 10: FastAPI and FastMCP integration workflows

## Milestone 1: Initial Python skill bundle

Scope:

- [x] Establish the repository and initial Python bootstrap surfaces.

Tickets:

- [x] Ship the first `uv` bootstrap skill.
- [x] Add repository-level install guidance.

Exit criteria:

- [x] The repository exists in a usable published form with Python-focused skills.

## Milestone 2: FastAPI and FastMCP bootstrap coverage

Scope:

- [x] Expand the repository beyond generic `uv` scaffolding into service-oriented workflows.

Tickets:

- [x] Add FastAPI bootstrap support.
- [x] Add FastMCP bootstrap support.
- [x] Include baseline verification commands in the shipped workflow guidance.

Exit criteria:

- [x] FastAPI and FastMCP bootstrap tasks are covered by active standalone skills.

## Milestone 3: `uv` pytest workflow coverage

Scope:

- [x] Add a dedicated pytest setup and execution skill for `uv` repositories.

Tickets:

- [x] Add bootstrap guidance for pytest in `uv` projects and workspaces.
- [x] Add package-targeted execution guidance for workspace members.

Exit criteria:

- [x] The repository includes a dedicated test workflow skill alongside the bootstrap skills.

## Milestone 4: Standards alignment and maintainer contract

Scope:

- [x] Align repo docs, roadmap shape, maintainer docs, skill contracts, and metadata with the standards used in the more recent skill repositories.

Tickets:

- [x] Rewrite the root `README.md` to the canonical section schema.
- [x] Add checklist-style `ROADMAP.md`.
- [x] Add `docs/maintainers/workflow-atlas.md` and `docs/maintainers/reality-audit.md`.
- [x] Retire per-skill `README.md` files as maintained surfaces.
- [x] Normalize each skill’s `SKILL.md` and `agents/openai.yaml` against shipped behavior.
- [x] Add repo-local metadata validation tooling and tests.
- [x] Normalize developer-facing shell entrypoints toward the repo’s Zsh-oriented shell policy.

Exit criteria:

- [x] Repo docs, maintainer docs, skill metadata, and validation tooling all describe the same active surface.

## Milestone 5: Validation expansion and release hardening

Scope:

- [x] Extend validation and smoke coverage now that the repo has a canonical maintainer contract.

Tickets:

- [x] Add validation for richer skill frontmatter and `agents/openai.yaml` metadata.
- [x] Align shipped scaffolds on `pydantic-settings`, committed `.env`, and ignored `.env.local`.
- [x] Document the repo’s standards and scaffold defaults in maintainer-facing docs.

Exit criteria:

- [x] Metadata validation, maintainer policy, and generated scaffold defaults now describe the same standards-aligned surface.

## Milestone 6: Codex plugin packaging

Scope:

- [x] Convert the repository from a flat skill bundle into a plugin-first Codex distribution root.

Tickets:

- [x] Move shipped skills under `skills/`.
- [x] Add `.codex-plugin/plugin.json`.
- [x] Add `.agents/plugins/marketplace.json` for local plugin testing.
- [x] Rewrite root docs and maintainer docs around the plugin-first layout.
- [x] Extend metadata validation to cover plugin packaging and the `skills/` directory layout.

Exit criteria:

- [x] The repo validates as a Codex plugin root and the bundled-skill inventory matches the live `skills/` tree.

## Milestone 7: Claude Code skill optimizations

Scope:

- [ ] Audit the shared `skills/` content for Claude Code compatibility and additive Claude-oriented improvements.

Tickets:

- [ ] Review each shipped `SKILL.md` against Claude Code skill behavior and supported frontmatter.
- [ ] Make shared skill wording more vendor-neutral where that improves portability.
- [ ] Define a maintainer policy for Claude-only skill optimizations so they stay additive rather than invasive.
- [ ] Update maintainer docs to explain the shared-core versus vendor-layer split.

Exit criteria:

- [ ] Shared skills remain single-source and intentionally portable.
- [ ] Claude-specific skill optimizations are documented or implemented without duplicating the skill tree.

## Milestone 8: Claude plugin and marketplace support

Scope:

- [x] Add Claude Code plugin packaging and local marketplace support on top of the shared `skills/` tree.

Tickets:

- [x] Add `plugins/python-skills/.claude-plugin/plugin.json`.
- [x] Add Claude marketplace metadata and maintainer install/testing guidance.
- [x] Extend validation to cover Claude packaging files and expected structure.
- [x] Add smoke coverage for the Claude packaging contract.
- [x] Document how OpenAI and Claude packaging surfaces coexist in one repository.

Exit criteria:

- [x] The repository supports both OpenAI Codex and Claude Code plugin packaging from the same shared `skills/` tree.
- [x] Vendor packaging surfaces stay thin and do not duplicate the underlying skill content.

## Milestone 9: Use `Agent Plugin Skills` plugin to align repo with skills/plugin repo standards

Scope:

- [x] Use the repo-scoped `agent-plugin-skills` plugin to audit and align this repository with the current shared skills/plugin repo standards.

Tickets:

- [x] Confirm the repo-scoped `agent-plugin-skills` install stays current for local maintainer work.
- [x] Use `sync-skills-repo-guidance`, `validate-plugin-install-surfaces`, `maintain-plugin-docs`, and bootstrap guidance where relevant to identify standards drift.
- [x] Align repo docs, packaging surfaces, marketplaces, ignores, and maintainer guidance with the current shared standards without flattening repo-specific policy.

Exit criteria:

- [x] The repository validates cleanly against the current shared skills/plugin repo standards.
- [x] Repo docs, plugin packaging, marketplace wiring, and maintainer guidance describe the same live behavior.

## Milestone 10: FastAPI and FastMCP integration workflows

Scope:

- [x] Add a dedicated skill for integrating FastAPI and FastMCP in existing or evolving `uv` projects.
- [x] Document the core composition patterns for mounting, generating, combining, and promoting FastAPI/FastMCP surfaces.
- [x] Wire the adjacent bootstrap skills to hand off to the integration skill when the task is not fresh scaffolding.

Tickets:

- [x] Add the `integrate-fastapi-fastmcp` skill under the shared `skills/` tree.
- [x] Update the bootstrap skill handoff guidance to mention the new integration path.
- [x] Add the new skill to the root discovery docs and plugin packaging metadata.

Exit criteria:

- [x] The repository describes FastAPI/FastMCP integration as a first-class workflow alongside bootstrap coverage.
- [x] The new skill is discoverable from the root docs and adjacent bootstrap skills.
