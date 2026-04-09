# private-skills

Private Codex skills repository for non-public workflows and experiments.

## What These Agent Skills Help With

This repository is intended for personal or internal-use skills that are not published for broad public reuse.

## Skill Guide (When To Use What)

- `github-repo-defaults`
  - Use when creating a new GitHub remote/repository and you want your default repository settings applied consistently.
  - Helps by standardizing visibility, merge settings, description generation, and initial topics.

- `resume-repo-line-items`
  - Use when you need structured resume-style line item generation from repository work.
  - Helps by turning repository activity into concise, usable resume bullets.

## Quick Start (Vercel Skills CLI)

If you have access to this private repository:

```bash
npx skills add gaelic-ghost/private-skills -a codex
```

```bash
npx skills add gaelic-ghost/private-skills -a codex -g
```

## Install individually by Skill

```bash
npx skills add gaelic-ghost/private-skills@resume-repo-line-items -a codex
```

```bash
npx skills add gaelic-ghost/private-skills@github-repo-defaults -a codex
```

## Repository Layout

```text
.
├── README.md
├── ROADMAP.md
├── docs/
├── github-repo-defaults/
└── resume-repo-line-items/
```

## Notes

- Keep this repo private; do not copy sensitive content into public repos.
- Keep README and skill directory names synchronized.

## License

This is a private repository and does not currently define an open-source license.

## Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "xcode mcp"
npx skills find "swift package workflow"
npx skills find "dash docset apple docs"
```
