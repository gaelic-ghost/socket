---
name: maintain-agent-plugins
description: Create or align agent plugin repositories, install deterministic managed FSX plugin maintenance, and validate or apply the whole plugin set through exactly two aggregate Just commands.
license: Apache-2.0
metadata:
  semver: 1.0.0
---

# Maintain Agent Plugins

## Purpose

Create and maintain Codex plugin source without reintroducing hand-maintained
metadata, per-plugin commands, Python automation, or customizable scaffolding.
Use current official OpenAI plugin documentation for host schema facts, then
apply the fixed Socket repository policy through the managed runtime.

## Required Interface

Plugin maintenance has exactly two public commands. Each processes every plugin
manifest and marketplace entry owned by the repository:

```text
just plugins-check
just plugins-apply
```

Do not add per-plugin, per-manifest, scaffold, sync, bootstrap, or alternate
mode recipes. `plugins-check` is read-only. `plugins-apply` performs the complete
deterministic reconciliation and then checks its result.

## Installation

1. Confirm the target is a Git repository root.
2. Run `scripts/maintain-agent-plugins.fsx --repo-root <path> --operation install`
   from this skill once to copy the managed runtime and Just import.
3. The installer also adds ordered repository-maintenance hooks when the target
   already uses the canonical `scripts/repo-maintenance/` runtime.
4. Run `just plugins-apply`, then `just repo-validate` when repository-skills is
   present.

Use `--operation refresh` to replace managed files from this skill and
`--operation report-only` for a read-only drift report. These installer modes
are skill internals, not additional Just tasks.

## Fixed Policy

- Publisher: Gale, `mail@galewilliams.com`,
  `https://github.com/gaelic-ghost`.
- License: Apache-2.0.
- Plugin names: stable kebab case matching their directory.
- Manifest: `.codex-plugin/plugin.json`; bundled skills: `./skills/`.
- Default plugin repository URL:
  `https://github.com/gaelic-ghost/<plugin-name>`.
- Local marketplace policy: `AVAILABLE` and `ON_INSTALL`.
- Default category: `Developer Tools` unless the plugin already has an
  intentional product category.
- Default-discovered hook files stay at `hooks/hooks.json`; do not duplicate
  that default path in the manifest.
- `interface.defaultPrompt` is an array of at most three concise prompts.

The runtime owns these choices. Do not add user profiles, policy files,
template variables, interactive questions, or project-local overrides.

## Creating a Plugin

1. Establish one bounded capability and its owning plugin name.
2. Create the plugin directory, `.codex-plugin/plugin.json`, `AGENTS.md`, and at
   least one complete skill under `skills/<skill-name>/SKILL.md`.
3. Add only real optional surfaces: `.mcp.json`, `.app.json`, `hooks/`, agents,
   or assets must have an actual consumer and validation path.
4. Use the fixed publisher and license policy. Write plugin-specific purpose,
   descriptions, prompts, keywords, and capability content directly; these are
   authored semantics, not customization inputs.
5. Run `just plugins-apply`. In Socket, this adds missing root marketplace
   wiring and checks the complete plugin set.
6. Run only the repository root integration/E2E path. Do not create tests under
   the plugin or skill.

## Ownership Handoffs

- Use `repository-skills:maintain-project-repo` for the four canonical docs,
  repo-wide synchronization and validation, protected-main releases, and
  version changes.
- Use `agent-engineering-skills` for agent orchestration, automation, eval, and
  scheduling behavior.
- Use `agent-portability-skills` for ACP, A2A, MCP boundary selection, Zed,
  Hermes, and other host adapters.
- Keep runtime hooks and MCP implementation with the plugin that ships them;
  this skill owns their packaging consistency, not their product behavior.

## Guards

- Never edit installed plugin caches or enabled-state configuration.
- Never restore `bootstrap-skills-plugin-repo`,
  `sync-skills-repo-guidance`, Python generators, or nested plugin tests.
- Never infer a new packaging layer or publish destination.
- Stop when a manifest name and directory disagree, a managed target is not a
  regular file, or a required optional asset is missing.

## Script Inventory

- `scripts/maintain-agent-plugins.fsx`
