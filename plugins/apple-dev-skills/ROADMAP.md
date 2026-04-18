# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 18: Claude Code Plugin Extras](#milestone-18-claude-code-plugin-extras)
- [Milestone 21: Swift Cleanup Automation Exploration](#milestone-21-swift-cleanup-automation-exploration)
- [Milestone 24: MCP App UI for Configuration and Customization](#milestone-24-mcp-app-ui-for-configuration-and-customization)
- [Milestone 25: macOS Menu Bar Extra for Skill Controls](#milestone-25-macos-menu-bar-extra-for-skill-controls)
- [Milestone 26: Dash Direct MCP and Call Library](#milestone-26-dash-direct-mcp-and-call-library)
- [Milestone 27: Repo Self-Compliance and Install-Surface Audit](#milestone-27-repo-self-compliance-and-install-surface-audit)
- [Milestone 28: Use `Agent Plugin Skills` plugin selectively for plugin and export-surface alignment](#milestone-28-use-agent-plugin-skills-plugin-selectively-for-plugin-and-export-surface-alignment)
- [Milestone 29: Swift and Xcode Testing Offload Workflow](#milestone-29-swift-and-xcode-testing-offload-workflow)
- [Milestone 37: Apple UI Accessibility Workflow](#milestone-37-apple-ui-accessibility-workflow)
- [Milestone 38: DocC Workflow](#milestone-38-docc-workflow)
- [Milestone 39: Swift Package Index Workflow](#milestone-39-swift-package-index-workflow)
- [Milestone 40: SwiftUI UI Architecture Workflow](#milestone-40-swiftui-ui-architecture-workflow)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Keep `apple-dev-skills` as the canonical Apple, Swift, and Xcode workflow repository, with Apple-docs-first guidance, clear top-level export boundaries, and maintainable supporting tooling.

## Product Principles

- Keep root `skills/` as the canonical authored and exported surface.
- Keep Apple documentation requirements explicit and enforceable in the skill guidance.
- Keep plugin packaging thin and secondary to the workflow-authoring surface.
- Expand the repo deliberately instead of adding loosely related helper features ad hoc.

## Milestone Progress

- Milestone 18: Claude Code Plugin Extras - Planned
- Milestone 21: Swift Cleanup Automation Exploration - Planned
- Milestone 24: MCP App UI for Configuration and Customization - Planned
- Milestone 25: macOS Menu Bar Extra for Skill Controls - Planned
- Milestone 26: Dash Direct MCP and Call Library - Completed
- Milestone 27: Repo Self-Compliance and Install-Surface Audit - Completed
- Milestone 28: Use `Agent Plugin Skills` plugin selectively for plugin and export-surface alignment - Completed
- Milestone 29: Swift and Xcode Testing Offload Workflow - Planned
- Milestone 37: Apple UI Accessibility Workflow - Planned
- Milestone 38: DocC Workflow - Completed
- Milestone 39: Swift Package Index Workflow - Planned
- Milestone 40: SwiftUI UI Architecture Workflow - Completed

## Milestone 18: Claude Code Plugin Extras

### Status

Planned

### Scope

- [ ] Add Claude-only plugin enhancements on top of the shared Codex and Claude common denominator without making cross-ecosystem workflows depend on them.

### Tickets

- [ ] Flesh out `hooks/` for Claude-only automation where it clearly helps maintainers or end users.
- [ ] Add `bin/` helpers only for Claude-only convenience wrappers that do not become required for the shared workflow contract.
- [ ] Document which Claude-only extras are optional sugar versus canonical workflow behavior.
- [ ] Validate that Claude-only extras degrade gracefully when absent from Codex.

### Exit Criteria

- [ ] Claude-only plugin extras exist as clearly separated enhancements, and the core workflow remains usable through the shared skill surface in both ecosystems.

## Milestone 21: Swift Cleanup Automation Exploration

### Status

Planned

### Scope

- [ ] Explore a larger maintainer automation flow for the `format-swift-sources` -> `structure-swift-sources` -> `format-swift-sources` choreography without overclaiming determinism for agent-driven file splits.

### Tickets

- [ ] Evaluate a `codex exec`-friendly maintainer wrapper for sequential formatting and structure passes.
- [ ] Define a structured-output contract for any `codex exec` helper so it can report findings, changed files, blocked steps, and follow-up recommendations deterministically.
- [ ] Decide whether `codex exec` should remain an on-demand maintainer tool, become a wrapper around deterministic repo helpers, or stay limited to advisory and enrichment work.
- [ ] Evaluate a Codex GUI App Automation that runs the same choreography on a schedule, preferably in a dedicated worktree.
- [ ] Document the boundary between deterministic local scripts, `codex exec` enrichment, and Codex GUI background automation.
- [ ] Audit the handoff boundary between `structure-swift-sources` and the Xcode execution skills, especially for file moves, target membership changes, and other project-integrity-sensitive follow-through.
- [ ] Explore a SwiftSyntax-backed assist for `structure-swift-sources` file headers so optional fields such as `Key Types` and `See Also` can be suggested or prefilled without inventing `Purpose` or `Concern` text from thin air.
- [ ] Add a starter inventory helper for `structure-swift-sources` file headers that can emit a user-editable YAML inventory with discovered file paths and blank meaning-bearing fields before any future SwiftSyntax assist is layered in.
- [ ] Keep file splitting and concern detection agent-driven unless a later design proves a safer deterministic boundary.

### Exit Criteria

- [ ] The repo has a written decision and an approved implementation direction for higher-level Swift cleanup automation.

## Milestone 24: MCP App UI for Configuration and Customization

### Status

Planned

### Scope

- [ ] Add an MCP App surface for inspecting and adjusting skill configuration and customization state without hand-editing YAML.

### Tickets

- [ ] Design the MCP App scope for viewing effective customization state across skills.
- [ ] Define which edits should remain metadata-only versus which should affect runtime-enforced behavior.
- [ ] Add UI resources and tool wiring for reading templates, durable overrides, and effective merged config.
- [ ] Validate that MCP App edits preserve the same contracts as the script-based customization flow.
- [ ] Document how the MCP App surface relates to the existing script-based customization flow.

### Exit Criteria

- [ ] The repo ships a documented MCP App path for viewing and editing customization state, or has an explicit bounded design ready for implementation.

## Milestone 25: macOS Menu Bar Extra for Skill Controls

### Status

Planned

### Scope

- [ ] Explore a native macOS menu bar utility for local maintainer workflows around skill installation, customization, and quick actions.

### Tickets

- [ ] Define the minimum viable menu bar feature set for local maintainer use.
- [ ] Evaluate whether the app should be a thin shell around existing scripts and MCP surfaces or a richer native controller.
- [ ] Identify which repo-local actions are safe and useful from a menu bar context.
- [ ] Document how the menu bar app would coexist with Codex plugin wiring and any future MCP App customization UI.
- [ ] Decide whether the menu bar app belongs in this repo, a sibling repo, or a plugin-bundled local-development surface.

### Exit Criteria

- [ ] Maintainers have a documented plan for whether to build the menu bar app, what it should own, and where it should live.

## Milestone 26: Dash Direct MCP and Call Library

### Status

Completed

### Scope

- [x] Remove avoidable indirection in the Dash-docsets workflow by teaching direct MCP usage first and documenting the Dash.app localhost HTTP call structure as a direct fallback surface.

### Tickets

- [x] Audit `explore-apple-swift-docs` for places where wrapper scripts stand in for MCP usage the agent could perform directly.
- [x] Teach the skill to prefer direct Dash MCP calls when the MCP service is available.
- [x] Document the Dash.app localhost HTTP call structure clearly enough that the agent can use it directly when MCP is unavailable or incomplete.
- [x] Provide a compact library of common Dash example calls and docset targets.
- [x] Reconcile references and runtime helpers so the documented primary path and the actual preferred path match again.

### Exit Criteria

- [x] The Dash workflow teaches direct MCP usage first, documents the localhost HTTP structure as a real fallback, and ships a practical library of common example calls and docset targets.

Completed Milestone 26 by rewriting `explore-apple-swift-docs` to teach direct Xcode MCP, Dash MCP, and Dash localhost HTTP usage ahead of the maintainer helper wrapper, by adding a compact Dash call library with common example calls and docset targets, and by updating the repo validator so the public contract and supporting references stay aligned.

## Milestone 27: Repo Self-Compliance and Install-Surface Audit

### Status

Completed

### Scope

- [x] Keep this repository checked against its own skill, symlink, export-surface, and local-discovery guidance.

### Tickets

- [x] Verify that root docs, maintainer docs, and skill docs stay aligned with the top-level export model after future refactors.
- [x] Document any mismatch between repo docs and the actual top-level export surface so guidance reflects operational reality instead of stale packaging assumptions.

### Exit Criteria

- [x] Maintainers have a verified, reality-based local discovery and top-level export story for this repo, with docs and tooling updated to match what the repository actually ships.

Completed Milestone 27 by keeping the top-level `skills/` export story, local discovery symlinks, maintainer docs, and repo validator aligned with the live shipped surface, and by confirming that `bash .github/scripts/validate_repo_docs.sh` plus `uv run pytest` cover the intended self-compliance checks.

## Milestone 28: Use `Agent Plugin Skills` plugin selectively for plugin and export-surface alignment

### Status

Completed

### Scope

- [x] Use the adjacent `agent-plugin-skills` maintainer workflows only where they still help with plugin-shape, export-surface, and install-metadata alignment, while keeping this repo's own contract focused on top-level exports only.
- [x] Keep broader README and maintainer-doc standards anchored in `productivity-skills` rather than reopening a stale shared-docs-standards pass through `agent-plugin-skills`.

### Tickets

- [x] Keep the personal-scope `agent-plugin-skills` install current for work on this repository without reintroducing a nested packaged plugin tree here.
- [x] Use `maintain-plugin-repo` and `sync-skills-repo-guidance` only for the plugin-shape and export-surface checks that still belong in that repo's standards layer.
- [x] Confirm that repo docs already align with the current `productivity-skills` documentation standards before treating docs wording drift as a Milestone 28 blocker.
- [x] Align plugin metadata, export surfaces, ignores, and maintainer guidance with the current shared plugin standards without flattening repo-specific policy.
- [x] Remove stale nested packaging language while keeping the adjacent standards repo as the maintainer-only setup.

### Exit Criteria

- [x] The repository validates cleanly against the current shared plugin and export-surface standards that still apply here.
- [x] Repo docs, packaging metadata, marketplace wiring, and maintainer guidance describe the same live behavior without treating `agent-plugin-skills` as the owner of broader documentation standards.

Completed Milestone 28 by narrowing `agent-plugin-skills` to its still-relevant plugin and export-surface role, keeping broader documentation standards anchored in `productivity-skills`, and confirming through the repo validator plus maintainer-doc audit that the live repo shape already matches that narrower standards model.

## Milestone 29: Swift and Xcode Testing Offload Workflow

### Status

Planned

### Scope

- [ ] Design and ship a dedicated offload workflow for repetitive, noisy SwiftPM and Xcode build, test, preview, and diagnostics work so the main agent thread can stay focused on higher-signal reasoning and implementation.

### Tickets

- [ ] Audit the repetitive Swift and Xcode verification work that is currently handled inline.
- [ ] Decide which implementation surface should own the offload path.
- [ ] Define the input and output contract for the offload path so verification work can be delegated without losing decision-useful detail.
- [ ] Cover the highest-value offload cases first, including `swift build`, `swift test`, `xcodebuild`, preview refresh, diagnostics refresh, and noisy failure summarization.
- [ ] Document when the main agent should stay local versus when it should hand verification work to the offload path.
- [ ] Add validation or smoke-test coverage once the implementation surface is chosen.

### Exit Criteria

- [ ] Maintainers have one documented and validated way to offload repetitive Swift and Xcode verification work from the main agent thread.
- [ ] The offload path returns concise, decision-useful results without obscuring the underlying build or test evidence.

## Milestone 37: Apple UI Accessibility Workflow

### Status

Planned

### Scope

- [ ] Add a dedicated Apple accessibility workflow skill that covers SwiftUI, UIKit, and AppKit accessibility implementation and review.
- [ ] Keep the skill grounded in current Apple accessibility APIs, platform semantics, focus behavior, VoiceOver behavior, Dynamic Type or text sizing expectations, and reduced-motion or contrast-related system settings.

Chosen first-slice direction:

- [x] Ship the durable public surface as `apple-ui-accessibility-workflow`.
- [x] Keep the first implementation SwiftUI-first while still covering UIKit and AppKit bridge guidance.
- [x] Keep runtime UI accessibility verification and `.xctestplan` execution with `xcode-testing-workflow` instead of collapsing those mechanics into the accessibility skill.
- [x] Keep `swift-package-testing-workflow` lighter by limiting it to package-side semantic testing guidance plus explicit handoff conditions.

### Tickets

- [ ] Define the skill boundary so it owns Apple UI accessibility implementation and review work without duplicating the broader docs-routing or generic repo-accessibility workflows.
- [ ] Gather the core Apple documentation references for SwiftUI, UIKit, AppKit, accessibility traits, labels, actions, announcements, focus, and testing surfaces.
- [ ] Ship a workflow surface that can help with both new implementation and review of existing Apple UI code.
- [ ] Cover the differences and overlap between SwiftUI accessibility modifiers, UIKit accessibility properties, and AppKit accessibility APIs.
- [ ] Document practical verification expectations, including simulator or device testing, VoiceOver checks, focus-order review, and content-scaling or motion-related checks where relevant.
- [ ] Add tests and maintainer docs once the workflow shape is stable.

### Exit Criteria

- [ ] The repository ships a documented Apple accessibility workflow skill for SwiftUI, UIKit, and AppKit work.
- [ ] The workflow clearly distinguishes framework-specific guidance from shared Apple accessibility principles and verification expectations.

## Milestone 38: DocC Workflow

### Status

Completed

### Scope

- [x] Add a dedicated DocC workflow skill for authoring, organizing, and reviewing Apple documentation content in Swift package and Xcode app or framework repositories.
- [x] Keep the first version centered on symbol documentation, articles, extension files, landing pages, topic groups, and correctness review, with explicit handoffs to the existing execution skills when the work becomes generation, export, or project-integrity heavy.
- [x] Treat DocC tutorials as a recognized but lighter first-pass surface in phase one, and defer deeper tutorial-authoring mechanics until a later follow-up.

### Tickets

- [x] Define the skill boundary so it owns DocC authoring and review guidance without absorbing generic Markdown maintenance work or duplicating the existing execution skills.
- [x] Gather the Apple Xcode documentation plus the fuller Swift.org DocC references needed for catalogs, articles, symbol links, directives, and structure guidance.
- [x] Ship a workflow surface that helps maintainers create, revise, and review DocC content in Swift package and Xcode repository shapes.
- [x] Teach the distinction between content correctness, DocC correctness, and project correctness so the skill stays honest about what it can verify directly.
- [x] Cover common failure modes such as broken symbol links, weak summaries, extension-file targeting mistakes, navigation drift, and catalog-structure mismatches.
- [x] Keep tutorial coverage phase-one light: classify tutorial-shaped requests, review conceptual flow at a high level, and route deeper directive-specific work to the fuller DocC references until the skill grows a dedicated tutorial-authoring phase.
- [x] Document the explicit handoffs to `swift-package-build-run-workflow`, `xcode-build-run-workflow`, and `explore-apple-swift-docs`.
- [x] Keep hosting and publishing guidance as a documented follow-up phase unless the first version proves it needs to absorb more.
- [x] Add tests and maintainer docs once the workflow shape is stable.

### Exit Criteria

- [x] The repository ships a documented DocC workflow skill with clear authoring and review guidance for Swift package and Xcode app or framework repos.
- [x] The workflow explains its handoff boundary cleanly instead of trying to own both content work and all DocC execution paths at once.

Completed Milestone 38 by shipping `author-swift-docc-docs`, adding its runtime customization and tests, capturing the first-slice authoring and review boundary directly in the shipped docs, and keeping tutorial handling intentionally light in phase one.

## Milestone 39: Swift Package Index Workflow

### Status

Planned

### Scope

- [ ] Add a dedicated Swift Package Index workflow skill for package distribution, documentation hosting, build readiness, metadata, and submission or listing expectations.
- [ ] Cover the parts of SPI work that matter to maintainers shipping public Swift packages, including documentation hosting, build compatibility, supported platform metadata, README and package-surface expectations, and listing hygiene.

### Tickets

- [ ] Define the skill boundary so it owns SPI-specific distribution and hosting guidance without replacing the core Swift package build or testing workflows.
- [ ] Gather the relevant Swift Package Index documentation for package metadata, documentation hosting, build surfaces, listing or submission expectations, and compatibility signals.
- [ ] Ship a workflow surface that can help maintainers prepare a package for SPI, diagnose common SPI-facing build or docs issues, and understand what SPI is deriving from the repository.
- [ ] Cover the relationship between SPI docs hosting, DocC output, README quality, package metadata, and supported platform declarations.
- [ ] Document common SPI failure modes such as unsupported package structure, incomplete metadata, broken docs generation, or platform mismatch signals.
- [ ] Add tests and maintainer docs once the workflow shape is stable.

### Exit Criteria

- [ ] The repository ships a documented Swift Package Index workflow skill for package distribution and SPI-facing readiness work.
- [ ] The workflow clearly explains how SPI distribution, documentation hosting, and package metadata fit together for public Swift packages.

## Milestone 40: SwiftUI UI Architecture Workflow

### Status

Completed

### Scope

- [x] Add a dedicated SwiftUI workflow skill for application UI architecture and implementation across scenes, commands, environment, preferences, focus, and reusable view composition.
- [x] Keep the skill grounded in current Apple SwiftUI behavior for app structure and desktop-oriented SwiftUI surfaces instead of generic component-library advice or framework-agnostic UI theory.
- [x] Make the workflow explicitly resistant to common agent anti-patterns, especially the sprawling wrapper-heavy, state-scattering, over-abstracted, and environment-abusing shapes that codegen tools constantly try to introduce.

### Tickets

- [x] Define the skill boundary so it owns SwiftUI application UI architecture and composition guidance without replacing the lower-level Apple docs routing skill or the broader accessibility workflow.
- [x] Gather the core Apple documentation references for `App`, scenes, scene types, commands, command groups, focused values, scene-focused values, environment values, preferences, window and document structure, and view composition.
- [x] Cover practical SwiftUI app-structure topics including commands, command menus, command groups, scenes, scene identity, scene focus values, focused values, environment propagation, preference keys, and reusable component and view patterns.
- [x] Teach when to use `Environment`, when to prefer explicit dependency injection, when preferences are the right upward data-flow tool, and when neither should be used.
- [x] Cover anti-patterns directly, including stuffing everything into environment objects, building giant root views, inventing wrapper layers instead of small composable views, overusing preference keys, hiding control flow in modifiers, and pushing app-level command logic into unrelated leaf views.
- [x] Include guidance for desktop-centric SwiftUI surfaces such as menu commands, focused command handling, window or scene coordination, and top-level app structure where macOS-style SwiftUI differs from simpler iOS-only examples.
- [x] Add tests and maintainer docs once the workflow shape is stable.
- [ ] Future refinement: add explicit `UtilityWindow`, `WindowVisibilityToggle`, and `commandsRemoved()` follow-up guidance for deeper desktop utility-window coverage.
- [ ] Future refinement: expand desktop-oriented examples around native sidebar, inspector, and auxiliary-window command composition if the first release proves too compressed.

### Exit Criteria

- [x] The repository ships a documented SwiftUI UI architecture workflow skill that covers scenes, commands, environment, preferences, focus, and component composition.
- [x] The workflow gives maintainers concrete guardrails against common SwiftUI agent anti-patterns instead of only describing ideal patterns abstractly.

Completed Milestone 40 by shipping `swiftui-app-architecture-workflow`, grounding the workflow in current SwiftUI scene, command, focus, and environment behavior, adding desktop-oriented split-view and inspector guidance, and covering the shipped surface with repo-validator and targeted pytest checks.

## Backlog Candidates

- [ ] Record plausible future work that is not yet committed to a milestone.

## History

- Completed Milestones 1 through 17 by establishing the repository, shipping the core Apple skill bundle, improving portability and customization guidance, adding bootstrap and repo-sync workflows, extracting Apple docs exploration into its own skill, and cleaning up the install surface around the top-level export model.
- Completed Milestones 19 and 20 by shipping `format-swift-sources` and `structure-swift-sources` as distinct cleanup workflows with clear boundaries.
- Completed Milestones 22 and 23 by expanding deterministic TODO/FIXME ledger normalization and finishing the customization consolidation review. See `docs/maintainers/customization-consolidation-review.md`.
- Completed Milestones 27 and 28 by validating the top-level `skills/` export story against the live repo validator and tests, and by narrowing `agent-plugin-skills` usage to selective plugin and export-surface alignment while leaving broader docs standards with `productivity-skills`.
- Completed Milestones 30 through 36 by shrinking the customization surface, adding the repo-maintenance toolkit and shared extraction work, splitting execution workflows, and preserving guidance through the refactor.
- Collapsed the older first-slice planning docs for Milestones 37, 38, and 40 plus the standalone execution guidance-preservation matrix into this roadmap history and the still-live maintainer docs once those decisions were absorbed into the shipped skills, validator rules, and synced guidance assets.
