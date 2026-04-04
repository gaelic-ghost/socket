# Section Schema

## Core Sections

1. `# <repo-name>`
2. one-line value proposition
3. `## Table of Contents` (compact, H2 links only)
4. `## What These Agent Skills Help With`
5. `## Skill Guide (When To Use What)`
6. `## Install`
7. `## Quick Start (Vercel Skills CLI)` when Vercel `skills` CLI guidance is still documented
8. `## Install individually by Skill or Skill Pack` when individual `skills` CLI examples are documented
9. `## Update Skills` when `skills` CLI upkeep is documented
10. `## More resources for similar Skills`
11. `## Repository Layout`
12. `## Notes`
13. `## Keywords`
14. `## License`

## Plugin Maintainer Sections

1. `# <repo-name>`
2. one-line maintainer-facing value proposition
3. `## Active Skills`
4. `## Repo Purpose`
5. `## Packaging And Discovery`
6. `## Standards And Docs`
7. `## Maintainer Python Tooling`
8. `## Install`
9. `## Repository Layout`
10. `## License`

## Table of Contents Rules

- must be the first H2 section in README
- use top-level bullets only (`- [Section](#fragment)`)
- no nested bullets
- no self-link to `#table-of-contents`
- every TOC link must target an existing H2 heading
- TOC should include every H2 heading except `Table of Contents`

## Public Profile Additions

- when Codex Plugin or Claude Code plugin packaging is present in the repo, `## Install` should lead with Codex local plugin install guidance and Claude Code plugin usage guidance before secondary Vercel `skills` CLI examples
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

## Plugin Maintainer Additions

- keep the README maintainer-facing rather than converting it into the public skill-pack schema
- document canonical `skills/` authoring, plugin packaging roots, and discovery mirrors explicitly
- under `## Maintainer Python Tooling`, document `uv sync --dev`, `uv tool install ruff`, `uv tool install mypy`, and `uv run --group dev pytest`
- document Codex local plugin installs and Claude Code plugin usage before secondary Vercel `skills` CLI distribution paths
