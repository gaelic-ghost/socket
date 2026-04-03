# Project Roadmap

## Vision

Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, plugin-ready packaging, and direct standalone install surfaces.

## Product principles

- Keep skill names clear, stable, and domain-grouped.
- Keep workflow instructions deterministic and safety-forward.
- Keep docs and metadata synchronized with the active skill set.
- Keep this repository focused on broadly useful global-install skills.
- Prefer dedicated language-, framework-, stack-, or repository-specific plugins for project-level or repo-level install.
- Treat agent-skills and agent-plugin repository maintenance as a distinct product line now housed in `/Users/galew/Workspace/agent-plugin-skills`.

## Milestone Progress

- [x] Milestone 0: Naming and structural refactor (completed)
- [x] Milestone 1: Docs skill consolidation and canonical maintenance entrypoints (completed)
- [x] Milestone 2: Validation hardening and maintainer-doc cleanup (completed)
- [x] Milestone 3: Standalone top-level skill recentering (completed)
- [x] Milestone 4: Python tooling and test standardization (completed)
- [x] Milestone 5: Code slice walkthrough skill (completed)
- [x] Milestone 6: Codex plugin-ready repo layout (completed)
- [x] Milestone 7: Docs skill split by document type (completed)
- [x] Milestone 8: Project README maintainer hardening (completed)
- [x] Milestone 9: Codex plugin marketplace wiring (completed)
- [x] Milestone 10: Inventory cleanup after Things and speech split (completed)
- [x] Milestone 11: Plugin-first packaging alignment (completed)
- [x] Milestone 12: `sync-skills-repo-guidance` (moved to `agent-plugin-skills` and removed from local inventory)
- [x] Milestone 13: `bootstrap-skills-plugin-repo` (moved to `agent-plugin-skills` and removed from local inventory)
- [ ] Milestone 14: Claude Code optimization pass
- [x] Milestone 15: Claude plugin support (completed)

## Milestone 0: Naming and structural refactor

Scope:

- Rename skills to the current domain-grouped naming standard.
- Remove deprecated skill directories from active inventory.

Tickets:

- [x] Establish roadmap maintenance under a domain-grouped skill surface.
- [x] Rename workspace cleanup skill to `project-workspace-cleaner`.
- [x] Rename Things reminder skill to `things-reminders-manager`.
- [x] Rename Things digest skill to `things-digest-generator`.

Exit criteria:

- [x] Active skill folder names and frontmatter names match.
- [x] Deprecated names are absent from active invocation references.

## Milestone 1: Docs consolidation and canonical entrypoints

Scope:

- Consolidate docs maintenance skills into a single maintained entrypoint.
- Keep installation and invocation centered on canonical standalone skills.

Tickets:

- [x] Merge prior docs-maintenance skills into `project-docs-maintainer`.
- [x] Preserve both audit modes in the merged docs skill.
- [x] Keep roadmap maintenance under `project-docs-maintainer` through explicit modes.

Exit criteria:

- [x] Docs maintenance behavior remains available via explicit modes.
- [x] Canonical skills are directly installable and independently understandable.

## Milestone 2: Validation hardening and maintainer-doc cleanup

Scope:

- Validate metadata and reference consistency after refactor.
- Reduce repo-maintainer docs to the durable operating set.

Tickets:

- [x] Run stale-name sweeps and reference-integrity checks.
- [x] Validate each skill `agents/openai.yaml` against current SKILL intent.
- [x] Reduce maintainer docs to `AGENTS.md`, `docs/maintainers/reality-audit.md`, and `docs/maintainers/workflow-atlas.md`.
- [x] Consolidate roadmap handling under `project-docs-maintainer` with `mode=roadmap_maintenance`.
- [x] Keep roadmap guidance centered on the canonical docs-maintainer surface.

Exit criteria:

- [x] No stale skill names remain outside explicit compatibility or migration notes.
- [x] Maintainer guidance is reduced to the durable operating set.
- [x] Canonical roadmap ownership is documented under `project-docs-maintainer`.

## Milestone 3: Standalone top-level skill recentering

Scope:

- Remove the repo-level routing surface.
- Recenter docs and install guidance on direct skill invocation.

Tickets:

- [x] Remove the retired routing skill from the active inventory.
- [x] Rewrite public install guidance around standalone top-level skills.
- [x] Remove router-specific maintainer workflow documentation.

Exit criteria:

- [x] Active repo docs present only standalone skill entrypoints.
- [x] Maintainer docs describe the current post-router skill inventory.
- [x] Roadmap maintenance is presented only through the canonical docs-maintainer entrypoint.

## Milestone 4: Python tooling and test standardization

Scope:

- Standardize repo-maintainer Python workflows around the root `uv` tool surface and `pytest`.
- Add baseline smoke-test coverage for Python-backed skills that previously had scripts but no tests.

Tickets:

- [x] Add root `pytest` discovery settings for Python-backed skill test suites.
- [x] Replace lingering ad hoc `PyYAML` execution guidance with the root `uv` dev baseline where appropriate.
- [x] Standardize repo-maintainer Python command guidance on `uv run --group dev ...`.
- [x] Add smoke tests for `project-docs-maintainer`, `project-workspace-cleaner`, and `things-digest-generator`.
- [x] Remove stale direct `unittest` runner assumptions from the speech test surface.

Exit criteria:

- [x] `uv run --group dev pytest` works from repo root as the canonical Python test command.
- [x] Python-backed skills with scripts have at least minimal deterministic smoke-test coverage.
- [x] Repo docs and script dependency messages no longer point at ad hoc `uv --with ...` execution for maintained paths.

## Milestone 5: Code slice walkthrough skill

Scope:

- Add a reusable skill for end-to-end code-slice explanation.
- Normalize pipeline, execution-flow, request-lifecycle, and data-flow requests onto one canonical slice workflow.
- Keep explanation completeness invariant while making explanation density adjustable.

Tickets:

- [x] Add standalone `explain-code-slice` skill with a canonical slice vocabulary.
- [x] Define a structured narrative output contract with summary, walkthrough, diagram, and notes.
- [x] Add detail-level guidance for `quick`, `standard`, and `thorough` without allowing omitted meaningful steps.
- [x] Add a slice-comparison workflow for old/new or side-by-side path explanation.
- [x] Update public repo inventory and install guidance to include the new skill.

Exit criteria:

- [x] The repository contains a standalone skill for slice walkthroughs.
- [x] The skill treats data shape first and execution flow second as the canonical explanation order.
- [x] The skill documents a simple diagram format with branch and data-shape markers.

## Milestone 6: Codex plugin-ready repo layout

Scope:

- Historical note: this milestone captured the earlier repo-root Codex plugin layout and was later superseded by Milestone 11's plugin-subtree packaging model.

- Align the repository layout with the Codex plugins model while keeping skills as the authoring unit.
- Normalize active skill directories under `skills/` and add a repo-root plugin manifest.
- Update repo guidance to treat plugins as the bundle/distribution surface and skills as the workflow surface.

Tickets:

- [x] Add a repo-root Codex plugin manifest at `.codex-plugin/plugin.json`.
- [x] Move active skill directories under the top-level `skills/` directory.
- [x] Update repo docs and maintainer guidance for the new `skills/` layout.
- [x] Update skill-splitting guidance to prefer separate skills bundled by the plugin when workflows are naturally distinct.
- [x] Reconcile maintainer tooling and tests with the new directory layout.

Exit criteria:

- [x] The repository root is plugin-ready for Codex with a valid manifest and `skills/` path.
- [x] No active repo guidance still presents top-level skill directories as the canonical layout.
- [x] Maintainer docs describe plugins as the distribution unit and skills as the authoring unit.

## Milestone 7: Docs skill split by document type

Scope:

- Replace the umbrella docs-maintenance skill with separate README and roadmap skills.
- Keep specialized README maintenance for skills/plugin repositories separate from general project README work.
- Retire `project-docs-maintainer` as a canonical skill without leaving a wrapper behind.

Tickets:

- [x] Split the old roadmap workflow into `maintain-project-roadmap`.
- [x] Split the old skills/plugin README workflow into `maintain-skills-readme`, then moved it to `agent-plugin-skills`.
- [x] Add `maintain-project-readme` as the general ordinary-project README skill.
- [x] Update tests, metadata, and repo docs to use the new skills.
- [x] Retire `project-docs-maintainer` from the active inventory and replace it with compatibility notes in docs.

Exit criteria:

- [x] No active repo docs present `project-docs-maintainer` as canonical.
- [x] README and roadmap maintenance now route through separate skill names.
- [x] General project README maintenance is separated from skills/plugin README maintenance.

## Milestone 8: Project README maintainer hardening

Scope:

- Fix destructive rewrite behavior in `maintain-project-readme`.
- Bring the root `README.md` back to current-state guidance instead of transition-heavy legacy notes.
- Track the next maturity work for project README automation beyond the initial scripted maintainer.

Tickets:

- [x] Preserve rich README preamble content during `maintain-project-readme` apply runs.
- [x] Expand `maintain-project-readme` tests to cover preamble preservation and CLI exit behavior.
- [x] Refresh the root `README.md` to remove retired guidance and reduce duplicate install instructions.
- [x] Add `maintain-project-readme` automation prompts/reference guidance comparable to the other mature maintainer skills.
- [x] Improve repo-profile normalization so profile-specific README structure can be added and normalized more deliberately.

Exit criteria:

- [x] `maintain-project-readme` no longer drops badges, callouts, or extra intro prose before the first H2 section.
- [x] The root `README.md` describes only the current active skill surface and current install guidance.
- [x] `maintain-project-readme` has a documented automation-prompts surface.
- [x] Repo-profile normalization behavior is explicit, documented, and test-backed.

## Milestone 9: Codex plugin marketplace wiring

Scope:

- Historical note: this milestone captured the earlier repo-root marketplace wiring and was later superseded by Milestone 11's plugin-subtree packaging model.

- Add the Codex plugin marketplace file for this repository.
- Make plugin-distribution metadata locally consumable in the expected marketplace surface.
- Keep the repository root as the canonical plugin root instead of introducing a duplicate packaged copy.
- Present bundled Codex plugin installation and direct standalone skill installation as equally supported user-facing paths.

Tickets:

- [x] Add the repo-level Codex marketplace file at `.agents/plugins/marketplace.json`.
- [x] Register the repo-root `productivity-skills` plugin in that marketplace with a local `./` source path.
- [x] Document how `.agents/plugins/marketplace.json` relates to `.codex-plugin/plugin.json` and the repo-root plugin layout.
- [x] Rewrite the root `README.md` install guidance so Codex plugin installation and `skills` CLI installation are both first-class supported paths.
- [x] Verify plugin-manifest and marketplace metadata stay in sync.

Exit criteria:

- [x] A repo-local marketplace file exists and includes this plugin.
- [x] The repo-local marketplace entry points at the repo-root plugin rather than a duplicate plugin copy.
- [x] Repo guidance explains how the marketplace file relates to `.codex-plugin/plugin.json`.
- [x] The root `README.md` presents both supported install paths without treating either one as secondary.
- [x] Plugin packaging metadata and marketplace metadata are consistent.

## Milestone 10: Inventory cleanup after Things and speech split

Scope:

- Restore `explain-code-slice` after its accidental removal.
- Remove speech, workspace-cleanup, and Things workflow claims from the active repo inventory.
- Recenter this repository on the four surviving maintainer and code-walkthrough skills.

Tickets:

- [x] Restore `explain-code-slice` from the last pre-deletion commit.
- [x] Move `things-digest-generator` and `things-reminders-manager` into `../things-app/skills`.
- [x] Remove stale active-inventory references to `project-workspace-cleaner`, `speak-with-profile`, and the moved Things skills.
- [x] Update plugin metadata and maintainer tooling to match the current skill inventory.

Exit criteria:

- [x] `explain-code-slice` is present again in `skills/`.
- [x] The active inventory is limited to the four surviving skills.
- [x] Repo docs and plugin metadata no longer advertise removed or relocated skills.

## Milestone 11: Plugin-first packaging alignment

Scope:

- Move plugin packaging off the repository root and into a dedicated plugin subtree.
- Align Codex and Claude packaging docs around a shared plugin-first story while keeping root `skills/` canonical.
- Point local marketplace metadata at the packaged plugin subtree instead of the repository root.

Tickets:

- [x] Add `plugins/productivity-skills/` as the packaging root.
- [x] Move the Codex plugin manifest into the plugin subtree.
- [x] Add the parallel Claude plugin manifest and hooks scaffold.
- [x] Update repo docs and maintainer docs to describe plugin-first packaging with root `skills/` as the authoring source.
- [x] Retarget `.agents/plugins/marketplace.json` to the plugin subtree.

Exit criteria:

- [x] Codex and Claude packaging manifests live under `plugins/productivity-skills/`.
- [x] The repository no longer documents the repo root as the plugin root.
- [x] README, AGENTS, and maintainer docs describe the same packaging model.

## Milestone 12: `sync-skills-repo-guidance`

Scope:

- Historical note: this milestone was incubated here and then moved into the dedicated agent-plugin maintainer repo at `/Users/galew/Workspace/agent-plugin-skills`.
- `productivity-skills` no longer treats repo-wide agent-stack guidance synchronization as part of its primary growth lane.

Tickets:

- [x] Define the skill scope and trigger surface for skills-repo guidance synchronization.
- [x] Move the skill and its future roadmap ownership into `/Users/galew/Workspace/agent-plugin-skills`.
- [x] Update `productivity-skills` docs to point new agent-stack maintainer work at the dedicated repo.

Exit criteria:

- [x] `productivity-skills` no longer presents this milestone as part of its primary future expansion path.
- [x] The dedicated maintainer repo owns the future roadmap for this workflow.

## Milestone 13: `bootstrap-skills-plugin-repo`

Scope:

- Historical note: this milestone was incubated here and then moved into the dedicated agent-plugin maintainer repo at `/Users/galew/Workspace/agent-plugin-skills`.
- `productivity-skills` no longer treats repo bootstrap for agent-stack repositories as part of its primary future expansion path.

Tickets:

- [x] Define the generated repository layout, including `skills/`, `plugins/<repo>/`, marketplace wiring, and maintainer docs.
- [x] Move the skill and its future roadmap ownership into `/Users/galew/Workspace/agent-plugin-skills`.
- [x] Update `productivity-skills` docs to point new agent-stack repo bootstrap work at the dedicated repo.

Exit criteria:

- [x] `productivity-skills` no longer presents this milestone as part of its primary future expansion path.
- [x] The dedicated maintainer repo owns the future roadmap for this workflow.

## Milestone 14: Claude Code optimization pass

Scope:

- Improve this repository’s skill surfaces for Claude Code routing and ergonomics.
- Reconcile wording, references, and metadata where Claude-specific behavior benefits from tighter optimization.
- Keep Claude-facing improvements additive to the shared standards-based skill core and the existing Codex/OpenAI overlays.

Tickets:

- [ ] Audit skill trigger wording and references for Claude Code activation quality.
- [ ] Add or refine Claude-facing guidance where Codex-first wording currently leaves avoidable ambiguity.
- [ ] Review metadata and examples for Claude Code compatibility and discoverability.

Exit criteria:

- [ ] Active skills have Claude Code-aware trigger and usage guidance where it materially improves routing.
- [ ] Claude-facing docs no longer lag behind the current skill layout and plugin-ready repo model.

## Milestone 15: Claude plugin support

Scope:

- Add first-class Claude plugin packaging support alongside the Codex plugin-ready repo layout.
- Define the repo surfaces needed to bundle and distribute this skill set for Claude plugin workflows.
- Keep Claude plugin packaging aligned with the same root-`skills/` source-of-truth model used for Codex packaging.

Tickets:

- [x] Add the canonical Claude plugin metadata/config surface for this repository.
- [x] Update docs to explain Codex plugin support and Claude plugin support side by side.
- [x] Verify active skills and metadata remain aligned across both plugin ecosystems.

Exit criteria:

- [x] The repository contains a current Claude plugin packaging surface.
- [x] User-facing docs explain the Claude plugin path without conflicting with Codex plugin guidance.
- [x] Cross-ecosystem packaging guidance is internally consistent.

## Risks and mitigations

- Risk: Users still invoke deprecated names.
  Mitigation: keep canonical usage guidance explicit in repo docs and skill prompts.
- Risk: Users may choose the wrong README-maintenance skill.
  Mitigation: keep strong repo-genre routing guidance in `maintain-project-readme` and `maintain-skills-readme`.

## Backlog candidates

- Add lightweight validation tooling for SKILL/frontmatter/openai.yaml alignment.
- Add validation checks for README layout and skill inventory consistency.
