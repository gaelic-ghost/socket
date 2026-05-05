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
- Root `.codex-plugin/plugin.json` points at that surface with `"skills": "./skills/"`.
- `.agents/skills` is the local discovery mirror.
- No skill in this repo should teach a nested staged plugin directory for this repo.
- No skill in this repo should treat repo-local Codex plugin installs as a richer private scoping model than the marketplace-based behavior OpenAI documents.
- User-facing plugin install and update guidance should default to Git-backed marketplace sources and official `codex plugin marketplace add` / `codex plugin marketplace upgrade` commands.
- Manual local marketplace roots and copied plugin payload directories should stay scoped to local development, unpublished testing, or fallback cases.
- No skill in this repo should resurrect installer or install-validation workflows.
- Use [codex-subagent-skill-guidance.md](./codex-subagent-skill-guidance.md) when bootstrap or sync work needs to add or audit optional Codex subagent guidance in a skills repository.
- When auditing OpenAI Codex Hooks wording, keep hooks framed as Codex runtime lifecycle scripts rather than plugin packaging, discovery mirrors, or install surfaces.

## Recommended Flow

1. Use `bootstrap-skills-plugin-repo` when creating or aligning a new skills-export repo.
2. Use `sync-skills-repo-guidance` when the repo shape is right but the docs and mirrors have drifted.
