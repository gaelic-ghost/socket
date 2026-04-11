# productivity-skills

Broadly useful productivity skills plus durable base template skills that downstream language-, stack-, and repo-specific plugins can adapt.

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

This plugin is active and maintained as the shared productivity-skills base layer.

### What This Project Is

This repository bundles broadly useful global-install skills and the canonical general-purpose versions of workflow families that later specialize in adjacent plugins. It keeps root [`skills/`](./skills/) as the authored source of truth, with thin Codex and Claude marketplace metadata pointing back at that same skill surface.

It currently ships these active skills:

- [`explain-code-slice`](./skills/explain-code-slice/SKILL.md)
- [`maintain-project-readme`](./skills/maintain-project-readme/SKILL.md)
- [`maintain-project-agents`](./skills/maintain-project-agents/SKILL.md)
- [`maintain-project-contributing`](./skills/maintain-project-contributing/SKILL.md)
- [`maintain-project-roadmap`](./skills/maintain-project-roadmap/SKILL.md)
- [`maintain-project-repo`](./skills/maintain-project-repo/SKILL.md)

Agent-skills and plugin-maintainer workflows now live in the sibling [`agent-plugin-skills`](../agent-plugin-skills) repository instead of here.

### Motivation

This repository exists to keep the durable superclass layer coherent on its own. The goal is to preserve strong general-purpose defaults for common workflow families while leaving room for downstream plugins to make tighter language-, framework-, or repo-specific assumptions when those assumptions materially improve the workflow.

## Quick Start

Install one skill:

```bash
npx skills add gaelic-ghost/productivity-skills --skill explain-code-slice
```

Install all active skills from this plugin:

```bash
npx skills add gaelic-ghost/productivity-skills --all
```

If you are looking for agent-skills or plugin-repository maintenance workflows instead, start with the sibling plugin:

```bash
npx skills add gaelic-ghost/agent-plugin-skills --skill maintain-skills-readme
```

## Usage

Use this plugin when you want globally useful workflow help rather than project-specific specialization.

Common starting points:

- Code walkthroughs:

```bash
npx skills add gaelic-ghost/productivity-skills --skill explain-code-slice
```

- README maintenance for ordinary software projects:

```bash
npx skills add gaelic-ghost/productivity-skills --skill maintain-project-readme
```

- Project-local `AGENTS.md` maintenance:

```bash
npx skills add gaelic-ghost/productivity-skills --skill maintain-project-agents
```

- `CONTRIBUTING.md` maintenance:

```bash
npx skills add gaelic-ghost/productivity-skills --skill maintain-project-contributing
```

- Checklist-style roadmap maintenance:

```bash
npx skills add gaelic-ghost/productivity-skills --skill maintain-project-roadmap
```

- Reusable repo-maintenance toolkit work:

```bash
npx skills add gaelic-ghost/productivity-skills --skill maintain-project-repo
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
