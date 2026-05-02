# socket

Mixed-model monorepo for Gale's Codex plugin and skills repositories.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [License](#license)
- [Repository Docs](#repository-docs)
- [Plugin Surfaces](#plugin-surfaces)
- [Marketplace Shape](#marketplace-shape)

## Overview

### Status

This repository is active and maintained as the superproject coordination layer.

### What This Project Is

`socket` is the superproject Gale uses to keep several Codex plugin and skills repositories under one Git root while OpenAI's documented Codex plugin system still lacks a better shared-parent scoping model. It owns the repo-root Codex marketplace at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json), the monorepo-owned child directories under [`plugins/`](./plugins/), the remaining subtree sync paths for `apple-dev-skills` and `SpeakSwiftlyServer`, and the root maintainer docs that explain how the mixed model works.

### Motivation

It exists to keep the plugin and skills experiment workable under one repository without pretending Codex currently supports clean repo-private plugin packs, hidden repo-local install surfaces, or richer parent-level scoping than the documented marketplace model provides.

## Quick Start

Start here when the task is about the superproject layer rather than one child repository:

1. Read [`README.md`](./README.md), [`AGENTS.md`](./AGENTS.md), and [`docs/maintainers/subtree-workflow.md`](./docs/maintainers/subtree-workflow.md).
2. Confirm whether the work belongs at the root `socket` layer or inside a specific child repo under [`plugins/`](./plugins/).
3. If you need the root maintainer Python environment, sync it with:

```bash
uv sync --dev
```

4. Run the root validation path when the change touches marketplace wiring or the root metadata contract:

```bash
uv run scripts/validate_socket_metadata.py
```

For ordinary user installation, prefer the official Git-backed marketplace path. Add the `socket` marketplace from Git, then update it through Codex when the marketplace or child plugin entries change:

```bash
codex plugin marketplace add gaelic-ghost/socket
codex plugin marketplace upgrade socket
```

After the marketplace is added or upgraded, restart Codex, open the plugin directory in the Codex GUI, choose the `Socket` marketplace, and install or enable the desired child plugins there. Manual local marketplace roots are useful for development, unpublished testing, and fallback work, but they are not the default user install or update path.

## Usage

Use `socket` when the task is about the superproject layer:

- root marketplace wiring
- mixed monorepo policy
- subtree sync flow for `apple-dev-skills` or `SpeakSwiftlyServer`
- cross-repo maintainer guidance
- coordinated child-skill guidance, such as Codex subagent wording that must stay consistent across exported skills
- coordinated release-prep work that needs the root docs and child version surfaces to stay in sync
- coordinated semantic-version bumps that keep the maintained manifests aligned across the superproject

When the work is really about one child repository's own behavior, start from that child directory's docs instead.

## Development

### Setup

Sync the root maintainer environment with:

```bash
uv sync --dev
```

For Python-backed maintainer tooling in this superproject or its child repositories, keep the repo-local baseline explicit in `pyproject.toml` instead of assuming machine-global tools. When a repo expects Python validation, declare the needed dev dependencies there, including `pytest`, `ruff`, and `mypy` when those checks are part of the shipped workflow.

Only `apple-dev-skills` and `SpeakSwiftlyServer` still use subtree sync workflows. `python-skills` is now maintained as a normal monorepo-owned child directory. `socket` itself does not ship a root plugin; the repo marketplace is the root Codex-facing catalog here.

### Workflow

Treat Gale's local `socket` checkout as the normal day-to-day checkout on `main`. Work in the monorepo copy first, and use the relevant directory under [`plugins/`](./plugins/) for child-repository changes unless the task is explicitly about the root marketplace or root maintainer docs. Reach for a feature branch or a dedicated worktree only when the change needs extra isolation.

Keep root docs and marketplace wiring in sync with packaging changes in the same pass. For monorepo-owned child directories, edit the relevant directory under [`plugins/`](./plugins/) directly and commit in `socket`. For `apple-dev-skills` and `SpeakSwiftlyServer`, keep subtree sync operations explicit and isolated. `SpeakSwiftlyServer` is pull-only from `socket` by default: release and validate it in its standalone checkout, then pull the released state down here.

When a guidance change intentionally spans multiple child skill repositories, update the affected child docs and the root `socket` docs in the same pass so the superproject still explains why the coordinated edit belongs here.

### Shared Versioning

The maintained version surfaces in `socket` now move together on one shared semantic version. Use the root release-version script to inventory the live targets or to apply a patch, minor, major, or explicit custom version across the superproject:

```bash
scripts/release.sh inventory
scripts/release.sh patch
scripts/release.sh minor
scripts/release.sh major
scripts/release.sh custom 1.2.3
```

`patch`, `minor`, and `major` are intentionally blocked until every maintained version surface already agrees on one shared version. Use `custom <x.y.z>` once to align them, then use the normal bump modes afterward.

Use [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the maintainer workflow boundary and [`ROADMAP.md`](./ROADMAP.md) for root planning and historical notes.

Use [`docs/maintainers/release-modes.md`](./docs/maintainers/release-modes.md) for the full release flow. `standard` is the normal `socket` release mode; `subtrees` is the standard mode plus explicit pull/push accounting for subtree-managed children.

### Validation

The current root validation surface is structural:

- keep [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json) valid JSON
- verify that every listed `source.path` matches the real child surface that the child repo treats as installable
- verify that every packaged plugin path still exposes a matching `.codex-plugin/plugin.json`
- review child-repo docs when plugin packaging paths move
- run child-repo-specific validation from the relevant child repo when the change is really about that child repo

Run the root validator locally with:

```bash
uv run scripts/validate_socket_metadata.py
```

When a child repository or helper surface grows Python-backed validation beyond this root metadata check, add those checks as repo-local `uv` dev dependencies and document the exact `uv run ...` commands in that child repo instead of assuming a globally provisioned toolchain.

## Repo Structure

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── ACCESSIBILITY.md
├── CONTRIBUTING.md
├── docs/
│   └── maintainers/
│       ├── plugin-packaging-strategy.md
│       ├── release-modes.md
│       └── subtree-workflow.md
├── plugins/
├── scripts/
│   └── validate_socket_metadata.py
├── AGENTS.md
├── README.md
└── ROADMAP.md
```

## Release Notes

Use Git history and GitHub releases for root-level superproject changes. Child repositories should continue to track their own shipped release notes inside their own surfaces.

## License

The `socket` superproject is licensed under the Apache License 2.0. See [LICENSE](./LICENSE) for the full text and [NOTICE](./NOTICE) for the root superproject notice surface.

## Repository Docs

The root superproject docs are:

- [README.md](./README.md) for the superproject overview and root workflow
- [CONTRIBUTING.md](./CONTRIBUTING.md) for root contribution workflow expectations
- [AGENTS.md](./AGENTS.md) for root operating rules and repo-boundary guidance
- [ROADMAP.md](./ROADMAP.md) for root planning and milestone tracking
- [ACCESSIBILITY.md](./ACCESSIBILITY.md) for the root accessibility contract around docs, metadata, and maintainer automation
- [`docs/maintainers/`](./docs/maintainers/) for the deeper maintainer references behind the mixed-monorepo and subtree model
- [`docs/maintainers/release-modes.md`](./docs/maintainers/release-modes.md) for the `standard` and `subtrees` release modes

## Plugin Surfaces

Treat `socket` as the canonical home for the monorepo-owned child directories and as the subtree host for the remaining imported child repos.

- `agent-plugin-skills`, `cardhop-app`, `dotnet-skills`, `productivity-skills`, `rust-skills`, `spotify`, `things-app`, and `web-dev-skills` are monorepo-owned here.
- `apple-dev-skills` and `SpeakSwiftlyServer` preserve explicit subtree sync paths.
- `SpeakSwiftlyServer` is synchronized into `socket` by subtree pull after the standalone child release lands; do not subtree-push it from `socket` unless Gale explicitly asks for that exception.
- `python-skills` is monorepo-owned here with no separate upstream GitHub release target.
- Child repos may expose plugin packaging from their own repo roots whether they are monorepo-owned here or still preserve subtree sync.
- `apple-dev-skills` packages from its child-repo root at `./plugins/apple-dev-skills`, and its Codex plugin manifest registers Xcode's built-in MCP bridge through a root `.mcp.json`.
- `apple-dev-skills` and `SpeakSwiftlyServer` also carry their own repo-local `.agents/plugins/marketplace.json` files so Codex can track either child repository as a Git-backed standalone marketplace without cloning `socket`.
- `things-app` packages from its child-repo root at `./plugins/things-app`, and its bundled MCP server lives directly under that child repo's top-level `mcp/` directory.
- `cardhop-app` packages from its child-repo root at `./plugins/cardhop-app`, and its bundled MCP server lives directly under that child repo's top-level `mcp/` directory.

## Marketplace Shape

The repo-root marketplace lives at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json).

That marketplace points at the actual plugin root each child repository treats as installable today:

- `./plugins/agent-plugin-skills`
- `./plugins/apple-dev-skills`
- `./plugins/cardhop-app`
- `./plugins/dotnet-skills`
- `./plugins/productivity-skills`
- `./plugins/SpeakSwiftlyServer`
- `./plugins/python-skills`
- `./plugins/rust-skills`
- `./plugins/spotify`
- `./plugins/things-app`
- `./plugins/web-dev-skills`

For `things-app`, that marketplace path stays `./plugins/things-app` because the installable plugin root is the child repo root even though the bundled server now lives at top-level `mcp/` inside that child repo.

For `cardhop-app`, that marketplace path stays `./plugins/cardhop-app` because the installable plugin root is the child repo root while the bundled Cardhop MCP server now lives at top-level `mcp/` inside that child repo.

The mixed shape is intentional for now. `socket` does not try to flatten those child repo packaging models into one fake uniform layout, and it does not define a second aggregate Codex plugin root above the child repos.

Current [OpenAI Codex plugin docs](https://developers.openai.com/codex/plugins/build) support Git-backed marketplace sources and the [`codex plugin marketplace add`](https://developers.openai.com/codex/plugins/build#add-a-marketplace-from-the-cli) command. That makes the Git-backed marketplace the preferred install and update path for `socket`:

```bash
codex plugin marketplace add gaelic-ghost/socket
codex plugin marketplace upgrade socket
```

Standalone child repositories that carry their own repo marketplace should use the same pattern against their own Git repository:

```bash
codex plugin marketplace add gaelic-ghost/apple-dev-skills
codex plugin marketplace add gaelic-ghost/SpeakSwiftlyServer
```

Use an explicit ref, such as `gaelic-ghost/socket@vX.Y.Z`, only when you want a pinned, reproducible install instead of the release-aligned default branch. Manual clone-and-local-marketplace instructions remain valid for development, unpublished testing, and fallback cases. They should not be the first user-facing install or update story when the Git-backed marketplace path is available.
