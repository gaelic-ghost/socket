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
- a single aggregate plugin manifest that becomes the source of truth for several subtree directories
- cross-repo bundle ownership rules for hooks, apps, or MCP server packaging

## Immediate Packaging Direction

The current direction is:

1. keep monorepo-owned child repos as ordinary directories under `socket/plugins/` when they no longer need an upstream subtree sync target
2. preserve explicit subtree sync only for child repos that still need to publish back out independently
3. keep the `socket` marketplace ready to list each plugin independently
4. only add marketplace entries for child repos that actually ship `.codex-plugin/plugin.json`
5. keep root `socket` docs aligned with child packaging moves and coordinated release-prep changes instead of treating the marketplace file as the only source of truth
6. keep the maintained version-bearing manifests aligned on one shared semantic version through the root release-version workflow instead of hand-editing scattered files

Recent monorepo-owned examples follow that rule directly: `things-app` and `cardhop-app` both package from their child-repo roots while keeping bundled MCP server code under each child repo's top-level `mcp/` directory, and placeholder child repos like `evidence-locker` can still ship a minimal child-root plugin manifest before their first real workflow surface exists.

Child-repo internal layout changes do not automatically imply root marketplace changes. If a child repo keeps the same packaged plugin root, keep the `socket` marketplace path stable and only update the root docs to explain the child's new internal layout. Recent example: `things-app` keeps its marketplace path at `./plugins/things-app` while its bundled MCP server lives at top-level `mcp/` inside that child repo.

`socket` itself still does not define an aggregate root plugin above the child repos. The root packaged surface here is the marketplace catalog, not a second shared plugin bundle.

## Follow-up Decision

Once several child repos have stable plugin packaging, decide whether `socket` needs:

- only an independent plugin catalog, or
- an additional aggregate plugin layer for curated bundles
