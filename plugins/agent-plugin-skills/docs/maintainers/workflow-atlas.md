# Workflow Atlas

This repository exports maintainer skills for skills-export repositories.

For the maintainers' plugin-surface diagram and glossary, see [codex-plugin-install-surfaces.md](./codex-plugin-install-surfaces.md).

## Active Skill Roles

| Skill | Role | Output |
| --- | --- | --- |
| `bootstrap-skills-plugin-repo` | bootstrap or align a clean skills-export repo shape | scaffold actions, findings |
| `sync-skills-repo-guidance` | audit README, AGENTS, maintainer docs, and discovery mirrors for guidance drift | guidance findings |

## Shared Boundary Rules

- Treat `productivity-skills` as the default baseline maintainer layer for ordinary repo-doc and maintenance work.
- Use this repo only when the target repository is itself a skills-export or plugin-export surface and needs narrower packaging or discovery guidance.
- Root `skills/` is canonical.
- `.agents/skills` and `.claude/skills` are local discovery mirrors.
- No skill in this repo should teach a nested staged plugin directory for this repo.
- No skill in this repo should treat repo-local Codex plugin installs as a richer private scoping model than the marketplace-based behavior OpenAI documents.
- No skill in this repo should resurrect installer or install-validation workflows.

## Recommended Flow

1. Use `bootstrap-skills-plugin-repo` when creating or aligning a new skills-export repo.
2. Use `sync-skills-repo-guidance` when the repo shape is right but the docs and mirrors have drifted.
