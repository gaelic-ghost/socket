# socket

Mixed-model monorepo for Gale's Codex plugin and skills repositories.

![Codex plugin directory filtered to the Socket marketplace, showing Productivity Skills featured above installable Socket child plugins.](./docs/media/codex-plugin-directory-socket-productivity-skills.png)

The screenshot shows the Codex plugin directory filtered to the `Socket` marketplace. This is the user-facing catalog surface that `socket` provides: adding the marketplace exposes the child plugins, and users still choose which entries to install or enable.

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

`socket` is the superproject Gale uses to keep several Codex plugin and skills repositories under one Git root while OpenAI's documented Codex plugin system still lacks a better shared-parent scoping model. It owns the repo-root Codex marketplace at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json), the monorepo-owned child directories under [`plugins/`](./plugins/), the remaining subtree sync path for `apple-dev-skills`, and the root maintainer docs that explain how the mixed model works.

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

For ordinary user installation, prefer the official Git-backed marketplace path. Add the `socket` marketplace from Git when you want one Codex marketplace that exposes Gale's plugin and skill collection, including companion plugins such as `productivity-skills`, `apple-dev-skills`, `agent-plugin-skills`, `python-skills`, and the other child plugins listed below. Update that marketplace through Codex when the marketplace or child plugin entries change:

```bash
codex plugin marketplace add gaelic-ghost/socket
codex plugin marketplace upgrade socket
```

After the marketplace is added or upgraded, restart Codex, open the plugin directory in the Codex GUI, choose the `Socket` marketplace, and install or enable the child plugins you want. This is the preferred way to get sibling or companion skills from one catalog instead of adding each child repository as a separate marketplace. Manual local marketplace roots are useful for development, unpublished testing, and fallback work, but they are not the default user install or update path.

If you previously used the older copied-plugin or personal-local-marketplace install path, run the legacy cleanup helper after the Git-backed marketplace works:

```bash
uv run scripts/cleanup_legacy_socket_installs.py
uv run scripts/cleanup_legacy_socket_installs.py --apply
```

The first command is a dry run. The `--apply` mode backs up affected files and copied plugin directories before removing only known legacy `socket` install artifacts. It does not delete Codex's installed plugin cache under `~/.codex/plugins/cache/`.

## Usage

Use `socket` when the task is about the superproject layer:

- root marketplace wiring
- mixed monorepo policy
- subtree sync flow for `apple-dev-skills`
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

Only `apple-dev-skills` still uses a subtree sync workflow. `SpeakSwiftlyServer` is exposed through a Git-backed marketplace entry, and `python-skills` is maintained as a normal monorepo-owned child directory. `socket` itself does not ship a root plugin; the repo marketplace is the root Codex-facing catalog here.

### Workflow

Treat Gale's local `socket` checkout as the normal day-to-day checkout on `main`. Work in the monorepo copy first, and use the relevant directory under [`plugins/`](./plugins/) for child-repository changes unless the task is explicitly about the root marketplace or root maintainer docs. Reach for a feature branch or a dedicated worktree only when the change needs extra isolation.

Keep root docs and marketplace wiring in sync with packaging changes in the same pass. For monorepo-owned child directories, edit the relevant directory under [`plugins/`](./plugins/) directly and commit in `socket`. For `apple-dev-skills`, keep subtree sync operations explicit and isolated. For Speak Swiftly plugin payload changes, work in the standalone `SpeakSwiftlyServer` checkout; the Socket marketplace points at that Git-backed plugin source and does not carry a copied payload or source mirror here.

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

Use [`docs/maintainers/release-modes.md`](./docs/maintainers/release-modes.md) for the full release flow. `standard` is the normal `socket` release mode; `subtrees` is the standard mode plus explicit pull/push accounting for subtree-managed children such as `apple-dev-skills`.

### Validation

The current root validation surface is structural:

- keep [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json) valid JSON
- verify that every local entry's `source.path` matches the real child surface that the child repo treats as installable
- verify that every local packaged plugin path still exposes a matching `.codex-plugin/plugin.json`
- verify that every Git-backed entry uses the documented root-plugin or subdirectory source shape
- review child-repo docs when plugin packaging paths move
- run child-repo-specific validation from the relevant child repo when the change is really about that child repo

Run the root validator locally with:

```bash
uv run scripts/validate_socket_metadata.py
```

To audit or remove old copied personal plugin payloads after moving to the Git-backed marketplace path, run:

```bash
uv run scripts/cleanup_legacy_socket_installs.py
```

Add `--apply` only after reviewing the dry-run output. The helper backs up the personal marketplace file and copied plugin directories under `~/.codex/backups/socket-legacy-install-cleanup/<timestamp>/` before changing anything. It reports stale non-`socket` plugin enablement entries in `~/.codex/config.toml`, but it does not rewrite that config file.

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
│   ├── media/
│   │   └── codex-plugin-directory-socket-productivity-skills.png
│   └── maintainers/
│       ├── plugin-install-testing.md
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
- [`docs/maintainers/plugin-install-testing.md`](./docs/maintainers/plugin-install-testing.md) for isolated local and Git-backed marketplace install tests that leave personal production installs untouched
- [`docs/maintainers/automation-suitability.md`](./docs/maintainers/automation-suitability.md) for the cross-repo automation fit of productivity skills, Apple sync skills, `codex exec`, Codex GUI automations, and external Agents SDK services
- [`docs/maintainers/release-modes.md`](./docs/maintainers/release-modes.md) for the `standard` and `subtrees` release modes
- [`docs/media/`](./docs/media/) for README screenshots and other root documentation media assets

## Plugin Surfaces

Treat `socket` as the canonical home for the monorepo-owned child directories, the subtree host for `apple-dev-skills`, and the Git-backed catalog host for Speak Swiftly.

- `agent-plugin-skills`, `cardhop-app`, `dotnet-skills`, `productivity-skills`, `rust-skills`, `spotify`, `swiftasb-skills`, `things-app`, and `web-dev-skills` are monorepo-owned here.
- `apple-dev-skills` preserves an explicit subtree sync path.
- `SpeakSwiftlyServer` is no longer imported under `plugins/`; the Socket catalog installs it from the Git-backed standalone repository.
- `python-skills` is monorepo-owned here with no separate upstream GitHub release target.
- Child repos may expose plugin packaging from their own repo roots whether they are monorepo-owned here, subtree-managed, or exposed through a Git-backed marketplace entry.
- `apple-dev-skills` packages from its child-repo root at `./plugins/apple-dev-skills`, and its Codex plugin manifest registers Xcode's built-in MCP bridge through a root `.mcp.json`.
- `swiftasb-skills` packages from its child-repo root at `./plugins/swiftasb-skills`, and ships companion guidance for explaining SwiftASB, choosing integration shapes, diagnosing integration failures, and building SwiftUI, AppKit, and Swift package integrations on top of the SwiftASB package.
- `apple-dev-skills` and `SpeakSwiftlyServer` carry their own repo-local `.agents/plugins/marketplace.json` files so Codex can track either repository as a Git-backed standalone marketplace without cloning `socket`.
- `SpeakSwiftlyServer` owns the canonical `speak-swiftly` plugin payload. The Socket marketplace exposes that payload by Git-backed reference so users can enable `Speak Swiftly` from the Socket catalog without `socket` carrying a second copied plugin directory.
- `things-app` packages from its child-repo root at `./plugins/things-app`, and its bundled MCP server lives directly under that child repo's top-level `mcp/` directory.
- `cardhop-app` packages from its child-repo root at `./plugins/cardhop-app`, and its bundled MCP server lives directly under that child repo's top-level `mcp/` directory.

## Marketplace Shape

The repo-root marketplace lives at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json).

That marketplace points at the plugin root for each cataloged child repository. Entries with real shipped skills, MCP servers, hooks, or apps are installable. Placeholder entries stay visible as planned surfaces but use `policy.installation: NOT_AVAILABLE` until they ship actual content:

- Installable: `./plugins/agent-plugin-skills`
- Installable: `./plugins/apple-dev-skills`
- Installable: `./plugins/cardhop-app`
- Installable: `./plugins/productivity-skills`
- Installable: `gaelic-ghost/SpeakSwiftlyServer` for `speak-swiftly`, displayed as `Speak Swiftly`
- Installable: `./plugins/python-skills`
- Installable: `./plugins/swiftasb-skills`
- Installable: `./plugins/things-app`
- Not available yet: `./plugins/dotnet-skills`
- Not available yet: `./plugins/rust-skills`
- Not available yet: `./plugins/spotify`
- Not available yet: `./plugins/web-dev-skills`

For `things-app`, that marketplace path stays `./plugins/things-app` because the installable plugin root is the child repo root even though the bundled server now lives at top-level `mcp/` inside that child repo.

For `cardhop-app`, that marketplace path stays `./plugins/cardhop-app` because the installable plugin root is the child repo root while the bundled Cardhop MCP server now lives at top-level `mcp/` inside that child repo.

For Speak Swiftly, the marketplace points at the canonical `SpeakSwiftlyServer` repository as a Git-backed plugin source named `speak-swiftly`, with the UI display name `Speak Swiftly`. That keeps the standalone `SpeakSwiftlyServer` marketplace fully functional while avoiding two plugin payload copies that can drift.

The mixed shape is intentional for now. `socket` does not try to flatten those child repo packaging models into one fake uniform layout, and it does not define a second aggregate Codex plugin root above the child repos.

Current [OpenAI Codex plugin docs](https://developers.openai.com/codex/plugins/build) support Git-backed marketplace sources and the [`codex plugin marketplace add`](https://developers.openai.com/codex/plugins/build#add-a-marketplace-from-the-cli) command. That makes the Git-backed marketplace the preferred install and update path for `socket`:

```bash
codex plugin marketplace add gaelic-ghost/socket
codex plugin marketplace upgrade socket
```

Use the `socket` marketplace when you want one catalog for Gale's plugin set. From that marketplace, users can install or enable individual available entries such as `apple-dev-skills`, `productivity-skills`, `agent-plugin-skills`, `python-skills`, `swiftasb-skills`, `things-app`, and `cardhop-app`. This is especially useful for workflows that need companion skills, such as Apple bootstrap or guidance-sync workflows that rely on both `apple-dev-skills` and `productivity-skills`.

When both the Socket marketplace and the standalone SpeakSwiftlyServer marketplace are configured, prefer enabling `speak-swiftly` from the Socket catalog and disabling duplicate standalone enablement. The Speak Swiftly doctor should detect duplicate installs or enablement and offer a repair path that keeps the Socket entry active.

Standalone child repositories that carry their own repo marketplace should use the same pattern against their own Git repository:

```bash
codex plugin marketplace add gaelic-ghost/apple-dev-skills
codex plugin marketplace add gaelic-ghost/SpeakSwiftlyServer
```

Use an explicit ref, such as `gaelic-ghost/socket@vX.Y.Z`, only when you want a pinned, reproducible install instead of the release-aligned default branch. Manual clone-and-local-marketplace instructions remain valid for development, unpublished testing, and fallback cases. They should not be the first user-facing install or update story when the Git-backed marketplace path is available.
