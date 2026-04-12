# Project Roadmap

## Vision

- Maintain a focused set of reusable productivity skills with clear naming, deterministic workflows, plugin-ready packaging, and direct standalone install surfaces.

## Product principles

- Keep this repository focused on broadly reusable baseline workflows.
- Keep document-maintenance skills separate by document type.
- Keep plugin packaging thin and secondary to the shared `skills/` authored surface.

## Milestone Progress

- [ ] Milestone 14: Claude Code optimization pass

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

## Backlog Candidates

- [ ] Add lightweight validation tooling for `SKILL.md`, frontmatter, and `agents/openai.yaml` alignment.
- [ ] Add validation checks for README layout and active skill inventory consistency.

## History

- Completed Milestones 0 through 11 by refactoring the naming and structure, splitting README and roadmap maintenance into dedicated skills, restoring `explain-code-slice`, and aligning the repository around the current plugin-ready packaging model.
- Completed Milestones 12 and 13 by moving the agent-stack maintainer bootstrap and guidance-sync workflows into `agent-plugin-skills`.
- Completed Milestones 15 through 21 by adding Claude plugin support, shipping `maintain-project-repo`, `maintain-project-contributing`, and `maintain-project-agents`, and clarifying the repository's role as the general-purpose productivity baseline layer.
