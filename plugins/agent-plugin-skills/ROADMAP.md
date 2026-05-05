# Project Roadmap

Use this roadmap to track milestone-level delivery through checklist sections.

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 4: Docs Visibility And Wording Hardening](#milestone-4-docs-visibility-and-wording-hardening)
- [Milestone 5: Skills Repo Migration And Split Support](#milestone-5-skills-repo-migration-and-split-support)
- [Milestone 6: Upstream Docs Watch And Change Intake](#milestone-6-upstream-docs-watch-and-change-intake)
- [Milestone 7: Skill Evals](#milestone-7-skill-evals)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Keep `agent-plugin-skills` as the focused home for maintainer skills that help skills-export and plugin-export repositories stay honest about packaging, discovery, and documentation boundaries.

## Product Principles

- Keep the repository explicit about Codex's currently documented plugin model, install surfaces, and Git-backed marketplace update path.
- Keep maintainer workflows audit-first, bounded, and backed by small deterministic tests.
- Keep root `skills/` canonical and avoid reviving installer-era machinery inside this repo.

## Milestone Progress

- Milestone 4: docs visibility and wording hardening - In Progress
- Milestone 5: skills repo migration and split support - Planned
- Milestone 6: upstream docs watch and change intake - Planned
- Milestone 7: `skill-evals` - Planned

## Milestone 4: Docs Visibility And Wording Hardening

### Status

In Progress

### Scope

- [ ] Keep top-level docs and shipped skills abundantly clear about what this repo exports and what Codex's documented plugin model does and does not describe.

### Tickets

- [ ] Audit exported skills for wording that softens or blurs the current OpenAI Codex plugin guidance.
- [ ] Keep Git-backed user install and update guidance ahead of local authoring notes.
- [ ] Keep repo-local discovery mirror guidance separate from install guidance.
- [ ] Add or refine troubleshooting language for confusing Codex plugin expectations.
- [ ] Keep `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, and `ROADMAP.md` aligned on the same repo shape and maintainer split.

### Exit Criteria

- [ ] End users can quickly tell that this repo exports installable maintainer skills and does not provide a richer repo-private Codex plugin product.
- [ ] Plugin-boundary wording is consistent across the shipped skill surface and repo docs, including the preference for official marketplace add/upgrade commands.
- [ ] The core maintainer docs follow the current house templates without blurring their responsibilities.

## Milestone 5: Skills Repo Migration And Split Support

### Status

Planned

### Scope

- [ ] Add a maintainer workflow for moving or re-homing skills between repositories while preserving docs and guidance.

### Tickets

- [ ] Define migration inputs and guardrails for moving one or more skills between repos.
- [ ] Add guidance for updating install examples, docs, and roadmap references after a move.
- [ ] Add deterministic validation for orphaned references and stale naming after migration.
- [ ] Decide whether subtree-managed superprojects such as `socket` should become an explicitly supported repo family here.

### Exit Criteria

- [ ] Maintainers can move skills between repos without manual cross-surface cleanup.

## Milestone 6: Upstream Docs Watch And Change Intake

### Status

Planned

### Scope

- [ ] Add durable process support for noticing changes in the Agent Skills standard and OpenAI docs and turning those changes into actionable maintainer work.

### Tickets

- [ ] Define the upstream sources and canonical refresh cadence.
- [ ] Add a dated findings format for upstream changes that affect repo policy or docs.
- [ ] Decide whether this belongs inside `sync-skills-repo-guidance` or becomes a separate audit skill.

### Exit Criteria

- [ ] Upstream ecosystem drift can be tracked deliberately instead of ad hoc.

## Milestone 7: Skill Evals

### Status

Planned

### Scope

- [ ] Add a workflow for evaluating shipped skills against real Codex runtimes.

### Tickets

- [ ] Define the eval targets and supported runtimes.
- [ ] Define the eval artifact set, including prompts, expected behaviors, failure notes, and dated run summaries.
- [ ] Add deterministic guidance for comparing trigger activation, tool usage, and final output shape against the intended skill contract.
- [ ] Decide whether the workflow is audit-only, report-generating, or can also scaffold eval fixtures.

### Exit Criteria

- [ ] Maintainers have one coherent workflow for evaluating a skill on real agent surfaces instead of relying only on static review.

## Backlog Candidates

- [ ] No additional backlog candidates are recorded yet.

## History

- Added Codex Hooks audit guidance to keep skills-export and plugin-export repos from confusing runtime hooks with plugin packaging or discovery surfaces.
- Updated Codex plugin install-surface guidance so user-facing install and update examples default to Git-backed marketplace sources and official marketplace add/upgrade commands.
- Added maintainer guidance for auditing optional Codex subagent wording in skills-export and plugin-export repositories, using OpenAI's current `subagents` terminology and explicit-trigger rule.
- Initial roadmap scaffold established the repository and its first maintainer-skill milestones.
- Completed the foundational milestones that created the repository, shipped the first maintainer skills, and removed installer-era nested packaging guidance.
- Completed the later cleanup milestone that retired the old `maintain-plugin-docs` surface and aligned the shipped inventory around the remaining maintainer workflows.
