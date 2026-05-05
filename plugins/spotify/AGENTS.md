# AGENTS.md

This file is the Spotify child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `spotify` is a monorepo-owned placeholder source for future Spotify-focused Codex workflows.
- Keep the repo intentionally minimal until the first real workflow lands.
- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) is the required plugin root today.

## Local Rules

- Do not add extra packaging layers, repo-local install machinery, or broad maintainer automation before real workflow content exists.
- Prefer adding actual Spotify workflow content before expanding docs or workflow complexity.
- When this repository changes the root Socket marketplace or root docs, update those root surfaces in the same pass.
