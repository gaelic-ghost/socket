# Project Roadmap

## Vision

- Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, plugin-ready packaging, and direct standalone install surfaces.

## Product principles

- Keep this repository focused on broadly reusable baseline workflows.
- Keep document-maintenance skills separate by document type.
- Keep plugin packaging thin and secondary to the shared `skills/` authored surface.

## Milestone Progress

- [ ] Milestone 14: Claude Code optimization pass
- [ ] Milestone 22: Accessibility maintenance baseline

## Milestone 14: Claude Code optimization pass

Scope:

- Improve this repository's skill surfaces for Claude Code routing and ergonomics.
- Reconcile wording, references, and metadata where Claude-specific behavior benefits from tighter optimization.
- Keep Claude-facing improvements additive to the shared standards-based skill core and the existing Codex and OpenAI overlays.

Tickets:

- [ ] Audit skill trigger wording and references for Claude Code activation quality.
- [ ] Add or refine Claude-facing guidance where Codex-first wording currently leaves avoidable ambiguity.
- [ ] Review metadata and examples for Claude Code compatibility and discoverability.

Exit criteria:

- [ ] Active skills have Claude Code-aware trigger and usage guidance where it materially improves routing.
- [ ] Claude-facing docs no longer lag behind the current skill layout and plugin-ready repo model.

## Milestone 22: Accessibility maintenance baseline

Scope:

- Add a new `maintain-project-accessibility` baseline skill for canonical `ACCESSIBILITY.md` maintenance.
- Define `ACCESSIBILITY.md` as the repo-local accessibility control document for standards, architecture, verification, ownership, and known gaps.
- Extend `maintain-project-contributing` so accessibility expectations become part of the contributor contract instead of optional follow-up guidance.

Tickets:

- [ ] Draft and ship the `maintain-project-accessibility` skill surface with template, config, script, references, and tests.
- [ ] Define and validate the canonical `ACCESSIBILITY.md` schema, including standards baseline, architecture, workflow, known gaps, and evidence sections.
- [ ] Add claim-integrity checks so the baseline workflow does not overstate compliance or invent unsupported accessibility evidence.
- [ ] Extend `maintain-project-contributing` with a required `Accessibility Expectations` subsection under `Development Expectations`.
- [ ] Update repo-level maintainer docs and active-skill inventory once the new skill is implemented.

Exit criteria:

- [ ] The repository ships a working `maintain-project-accessibility` skill with deterministic `check-only` and bounded `apply` behavior.
- [ ] The canonical `ACCESSIBILITY.md` contract is documented, test-covered, and grounded in the baseline maintainers' workflow family.
- [ ] `maintain-project-contributing` enforces contributor-facing accessibility expectations that point back to `ACCESSIBILITY.md`.

## Backlog Candidates

- [ ] Add lightweight validation tooling for `SKILL.md`, frontmatter, and `agents/openai.yaml` alignment.
- [ ] Add validation checks for README layout and active skill inventory consistency.

## History

- Completed Milestones 0 through 11 by refactoring the naming and structure, splitting README and roadmap maintenance into dedicated skills, restoring `explain-code-slice`, and aligning the repository around the current plugin-ready packaging model.
- Completed Milestones 12 and 13 by moving the agent-stack maintainer bootstrap and guidance-sync workflows into `agent-plugin-skills`.
- Completed Milestones 15 through 21 by adding Claude plugin support, shipping `maintain-project-repo`, `maintain-project-contributing`, and `maintain-project-agents`, and clarifying the repository's role as the general-purpose productivity baseline layer.
