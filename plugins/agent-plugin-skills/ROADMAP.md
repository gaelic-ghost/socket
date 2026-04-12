# Project Roadmap

## Vision

- Keep `agent-plugin-skills` as the focused home for maintainer skills that help skills-export and plugin-export repositories stay honest about packaging, discovery, and documentation boundaries.

## Product principles

- Keep the repository blunt about Codex's documented plugin-scoping limits.
- Keep maintainer workflows audit-first and bounded.
- Keep root `skills/` canonical and avoid reintroducing local installer machinery into this repo.

## Milestone Progress

- [ ] Milestone 4: docs visibility and wording hardening
- [ ] Milestone 5: skills repo migration and split support
- [ ] Milestone 6: upstream docs watch and change intake
- [ ] Milestone 7: `skill-evals`

## Milestone 4: docs visibility and wording hardening

Scope:

- Keep top-level docs and shipped skills abundantly clear about what this repo exports and what Codex still cannot scope properly.

Tickets:

- [ ] Audit exported skills for wording that softens OpenAI's Codex scoping limits.
- [ ] Keep global-install guidance ahead of local authoring notes.
- [ ] Keep repo-local discovery mirror guidance separate from install guidance.
- [ ] Add or refine troubleshooting language for confusing Codex plugin expectations.

Exit criteria:

- [ ] End users can quickly tell that this repo exports installable maintainer skills and does not provide a richer repo-private Codex plugin product.
- [ ] Limitation messaging is consistent across the shipped skill surface and repo docs.

## Milestone 5: skills repo migration and split support

Scope:

- Add a maintainer workflow for moving or re-homing skills between repositories while preserving docs and guidance.

Tickets:

- [ ] Define migration inputs and guardrails for moving one or more skills between repos.
- [ ] Add guidance for updating install examples, docs, and roadmap references after a move.
- [ ] Add deterministic validation for orphaned references and stale naming after migration.
- [ ] Decide whether subtree-managed superprojects such as `socket` should become an explicitly supported repo family here.

Exit criteria:

- [ ] Maintainers can move skills between repos without manual cross-surface cleanup.

## Milestone 6: upstream docs watch and change intake

Scope:

- Add durable process support for noticing changes in the Agent Skills standard, OpenAI docs, and Claude docs and turning those changes into actionable maintainer work.

Tickets:

- [ ] Define the upstream sources and canonical refresh cadence.
- [ ] Add a dated findings format for upstream changes that affect repo policy or docs.
- [ ] Decide whether this belongs inside `sync-skills-repo-guidance` or becomes a separate audit skill.

Exit criteria:

- [ ] Upstream ecosystem drift can be tracked deliberately instead of ad hoc.

## Milestone 7: `skill-evals`

Scope:

- Add a workflow for evaluating shipped skills against real agent runtimes such as Codex and Claude Code.

Tickets:

- [ ] Define the eval targets and supported runtimes.
- [ ] Define the eval artifact set, including prompts, expected behaviors, failure notes, and dated run summaries.
- [ ] Add deterministic guidance for comparing trigger activation, tool usage, and final output shape against the intended skill contract.
- [ ] Decide whether the workflow is audit-only, report-generating, or can also scaffold eval fixtures.

Exit criteria:

- [ ] Maintainers have one coherent workflow for evaluating a skill on real agent surfaces instead of relying only on static review.

## History

- Completed Milestones 0 through 3 by establishing the repository, shipping the foundational maintainer skills, and removing installer-era nested packaging guidance.
- Completed Milestone 8 by retiring the old `maintain-plugin-docs` surface and aligning the shipped inventory around the remaining maintainer workflows.
