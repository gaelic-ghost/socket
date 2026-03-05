# Project Roadmap

## Vision

Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, and lightweight composition for installation and routing.

## Product principles

- Keep skill names clear, stable, and domain-grouped.
- Keep workflow instructions deterministic and safety-forward.
- Keep docs and metadata synchronized with the active skill set.

## Milestone Progress

- [x] Milestone 0: Naming and structural refactor (completed)
- [x] Milestone 1: Docs skill consolidation and orchestrator addition (completed)
- [ ] Milestone 2: Validation hardening and snippet adoption (in progress)

## Milestone 0: Naming and structural refactor

Scope:

- Rename skills to the current domain-grouped naming standard.
- Remove deprecated skill directories from active inventory.

Tickets:

- [x] Rename roadmap skill to `project-roadmap-maintainer`.
- [x] Rename workspace cleanup skill to `project-workspace-cleaner`.
- [x] Rename Things reminder skill to `things-reminders-manager`.
- [x] Rename Things digest skill to `things-digest-generator`.

Exit criteria:

- [x] Active skill folder names and frontmatter names match.
- [x] Deprecated names are absent from active invocation references.

## Milestone 1: Docs consolidation and orchestration

Scope:

- Consolidate docs maintenance skills into a single maintained entrypoint.
- Add a front-door orchestrator skill for routing and install guidance.

Tickets:

- [x] Merge prior docs-maintenance skills into `project-docs-maintainer`.
- [x] Preserve both audit modes in the merged docs skill.
- [x] Add `project-skills-orchestrator-agent` with deterministic response sections.

Exit criteria:

- [x] Docs maintenance behavior remains available via explicit modes.
- [x] Orchestrator emits exact install commands and never auto-installs.

## Milestone 2: Validation hardening and snippet adoption

Scope:

- Validate metadata and reference consistency after refactor.
- Promote reusable AGENTS standards snippets for end users.

Tickets:

- [ ] Run stale-name sweeps and reference-integrity checks.
- [ ] Validate each skill `agents/openai.yaml` against current SKILL intent.
- [ ] Socialize `docs/agents-standards-snippets.md` for copy/paste adoption.

Exit criteria:

- [ ] No stale skill names remain outside migration docs.
- [ ] Shared passive standards are documented and reusable.

## Risks and mitigations

- Risk: Users still invoke deprecated names.
  Mitigation: keep migration table in README and clear install examples.
- Risk: Consolidated docs skill loses specificity.
  Mitigation: enforce explicit mode selection in `project-docs-maintainer`.

## Backlog candidates

- Add lightweight validation tooling for SKILL/frontmatter/openai.yaml alignment.
- Add orchestrator examples for multi-skill composition workflows.
