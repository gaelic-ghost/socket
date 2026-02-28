# productivity-skills

Curated Codex skills focused on productivity workflows, intended for sharing and installation via skills tooling.

## How To Add (Skills CLI)

```bash
npx @vercel/skills add gaelic-ghost/productivity-skills
```

```bash
npx skills add gaelic-ghost/productivity-skills
```

CLI flags from the [`skills` package docs](https://www.npmjs.com/package/skills):

- `-a, --agent <agents...>`: target specific agents (recommended here: `-a codex`)
- `-g, --global`: install globally instead of project-local

Examples:

```bash
# Project-local install for Codex
npx skills add gaelic-ghost/productivity-skills -a codex

# Global install for Codex
npx skills add gaelic-ghost/productivity-skills -a codex -g
```

## Included skills

- `docs-alignment-maintainer`
- `skills-readme-alignment-maintainer`
- `project-roadmap-manager`
- `workspace-cleanup-audit`
- `things-week-ahead-digest`
- `talktomepy-tts`

## Customization guides

Most skill directories include a `README.md` with personalization points, common tuning profiles, example Codex prompts, and validation checklists.

- [`project-roadmap-manager/README.md`](./project-roadmap-manager/README.md)
- [`workspace-cleanup-audit/README.md`](./workspace-cleanup-audit/README.md)
- [`things-week-ahead-digest/README.md`](./things-week-ahead-digest/README.md)
- [`talktomepy-tts/README.md`](./talktomepy-tts/README.md)

## Automation prompt templates

Each skill now includes `references/automation-prompts.md` with:
- Codex App automation prompt templates
- Codex CLI (`codex exec`) automation prompt templates
- Suitability ratings, placeholders, guardrails, and customization points

- [`docs-alignment-maintainer/references/automation-prompts.md`](./docs-alignment-maintainer/references/automation-prompts.md)
- [`skills-readme-alignment-maintainer/references/automation-prompts.md`](./skills-readme-alignment-maintainer/references/automation-prompts.md)
- [`project-roadmap-manager/references/automation-prompts.md`](./project-roadmap-manager/references/automation-prompts.md)
- [`workspace-cleanup-audit/references/automation-prompts.md`](./workspace-cleanup-audit/references/automation-prompts.md)
- [`things-week-ahead-digest/references/automation-prompts.md`](./things-week-ahead-digest/references/automation-prompts.md)
- [`talktomepy-tts/references/automation-prompts.md`](./talktomepy-tts/references/automation-prompts.md)

## Source and curation

All skills were copied from `~/.codex/skills` using git-tracked files only.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
