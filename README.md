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
- `bootstrap-skills-plugin-repo`
  - Use when creating or structurally aligning a skills repository to the shared plugin-first layout with maintainer docs and POSIX discovery mirrors.
- `sync-skills-repo-guidance`
  - Use when an existing skills repository needs repo-wide guidance reconciliation across docs, AGENTS policy, symlink mirrors, and plugin metadata.
- `explain-code-slice`
  - Use when you want a code path, flow, pipeline, request lifecycle, trace, or part of a system explained step by step.

Maintainer-facing workflow maps, audit procedure, and source-of-truth rules live in [docs/maintainers/workflow-atlas.md](./docs/maintainers/workflow-atlas.md) and [docs/maintainers/reality-audit.md](./docs/maintainers/reality-audit.md).

## Packaging and Delegation

This repository now uses a plugin-first packaging layout while keeping root [`skills/`](./skills/) as the canonical workflow-authoring surface. In repo-policy shorthand, keep root `skills/` as the canonical authoring surface.

Shared guidance across both ecosystems:

- keep reusable workflow behavior in root `skills/`
- keep deterministic helper logic skill-scoped so both Codex and Claude can rely on it
- treat plugin manifests, hooks, and marketplace wiring as install-surface metadata, not as the workflow source of truth
- use POSIX symlink mirrors for local Codex and Claude project discovery on macOS and Linux:
  - `.agents/skills -> ../skills`
  - `.claude/skills -> ../skills`
  - `plugins/productivity-skills/skills -> ../../skills`

Current packaging scaffolding lives under:

- [`plugins/productivity-skills/.codex-plugin/plugin.json`](./plugins/productivity-skills/.codex-plugin/plugin.json)
- [`plugins/productivity-skills/.claude-plugin/plugin.json`](./plugins/productivity-skills/.claude-plugin/plugin.json)
- [`plugins/productivity-skills/skills`](./plugins/productivity-skills/skills)
- [`plugins/productivity-skills/hooks/hooks.json`](./plugins/productivity-skills/hooks/hooks.json)
- [`.agents/skills`](./.agents/skills)
- [`.claude/skills`](./.claude/skills)
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

Standalone skill installation is handled through the Vercel `skills` CLI against root [`skills/`](./skills). Plugin packaging and local marketplace wiring target [`plugins/productivity-skills/`](./plugins/productivity-skills). For local project discovery on macOS and Linux, this repo also exposes `.agents/skills` and `.claude/skills` as symlink mirrors into root `skills/`.

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
- repo bootstrap or structural alignment:
  `npx skills add gaelic-ghost/productivity-skills --skill bootstrap-skills-plugin-repo`
- repo-wide guidance sync:
  `npx skills add gaelic-ghost/productivity-skills --skill sync-skills-repo-guidance`
- code walkthrough work:
  `npx skills add gaelic-ghost/productivity-skills --skill explain-code-slice`

Use the narrower skills when the task is README-only or roadmap-only. Use the repo bootstrap or sync skills when the task spans structure, manifests, `AGENTS.md`, maintainer docs, or cross-surface guidance drift.

## Repository Layout

```text
.
├── .agents/
│   ├── skills -> ../skills
│   └── plugins/
│       └── marketplace.json
├── .claude/
│   └── skills -> ../skills
├── README.md
├── AGENTS.md
├── plugins/
│   └── productivity-skills/
│       ├── .codex-plugin/
│       ├── .claude-plugin/
│       ├── assets/
│       ├── bin/
│       ├── hooks/
│       └── skills -> ../../skills
├── skills/
│   ├── bootstrap-skills-plugin-repo/
│   ├── explain-code-slice/
│   ├── maintain-project-readme/
│   ├── maintain-project-roadmap/
│   ├── maintain-skills-readme/
│   └── sync-skills-repo-guidance/
├── docs/
│   └── maintainers/
├── ROADMAP.md
└── pyproject.toml
```

The canonical workflow content still lives under root `skills/`. The discovery mirrors are local POSIX symlinks for macOS and Linux development, including WSL 2 when Windows is involved.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
