# agent-plugin-skills

Installable maintainer skills for skills-export and plugin-export repositories.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [License](#license)
- [Active Skills](#active-skills)

## Overview

### Status

This repository is active and currently ships two maintainer workflows.

### What This Project Is

This repository is the canonical home for maintainer skills that help Gale keep skills-export and plugin-export repositories aligned on packaging, discovery, and documentation boundaries.

It ships source-first Codex plugin packaging at [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json), keeps root [`skills/`](./skills/) as the authored surface, and keeps deeper maintainer explanation under [`docs/maintainers/`](./docs/maintainers/).

### Motivation

It exists so repo-maintenance guidance for skills and plugin repositories can live in one focused place instead of being repeated across unrelated repos.

## Quick Start

Install the plugin through a Git-backed Codex marketplace when you want these skills available in your Codex environment. The preferred user path is to add Gale's `socket` marketplace, let Codex track that Git source, and then install or enable `agent-plugin-skills` from the plugin directory:

```bash
codex plugin marketplace add gaelic-ghost/socket --ref main
codex plugin marketplace upgrade socket
```

In the `socket` superproject, the repo marketplace is [`.agents/plugins/marketplace.json`](../../.agents/plugins/marketplace.json), and its `agent-plugin-skills` entry points at `./plugins/agent-plugin-skills`.

Manual local marketplace roots are for local development, unpublished testing, or fallback cases. User-facing install and update examples should prefer `codex plugin marketplace add` and `codex plugin marketplace upgrade` against the Git-backed marketplace source.

If you are inspecting or changing the repository itself, go to [Development](#development).

## Usage

Use this repository when the target project is itself a skills-export or plugin-export repository and the job is about repo structure, packaging guidance, discovery mirrors, or cross-surface documentation alignment.

For general-purpose repository docs and maintainer workflow cleanup, start with `productivity-skills` first and reach for `agent-plugin-skills` only when the repository shape is narrow enough to need plugin-specific maintainer guidance.

When this repo discusses Codex packaging, it stays explicit about the current documented model:

- plugins have a root manifest at `.codex-plugin/plugin.json`
- only `plugin.json` belongs in `.codex-plugin/`
- `skills/` stays at the plugin root
- the plugin manifest points to bundled skills with `"skills": "./skills/"`
- repo-visible Codex plugins come from marketplace catalogs, and OpenAI does not document a richer repo-private scoping model beyond that
- ordinary user installs should use Git-backed marketplace sources and the official marketplace add/upgrade commands

When this repo discusses Codex subagents, it follows OpenAI's current `subagents` terminology: subagent use is explicit user-triggered delegation for bounded parallel work, not automatic behavior that every skill should perform.

## Development

### Setup

Sync the local maintainer environment before changing the Python-backed audit tooling or tests:

```bash
uv sync --dev
```

Keep the Python maintainer baseline repo-local. When this repo or a target repo expects Python checks, declare the required dev dependencies in `pyproject.toml` instead of assuming contributors already installed standalone tools globally. The normal baseline is `pytest`, `ruff`, and `mypy` when those checks are part of the shipped workflow.

### Workflow

Keep root [`skills/`](./skills/) canonical, keep maintainer docs under [`docs/maintainers/`](./docs/maintainers/), and keep plugin metadata in [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).

When you update a skill here, align the nearby docs and tests in the same pass. Keep discovery mirrors, plugin packaging, marketplace sources, marketplace catalogs, plugin root payloads, cache paths, and enabled-state wording separate instead of collapsing them into one vague install story.

For optional Codex subagent wording in target skills repos, use [`docs/maintainers/codex-subagent-skill-guidance.md`](./docs/maintainers/codex-subagent-skill-guidance.md).

Contributor workflow and review expectations live in [CONTRIBUTING.md](./CONTRIBUTING.md).

### Validation

Run the repo-local tests before landing changes that touch skill behavior, docs-backed automation, or plugin metadata:

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run mypy .
```

## Repo Structure

```text
.
├── .codex-plugin/
│   └── plugin.json
├── AGENTS.md
├── CONTRIBUTING.md
├── README.md
├── ROADMAP.md
├── docs/
│   └── maintainers/
├── skills/
│   ├── bootstrap-skills-plugin-repo/
│   └── sync-skills-repo-guidance/
├── pyproject.toml
└── uv.lock
```

## Release Notes

Use Git history and GitHub releases to track shipped changes to the maintainer-skill surface.

## License

See [LICENSE](./LICENSE).

## Active Skills

- `bootstrap-skills-plugin-repo`: bootstrap or align a skills-export repository around root `skills/`, discovery mirrors, and maintainer guidance
- `sync-skills-repo-guidance`: audit guidance drift across README, AGENTS, maintainer docs, and discovery mirrors in an existing skills-export repository
