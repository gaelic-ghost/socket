# productivity-skills

Curated Codex skills for productivity workflows, maintenance automation, code-understanding walkthroughs, operational hygiene, and reusable speech-output tasks.

For standards and applicability guidance, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [What These Agent Skills Help With](#what-these-agent-skills-help-with)
- [Skill Guide (When To Use What)](#skill-guide-when-to-use-what)
- [Quick Start (Vercel Skills CLI)](#quick-start-vercel-skills-cli)
- [Install individually by Skill or Skill Pack](#install-individually-by-skill-or-skill-pack)
- [Update Skills](#update-skills)
- [More resources for similar Skills](#more-resources-for-similar-skills)
- [Repository Layout](#repository-layout)
- [Notes](#notes)
- [Keywords](#keywords)
- [License](#license)

## What These Agent Skills Help With

This repository packages reusable Codex skills for canonical docs maintenance, read-only workspace hygiene, code-slice walkthroughs, Things planning/reminder workflows, and profile-aware speech generation for narrated work.

## Skill Guide (When To Use What)

- `project-docs-maintainer`
  - Use when a `*-skills` repo needs README maintenance or checklist-style roadmap validation.
  - Helps by providing one canonical doc-maintenance entrypoint with explicit modes.
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

## Quick Start (Vercel Skills CLI)

Use the Vercel `skills` CLI to install from this repository.

```bash
# Install from this repository (interactive picker)
npx skills add gaelic-ghost/productivity-skills
```

## Upgrade Note for v2.0.0

`v2.0.0` is a breaking release.

- Removed skill surfaces:
  - `project-skills-orchestrator-agent`
  - `project-roadmap-maintainer`
- Use direct standalone skill installs instead of orchestrator-first flows.
- For roadmap maintenance, use `project-docs-maintainer` with `mode=roadmap_maintenance`.

Canonical installs:

```bash
npx skills add gaelic-ghost/productivity-skills --skill project-docs-maintainer
npx skills add gaelic-ghost/productivity-skills --skill code-slice-explainer
npx skills add gaelic-ghost/productivity-skills --skill project-workspace-cleaner
npx skills add gaelic-ghost/productivity-skills --skill things-reminders-manager
npx skills add gaelic-ghost/productivity-skills --skill things-digest-generator
npx skills add gaelic-ghost/productivity-skills --skill speak-with-profile
```

Install all skills from this repository:

```bash
npx skills add gaelic-ghost/productivity-skills --all
```

## Install individually by Skill or Skill Pack

```bash
npx skills add gaelic-ghost/productivity-skills --skill project-docs-maintainer
npx skills add gaelic-ghost/productivity-skills --skill code-slice-explainer
npx skills add gaelic-ghost/productivity-skills --skill project-workspace-cleaner
npx skills add gaelic-ghost/productivity-skills --skill things-reminders-manager
npx skills add gaelic-ghost/productivity-skills --skill things-digest-generator
npx skills add gaelic-ghost/productivity-skills --skill speak-with-profile
```

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

- Latest release: [`v2.2.0`](https://github.com/gaelic-ghost/productivity-skills/releases/tag/v2.2.0)
- Includes the new `code-slice-explainer` skill plus widened trigger coverage for natural-language walkthrough requests.

### Leaderboard

- Skills catalog: [skills.sh](https://skills.sh/)

## Repository Layout

```text
.
├── README.md
├── AGENTS.md
├── code-slice-explainer/
├── docs/
│   └── maintainers/
├── project-docs-maintainer/
├── project-workspace-cleaner/
├── speak-with-profile/
├── things-digest-generator/
└── things-reminders-manager/
```

## Notes

- Install and use skills individually; do not assume access to repo-level maintainer docs.
- Prefer canonical skills over compatibility shims for new prompts.
- `speak-with-profile` is the canonical speech workflow in this repository; prefer it over direct speech calls when profile resolution or manifest reporting matters.

## Keywords

Codex skills, code walkthrough, slice explanation, execution flow, request lifecycle, pipeline explanation, data flow, skills README maintenance, roadmap maintenance, workspace cleanup, Things reminders, Things digest, productivity automation, text-to-speech, audio summaries, narrated notes.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
