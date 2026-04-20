# Project Roadmap

## Vision

- Keep `spotify` as a small, honest placeholder repository until the first real Spotify-focused Codex workflow is ready to ship.

## Product Principles

- Keep the repository minimal until there is a real exported Spotify surface.
- Keep placeholder docs honest about what the repository does and does not ship.
- Add richer packaging, docs, and validation guidance only after real workflow content exists.

## Milestone Progress

- [ ] Milestone 1: first exported Spotify workflow
- [ ] Milestone 2: repository docs and validation expansion
- [ ] Milestone 3: long-term home decision

## Milestone 1: first exported Spotify workflow

Scope:

- Author the first real Spotify-focused Codex workflow for this repository.

Tickets:

- [ ] Add the first maintained Spotify skill, app, or MCP-backed workflow under the canonical exported surface.
- [ ] Update root docs to describe the real shipped behavior instead of the placeholder state.

Exit criteria:

- [ ] The repository ships at least one real Spotify-focused workflow.

## Milestone 2: repository docs and validation expansion

Scope:

- Add the supporting docs and validation surface that become worthwhile once real workflow content exists.

Tickets:

- [ ] Add richer repository docs once the exported surface is real.
- [ ] Add the minimum validation or smoke coverage needed for the shipped Spotify surface.

Exit criteria:

- [ ] Public docs and validation describe the same live exported surface.

## Milestone 3: long-term home decision

Scope:

- Decide whether this repository should remain monorepo-owned inside `socket` or eventually move into its own standalone repository.

Tickets:

- [ ] Decide whether `socket` remains the canonical home after the first real shipped workflow.
- [ ] Align repository docs with that chosen long-term home.

Exit criteria:

- [ ] The repository's long-term role relative to `socket` is explicit.
