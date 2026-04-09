---
name: bootstrap-skills-plugin-repo
description: Bootstrap or align a skills-export repository with root `skills/`, repo-local discovery mirrors, maintainer docs, and explicit Codex limitation wording. Use when creating a new skills repo or structurally aligning an existing one. Do not use this for narrow README-only or roadmap-only maintenance.
---

# Bootstrap Skills Plugin Repo

Bootstrap or align a skills-export repository.

## Codex Limitation Warning

Warn plainly that OpenAI's documented Codex plugin system does not provide proper repo-private plugin scoping. This repository pattern does not normalize nested plugin directories or repo marketplaces for itself.

## Codex Install-Surface Map

When bootstrapping or aligning repo guidance, teach Codex plugin wiring with four separate surfaces:

- marketplace catalog
  - personal: `~/.agents/plugins/marketplace.json`
  - repo: `$REPO_ROOT/.agents/plugins/marketplace.json`
  - role: the catalog Codex reads from; each plugin entry points `source.path` at a staged plugin directory
- staged plugin directory
  - common personal pattern: `~/.codex/plugins/<plugin-name>`
  - common repo pattern from the docs: `$REPO_ROOT/plugins/<plugin-name>`
  - role: the plugin payload on disk
- installed plugin cache
  - `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`
  - role: Codex's installed copy for runtime loading
- enabled-state config
  - personal: `~/.codex/config.toml`
  - optional repo override: `$REPO_ROOT/.codex/config.toml`
  - role: on or off state keyed by plugin plus marketplace identity, such as `[plugins."my-plugin@socket"]`

Bootstrap docs should keep discovery mirrors, plugin packaging, marketplace catalogs, staged payload directories, cache paths, and config-state separate. Do not blur "where Codex can see a plugin", "where the plugin payload lives", and "whether the plugin is enabled" into one sentence.
