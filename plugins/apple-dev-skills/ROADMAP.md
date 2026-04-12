# Project Roadmap

## Vision

- Keep `apple-dev-skills` as a durable Apple development skill source-of-truth repo with plugin-first packaging for Codex and Claude Code.

## Product Principles

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
- [x] Milestone 19: Format Swift Sources
- [x] Milestone 20: Structure Swift Sources
- [ ] Milestone 21: Swift Cleanup Automation Exploration
- [x] Milestone 22: Expand TODO and FIXME Ledger Normalization
- [x] Milestone 23: Customization Consolidation Review
- [ ] Milestone 24: MCP App UI for Configuration and Customization
- [ ] Milestone 25: macOS Menu Bar Extra for Skill Controls
- [ ] Milestone 26: Dash Direct MCP and Call Library
- [ ] Milestone 27: Repo Self-Compliance and Install-Surface Audit
- [ ] Milestone 28: Use `Agent Dev Skills` plugin to align repo with skills/plugin repo standards
- [ ] Milestone 29: Swift and Xcode Testing Offload Workflow
- [x] Milestone 30: Customization Surface Simplification Implementation
- [x] Milestone 31: Repo Maintenance Toolkit Skill
- [x] Milestone 32: Shared Toolkit Extraction to `productivity-skills`
- [x] Milestone 33: Swift Package Execution Skill Split
- [x] Milestone 34: Execution Skill Split and Inference Refactor
- [x] Milestone 35: Swift/Xcode Repo-Maintenance Toolkit Profiles
- [x] Milestone 36: Guidance Preservation and AGENTS Expansion

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

- [x] Close out the grouped nested plugin manifest experiment and record that it is not part of the enduring repository contract.

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
- [x] Keep `bootstrap-swift-package` as the explicit shipped skill name for Swift package bootstrap work in roadmap and repo docs.
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

## Milestone 14: Top-Level Export Surface Foundation

Scope:

- [x] Establish the repository's top-level export shape while keeping root `skills/` as the workflow-authoring source of truth.

Tickets:

- [x] Define top-level `skills/` as the active export surface.
- [x] Keep local discovery mirrors explicit without treating them as second sources of truth.
- [x] Document that future `mcps/` or `apps/` must also live at the repository top level.
- [x] Remove stale nested packaging language from the enduring repository contract.
- [x] Keep root docs and validation aligned with the top-level export model.

Exit criteria:

- [x] The repository contains one clear top-level export model and does not imply a nested packaged plugin tree is still active.

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
- [x] Document the final exported skill names without tying them to a nested packaged plugin tree.
- [x] Preserve migration notes for any renamed skill IDs so maintainers can map old references cleanly.

Exit criteria:

- [x] The active install surface uses the final intended names, and repo docs no longer teach stale IDs as the preferred user-facing surface.

## Milestone 18: Claude Code Plugin Extras

Scope:

- [ ] Add Claude-only plugin enhancements on top of the shared Codex/Claude common denominator without making cross-ecosystem workflows depend on them.

Tickets:

- [ ] Flesh out `hooks/` for Claude-only automation where it clearly helps maintainers or end users.
- [ ] Add `bin/` helpers only for Claude-only convenience wrappers that do not become required for the shared workflow contract.
- [ ] Document which Claude-only extras are optional sugar versus canonical workflow behavior.
- [ ] Validate that Claude-only extras degrade gracefully when absent from Codex.

Exit criteria:

- [ ] Claude-only plugin extras exist as clearly separated enhancements, and the core workflow remains usable through the shared skill surface in both ecosystems.

## Milestone 19: Format Swift Sources

Scope:

- [x] Add a dedicated active skill for SwiftLint and SwiftFormat integration instead of scattering style-tooling guidance across bootstrap, sync, and execution surfaces.

Tickets:

- [x] Ship `format-swift-sources` as the active skill for SwiftLint and SwiftFormat setup across CLI, Xcode, SwiftPM, Git hooks, and GitHub Actions.
- [x] Document the actual support matrix so unsupported tool-and-surface combinations are blocked instead of implied.
- [x] Add a deterministic helper for exporting SwiftFormat for Xcode shared settings into a checked-in `.swiftformat` file.
- [x] Update README, maintainer docs, validation, and tests to treat `format-swift-sources` as part of the active public skill surface.
- [x] Narrow the future-direction placeholder so style-tooling is no longer treated as deferred non-Xcode Swift expansion.

Exit criteria:

- [x] The repo ships a first-class style-tooling skill with explicit surface boundaries, deterministic SwiftFormat config export support, and fully updated maintainer and validation docs.

## Milestone 20: Structure Swift Sources

Scope:

- [x] Add a dedicated active skill for structural Swift source cleanup instead of overloading the formatting skill with file-splitting and source-layout policy.

Tickets:

- [x] Rename `swift-style-tooling-workflow` to `format-swift-sources`.
- [x] Add `structure-swift-sources` as the active skill for file splitting, source moves, MARK normalization, DocC coverage, and TODO/FIXME ledger policy.
- [x] Cross-link the formatting and structure skills so formatting is the canonical first and last pass around structural mutation.
- [x] Add a deterministic helper for normalizing Swift TODO/FIXME comments into `TODO.md` and `FIXME.md`.
- [x] Update README, maintainer docs, roadmap entries, and tests to treat both skills as part of the active public skill surface.

Exit criteria:

- [x] The repo ships distinct formatting and structural Swift cleanup skills with clear boundaries and shared choreography.

## Milestone 21: Swift Cleanup Automation Exploration

Scope:

- [ ] Explore a larger maintainer automation flow for the `format-swift-sources` -> `structure-swift-sources` -> `format-swift-sources` choreography without overclaiming determinism for agent-driven file splits.

Tickets:

- [ ] Evaluate a `codex exec`-friendly maintainer wrapper for sequential formatting and structure passes.
- [ ] Define a structured-output contract for any `codex exec` helper so it can report findings, changed files, blocked steps, and follow-up recommendations deterministically.
- [ ] Decide whether `codex exec` should remain an on-demand maintainer tool, become a wrapper around deterministic repo helpers, or stay limited to advisory and enrichment work.
- [ ] Evaluate a Codex GUI App Automation that runs the same high-level choreography on a schedule, preferably in a dedicated worktree.
- [ ] Document the boundary between deterministic local scripts, `codex exec` enrichment, and Codex GUI background automation so the repo does not imply that file splitting is fully automatable.
- [ ] Keep file splitting and concern detection agent-driven unless a later design proves a safer deterministic boundary.

Exit criteria:

- [ ] The repo has a written decision and an approved implementation direction for higher-level Swift cleanup automation.

## Milestone 22: Expand TODO and FIXME Ledger Normalization

Scope:

- [x] Expand the deterministic TODO/FIXME helper so it is useful across expected Swift and Objective-C source patterns, while keeping source rewriting and ledger rendering deterministic.

Tickets:

- [x] Extend source discovery beyond `.swift` to include Objective-C source files such as `.h`, `.m`, and `.mm`.
- [x] Support line-comment TODO/FIXME forms and compiler-warning forms that are common in Swift and Objective-C sources.
- [x] Preserve existing ticket IDs when source comments already reference a normalized `TODO-####` or `FIXME-####` ticket.
- [x] Add deterministic metadata to ledger entries for source syntax kind so future tooling can distinguish line comments from warning directives.
- [x] Add deterministic roadmap-link support by parsing explicit milestone or ticket references from source comments and resolving them into `ROADMAP.md` links in the corresponding ledger entries.
- [x] Add deterministic saved-plan-doc link support by parsing explicit references to related planning documents from source comments and rendering those links into the ledger entries.
- [x] Keep the helper reportable in JSON so higher-level tooling can reuse the scan and rewrite summary safely.
- [x] Add focused tests for Swift line comments, Objective-C line comments, compiler-warning forms, roadmap-link extraction, and saved-plan-doc link extraction.
- [x] Update skill references so the helper contract documents the expanded source coverage and ledger schema clearly.

Exit criteria:

- [x] The helper can normalize supported Swift and Objective-C TODO/FIXME forms into stable ledger entries with source-location data, syntax metadata, and optional deterministic links to roadmap milestones or related saved plan docs.

## Milestone 23: Customization Consolidation Review

Scope:

- [x] Evaluate whether the current per-skill customization system should be consolidated, simplified, or made more inference-driven.

Tickets:

- [x] Audit all active customization knobs for duplication, overlap, and repo-shape inferability.
- [x] Evaluate consolidating duplicated `customization_config.py` helpers into a shared maintainer implementation or generator path.
- [x] Identify knobs that should become opinionated defaults instead of user-facing customization.
- [x] Identify knobs that can be inferred from repo type, file layout, active IDE state, tool availability, stored agent preferences, or project-level guidance.
- [x] Propose a smaller long-term customization surface with a clear split between runtime-enforced settings and policy-only defaults.
- [x] Track the repo-shape inference candidates already identified:
  - bootstrap app defaults such as project kind, platform, and often UI stack
  - bootstrap package defaults such as package type, platform preset, and often testing mode
  - style-tooling defaults such as tool selection, preferred surface, checked-in config posture, and plugin-vs-script preference
  - docs troubleshooting preference when the failure mode itself already makes the best recovery path obvious
- [x] Track the environment-inference candidates already identified:
  - SwiftFormat host-app export preference based on whether the host app or shared defaults domain exists
  - SwiftLint plugin preference based on package-manager compatibility and config placement
  - Xcode fallback-command profile based on workspace type, MCP availability, and available CLIs
- [x] Track the simplification candidates already identified:
  - collapse sync-skill booleans into a smaller write-mode model
  - replace low-value explicit defaults with inference-first behavior and rare escape hatches
  - separate maintainer-tuning knobs from user-meaningful customization
  - centralize duplicated customization helper plumbing only if that remains the right architecture after the surface is reduced
- [x] Break the work into phases:
  - audit and classify knobs
  - decide what to remove, infer, or keep
  - implement the smaller surface
  - update tests, validators, and maintainer docs to match

Exit criteria:

- [x] Maintainers have a written decision on whether to keep, consolidate, or shrink the customization system, with a concrete follow-up plan for any approved architecture change.

See `docs/maintainers/customization-consolidation-review.md`.

## Milestone 24: MCP App UI for Configuration and Customization

Scope:

- [ ] Add an MCP App surface for inspecting and adjusting skill configuration and customization state without hand-editing YAML.

Tickets:

- [ ] Design the MCP App scope for viewing effective customization state across skills.
- [ ] Define which edits should remain metadata-only versus which should affect runtime-enforced behavior.
- [ ] Add UI resources and tool wiring for reading templates, durable overrides, and effective merged config.
- [ ] Validate that MCP App edits preserve the same contracts as the script-based customization flow.
- [ ] Document the relationship between skill-local scripts and the MCP App surface so the UI does not become a shadow workflow.

Exit criteria:

- [ ] The repo ships a documented MCP App path for viewing and editing customization state, or has an explicit bounded design that is ready for implementation.

## Milestone 25: macOS Menu Bar Extra for Skill Controls

Scope:

- [ ] Explore a native macOS menu bar utility for local maintainer workflows around skill installation, customization, and quick actions.

Tickets:

- [ ] Define the minimum viable menu bar feature set for local maintainer use.
- [ ] Evaluate whether the app should be a thin shell around existing scripts and MCP surfaces or a richer native controller.
- [ ] Identify which repo-local actions are safe and useful from a menu bar context, such as showing effective customization, opening maintainer docs, or triggering local plugin refresh.
- [ ] Document how the menu bar app would coexist with Codex plugin wiring and any future MCP App customization UI.
- [ ] Decide whether the menu bar app belongs in this repo, a sibling repo, or a plugin-bundled local-development surface.

Exit criteria:

- [ ] Maintainers have a documented plan for whether to build the menu bar app, what it should own, and where it should live.

## Milestone 26: Dash Direct MCP and Call Library

Scope:

- [ ] Remove avoidable indirection in the Dash-docsets workflow by teaching direct MCP usage first and documenting the Dash.app localhost HTTP call structure as a direct fallback surface.

Tickets:

- [ ] Audit the current `explore-apple-swift-docs` skill for places where local helper-script indirection is standing in for direct MCP usage that the agent could perform itself.
- [ ] Teach the skill to prefer direct Dash MCP calls when the MCP service is available instead of routing ordinary search behavior through wrapper scripts.
- [ ] Document the Dash.app localhost HTTP call structure clearly enough that the agent can use it directly when MCP is unavailable or incomplete.
- [ ] Design and provide a compact library of common Dash example calls:
  - most common search calls
  - most popular docsets
  - most common frameworks and ecosystems to query through Dash
  - strict versus snippet-rich search shapes
- [ ] Keep the example-call library small, high-signal, and organized for quick agent pickup instead of encyclopedic coverage.
- [ ] Reconcile `explore-apple-swift-docs` references and runtime helpers so the documented primary path and the actual preferred path match again.

Exit criteria:

- [ ] The Dash workflow teaches direct MCP usage first, documents the localhost HTTP structure as a real fallback, and ships a practical library of common example calls and docset targets.

## Milestone 27: Repo Self-Compliance and Install-Surface Audit

Scope:

- [ ] Check this repository against its own skill, symlink, export-surface, and local-discovery guidance and close any real gaps between docs and the actual top-level export model.

Tickets:

- [x] Audit the repo against its documented symlink expectations for `.agents/skills` and `.claude/skills`.
- [x] Audit the repo against its documented top-level export model and remove the nested packaging tree.
- [ ] Verify that root docs, maintainer docs, and skill docs all stay aligned with the top-level export model after future refactors.
- [ ] Document any mismatch between repo docs and the actual top-level export surface so guidance reflects operational reality instead of stale packaging assumptions.
- [x] Add a maintainer smoke-test flow for local discovery and top-level export-surface verification.

Exit criteria:

- [ ] Maintainers have a verified, reality-based local discovery and top-level export story for this repo, with docs and tooling updated to match what the repository actually ships.

## Milestone 28: Use `Agent Dev Skills` plugin to align repo with skills/plugin repo standards

Scope:

- Use the adjacent `agent-plugin-skills` maintainer workflow to audit and align this repository with the current shared skills/plugin repo standards, while keeping this repository's own contract focused on top-level exports only.

Tickets:

- Confirm the personal-scope maintainer install of `agent-plugin-skills` stays current for work on this repository without reintroducing a nested packaged plugin tree here.
- Use `maintain-plugin-repo` and `sync-skills-repo-guidance` as the maintainer entrypoints for repo-wide audit, coordination, and documentation alignment where relevant.
- Align repo docs, export surfaces, ignores, and maintainer guidance with the current shared standards without flattening repo-specific policy.
- Remove tracked vendored maintainer-plugin copies and stale nested packaging language from this repo while keeping the adjacent standards source as the maintainer-only setup.

Exit criteria:

- The repository validates cleanly against the current shared skills/plugin repo standards.
- Repo docs, plugin packaging, marketplace wiring, and maintainer guidance describe the same live behavior.

## Milestone 29: Swift and Xcode Testing Offload Workflow

Scope:

- Design and ship a dedicated offload workflow for repetitive, noisy SwiftPM and Xcode build, test, preview, and diagnostics work so the main agent thread can stay focused on higher-signal reasoning and implementation.

Tickets:

- Audit the current repetitive and noisy Swift and Xcode testing work that is currently handled inline in the main agent thread.
- Decide which implementation surface should own the offload path:
  - skill guidance only
  - subagent-backed workflow
  - MCP-backed helper
  - another simpler durable surface if that better matches the actual constraints
- Define the input and output contract for the offload path so verification work can be delegated without losing the details the main thread still needs.
- Cover the highest-value offload cases first:
  - `swift build`
  - `swift test`
  - `xcodebuild` test or build flows
  - preview or diagnostics refresh
  - noisy failure summarization back into the main thread
- Keep the design aligned with the existing Apple-docs-first and Xcode-MCP-first guidance instead of creating a parallel Apple workflow model.
- Document when the main agent should stay local versus when it should hand noisy verification work to the offload path.
- Add validation or smoke-test coverage for the offload contract once the implementation surface is chosen.

Exit criteria:

- Maintainers have one documented and validated way to offload repetitive Swift and Xcode verification work from the main agent thread.
- The offload path returns concise, decision-useful results without obscuring the underlying build or test evidence.

## Milestone 30: Customization Surface Simplification Implementation

Scope:

- [x] Implement the smaller customization surface approved by Milestone 23 before building any MCP App or other UI on top of customization state.

Tickets:

- [x] Reduce each active customization template to the remaining user-meaningful knobs approved in the review.
- [x] Collapse the two sync-skill booleans into one smaller write-mode model.
- [x] Reclassify safety invariants and maintainer tuning so they stop appearing as ordinary durable user customization.
- [x] Teach the approved inference-first defaults in the affected workflow docs and runtime wrappers.
- [x] Decide whether maintainer-time generation or sync is still needed for duplicated `customization_config.py` copies after the surface reduction lands.
- [x] Update tests, validators, and maintainer docs to match the reduced surface.

Exit criteria:

- [x] The shipped customization surface is materially smaller, better classified, and ready to support future UI work without carrying the current drift forward.
- [x] Completed 2026-04-04 by reducing the live customization surface, introducing sync-skill `writeMode`, and aligning wrappers, tests, and maintainer docs with the smaller model.

## Milestone 31: Repo Maintenance Toolkit Skill

Scope:

- [x] Add a reusable local-first maintainer toolkit integration for Swift and Xcode repositories, then wire the bootstrap and guidance-sync skills to install or refresh that toolkit in target repos.

Tickets:

- [x] Add a managed `scripts/repo-maintenance/` asset tree and thin GitHub workflow wrapper for Apple repo bootstraps and guidance-sync runs.
- [x] Ship a thin GitHub workflow wrapper that calls the local validation entrypoint instead of owning logic itself.
- [x] Add standard and submodule-aware release flows to the managed toolkit.
- [x] Update bootstrap and guidance-sync skills to install or refresh the toolkit in target repos.
- [x] Update tests, validators, root docs, and maintainer docs to reflect the expanded active skill surface.

Exit criteria:

- [x] Successful bootstrap and guidance-sync runs install or refresh the managed toolkit in target repos.
- [x] The Apple repo keeps a canonical vendored toolkit snapshot for its integration surfaces.
- [x] Root docs, maintainer docs, and validation all describe the same Apple-specific integration surface.
- [x] Completed 2026-04-05 by shipping the toolkit assets, adding managed repo-maintenance resources, and wiring bootstrap and sync workflows to install or refresh them.

## Milestone 32: Shared Toolkit Extraction to `productivity-skills`

Scope:

- [x] Move the standalone shared `repo-maintenance-toolkit` skill into `../productivity-skills` because it is globally useful rather than Apple-specific.
- [x] Keep `apple-dev-skills` focused on Apple workflow skills while preserving self-contained bootstrap and guidance-sync integrations.

Tickets:

- [x] Add `repo-maintenance-toolkit` as an active shared skill in `../productivity-skills`.
- [x] Remove `repo-maintenance-toolkit` from the Apple repo's active skill inventory.
- [x] Vendor the managed toolkit snapshot under `shared/repo-maintenance-toolkit/` so Apple bootstrap and sync workflows stay independently usable.
- [x] Realign docs, roadmap notes, validators, and tests in both repos to match the new ownership boundary.

Exit criteria:

- [x] `productivity-skills` is the canonical home of the standalone `repo-maintenance-toolkit` skill.
- [x] Successful bootstrap and guidance-sync runs install or refresh the managed toolkit in target repos.
- [x] `apple-dev-skills` no longer presents the toolkit as an active top-level skill, but still keeps the vendored integration snapshot needed for standalone Apple workflows.
- [x] Completed 2026-04-05 by extracting the shared skill to `productivity-skills`, vendoring the Apple snapshot under `shared/repo-maintenance-toolkit/`, and re-aligning both repos' docs and tests.

## Milestone 33: Swift Package Execution Skill Split

Scope:

- [x] Split ordinary Swift package execution out of the Xcode workflow so plain SwiftPM work has its own terminal-first and editor-first skill boundary.

Tickets:

- [x] Add `swift-package-workflow` as the canonical execution skill for existing Swift package repos whose source of truth is `Package.swift`.
- [x] Narrow `xcode-app-project-workflow` so it focuses on Xcode-managed and Xcode-adjacent execution concerns instead of general package development.
- [x] Update package bootstrap, package guidance sync, style-tooling, and structure-cleanup skills so ordinary package work hands off to `swift-package-workflow` instead of defaulting to the Xcode workflow.
- [x] Update package-facing `AGENTS.md` assets and maintainer docs to reflect the new SwiftPM-first versus Xcode-managed boundary.
- [x] Replace the old non-Xcode Swift future-direction placeholder in the maintainer atlas with the shipped `swift-package-workflow` surface.

Exit criteria:

- [x] The repo ships a dedicated SwiftPM execution skill, the Xcode workflow is more tightly scoped, and package-facing docs consistently route ordinary package work through the new boundary.
- [x] Completed 2026-04-07 by adding `swift-package-workflow`, tightening `xcode-app-project-workflow`, and updating package-facing handoffs and maintainer docs.

## Milestone 34: Execution Skill Split and Inference Refactor

Scope:

- Split the current execution workflows into narrower build-run and testing skills with stronger runtime inference so agents need fewer manual routing decisions.

Tickets:

- [x] Document the planned execution split, inference direction, and guidance-preservation contract in maintainer docs.
- [x] Start the first runtime-inference slice by teaching current execution wrappers to infer likely operation type from natural request text.
- [x] Add `swift-package-build-run-workflow`.
- [x] Add `swift-package-testing-workflow`.
- [x] Convert `swift-package-workflow` into a compatibility surface for the narrower package execution skills.
- [x] Add `xcode-build-run-workflow`.
- [x] Add `xcode-testing-workflow`.
- [x] Convert `xcode-app-project-workflow` and `swift-package-workflow` into compatibility surfaces for one release cycle after the narrower skills land.
- [x] Strengthen repo-root, workspace, scheme, target, and test-surface inference in the new runtime wrappers.
- [x] Add specialized fallback inference for `.xctestplan`, package resources, and Metal-related signals.
- [x] Update docs, validators, and tests so the narrower execution matrix becomes the active long-term surface.

Exit criteria:

- [x] The repo ships narrower execution skills with stronger inference, and the old monolithic execution skills are no longer the primary long-term workflow surfaces.
- [x] Completed 2026-04-07 package-side by adding the narrower Swift package build/run and testing skills, converting `swift-package-workflow` into a compatibility surface, and updating package-facing docs, validators, and tests.
- [x] Continued 2026-04-07 Xcode-side by adding `xcode-build-run-workflow` and `xcode-testing-workflow`, converting `xcode-app-project-workflow` into a compatibility surface, and updating the surrounding docs, sync assets, validators, and tests.
- [x] Continued 2026-04-08 by teaching the narrower wrappers to infer nested package and Xcode roots, scheme and target hints, test-plan context, UI-test surfaces, and Metal-related signals, with richer payload context and fallback commands.
- [x] Continued 2026-04-08 by adding specialized package-resource fallback guidance, `.xctestplan`-aware compatibility routing, Xcode bundle-integration handoffs, and richer inferred context in the compatibility surfaces.
- [x] Continued 2026-04-08 by thinning the compatibility surfaces themselves so they stay routing-focused, with the package compatibility wrapper returning routing context instead of shadow command planning.

## Milestone 35: Swift/Xcode Repo-Maintenance Toolkit Profiles

Scope:

- Promote a first-class Swift/Xcode-aware `repo-maintenance-toolkit` direction that keeps the shipped Apple plugin self-contained for end users while remaining maintainable for repo authors.

Tickets:

- [x] Document the planned toolkit direction and profile model in maintainer docs.
- [x] Define the profile contract for `generic`, `swift-package`, and `xcode-app`.
- [x] Add the Swift/Xcode-aware toolkit profiles and bundle them into the shipped Apple plugin surface.
- [x] Update Apple bootstrap and guidance-sync skills to consume the shipped shared toolkit contract.
- [x] Reduce local vendored-toolkit duplication after the shared contract is proven and stable.

Exit criteria:

- [x] The canonical shipped Swift/Xcode-aware toolkit contract lives in this repository, and Apple workflow skills consume it through a stable shared profile surface.
- [x] Continued 2026-04-08 in this repo by making the vendored toolkit installer profile-aware, emitting `scripts/repo-maintenance/config/profile.env`, and teaching Apple bootstrap and guidance-sync skills to install the `swift-package` or `xcode-app` profile explicitly.
- [x] Completed 2026-04-08 by making the shipped Apple plugin self-contained, bundling the toolkit contract locally, and re-scoping docs and validation around a one-and-done install surface instead of an external contract owner.

## Milestone 36: Guidance Preservation and AGENTS Expansion

Scope:

- Ensure the execution-skill split does not lose any guidance from the current monolithic workflow skills, and promote durable policy into synced and bootstrapped `AGENTS.md` where that policy belongs.

Tickets:

- [x] Document the guidance-preservation contract and AGENTS expansion strategy in maintainer docs.
- [x] Audit the current monolithic workflow guidance into a concrete preservation matrix for the split.
- [x] Audit all current `xcode-app-project-workflow` and `swift-package-workflow` guidance areas against the future narrower skills.
- [x] Promote durable testing, package-resource, Metal handoff, file-membership, and Debug-versus-Release guidance into synced and bootstrapped `AGENTS.md` where appropriate.
- [x] Keep transient runtime mechanics in skill-local docs and wrappers instead of pushing them into repo policy.
- [x] Add validation coverage that checks the preserved-guidance contract after the split lands.

Exit criteria:

- [x] Every important guidance area from the current monolithic workflow skills still exists in one explicit maintained location after the split.
- [x] Completed 2026-04-08 by auditing the compatibility workflow guidance against the narrower skills and synced `AGENTS.md` assets, strengthening the bootstrap Xcode `AGENTS.md` template, and adding validator plus workflow-test coverage for the preserved-guidance contract.
