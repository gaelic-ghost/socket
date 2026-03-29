# Project Roadmap

## Vision

Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, plugin-ready packaging, direct standalone install surfaces, and cross-cutting speech output where audio delivery improves productivity.

## Product principles

- Keep skill names clear, stable, and domain-grouped.
- Keep workflow instructions deterministic and safety-forward.
- Keep docs and metadata synchronized with the active skill set.

## Milestone Progress

- [x] Milestone 0: Naming and structural refactor (completed)
- [x] Milestone 1: Docs skill consolidation and canonical maintenance entrypoints (completed)
- [x] Milestone 2: Validation hardening and maintainer-doc cleanup (completed)
- [x] Milestone 3: Standalone top-level skill recentering (completed)
- [x] Milestone 4: Speech workflow expansion (completed)
- [ ] Milestone 5: Speech summarization planning (planned)
- [ ] Milestone 6: Default profile expansion planning (planned)
- [ ] Milestone 7: Cross-agent speech compatibility planning (planned)
- [x] Milestone 8: Python tooling and test standardization (completed)
- [x] Milestone 9: Code slice walkthrough skill (completed)
- [x] Milestone 10: Codex plugin-ready repo layout (completed)
- [x] Milestone 11: Docs skill split by document type (completed)

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

## Milestone 4: Speech workflow expansion

Scope:

- Add a canonical speech workflow that fits the repo's standalone skill model.
- Keep repo messaging centered on productivity workflows while broadening the inventory to include audio-output use cases.

Tickets:

- [x] Migrate `speak-with-profile` into this repository as a standalone top-level skill.
- [x] Reframe the moved skill around narrated notes, spoken drafts, audio summaries, and hands-free review.
- [x] Keep profile-based accessibility options and disclosure policy as part of the canonical speech workflow.
- [x] Update public install guidance and repo inventory to include the new speech skill.

Exit criteria:

- [x] `speak-with-profile` is listed alongside the other standalone skills in repo docs.
- [x] The moved skill metadata and runtime docs describe a productivity-first speech workflow.
- [x] Repo-level docs no longer imply that productivity workflows exclude speech-output tasks.

## Milestone 5: Speech summarization planning

Scope:

- Plan the next speech feature set around summarize-then-speak workflows without changing the current public skill contract.
- Define the intended planning surface for summarization modes, targeting, and safety constraints before implementation starts.

Tickets:

- [ ] Define the planning envelope for summarize-then-speak workflows in `speak-with-profile`.
- [ ] Identify candidate summarize modes and their intended use cases for productivity listening.
- [ ] Plan length-targeting and output-shaping behavior for audio summaries.
- [ ] Plan safety constraints for summaries that must preserve entities, numbers, and ordered steps.
- [ ] Define the validation and regression-test strategy for summarize-then-speak behavior.

Exit criteria:

- [ ] The roadmap describes summarize-then-speak as a concrete planned milestone with bounded tickets.
- [ ] No implementation claims are made for summarization features that do not exist yet.

## Milestone 6: Default profile expansion planning

Scope:

- Plan a broader starter profile set for common productivity listening tasks beyond the current baseline examples.
- Keep accessibility-conscious defaults as part of the canonical speech workflow while expanding productivity-oriented options.

Tickets:

- [ ] Define the first additional default profiles to add beyond the current baseline.
- [ ] Plan profile coverage for narrated notes, spoken drafts, audio summaries, and review-oriented listening.
- [ ] Plan how new defaults should balance general productivity use with accessibility-friendly listening needs.
- [ ] Define the documentation and example updates required when new default profiles are introduced.

Exit criteria:

- [ ] The roadmap names the next profile-expansion work as a planned milestone.
- [ ] The milestone identifies a small curated default-profile expansion rather than an open-ended profile catalog.

## Milestone 7: Cross-agent speech compatibility planning

Scope:

- Plan paths for `speak-with-profile` compatibility beyond Codex's built-in `$speech` workflow.
- Explore multiple agent surfaces without promising implementation until target-specific constraints are understood.

Tickets:

- [ ] Evaluate Claude Code compatibility for speech-oriented workflows and delegation patterns.
- [ ] Evaluate Claude Desktop compatibility for profile-aware speech workflows.
- [ ] Evaluate OpenCode as an initial open-source coding-agent target.
- [ ] Evaluate Aider as a backup open-source compatibility candidate.
- [ ] Identify adapter and documentation constraints needed to support multiple agent speech capabilities without fragmenting the canonical skill.

Exit criteria:

- [ ] The roadmap explicitly names Claude Code, Claude Desktop, OpenCode, and Aider as initial planning targets.
- [ ] The milestone remains planning-only and does not imply existing multi-agent support.

## Milestone 8: Python tooling and test standardization

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

## Milestone 9: Code slice walkthrough skill

Scope:

- Add a reusable skill for end-to-end code-slice explanation.
- Normalize pipeline, execution-flow, request-lifecycle, and data-flow requests onto one canonical slice workflow.
- Keep explanation completeness invariant while making explanation density adjustable.

Tickets:

- [x] Add standalone `code-slice-explainer` skill with a canonical slice vocabulary.
- [x] Define a structured narrative output contract with summary, walkthrough, diagram, and notes.
- [x] Add detail-level guidance for `quick`, `standard`, and `thorough` without allowing omitted meaningful steps.
- [x] Add a slice-comparison workflow for old/new or side-by-side path explanation.
- [x] Update public repo inventory and install guidance to include the new skill.

Exit criteria:

- [x] The repository contains a standalone skill for slice walkthroughs.
- [x] The skill treats data shape first and execution flow second as the canonical explanation order.
- [x] The skill documents a simple diagram format with branch and data-shape markers.

## Milestone 10: Codex plugin-ready repo layout

Scope:

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

## Milestone 11: Docs skill split by document type

Scope:

- Replace the umbrella docs-maintenance skill with separate README and roadmap skills.
- Keep specialized README maintenance for skills/plugin repositories separate from general project README work.
- Retire `project-docs-maintainer` as a canonical skill without leaving a wrapper behind.

Tickets:

- [x] Split the old roadmap workflow into `maintain-project-roadmap`.
- [x] Split the old skills/plugin README workflow into `maintain-skills-readme`.
- [x] Add `maintain-project-readme` as the general ordinary-project README skill.
- [x] Update tests, metadata, and repo docs to use the new skills.
- [x] Retire `project-docs-maintainer` from the active inventory and replace it with compatibility notes in docs.

Exit criteria:

- [x] No active repo docs present `project-docs-maintainer` as canonical.
- [x] README and roadmap maintenance now route through separate skill names.
- [x] General project README maintenance is separated from skills/plugin README maintenance.

## Milestone 12: Project README maintainer hardening

Scope:

- Fix destructive rewrite behavior in `maintain-project-readme`.
- Bring the root repo README back to current-state guidance instead of transition-heavy legacy notes.
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

## Milestone 13: Codex plugin marketplace wiring

Scope:

- Add the Codex plugin marketplace file for this repository.
- Make plugin-distribution metadata locally consumable in the expected marketplace surface.
- Keep repo-root plugin packaging aligned with future marketplace usage.

Tickets:

- [ ] Add the repo-level Codex plugin marketplace file with this plugin registered.
- [ ] Document marketplace-file expectations and ordering metadata for this repository.
- [ ] Verify plugin-manifest and marketplace metadata stay in sync.

Exit criteria:

- [ ] A repo-local marketplace file exists and includes this plugin.
- [ ] Repo guidance explains how the marketplace file relates to `.codex-plugin/plugin.json`.
- [ ] Plugin packaging metadata and marketplace metadata are consistent.

## Milestone 14: Claude Code optimization pass

Scope:

- Improve this repository’s skill surfaces for Claude Code routing and ergonomics.
- Reconcile wording, references, and metadata where Claude-specific behavior benefits from tighter optimization.

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

Tickets:

- [ ] Add the canonical Claude plugin metadata/config surface for this repository.
- [ ] Update docs to explain Codex plugin support and Claude plugin support side by side.
- [ ] Verify active skills and metadata remain aligned across both plugin ecosystems.

Exit criteria:

- [ ] The repository contains a current Claude plugin packaging surface.
- [ ] User-facing docs explain the Claude plugin path without conflicting with Codex plugin guidance.
- [ ] Cross-ecosystem packaging guidance is internally consistent.

## Risks and mitigations

- Risk: Users still invoke deprecated names.
  Mitigation: keep canonical usage guidance explicit in repo docs and skill prompts.
- Risk: Users may choose the wrong README-maintenance skill.
  Mitigation: keep strong repo-genre routing guidance in `maintain-project-readme` and `maintain-skills-readme`.

## Backlog candidates

- Add lightweight validation tooling for SKILL/frontmatter/openai.yaml alignment.
- Add validation checks for README layout and skill inventory consistency.
- Add broader automated testing for Things workflow surfaces, including deterministic validation paths where feasible.
- Decide the `speak-with-profile` e2e test strategy, including whether to use a fake downstream CLI, real tool integration, or a bounded hybrid approach.
