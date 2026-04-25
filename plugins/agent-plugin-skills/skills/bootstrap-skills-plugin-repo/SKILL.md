---
name: bootstrap-skills-plugin-repo
description: Bootstrap or align a skills-export repository with root `skills/`, repo-local discovery mirrors, maintainer docs, and clear Codex plugin-boundary wording. Use when creating a new skills repo or structurally aligning an existing one. Do not use this for narrow README-only or roadmap-only maintenance.
---

# Bootstrap Skills Plugin Repo

Bootstrap or align a skills-export repository.

## Codex Model Note

State plainly that OpenAI's documented Codex plugin system exposes repo-visible plugins through marketplace catalogs and does not document a richer repo-private scoping model beyond that. This repository pattern allows root `.codex-plugin` packaging, but it does not normalize nested staged plugin directories or repo marketplaces for itself.

## Codex Plugin Root Structure

When bootstrapping or aligning a plugin repo, follow the current OpenAI plugin structure:

- every plugin has a manifest at `.codex-plugin/plugin.json`
- only `plugin.json` belongs in `.codex-plugin/`
- `skills/`, `.app.json`, `.mcp.json`, and `assets/` belong at the plugin root
- plugin manifests should point to bundled skill folders with `"skills": "./skills/"`
- marketplace `source.path` should point at the plugin root directory

## Dependency Provenance

When creating or aligning `AGENTS.md`, include strict dependency guidance:

- shared project dependencies must resolve from GitHub repository URLs, package managers, package registries, or other real remote repositories
- committed dependency declarations, lockfiles, scripts, docs, examples, generated project files, and CI config must not point at machine-local paths
- machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly

## Codex Install-Surface Map

When bootstrapping or aligning repo guidance, teach Codex plugin wiring with four separate surfaces:

- marketplace catalog
  - personal: `~/.agents/plugins/marketplace.json`
  - repo: `$REPO_ROOT/.agents/plugins/marketplace.json`
  - role: the catalog Codex reads from; each plugin entry points `source.path` at a staged plugin directory
- staged plugin directory
  - common personal pattern: `~/.codex/plugins/<plugin-name>`
  - common repo pattern from the docs: `$REPO_ROOT/plugins/<plugin-name>`
  - role: the plugin root payload on disk
- installed plugin cache
  - `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`
  - role: Codex's installed copy for runtime loading
- enabled-state config
  - documented plugin path: `~/.codex/config.toml`
  - role: on or off state keyed by plugin plus marketplace identity, such as `[plugins."my-plugin@socket"]`

Bootstrap docs should keep discovery mirrors, plugin packaging, marketplace catalogs, staged payload directories, cache paths, and config-state separate. Do not blur "where Codex can see a plugin", "where the plugin payload lives", and "whether the plugin is enabled" into one sentence.

If you mention project-scoped `.codex/config.toml`, describe it as a general Codex config surface from the config reference, not as a separate documented plugin install surface.
