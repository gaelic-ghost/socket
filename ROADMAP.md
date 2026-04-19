# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 2: subtree workflow hardening](#milestone-2-subtree-workflow-hardening)
- [Milestone 3: release and sync discipline](#milestone-3-release-and-sync-discipline)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Keep `socket` as the honest superproject layer for Gale's public Codex plugin and skills ecosystem, with subtree imports, root marketplace wiring, and cross-repo maintainer guidance kept consistent.

## Product Principles

- Keep the superproject focused on subtree coordination, root marketplace wiring, and cross-repo maintainer guidance.
- Keep child-repository ownership boundaries explicit instead of flattening repo-local behavior into `socket`.
- Keep public imported plugin surfaces and root marketplace wiring aligned in the same pass.

## Milestone Progress

- Milestone 2: subtree workflow hardening - Planned
- Milestone 3: release and sync discipline - In Progress

## Milestone 2: subtree workflow hardening

### Status

In Progress

### Scope

- [ ] Tighten the documented subtree add, pull, and push workflows without changing the child-repo ownership model.

### Tickets

- [ ] Review subtree workflow docs against the current import and publish path.

### Exit Criteria

- [ ] Root maintainer workflow docs describe the actual subtree sync path without stale or duplicate guidance.

## Milestone 3: release and sync discipline

### Status

Planned

### Scope

- [ ] Keep root release and synchronization guidance explicit when superproject-level changes ship.

### Tickets

- [ ] Document the expected root release and sync rhythm once the current subtree migration experiment stabilizes.
- [ ] Keep the root docs aligned with the current child packaging model during coordinated release-prep passes.
- [ ] Make coordinated minor or patch bumps across `socket` and subtree-managed child repos explicit instead of relying on ad hoc release notes.

### Exit Criteria

- [ ] Superproject release guidance is explicit enough that root changes can be shipped without improvising process each time.
- [ ] Root docs still describe the live packaging and versioning model after a coordinated release-prep pass.

## Backlog Candidates

- [ ] Add a documented audit pass for detecting stale child packaging paths in the root marketplace.
- [ ] Add a superproject-level checklist for removing public child repos that should no longer be imported.

## History

- Completed Milestone 1, `superproject docs and marketplace alignment`, by bringing the root README, AGENTS guidance, roadmap shape, and marketplace-path explanation back into alignment with the live mixed-monorepo model.
- Added the first root `ROADMAP.md` and established the checklist-style planning format for the superproject.
- Added a root marketplace-validation script and GitHub Actions workflow so `socket` now checks packaged plugin paths and manifest alignment instead of leaving that audit entirely manual.
- Added root `CONTRIBUTING.md`, `ACCESSIBILITY.md`, `LICENSE`, and `NOTICE` so the superproject's contributor, accessibility, and legal surfaces are explicit at the repository root.
- Collapsed the older subtree migration and plugin-alignment planning docs into this roadmap history plus the still-live root maintainer references once those plans had become historical rather than active operating guidance.
