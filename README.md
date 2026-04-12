# socket

Subtree-managed superproject for Gale's public Codex plugins and skills repositories.

## Overview

Some skills and plugins I've been building to make Codex better and more useful at stuff that's important to me. Claude Code compat is in-progress.

## Motivation

`socket` exists because Codex's current plugin and marketplace scoping is still awkward for multi-repo local work. The superproject keeps one repo-root marketplace, one Git root, and one maintainer surface while preserving each imported child repository as its own real project.

## Current Status

Active experiment, with the current public child repositories already imported as subtrees and wired into the root marketplace.

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

Each child repository keeps its own docs, release history, and packaging decisions inside its imported subtree. `socket` owns only the superproject layer: subtree layout, root marketplace wiring, and cross-repo maintainer guidance.

## Marketplace Shape

The repo-root marketplace lives at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json).

`socket` lists public child plugin surfaces by default. Some children expose a top-level `.codex-plugin/plugin.json`, some keep their packaged plugin root inside their own nested `plugins/<plugin-name>/` directory, and some intentionally expose root `skills/` through a thin repo-local marketplace file. The socket marketplace points at the actual child surface that the imported repo treats as installable. I'll standardize this once there's something to standardize to.

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
- For ordinary child-repo fixes that should publish back upstream, edit the monorepo copy first under `plugins/<name>/`, commit in `socket`, then push the result back out with `git subtree push --prefix=plugins/<name> <remote> <branch>`.
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
