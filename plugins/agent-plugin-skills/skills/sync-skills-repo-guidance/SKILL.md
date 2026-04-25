---
name: sync-skills-repo-guidance
description: Audit guidance across README.md, AGENTS.md, maintainer docs, and discovery mirrors in an existing skills-export repository. Use when a skills repo may have stale guidance, missing discovery mirrors, or outdated references to the Agent Skills standard, OpenAI Codex docs, or Claude Code docs. Defer narrow README-only or roadmap-only requests to the specialized maintainer skills.
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

- marketplace catalog
  - personal: `~/.agents/plugins/marketplace.json`
  - repo: `$REPO_ROOT/.agents/plugins/marketplace.json`
  - purpose: catalog that Codex can read from; plugin entries point `source.path` at a staged plugin directory
- staged plugin directory
  - common personal pattern: `~/.codex/plugins/<plugin-name>`
  - common repo pattern from the docs: `$REPO_ROOT/plugins/<plugin-name>`
  - purpose: plugin root payload directory that the marketplace entry points at
- installed plugin cache
  - `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`
  - purpose: Codex's installed copy; for local plugins the documented version token is `local`
- enabled-state config
  - documented plugin path: `~/.codex/config.toml`
  - purpose: per-plugin on or off state keyed by plugin name plus marketplace name, for example `[plugins."my-plugin@local-repo"]`

Do not describe `config.toml` as the place plugins install into. Do not describe a marketplace file as the install destination. Keep the wording explicit: marketplaces are catalogs, staged plugin directories are payload roots, the cache is Codex's installed copy, and `config.toml` stores enabled-state.

If you mention project-scoped `.codex/config.toml`, label it as a general Codex config capability from the config reference rather than as part of the documented plugin install-surface map.
