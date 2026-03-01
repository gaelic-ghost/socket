# web-dev-skills

Task-focused agent skills for web development workflows.

## What These Agent Skills Help With

- Use when you want reusable, repo-local instructions for recurring web development tasks.
- Helps by packaging conventions, commands, and guardrails into composable `SKILL.md` units.
- Use when you need consistent execution across coding, docs, testing, and deployment steps.

## Skill Guide (When To Use What)

This repository is currently a bootstrap template and does not include published skills yet.

## Quick Start (Vercel Skills CLI)

```bash
npx skills add gaelic-ghost/web-dev-skills
```

## Install individually by Skill

Individual skill paths are not published in this bootstrap repository yet.

## Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "web development workflow"
npx skills find "frontend testing and linting"
npx skills find "deployment and release automation"
```

## Find Skills like these with Find Skills

Use the Find Skills catalog to discover related packages and install options:

- https://skills.sh/
- https://github.com/vercel-labs/skills
- https://github.com/vercel-labs/agent-skills

## Repository Layout

```text
.
├── README.md
└── <skill-name>/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

## Notes

- Keep each skill narrowly scoped and action-oriented.
- Prefer deterministic commands and minimal assumptions.
- Validate relative links and command syntax before publishing.

## License

No license is currently declared for this repository.

## Search Keywords

web development skills, agent skills, codex skills, frontend workflow, backend workflow, testing automation, deployment automation, documentation workflow
