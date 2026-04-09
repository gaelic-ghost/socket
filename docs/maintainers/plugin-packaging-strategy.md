# Plugin Packaging Strategy

This document records the current packaging decision for the `socket` superproject.

## Working Rule

Package child repositories as independent plugins first.

If a combined plugin becomes useful later, add that as a separate `socket`-level packaging layer instead of redefining the child repositories around bundle semantics.

## Why

This keeps the near-term model simpler and lowers coupling:

- each child repository can be developed and versioned independently
- the repo-root marketplace can list plugins one by one without inventing a bundle model too early
- aggregate plugins can be added later as a deliberate packaging feature
- reverting back toward fully independent repos stays easier if the superproject experiment fails

## What Is Deferred

These are intentionally not phase-one requirements:

- one plugin composed from multiple child repositories
- shared versioning across child repos
- a single aggregate plugin manifest that becomes the source of truth for several subtree directories
- cross-repo bundle ownership rules for hooks, apps, or MCP server packaging

## Immediate Packaging Direction

The current direction is:

1. initialize empty `*-skills` repositories as standalone plugin repos
2. import them into `socket/plugins/` as subtrees
3. keep the `socket` marketplace ready to list each plugin independently
4. only add marketplace entries for child repos that actually ship `.codex-plugin/plugin.json`

## Follow-up Decision

Once several child repos have stable plugin packaging, decide whether `socket` needs:

- only an independent plugin catalog, or
- an additional aggregate plugin layer for curated bundles
