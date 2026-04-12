# Plugin Alignment Plan

This document records the current plan for bringing the child directories in `socket` into closer alignment with the maintainer standards anchored by `agent-plugin-skills`.

## Standards Baseline

Treat the current [`plugins/agent-plugin-skills/AGENTS.md`](../../plugins/agent-plugin-skills/AGENTS.md) as the practical standards reference for this pass.

The near-term standards that matter most across the imported repos are:

- keep each repository honest about what it really ships today
- make the source-of-truth model explicit
- keep skill authoring rooted in top-level `skills/` when the repo is truly a skills-export repository
- keep plugin packaging thin and explicit instead of hiding it behind duplicated trees
- keep Codex marketplace limitations documented plainly
- keep maintainer docs and packaging surfaces aligned with the real repo shape
- avoid stale vendored copies of other plugin repos inside nested directories

## Current Socket-Level Agent Plugin Skills State

Codex currently has the `socket`-scoped `agent-plugin-skills` plugin enabled, and the installed cache at `~/.codex/plugins/cache/socket/agent-plugin-skills/local/.codex-plugin/plugin.json` reports version `1.2.0`.

That means the superproject is currently using the top-level imported `agent-plugin-skills` subtree as the relevant standards reference, not an older vendored copy.

## Imported Repo Inventory

### Already Closest To The Standards Model

- `agent-plugin-skills`
  - top-level `.codex-plugin/plugin.json`
  - top-level `skills/`
  - explicit repo-local standards and source-of-truth guidance
- `web-dev-skills`
  - honest minimal standalone plugin repo
  - top-level `.codex-plugin/plugin.json`
  - no fake exported skill inventory yet
- `dotnet-skills`
  - top-level `.codex-plugin/plugin.json`
  - still minimal, but the shape is simple and honest
- `rust-skills`
  - top-level `.codex-plugin/plugin.json`
  - still minimal, but the shape is simple and honest

### Partially Aligned But Still Divergent

- `python-skills`
  - root `skills/` is canonical
  - keeps nested packaged plugin roots under `plugins/python-skills/`
  - still carries repo-local marketplace and Claude packaging surfaces that should be reviewed against the current simpler standards posture
- `productivity-skills`
  - root `skills/` is canonical
  - still uses repo-local marketplace and Claude marketplace surfaces rather than top-level source-first Codex packaging
- `apple-dev-skills`
  - root `skills/` is canonical
  - still uses repo-local marketplace and Claude packaging surfaces
  - needs a deliberate decision on whether it should stay in that model or converge toward the simpler top-level source-first packaging model
- `things-app`
  - intentionally mixed repo with root `skills/`, bundled MCP server, and nested packaged plugin root
  - should align on honesty, source-of-truth wording, and packaging clarity, but should not be forced into a pure skills-export shape if that would erase the MCP-first repo reality

### Excluded Or Retired From Public Socket

- `private-skills`
  - private repo that should stay outside the public `socket` superproject
  - do not expose it through the root marketplace or public subtree inventory
- `speak-to-user-skills`
  - no longer exists as a live directory in this working tree
  - remove stale root-marketplace or docs references instead of treating it as active inventory

## First Alignment Pass

The first pass should focus on cross-repo clarity, not forced uniformity.

1. Audit every imported repo for the same core questions:
   - what is the canonical authored surface
   - where does Codex packaging actually live
   - where does Claude packaging actually live
   - does the README describe the real repo shape
   - does `AGENTS.md` describe the real source-of-truth order
2. Remove stale vendored plugin copies wherever the top-level subtree already exists in `socket`.
3. Normalize minimal placeholder repos so they stay small and honest until real skills exist.
4. Decide which repos should converge toward top-level source-first Codex packaging versus which repos intentionally keep nested or mixed packaging because their repo purpose is materially different.

## Repo-By-Repo Next Actions

### High Priority

- `apple-dev-skills`
  - [x] audit README, `AGENTS.md`, and packaging surfaces against the current `agent-plugin-skills` honesty rules
  - [x] decide the repo-local marketplaces should point directly at root `skills/` rather than describe a nonexistent packaged plugin tree
- `productivity-skills`
  - [x] run the same source-of-truth and packaging honesty audit
  - [x] tighten the README so the repo is described as root `skills/` plus thin marketplace metadata instead of as a separately staged packaged plugin tree
- `python-skills`
  - [x] confirm the nested plugin-root model is still the intended long-term packaging shape
  - [x] align docs and maintainer guidance with that chosen shape and active five-skill inventory
- `things-app`
  - [x] verify that the mixed skills plus MCP plus nested plugin model is described plainly and consistently
  - [x] strengthen maintainer guidance so the mixed repo model is explicit in `AGENTS.md`

### Medium Priority

- `dotnet-skills`
  - keep the repo minimal until real skills land
  - add richer maintainer guidance only when the repo starts shipping real content
- `rust-skills`
  - same as `dotnet-skills`
- `web-dev-skills`
  - keep it minimal until the first real web-focused skill exists

### Deferred Outside Socket

- `private-skills`
  - maintain it separately as a private repo instead of standardizing it inside public `socket`

## Practical Rule

Alignment here should mean "clearer, more honest, and more maintainable relative to the current standards anchor", not "force every imported repo into the exact same packaging topology."
