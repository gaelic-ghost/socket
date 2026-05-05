---
name: sync-skills-repo-guidance
description: Audit guidance across README.md, AGENTS.md, maintainer docs, and discovery mirrors in an existing skills-export repository. Use when a skills repo may have stale guidance, missing discovery mirrors, or outdated references to the Agent Skills standard or OpenAI Codex docs. Defer narrow README-only or roadmap-only requests to the specialized maintainer skills.
---

# Sync Skills Repo Guidance

Audit an existing skills-export repository against the current house guidance and upstream standards.

## Codex Model Note

When syncing Codex guidance, state clearly that OpenAI's documented Codex plugin system exposes repo-visible plugins through marketplace catalogs and does not document a richer repo-private scoping model beyond that.

## Codex Plugin Root Structure

When this skill touches Codex packaging guidance, keep the plugin-root structure aligned with the current OpenAI docs:

- every plugin has a manifest at `.codex-plugin/plugin.json`
- only `plugin.json` belongs in `.codex-plugin/`
- `skills/`, `.app.json`, `.mcp.json`, and `assets/` belong at the plugin root
- plugin manifests should point to bundled skill folders with `"skills": "./skills/"`
- marketplace entries point `source.path` at the plugin root directory, not at `.codex-plugin/`

## Codex Install-Surface Map

When this skill touches Codex plugin guidance, keep these surfaces distinct instead of collapsing them into one vague "plugin install" concept:

- tracked marketplace source
  - preferred user path: `codex plugin marketplace add <owner>/<repo>`
  - update path: `codex plugin marketplace upgrade <marketplace-name>`
  - purpose: let Codex clone, track, and refresh a marketplace from Git instead of asking users to copy plugin payload directories by hand
- marketplace catalog
  - personal: `~/.agents/plugins/marketplace.json`
  - repo: `$REPO_ROOT/.agents/plugins/marketplace.json`
  - purpose: catalog that Codex can read from; plugin entries point at plugin roots inside the marketplace source
- plugin root payload
  - common personal pattern: `~/.codex/plugins/<plugin-name>`
  - common repo pattern from the docs: `$REPO_ROOT/plugins/<plugin-name>`
  - Git-backed marketplace pattern: a plugin root inside the tracked marketplace checkout, often the repo root for standalone plugins or `plugins/<plugin-name>` for `socket`
  - purpose: plugin root payload directory that the marketplace entry points at
- installed plugin cache
  - `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`
  - purpose: Codex's installed copy; for local plugins the documented version token is `local`
- enabled-state config
  - documented plugin path: `~/.codex/config.toml`
  - purpose: per-plugin on or off state keyed by plugin name plus marketplace name, for example `[plugins."my-plugin@local-repo"]`

Default user-facing install and update guidance to the official Git-backed marketplace commands. Use explicit refs such as `<owner>/<repo>@vX.Y.Z` only for pinned reproducible installs. Use manual local marketplace or copied-payload instructions only for local development, testing unpublished changes, or fallback cases where the Git-backed path is not available.

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

When auditing target skills or plugin-repo docs that mention OpenAI Codex Hooks, keep hooks separate from plugin packaging and discovery mirrors. Hooks are Codex runtime lifecycle scripts, not a plugin install surface.

Flag hooks guidance that omits `features.codex_hooks = true`, implies project-local hooks load without a trusted `.codex/` layer, treats `PreToolUse` or `PostToolUse` as complete enforcement for every tool path, or confuses Codex Hooks with git pre-commit hooks or repo-maintenance hook scripts.
