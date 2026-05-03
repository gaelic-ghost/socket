# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 14: Claude Code optimization pass](#milestone-14-claude-code-optimization-pass)
- [Milestone 22: Accessibility maintenance baseline](#milestone-22-accessibility-maintenance-baseline)
- [Milestone 23: Security and support maintenance baseline](#milestone-23-security-and-support-maintenance-baseline)
- [Milestone 24: API maintenance baseline](#milestone-24-api-maintenance-baseline)
- [Milestone 25: Codex Hooks maintenance baseline](#milestone-25-codex-hooks-maintenance-baseline)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, plugin-ready packaging, and direct standalone install surfaces.

## Product Principles

- Keep this repository focused on broadly reusable baseline workflows.
- Keep document-maintenance skills separate by document type.
- Keep plugin packaging thin and secondary to the shared `skills/` authored surface.

## Milestone Progress

- Milestone 14: Claude Code optimization pass - Planned
- Milestone 22: Accessibility maintenance baseline - Planned
- Milestone 23: Security and support maintenance baseline - Planned
- Milestone 24: API maintenance baseline - Completed
- Milestone 25: Codex Hooks maintenance baseline - Planned

## Milestone 14: Claude Code optimization pass

### Status

Planned

### Scope

- [ ] Improve this repository's skill surfaces for Claude Code routing and ergonomics.
- [ ] Reconcile wording, references, and metadata where Claude-specific behavior benefits from tighter optimization.
- [ ] Keep Claude-facing improvements additive to the shared standards-based skill core and the existing Codex and OpenAI overlays.

### Tickets

- [ ] Audit skill trigger wording and references for Claude Code activation quality.
- [ ] Add or refine Claude-facing guidance where Codex-first wording currently leaves avoidable ambiguity.
- [ ] Review metadata and examples for Claude Code compatibility and discoverability.

### Exit Criteria

- [ ] Active skills have Claude Code-aware trigger and usage guidance where it materially improves routing.
- [ ] Claude-facing docs no longer lag behind the current skill layout and plugin-ready repo model.

## Milestone 22: Accessibility maintenance baseline

### Status

Planned

### Scope

- [ ] Add a new `maintain-project-accessibility` baseline skill for canonical `ACCESSIBILITY.md` maintenance.
- [ ] Define `ACCESSIBILITY.md` as the repo-local accessibility control document for standards, architecture, verification, ownership, and known gaps.
- [ ] Extend `maintain-project-contributing` so accessibility expectations become part of the contributor contract instead of optional follow-up guidance.

### Tickets

- [ ] Draft and ship the `maintain-project-accessibility` skill surface with template, config, script, references, and tests.
- [ ] Define and validate the canonical `ACCESSIBILITY.md` schema, including standards baseline, architecture, workflow, known gaps, and evidence sections.
- [ ] Add claim-integrity checks so the baseline workflow does not overstate compliance or invent unsupported accessibility evidence.
- [ ] Extend `maintain-project-contributing` with a required `Accessibility Expectations` subsection under `Development Expectations`.
- [ ] Update repo-level maintainer docs and active-skill inventory once the new skill is implemented.

### Exit Criteria

- [ ] The repository ships a working `maintain-project-accessibility` skill with deterministic `check-only` and bounded `apply` behavior.
- [ ] The canonical `ACCESSIBILITY.md` contract is documented, test-covered, and grounded in the baseline maintainers' workflow family.
- [ ] `maintain-project-contributing` enforces contributor-facing accessibility expectations that point back to `ACCESSIBILITY.md`.

## Milestone 23: Security and support maintenance baseline

### Status

Planned

### Scope

- [ ] Add a new `maintain-project-security` baseline skill for canonical `SECURITY.md` maintenance.
- [ ] Add a new `maintain-project-support` baseline skill for canonical `SUPPORT.md` maintenance.
- [ ] Keep both skills aligned with the existing docs-maintenance family so security reporting, support boundaries, and escalation paths can be maintained with the same deterministic `check-only` and bounded `apply` workflow model.

### Tickets

- [ ] Draft and ship the `maintain-project-security` skill surface with template, config, script, references, and tests.
- [ ] Define and validate the canonical `SECURITY.md` schema, including reporting path, intake expectations, disclosure language, scope boundaries, and verification evidence rules.
- [ ] Add claim-integrity checks so the security workflow does not invent vulnerability-handling guarantees, response timelines, or private-reporting channels that are not grounded in the target repo.
- [ ] Draft and ship the `maintain-project-support` skill surface with template, config, script, references, and tests.
- [ ] Define and validate the canonical `SUPPORT.md` schema, including supported surfaces, support boundaries, contact paths, triage expectations, and unsupported-request language.
- [ ] Add claim-integrity checks so the support workflow does not invent staffing promises, service-level expectations, or support channels that are not grounded in the target repo.
- [ ] Update repo-level maintainer docs and active-skill inventory once the new skills are implemented.

### Exit Criteria

- [ ] The repository ships a working `maintain-project-security` skill with deterministic `check-only` and bounded `apply` behavior.
- [ ] The repository ships a working `maintain-project-support` skill with deterministic `check-only` and bounded `apply` behavior.
- [ ] The canonical `SECURITY.md` and `SUPPORT.md` contracts are documented, test-covered, and grounded in the baseline maintainers' workflow family.

## Milestone 24: API maintenance baseline

### Status

Completed

### Scope

- [x] Add a new `maintain-project-api` baseline skill for canonical `API.md` maintenance.
- [x] Define `API.md` as the repo-local API contract document for surface area, access, request and response shapes, errors, compatibility, local verification, and ownership.
- [x] Keep the skill aligned with the existing docs-maintenance family so API references can be audited and normalized with deterministic `check-only` and bounded `apply` workflow modes.

### Tickets

- [x] Draft and ship the `maintain-project-api` skill surface with template, config, script, references, and tests.
- [x] Define and validate the canonical `API.md` schema, including surface, auth, schemas, errors, versioning, verification, and support ownership sections.
- [x] Add claim-integrity guardrails so the workflow does not invent endpoints, schemas, credentials, permissions, version guarantees, or support paths.
- [x] Update repo-level maintainer docs and active-skill inventory once the new skill is implemented.

### Exit Criteria

- [x] The repository ships a working `maintain-project-api` skill with deterministic `check-only` and bounded `apply` behavior.
- [x] The canonical `API.md` contract is documented, test-covered, and grounded in the baseline maintainers' workflow family.

Completed Milestone 24 by adding `maintain-project-api` as a template-backed `API.md` maintenance workflow with check/apply modes, schema references, OpenAI metadata, and regression coverage for clean missing-file creation.

## Milestone 25: Codex Hooks maintenance baseline

### Status

Planned

### Scope

- [ ] Add a future `maintain-project-hooks` baseline skill for auditing and documenting OpenAI Codex Hooks in repositories that intentionally use `.codex/hooks.json` or inline `[hooks]` config.
- [ ] Keep hooks guidance distinct from `AGENTS.md`, approval policy, tests, git hooks, and repo-maintenance hook scripts.
- [ ] Ground hook wording in the official OpenAI Codex Hooks guide, including the `features.codex_hooks` flag, trusted project-local `.codex/` loading, supported events, matcher behavior, and known guardrail limits.

### Tickets

- [ ] Define the canonical hook audit inputs, including project root, `.codex/hooks.json`, `.codex/config.toml`, user-level references, and managed-environment notes.
- [ ] Define a hooks documentation schema that records event, matcher, script path, timeout, status message, expected effect, and safety boundary for each hook.
- [ ] Add checks that flag missing feature flags, relative repo-local script paths, untrusted-project assumptions, unsupported event claims, and confusion between Codex Hooks and git hooks.
- [ ] Decide whether the first version is audit-only or can also scaffold a minimal hooks reference document.

### Exit Criteria

- [ ] Maintainers have one coherent workflow for checking Codex Hooks guidance without folding runtime hooks into ordinary AGENTS, validation, or repo-maintenance scripts.
- [ ] Repositories that use Codex Hooks can document what each hook does, when it fires, and what it can and cannot enforce.

## Backlog Candidates

- [ ] Add lightweight validation tooling for `SKILL.md`, frontmatter, and `agents/openai.yaml` alignment.
- [ ] Add validation checks for README layout and active skill inventory consistency.

## History

- Added `maintain-project-architecture` as the baseline `docs/architecture/ARCHITECTURE.md`, `SLICES.md`, and `architecture.json` maintenance skill, with first-pass SwiftPM product/target detection and stale model checks.
- Added first-pass OpenAI Codex Hooks guidance for AGENTS and repo-maintenance workflows, plus a planned `maintain-project-hooks` baseline skill for future deterministic hook audits.
- Added maintainer guidance for optional Codex subagent use in documentation, maintenance, and explanation skills, keeping delegation explicitly user-triggered and read-heavy by default.
- Fixed `maintain-project-repo` standard release handling so new release PRs wait for initial GitHub checks before watching CI, approval-only reviews no longer count as unresolved review comments, and release tags are created only after CI and the review-comment gate pass.
- Added `maintain-project-api` as the baseline `API.md` maintenance skill for API surface, access, schema, error, compatibility, verification, and support ownership docs.
- Clarified that the managed repo-maintenance workflow exposes `validate` as the branch-protection check context, avoiding blocked PRs caused by requiring the workflow-title display string instead.
- Completed Milestones 0 through 11 by refactoring the naming and structure, splitting README and roadmap maintenance into dedicated skills, restoring `explain-code-slice`, and aligning the repository around the current plugin-ready packaging model.
- Completed Milestones 12 and 13 by moving the agent-stack maintainer bootstrap and guidance-sync workflows into `agent-plugin-skills`.
- Completed Milestones 15 through 21 by adding Claude plugin support, shipping `maintain-project-repo`, `maintain-project-contributing`, and `maintain-project-agents`, and clarifying the repository's role as the general-purpose productivity baseline layer.
