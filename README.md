# productivity-skills

Canonical productivity skills with a plugin-first packaging layout for Codex and Claude Code.

For maintainer guidance, standards references, and cross-ecosystem packaging policy, see [AGENTS.md](./AGENTS.md).

## Active Skills

- `maintain-project-readme`
  - Use when an ordinary software project `README.md` needs deterministic auditing or bounded fixes for overview, motivation, setup, usage, development, or verification guidance.
- `maintain-project-roadmap`
  - Use when a checklist-style `ROADMAP.md` needs validation, normalization, or bounded updates.
- `maintain-skills-readme`
  - Use when an agent-skills, Codex plugin, Claude plugin, or similar skills/plugin repo `README.md` needs auditing or bounded fixes.
- `explain-code-slice`
  - Use when you want a code path, flow, pipeline, request lifecycle, trace, or part of a system explained step by step.

Maintainer-facing workflow maps, audit procedure, and source-of-truth rules live in [docs/maintainers/workflow-atlas.md](./docs/maintainers/workflow-atlas.md) and [docs/maintainers/reality-audit.md](./docs/maintainers/reality-audit.md).

## Packaging and Delegation

This repository now uses a plugin-first packaging layout while keeping root [`skills/`](./skills/) as the canonical workflow-authoring surface.

Shared guidance across both ecosystems:

- keep reusable workflow behavior in root `skills/`
- keep deterministic helper logic skill-scoped so both Codex and Claude can rely on it
- treat plugin manifests, hooks, and marketplace wiring as install-surface metadata, not as the workflow source of truth

Current packaging scaffolding lives under:

- [`plugins/productivity-skills/.codex-plugin/plugin.json`](./plugins/productivity-skills/.codex-plugin/plugin.json)
- [`plugins/productivity-skills/.claude-plugin/plugin.json`](./plugins/productivity-skills/.claude-plugin/plugin.json)
- [`plugins/productivity-skills/hooks/hooks.json`](./plugins/productivity-skills/hooks/hooks.json)
- [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)

The plugin scaffold is intentionally conservative:

- Codex-compatible common denominator first
- Claude-only extras layered on top under `plugins/productivity-skills/.claude-plugin`, `hooks/`, and `bin/`
- no essential workflow behavior should depend on plugin-only extras

Helpful docs for this packaging model:

- OpenAI Codex Skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI Codex customization: [developers.openai.com/codex/concepts/customization](https://developers.openai.com/codex/concepts/customization/)
- OpenAI Codex plugins overview: [developers.openai.com/codex/plugins](https://developers.openai.com/codex/plugins)
- OpenAI Codex plugin authoring: [developers.openai.com/codex/plugins/build](https://developers.openai.com/codex/plugins/build)
- Claude Code Skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- Claude Code Plugins: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)

## Maintainer Python Tooling

This repository standardizes maintainer-side Python tooling around `uv`.

```bash
uv sync --dev
uv run --group dev pytest
```

Use the skill entrypoints directly when you need focused validation, for example:

```bash
uv run --group dev python /Users/galew/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/explain-code-slice
```

## Install

Plugin-first installation and local marketplace wiring now target [`plugins/productivity-skills/`](./plugins/productivity-skills). Standalone skill installation through the Vercel `skills` CLI remains supported and is the documented direct-install path today.

Install one skill:

```bash
npx skills add gaelic-ghost/productivity-skills --skill explain-code-slice
```

Install all active skills:

```bash
npx skills add gaelic-ghost/productivity-skills --all
```

Common starting points:

- README work:
  `npx skills add gaelic-ghost/productivity-skills --skill maintain-project-readme`
- roadmap work:
  `npx skills add gaelic-ghost/productivity-skills --skill maintain-project-roadmap`
- skills/plugin README work:
  `npx skills add gaelic-ghost/productivity-skills --skill maintain-skills-readme`
- code walkthrough work:
  `npx skills add gaelic-ghost/productivity-skills --skill explain-code-slice`

## Planned Expansion

The next planned repo-surface expansion adds two skills focused on maintaining skills repositories and plugin packaging guidance:

- `sync-skills-repo-guidance`
- `bootstrap-skills-plugin-repo`

See [ROADMAP.md](./ROADMAP.md) for the milestone plan.

## Repository Layout

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── README.md
├── AGENTS.md
├── plugins/
│   └── productivity-skills/
│       ├── .codex-plugin/
│       ├── .claude-plugin/
│       ├── assets/
│       ├── bin/
│       ├── hooks/
│       └── skills/
├── skills/
│   ├── explain-code-slice/
│   ├── maintain-project-readme/
│   ├── maintain-project-roadmap/
│   └── maintain-skills-readme/
├── docs/
│   └── maintainers/
├── ROADMAP.md
└── pyproject.toml
```

The plugin directories are packaging scaffolds. The canonical workflow content still lives under root `skills/`.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
