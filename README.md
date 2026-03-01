# productivity-skills

Curated Codex skills for productivity workflows, maintenance automation, and operational hygiene.

## What These Agent Skills Help With

This repository helps users and agents run recurring maintenance tasks with consistent guardrails and predictable outputs.

## Skill Guide (When To Use What)

- `docs-alignment-maintainer`
  - Use when you need workspace-wide docs drift checks and bounded docs fixes.
  - Helps by producing deterministic Markdown/JSON findings with safe remediation options.
- `skills-readme-alignment-maintainer`
  - Use when you need profile-aware README standards maintenance across `*-skills` repos.
  - Helps by normalizing structure and command integrity without touching code files.
- `project-roadmap-manager`
  - Use when you need a canonical `ROADMAP.md` workflow for milestones and accepted plans.
  - Helps by keeping project planning state explicit and current.
- `workspace-cleanup-audit`
  - Use when you need a read-only cleanup audit across workspace repos.
  - Helps by identifying artifact buildup and cleanup priorities.
- `things-week-ahead-digest`
  - Use when you want weekly planning summaries from Things data.
  - Helps by surfacing priorities and actionable next steps.

## Quick Start (Vercel Skills CLI)

Use the Vercel `skills` CLI against this repository to install any skill directory you want to use. Or install them all conveniently with one command.

```bash
# Install your choice of skill(s) via the Vercel `skills` CLI
# Using `npx` fetches `skills` without installing it on your machine
npx skills add gaelic-ghost/productivity-skills
```

The CLI will prompt you to choose which skill(s) to install from this repo.

## Install individually by Skill

```bash

npx skills add gaelic-ghost/productivity-skills@docs-alignment-maintainer

npx skills add gaelic-ghost/productivity-skills@skills-readme-alignment-maintainer

npx skills add gaelic-ghost/productivity-skills@project-roadmap-manager

npx skills add gaelic-ghost/productivity-skills@workspace-cleanup-audit

npx skills add gaelic-ghost/productivity-skills@things-week-ahead-digest
```

## Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "workspace maintenance codex"
npx skills find "readme alignment skill"
npx skills find "productivity automation"
```

## Find Skills like these with `Find Skills` by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```bash
npx skills add vercel-labs/agent-skills -a codex
npx skills find "codex automation templates"
npx skills find "docs drift maintenance"
```

- Skills catalog: [skills.sh](https://skills.sh/)

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── docs-alignment-maintainer/
├── skills-readme-alignment-maintainer/
├── project-roadmap-manager/
├── workspace-cleanup-audit/
└── things-week-ahead-digest/
```

## Notes

- Each skill includes `references/automation-prompts.md` templates for Codex App and Codex CLI automation usage.
- `docs-alignment-maintainer` is docs-focused only; AGENTS maintenance is intentionally out-of-scope.

## Search Keywords

Codex skills, productivity automation, docs alignment, README alignment, workspace cleanup, roadmap maintenance, Things planning.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
