---
name: sync-skills-repo-guidance
description: Audit guidance across AGENTS.md, optional README.md, maintainer docs, and discovery mirrors in an existing skills-export repository. Use when a skills repo may have stale guidance, missing discovery mirrors, or outdated references to the Agent Skills standard or OpenAI Codex docs. Defer narrow README-only or roadmap-only requests to the specialized maintainer skills.
---

# Sync Skills Repo Guidance

Audit an existing skills-export repository against the current house guidance and upstream standards.

## Codex Model Note

When syncing Codex guidance, state clearly that OpenAI's documented Codex plugin system exposes repo-visible plugins through marketplace catalogs and does not document a richer repo-private scoping model beyond that.

Before making policy claims about Codex Plugins, Skills, MCP, Hooks, marketplaces, or subagents, refresh the relevant OpenAI Codex docs. Keep this skill's local guidance focused on durable repo policy and remove copied upstream detail when the official docs already cover it clearly.

## Codex Plugin Root Structure

When this skill touches Codex packaging guidance, keep the plugin-root structure aligned with the current OpenAI docs:

- every plugin has a manifest at `.codex-plugin/plugin.json`
- only `plugin.json` belongs in `.codex-plugin/`
- `skills/`, `.app.json`, `.mcp.json`, `hooks/`, and `assets/` belong at the plugin root
- plugin manifests should point to bundled skill folders with `"skills": "./skills/"`
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

When auditing target skills, treat subagent guidance as useful only when it is explicit, bounded, and tied to real parallel support work. Match OpenAI's current Codex wording:

- use `subagent` and `subagent workflow` rather than vague older `multi-agent` language
- say Codex only spawns subagents when the user explicitly asks for subagents or parallel agent work
- prefer subagents for read-heavy discovery, docs pulling, tests, triage, log analysis, and summarization
- ask workers for concise findings, evidence, links, or file references instead of raw intermediate output
- keep write-heavy apply work in the main thread unless the user explicitly requests parallel implementation with disjoint write scopes

Flag skill guidance that implies automatic delegation, recommends parallel writes without ownership boundaries, or adds subagent advice to narrow single-file or sequential workflows.

## Codex Hooks Guidance

When auditing target skills or plugin-repo docs that mention OpenAI Codex Hooks, keep hooks conceptually separate from marketplace and install-surface guidance. Hooks are Codex runtime lifecycle scripts; plugins may bundle lifecycle config, but hooks are not themselves a plugin install surface.

Flag hooks guidance that omits `features.codex_hooks = true`, implies project-local hooks load without a trusted `.codex/` layer, treats `PreToolUse` or `PostToolUse` as complete enforcement for every tool path, or confuses Codex Hooks with git pre-commit hooks or repo-maintenance hook scripts.
