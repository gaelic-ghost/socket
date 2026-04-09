---
name: sync-skills-repo-guidance
description: Audit guidance across README.md, AGENTS.md, maintainer docs, and discovery mirrors in an existing skills-export repository. Use when a skills repo may have stale guidance, missing discovery mirrors, or outdated references to the Agent Skills standard, OpenAI Codex docs, or Claude Code docs. Defer narrow README-only or roadmap-only requests to the specialized maintainer skills.
---

# Sync Skills Repo Guidance

Audit an existing skills-export repository against the current house guidance and upstream standards.

## Codex Limitation Warning

When syncing Codex guidance, warn explicitly that OpenAI's documented Codex plugin system does not provide proper repo-private plugin scoping.

## Codex Install-Surface Map

When this skill touches Codex plugin guidance, keep these surfaces distinct instead of collapsing them into one vague "plugin install" concept:

- marketplace catalog
  - personal: `~/.agents/plugins/marketplace.json`
  - repo: `$REPO_ROOT/.agents/plugins/marketplace.json`
  - purpose: catalog that Codex can read from; plugin entries point `source.path` at a staged plugin directory
- staged plugin directory
  - common personal pattern: `~/.codex/plugins/<plugin-name>`
  - common repo pattern from the docs: `$REPO_ROOT/plugins/<plugin-name>`
  - purpose: source payload the marketplace entry points at
- installed plugin cache
  - `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`
  - purpose: Codex's installed copy; for local plugins the documented version token is `local`
- enabled-state config
  - personal: `~/.codex/config.toml`
  - optional repo override: `$REPO_ROOT/.codex/config.toml`
  - purpose: per-plugin on or off state keyed by plugin name plus marketplace name, for example `[plugins."my-plugin@local-repo"]`

Do not describe `config.toml` as the place plugins install into. Do not describe a marketplace file as the install destination. Keep the wording explicit: marketplaces are catalogs, staged plugin directories are payload roots, the cache is Codex's installed copy, and `config.toml` stores enabled-state.
