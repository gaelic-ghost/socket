# socket

Mixed-model monorepo for Gale's Codex plugins and skills repositories.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Release Notes](#release-notes)
- [Verification](#verification)
- [License](#license)
- [Current Status](#current-status)
- [Imported Repositories](#imported-repositories)
- [Marketplace Shape](#marketplace-shape)
- [Working In Socket](#working-in-socket)
- [Repository Layout](#repository-layout)

## Overview

Some skills and plugins I've been building to make Codex better and more useful at stuff that's important to me. Claude Code compat is in-progress.

### Status

`socket` is an active monorepo with two remaining subtree-managed child repositories, `apple-dev-skills` and `python-skills`, and the rest of the child directories now treated as ordinary monorepo-owned nested directories wired into the root marketplace.

### What This Project Is

This repository owns the root marketplace, the monorepo-owned nested directories under `plugins/`, the remaining subtree sync paths for `apple-dev-skills` and `python-skills`, and the root maintainer docs.

### Motivation

It exists to keep the plugin and skills experiment workable under one Git root while Codex still lacks better shared-parent scoping, without carrying subtree sync complexity for repos that no longer need to live as separate public sources of truth.

## Setup

Read the overview and marketplace sections first, then use the mixed monorepo workflow below. Only `apple-dev-skills` and `python-skills` still use subtree sync.

## Usage

Use the root marketplace and maintainer docs for the monorepo layer. Use the docs inside each nested directory for repo-specific authoring, validation, and release work.

## Development

### Setup

Clone the repository, use the root `uv` dev environment when running the productivity maintainer scripts, and work in `plugins/<repo>/` for child-directory changes unless the task is explicitly root-level.

### Workflow

Edit the monorepo copy first, keep root docs and marketplace wiring in sync with packaging changes, and reserve `git subtree pull` / `git subtree push` for `plugins/apple-dev-skills/` and `plugins/python-skills/`.

## Verification

There is no single heavy repo-wide build or test pipeline for `socket` yet.

The current superproject validation surface is lightweight and structural:

- keep `.agents/plugins/marketplace.json` valid JSON
- verify that every listed `source.path` matches the real child surface the imported repo treats as installable
- review child repository docs and packaging paths when imports or packaging layouts change
- run child-repo-specific checks from the relevant imported subtree when the change is really about that child repo

## Release Notes

Use Git history plus GitHub releases for root-level superproject changes, and rely on each imported child repository to track its own shipped release notes inside its subtree.

## License

See [LICENSE](./LICENSE).

## Current Status

Active experiment, with `apple-dev-skills` and `python-skills` still subtree-managed and the other child repositories now living as ordinary nested directories inside the monorepo.

## Imported Repositories

The current plugin and skills directories under `plugins/` are:

- `agent-plugin-skills`
- `apple-dev-skills`
- `dotnet-skills`
- `productivity-skills`
- `python-skills`
- `rust-skills`
- `web-dev-skills`
- `things-app`

`apple-dev-skills` and `python-skills` are the only directories in that list that still keep live subtree relationships to separate source repositories. The other directories are now monorepo-owned nested directories. `socket` is their canonical source of truth.

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
- `./plugins/things-app/plugins/things-app`
- `./plugins/web-dev-skills`

## Working In Socket

Treat `socket` as the canonical authoring home for the monorepo-owned nested directories, and as the subtree host for `apple-dev-skills` and `python-skills`.

- Use the root docs to understand the mixed monorepo model, root marketplace wiring, and release flow.
- Use the child directory docs inside `plugins/<name>/` when the work is really about that directory's own skills, plugin packaging, tests, or release process.
- For ordinary fixes in monorepo-owned child directories, edit `plugins/<name>/` directly and commit in `socket`.
- For `apple-dev-skills` and `python-skills`, keep the subtree workflow explicit when you need to sync with or publish back to their separate source repositories.
- Keep the root marketplace and maintainer docs in sync whenever a child repo gains, moves, or removes plugin packaging.

## Repository Layout

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
│   ├── web-dev-skills/
│   └── things-app/
└── README.md
```
