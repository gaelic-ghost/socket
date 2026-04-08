# Project Roadmap

## Vision

- Build a focused maintainer toolkit for skills-export repositories.
- Keep the open Agent Skills standard as the portable core while fully adopting useful OpenAI Codex and Claude Code extensions.
- Keep this repository honest about the severe scoping limits in OpenAI's current Codex plugin system.

## Product Principles

- Root `skills/` stays canonical.
- This repository does not track a nested plugin directory for itself.
- This repository does not ship an installer skill.
- This repository does not ship an install-validation skill.
- Codex limitation wording stays blunt and explicit.
- POSIX discovery mirrors stay explicit and documented.
- Narrow file-level maintainers and broader repo-level maintainers should stay distinct.
- Upstream docs drift is expected and should be audited deliberately.
- Skill behavior on real agents should be evaluated deliberately instead of inferred from static docs alone.

## Milestone Progress

- [x] Milestone 0: Foundation bootstrap
- [x] Milestone 1: `maintain-plugin-docs` evolution
- [x] Milestone 2: remove nested plugin packaging and installer workflows
- [x] Milestone 3: `maintain-plugin-repo`
- [ ] Milestone 4: docs visibility and wording hardening
- [ ] Milestone 5: skills repo migration and split support
- [ ] Milestone 6: upstream docs watch and change intake
- [ ] Milestone 7: `skill-evals`

## Milestone 0: Foundation bootstrap

Scope:

- Create the dedicated `agent-plugin-skills` repository.
- Bootstrap a source-first skills-export layout with root `skills/` canonical.
- Seed the repo with the first maintainer skills.

Tickets:

- [x] Add the predecessor README-maintenance skill that evolved into `maintain-plugin-docs`.
- [x] Add `bootstrap-skills-plugin-repo`.
- [x] Add `sync-skills-repo-guidance`.
- [x] Add maintainer docs, repo-level discovery mirrors, and maintainer Python tooling.
- [x] Add tests.

Exit criteria:

- [x] The repository has a coherent maintainer-skills purpose.
- [x] Root `skills/` is canonical and local repo discovery paths use symlinks.
- [x] Active skills, docs, and source layout describe the same repo model.

## Milestone 1: `maintain-plugin-docs` evolution

Scope:

- Rename the current README-maintenance skill to `maintain-plugin-docs`.
- Re-scope it from narrow README maintenance into the docs maintainer for skills-export repositories.
- Combine README and ROADMAP maintenance in one bounded workflow.

Tickets:

- [x] Rename the skill surface from `maintain-skills-readme` to `maintain-plugin-docs`.
- [x] Add a `--doc-scope <readme|roadmap|all>` interface.
- [x] Keep the existing README maintenance path as the `readme` scope.
- [x] Implement a checklist-style `ROADMAP.md` validator and apply flow for the `roadmap` scope.
- [x] Add `all` scope behavior that runs README and ROADMAP audits together.
- [x] Add tests for README-only, ROADMAP-only, and combined `all` mode runs.

Exit criteria:

- [x] The docs-maintainer role for skills-export repos is clear.
- [x] The skill has an explicit non-overlapping boundary relative to repo-wide sync work.

## Milestone 2: remove nested plugin packaging and installer workflows

Scope:

- Remove nested plugin-package guidance from this repository.
- Remove installer and install-validation workflows from this exported skill set.
- Keep the repository blunt about the documented Codex limitation instead of normalizing around it.

Tickets:

- [x] Remove `install-plugin-to-socket` from the exported skill surface.
- [x] Remove `validate-plugin-install-surfaces` from the exported skill surface.
- [x] Remove nested plugin-directory and repo-marketplace guidance from repo docs and skills.
- [x] Keep the Codex limitation wording blunt and explicit in repo docs and exported skills.

Exit criteria:

- [x] The repository no longer ships installer or install-validation workflows.
- [x] The repository no longer teaches a nested plugin-directory model for itself.
- [x] Repo docs say plainly that proper plugin scoping is not something Codex currently supports.

## Milestone 3: `maintain-plugin-repo`

Scope:

- Add a repo-level maintainer orchestrator for skills-export repositories that feel drifted overall.
- Keep the skill audit-first and route to existing specialist owners instead of replacing them.

Tickets:

- [x] Define the repo-level role and boundaries relative to `maintain-plugin-docs` and the repo's own hard-limit policy.
- [x] Add a bounded `audit-only` workflow that returns one grouped report for repo-model findings, docs findings, deferred work, and owner assignments.
- [x] Add a bounded `apply-safe-fixes` workflow that routes docs maintenance through `maintain-plugin-docs`.
- [x] Document the output contract and owner-routing rules inside the skill runtime surface.
- [x] Add tests for clean runs, exact `No findings.` behavior, and apply-mode routing.

Exit criteria:

- [x] Maintainers have one bounded entrypoint for repo-level maintenance instead of manually coordinating multiple specialist skills.
- [x] The skill stays honest about what it coordinates versus what it directly fixes.

## Milestone 4: docs visibility and wording hardening

Scope:

- Keep top-level docs and skill docs abundantly clear about what this repo exports and what Codex cannot scope properly.

Tickets:

- [ ] Audit all exported skills for wording that softens OpenAI's Codex scoping limits.
- [ ] Keep global-install guidance ahead of local authoring notes.
- [ ] Keep repo-local discovery mirror guidance separate from install guidance.
- [ ] Add or refine troubleshooting language for confusing Codex plugin expectations.

Exit criteria:

- [ ] End users can tell quickly that this repo exports installable skills, not a nested repo-local plugin product.
- [ ] Limitation messaging is consistent across exported skills and top-level docs.

## Milestone 5: skills repo migration and split support

Scope:

- Add a skill for splitting, extracting, or re-homing skills between repositories while preserving docs and guidance.

Tickets:

- [ ] Define migration inputs and guardrails for moving one or more skills between repos.
- [ ] Add guidance for updating install examples, docs, and roadmap references after a move.
- [ ] Add deterministic validation for orphaned references and stale naming after migration.

Exit criteria:

- [ ] Maintainers can move skills between repos without manual cross-surface cleanup.

## Milestone 6: upstream docs watch and change intake

Scope:

- Add durable process support for noticing changes in the Agent Skills standard, OpenAI docs, and Claude docs and turning those changes into actionable repo maintenance.

Tickets:

- [ ] Define the upstream sources and canonical refresh cadence.
- [ ] Add a dated findings format for upstream changes that affect repo policy or docs.
- [ ] Decide whether this belongs inside `sync-skills-repo-guidance` or becomes a separate audit skill.

Exit criteria:

- [ ] Upstream ecosystem drift can be tracked deliberately instead of ad hoc.

## Milestone 7: `skill-evals`

Scope:

- Add a skill for evaluating and testing skills against real agent runtimes such as Codex and Claude Code.

Tickets:

- [ ] Define the eval targets and supported runtimes.
- [ ] Define the eval artifact set, including prompts, expected behaviors, failure notes, and dated run summaries.
- [ ] Add deterministic guidance for comparing trigger activation, tool usage, and final output shape against the intended skill contract.
- [ ] Decide whether this skill is audit-only, report-generating, or can also scaffold eval fixtures and cases.

Exit criteria:

- [ ] Maintainers can run one coherent workflow to evaluate a skill on real agent surfaces instead of relying only on static review.
- [ ] The repo has a durable place for testing trigger behavior and workflow fidelity across supported agents.
