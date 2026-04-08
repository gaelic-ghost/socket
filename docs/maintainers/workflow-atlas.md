# Workflow Atlas

This repository exports maintainer skills for skills-export repositories.

## Active Skill Roles

| Skill | Role | Output |
| --- | --- | --- |
| `maintain-plugin-repo` | repo-level audit and bounded remediation entrypoint | grouped findings, owner assignments, bounded fixes |
| `maintain-plugin-docs` | README, ROADMAP, and cross-doc maintenance | docs findings, fixes applied |
| `bootstrap-skills-plugin-repo` | bootstrap or align a clean skills-export repo shape | scaffold actions, findings |
| `sync-skills-repo-guidance` | reconcile README, AGENTS, ROADMAP, maintainer docs, and discovery mirrors | guidance findings |

## Shared Boundary Rules

- Root `skills/` is canonical.
- `.agents/skills` and `.claude/skills` are local discovery mirrors.
- No skill in this repo should teach a nested plugin directory for this repo.
- No skill in this repo should treat repo-local Codex plugin installs as proper private scoping.
- No skill in this repo should resurrect installer or install-validation workflows.

## Recommended Flow

1. Use `maintain-plugin-repo` when the repo feels drifted overall.
2. Use `maintain-plugin-docs` for bounded README or ROADMAP work.
3. Use `bootstrap-skills-plugin-repo` when creating or aligning a new skills-export repo.
4. Use `sync-skills-repo-guidance` when the repo shape is right but the docs and mirrors have drifted.
