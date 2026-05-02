# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 2: subtree workflow hardening](#milestone-2-subtree-workflow-hardening)
- [Milestone 3: release and sync discipline](#milestone-3-release-and-sync-discipline)
- [Milestone 4: Speak Swiftly plugin catalog split](#milestone-4-speak-swiftly-plugin-catalog-split)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Keep `socket` as the honest superproject layer for Gale's public Codex plugin and skills ecosystem, with subtree imports, root marketplace wiring, and cross-repo maintainer guidance kept consistent.

## Product Principles

- Keep the superproject focused on subtree coordination, root marketplace wiring, and cross-repo maintainer guidance.
- Keep child-repository ownership boundaries explicit instead of flattening repo-local behavior into `socket`.
- Keep public imported plugin surfaces and root marketplace wiring aligned in the same pass.
- Keep user-facing plugin install and update docs on the official Git-backed marketplace path.

## Milestone Progress

- Milestone 2: subtree workflow hardening - Completed
- Milestone 3: release and sync discipline - Completed
- Milestone 4: Speak Swiftly plugin catalog split - Planned

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

## Milestone 4: Speak Swiftly plugin catalog split

### Status

In Progress

### Scope

- [x] Keep the canonical Codex plugin payload in the standalone `SpeakSwiftlyServer` repository so `.codex-plugin/plugin.json`, `.mcp.json`, `hooks/`, `skills/`, user guidance, and doctor scripts have one source of truth.
- [x] Rename the canonical plugin identity to `speak-swiftly` while keeping the display name `Speak Swiftly`.
- [x] Update the root marketplace so the public Speak Swiftly entry is listed as `speak-swiftly` from the `gaelic-ghost/SpeakSwiftlyServer` Git-backed plugin source instead of the local `./plugins/SpeakSwiftlyServer` subtree mirror.
- [ ] Keep `plugins/SpeakSwiftlyServer/` as a pull-only subtree mirror of the standalone Swift package only for source, release, and superproject accounting while that mirror remains useful.
- [x] Update root README, plugin-packaging strategy, subtree workflow guidance, and child-facing docs so users understand the split: Codex users can install `Speak Swiftly` from either the `socket` marketplace or the standalone `SpeakSwiftlyServer` marketplace, while app embedders use the Swift package directly.

### Tickets

- [x] Update `SpeakSwiftlyServer`'s plugin manifest and repo-local marketplace from `speak-swiftly-server` to `speak-swiftly`, with `interface.displayName` remaining `Speak Swiftly`.
- [x] Update `socket` marketplace validation so Git-backed remote plugin entries are allowed and checked for required metadata without requiring a local packaged plugin directory.
- [x] Change the `socket` marketplace entry from local `./plugins/SpeakSwiftlyServer` to the canonical `gaelic-ghost/SpeakSwiftlyServer` plugin source. Because the plugin root is the repository root, use the Codex marketplace source shape for a Git-backed root plugin rather than a `git-subdir` entry.
- [x] Adapt MCP registration and hooks in `SpeakSwiftlyServer` so paths stay `./`-relative to the plugin root and still target the installed local service at `127.0.0.1:7337`.
- [x] Update the hook doctor so it detects legacy `speak-swiftly-server` installs, duplicate installs from both marketplaces, plugin-managed hook state, live service reachability, and expected voice profile.
- [ ] Add doctor repair mode that prefers the `speak-swiftly@socket` install when both the `socket` marketplace and standalone `SpeakSwiftlyServer` marketplace are present, and disables or removes the duplicate standalone enablement only after reporting the intended change.
- [x] Add migration notes for users who installed `speak-swiftly-server` from either marketplace, including how to enable `speak-swiftly` from `socket` and when the old entry is safe to disable or remove.
- [x] Document isolated repo-scope install testing in `docs/maintainers/plugin-install-testing.md` so local checkout tests do not mutate Gale's personal production Codex installs.
- [ ] After this branch lands, run the Git-backed Socket marketplace install/upgrade test with a temporary `CODEX_HOME` and confirm the cached Socket catalog shows `Speak Swiftly` from the canonical `SpeakSwiftlyServer` source.

### Exit Criteria

- [x] The `socket` marketplace exposes `speak-swiftly` as a Git-backed reference to the canonical `SpeakSwiftlyServer` plugin payload instead of a second copied plugin directory.
- [x] `SpeakSwiftlyServer` remains the source of truth for the plugin payload, Swift package, executable, LaunchAgent, embedded API, HTTP/MCP implementation, and release notes.
- [x] User-facing docs no longer recommend installing the full `SpeakSwiftlyServer` subtree mirror from `socket` as the default Codex plugin path.
- [ ] `Speak Swiftly` can be installed or enabled from either the Git-backed `gaelic-ghost/socket` marketplace or the standalone `gaelic-ghost/SpeakSwiftlyServer` marketplace.
- [ ] The doctor confirms hook, MCP, runtime, and voice-profile health, detects duplicate marketplace enablement, and can repair duplicates with preference for `speak-swiftly@socket`.
- [x] The old `speak-swiftly-server` plugin id is either migrated away, marked transitional with a documented sunset path, or intentionally retained with a clear reason.

Verified against `gaelic-ghost/SpeakSwiftlyServer` `v4.5.0`: the released repository root plugin manifest declares `name: speak-swiftly`, version `2.2.0`, `interface.displayName: Speak Swiftly`, `mcpServers: ./.mcp.json`, `hooks: ./hooks/hooks.json`, and `skills: ./skills/`; its standalone marketplace entry also exposes `speak-swiftly` from `./`. Local checkout install/remove tests for both repositories passed with temporary `CODEX_HOME` directories, leaving the test marketplaces removed. The Git-backed standalone SpeakSwiftlyServer marketplace add/upgrade test passed from isolated state; the Git-backed Socket test still needs to run after this branch lands because the current `gaelic-ghost/socket` default branch predates the new `speak-swiftly` entry.

## Backlog Candidates

No active backlog candidates are currently tracked here. Add new candidates only when they represent real future work that is not already covered by the maintainer docs or milestone history.

## History

- Added root `docs/media` screenshot assets and README media guidance so the Codex plugin-directory catalog surface is visible without weakening text-first documentation.
- Planned the `Speak Swiftly` plugin catalog split so the Socket marketplace can expose the canonical `SpeakSwiftlyServer` plugin payload by Git-backed reference instead of carrying a second copied plugin directory.
- Added coordinated OpenAI Codex Hooks guidance across `agent-plugin-skills` and `productivity-skills`, with future `maintain-project-hooks` work tracked in the productivity roadmap.
- Updated `socket` and plugin guidance so ordinary user installs and updates default to Git-backed Codex marketplace sources and official marketplace add/upgrade commands.
- Added coordinated Codex subagent guidance across `agent-plugin-skills` and `productivity-skills`, grounding skill wording in OpenAI's current explicit-trigger `subagents` model while keeping the root docs clear about why the pass belongs in `socket`.
- Completed the subtree workflow and release-discipline milestones by adding the root marketplace audit pass, the public child plugin removal checklist, and a tighter roadmap state that no longer carries stale backlog items as active work.
- Prepared the `v6.1.0` minor release by adding the `maintain-project-api` productivity skill and keeping the monorepo-owned child docs, tests, and shared version surfaces aligned.
- Added explicit `standard` and `subtrees` release-mode guidance, including the pull-only `SpeakSwiftlyServer` rule for `socket` subtree sync.
- Published `apple-dev-skills` `v6.0.11` after adding direct regression coverage for SwiftPM-generated `.swiftpm/xcode/package.xcworkspace` classification and synced the released child state back into `socket`.
- Prepared the shared `v6.0.11` patch release after fixing `productivity-skills:maintain-project-repo` release-helper regressions for initial PR check discovery and approval-only review handling.
- Added the placeholder `plugins/spotify` child repository, wired it into the root marketplace, and kept the superproject docs honest about that new monorepo-owned plugin surface.
- Converted the former standalone `cardhop-mcp` checkout into the monorepo-owned `plugins/cardhop-app` child, added first-pass Codex plugin metadata plus a bundled MCP config, and recorded the new child as a normal `socket` marketplace entry.
- Retired the remaining `things-app` subtree-era wording from the root maintainer docs, removed the now-redundant local `things-app` and `things-app-mcp` sibling checkouts after verification, and prepared the `v0.11.1` plus `things-app v0.1.3` patch bump.
- Synced the `SpeakSwiftlyServer` subtree through the newer `v4.2.x` plugin and embedded live-speech updates, confirmed the root marketplace path still stayed valid, and kept the superproject release trail explicit with the `v0.11.0` bump.
- Re-checked the root packaging strategy against current OpenAI Codex plugin docs, added standalone repo-marketplace coverage for `apple-dev-skills`, normalized `SpeakSwiftlyServer`'s child marketplace path, and documented that the subtree-managed child plugins can be installed from their own clones without using `socket`.
- Added a root version-alignment script, switched `python-skills` to the monorepo-owned workflow, and documented the shared-version policy for the maintained manifest surfaces.
- Completed Milestone 1, `superproject docs and marketplace alignment`, by bringing the root README, AGENTS guidance, roadmap shape, and marketplace-path explanation back into alignment with the live mixed-monorepo model.
- Added the first root `ROADMAP.md` and established the checklist-style planning format for the superproject.
- Added a root marketplace-validation script and GitHub Actions workflow so `socket` now checks packaged plugin paths and manifest alignment instead of leaving that audit entirely manual.
- Added root `CONTRIBUTING.md`, `ACCESSIBILITY.md`, `LICENSE`, and `NOTICE` so the superproject's contributor, accessibility, and legal surfaces are explicit at the repository root.
- Collapsed the older subtree migration and plugin-alignment planning docs into this roadmap history plus the still-live root maintainer references once those plans had become historical rather than active operating guidance.
