# productivity-skills

Curated productivity skills for maintenance automation, code-understanding walkthroughs, operational hygiene, and reusable speech-output tasks. This repository supports two equally first-class installation paths: direct skill installation through the Vercel `skills` CLI / [skills.sh](https://skills.sh/) ecosystem, and bundled plugin installation in Codex through the repo-root plugin at [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).

For standards and applicability guidance, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [What These Agent Skills Help With](#what-these-agent-skills-help-with)
- [Skill Guide (When To Use What)](#skill-guide-when-to-use-what)
- [Install with skills.sh / Vercel Skills CLI](#install-with-skillssh--vercel-skills-cli)
- [Install as a Codex Plugin](#install-as-a-codex-plugin)
- [Update Skills](#update-skills)
- [More resources for similar Skills](#more-resources-for-similar-skills)
- [Repository Layout](#repository-layout)
- [Notes](#notes)
- [Keywords](#keywords)
- [License](#license)

## What These Agent Skills Help With

This repository packages reusable skills for project README maintenance, skills/plugin README maintenance, checklist roadmap maintenance, read-only workspace hygiene, code-slice walkthroughs, Things planning/reminder workflows, and profile-aware speech generation for narrated work.

The same skill set is available as either standalone installable skills or as a bundled Codex plugin, while keeping the underlying skill directories usable as normal repo-authored skills built on the open agent skills standard. Where platform-specific enhancements are useful, this repository intentionally preserves Codex/OpenAI-specific metadata and packaging surfaces instead of flattening everything down to the lowest common denominator.

## Skill Guide (When To Use What)

- `maintain-project-readme`
  - Use when an ordinary software project `README.md` needs deterministic auditing or bounded fixes for overview, motivation, setup, usage, development, or verification guidance.
  - Helps by applying a shared README schema, repo-profile detection, and README-only fixes instead of skills/plugin catalog rules.
- `maintain-project-roadmap`
  - Use when a checklist-style `ROADMAP.md` needs validation, normalization, or bounded updates.
  - Helps by keeping roadmap maintenance deterministic through explicit `check-only` and `apply` modes.
- `maintain-skills-readme`
  - Use when an agent-skills, Codex plugin, Claude plugin, or similar skills/plugin repo `README.md` needs auditing or bounded fixes.
  - Helps by enforcing specialized install, discoverability, and catalog conventions for skills/plugin repositories.
- `code-slice-explainer`
  - Use when you want a code path, flow, pipeline, request lifecycle, trace, or part of a system explained step by step.
  - Helps by starting with data shape, then walking the full slice through branches, boundaries, transformations, and outputs.
- `project-workspace-cleaner`
  - Use when a workspace needs a read-only cleanup audit.
  - Helps by ranking cleanup chores and surfacing repo-level hygiene hotspots.
- `things-reminders-manager`
  - Use when Things reminders need deterministic create or update handling.
  - Helps by applying duplicate checks and date-safety guardrails.
- `things-digest-generator`
  - Use when you want a week-ahead Things planning digest.
  - Helps by summarizing active work and generating prioritized next-step suggestions.
- `speak-with-profile`
  - Use when speech output needs reusable profiles, disclosure, and reproducible reporting.
  - Helps by routing narrated notes, spoken drafts, audio summaries, and accessibility reads through one profile-aware workflow.

## Install with skills.sh / Vercel Skills CLI

Use the Vercel `skills` CLI when you want one or more standalone skills from this repository.

```bash
# Install from this repository with the interactive picker
npx skills add gaelic-ghost/productivity-skills
```

```bash
# Install every skill from this repository
npx skills add gaelic-ghost/productivity-skills --all
```

```bash
# Install one specific skill
npx skills add gaelic-ghost/productivity-skills --skill maintain-project-readme
```

```bash
# Install a selected skill pack in one command
npx skills add gaelic-ghost/productivity-skills \
  --skill maintain-project-readme \
  --skill maintain-project-roadmap \
  --skill maintain-skills-readme
```

Current active skill names:

- `maintain-project-readme` for ordinary software-project `README.md` maintenance
- `maintain-skills-readme` for skills/plugin repository `README.md` maintenance
- `maintain-project-roadmap` for checklist-style `ROADMAP.md` maintenance
- `code-slice-explainer` for end-to-end code walkthroughs
- `project-workspace-cleaner` for read-only workspace cleanup audits
- `things-reminders-manager` for deterministic Things reminder create/update workflows
- `things-digest-generator` for week-ahead Things planning digests
- `speak-with-profile` for profile-aware speech output workflows

## Install as a Codex Plugin

Use the Codex plugin path when you want the whole repository bundled as one installable Codex package.

This repository is organized around the Codex plugin model:

- Skills remain the authoring unit.
- Plugins are the bundled Codex distribution unit.
- Active repo-authored skills live under [`skills/`](./skills/).
- The repo root plugin manifest lives at [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- The repo-scoped Codex marketplace file lives at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json).

To install this plugin in Codex:

1. Keep the repository checked out locally.
2. Keep the repo marketplace file at `.agents/plugins/marketplace.json`; Codex reads repo-scoped marketplaces from that path.
3. Restart Codex after adding or updating the marketplace file.
4. Open the Codex plugin directory in the app, or run `codex` and then `/plugins` in the CLI, and select this repo marketplace.
5. Install the `productivity-skills` plugin from that marketplace.

The marketplace file is the Codex catalog surface, and `.codex-plugin/plugin.json` is the plugin package manifest. They are maintained together in this repository.

For the current OpenAI plugin packaging model, see [Build plugins](https://developers.openai.com/codex/plugins/build) and [Plugins](https://developers.openai.com/codex/plugins/).

## Update Skills

```bash
npx skills check
npx skills update
```

## More resources for similar Skills

### Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "skills readme maintenance"
npx skills find "code slice walkthrough"
npx skills find "workspace cleanup automation"
npx skills find "things productivity automation"
npx skills find "text to speech workflow"
```

### Find Skills like these with the `Find Skills` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```bash
# `Find Skills` is a part of Vercel's `agent-skills` repo
npx skills add vercel-labs/agent-skills --skill find-skills
```

Then ask your Agent for help finding a skill for "" or ""

### Release highlights

- Latest release: [`v3.0.0`](https://github.com/gaelic-ghost/productivity-skills/releases/tag/v3.0.0)
- Marks the breaking transition to the plugin-ready `skills/` layout, split docs-maintenance skills, and the matured project README maintainer workflow.

### Leaderboard

- Skills catalog: [skills.sh](https://skills.sh/)

## Repository Layout

```text
.
├── README.md
├── AGENTS.md
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .codex-plugin/
├── skills/
│   ├── code-slice-explainer/
│   ├── maintain-project-readme/
│   ├── maintain-project-roadmap/
│   ├── maintain-skills-readme/
│   ├── project-workspace-cleaner/
│   ├── speak-with-profile/
│   ├── things-digest-generator/
│   └── things-reminders-manager/
├── docs/
│   └── maintainers/
├── ROADMAP.md
└── pyproject.toml
```

## Notes

- Both standalone skills installation and Codex plugin installation are first-class supported paths in this repository.
- Install and use skills individually when you want narrow workflow selection; use the Codex plugin path when you want the bundled package.
- Active repo-authored skills live under `skills/`, and the repository root acts as the plugin root for Codex plugin packaging.
- The repo marketplace file at `.agents/plugins/marketplace.json` is the Codex discovery/catalog surface for the repo-root plugin.
- The standard skill core remains portable, and Codex/OpenAI-specific enhancements stay layered on where they improve install UX, metadata quality, or invocation ergonomics.
- Prefer the current skill names in new prompts; retired compatibility names are no longer the active guidance surface.
- `speak-with-profile` is the canonical speech workflow in this repository; prefer it over direct speech calls when profile resolution or manifest reporting matters.

## Keywords

Codex skills, code walkthrough, slice explanation, execution flow, request lifecycle, pipeline explanation, data flow, skills README maintenance, roadmap maintenance, workspace cleanup, Things reminders, Things digest, productivity automation, text-to-speech, audio summaries, narrated notes.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
