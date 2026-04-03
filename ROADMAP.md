# Project Roadmap

## Vision

- Build a focused maintainer toolkit for agent-skills and agent-plugin repositories.
- Keep the open Agent Skills standard as the portable core while fully adopting useful OpenAI Codex and Claude Code extensions.
- Make repo bootstrap, guidance sync, docs maintenance, packaging validation, install-surface auditing, and skill evaluation first-class maintainable workflows.

## Product Principles

- Root `skills/` stays canonical.
- Packaging and discovery metadata stay under `plugins/` and `.agents/plugins/`.
- POSIX symlink mirrors are explicit, documented, and validated.
- Narrow file-level maintainers and broader repo-level maintainers should stay distinct.
- Upstream docs drift is expected and should be audited deliberately.
- Skill behavior on real agents should be evaluated deliberately instead of inferred from static docs alone.

## Milestone Progress

- [x] Milestone 0: Foundation bootstrap
- [ ] Milestone 1: `maintain-plugin-docs` evolution
- [ ] Milestone 2: install-surface and metadata validation skill
- [ ] Milestone 3: MCP and app packaging maintainer skill
- [ ] Milestone 4: skills repo migration and split support
- [ ] Milestone 5: upstream docs watch and change intake
- [ ] Milestone 6: `skill-evals`

## Milestone 0: Foundation bootstrap

Scope:

- Create the dedicated `agent-plugin-skills` repository.
- Bootstrap plugin-first packaging with root `skills/` canonical.
- Seed the repo with the first three stack-specific maintainer skills.

Tickets:

- [x] Add the predecessor README-maintenance skill that now evolves into `maintain-plugin-docs`.
- [x] Add `bootstrap-skills-plugin-repo`.
- [x] Add `sync-skills-repo-guidance`.
- [x] Add plugin manifests, marketplace wiring, maintainer docs, and POSIX symlink mirrors.
- [x] Add maintainer Python tooling baseline and tests.

Exit criteria:

- [x] The repository has a coherent stack-specific purpose.
- [x] Root `skills/` is canonical and mirrored into project-level discovery paths with symlinks.
- [x] Active skills, docs, and packaging metadata describe the same repo model.

## Milestone 1: `maintain-plugin-docs` evolution

Scope:

- Rename the current README-maintenance skill to `maintain-plugin-docs`.
- Re-scope it from a narrow README maintainer into the stack-specific, plugin-repo-local docs maintainer for agent-skills and agent-plugin development repositories.
- Combine the current specialized README maintenance behavior with the same checklist-style roadmap maintenance model used by `maintain-project-roadmap`.
- Preserve explicit deferral to repo-wide sync and bootstrap workflows.

Tickets:

- [x] Rename the skill surface from `maintain-skills-readme` to `maintain-plugin-docs`.
- [x] Clarify current README-only behavior versus planned wider docs-maintainer scope in repo docs.
- [x] Clarify that `sync-skills-repo-guidance` currently owns ongoing guidance alignment while wider docs-maintainer work is still planned.
- [x] Add a `--doc-scope <readme|roadmap|all>` interface to `maintain-plugin-docs`.
- [x] Keep the existing README maintenance path as the `readme` scope without changing its bounded-write guarantees.
- [x] Implement a checklist-style `ROADMAP.md` validator for the `roadmap` scope.
- [x] Implement bounded `ROADMAP.md` apply behavior for the `roadmap` scope, modeled on `maintain-project-roadmap`.
- [ ] Enforce canonical roadmap structure: `Vision`, `Product Principles`, `Milestone Progress`, and milestone sections with `Scope`, `Tickets`, and `Exit criteria`.
- [ ] Validate that `Milestone Progress` reflects milestone-level reality.
- [ ] Validate markdown checkbox syntax and deterministic milestone ordering.
- [ ] Treat legacy roadmap formats as migration targets in apply mode and as reported findings in check-only mode.
- [x] Add `all` scope behavior that runs README and ROADMAP audits together in one pass.
- [ ] Add cross-doc consistency checks between `README.md` and `ROADMAP.md` for current skill names, current-versus-planned scope wording, and install-surface priorities.
- [ ] Add deterministic validation for README sections, docs links, install examples, and docs-adjacent maintainer snippets.
- [ ] Rebalance README install guidance so Codex Plugin and Claude Code Plugin installs are primary and Vercel `skills` CLI installs are secondary.
- [x] Update the JSON and Markdown output contract to report `readme_findings`, `roadmap_findings`, and `cross_doc_findings`.
- [ ] Update prompt templates and references so automation and subagents can target `readme`, `roadmap`, or `all`.
- [x] Add tests for README-only, ROADMAP-only, and combined `all` mode runs.
- [ ] Add tests for cross-doc drift detection and install-surface ordering checks.
- [ ] Document deferral boundaries relative to `sync-skills-repo-guidance`.

Exit criteria:

- [ ] The docs-maintainer role for skills/plugin repos is clearer than README-only maintenance.
- [ ] The skill has an explicit non-overlapping boundary relative to repo-wide sync work.

## Milestone 2: install-surface and metadata validation skill

Scope:

- Add a skill for auditing skill frontmatter, `agents/openai.yaml`, plugin manifests, marketplace metadata, discovery mirrors, and install examples together.

Tickets:

- [ ] Define the validation surface across the Agent Skills standard plus OpenAI and Claude overlays.
- [ ] Add deterministic checks for missing or stale metadata fields.
- [ ] Add install-command and discovery-path validation.
- [ ] Decide whether this skill should mutate or remain audit-only.

Exit criteria:

- [ ] Maintainers can run one bounded workflow to detect install-surface drift.
- [ ] The audit distinguishes canonical authored surfaces from packaging mirrors.

## Milestone 3: MCP and app packaging maintainer skill

Scope:

- Add a skill for maintaining MCP packaging, `.app.json` or app metadata, hook config, and related plugin-side surfaces in agent-stack repos.

Tickets:

- [ ] Define the supported MCP and app packaging surfaces.
- [ ] Add guidance for when packaging data belongs in plugin metadata versus repo docs.
- [ ] Add deterministic validation for missing or stale MCP or app references.
- [ ] Document boundaries relative to bootstrap and repo-guidance sync.

Exit criteria:

- [ ] Maintainers have a dedicated workflow for plugin-side MCP and app packaging surfaces.
- [ ] The repo can evolve beyond skills-only packaging cleanly.

## Milestone 4: skills repo migration and split support

Scope:

- Add a skill for splitting, extracting, or re-homing skills between repositories while preserving docs, packaging, and install guidance.

Tickets:

- [ ] Define migration inputs and guardrails for moving one or more skills between repos.
- [ ] Add guidance for updating install examples, plugin manifests, and roadmap references after a move.
- [ ] Add deterministic validation for orphaned references and stale naming after migration.

Exit criteria:

- [ ] Maintainers can move skills between repos without manual cross-surface cleanup.

## Milestone 5: upstream docs watch and change intake

Scope:

- Add durable process support for noticing changes in the Agent Skills standard, OpenAI docs, and Claude docs and turning those changes into actionable repo maintenance.
- Keep `sync-skills-repo-guidance` focused on guidance alignment unless a stronger case emerges for folding upstream-doc intake directly into that skill.

Tickets:

- [ ] Define the upstream sources and the canonical refresh cadence.
- [ ] Add a dated findings format for upstream changes that affect repo policy or packaging.
- [ ] Decide whether this belongs inside `sync-skills-repo-guidance` or becomes a separate audit skill.

Exit criteria:

- [ ] Upstream ecosystem drift can be tracked deliberately instead of ad hoc.

## Milestone 6: `skill-evals`

Scope:

- Add a skill for evaluating and testing skills against real agent runtimes such as Codex and Claude Code.
- Make it easier to validate trigger quality, workflow fidelity, instruction clarity, and output contracts with reproducible eval runs instead of ad hoc spot checks.

Tickets:

- [ ] Define the eval targets and supported runtimes, including Codex and Claude Code.
- [ ] Define the eval artifact set, including prompts, expected behaviors, failure notes, and dated run summaries.
- [ ] Add deterministic guidance for comparing trigger activation, tool usage, and final output shape against the intended skill contract.
- [ ] Decide whether this skill is audit-only, report-generating, or can also scaffold eval fixtures and cases.
- [ ] Document how `skill-evals` composes with `$skill-creator`, `sync-skills-repo-guidance`, and future metadata-validation skills.

Exit criteria:

- [ ] Maintainers can run one coherent workflow to evaluate a skill on real agent surfaces instead of relying only on static review.
- [ ] The repo has a durable place for testing trigger behavior and workflow fidelity across supported agents.
