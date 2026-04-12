# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 1: superproject docs and marketplace alignment](#milestone-1-superproject-docs-and-marketplace-alignment)
- [Milestone 2: subtree workflow hardening](#milestone-2-subtree-workflow-hardening)
- [Milestone 3: release and sync discipline](#milestone-3-release-and-sync-discipline)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Keep `socket` as the honest superproject layer for Gale's public Codex plugin and skills ecosystem, with subtree imports, root marketplace wiring, and cross-repo maintainer guidance kept consistent.

## Product principles

- Keep the superproject focused on subtree coordination, root marketplace wiring, and cross-repo maintainer guidance.
- Keep child-repository ownership boundaries explicit instead of flattening repo-local behavior into `socket`.
- Keep public imported plugin surfaces and root marketplace wiring aligned in the same pass.

## Milestone Progress

- Milestone 1: superproject docs and marketplace alignment - In Progress
- Milestone 2: subtree workflow hardening - Planned
- Milestone 3: release and sync discipline - Planned

## Milestone 1: superproject docs and marketplace alignment

### Status

In Progress

### Scope

- [x] Normalize the root superproject README and roadmap surfaces to the current shared documentation standards.
- [ ] Keep root maintainer docs and repo-root marketplace wiring aligned with the real packaged child plugin surfaces.

### Tickets

- [x] Align the maintained `README.md` and `ROADMAP.md` files in this repo to one consistent shared schema.
- [ ] Re-check root maintainer docs after any subtree packaging-path change.

### Exit criteria

- [ ] Root docs describe the actual superproject layer clearly and match the current root marketplace wiring.
- [ ] The superproject no longer has missing or obviously inconsistent top-level planning surfaces.

## Milestone 2: subtree workflow hardening

### Status

Planned

### Scope

- [ ] Tighten the documented subtree add, pull, and push workflows without changing the child-repo ownership model.

### Tickets

- [ ] Review subtree workflow docs against the current import and publish path.

### Exit criteria

- [ ] Root maintainer workflow docs describe the actual subtree sync path without stale or duplicate guidance.

## Milestone 3: release and sync discipline

### Status

Planned

### Scope

- [ ] Keep root release and synchronization guidance explicit when superproject-level changes ship.

### Tickets

- [ ] Document the expected root release and sync rhythm once the current subtree migration experiment stabilizes.

### Exit criteria

- [ ] Superproject release guidance is explicit enough that root changes can be shipped without improvising process each time.

## Backlog Candidates

- [ ] Add a documented audit pass for detecting stale child packaging paths in the root marketplace.
- [ ] Add a superproject-level checklist for removing public child repos that should no longer be imported.

## History

- Added the first root `ROADMAP.md` and aligned it to the checklist-standard format.
