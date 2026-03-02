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
- `things-mcp-reminder-wrapper`
  - Use when you need deterministic create/update reminder handling in Things via MCP.
  - Helps by normalizing relative dates, checking auth early, and preventing accidental duplicate tasks.

## Quick Start (Vercel Skills CLI)

Use the Vercel `skills` CLI against this repository to install any skill directory you want to use. Or install them all conveniently with one command.

```bash
# Install your choice of skill(s) interactively via the Vercel `skills` CLI
# Using `npx` fetches `skills` without installing it on your machine
npx skills add gaelic-ghost/productivity-skills
```

The CLI will prompt you to choose which skill(s) to install from this repo.

```bash
# Install all skills from this repo non-interactively
npx skills add gaelic-ghost/productivity-skills --all
```

## Install individually by Skill

```bash

npx skills add gaelic-ghost/productivity-skills --skill docs-alignment-maintainer

npx skills add gaelic-ghost/productivity-skills --skill skills-readme-alignment-maintainer

npx skills add gaelic-ghost/productivity-skills --skill project-roadmap-manager

npx skills add gaelic-ghost/productivity-skills --skill workspace-cleanup-audit

npx skills add gaelic-ghost/productivity-skills --skill things-week-ahead-digest

npx skills add gaelic-ghost/productivity-skills --skill things-mcp-reminder-wrapper
```

## Update Skills

```bash
# Check for available updates to installed Skills
npx skills check
# Update installed Skills
npx skills update
```

## More resources for similar Skills

### Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "workspace maintenance codex"
npx skills find "readme alignment skill"
npx skills find "productivity automation"
```

### Find Skills like these with the `Find Skills` Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```bash
# `Find Skills` is a part of Vercel's `agent-skills` repo
npx skills add vercel-labs/agent-skills --skill find-skills
```

Then ask your Agent for help finding a skill for "" or ""

### Leaderboard

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
├── things-week-ahead-digest/
└── things-mcp-reminder-wrapper/
```

## Notes

- Each skill includes `references/automation-prompts.md` templates for Codex App and Codex CLI automation usage.
- `docs-alignment-maintainer` is docs-focused only; AGENTS maintenance is intentionally out-of-scope.

## Search Keywords

Codex skills, productivity automation, docs alignment, README alignment, workspace cleanup, roadmap maintenance, Things planning, Things reminders, task deduplication.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
