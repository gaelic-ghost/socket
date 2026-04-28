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

- Milestone 2: subtree workflow hardening - Completed
- Milestone 3: release and sync discipline - Completed

## Milestone 2: subtree workflow hardening

### Status

Completed

### Scope

- [x] Tighten the documented subtree add, pull, and push workflows without changing the child-repo ownership model.
- [x] Define `standard` and `subtrees` release modes so umbrella releases follow the `maintain-project-repo` protected-main shape with subtree-specific accounting.

### Tickets

- [x] Review subtree workflow docs against the current import and publish path.
- [x] Add a documented audit pass for detecting stale child packaging paths in the root marketplace.
- [x] Add a superproject-level checklist for removing public child repos that should no longer be imported.

### Exit Criteria

- [x] Root maintainer workflow docs describe the actual subtree sync path without stale or duplicate guidance.

Completed Milestone 2 by documenting the current subtree add, pull, and push paths, preserving the child-specific `apple-dev-skills` push-capable and `SpeakSwiftlyServer` pull-only rules, and adding explicit marketplace-audit and public-child-removal checklists to the maintainer workflow.

## Milestone 3: release and sync discipline

### Status

Completed

### Scope

- [x] Keep root release and synchronization guidance explicit when superproject-level changes ship.

### Tickets

- [x] Document the expected root release and sync rhythm once the current subtree migration experiment stabilizes.
- [x] Keep the root docs aligned with the current child packaging model during coordinated release-prep passes.
- [x] Make coordinated semantic-version bumps across `socket` and the maintained child manifests explicit instead of relying on ad hoc release notes.

### Exit Criteria

- [x] Superproject release guidance is explicit enough that root changes can be shipped without improvising process each time.
- [x] Root docs still describe the live packaging and versioning model after a coordinated release-prep pass.

Completed Milestone 3 by aligning the release-mode docs, subtree sync rules, shared-version workflow, and roadmap backlog cleanup around the current mixed monorepo model.

## Backlog Candidates

No active backlog candidates are currently tracked here. Add new candidates only when they represent real future work that is not already covered by the maintainer docs or milestone history.

## History

- Completed the subtree workflow and release-discipline milestones by adding the root marketplace audit pass, the public child plugin removal checklist, and a tighter roadmap state that no longer carries stale backlog items as active work.
- Prepared the `v6.1.0` minor release by adding the `maintain-project-api` productivity skill and keeping the monorepo-owned child docs, tests, and shared version surfaces aligned.
- Added explicit `standard` and `subtrees` release-mode guidance, including the pull-only `SpeakSwiftlyServer` rule for `socket` subtree sync.
- Published `apple-dev-skills` `v6.0.11` after adding direct regression coverage for SwiftPM-generated `.swiftpm/xcode/package.xcworkspace` classification and synced the released child state back into `socket`.
- Prepared the shared `v6.0.11` patch release after fixing `productivity-skills:maintain-project-repo` release-helper regressions for initial PR check discovery and approval-only review handling.
- Added the placeholder `plugins/spotify` child repository, wired it into the root marketplace, and kept the superproject docs honest about that new monorepo-owned plugin surface.
- Converted the former standalone `cardhop-mcp` checkout into the monorepo-owned `plugins/cardhop-app` child, added first-pass Codex plugin metadata plus a bundled MCP config, and recorded the new child as a normal `socket` marketplace entry.
- Retired the remaining `things-app` subtree-era wording from the root maintainer docs, removed the now-redundant local `things-app` and `things-app-mcp` sibling checkouts after verification, and prepared the `v0.11.1` plus `things-app v0.1.3` patch bump.
- Synced the `SpeakSwiftlyServer` subtree through the newer `v4.2.x` plugin and embedded live-speech updates, confirmed the root marketplace path still stayed valid, and kept the superproject release trail explicit with the `v0.11.0` bump.
- Added a root version-alignment script, switched `python-skills` to the monorepo-owned workflow, and documented the shared-version policy for the maintained manifest surfaces.
- Completed Milestone 1, `superproject docs and marketplace alignment`, by bringing the root README, AGENTS guidance, roadmap shape, and marketplace-path explanation back into alignment with the live mixed-monorepo model.
- Added the first root `ROADMAP.md` and established the checklist-style planning format for the superproject.
- Added a root marketplace-validation script and GitHub Actions workflow so `socket` now checks packaged plugin paths and manifest alignment instead of leaving that audit entirely manual.
- Added root `CONTRIBUTING.md`, `ACCESSIBILITY.md`, `LICENSE`, and `NOTICE` so the superproject's contributor, accessibility, and legal surfaces are explicit at the repository root.
- Collapsed the older subtree migration and plugin-alignment planning docs into this roadmap history plus the still-live root maintainer references once those plans had become historical rather than active operating guidance.
