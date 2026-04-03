# Project Roadmap

## Vision

- Build a focused maintainer toolkit for agent-skills and agent-plugin repositories.
- Keep the open Agent Skills standard as the portable core while fully adopting useful OpenAI Codex and Claude Code extensions.
- Make repo bootstrap, guidance sync, docs maintenance, packaging validation, and install-surface auditing first-class maintainable workflows.

## Product Principles

- Root `skills/` stays canonical.
- Packaging and discovery metadata stay under `plugins/` and `.agents/plugins/`.
- POSIX symlink mirrors are explicit, documented, and validated.
- Narrow file-level maintainers and broader repo-level maintainers should stay distinct.
- Upstream docs drift is expected and should be audited deliberately.

## Milestone Progress

- [x] Milestone 0: Foundation bootstrap
- [ ] Milestone 1: `maintain-skills-readme` evolution
- [ ] Milestone 2: install-surface and metadata validation skill
- [ ] Milestone 3: MCP and app packaging maintainer skill
- [ ] Milestone 4: skills repo migration and split support
- [ ] Milestone 5: upstream docs watch and change intake

## Milestone 0: Foundation bootstrap

Scope:

- Create the dedicated `agent-plugin-skills` repository.
- Bootstrap plugin-first packaging with root `skills/` canonical.
- Seed the repo with the first three stack-specific maintainer skills.

Tickets:

- [x] Add `maintain-skills-readme`.
- [x] Add `bootstrap-skills-plugin-repo`.
- [x] Add `sync-skills-repo-guidance`.
- [x] Add plugin manifests, marketplace wiring, maintainer docs, and POSIX symlink mirrors.
- [x] Add maintainer Python tooling baseline and tests.

Exit criteria:

- [x] The repository has a coherent stack-specific purpose.
- [x] Root `skills/` is canonical and mirrored into project-level discovery paths with symlinks.
- [x] Active skills, docs, and packaging metadata describe the same repo model.

## Milestone 1: `maintain-skills-readme` evolution

Scope:

- Re-scope `maintain-skills-readme` from a narrow README maintainer into a skills-repo docs maintainer with clearer stack-specific boundaries.
- Preserve explicit deferral to repo-wide sync and bootstrap workflows.

Tickets:

- [ ] Define the widened scope and new trigger surface for skills-repo documentation maintenance.
- [ ] Decide whether the skill should rename or keep the current name as a compatibility surface.
- [ ] Add deterministic validation for README sections, docs links, install examples, and docs-adjacent maintainer snippets.
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

Tickets:

- [ ] Define the upstream sources and the canonical refresh cadence.
- [ ] Add a dated findings format for upstream changes that affect repo policy or packaging.
- [ ] Decide whether this belongs inside `sync-skills-repo-guidance` or becomes a separate audit skill.

Exit criteria:

- [ ] Upstream ecosystem drift can be tracked deliberately instead of ad hoc.
