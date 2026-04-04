# Project Roadmap

## Vision

- Keep `apple-dev-skills` as a durable Apple development skill source-of-truth repo with plugin-first packaging for Codex and Claude Code.

## Product principles

- Keep root `skills/` as the canonical workflow-authoring surface.
- Prefer deterministic local scripts and validation over implied workflow behavior.
- Keep cross-ecosystem behavior grounded in the Codex-and-Claude common denominator first, then add Claude-only extras separately.
- Treat tests, shipped skill assets, plugin manifests, and maintainer validation as the source of truth for roadmap updates.

## Milestone Progress

- [x] Milestone 1: Initial Apple Skill Bundle
- [x] Milestone 2: Portability and Customization Docs
- [x] Milestone 3: Automation Prompt Support
- [x] Milestone 4: Hybrid Apple/Xcode Workflow Suite
- [x] Milestone 5: Discovery and README Polish
- [x] Milestone 6: Readiness and Documentation Parity
- [x] Milestone 7: Claude Code Compatibility Completion
- [x] Milestone 8: Canonical Skill v2.0.0 Consolidation
- [x] Milestone 9: AGENTS Sync Skill Retirement
- [x] Milestone 10: Top-Level Skill Reset
- [x] Milestone 11: Documentation Maintenance Cadence
- [x] Milestone 12: Deferred Audit Reporting and Future Swift Direction
- [x] Milestone 13: SwiftPM Bootstrap Parity
- [x] Milestone 14: Plugin-First Packaging Foundation
- [x] Milestone 15: Xcode App Bootstrap and Guidance Sync Skills
- [x] Milestone 16: Apple and Swift Docs Skill Extraction
- [x] Milestone 17: Existing Skill Rename and Install-Surface Cleanup
- [ ] Milestone 18: Claude Code Plugin Extras
- [x] Milestone 19: Swift Style Tooling Workflow

## Milestone 1: Initial Apple Skill Bundle

Scope:

- [x] Establish the initial Apple skill repository and baseline layout.

Tickets:

- [x] Ship the first Apple-focused skill bundle.
- [x] Establish repository-level documentation and validation expectations.

Exit criteria:

- [x] The initial Apple skill bundle exists in a usable published form.

## Milestone 2: Portability and Customization Docs

Scope:

- [x] Improve portability guidance and document customization contracts for the early skill set.

Tickets:

- [x] Document per-skill customization behavior.
- [x] Reduce portability ambiguity in repo and skill docs.

Exit criteria:

- [x] Portability and customization guidance are documented for the shipped skills.

## Milestone 3: Automation Prompt Support

Scope:

- [x] Add automation-oriented prompt references to the skill set.

Tickets:

- [x] Add automation prompt templates to the active skills at the time.

Exit criteria:

- [x] Automation prompt support is available in shipped skill references.

## Milestone 4: Hybrid Apple/Xcode Workflow Suite

Scope:

- [x] Expand the repository into a broader Apple/Xcode workflow suite.

Tickets:

- [x] Add orchestrator-era workflow components and supporting docs.
- [x] Document MCP-first execution, CLI fallback, and safety/docs routing patterns.

Exit criteria:

- [x] The broader Apple/Xcode workflow suite shipped and established the later consolidation baseline.

## Milestone 5: Discovery and README Polish

Scope:

- [x] Improve discoverability and root documentation quality.

Tickets:

- [x] Refine README wording and install guidance.
- [x] Reduce discoverability drift in root docs through follow-up polish.

Exit criteria:

- [x] Root discoverability docs were cleaned up through the `v1.4.x` line.

## Milestone 6: Readiness and Documentation Parity

Scope:

- [x] Establish roadmap tracking and align docs with implementation reality.

Tickets:

- [x] Create and maintain the repository roadmap.
- [x] Add CI-oriented validation guardrails for docs and skills.

Exit criteria:

- [x] Readiness tracking and documentation parity work landed with validation support.

## Milestone 7: Claude Code Compatibility Completion

Scope:

- [x] Complete compatibility work needed for Claude-oriented packaging support.

Tickets:

- [x] Add grouped nested plugin manifest support.

Exit criteria:

- [x] Claude Code compatibility completion work shipped.

## Milestone 8: Canonical Skill v2.0.0 Consolidation

Scope:

- [x] Consolidate the repository around canonical Apple skills and shared baseline guidance.

Tickets:

- [x] Reduce the surface to the canonical Apple skill set for the next release line.
- [x] Extract the shared Swift/Apple baseline snippet for reuse.

Exit criteria:

- [x] Canonical v2.0.0 consolidation shipped with shared snippet guidance in place.

## Milestone 9: AGENTS Sync Skill Retirement

Scope:

- [x] Retire the dedicated AGENTS sync skill and replace it with lighter guidance.

Tickets:

- [x] Remove `apple-swift-package-agents-sync` from the active surface.
- [x] Replace sync guidance with snippet-first and external docs-alignment recommendations.

Exit criteria:

- [x] AGENTS sync responsibilities were removed from the active skill surface without breaking migration clarity.

## Milestone 10: Top-Level Skill Reset

Scope:

- [x] Reset the repository around three parallel top-level skills and straighten the docs contract.

Tickets:

- [x] Remove the router layer from the active surface.
- [x] Restore three independent top-level skills.
- [x] Normalize skill contracts around `status`, `path_type`, fallback, and handoff language.

Exit criteria:

- [x] The active public skill surface is the current three-skill top-level model.

## Milestone 11: Documentation Maintenance Cadence

Scope:

- [x] Align maintainer docs and validation with the actual shipped repository structure.

Tickets:

- [x] Point root docs at `docs/maintainers/` as the canonical maintainer-doc location.
- [x] Add the durable reality-audit guide.
- [x] Realign repo validation with the canonical maintainer-doc contract.
- [x] Normalize shipped customization-template defaults under each skill's `references/` directory while preserving `~/.config/...` overrides.

Exit criteria:

- [x] Maintainer docs, validation, and shipped skill layout match current repo reality.

## Milestone 12: Deferred Audit Reporting and Future Swift Direction

Scope:

- [x] Convert the old deferred bucket into concrete hardening coverage plus one explicit future-direction placeholder.

Tickets:

- [x] Defer recurring maintainer audit/report cadence refinement until it has a clearer operational need.
- [x] Park follow-up roadmap/reporting cleanup that is not required for the current shipped surface.
- [x] Hold a placeholder for future non-Xcode Swift skill design direction.
- [x] Add Dash end-to-end coverage for real install and fallback flows beyond dry-run and blocked-path assertions.
- [x] Add Xcode end-to-end coverage for real MCP or CLI fallback execution beyond policy-shaping tests.
- [x] Add broader bootstrap coverage for blocked-vs-failed negative paths, alternate testing modes, and dry-run toolchain-validation behavior beyond the immediate SwiftPM parity fixes.

Exit criteria:

- [x] The repo contains the missing docs and Xcode workflow hardening coverage, and maintainer docs hold one explicit placeholder for future non-Xcode Swift expansion instead of an unbounded deferred bucket.

## Milestone 13: SwiftPM Bootstrap Parity

Scope:

- [x] Align the Swift package bootstrap skill with current `swift package init` behavior and option support.

Tickets:

- [x] Audit current SwiftPM `swift package init` flags and template behavior on supported `Swift 5.10+` toolchains.
- [x] Update the bootstrap workflow to use current `swift package init` testing options and keep generated tests aligned with the selected testing mode.
- [x] Document and enforce `Swift 5.10+` as the supported and validated bootstrap floor, and block older toolchains such as `5.9` with clear upgrade guidance.
- [x] Document how the skill should choose between `swift package init` flags and follow-up package edits when toolchain support differs within the supported `5.10+` floor.
- [x] Document when Swift packages should stay on `swift build` and when they should hand off to `xcodebuild` through `xcode-app-project-workflow`.
- [x] Add validation coverage for executable-package bootstrap output so generated tests and package shape match documented expectations.

Exit criteria:

- [x] The bootstrap skill matches current SwiftPM testing options and generated package behavior on supported `Swift 5.10+` toolchains.
- [x] Maintainer docs explain the expected blocked behavior for toolchains older than `5.10` and the expected fallback behavior within the supported `5.10+` floor when newer `swift package init` options are unavailable.
- [x] Maintainer docs explain when Swift package builds should use `xcodebuild` because Xcode-managed toolchain behavior is required.
- [x] Validation catches drift between documented bootstrap behavior and actual generated package output.

## Milestone 14: Plugin-First Packaging Foundation

Scope:

- [x] Establish the repository's plugin-first install shape while keeping root `skills/` as the workflow-authoring source of truth.

Tickets:

- [x] Add a repo-local Codex plugin scaffold with `.codex-plugin/plugin.json` and a local marketplace entry.
- [x] Add a repo-local Claude Code plugin scaffold with `.claude-plugin/plugin.json`.
- [x] Document the supported common-denominator plugin structure shared by Codex and Claude.
- [x] Document which plugin surfaces are Codex-only, Claude-only, or shared.
- [x] Keep plugin packaging metadata and assets in sync with the canonical root skills as that packaging layer grows.

Exit criteria:

- [x] The repository contains a documented plugin scaffold for both ecosystems, and maintainers can point to one canonical packaging plan without implying unsupported Codex plugin behavior.

## Milestone 15: Xcode App Bootstrap and Guidance Sync Skills

Scope:

- [x] Add the new Xcode app bootstrap surface and split repo-guidance sync into dedicated skills instead of overloading the main Xcode workflow skill.

Tickets:

- [x] Ship `bootstrap-xcode-app-project` for new native Apple app creation on macOS.
- [x] Ship `sync-xcode-project-guidance` for bringing existing Xcode app repos up to the expected docs and guidance baseline.
- [x] Ship `sync-swift-package-guidance` for bringing existing Swift package repos up to the expected docs and guidance baseline.
- [x] Define clean handoffs between the bootstrap skill, the sync skills, and the main Xcode workflow skill.
- [x] Add customization guidance for `XcodeGen` as an optional project-generation preference, without making it the only supported bootstrap path.

Exit criteria:

- [x] New native Apple app creation and existing-repo guidance sync are available as dedicated skills with clear trigger boundaries and explicit handoffs.

## Milestone 16: Apple and Swift Docs Skill Extraction

Scope:

- [x] Extract Apple and Swift docs exploration into a dedicated skill so the main Xcode workflow can stay focused on execution work.

Tickets:

- [x] Ship `explore-apple-swift-docs` as the active docs skill across Xcode MCP docs, Dash, and official web docs.
- [x] Deprecate `apple-dash-docsets` into a compatibility redirect instead of keeping it in the active public surface.
- [x] Move docs-source routing responsibility out of `xcode-app-project-workflow` and keep only the Apple docs gate plus a smooth handoff.
- [x] Update README, maintainer docs, validation, and tests to treat `explore-apple-swift-docs` as the active docs skill.

Exit criteria:

- [x] Apple and Swift docs exploration has its own dedicated active skill, and the main Xcode workflow no longer owns docs-source machinery.

## Milestone 17: Existing Skill Rename and Install-Surface Cleanup

Scope:

- [x] Rename the remaining legacy-prefixed skills where a search-oriented action name improves install UX and discoverability.

Tickets:

- [x] Audit the current skill names for the plugin-first install model and Codex/Claude search surfaces.
- [x] Rename any retained `apple-*` skills whose names no longer carry useful disambiguation once the plugin name already provides Apple scope.
- [x] Update README, roadmap, marketplace entries, plugin manifests, and install examples to the new names.
- [x] Document the concrete local Codex plugin install flow for `plugins/apple-dev-skills/`, keeping the official marketplace-based path canonical and any Gale-local helpers optional.
- [x] Preserve migration notes for any renamed skill IDs so maintainers can map old references cleanly.

Exit criteria:

- [x] The active install surface uses the final intended names, and repo docs no longer teach stale IDs as the preferred user-facing surface.

## Milestone 18: Claude Code Plugin Extras

Scope:

- [ ] Add Claude-only plugin enhancements on top of the shared Codex/Claude common denominator without making cross-ecosystem workflows depend on them.

Tickets:

## Milestone 19: Swift Style Tooling Workflow

Scope:

- [x] Add a dedicated active skill for SwiftLint and SwiftFormat integration instead of scattering style-tooling guidance across bootstrap, sync, and execution surfaces.

Tickets:

- [x] Ship `swift-style-tooling-workflow` as the active skill for SwiftLint and SwiftFormat setup across CLI, Xcode, SwiftPM, Git hooks, and GitHub Actions.
- [x] Document the actual support matrix so unsupported tool-and-surface combinations are blocked instead of implied.
- [x] Add a deterministic helper for exporting SwiftFormat for Xcode shared settings into a checked-in `.swiftformat` file.
- [x] Update README, maintainer docs, validation, and tests to treat `swift-style-tooling-workflow` as part of the active public skill surface.
- [x] Narrow the future-direction placeholder so style-tooling is no longer treated as deferred non-Xcode Swift expansion.

Exit criteria:

- [x] The repo ships a first-class style-tooling skill with explicit surface boundaries, deterministic SwiftFormat config export support, and fully updated maintainer and validation docs.

- [ ] Flesh out `hooks/` for Claude-only automation where it clearly helps maintainers or end users.
- [ ] Add `bin/` helpers only for Claude-only convenience wrappers that do not become required for the shared workflow contract.
- [ ] Document which Claude-only extras are optional sugar versus canonical workflow behavior.
- [ ] Validate that Claude-only extras degrade gracefully when absent from Codex.

Exit criteria:

- [ ] Claude-only plugin extras exist as clearly separated enhancements, and the core workflow remains usable through the shared skill surface in both ecosystems.
