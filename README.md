# socket

Superproject for Gale's local Codex plugin and skills monorepo experiment.

## Purpose

This repository is a durable building-block change, not a local convenience wrapper.

It is intended to unlock:

- one shared Codex repo root for plugin marketplace experiments
- one place to stage adjacent `*-skills` and related plugin repositories as in-repo directories
- a lower-maintenance path than submodules for evaluating whether Codex behaves better with a single repo root
- a reversible path from separate repos toward a real monorepo if the subtree model proves worthwhile

## Current Status

This repo is in migration-planning and scaffold phase.

- the target layout is documented in [docs/maintainers/subtree-migration-plan.md](./docs/maintainers/subtree-migration-plan.md)
- `plugins/` is reserved for subtree imports
- `.agents/plugins/marketplace.json` is reserved for the repo-root Codex marketplace catalog
- non-git directories are explicitly excluded from phase one subtree imports

## Layout

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── docs/
│   └── maintainers/
│       └── subtree-migration-plan.md
├── plugins/
└── README.md
```
