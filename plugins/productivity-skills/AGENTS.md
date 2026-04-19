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
- Treat repo-sync verification and local-branch accounting as hard gates before cleanup or "done" claims.
- When work in this repository is performed from the `socket` superproject or is expected to ship back through `socket`, verify whether `socket` now needs an explicit sync step and either complete it or say plainly why no sync is required.
- Before saying work is merged, preserved, or safe to delete, verify the exact commit reachability in the repo and remote being discussed.
- Before deleting local branches, remote branches, worktrees, or rescue refs, enumerate every local branch not contained by `main` and account for each one explicitly as preserved elsewhere, intentionally in progress, newly archived, newly merged, or safe to delete.
- Do not treat branch cleanup as routine hygiene that can happen before that accounting pass.
