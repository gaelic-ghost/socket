# productivity-skills

Curated productivity skills for maintenance automation and code-understanding walkthroughs.

For standards and applicability guidance, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [What These Agent Skills Help With](#what-these-agent-skills-help-with)
- [Skill Guide (When To Use What)](#skill-guide-when-to-use-what)
- [Codex Plugin Packaging](#codex-plugin-packaging)
- [Install with skills.sh / Vercel Skills CLI](#install-with-skillssh--vercel-skills-cli)
- [Update Skills](#update-skills)
- [More resources for similar Skills](#more-resources-for-similar-skills)
- [Repository Layout](#repository-layout)
- [Notes](#notes)
- [Keywords](#keywords)
- [License](#license)

## What These Agent Skills Help With

This repository packages reusable skills for project README maintenance, skills/plugin README maintenance, checklist roadmap maintenance, and code-slice walkthroughs.

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
- `explain-code-slice`
  - Use when you want a code path, flow, pipeline, request lifecycle, trace, or part of a system explained step by step.
  - Helps by starting with data shape, then walking the full slice through branches, boundaries, transformations, and outputs.

## Codex Plugin Packaging

This repository is also packaged as a Codex plugin root.

- Plugin manifest: [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json)
- Local marketplace entry: [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)

Use those files when wiring the whole repository into a Codex plugin workflow, and use the `skills` CLI commands below when you want documented standalone skill installation.

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
npx skills add gaelic-ghost/productivity-skills --skill explain-code-slice
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
- `explain-code-slice` for end-to-end code walkthroughs

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
npx skills find "project roadmap maintenance"
npx skills find "plugin readme audit"
```

### Find Skills like these with the `Find Skills` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```bash
# `Find Skills` is a part of Vercel's `agent-skills` repo
npx skills add vercel-labs/agent-skills --skill find-skills
```

Then ask your Agent for help finding a skill for project roadmap maintenance, code walkthroughs, or README auditing.

### Release highlights

- Latest release: [`v3.0.0`](https://github.com/gaelic-ghost/productivity-skills/releases/tag/v3.0.0)
- Marks the breaking transition to the `skills/` layout, split docs-maintenance skills, and the matured project README maintainer workflow.

### Leaderboard

- Skills catalog: [skills.sh](https://skills.sh/)

## Repository Layout

```text
.
├── README.md
├── AGENTS.md
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

## Notes

- Prefer the current skill names in new prompts; retired compatibility names are no longer the active guidance surface.
- The Things-focused skills now live in `../things-app/skills` rather than in this repository.

## Keywords

Codex skills, code walkthrough, slice explanation, execution flow, request lifecycle, pipeline explanation, data flow, skills README maintenance, roadmap maintenance, productivity automation.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
