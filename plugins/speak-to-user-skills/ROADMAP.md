# Project Roadmap

## Vision

- Keep `speak-to-user-skills` as a small, honest placeholder repository until the first real speech-facing skill is ready to ship.

## Product Principles

- Keep the repository minimal until there is a real exported skill surface.
- Keep placeholder docs honest about what the repository does and does not ship.
- Add richer packaging, docs, and validation guidance only after real skill content exists.

## Milestone Progress

- [ ] Milestone 1: first exported speech skill
- [ ] Milestone 2: repository docs and validation expansion
- [ ] Milestone 3: long-term home decision

## Milestone 1: first exported speech skill

Scope:

- Author the first real speech-facing skill for Codex.

Tickets:

- [ ] Add the first maintained skill under the canonical exported surface.
- [ ] Update root docs to describe the real shipped behavior instead of the placeholder state.

Exit criteria:

- [ ] The repository ships at least one real speech-facing skill.

## Milestone 2: repository docs and validation expansion

Scope:

- Add the supporting docs and validation surface that become worthwhile once real skill content exists.

Tickets:

- [ ] Add richer repository docs once the exported skill surface is real.
- [ ] Add the minimum validation or smoke coverage needed for the shipped skill surface.

Exit criteria:

- [ ] Public docs and validation describe the same live exported surface.

## Milestone 3: long-term home decision

Scope:

- Decide whether this repository should remain standalone or stay primarily subtree-managed through `socket`.

Tickets:

- [ ] Decide whether the standalone repository remains the canonical home after the first real shipped skill.
- [ ] Align repository docs with that chosen long-term home.

Exit criteria:

- [ ] The repository’s long-term role relative to `socket` is explicit.
