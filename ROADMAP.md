# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 5: SwiftASB skills plugin](#milestone-5-swiftasb-skills-plugin)
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

- Milestone 5: SwiftASB skills plugin - In Progress

## Milestone 5: SwiftASB skills plugin

### Status

In Progress

### Scope

- [x] Add a Socket-hosted `swiftasb-skills` child plugin that helps agents explain SwiftASB, choose an integration shape, and build SwiftUI, AppKit, and Swift package surfaces on top of SwiftASB.
- [x] Keep the plugin as a companion guidance surface rather than a runtime plugin: do not bundle an MCP server, duplicate SwiftASB source, or copy generated schema files into `socket`.
- [x] Keep Apple framework workflow rules delegated to `apple-dev-skills`, with this plugin focused on SwiftASB-specific explanation, decision support, integration, and troubleshooting.

### Tickets

- [x] Create `plugins/swiftasb-skills/` with its own `.codex-plugin/plugin.json` and authored `skills/` source.
- [x] Add first-slice skills for explaining SwiftASB, choosing an integration shape, and building a SwiftUI app on top of SwiftASB.
- [x] Add `swiftasb:build-appkit-app` for AppKit apps after the first slice proves useful.
- [x] Add `swiftasb:build-swift-package` for Swift package authors after the first slice proves useful.
- [x] Add an integration diagnostics skill for runtime discovery, app-server startup, threads, turns, approvals, diagnostics, MCP status, history reads, and live-test isolation.
- [x] Wire `swiftasb-skills` into the root Socket marketplace as a normal local child plugin.
- [x] Update root README and maintainer docs so users understand the split between the SwiftASB package source of truth and the Socket-hosted Codex guidance plugin.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py` and any child-plugin checks added by the new plugin.
- [ ] Sync `swiftasb-skills` with current SwiftASB changes, starting from the live SwiftASB source and docs so the explanation, integration-shape, SwiftUI, AppKit, package, and diagnostics skills match the current client API and runtime behavior.

### Exit Criteria

- [x] The Socket marketplace exposes `swiftasb-skills` as an installable child plugin.
- [x] The new skills can help an agent explain SwiftASB to a user before implementation, including when SwiftASB is not the right fit.
- [x] The new skills guide SwiftUI, AppKit, and Swift package integrations without duplicating broad Apple framework guidance that belongs to `apple-dev-skills`.
- [x] Root Socket docs, marketplace wiring, and validation agree on the plugin's install surface.

## Backlog Candidates

- [ ] Overhaul `agent-plugin-skills` so its docs, tests, generated bootstrap content, and sync audit logic target Codex/OpenAI plus the open `.agents/skills` discovery mirror only. Remove stale expectations for retired child maintainer docs such as reality-audit and install-surface docs, and keep the wording away from unsupported non-Codex or generic multi-agent surfaces.
- [ ] Evaluate a centralized Socket validation setup that can check marketplace metadata, plugin manifests, child README/AGENTS shape, `SKILL.md` frontmatter, and `agents/openai.yaml` alignment from one root command while still leaving child-local tests where behavior needs them.
- [ ] Track the remaining Speak Swiftly duplicate-enable repair behavior in the standalone `SpeakSwiftlyServer` plugin workflow rather than keeping the completed Socket catalog split open.

## History

- Released `v6.7.0` after aggressively simplifying Socket documentation: root README and CONTRIBUTING split, child roadmap consolidation into root planning docs, child README collapse with user-owned `TBD` overview sections, nested maintainer doc cleanup, workflow atlas removal, and unsupported non-Codex surface removal.
- Completed the Speak Swiftly plugin catalog split by exposing `speak-swiftly` from the canonical `gaelic-ghost/SpeakSwiftlyServer` Git-backed source, retiring the local `plugins/SpeakSwiftlyServer/` mirror, validating isolated marketplace install paths, and keeping standalone SpeakSwiftlyServer as the plugin payload source of truth.
- Completed the release and sync discipline milestone by aligning release-mode docs, subtree sync rules, shared-version workflow, release-ready gates, and marketplace refresh ordering around the current mixed monorepo model.
- Completed the subtree workflow hardening milestone by documenting subtree add, pull, and push paths, adding the root marketplace audit pass, and adding a public child plugin removal checklist.
- Completed [#35](https://github.com/gaelic-ghost/socket/issues/35) / [#37](https://github.com/gaelic-ghost/socket/issues/37) by hardening release and PR scripts around delayed GitHub state.
- Completed [#39](https://github.com/gaelic-ghost/socket/issues/39) by adding the Swift Package Index add-package gate and one-shot script around the documented `SwiftPackageIndex/PackageList` Add Package issue form.
- Planned a `swiftasb-skills` child plugin to help agents explain SwiftASB and build SwiftUI, AppKit, and Swift package integrations from a Socket-visible guidance surface.
- Updated `productivity-skills:maintain-project-repo` so heavy remote CI can be deferred after full local validation, branch push, PR creation, and initial check discovery, with Codex expected to use native thread Timer/Wakeup or heartbeat automation to resume the release instead of keeping an idle CI-waiting script open.
- Added root `docs/media` screenshot assets and README media guidance so the Codex plugin-directory catalog surface is visible without weakening text-first documentation.
- Added coordinated OpenAI Codex Hooks guidance across `agent-plugin-skills` and `productivity-skills`, with future `maintain-project-hooks` work tracked in the productivity roadmap.
- Updated `socket` and plugin guidance so ordinary user installs and updates default to Git-backed Codex marketplace sources and official marketplace add/upgrade commands.
- Added coordinated Codex subagent guidance across `agent-plugin-skills` and `productivity-skills`, grounding skill wording in OpenAI's current explicit-trigger `subagents` model while keeping the root docs clear about why the pass belongs in `socket`.
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
