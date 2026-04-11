# productivity-skills

Useful productivity skills, and durable template skills for downstream lang/stack-specific repos to adapt.

For maintainer guidance, standards references, and cross-ecosystem packaging policy, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Repo Structure](#repo-structure)
- [Release Notes](#release-notes)
- [License](#license)

## Overview

### Status

This plugin is active and maintained.

### What This Project Is

This repo houses some general productivity skills I've built, as well as the templates for my lang/stack-specific skills in other repos.

It currently ships these active skills:

- [`explain-code-slice`](./skills/explain-code-slice/SKILL.md)
- [`maintain-project-readme`](./skills/maintain-project-readme/SKILL.md)
- [`maintain-project-agents`](./skills/maintain-project-agents/SKILL.md)
- [`maintain-project-contributing`](./skills/maintain-project-contributing/SKILL.md)
- [`maintain-project-roadmap`](./skills/maintain-project-roadmap/SKILL.md)
- [`maintain-project-repo`](./skills/maintain-project-repo/SKILL.md)

Agent-skills and plugin-maintainer workflows now live in the sibling [`agent-plugin-skills`](../agent-plugin-skills) repository instead of here.

### Motivation

I like automating busywork, and staying focused on what I'm building, simple as that.

## Quick Start

Install one (or more) skills interactively:

```bash
npx skills add gaelic-ghost/productivity-skills
```

Install as a Codex Plugin:

Install as a Claude Code Plugin:


## Usage

Use this plugin when you want globally useful workflow help rather than project-specific specialization.

Common starting points:

- Global productivity skills:
```bash
npx skills add gaelic-ghost/productivity-skills --skill explain-code-slice
```

- Adaptable template skills:

```bash
npx skills add gaelic-ghost/productivity-skills --skill maintain-project-readme maintain-project-roadmap
```

Discovery and install surfaces in this repository are intentionally thin. Root [`skills/`](./skills/) remains the canonical authored surface, while local discovery mirrors and marketplace catalogs expose that same skill tree directly:

- [`.agents/skills`](./.agents/skills)
- [`.claude/skills`](./.claude/skills)
- [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
- [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json)

Helpful ecosystem docs:

- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [OpenAI Codex customization](https://developers.openai.com/codex/concepts/customization/)
- [OpenAI Codex plugins overview](https://developers.openai.com/codex/plugins)
- [OpenAI Codex plugin authoring](https://developers.openai.com/codex/plugins/build)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)

## Development

### Setup

This repository standardizes maintainer-side Python tooling around `uv`.

```bash
uv sync --dev
uv tool install ruff
uv tool install mypy
uv run --group dev pytest
```

For maintainer workflow guidance, source-of-truth rules, and cross-ecosystem packaging policy, use:

- [AGENTS.md](./AGENTS.md)
- [docs/maintainers/workflow-atlas.md](./docs/maintainers/workflow-atlas.md)
- [docs/maintainers/reality-audit.md](./docs/maintainers/reality-audit.md)

### Workflow

Keep root [`skills/`](./skills/) as the canonical workflow-authoring surface. Treat `.agents/skills` and `.claude/skills` as discovery mirrors, and keep the repo-local marketplace catalogs aligned directly to the same source tree instead of staging nested packaged plugin copies.

When a workflow becomes meaningfully stack-, language-, or repo-specific, prefer moving that stronger specialization into a dedicated adjacent plugin instead of weakening the shared productivity-skills baseline.

### Validation

Run focused maintainer checks before shipping changes:

```bash
uv run --group dev pytest
```

When validating a single skill, use its deterministic helper entrypoints directly. For example:

```bash
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/explain-code-slice
```

## Repo Structure

```text
.
├── .agents/
│   ├── skills -> ../skills
│   └── plugins/
│       └── marketplace.json
├── .claude/
│   └── skills -> ../skills
├── .claude-plugin/
│   └── marketplace.json
├── AGENTS.md
├── README.md
├── ROADMAP.md
├── docs/
│   └── maintainers/
├── skills/
│   ├── explain-code-slice/
│   ├── maintain-project-agents/
│   ├── maintain-project-contributing/
│   ├── maintain-project-readme/
│   ├── maintain-project-roadmap/
│   └── maintain-project-repo/
└── pyproject.toml
```

## Release Notes

Track notable shipped changes through Git history and GitHub releases when cuts are made, and keep in-flight maintainer planning reflected in [ROADMAP.md](./ROADMAP.md) when milestone work changes materially.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
