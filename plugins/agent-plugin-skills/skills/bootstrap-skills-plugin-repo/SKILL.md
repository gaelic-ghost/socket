---
name: bootstrap-skills-plugin-repo
description: Bootstrap or align a skills-export repository with root `skills/`, repo-local discovery mirrors, maintainer docs, and clear Codex plugin-boundary wording. Use when creating a new skills repo or structurally aligning an existing one. Do not use this for narrow README-only or roadmap-only maintenance.
---

# Bootstrap Skills Plugin Repo

Bootstrap or align a skills-export repository.

## Codex Model Note

State plainly that OpenAI's documented Codex plugin system exposes repo-visible plugins through marketplace catalogs and does not document a richer repo-private scoping model beyond that. This repository pattern allows root `.codex-plugin` packaging, and standalone plugin repositories should carry a repo-local marketplace when they are meant to be installed directly. Do not normalize nested staged plugin directories or installer-era helper workflows for this repo family.

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

## Codex Subagent Guidance

When creating or aligning skills that can benefit from parallel support work, add optional `Codex Subagent Fit` guidance that matches OpenAI's current Codex subagent docs:

- Codex only spawns subagents when the user explicitly asks for subagents or parallel agent work.
- Good fits are bounded read-heavy discovery, docs pulling, tests, triage, log analysis, and summarization.
- Subagents should return concise findings, evidence, links, or file references instead of raw intermediate output.
- Apply-mode or implementation edits should stay in the main thread unless the user explicitly asks for parallel implementation and each worker has a disjoint write scope.

Do not add subagent guidance to every skill by default. Use `docs/maintainers/codex-subagent-skill-guidance.md` to decide whether the target skill has real parallelizable support work.

## Codex Install-Surface Map

When bootstrapping or aligning repo guidance, teach Codex plugin wiring with five separate surfaces:

- tracked marketplace source
  - preferred user path: `codex plugin marketplace add <owner>/<repo> --ref main`
  - update path: `codex plugin marketplace upgrade <marketplace-name>`
  - role: Codex-managed Git checkout for a marketplace source
- marketplace catalog
  - personal: `~/.agents/plugins/marketplace.json`
  - repo: `$REPO_ROOT/.agents/plugins/marketplace.json`
  - role: the catalog Codex reads from; each plugin entry points at a plugin root
- plugin root payload
  - common personal pattern: `~/.codex/plugins/<plugin-name>`
  - common repo pattern from the docs: `$REPO_ROOT/plugins/<plugin-name>`
  - Git-backed marketplace pattern: a plugin root inside the tracked marketplace checkout
  - role: the plugin root payload on disk
- installed plugin cache
  - `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`
  - role: Codex's installed copy for runtime loading
- enabled-state config
  - documented plugin path: `~/.codex/config.toml`
  - role: on or off state keyed by plugin plus marketplace identity, such as `[plugins."my-plugin@socket"]`

Bootstrap docs should make the Git-backed marketplace path the default user install/update story. Use manual local marketplace or copied-payload instructions only for local development, unpublished testing, or fallback cases.

Bootstrap docs should keep discovery mirrors, plugin packaging, marketplace sources, marketplace catalogs, plugin root payload directories, cache paths, and config-state separate. Do not blur "where Codex can see a plugin", "where the plugin payload lives", "how Codex updates the marketplace", and "whether the plugin is enabled" into one sentence.

If you mention project-scoped `.codex/config.toml`, describe it as a general Codex config surface from the config reference, not as a separate documented plugin install surface.
