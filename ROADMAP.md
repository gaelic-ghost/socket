# Project Roadmap

## Vision

- Build a focused maintainer toolkit for agent-skills and agent-plugin repositories.
- Keep the open Agent Skills standard as the portable core while fully adopting useful OpenAI Codex and Claude Code extensions.
- Make repo bootstrap, guidance sync, docs maintenance, local plugin install wiring, packaging validation, install-surface auditing, and skill evaluation first-class maintainable workflows.

## Product Principles

- Root `skills/` stays canonical.
- Packaging and discovery metadata stay under `plugins/` and `.agents/plugins/`.
- POSIX discovery mirrors are explicit, documented, and validated.
- Bundled plugin-root skills directories are explicit, documented, and kept in sync with root `skills/`.
- Narrow file-level maintainers and broader repo-level maintainers should stay distinct.
- Action-oriented local install wiring should stay distinct from audit-only metadata validation.
- Upstream docs drift is expected and should be audited deliberately.
- Skill behavior on real agents should be evaluated deliberately instead of inferred from static docs alone.

## Milestone Progress

- [x] Milestone 0: Foundation bootstrap
- [x] Milestone 1: `maintain-plugin-docs` evolution
- [ ] Milestone 2: `install-plugin-to-socket`
- [x] Milestone 3: install-surface and metadata validation skill
- [ ] Milestone 4: MCP and app packaging maintainer skill
- [ ] Milestone 5: skills repo migration and split support
- [ ] Milestone 6: upstream docs watch and change intake
- [ ] Milestone 7: `skill-evals`
- [ ] Milestone 8: customization systems guidance
- [ ] Milestone 9: end-user docs visibility

## Milestone 0: Foundation bootstrap

Scope:

- Create the dedicated `agent-plugin-skills` repository.
- Bootstrap plugin-first packaging with root `skills/` canonical.
- Seed the repo with the first three stack-specific maintainer skills.

Tickets:

- [x] Add the predecessor README-maintenance skill that now evolves into `maintain-plugin-docs`.
- [x] Add `bootstrap-skills-plugin-repo`.
- [x] Add `sync-skills-repo-guidance`.
- [x] Add plugin manifests, marketplace wiring, maintainer docs, repo-level discovery mirrors, and bundled plugin skills directories.
- [x] Add maintainer Python tooling baseline and tests.

Exit criteria:

- [x] The repository has a coherent stack-specific purpose.
- [x] Root `skills/` is canonical, repo-level discovery paths use symlinks, and plugin packaging keeps a bundled `skills/` directory.
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
- [x] Enforce canonical roadmap structure: `Vision`, `Product Principles`, `Milestone Progress`, and milestone sections with `Scope`, `Tickets`, and `Exit criteria`.
- [x] Validate that `Milestone Progress` reflects milestone-level reality.
- [x] Validate markdown checkbox syntax and deterministic milestone ordering.
- [x] Treat legacy roadmap formats as migration targets in apply mode and as reported findings in check-only mode.
- [x] Add `all` scope behavior that runs README and ROADMAP audits together in one pass.
- [x] Add cross-doc consistency checks between `README.md` and `ROADMAP.md` for current skill names, current-versus-planned scope wording, and install-surface priorities.
- [x] Add deterministic validation for README sections, docs links, install examples, and docs-adjacent maintainer snippets.
- [x] Rebalance README install guidance so Codex Plugin and Claude Code Plugin installs are primary and Vercel `skills` CLI installs are secondary.
- [x] Update the JSON and Markdown output contract to report `readme_findings`, `roadmap_findings`, and `cross_doc_findings`.
- [x] Update prompt templates and references so automation and subagents can target `readme`, `roadmap`, or `all`.
- [x] Add tests for README-only, ROADMAP-only, and combined `all` mode runs.
- [x] Add tests for cross-doc drift detection and install-surface ordering checks.
- [x] Document deferral boundaries relative to `sync-skills-repo-guidance`.

Exit criteria:

- [x] The docs-maintainer role for skills/plugin repos is clearer than README-only maintenance.
- [x] The skill has an explicit non-overlapping boundary relative to repo-wide sync work.

## Milestone 2: `install-plugin-to-socket`

Scope:

- Add a skill for wiring an in-development Codex plugin into a local Codex install surface at repo scope or personal scope.
- Keep the skill aligned to the documented OpenAI local-plugin flow: scope-local plugin directory plus marketplace wiring, followed by restart and verification guidance.
- Treat repo scope and personal scope as the primary supported targets:
  - repo scope: `$REPO_ROOT/plugins/<plugin-name>` plus `$REPO_ROOT/.agents/plugins/marketplace.json`
  - personal scope: `~/.codex/plugins/<plugin-name>` plus `~/.agents/plugins/marketplace.json`
- Keep plugin source inspection manifest-aware so the installer can infer the plugin name, version, category, and install-surface metadata from `.codex-plugin/plugin.json`.
- Avoid pretending to control undocumented Codex installed-state internals. In the current docs-supported model, the skill should make the plugin installable and discoverable locally, then guide restart and verification.

Tickets:

- [x] Define the user-facing contract around the phrase "install to socket" so the skill is explicit that it targets Codex local plugin discovery surfaces.
- [x] Add a deterministic source audit for:
  - `.codex-plugin/plugin.json`
  - plugin name and version
  - optional `skills/`, `.mcp.json`, `.app.json`, and `assets/`
- [x] Support repo-scoped install planning and apply behavior.
- [x] Support personal-scoped install planning and apply behavior.
- [x] Preserve and merge existing marketplace entries instead of overwriting marketplace catalogs wholesale.
- [x] Enforce documented `source.path` rules:
  - path stays relative to the marketplace root
  - path starts with `./`
  - path stays inside the chosen marketplace root
- [x] Default to docs-aligned local copy or sync behavior into the chosen scope-local plugin directory instead of inventing an unsupported direct-external-path install mode.
- [x] Add a bounded update path for updating an already wired local development plugin after source changes.
- [x] Add a bounded uninstall path that can remove the local plugin directory and marketplace entry for one plugin without disturbing others.
- [x] Add a persistent default install-scope preference with repo-profile and global-profile resolution before the built-in default.
- [x] Decide whether disable or enable behavior belongs in v1 through `~/.codex/config.toml`, or whether v1 should stay focused on marketplace wiring only.
- [x] Add optional config-state management for Codex plugin enable or disable behavior in `~/.codex/config.toml` once the repo wants that broader contract.
- [x] Make personal-scope `install` enable the plugin by default so a new global install is active after restart without requiring a separate `enable` pass.
- [x] Prefer Codex app-server `plugin/install` and `plugin/uninstall` RPCs for personal-scope cache sync when the local Codex build exposes them, while keeping staged-surface fallback behavior for older or missing app-server paths.
- [x] Add a verification-oriented mode that audits an already installed local plugin and reports marketplace drift, missing copied files, and likely restart state.
- [x] Extend personal-scope verification so it can report when Codex still sees the plugin as available but not installed in its own local cache.
- [x] Add a bounded repair workflow that can normalize a drifted install surface in one pass, including the common legacy repo-root plugin case where a repo-local marketplace entry still points at `./`.
- [ ] Add a safer overwrite policy for personal-scope updates so maintainers can choose between replace, backup-then-replace, or fail-on-existing behavior.
- [x] Document install, update, and uninstall usage examples so update and remove workflows are explicit in repo guidance.
- [x] Add support for promoting a plugin from repo-local scope into personal scope in one bounded workflow without forcing the maintainer to rerun separate install and uninstall flows manually.
- [x] Add richer manifest-aware checks for optional plugin surfaces such as `.mcp.json`, `.app.json`, hooks, and install-surface assets before copying them into place.
- [x] Return a structured report with:
  - `run_context`
  - `scope`
  - `source_plugin`
  - `target_plugin_root`
  - `marketplace_path`
  - `findings`
  - `apply_actions`
  - `restart_required`
  - `verification_steps`
  - `errors`
- [x] Add tests for repo scope, personal scope, update, uninstall, and marketplace merge behavior.

Exit criteria:

- [x] Maintainers can wire an in-development Codex plugin into repo or personal scope without hand-editing marketplace JSON.
- [x] The skill stays honest about the documented local-plugin contract and does not claim unsupported cache or installed-state control.
- [ ] The workflow reduces the repetitive manual loop of copying plugin files, updating marketplace metadata, restarting Codex, and checking discovery paths.

## Milestone 3: install-surface and metadata validation skill

Scope:

- Add a skill for auditing skill frontmatter, `agents/openai.yaml`, plugin manifests, marketplace metadata, discovery mirrors, and install examples together.
- Keep `validate-plugin-install-surfaces` explicitly represented in the roadmap so the active skill inventory and milestone plan stay aligned.

Tickets:

- [x] Define the validation surface across the Agent Skills standard plus OpenAI and Claude overlays.
- [x] Add deterministic checks for missing or stale metadata fields.
- [x] Add install-command and discovery-path validation.
- [x] Decide whether this skill should mutate or remain audit-only.

Exit criteria:

- [x] Maintainers can run one bounded workflow to detect install-surface drift.
- [x] The audit distinguishes canonical authored surfaces from packaging mirrors.

## Milestone 4: MCP and app packaging maintainer skill

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

## Milestone 5: skills repo migration and split support

Scope:

- Add a skill for splitting, extracting, or re-homing skills between repositories while preserving docs, packaging, and install guidance.

Tickets:

- [ ] Define migration inputs and guardrails for moving one or more skills between repos.
- [ ] Add guidance for updating install examples, plugin manifests, and roadmap references after a move.
- [ ] Add deterministic validation for orphaned references and stale naming after migration.

Exit criteria:

- [ ] Maintainers can move skills between repos without manual cross-surface cleanup.

## Milestone 6: upstream docs watch and change intake

Scope:

- Add durable process support for noticing changes in the Agent Skills standard, OpenAI docs, and Claude docs and turning those changes into actionable repo maintenance.
- Keep `sync-skills-repo-guidance` focused on guidance alignment unless a stronger case emerges for folding upstream-doc intake directly into that skill.

Tickets:

- [ ] Define the upstream sources and the canonical refresh cadence.
- [ ] Add a dated findings format for upstream changes that affect repo policy or packaging.
- [ ] Decide whether this belongs inside `sync-skills-repo-guidance` or becomes a separate audit skill.

Exit criteria:

- [ ] Upstream ecosystem drift can be tracked deliberately instead of ad hoc.

## Milestone 7: `skill-evals`

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

## Milestone 8: customization systems guidance

Scope:

- Add durable maintainer guidance for how skills in this repo should expose persistent customization without inventing one-off config surfaces each time.
- Standardize repo-profile and global-profile conventions where they make sense for maintainer workflows in this repository.
- Make it easier to tell which skills should adopt persistent customization, which should stay argument-only, and how those decisions should be documented.

Tickets:

- [ ] Define the canonical customization guidance for this repo family, including repo-profile and global-profile path conventions.
- [ ] Document when a skill should add persistent customization versus keeping defaults inline and CLI-only.
- [ ] Add shared guidance for documenting config schema, precedence order, and example customization files in relevant skills here.
- [ ] Audit the relevant existing skills in this repo and note which ones should adopt or explicitly avoid persistent customization.

Exit criteria:

- [ ] Maintainers have one documented customization pattern to follow instead of ad hoc per-skill config behavior.
- [ ] Relevant skills in this repo can converge on the same customization vocabulary, path layout, and documentation shape.

## Milestone 9: end-user docs visibility

Scope:

- Improve how end users of this plugin discover the right docs and install path without having to read maintainer-oriented repo internals first.
- Make Codex and Claude install and sharing guidance easier to find from top-level repo surfaces.
- Clarify what belongs in git, what is local-only runtime state, and which workflow owns each install or sharing step.

Tickets:

- [ ] Add clearer end-user doc entrypoints for Codex local plugins, Claude `--plugin-dir` development, and Claude marketplace sharing.
- [ ] Audit whether install, update, uninstall, enable, disable, verify, and promote workflows are discoverable from user-facing docs rather than only maintainer references.
- [ ] Add or refine doc cross-links so users can move cleanly between plugin install guidance, marketplace guidance, and skill-specific workflows.
- [ ] Check whether plugin README examples and metadata surfaces surface the right docs for users before maintainers.
- [ ] Add troubleshooting guidance for Codex marketplace reload behavior, skipped-marketplace log warnings, repo-versus-personal scope confusion, and non-intuitive `/plugins` ordering.

Exit criteria:

- [ ] End users can find the right install and sharing path quickly without reading maintainer-only documentation first.
