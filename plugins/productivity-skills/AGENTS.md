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
- Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch.
- Do not commit dependency declarations, lockfiles, scripts, docs, examples, generated project files, or CI config that point at machine-local paths such as `/Users/...`, `~/...`, `../...`, local worktrees, or private checkout paths.
- Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly. If local integration is needed, keep it uncommitted or convert it to a tagged release, branch, or registry dependency before sharing.
- Keep workflow scale tied to the user's actual request. Do not turn ordinary questions, investigations, doc edits, or small local fixes into branch, PR, CI, release, tag, or cleanup workflows unless the user explicitly asks for that lifecycle step or a closer repo-local rule requires it for the exact task.
- Treat `maintain-project-repo` release choreography as release-only guidance. It does not override the narrower document-maintenance skills that say not to auto-commit, auto-push, or open a PR.
- When a commit is made on a branch with a reachable remote, push that branch as the normal checkpoint unless the user asked for local-only work or the branch is intentionally incomplete. Do not treat that push as permission to open a PR, watch CI, merge, tag, or release.
- Treat repo-sync verification and local-branch accounting as hard gates before cleanup or "done" claims.
- When work in this repository is performed from the `socket` superproject or is expected to ship back through `socket`, verify whether `socket` now needs an explicit sync step and either complete it or say plainly why no sync is required.
- Before saying work is merged, preserved, or safe to delete, verify the exact commit reachability in the repo and remote being discussed.
- Before deleting local branches, remote branches, worktrees, or rescue refs, enumerate every local branch not contained by `main` and account for each one explicitly as preserved elsewhere, intentionally in progress, newly archived, newly merged, or safe to delete.
- Do not treat branch cleanup as routine hygiene that can happen before that accounting pass.
