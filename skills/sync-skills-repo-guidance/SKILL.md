---
name: sync-skills-repo-guidance
description: Audit guidance across AGENTS.md, optional README.md, maintainer docs, and discovery mirrors in an existing Agent Skills or Codex plugin repository. Use when a skills repo may have stale guidance, missing discovery mirrors, outdated OpenAI Codex policy, or unclear boundaries between portable skills and host-specific plugin surfaces. Defer narrow README-only, roadmap-only, or host-adapter design requests to the specialized maintainer skills.
metadata:
  hermes:
    category: agent-portability
    tags: [agent-skills, codex, plugin, guidance]
---

# Sync Skills Repo Guidance

Audit an existing Agent Skills or Codex plugin repository against the current house guidance and upstream standards.

This is the Codex and shared-skills guidance-sync workflow inside Agent Portability Skills. It should preserve the difference between portable Agent Skills and host-specific packaging such as Codex plugins, Xcode plug-ins, Zed extensions, OpenCode config, Claude Code settings, MCP declarations, hooks, apps, and custom agents.

## Codex Model Note

When syncing Codex guidance, state clearly that OpenAI's documented Codex plugin system exposes repo-visible plugins through marketplace catalogs and does not document a richer repo-private scoping model beyond that.

Before making policy claims about Codex Plugins, Skills, MCP, Hooks, marketplaces, or subagents, refresh the relevant OpenAI Codex docs. Keep this skill's local guidance focused on durable repo policy and remove copied upstream detail when the official docs already cover it clearly.

## Codex Plugin Root Structure

When this skill touches Codex packaging guidance, keep the plugin-root structure aligned with the current OpenAI docs:

- every plugin has a manifest at `.codex-plugin/plugin.json`
- only `plugin.json` belongs in `.codex-plugin/`
- `skills/`, `.app.json`, `.mcp.json`, `hooks/`, and `assets/` belong at the plugin root
- plugin manifests should point to bundled skill folders with `"skills": "./skills/"`
- plugin manifests may point to bundled lifecycle hooks with `"hooks": "./hooks/hooks.json"`; if hooks live at `./hooks/hooks.json`, Codex checks that default path automatically
- plugin-bundled hooks are non-managed hooks, so installing or enabling a plugin does not make those hooks trusted automatically
- marketplace entries point `source.path` at the plugin root directory, not at `.codex-plugin/`

## Codex Install Guidance

Default user-facing install and update guidance to the official Git-backed marketplace commands. Use explicit refs such as `<owner>/<repo>@vX.Y.Z` only for pinned reproducible installs. Use manual local marketplace or copied-payload instructions only for local development, testing unpublished changes, or fallback cases where the Git-backed path is not available.

Keep marketplace sources, marketplace catalogs, plugin payload directories, installed cache paths, and config-state distinct instead of collapsing them into one vague "plugin install" concept. Do not reproduce the full install-surface map unless the target repo truly needs a maintainer reference; link to the OpenAI docs for the full current details.

When a workflow depends on a companion skill or plugin, first route through the Codex harness surfaces that are already available in the current session. Name the current-session skill to use, such as `productivity-skills:maintain-project-repo`, before giving install advice. If the companion skill is missing from the session, tell the user to add or update the marketplace and install the plugin through Codex's plugin directory for future sessions; do not imply that editing `config.toml`, copying payload folders, or searching an arbitrary checkout is the standard way to make a skill callable from Codex.

For `socket`, prefer:

```bash
codex plugin marketplace add gaelic-ghost/socket
codex plugin marketplace upgrade socket
```

For standalone plugin repositories that carry their own repo marketplace, prefer the same pattern with that repository, for example:

```bash
codex plugin marketplace add gaelic-ghost/apple-dev-skills
codex plugin marketplace add gaelic-ghost/SpeakSwiftlyServer
```

Do not describe `config.toml` as the place plugins install into. Do not describe a marketplace file as the install destination. Keep the wording explicit: marketplace sources are tracked by Codex, marketplaces are catalogs, plugin roots are payload directories, the cache is Codex's installed copy, and `config.toml` stores enabled-state.

If you mention project-scoped `.codex/config.toml`, label it as a general Codex config capability from the config reference rather than as part of the documented plugin install-surface map.

## Dependency Provenance

When syncing `AGENTS.md`, include strict dependency guidance:

- shared project dependencies must resolve from GitHub repository URLs, package managers, package registries, or other real remote repositories
- committed dependency declarations, lockfiles, scripts, docs, examples, generated project files, and CI config must not point at machine-local paths
- machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly

## Codex Subagent Guidance

When the user explicitly requests subagents, `skills-repo-guidance-sync`, review-packet planning, or asks to keep working while broad skills-repo guidance discovery happens in parallel, use the `skills-repo-guidance-sync` custom-agent role for bounded read-heavy discovery before this skill applies guidance sync. When the target is the Socket superproject itself, consider Socket Steward's deterministic audits and proposal reports first so the repo-local maintainer agent stays tied into cross-Socket docs and marketplace maintenance.

Good `skills-repo-guidance-sync` jobs for this skill:

- inspect AGENTS, README, maintainer docs, discovery mirrors, and plugin metadata for drift
- compare plugin, skill, hook, marketplace, and subagent claims against current official Codex docs
- inventory stale install-surface wording, unsupported non-Codex surfaces, and machine-local dependency guidance
- return a review packet with proposed patch set, validation handoff, affected files, and blockers

Keep apply-mode edits in the main thread. The guidance sync worker may return proposed patch-set entries, but the main agent should review them with the user before saving, editing, or applying any edits.

When auditing target skills, treat subagent guidance as useful only when it is explicit, bounded, and tied to real parallel support work. Match OpenAI's current Codex wording:

- use `subagent` and `subagent workflow` rather than vague older `multi-agent` language
- say current Codex releases enable subagent workflows by default, but Codex only spawns subagents when there is an explicit trigger: the user asks for subagents or parallel agent work, or a narrower skill/plugin workflow instructs the agent to ask first and the user grants explicit permission
- mention built-in `default`, `worker`, and `explorer` agents only when agent configuration matters; avoid turning custom `.codex/agents/` setup into default skill boilerplate
- prefer subagents for read-heavy discovery, docs pulling, tests, triage, log analysis, and summarization
- ask workers for concise findings, evidence, links, or file references instead of raw intermediate output
- keep write-heavy apply work in the main thread unless the user explicitly requests parallel implementation with disjoint write scopes
- preserve plugin-specific guidance that is stricter about subagent use, such as Codex Security repository-wide scan workflows that ask for subagents because the file-pass review depends on parallel workers

Flag skill guidance that implies automatic delegation, recommends parallel writes without ownership boundaries, adds subagent advice to narrow single-file or sequential workflows, or suppresses narrower plugin guidance that explicitly calls for subagents.

## Codex Hooks Guidance

When auditing target skills or plugin-repo docs that mention OpenAI Codex Hooks, keep hooks conceptually separate from marketplace and install-surface guidance. Hooks are Codex runtime lifecycle scripts; plugins may bundle lifecycle config, but hooks are not themselves a plugin install surface.

Flag hooks guidance that uses deprecated `features.codex_hooks` wording instead of canonical `features.hooks`, refers to removed or legacy plugin-hook gates such as `features.plugin_hooks`, implies hooks are disabled by default, implies project-local hooks load without a trusted `.codex/` layer, treats `PreToolUse` or `PostToolUse` as complete enforcement for every tool path, omits non-managed hook trust review, or confuses Codex Hooks with git pre-commit hooks or repo-maintenance hook scripts.

## GitHub Repository Settings

When the target repository has a GitHub remote, include repository settings in
the sync audit and route the canonical baseline through
`productivity-skills:maintain-github-repository`. Report drift in repository
features, merge modes, Dependabot and security settings, private vulnerability
reporting, web commit sign-off, and branch protection.

Keep this audit read-only unless the user requested settings changes. Do not
infer visibility changes, do not require reviewers a single-maintainer repo
does not have, and do not block a documented maintainer direct-push workflow.
