# socket

Superproject for Gale's local Codex plugin and skills monorepo experiment.

## Overview

This repository is a durable building-block change, not a local convenience wrapper.

It is intended to unlock:

- one shared Codex repo root for plugin marketplace experiments
- one place to stage adjacent `*-skills` and related plugin repositories as in-repo directories
- a lower-maintenance path than submodules for evaluating whether Codex behaves better with a single repo root
- a reversible path from separate repos toward a real monorepo if the subtree model proves worthwhile

## Motivation

`socket` exists because Codex's current marketplace behavior is still strongly repo-root scoped.

Keeping the adjacent plugin and skills repositories under one Git root gives this experiment one clear place to:

- expose a shared repo-root Codex marketplace
- stage multiple child plugin repositories side by side without nested Git roots
- validate whether repo-root discovery behaves better than personal-scope installs for Gale's actual day-to-day repos
- keep a path back to independent child repositories if the experiment stops paying for itself

## Current Status

This repo is now in first-pass imported-monorepo shape.

- the target layout is documented in [docs/maintainers/subtree-migration-plan.md](./docs/maintainers/subtree-migration-plan.md)
- the packaging direction is documented in [docs/maintainers/plugin-packaging-strategy.md](./docs/maintainers/plugin-packaging-strategy.md)
- the day-to-day subtree maintenance workflow is documented in [docs/maintainers/subtree-workflow.md](./docs/maintainers/subtree-workflow.md)
- the cross-repo standards alignment plan is documented in [docs/maintainers/plugin-alignment-plan.md](./docs/maintainers/plugin-alignment-plan.md)
- `plugins/` is reserved for subtree imports
- `.agents/plugins/marketplace.json` is reserved for the repo-root Codex marketplace catalog
- the repo-root marketplace now lists every non-private child plugin surface by default
- aggregate multi-repo plugins are explicitly deferred behind independent child plugin packaging

## Imported Repositories

The current subtree-managed child repositories are:

- `agent-plugin-skills`
- `apple-dev-skills`
- `dotnet-skills`
- `productivity-skills`
- `python-skills`
- `rust-skills`
- `speak-to-user-skills`
- `web-dev-skills`
- `things-app`

Each child repository keeps its own source-of-truth docs and history inside its imported subtree. `socket` is responsible for the superproject concerns around import shape, root marketplace wiring, and cross-repo maintenance workflow.

`private-skills` is intentionally excluded from this public superproject and from the root marketplace. It remains a separate private repository.

Public source repositories that now back the rebuilt minimal child repos:

- [`gaelic-ghost/speak-to-user-skills`](https://github.com/gaelic-ghost/speak-to-user-skills)
- [`gaelic-ghost/web-dev-skills`](https://github.com/gaelic-ghost/web-dev-skills)

## Marketplace Shape

The repo-root marketplace lives at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json).

`socket` lists every non-private child plugin surface by default. Some children expose a top-level `.codex-plugin/plugin.json`, some keep their packaged plugin root inside their own nested `plugins/<plugin-name>/` directory, and some intentionally expose root `skills/` through thin repo-local marketplace metadata. The socket marketplace points at the actual child surface that the imported repo treats as installable.

Current listed plugin roots are:

- `./plugins/agent-plugin-skills`
- `./plugins/apple-dev-skills/skills`
- `./plugins/dotnet-skills`
- `./plugins/productivity-skills/skills`
- `./plugins/python-skills/plugins/python-skills`
- `./plugins/rust-skills`
- `./plugins/speak-to-user-skills`
- `./plugins/things-app/plugins/things-app`
- `./plugins/web-dev-skills`

## Working In Socket

Treat `socket` as a superproject, not as the canonical authoring home for every child repository concern.

- Use the root docs to understand how subtree imports, root marketplace wiring, and release flow work.
- Use the child repository docs inside `plugins/<name>/` when the work is really about that child repo's own skills, plugin packaging, tests, or release process.
- Prefer updating child repositories at their source roots and then syncing the subtree into `socket` unless the task is explicitly about the monorepo itself.
- Keep the root marketplace and maintainer docs in sync whenever a child repo gains, moves, or removes plugin packaging.

## Verification

There is no single heavy repo-wide build or test pipeline for `socket` yet.

The current superproject validation surface is lightweight and structural:

- keep `.agents/plugins/marketplace.json` valid JSON
- verify that every listed `source.path` matches the real child surface the imported repo treats as installable
- review child repository docs and packaging paths when imports or packaging layouts change
- run child-repo-specific checks from the relevant imported subtree when the change is really about that child repo

## Layout

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── docs/
│   └── maintainers/
│       ├── plugin-alignment-plan.md
│       ├── plugin-packaging-strategy.md
│       ├── subtree-migration-plan.md
│       └── subtree-workflow.md
├── plugins/
│   ├── agent-plugin-skills/
│   ├── apple-dev-skills/
│   ├── dotnet-skills/
│   ├── productivity-skills/
│   ├── python-skills/
│   ├── rust-skills/
│   ├── speak-to-user-skills/
│   ├── web-dev-skills/
│   └── things-app/
└── README.md
```
