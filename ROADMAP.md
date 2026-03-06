# Project Roadmap

## Vision

Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, direct standalone install surfaces, and cross-cutting speech output where audio delivery improves productivity.

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

## Risks and mitigations

- Risk: Users still invoke deprecated names.
  Mitigation: keep canonical usage guidance explicit in repo docs and skill prompts.
- Risk: Consolidated docs skill loses specificity.
  Mitigation: enforce explicit mode selection in `project-docs-maintainer`.

## Backlog candidates

- Add lightweight validation tooling for SKILL/frontmatter/openai.yaml alignment.
- Add validation checks for README layout and skill inventory consistency.
