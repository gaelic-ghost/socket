# AGENTS.md

This file is the Productivity Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `productivity-skills` is the canonical home for broadly useful general-purpose productivity workflows.
- Keep this repo focused on reusable baseline workflow families whose best version does not depend on strong stack- or repo-specific assumptions.
- Root [`skills/`](./skills/) is the canonical authored surface.
- Treat plugin packaging and marketplace metadata as thin discovery layers around the authored skill surface.

## Local Rules

- Keep documentation-maintenance skills split by document type instead of collapsing README, AGENTS, CONTRIBUTING, ROADMAP, and other document maintenance into one oversized workflow.
- Keep stack-specific or repo-family-specific maintainer skills in the dedicated repos that own them.
- `bootstrap-skills-plugin-repo` and `sync-skills-repo-guidance` moved to `agent-plugin-skills` and should stay there.
- Treat `maintain-project-repo` release choreography as release-only guidance; it does not override narrower document-maintenance skills that forbid auto-commit, auto-push, or PR creation.

## Validation

```bash
uv run pytest
```
