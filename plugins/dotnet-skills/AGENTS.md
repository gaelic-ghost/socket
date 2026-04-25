# AGENTS.md

## Repository Role

- This repository is the standalone placeholder source for future .NET-focused Codex skills.
- Keep the repo intentionally minimal until the first real skill lands.

## Repo-specific Rules

- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) is the required plugin root today.
- Do not add extra packaging layers, repo-local install machinery, or broad maintainer automation before the repo ships real skill content.
- Prefer adding actual skill content before expanding docs or workflow complexity.
- Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch.
- Do not commit dependency declarations, lockfiles, scripts, docs, examples, generated project files, or CI config that point at machine-local paths such as `/Users/...`, `~/...`, `../...`, local worktrees, or private checkout paths.
- Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly. If local integration is needed, keep it uncommitted or convert it to a tagged release, branch, or registry dependency before sharing.
- Treat repo-sync verification and local-branch accounting as hard gates before cleanup or "done" claims.
- When work in this repository is performed from the `socket` superproject or is expected to ship back through `socket`, verify whether `socket` now needs an explicit sync step and either complete it or say plainly why no sync is required.
- Before saying work is merged, preserved, or safe to delete, verify the exact commit reachability in the repo and remote being discussed.
- Before deleting local branches, remote branches, worktrees, or rescue refs, enumerate every local branch not contained by `main` and account for each one explicitly as preserved elsewhere, intentionally in progress, newly archived, newly merged, or safe to delete.
- Do not treat branch cleanup as routine hygiene that can happen before that accounting pass.
