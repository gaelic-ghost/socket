# AGENTS.md

## Repository Role

- This repository is the canonical home for broadly useful general-purpose productivity workflows.
- Keep this repo focused on reusable baseline workflow families whose best version does not depend on strong stack- or repo-specific assumptions.
- Prefer dedicated plugins for workflows that become materially better once they depend on narrower project assumptions.

## Repo-specific Rules

- Root `skills/` is the canonical authored surface.
- Treat standalone skill installation as the primary distribution story, with plugin packaging and marketplace metadata as thin additive discovery layers.
- Keep documentation-maintenance skills split by document type instead of collapsing README, AGENTS, CONTRIBUTING, and ROADMAP maintenance into one oversized workflow.
- Keep stack-specific or repo-family-specific maintainer skills in the dedicated repos that own them. Historical note: `bootstrap-skills-plugin-repo` and `sync-skills-repo-guidance` moved out to `agent-plugin-skills` and should stay there.
