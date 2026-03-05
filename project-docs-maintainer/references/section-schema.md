# Section Schema

## Core Sections

1. `# <repo-name>`
2. one-line value proposition
3. `## What These Agent Skills Help With`
4. `## Skill Guide (When To Use What)`
5. `## Customization Workflow Matrix`
6. `## Quick Start (Vercel Skills CLI)`
7. `## Install individually by Skill or Skill Pack`
8. `## Update Skills`
9. `## More resources for similar Skills`
10. `## Repository Layout`
11. `## Notes`
12. `## Keywords`
13. `## License`

## Public Profile Additions

- under `## More resources for similar Skills`, require:
  - `### Find Skills like these with the \`skills\` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)`
  - `### Find Skills like these with the \`Find Skills\` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)`
  - compatibility note: the older heading variant using `Find Skills` Skill (without `Agent`) is accepted and normalized to the canonical heading above
- optional extra `###` headings are allowed only after:
  - `Then ask your Agent for help finding a skill for "" or ""`
- use current install command syntax:
  - base install: `npx skills add <owner/repo>`
  - all skills: `npx skills add <owner/repo> --all`
  - one skill: `npx skills add <owner/repo> --skill <skill-name>`
- release highlights/history (for active release repos)
- `## Keywords`
