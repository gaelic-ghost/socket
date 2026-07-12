# Project Roadmap

Swift naming and persistence ownership are now standardized: each project explicitly selects a three-letter prefix, project-owned Swift filenames use concatenated Xcode-friendly names without `+`, runtime/domain values use bare names, `Model` is reserved for persistence, and `swiftdata-workflow` owns SwiftData guidance.

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
- [Milestone 21: Swift Cleanup Automation Exploration](#milestone-21-swift-cleanup-automation-exploration)
- [Milestone 24: MCP App UI for Configuration and Customization](#milestone-24-mcp-app-ui-for-configuration-and-customization)
- [Milestone 25: macOS Menu Bar Extra for Skill Controls](#milestone-25-macos-menu-bar-extra-for-skill-controls)
- [Milestone 26: Dash Direct MCP and Call Library](#milestone-26-dash-direct-mcp-and-call-library)
- [Milestone 27: Repo Self-Compliance and Install-Surface Audit](#milestone-27-repo-self-compliance-and-install-surface-audit)
- [Milestone 28: Use `Agent Portability Skills` plugin selectively for plugin and export-surface alignment](#milestone-28-use-agent-portability-skills-plugin-selectively-for-plugin-and-export-surface-alignment)
- [Milestone 29: Swift and Xcode Testing Offload Workflow](#milestone-29-swift-and-xcode-testing-offload-workflow)
- [Milestone 37: Apple UI Accessibility Workflow](#milestone-37-apple-ui-accessibility-workflow)
- [Milestone 38: DocC Workflow](#milestone-38-docc-workflow)
- [Milestone 39: Swift Package Index Workflow](#milestone-39-swift-package-index-workflow)
- [Milestone 40: SwiftUI UI Architecture Workflow](#milestone-40-swiftui-ui-architecture-workflow)
- [Milestone 41: Swift Package Extension Workflow](#milestone-41-swift-package-extension-workflow)
- [Milestone 42: Safari Extension And Control Workflow](#milestone-42-safari-extension-and-control-workflow)
- [Milestone 43: Client Auth, Keychain, and App Sync Workflow](#milestone-43-client-auth-keychain-and-app-sync-workflow)
- [Milestone 44: Swift OpenAPI Client Workflow](#milestone-44-swift-openapi-client-workflow)
- [Milestone 45: Icon Composer App Icon Workflow](#milestone-45-icon-composer-app-icon-workflow)
- [Milestone 46: AppKit App Architecture Workflow](#milestone-46-appkit-app-architecture-workflow)
- [Milestone 47: Xcode Coding Intelligence Workflow](#milestone-47-xcode-coding-intelligence-workflow)
- [Milestone 48: Core AI and Foundation Models Workflow Planning](#milestone-48-core-ai-and-foundation-models-workflow-planning)
- [Milestone 49: Apple Media and Audio Workflow Skills](#milestone-49-apple-media-and-audio-workflow-skills)
- [Milestone 50: Swift Lang Handoff And Compatibility](#milestone-50-swift-lang-handoff-and-compatibility)
- [Milestone 52: Apple Design Animation And Symbols Workflow Skills](#milestone-52-apple-design-animation-and-symbols-workflow-skills)
- [Milestone 53: DeviceCheck and App Attest Workflow](#milestone-53-devicecheck-and-app-attest-workflow)
- [Milestone 54: Apple Developer Provisioning and CloudKit Workflow](#milestone-54-apple-developer-provisioning-and-cloudkit-workflow)
- [Milestone 55: TipKit Workflow](#milestone-55-tipkit-workflow)
- [Milestone 56: Apple Imaging Foundations](#milestone-56-apple-imaging-foundations)
- [Milestone 57: Vision and Image Recognition](#milestone-57-vision-and-image-recognition)
- [Milestone 58: Camera, Depth, and Computational Capture](#milestone-58-camera-depth-and-computational-capture)
- [Milestone 59: ARKit Spatial, Face, and Body Sensing](#milestone-59-arkit-spatial-face-and-body-sensing)
- [Milestone 60: Video Codecs and Pixel Processing](#milestone-60-video-codecs-and-pixel-processing)
- [Milestone 61: Photos Library and Media Selection](#milestone-61-photos-library-and-media-selection)
- [Milestone 62: Media Expansion Audit and Socket Major Release](#milestone-62-media-expansion-audit-and-socket-major-release)
- [Backlog Candidates](#backlog-candidates)
- [History](#history)

## Vision

- Keep `apple-dev-skills` as the canonical Apple, Swift, and Xcode workflow repository, with Apple-docs-first guidance, clear top-level export boundaries, and maintainable supporting tooling.

## Product Principles

- Keep root `skills/` as the canonical authored and exported surface.
- Keep Apple documentation requirements explicit and enforceable in the skill guidance.
- Keep plugin packaging thin and secondary to the workflow-authoring surface.
- Keep standalone install behavior honest: Apple-only workflows should remain usable from `apple-dev-skills` alone through the Git-backed marketplace path, while repo-maintenance bootstrap and sync workflows should name their `productivity-skills` companion requirement and the optional `socket` marketplace path.
- Expand the repo deliberately instead of adding loosely related helper features ad hoc.
- Keep Swift package workflow guidance focused on the latest stable Swift toolchain minor and the previous stable minor. The current trait-enabled bootstrap floor is Swift `6.2`; newer stable Swift toolchains should be used when validated, and the documented floor/window should move forward as part of normal maintenance.

## Milestone Progress

### Declarative SwiftUI Component Alignment

- [x] Make self-contained, reactive, flexible, reusable declarative `View` components the required SwiftUI shape.
- [x] Remove external ViewModels as a recommended SwiftUI architecture and require view-local observable state to be owned with `@State`.
- [x] Add `swiftui-component-audit-workflow` for repeatable audits and repairs of collaborator injection, imperative coordination, state duplication, environment misuse, and unnecessary initializers.
- [x] Align SwiftUI guidance around direct SwiftData integration, existing and custom environment actions, preferences, focus, commands, bindings, and memberwise initializers.

- Milestone 21: Swift Cleanup Automation Exploration - Planned
- Milestone 24: MCP App UI for Configuration and Customization - Planned
- Milestone 25: macOS Menu Bar Extra for Skill Controls - Planned
- Milestone 26: Dash Direct MCP and Call Library - Completed
- Milestone 27: Repo Self-Compliance and Install-Surface Audit - Completed
- Milestone 28: Use `Agent Portability Skills` plugin selectively for plugin and export-surface alignment - Completed
- Milestone 29: Swift and Xcode Testing Offload Workflow - Planned
- Milestone 37: Apple UI Accessibility Workflow - Planned
- Milestone 38: DocC Workflow - Completed
- Milestone 39: Swift Package Index Workflow - Planned
- Milestone 40: SwiftUI UI Architecture Workflow - Completed
- Milestone 41: Swift Package Extension Workflow - Planned
- Milestone 42: Safari Extension And Control Workflow - Completed
- Milestone 43: Client Auth, Keychain, and App Sync Workflow - Planned
- Milestone 44: Swift OpenAPI Client Workflow - Completed
- Milestone 45: Icon Composer App Icon Workflow - Completed
- Milestone 46: AppKit App Architecture Workflow - Completed
- Milestone 47: Xcode Coding Intelligence Workflow - Completed
- Milestone 48: Core AI and Foundation Models Workflow Planning - Planned
- Milestone 49: Apple Media and Audio Workflow Skills - Completed
- Milestone 50: Swift Lang Handoff And Compatibility - In Progress
- Milestone 52: Apple Design Animation And Symbols Workflow Skills - In Progress
- Milestone 53: DeviceCheck and App Attest Workflow - Completed
- Milestone 54: Apple Developer Provisioning and CloudKit Workflow - Completed
- Milestone 55: TipKit Workflow - Completed
- Milestone 56: Apple Imaging Foundations - Completed
- Milestone 57: Vision and Image Recognition - Completed
- Milestone 58: Camera, Depth, and Computational Capture - Completed
- Milestone 59: ARKit Spatial, Face, and Body Sensing - Planned
- Milestone 60: Video Codecs and Pixel Processing - Planned
- Milestone 61: Photos Library and Media Selection - Planned
- Milestone 62: Media Expansion Audit and Socket Major Release - Planned

## Milestone 21: Swift Cleanup Automation Exploration

### Status

In Progress

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

## Milestone 28: Use `Agent Portability Skills` plugin selectively for plugin and export-surface alignment

### Status

Completed

### Scope

- [x] Use the adjacent `agent-portability-skills` maintainer workflows only where they still help with plugin-shape, export-surface, and install-metadata alignment, while keeping this repo's own contract focused on top-level exports only.
- [x] Keep broader README and maintainer-doc standards anchored in `productivity-skills` rather than reopening a stale shared-docs-standards pass through `agent-portability-skills`.

### Tickets

- [x] Keep the personal-scope `agent-portability-skills` install current for work on this repository without reintroducing a nested packaged plugin tree here.
- [x] Use `maintain-plugin-repo` and `sync-skills-repo-guidance` only for the plugin-shape and export-surface checks that still belong in that repo's standards layer.
- [x] Confirm that repo docs already align with the current `productivity-skills` documentation standards before treating docs wording drift as a Milestone 28 blocker.
- [x] Align plugin metadata, export surfaces, ignores, and maintainer guidance with the current shared plugin standards without flattening repo-specific policy.
- [x] Remove stale nested packaging language while keeping the adjacent standards repo as the maintainer-only setup.

### Exit Criteria

- [x] The repository validates cleanly against the current shared plugin and export-surface standards that still apply here.
- [x] Repo docs, packaging metadata, marketplace wiring, and maintainer guidance describe the same live behavior without treating `agent-portability-skills` as the owner of broader documentation standards.

Completed Milestone 28 by narrowing `agent-portability-skills` to its still-relevant plugin and export-surface role, keeping broader documentation standards anchored in `productivity-skills`, and confirming through the repo validator plus maintainer-doc audit that the live repo shape already matches that narrower standards model.

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
- [ ] Cover performance-sensitive Apple silicon package and Xcode workflows, including `OSSignposter`, `xctrace`, Time Profiler, Metal System Trace, Allocations, VM Tracker, Audio, MLX, local AI, and trace artifact reporting.
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
- [ ] Cover the parts of SPI work that matter to maintainers shipping public Swift packages, including documentation hosting, build compatibility, supported platform metadata, README compatibility badges, package-surface expectations, and listing hygiene.

### Tickets

- [ ] Define the skill boundary so it owns SPI-specific distribution and hosting guidance without replacing the core Swift package build or testing workflows.
- [x] Gather the relevant Swift Package Index documentation for package metadata, documentation hosting, build surfaces, listing or submission expectations, and compatibility signals.
- [ ] Ship a workflow surface that can help maintainers prepare a package for SPI, diagnose common SPI-facing build or docs issues, and understand what SPI is deriving from the repository.
- [ ] Integrate the Socket `scripts/spi_add_package.py` one-shot readiness, issue-form, Zen, and Codex Computer Use handoff contract into the workflow.
- [ ] Explicitly forbid non-form PackageList actions, including `gh issue create`, manual label edits, PackageList forks, `packages.json` edits, PackageList branches, PackageList PRs, and CLA-triggering contribution paths.
- [ ] Cover the relationship between SPI docs hosting, DocC output, README quality, package metadata, and supported platform declarations.
- [ ] Document the post-indexing badge workflow for copying SPI-generated shields.io Swift-version and platform compatibility badges into README preambles.
- [ ] Document common SPI failure modes such as unsupported package structure, incomplete metadata, broken docs generation, or platform mismatch signals.
- [ ] Add tests and maintainer docs once the workflow shape is stable.

Research note: the current supported listing path is the Swift Package Index Add Package issue workflow in `SwiftPackageIndex/PackageList`, not a manual-first `packages.json` edit. Socket owns the durable add-package automation contract in [`../../docs/maintainers/spi-add-package-automation-plan.md`](../../docs/maintainers/spi-add-package-automation-plan.md).

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
- [x] Teach when to use `Environment`, values/bindings/actions, custom environment actions, and preferences as the right upward data-flow tool, and when neither should be used.
- [x] Cover anti-patterns directly, including stuffing everything into environment objects, building giant root views, inventing wrapper layers instead of small composable views, overusing preference keys, hiding control flow in modifiers, and pushing app-level command logic into unrelated leaf views.
- [x] Include guidance for desktop-centric SwiftUI surfaces such as menu commands, focused command handling, window or scene coordination, and top-level app structure where macOS-style SwiftUI differs from simpler iOS-only examples.
- [x] Add tests and maintainer docs once the workflow shape is stable.
- [ ] Future refinement: add explicit `UtilityWindow`, `WindowVisibilityToggle`, and `commandsRemoved()` follow-up guidance for deeper desktop utility-window coverage.
- [ ] Future refinement: expand desktop-oriented examples around native sidebar, inspector, and auxiliary-window command composition if the first release proves too compressed.

### Exit Criteria

- [x] The repository ships a documented SwiftUI UI architecture workflow skill that covers scenes, commands, environment, preferences, focus, and component composition.
- [x] The workflow gives maintainers concrete guardrails against common SwiftUI agent anti-patterns instead of only describing ideal patterns abstractly.

Completed Milestone 40 by shipping `swiftui-app-architecture-workflow`, grounding the workflow in current SwiftUI scene, command, focus, and environment behavior, adding desktop-oriented split-view and inspector guidance, and covering the shipped surface with repo-validator and targeted pytest checks.

## Milestone 41: Swift Package Extension Workflow

### Status

Planned

### Scope

- [ ] Add a dedicated SwiftPM package-extension workflow for package plugins, Xcode-capable package plugins, Swift macros, package traits, generated source, plugin permissions, and trait-aware build or test planning.
- [ ] Keep this workflow package-first while giving agents clear handoff rules for Xcode-managed execution, Xcode project plugin context, generated build products, macro expansion inspection, and package-trait matrices.
- [ ] Treat this as a durable building-block change: it keeps `swift-package-build-run-workflow` from becoming a broad catch-all again and gives package-extension work one explicit owner.
- [ ] Keep the active Swift support window focused on the latest stable minor and previous stable minor. Current minimum implementation floor: Swift `6.2`.

### Design Direction

- [ ] Ship the skill as `swift-package-extension-workflow`.
- [ ] Keep `swift-package-build-run-workflow` focused on ordinary manifest, dependency, resource, build, and run work, and route plugin, macro, trait, and generated-source questions into the new skill.
- [ ] Keep `swift-package-testing-workflow` focused on tests, fixtures, `.xctestplan`, profiling evidence, and test diagnosis, but teach it to hand off trait-matrix or macro/plugin test-shape work when the package-extension concern is primary.
- [ ] Keep `swift-package-workflow` as a compatibility router, not a second detailed implementation surface.
- [ ] Keep tool-specific formatter or linter plugin details in `format-swift-sources`, while linking back to the general package-extension workflow for plugin policy, permissions, generated files, and Xcode handoffs.

### Planned Reference Structure

- [ ] `package-plugins-build-command-and-xcode.md`: distinguish build tool plugins, command plugins, Xcode-capable command plugins, plugin products, target plugin usage, and when Xcode-managed context matters.
- [ ] `plugin-permissions-sandbox-and-outputs.md`: document write permissions, network permissions, sandbox behavior, generated outputs, cache/output directories, CI repeatability, and user-facing permission reasons.
- [ ] `swift-macros-package-shape.md`: document macro package shape, compiler-plugin dependencies, macro target boundaries, expansion inspection, diagnostics, and tests.
- [ ] `package-traits-feature-flags.md`: document trait design, default traits, explicit consumer choices, optional dependencies, `swift package show-traits`, `--traits`, `--enable-all-traits`, and `--disable-default-traits`.
- [ ] `generated-source-and-build-products.md`: document what should be generated at build time, what should be checked in, and when a plugin is more ceremony than value.
- [ ] `xcode-handoff-conditions.md`: document when package extension work should move to `xcode-build-run-workflow`, including Xcode project plugin context, app-hosted execution, generated file membership, and scheme/destination-sensitive behavior.
- [ ] `cli-command-matrix.md`: include command plugin listing and execution, trait commands and flags, macro-related build/test checks, and Xcode-aware fallback commands.

### Implementation Slices

- [ ] Slice 1: add the new skill skeleton, workflow references, docs anchors, and initial runtime router contract.
- [ ] Slice 2: update existing SwiftPM skills to route plugin, macro, trait, and generated-source work into `swift-package-extension-workflow`.
- [ ] Slice 3: update shared Swift package snippets, bootstrap guidance, and sync assets with the current Swift `6.2` floor, the latest stable Swift toolchain window, and trait-aware package guidance.
- [ ] Slice 4: add tests for skill metadata, routing, reference presence, command planning, support-window enforcement, and guidance-sync preservation.
- [ ] Slice 5: run the docs validator, pytest suite, and any focused bootstrap dry-run checks needed before release.

### Docs Anchors To Gather

- [ ] Swift Package Manager package plugin APIs, including build tool plugins, command plugins, plugin products, target plugin usage, permissions, and Xcode project plugin contexts. Start from the Swift Package Manager [PackageDescription API](https://docs.swift.org/package-manager/PackageDescription/index.html), Apple [`PackageDescription`](https://developer.apple.com/documentation/packagedescription), and Swift Evolution [SE-0303](https://forums.swift.org/t/se-0303-package-manager-extensible-build-tools/45106).
- [ ] Swift macros language and package-shape documentation, including compiler-plugin dependencies and expansion/diagnostic behavior. Start from Apple [Applying Macros](https://developer.apple.com/documentation/swift/applying-macros) and Swift Evolution [SE-0394](https://forums.swift.org/t/accepted-se-0394-package-manager-support-for-custom-macros/64589).
- [ ] Swift Package Manager package traits documentation and evolution context, especially defaults, explicit trait selection, disabled defaults, optional dependencies, and command-line flags. Start from `swift package --help`, `swift package show-traits --help`, and Swift Evolution [SE-0450](https://forums.swift.org/t/accepted-with-modifications-se-0450-package-traits/76705).
- [ ] Xcode documentation for package plugins that run from Xcode or need Xcode-managed project context. Start from Apple PackageDescription plugin surfaces and verify active Xcode behavior with local Xcode documentation or Xcode itself before claiming project-plugin behavior.

### Exit Criteria

- [ ] The repository ships `swift-package-extension-workflow` as the explicit owner for SwiftPM package plugins, macros, traits, generated source, and Xcode-capable package plugin guidance.
- [ ] Existing Swift package skills route extension work to the new skill without duplicating its policy.
- [ ] Bootstrap and guidance-sync outputs encode the Swift `6.2` floor and allow newer stable Swift toolchains after validation.
- [ ] The skill is covered by repo validation and targeted tests.

## Milestone 42: Safari Extension And Control Workflow

### Status

Completed

### Scope

- [x] Add a dedicated Safari workflow for choosing between Safari Web Extensions, Safari Web Inspector Extensions, Safari App Extensions, content blockers, SafariServices APIs, app-to-extension messaging, authentication surfaces, and external automation fallbacks.
- [x] Keep the workflow docs-first and explicit about Apple-documented Safari behavior before implementation choices.
- [x] Teach agents to treat "control Safari from a macOS app" as a scoped integration question rather than assuming unrestricted browser control.
- [x] Keep Xcode target, signing, entitlement, build, run, and testing work routed into the existing Xcode skills.

### Tickets

- [x] Add `safari-extension-control-workflow` with repo-standard skill metadata, OpenAI interface metadata, customization contract files, and shared Xcode policy snippet coverage.
- [x] Add references for extension-shape choice, Safari Web Inspector Extensions, SafariServices control surfaces, messaging and shared data, permissions, testing, debugging, and distribution.
- [x] Add targeted pytest coverage for extension-shape boundaries, supported control surfaces, messaging contexts, privacy posture, and explicit handoffs.
- [x] Update the active skill inventory, repo validator, shared-snippet sync script, README, and customization review counts.

### Exit Criteria

- [x] The repository ships `safari-extension-control-workflow` as the explicit owner for Safari extension and SafariServices integration-shape guidance.
- [x] The workflow keeps WebExtension, Safari Web Inspector Extension, Safari App Extension, content blocker, authentication, and external automation paths distinct.
- [x] The skill is covered by repo validation and targeted tests.

## Milestone 43: Client Auth, Keychain, and App Sync Workflow

### Status

Planned

### Scope

- [ ] Add a dedicated Apple client workflow for app-side authentication, secure credential storage, and sync behavior in iOS, macOS, and related Apple-platform apps.
- [ ] Keep Keychain, ASWebAuthenticationSession, Sign in with Apple, URLSession credential handling, token refresh, background refresh, and app-side sync guidance grounded in current Apple documentation.
- [ ] Keep this client workflow separate from server-side authentication, server persistence, OpenAPI, and RPC guidance while documenting clear handoffs to those plugins when an app crosses that boundary.

### Tickets

- [ ] Define the skill boundary so it owns Apple client auth, Keychain storage, credential refresh, and app-side sync without duplicating server authentication or transport-contract workflow.
- [ ] Gather Apple documentation anchors for Keychain Services, Authentication Services, Sign in with Apple, URLSession authentication, background tasks, push notification handoffs, and relevant data-protection behavior.
- [ ] Add guidance for token storage, refresh timing, logout and credential revocation, multi-account behavior, app group or extension sharing, and operator-facing auth errors.
- [ ] Add app-sync guidance for local cache shape, offline edits, conflict handling, change tokens or cursors, retry behavior, background refresh, and user-visible sync status.
- [ ] Define handoffs to `server-side-swift` for backend auth and sync contracts, and to OpenAPI or RPC skills when generated clients or transport schemas are the primary concern.
- [ ] Add tests and maintainer docs once the workflow shape is stable.

### Exit Criteria

- [ ] The repository ships an Apple client auth and app-sync workflow skill with clear Keychain, authentication, credential-refresh, and sync-state guidance.
- [ ] The workflow clearly separates client responsibilities from server authentication, persistence, OpenAPI, and RPC concerns.

## Milestone 44: Swift OpenAPI Client Workflow

### Status

Completed

### Scope

- [x] Add an Apple-platform client-side workflow for generated Swift OpenAPI clients, keeping app integration separate from server-side Vapor and Hummingbird transports.
- [x] Require Apple and Swift docs checks for `URLSession`, SwiftPM plugins, Xcode package integration, app lifecycle, and UI-state behavior before making design or implementation claims.
- [x] Keep server API contract and transport changes handed off to the server-side Swift plugin instead of making Apple Dev Skills own backend behavior.

### Tickets

- [x] Add `swift-openapi-client-workflow` with guidance for `swift-openapi-generator`, `OpenAPIRuntime`, `OpenAPIURLSession`, `URLSessionTransport`, generated `Client`, response handling, cancellation, and app-facing service boundaries.
- [x] Add skill interface metadata for the plugin directory.
- [x] Update Apple Dev Skills plugin metadata, README active skill inventory, and roadmap status.

### Exit Criteria

- [x] Apple app agents have a first stop for generated OpenAPI clients.
- [x] The workflow keeps generated client code out of UI views when a small app-facing service is the cleaner boundary.
- [x] The workflow names server-side OpenAPI/RPC, Xcode build/run, Xcode testing, Swift package, and docs-exploration handoffs.

## Milestone 45: Icon Composer App Icon Workflow

### Status

Completed

### Scope

- [x] Add a dedicated Icon Composer workflow skill for Apple app icon production across brief intake, source artwork preparation, GUI guidance, preview export, and Xcode handoff.
- [x] Keep the workflow docs-first and explicit about current Apple Icon Composer behavior before design or integration choices.
- [x] Prefer mature Mac-native artwork tools such as Pixelmator Pro, Acorn 8, and Retrobatch when image editing or batch export work is needed.
- [x] Include Computer Use guidance for operating Icon Composer's GUI without silently making destructive file or project changes.
- [x] Preserve the future packaged Mac App Store agent direction without folding that product into the first skill implementation.

### Exit Criteria

- [x] The repository ships `icon-composer-app-icon-workflow` as the explicit owner for Icon Composer app icon production guidance.
- [x] The workflow names `ictool` preview export, source artwork preparation, Computer Use, and Xcode workflow handoffs without pretending the design pass is fully automated.

## Milestone 46: AppKit App Architecture Workflow

### Status

Completed

### Scope

- [x] Add a dedicated AppKit workflow skill for macOS app architecture across app delegates, menu bar apps, responder-chain menus, windows, controllers, restoration, archiving, Observation, and mixed AppKit/SwiftUI composition.
- [x] Keep the skill grounded in current Apple AppKit behavior instead of treating AppKit as legacy-only or steering macOS apps toward SwiftUI by default.
- [x] Make the workflow explicitly resistant to common agent anti-patterns, especially SwiftUI-only steering, catch-all app delegates, controller dumping grounds, restoration-as-storage, unsafe archives, hidden command buses, and split ownership across AppKit and SwiftUI.

### Tickets

- [x] Define the skill boundary so it owns AppKit application architecture guidance without replacing the lower-level Apple docs routing skill, SwiftUI architecture workflow, accessibility workflow, or Xcode execution workflows.
- [x] Cover practical AppKit app-structure topics including `NSApplication`, app delegates, status items, menu bar apps, activation policy, menus, responder-chain actions, menu validation, windows, controllers, panels, inspectors, restoration, documents, and workspaces.
- [x] Cover AppKit MVC, target/action, delegates, bindings, object archiving, persistence choices, migration boundaries, and Observation/AppKit interop.
- [x] Cover mixed AppKit/SwiftUI composition through `NSHostingView`, `NSHostingController`, representable bridges, and single-owner state guidance.
- [x] Add tests and maintainer docs once the workflow shape is stable.

### Exit Criteria

- [x] The repository ships a documented AppKit app architecture workflow skill that covers menu bar apps, responder-chain menus, window/controller ownership, restoration, MVC, archiving, Observation, and mixed AppKit/SwiftUI composition.
- [x] The workflow gives maintainers concrete guardrails against AppKit undercoverage and framework-bias anti-patterns.

Completed Milestone 46 by shipping `appkit-app-architecture-workflow`, grounding the workflow in AppKit app lifecycle, status-item, responder-chain, controller, restoration, archiving, Observation, and hosting boundaries, adding reference files for the major AppKit architecture surfaces, and covering the shipped surface with repo-validator and targeted pytest checks.

## Milestone 47: Xcode Coding Intelligence Workflow

### Status

Completed

### Scope

- [x] Add a dedicated Xcode coding-intelligence workflow for Xcode Intelligence setup, Xcode-hosted agents, external-agent access through `xcrun mcpbridge`, command and tool permissions, Xcode-only agent configuration homes, and setup handoffs.
- [x] Keep build, run, preview, file-membership, and project-integrity execution with `xcode-build-run-workflow`.
- [x] Keep Swift Testing, XCTest, XCUITest, and `.xctestplan` execution with `xcode-testing-workflow`.
- [x] Mark Xcode 27 beta claims with the date checked and separate them from local Xcode 26.5 `mcpbridge` evidence.

### Tickets

- [x] Ship `xcode-coding-intelligence-workflow` with setup, agent-surface, MCP bridge, permission, artifact, and source-evidence references.
- [x] Add plugin metadata and README inventory entries for the new workflow.
- [x] Update `xcode-build-run-workflow` and `xcode-testing-workflow` so setup and permission questions route to the new workflow.
- [x] Add targeted tests for the new workflow and routing boundaries.

### Exit Criteria

- [x] The repository ships a documented Xcode coding-intelligence workflow skill.
- [x] Existing Xcode execution skills keep execution ownership while linking to the setup workflow only where needed.
- [x] Beta-specific claims are dated, source-linked, and separated from stable or local-tool evidence.

Completed Milestone 47 by shipping `xcode-coding-intelligence-workflow`, updating the active skill inventory and plugin metadata, adding routing notes from build/test execution skills, and covering the new setup and permission boundary with targeted tests.

## Milestone 48: Core AI and Foundation Models Workflow Planning

### Status

Planned

### Scope

- [ ] Decide which Apple Dev Skills workflow should own app-facing Foundation Models guidance, including on-device models, Private Cloud Compute, dynamic profiles, multimodal prompts, Vision tools, Spotlight-backed retrieval, evaluations, and provider packages.
- [ ] Decide whether Core AI model conversion, optimization, and runtime work belongs in Apple Dev Skills, a future Socket `coreai-skills` child plugin, or a handoff to Apple-owned `coreai-models` skills.
- [ ] Keep stable Apple Intelligence and Core AI pages, beta Foundation Models claims, and Apple GitHub open-source projects separated by status and date checked.

### Tickets

- [ ] Record the first detailed root Socket plan for Core AI and Foundation Models workflow ownership.
- [ ] Gather official Apple source anchors for Apple Intelligence, Core AI, Foundation Models, Private Cloud Compute, Core AI Models, Core AI PyTorch Extensions, and Core AI Optimization.
- [ ] Treat Music Intelligence and Media Analyzer as open investigation items until an official Apple developer documentation or source surface is verified.
- [ ] Define handoffs to future `mlx-skills` and `coreml-skills` so Apple Dev Skills does not absorb model conversion, model packaging, or ML runtime maintenance by accident.
- [ ] Add a first app-facing workflow only after the ownership split is clear enough to avoid a catch-all AI skill.

### Exit Criteria

- [ ] Maintainers have a source-linked ownership decision for Foundation Models, Core AI, MLX, Core ML, and adjacent Apple Intelligence workflows.
- [ ] Any shipped skill distinguishes stable, beta, and open-source exploratory surfaces.

## Milestone 49: Apple Media and Audio Workflow Skills

### Status

Completed

### Scope

- [x] Add focused Apple media and audio workflow skills for AVFAudio, AVFoundation, Core Media, and Core Audio modernization work.
- [x] Treat repair and modernization of existing poor-quality implementations as first-class workflows, not as afterthoughts behind greenfield examples.
- [x] Keep each workflow docs-first, with current Xcode or Apple Developer Documentation preferred for modern behavior and Apple documentation archive material used only for legacy Core Audio context or migration research.
- [x] Keep Xcode build, run, signing, entitlements, target membership, simulator or device execution, and test mechanics routed into the existing Xcode execution skills.
- [x] Keep the first implementation focused on practical app and package code repair rather than broad media-authoring theory, codec encyclopedias, or speculative wrapper architecture.

### Planned Skill Split

- [x] Ship `avfaudio-session-workflow` as the explicit owner for app audio intent, audio-session categories, modes, options, activation and deactivation, permissions, interruptions, route changes, Bluetooth or AirPlay routing, capture-session audio-session interaction, and spoken-audio or call-adjacent behavior.
- [x] Ship `avaudio-engine-workflow` as the explicit owner for `AVAudioEngine`, node graph ownership, input and output nodes, player nodes, taps, source and sink nodes, `AVAudioFormat`, format conversion, manual rendering, offline processing, Audio Unit hosting through `AVAudioUnit`, and real-time callback safety.
- [x] Ship `avfoundation-media-pipeline-workflow` as the explicit owner for AVFoundation capture, playback, media assets, async asset loading, asset readers and writers, sample-buffer append back-pressure, export or transcode pipeline shape, and AVPlayer or AVCapture handoffs.
- [x] Ship `coremedia-timing-samplebuffer-workflow` as the explicit owner for `CMTime`, `CMTimeRange`, `CMClock`, `CMTimebase`, `CMFormatDescription`, `CMSampleBuffer`, attachments, readiness, presentation and decode timestamps, synchronization, and sample-buffer debugging.
- [x] Ship `coreaudio-modernization-repair-workflow` as the explicit owner for legacy Core Audio and Audio Toolbox repair, including when to keep low-level C APIs, when to migrate toward AVFAudio, how to inspect `OSStatus` failures, how to bridge `AudioStreamBasicDescription`, and how to avoid unsafe callback, pointer, and lifetime patterns.

### Repair Themes

- [x] Main-thread blocking repair for `AVCaptureSession.startRunning()`, media loading, export, and other blocking media operations.
- [x] Deprecated AVAsset synchronous property and `loadValuesAsynchronously(forKeys:)` modernization toward Swift concurrency and `AVAsyncProperty` loading.
- [x] Audio-session category, mode, option, activation, deactivation, route-change, and interruption repair, including `notifyOthersOnDeactivation` and headphones-disconnect behavior.
- [x] Microphone and capture permission repair, including `Info.plist` purpose-string gates, `AVAudioApplication.requestRecordPermission`, and `AVCaptureDevice` authorization paths.
- [x] AVAudioEngine graph repair for unattached nodes, illegal runtime graph mutation, mixer or channel-count breakage, format mismatch, missing input or output hardware, and manual-rendering misuse.
- [x] Real-time audio safety repair for render callbacks, taps, source nodes, sink nodes, allocation, locking, logging, actor isolation, and UI or main-actor leakage.
- [x] Sample-buffer timing repair for invalid or drifting `CMTime`, missing format descriptions, bad presentation or decode timestamp handling, dropped buffers, writer back-pressure, and incorrect real-time input configuration.
- [x] Legacy Core Audio repair for opaque `OSStatus` handling, unsafe pointer ownership, hand-rolled format structs, callback lifetime bugs, `AudioQueue` or Audio Unit code that should either be isolated behind a narrow boundary or replaced with AVFAudio.
- [x] Operator-facing media and audio error repair so logs explain the framework surface, operation, likely cause, and next inspection point instead of reporting vague audio or media failure strings.

### Planned Reference Structure

- [x] `session-policy-and-repair.md`: categories, modes, options, activation lifecycle, permission gates, interruptions, route changes, capture-session interaction, privacy expectations, and app-audio ownership.
- [x] `engine-graph-and-repair.md`: node graph construction, graph mutation, formats, taps, source and sink nodes, player scheduling, manual rendering, offline processing, and callback safety.
- [x] `media-pipeline-and-repair.md`: capture-session setup, queueing, audio/video outputs, player behavior, async media loading, asset readers and writers, export, and sample-buffer append policy.
- [x] `time-samplebuffer-and-repair.md`: `CMTime`, time ranges, clocks, timebases, format descriptions, sample buffers, attachments, timestamps, synchronization, and diagnostic probes.
- [x] `coreaudio-modernization-and-repair.md`: Core Audio and Audio Toolbox concepts, archive-only references, low-level API retention criteria, migration paths to AVFAudio, `OSStatus` diagnostics, and unsafe legacy patterns.
- [x] Cross-cutting repair anti-patterns are embedded in each workflow reference rather than centralized in a single large reference file.
- [x] Validation and handoff expectations are covered in `validation-and-handoffs.md`, `diagnostics-and-handoffs.md`, and each workflow's `Fallbacks and Handoffs`.

### Docs Anchors To Gather

- [x] AVFAudio and AVFoundation current documentation for `AVAudioSession`, `AVAudioApplication`, interruptions, route changes, `AVAudioEngine`, manual rendering, stereo and spatial capture, `AVCaptureSession`, `AVPlayer`, async asset loading, asset readers, asset writers, and sample-buffer APIs.
- [x] Core Media current documentation for `CMTime`, `CMTimeRange`, `CMClock`, `CMTimebase`, `CMFormatDescription`, `CMSampleBuffer`, sample attachments, and sample-buffer renderer synchronization.
- [x] Core Audio and Audio Toolbox current documentation for `AudioStreamBasicDescription`, `AudioComponentDescription`, `AudioUnit`, `AudioQueue`, `AudioConverter`, and `OSStatus`-based diagnostics.
- [x] Apple documentation archive pages for Core Audio Overview, Audio Session Programming Guide, Audio Queue Services, Audio Unit Programming Guide, and related legacy material, clearly marked as historical or migration context rather than default modern guidance.
- [x] Current Apple sample-code or guide anchors for camera capture, audio capture, offline audio processing, route changes, interruptions, asset loading, asset writing, and sample-buffer playback where available.

### Implementation Slices

- [x] Slice 1: add the milestone research notes and source-anchor list, then decide whether to ship all five workflows together or stage the first release around session, engine, and timing repair.
- [x] Slice 2: add the first skill skeletons, OpenAI interface metadata, customization contract files, and shared Xcode handoff wording.
- [x] Slice 3: add the reference files for session policy, engine graph repair, media pipelines, Core Media timing, Core Audio modernization, anti-patterns, and validation handoffs.
- [x] Slice 4: update README active skill inventory, plugin metadata, repo validator expectations, and any router or handoff notes from existing Xcode, SwiftUI, AppKit, accessibility, and docs-exploration skills.
- [x] Slice 5: add targeted tests for skill metadata, docs-gate language, repair anti-pattern coverage, deprecated API modernization guidance, Xcode handoffs, and active inventory preservation.
- [x] Slice 6: run the docs validator, targeted pytest files, full `uv run pytest`, and root Socket metadata validation before any release or marketplace refresh.

### Exit Criteria

- [x] The repository ships focused media and audio workflow skills instead of one catch-all AVFoundation skill.
- [x] Each workflow states the documented Apple behavior it relies on before recommending design or repair changes.
- [x] Repair guidance covers common existing-code failure modes for sessions, routes, interruptions, permissions, engine graphs, real-time callbacks, async media loading, sample-buffer timing, and legacy Core Audio code.
- [x] The skills keep execution mechanics with `xcode-build-run-workflow` and `xcode-testing-workflow` instead of silently claiming runtime validation they did not perform.
- [x] The active skill inventory, plugin metadata, tests, and docs validator agree with the shipped media and audio workflow surface.

Completed Milestone 49 by shipping five focused media and audio workflow skills: `avfaudio-session-workflow`, `avaudio-engine-workflow`, `avfoundation-media-pipeline-workflow`, `coremedia-timing-samplebuffer-workflow`, and `coreaudio-modernization-repair-workflow`. The first release keeps the workflows docs-first, repair-oriented, and explicit about Xcode execution handoffs while avoiding one broad catch-all media skill.

Follow-up hardening added a shared Apple media type ownership contract across the five media and audio workflows. The skills now strictly prefer AVFoundation, AVFAudio, Core Media, Core Audio, Audio Toolbox, and related Swift media types until an explicit app, package, test, wire, persistence, or cross-platform boundary makes those framework types unsuitable.

## Milestone 50: Swift Lang Handoff And Compatibility

### Status

Planned

### Scope

- [x] Preserve standalone `apple-dev-skills` behavior while Socket grows a dedicated `swift-lang` plugin for shared Swift language guidance.
- [x] Keep Apple Dev focused on Apple-platform docs, Xcode, SwiftUI, AppKit, UIKit, AVFoundation, AVFAudio, Core Media, Core Audio, DocC, Safari, SPI, and project-integrity workflows.
- [x] Route shared Swift style, formatting, source organization, functional data-flow, API ergonomics, and modernization cleanup guidance to `swift-lang` when that plugin is available.

### Tickets

- [x] Update Apple Dev skill handoffs so `format-swift-sources` and `structure-swift-sources` can point at `swift-lang` for shared-language cleanup without breaking Apple-only installs.
- [x] Keep Apple Dev's local formatting and structure skills available through the first `swift-lang` migration release.
- [ ] Decide in a later release whether Apple Dev should keep Apple-flavored wrappers or deprecate the local copies in favor of `swift-lang`.
- [x] Ensure Apple-specific skills continue to require Apple documentation before implementation changes, even when the Swift language style work comes from `swift-lang`.

### Exit Criteria

- [x] Apple Dev keeps its standalone install promise while Socket users get a cleaner shared Swift language layer.
- [x] Apple Dev docs and metadata explain the split between Apple-platform workflow ownership and shared Swift language cleanup ownership.

## Milestone 51: Xcode LLDB MCP Workflow

### Status

Planned

### Scope

- [ ] Add a dedicated Xcode 27 beta-era LLDB MCP workflow skill for debugger setup, target/session selection, breakpoint and expression workflows, crash investigation, and handoffs back to build/test skills.
- [ ] Keep the workflow docs-first and beta-gated until `xcrun lldb-mcp` startup, help output, tool inventory, and MCP client behavior are validated against an installed Xcode 27 beta.
- [ ] Keep Xcode-owned debugger integration separate from third-party debugger MCP servers and from normal `xcrun mcpbridge` project/build tools.

### Tickets

- [x] Add an experimental `xcode_lldb` MCP config entry that resolves through the selected Xcode toolchain with `xcrun lldb-mcp`.
- [ ] Capture `xcrun lldb-mcp --help`, startup behavior, and tool inventory from Xcode 27 Beta 2 or a later beta before claiming the config is stable.
- [ ] Document the observed Beta 2 rpath failure and the exact toolchain environment that fixes it, if Apple does not resolve the direct-launch issue in a later beta.
- [ ] Add the workflow skill, metadata, README inventory entry, and targeted tests after the launch and tool-surface evidence exists.

### Exit Criteria

- [ ] Apple Dev Skills exposes a debugger workflow that can safely decide when to use LLDB MCP, normal Xcode UI debugging, `lldb`, `lldb-dap`, or existing build/test handoffs.
- [ ] The plugin MCP config, README, skill guidance, and tests agree on whether `xcode_lldb` is experimental or stable.

## Milestone 52: Apple Design Animation And Symbols Workflow Skills

### Status

In Progress

### Scope

- [x] Add first-slice Apple design workflow skills for SF Symbols and SwiftUI animation.
- [x] Add second-slice workflow skills for Core Animation layer work and Apple typography/San Francisco font-family guidance.
- [x] Keep design, symbol, animation, typography, and app-icon ownership split across focused Apple Dev Skills instead of expanding `swiftui-app-architecture-workflow` into a catch-all UI skill.

### Tickets

- [x] Add `sf-symbols-workflow` for SF Symbols selection, app inspection, rendering modes, variable color, symbol effects, custom symbols, accessibility semantics, and Xcode integration handoffs.
- [x] Add `swiftui-animation-workflow` for state-driven SwiftUI animation, transitions, symbol effects in motion context, phase/keyframe animation, reduce-motion behavior, and validation handoffs.
- [x] Update Apple Dev plugin metadata, README active skill inventory, repo validator expectations, and targeted tests for the first slice.
- [x] Add `core-animation-layer-workflow` for `CALayer`, implicit and explicit animations, transactions, timing, shape/gradient/text layers, presentation-layer behavior, AppKit/UIKit bridging, and performance handoffs.
- [x] Add `apple-typography-workflow` for system typography APIs, San Francisco and New York system designs, Dynamic Type, accessibility, custom font boundaries, and redistribution warnings.
- [ ] Decide whether animated SF Symbols stay primarily in `sf-symbols-workflow` or whether `swiftui-animation-workflow` should own more symbol-effect implementation detail after field use.

### Exit Criteria

- [x] Apple Dev Skills has focused first-party guidance for SF Symbols, SwiftUI animation, Core Animation, and Apple typography without blurring architecture, app-icon, accessibility, and Xcode execution ownership.
- [x] The active skill inventory, plugin metadata, tests, and docs validator agree with the shipped design and animation workflow surface.

## Milestone 53: DeviceCheck and App Attest Workflow

### Status

Completed

### Scope

- [x] Add a dedicated Apple workflow for DeviceCheck and App Attest adoption in iOS, macOS, and related Apple-platform apps.
- [x] Keep `DCDevice` per-device two-bit state, `DCAppAttestService` key attestation, server challenges, assertions, receipts, fraud-risk metrics, App IDs, entitlements, sandbox/production behavior, rollout limits, and Xcode validation grounded in current Apple documentation.
- [x] Keep app-side framework use and client/server contract guidance separate from backend implementation, generated API clients, general auth, Keychain storage, or app-sync ownership.

### Tickets

- [x] Use [the DeviceCheck and App Attest skill plan](../../docs/maintainers/devicecheck-app-attest-skill-plan.md) as the implementation source of truth.
- [x] Add `devicecheck-app-attest-workflow` with clear routing between DeviceCheck two-bit state, App Attest app-instance integrity, broader client auth, and server-side validation implementation.
- [x] Add references for DeviceCheck device state, App Attest client flow, App Attest server validation, App ID and entitlement setup, sandbox/production behavior, rollout/rate-limit planning, and macOS-specific validation notes.
- [x] Add skill interface metadata and update Apple Dev Skills plugin metadata, README active skill inventory, and default prompt list.
- [x] Add targeted tests for skill frontmatter, docs-gate language, DeviceCheck/App Attest routing boundaries, server-handoff language, and metadata inventory.
- [x] Run the Apple Dev Skills docs validator and pytest when the skill lands, then run the Socket metadata validator after plugin metadata changes.

### Exit Criteria

- [x] The repository ships `devicecheck-app-attest-workflow` as the explicit owner for DeviceCheck and App Attest implementation-shape guidance.
- [x] The workflow states the documented Apple behavior it relies on before proposing app, entitlement, server-challenge, attestation, assertion, receipt, or rollout changes.
- [x] The workflow keeps server verification and API-contract implementation as explicit handoffs instead of hiding backend work inside Apple app guidance.

Completed Milestone 53 by adding `devicecheck-app-attest-workflow`, focused references for DeviceCheck state, App Attest client flow, server validation, and App ID/entitlement validation, plus plugin metadata, README inventory, shared snippet coverage, customization contract files, and targeted tests for routing, docs gates, and handoffs.

## Milestone 54: Apple Developer Provisioning and CloudKit Workflow

### Status

Completed

### Scope

- [x] Add a docs-first workflow for the official App Store Connect REST provisioning surface, Xcode-aware discovery, `cktool`, and CKTool JS.
- [x] Make team-key requirements, individual-key limits, Keychain/local-secret handling, short-lived JWTs, dry runs, and explicit mutation confirmation mandatory.
- [x] Keep App Groups, CloudKit container registration/assignment, Service IDs, and other undocumented configuration visibly portal-only.
- [x] Record the future interactive Apple Developer Portal Driver separately from the shipped official-API workflow.

### Exit Criteria

- [x] Apple Dev Skills ships `apple-developer-provisioning-workflow` with official and portal-only paths clearly separated.
- [x] The skill documents CloudKit management-token setup and safe `cktool` / CKTool JS boundaries without committing secrets.
- [x] Plugin metadata, README inventory, validator, and focused tests agree on the added skill.

Completed Milestone 54 by shipping `apple-developer-provisioning-workflow` with plan-first App Store Connect provisioning, local Xcode discovery handoffs, Keychain-backed CloudKit guidance, account/key prerequisites, and explicit portal-only fallbacks.

## Milestone 55: TipKit Workflow

### Status

Completed

### Scope

- [x] Add a docs-first TipKit workflow for SwiftUI, UIKit, and AppKit.
- [x] Cover one-time configuration, inline tips, tooltip popovers, actions, styling, eligibility, events, donations, invalidation, persistence, testing controls, and diagnosis.
- [x] Keep TipKit implementation direct instead of introducing a custom tooltip manager or mirrored state layer.

### Exit Criteria

- [x] Apple Dev Skills ships `tipkit-workflow` as the explicit owner for TipKit implementation and troubleshooting guidance.
- [x] Xcode documentation is the primary behavioral source, with Dash checked as the configured secondary local source.
- [x] Plugin metadata, README inventory, validator, roadmap, and focused tests agree on the added skill.

Completed Milestone 55 by shipping `tipkit-workflow` with focused presentation and lifecycle references, SwiftUI/UIKit/AppKit routing, deterministic test guidance, plugin metadata, inventory validation, and targeted tests.

## Milestone 56: Apple Imaging Foundations

### Status

Completed

### Scope

- [x] Add focused image-processing and image-representation workflows without expanding AVFoundation, AppKit architecture, or Core Animation into catch-all image skills.
- [x] Ship `core-image-processing-workflow` as the owner for `CIImage`, `CIContext`, built-in filters, RAW processing, custom kernels, color management, lazy evaluation, render destinations, and Core Image performance diagnostics.
- [x] Ship `apple-image-representation-workflow` as the owner for Image I/O, Core Graphics image values, AppKit and UIKit image representations, image metadata, incremental decoding, thumbnails, animation frames, and encoding.
- [x] Add a shared Apple image-type ownership contract that preserves framework types and makes orientation, scale, color-space, metadata, alpha, dynamic-range, and auxiliary-image loss explicit at every conversion boundary.
- [x] Keep image transformation separate from image interpretation: Core Image changes or renders pixels, while Vision analyzes their contents in Milestone 57.

### Framework Ownership

- [x] Core Image owns lazy processing graphs, filters, contexts, RAW development, custom kernels, and rendering into `CGImage`, `CVPixelBuffer`, `IOSurface`, or Metal-backed destinations.
- [x] Image I/O owns `CGImageSource`, `CGImageDestination`, format detection, incremental loading, thumbnail generation, multi-frame formats, metadata, properties, and auxiliary image data.
- [x] Core Graphics owns concrete raster images, drawing, color spaces, bitmap contexts, masks, and low-level image geometry.
- [x] AppKit owns `NSImage`, `NSImageRep`, `NSBitmapImageRep`, macOS drawing behavior, resolution-independent representations, and display-oriented image selection.
- [x] UIKit owns `UIImage` display conventions on iOS-family platforms; it does not replace Image I/O for controlled decode, encode, or metadata work.
- [x] Metal remains a handoff for custom GPU pipelines that exceed Core Image's documented filter and processor boundaries.

### Required Guidance

- [x] Explain that `CIImage` describes a lazily evaluated image recipe and does not become rendered pixel output until a context renders it.
- [x] Prefer reusing deliberately scoped `CIContext` instances; document context expense, caches, command-queue ownership, and the mutable-thread-safety boundary of filters.
- [x] Cover image extent, region of interest, tiling, cropping, premultiplication, alpha handling, working/output color spaces, HDR and extended-range data, and render format selection.
- [x] Cover downsampling at decode time, incremental sources, orientation metadata, image properties, animated or multi-frame sources, thumbnails, and destination finalization.
- [x] Explain `NSImage` representation selection and prevent accidental assumptions that one `NSImage` always contains one fixed bitmap at one scale.
- [x] Keep AppKit drawing helpers, Image I/O decoding, Core Image processing, and Core Graphics rendering as explicit cooperating boundaries instead of wrapping them in a generic image manager.

### Documentation Anchors

- [x] Refresh Xcode documentation for Core Image essentials, `CIImage`, `CIContext`, `CIFilter`, `CIRAWFilter`, custom kernels, render destinations, and color management during implementation.
- [x] Refresh Xcode documentation for Image I/O sources, destinations, incremental loading, properties, thumbnails, auxiliary data, and supported image formats during implementation.
- [x] Refresh Xcode documentation for `CGImage`, `CGColorSpace`, bitmap contexts, `NSImage`, `NSImageRep`, `NSBitmapImageRep`, `UIImage`, and platform-specific drawing behavior during implementation.
- [x] Use Dash only as the configured secondary local source when Xcode documentation is incomplete or when cross-symbol browsing is materially better there.

### Implementation and Review Gate

- [x] Add both skill directories, `SKILL.md` files, focused references, OpenAI interface metadata, customization contracts, and shared type-ownership guidance.
- [x] Review routing and handoffs against AVFoundation, Core Media, AppKit architecture, Core Animation, Xcode execution, and future Vision ownership.
- [x] Update the Apple Dev README, plugin metadata, active inventory validation, tests, and this roadmap before considering the milestone complete.
- [x] Run the docs validator, targeted tests, full Apple Dev test suite, and root Socket metadata validation serially.
- [x] Inspect the complete milestone diff for unsupported API claims, duplicated ownership, vague error guidance, and stale documentation before beginning Milestone 57.

### Exit Criteria

- [x] Apple Dev Skills provides a direct, docs-first path for image processing, decoding, encoding, metadata, representation, conversion, and macOS image tooling.
- [x] Image conversions preserve Apple types until an explicit boundary and identify every material loss of orientation, scale, metadata, color, dynamic range, or auxiliary data.
- [x] The new skills compose with the existing media workflows without making AVFoundation or AppKit architecture the owner of unrelated image work.

Completed Milestone 56 by shipping `core-image-processing-workflow` and `apple-image-representation-workflow`, a shared Apple image-type ownership and conversion-loss contract, focused processing, rendering, Image I/O, metadata, AppKit/UIKit bridging, and diagnostic references, plugin and README integration, synchronized Xcode guidance, customization contracts, and targeted inventory and behavior tests. Current Xcode documentation was checked for Core Image, Image I/O, Core Graphics, AppKit, and UIKit; both skill packages, the docs validator, 206 Apple Dev tests, and root Socket metadata validation passed before milestone closure.

## Milestone 57: Vision and Image Recognition

### Status

Completed

### Scope

- [x] Ship `vision-image-analysis-workflow` for Apple-provided image and video analysis requests, observations, request execution, tracking, segmentation, pose detection, feature prints, and coordinate conversion.
- [x] Ship `vision-coreml-recognition-workflow` for custom Core ML-backed classification, object detection, semantic segmentation, model input policy, compute selection, preprocessing, postprocessing, and regression evidence.
- [x] Keep Vision's image-analysis lifecycle separate from Core ML's model-execution lifecycle while documenting their intended integration through Vision Core ML requests.
- [x] Treat confidence values as model outputs rather than proof of identity, correctness, safety, or authorization.

### Framework Ownership

- [x] Vision owns image-oriented requests, handlers, observations, tracking, normalized coordinate systems, revisions, crop-and-scale policy, and Core ML image-model integration.
- [x] Core ML owns model loading, typed model inputs and outputs, compute-unit selection, prediction execution, model configuration, and model metadata.
- [x] Natural-language, sound, and tabular model tasks remain outside this image-focused milestone unless they are required to explain a clear handoff.
- [x] Core Image owns pixel preprocessing or presentation effects; it must not become a second recognition framework.
- [x] AVFoundation owns live capture and sample delivery; the Vision skills own analysis after a frame reaches the analysis boundary.

### Required Guidance

- [x] Cover text, barcode, face rectangle and landmark, rectangle, horizon, contour, saliency, trajectory, animal, body, and hand-pose requests where current platform documentation supports them.
- [x] Cover person and foreground segmentation, object tracking, feature prints, image similarity, request revisions, request cancellation, sequence handlers, and frame-dropping policy for live streams.
- [x] Explain image orientation, normalized Vision coordinates, lower-left versus upper-left origins, crop-and-scale behavior, preview-layer transforms, and bounding-box conversion back to source or display coordinates.
- [x] Cover `VNCoreMLModel` or its current documented successor surface, classification versus object detection, semantic segmentation, labels, confidence thresholds, nonmaximum suppression boundaries, and model-specific postprocessing.
- [x] Require pinned model provenance, repeatable fixtures, representative-device profiling, and a small regression or evaluation sanity check when model or request logic changes.
- [x] Keep face detection, face landmarks, and face tracking distinct from biometric identity and from Face ID authentication.

### Documentation Anchors

- [x] Refresh Xcode documentation for current Vision Swift and Objective-C request surfaces, request handlers, sequence analysis, observations, coordinate conversion, request revisions, and compute-stage behavior.
- [x] Refresh Xcode documentation for Core ML model integration, model configuration, compute units, image constraints, classification, object detection, and semantic segmentation.
- [x] Use current sample code where Xcode documentation exposes important lifecycle, concurrency, or coordinate behavior not apparent from symbol reference alone.

### Implementation and Review Gate

- [x] Add both skill directories, focused references, interface metadata, customization contracts, routing, and explicit camera/Core Image/Core ML handoffs.
- [x] Add tests for coordinate-system guidance, confidence semantics, model provenance, live-frame back-pressure, simulator/device claims, and Face ID boundary wording.
- [x] Update README, plugin metadata, active inventory, roadmap status, and cross-skill handoffs before completing the milestone.
- [x] Run targeted tests, docs validation, the full Apple Dev suite, and root Socket validation serially.
- [x] Review the milestone as a complete recognition surface before beginning camera and depth work.

### Exit Criteria

- [x] Apple Dev Skills can route built-in visual analysis and custom model-backed recognition without conflating Vision, Core ML, Core Image, AVFoundation, or biometric authentication.
- [x] Coordinate conversion, orientation, frame lifecycle, model confidence, evaluation evidence, and device-performance boundaries are explicit and test-covered.

Completed Milestone 57 by shipping `vision-image-analysis-workflow` and `vision-coreml-recognition-workflow`, a shared Vision coordinate, confidence, identity, and live-frame contract, focused built-in request, sequence, coordinate, custom Core ML integration, model provenance, evaluation, performance, and diagnostic references, plus plugin, README, inventory, customization, and cross-skill handoff updates. Current Xcode documentation was checked for the modern Swift Vision request surface, the original `VN*` API, image locations, request families, Vision/Core ML integration, model configuration, compute units, and image constraints; both skill packages, targeted tests, docs validation, 210 Apple Dev tests, and root Socket validation passed before milestone closure.

## Milestone 58: Camera, Depth, and Computational Capture

### Status

Completed

### Scope

- [x] Ship `camera-capture-depth-workflow` as the specialist owner for Apple camera discovery, camera configuration, photo and video capture controls, depth delivery, calibration, synchronized outputs, and computational capture features.
- [x] Keep `avfoundation-media-pipeline-workflow` as the general owner for capture-session topology, asset pipelines, playback, readers, writers, exports, back-pressure, and lifecycle handoffs.
- [x] Strengthen the existing AVFoundation workflow where necessary so ordinary capture remains there and only camera-sensor or depth-specialist requests route into the new skill.
- [x] Require capability discovery at runtime rather than assumptions based on product names or camera-count heuristics.

### Required Guidance

- [x] Cover built-in and virtual capture devices, discovery sessions, device formats, frame rates, multi-camera constraints, session presets, connections, rotation coordination, orientation, and mirroring.
- [x] Cover focus, exposure, white balance, zoom, torch, stabilization, low-light behavior, constituent-device switching, and configuration locking with descriptive failure diagnostics.
- [x] Cover processed and RAW photo capture, Live Photos, bracketed capture where supported, photo quality prioritization, responsive capture, and deferred photo delivery where supported.
- [x] Cover depth and disparity data, `AVDepthData`, `AVCaptureDepthDataOutput`, camera calibration data, intrinsic matrices, filtering, accuracy, quality, and alignment to color imagery.
- [x] Cover synchronized video, depth, audio, metadata, and data-output delivery through documented AVFoundation synchronizers and queue boundaries.
- [x] Cover portrait-effects mattes, semantic segmentation mattes, spatial photo or video capture, cinematic capture, and other computational features only where current documentation and capability checks support them.
- [x] Cover authorization, `Info.plist` purpose strings, interruptions, runtime errors, media-services reset, thermal pressure, bandwidth pressure, dropped data, cancellation, and teardown.
- [x] Require physical-device evidence before claiming camera topology, depth quality, calibration, LiDAR, TrueDepth, multi-camera, HDR, or computational capture behavior is verified.

### Documentation Anchors

- [x] Refresh Xcode documentation for capture setup, device discovery, formats, photo output, video data output, depth data output, output synchronization, calibration, portrait-effects mattes, semantic mattes, rotation, and capture-device controls.
- [x] Check current platform and hardware availability for every specialized capture feature while authoring its guidance.
- [x] Use Dash as a secondary local source when Xcode search does not expose a complete relationship among capture symbols.

### Implementation and Review Gate

- [x] Add the specialist skill, references, metadata, customization contract, tests, and shared camera-capability guidance.
- [x] Review and update `avfoundation-media-pipeline-workflow`, `avfaudio-session-workflow`, Core Media timing, Vision analysis, and Xcode device-execution handoffs in the same milestone.
- [x] Update README, plugin metadata, active inventory, roadmap status, validation expectations, and operator-facing error requirements.
- [x] Run targeted tests, docs validation, the full Apple Dev suite, and root Socket validation serially.
- [x] Perform a capture-boundary review before starting ARKit work so AVFoundation and ARKit do not duplicate ownership.

### Exit Criteria

- [x] Camera, photo, video, depth, calibration, synchronized output, and computational capture requests route to one clear specialist workflow.
- [x] The workflow distinguishes documented capability, simulator limitations, and physically verified device behavior.
- [x] General AVFoundation pipeline guidance remains coherent and does not become a competing camera-depth implementation path.

Completed Milestone 58 by shipping `camera-capture-depth-workflow`, a shared layered camera-capability and evidence contract, focused device discovery, format, control, rotation, photo, lifecycle, pressure, depth, calibration, synchronization, matte, and computational-capture references, plus AVFoundation, Vision, Core Image, plugin, README, inventory, customization, and test updates. Current Xcode documentation was checked for capture devices and formats, MultiCam, device controls, photo prioritization and responsiveness, Live Photos, depth and calibration, synchronized output and dropped data, rotation coordination, mattes, spatial video, cinematic capture, interruptions, authorization, and pressure; unsupported spatial-photo inference was explicitly rejected. The skill package, targeted tests, docs validation, 214 Apple Dev tests, and root Socket validation passed before milestone closure.

## Milestone 59: ARKit Spatial, Face, and Body Sensing

### Status

Planned

### Scope

- [ ] Ship `arkit-spatial-sensing-workflow` for world tracking, anchors, planes, ray casting, scene depth, LiDAR reconstruction, meshes, environment understanding, world-map persistence, and spatial diagnostics.
- [ ] Ship `arkit-face-body-tracking-workflow` for TrueDepth face tracking, face geometry, blend shapes, eye transforms, body tracking, skeleton data, and their rendering or analysis handoffs.
- [ ] Keep Local Authentication as the owner of Face ID and Touch ID authentication; do not imply that apps can access enrolled biometric templates, reusable Face ID identity data, or the system's authentication model.
- [ ] Keep ARKit tracking separate from Vision analysis and from AVFoundation sensor capture while documenting when a task crosses those boundaries.

### Required Guidance

- [ ] Cover AR session lifecycle, configuration support checks, tracking state, world alignment, anchors, planes, feature points, ray casting, environment texturing, relocalization, interruption, and reset choices.
- [ ] Cover scene depth, smoothed scene depth, scene reconstruction, mesh anchors, mesh classification, occlusion, hit testing, spatial measurements, and LiDAR capability checks.
- [ ] Cover world maps and persistence, reference images and objects, object scanning handoffs, geographic or location anchors where supported, and environment probes.
- [ ] Cover front-camera TrueDepth requirements, face anchors, geometry, topology, transforms, eye transforms, blend shapes, face-driven animation, and world-plus-face tracking where supported.
- [ ] Cover body tracking, skeleton definitions, joint transforms, scale estimation, and platform/device limitations.
- [ ] Route room-scale scanning to RoomPlan, presentation and interaction to RealityKit or SceneKit as appropriate, and advanced rendering to Metal without absorbing those frameworks into generic ARKit wrappers.
- [ ] Address privacy, stored spatial maps, face data, bystander data, data minimization, user notice, and lifecycle deletion as part of implementation guidance.
- [ ] Distinguish iOS/iPadOS ARKit behavior from visionOS ARKit authorization, provider, and data-access models where current documentation differs.

### Documentation Anchors

- [ ] Refresh Xcode documentation for AR world tracking, scene depth, scene reconstruction, mesh anchors, ray casting, environment understanding, face tracking, body tracking, and ARKit in visionOS.
- [ ] Refresh Xcode documentation for Local Authentication before writing any Face ID boundary or authentication handoff.
- [ ] Check current RoomPlan, RealityKit, and SceneKit documentation only where their handoff behavior affects the ARKit workflow contract.

### Implementation and Review Gate

- [ ] Add both skills, references, metadata, customization contracts, privacy guidance, device-capability rules, and handoffs.
- [ ] Add tests that reject Face ID/TrueDepth conflation, unsupported simulator claims, generic spatial-manager abstractions, and unqualified device assumptions.
- [ ] Update README, plugin metadata, active inventory, roadmap status, and handoffs from camera, Vision, accessibility, and Xcode execution workflows.
- [ ] Run targeted tests, docs validation, the full Apple Dev suite, and root Socket validation serially.
- [ ] Review the complete spatial surface for privacy, framework ownership, platform divergence, and physical-device evidence before beginning codec work.

### Exit Criteria

- [ ] Apple Dev Skills provides distinct, composable guidance for spatial sensing and face/body tracking.
- [ ] Face ID authentication, TrueDepth face tracking, Vision face analysis, and ordinary camera capture are explicitly different workflows.
- [ ] LiDAR, depth, reconstruction, world mapping, environment understanding, and platform-specific ARKit behavior are capability-gated and docs-backed.

## Milestone 60: Video Codecs and Pixel Processing

### Status

Planned

### Scope

- [ ] Ship `video-codec-processing-workflow` as the specialist owner for VideoToolbox compression, decompression, codec-session configuration, hardware capability, pixel-buffer pools, compressed sample output, and low-level video diagnostics.
- [ ] Keep AVFoundation readers, writers, export sessions, and general transcode pipelines with the existing AVFoundation workflow; use VideoToolbox only when the concrete codec, latency, hardware, or per-frame control requirement justifies it.
- [ ] Keep Core Media as the owner of sample timing and format descriptions, and Core Video as the owner of pixel-buffer storage, pools, attachments, and buffer interoperability.

### Required Guidance

- [ ] Cover compression and decompression session creation, property configuration, supported-property discovery, encode/decode callbacks, frame submission, delayed frames, completion, flush, invalidation, and teardown.
- [ ] Cover real-time versus offline policy, bitrate, data-rate limits, keyframes, frame reordering, latency, entropy mode where applicable, multipass boundaries, and encoder availability.
- [ ] Cover codec format descriptions, parameter sets, compressed `CMSampleBuffer` output, timestamps, dependencies, dropped frames, and handoffs into readers, writers, displays, or networks.
- [ ] Cover `CVPixelBuffer`, pixel-buffer pools, pixel formats, IOSurface compatibility, row bytes, locking, attachments, Metal texture caches, and zero-copy boundaries without inventing raw-buffer wrappers.
- [ ] Cover color primaries, transfer functions, YCbCr matrices, clean aperture, pixel aspect ratio, HDR metadata, alpha, and other format attachments that must survive the pipeline.
- [ ] Require capability probing and runtime evidence before claiming hardware acceleration, a specific codec profile, low latency, HDR, alpha, or device throughput.
- [ ] Require profiling under representative load and descriptive `OSStatus` diagnostics for low-level failures.

### Documentation Anchors

- [ ] Refresh Xcode documentation for VideoToolbox compression/decompression sessions, properties, encoder lists, supported-property dictionaries, hardware requirements, multipass encoding, and image-transfer behavior.
- [ ] Refresh Xcode documentation for Core Video pixel buffers, pools, attachments, Metal texture caches, and IOSurface interoperability.
- [ ] Refresh Core Media documentation for codec format descriptions and compressed sample buffers where the codec workflow crosses timing or sample ownership.

### Implementation and Review Gate

- [ ] Add the specialist skill, references, metadata, customization contract, codec/type ownership rules, and tests.
- [ ] Review and update AVFoundation transcode, Core Media timing, Core Image rendering, Metal handoff, and Xcode profiling routes.
- [ ] Update README, plugin metadata, active inventory, roadmap status, and validation contracts before milestone completion.
- [ ] Run targeted tests, docs validation, the full Apple Dev suite, and root Socket validation serially.
- [ ] Audit the milestone for unnecessary low-level API recommendations and ensure AVFoundation remains the preferred simpler path where it expresses the real requirement.

### Exit Criteria

- [ ] The plugin can guide low-level encode/decode and pixel-buffer work without duplicating AVFoundation or Core Media ownership.
- [ ] Codec, color, timing, memory, hardware, and error-diagnostic requirements remain inspectable from input through output.

## Milestone 61: Photos Library and Media Selection

### Status

Planned

### Scope

- [ ] Ship `photos-library-editing-workflow` for PhotoKit authorization, fetches, collections, assets, resource requests, change observation, creation, transactional changes, and nondestructive editing.
- [ ] Cover system media selection through PhotosUI as a privacy-preserving alternative to broad library access when the app only needs user-selected images or videos.
- [ ] Keep image decoding and processing with Milestone 56, video pipelines with AVFoundation, and Photos library ownership with PhotoKit.

### Required Guidance

- [ ] Cover read/write, add-only, limited-library, denied, restricted, and not-determined authorization states plus correct purpose-string and user-explanation behavior.
- [ ] Cover `PhotosPicker` or current PhotosUI picker APIs, transferable loading, selection limits, filters, ordering, cancellation, iCloud-backed transfer, and the boundary where no full-library permission is required.
- [ ] Cover `PHAsset`, collections, fetch options, fetch results, incremental changes, `PHPhotoLibraryChangeObserver`, caching image management, request identifiers, cancellation, degraded results, and network access.
- [ ] Cover asset resources, original versus adjusted content, Live Photos, paired video, RAW-plus-JPEG resources, metadata implications, and export boundaries.
- [ ] Cover creation and change requests, perform-changes transactions, placeholders, albums, save errors, content-editing input/output, adjustment data, and nondestructive editing compatibility.
- [ ] Avoid mirroring the entire Photos library into app state or inventing a repository layer when fetch results, identifiers, change observation, and picker bindings express the actual requirement.
- [ ] Require user-visible privacy behavior and runtime evidence for limited-library, iCloud, network, edited-resource, and save paths.

### Documentation Anchors

- [ ] Refresh Xcode documentation for Photos authorization, limited library, fetching, asset resources, image requests, change observation, creation, transactions, and content editing.
- [ ] Refresh Xcode documentation for PhotosUI pickers and current SwiftUI transfer/loading integration.
- [ ] Check current macOS, iOS, iPadOS, and visionOS availability before making cross-platform claims.

### Implementation and Review Gate

- [ ] Add the skill, focused references, metadata, customization contract, privacy rules, picker/library routing, and tests.
- [ ] Review handoffs to image representation, Core Image, AVFoundation, SwiftUI architecture, AppKit architecture, and Xcode privacy configuration.
- [ ] Update README, plugin metadata, active inventory, roadmap status, and docs before milestone completion.
- [ ] Run targeted tests, docs validation, the full Apple Dev suite, and root Socket validation serially.
- [ ] Review the entire media expansion after this milestone and record any cross-skill inconsistency before entering the final audit.

### Exit Criteria

- [ ] Apple Dev Skills clearly distinguishes privacy-preserving media selection from PhotoKit library access and editing.
- [ ] Authorization, iCloud delivery, cancellation, resource identity, transactional saves, and nondestructive editing are explicit and docs-backed.

## Milestone 62: Media Expansion Audit and Socket Major Release

### Status

Planned

### Scope

- [ ] Audit the complete Apple media family: existing AVFAudio, AVAudioEngine, AVFoundation, Core Media, and Core Audio skills plus all skills added in Milestones 56 through 61.
- [ ] Verify every skill has one defined owner, one main entry path, explicit handoffs, current Apple documentation anchors, descriptive diagnostics, physical-device evidence boundaries, and no duplicate compatibility path.
- [ ] Align the Apple Dev README, plugin manifest, marketplace metadata, root Socket docs, root roadmap, active inventory validation, tests, and release notes with the final shipped surface.
- [ ] Treat this as a major Socket release because the plugin's supported workflow surface and public capability inventory expand substantially, while still documenting whether any individual skill contract is breaking.

### Final Audit

- [ ] Re-run Xcode documentation searches for every framework family and refresh any claims that changed during implementation.
- [ ] Use Dash as the secondary local documentation source for gaps or cross-symbol verification; record any area where current authoritative documentation remains insufficient.
- [ ] Audit naming and terminology across `SKILL.md`, references, `agents/openai.yaml`, README, plugin metadata, tests, and roadmap.
- [ ] Audit framework and type ownership across images, sample buffers, pixel buffers, camera outputs, Vision observations, Core ML models, spatial data, Photos assets, and encoded samples.
- [ ] Audit privacy and permission guidance for camera, microphone, Photos, Local Authentication, TrueDepth face data, spatial maps, and bystander data.
- [ ] Audit availability and runtime-evidence language across macOS, iOS, iPadOS, tvOS, watchOS, and visionOS where each framework applies.
- [ ] Audit every new or modified skill for direct framework-first implementation before any wrapper, manager, coordinator, repository, store, or mirrored state recommendation.
- [ ] Audit all operator-facing error examples so they identify the framework surface, operation, location, likely cause, and next inspection point.
- [ ] Account for every milestone branch, commit, worktree, subtree boundary, and local branch before cleanup or release claims.

### Validation and Release Gate

- [ ] Run Apple Dev docs validation, targeted milestone tests, the complete Apple Dev test suite, and root Socket metadata validation serially from the reviewed release candidate.
- [ ] Run the repository's release-ready checks and resolve every actionable review, CI, metadata, documentation, and packaging finding.
- [ ] Verify no subtree pull or push is required for `apple-dev-skills` under the current canonical Socket-owned payload policy, and report that accounting explicitly.
- [ ] Bump all maintained Socket semantic-version surfaces together to the approved next major version with the root release workflow.
- [ ] Prepare concise release notes covering new skills, framework ownership, privacy/device constraints, breaking changes if any, migration guidance if any, and verification performed.
- [ ] Merge the reviewed release branch through the repository's protected-main workflow, fast-forward the clean local `main`, tag the reviewed `main`, push the tag, and create the GitHub release.
- [ ] Run `codex plugin marketplace upgrade socket` only after the major Socket release is published, then verify the installed marketplace and plugin version.
- [ ] Complete branch accounting and remove only merged, fully preserved branches and worktrees after the release is verified.

### Exit Criteria

- [ ] The Apple Dev plugin ships a coherent, docs-first media, imaging, vision, camera, depth, spatial, codec, and Photos workflow family without catch-all skills or duplicate framework ownership.
- [ ] All milestone review, documentation, test, metadata, packaging, privacy, and runtime-evidence gates are complete.
- [ ] The major Socket release is published from reviewed `main`, the marketplace upgrade is verified, and all branches and worktrees are explicitly accounted for.

## Backlog Candidates

- [ ] Record plausible future work that is not yet committed to a milestone.

## History

- Added `safari-extension-control-workflow` as the explicit owner for Safari Web Extension, Safari Web Inspector Extension, Safari App Extension, SafariServices, messaging, content blocker, authentication, and external automation decision guidance.
- Added `icon-composer-app-icon-workflow` as the explicit owner for Icon Composer app icon production, including Mac-native artwork preparation, Computer Use GUI guidance, `ictool` preview export, Xcode handoff, and future packaged-agent direction.
- Added `appkit-app-architecture-workflow` as the explicit owner for AppKit app architecture guidance, including app delegates, status items, responder-chain menus, windows, controllers, restoration, archiving, Observation, and mixed AppKit/SwiftUI composition.
- Added `xcode-coding-intelligence-workflow` as the explicit owner for Xcode Intelligence setup, Xcode-hosted agents, external-agent MCP access through `xcrun mcpbridge`, command/tool permission boundaries, and execution-skill handoffs.
- Added maintained XcodeGen and `.xcconfig` templates for SwiftUI app bootstrap, raised the generated XcodeGen baseline to `2.45.4`, and expanded XcodeGen guidance around explicit configs, schemes, package wiring, test-plan references, generated project review, and shared/target/configuration build-setting layers.
- Made XcodeGen plus checked-in `.xcconfig` files the default for new Xcode app-project bootstrap, updated shared Xcode project guidance to prefer external build configuration files for nontrivial build settings, and kept hand-managed Xcode projects as an explicit guided fallback or migration choice.
- Updated the XcodeGen bootstrap direction to prefer Xcode 16 synchronized folders for ordinary app and test source roots, keep broad recursive paths with `includes` and `excludes` as the fallback, and install checked-in external app entitlement files wired through `.xcconfig`.
- Added default tracked homes for app marketing/build versions, Swift 6 and concurrency settings, user-script sandboxing, macOS app sandbox state, and hardened-runtime state so Xcode GUI build-setting changes can be promoted back into `.xcconfig` files cleanly.
- Added a default asset catalog with app-icon and accent-color placeholders, explicit app-icon config wiring, Swift asset-symbol generation, and dead-code stripping defaults to the generated XcodeGen scaffold.
- Added `migrate-xcode-project-to-xcodegen` as the explicit owner for non-destructive Xcode-managed to XcodeGen conversion audits and stale XcodeGen modernization planning.
- Tightened Xcode project guidance so tracked `.pbxproj` diffs produced by Xcode, XcodeGen, or other project-aware workflows are treated as critical project state that must be reviewed, staged, and committed before push, merge, release, or cleanup.
- Updated standalone install guidance so `apple-dev-skills` defaults to Codex's Git-backed marketplace add/upgrade flow without an explicit ref, documents the optional `socket` marketplace path for Gale's broader plugin set, and keeps manual local clone marketplaces as development and fallback paths.
- Tightened the Swift public API guidance across shared snippets, skill-local snippet copies, and generated `AGENTS.md` templates so public call sites default to streamlined typed APIs, optional defaulted parameters over overloads, request/options structs at four or more public parameters, and enum-backed choice modeling.
- Previously aligned Xcode app-project guidance around strict Apple-app MVVM source structure; the later three-letter-prefix migration superseded its paired-file naming with concatenated Xcode-friendly names while retaining directional service folders and no root `Controllers/` directory.
- Added strict app-structure drift reporting to `sync-xcode-project-guidance` and updated the XcodeGen bootstrap scaffold so new SwiftUI app projects start with `Sources/Views/Shared`, `Sources/Views/macOS`, `Sources/Views/iOS`, `Sources/Models`, and directional `Sources/Services` folders.
- Registered Xcode's built-in MCP bridge through the Codex plugin manifest so installed `apple-dev-skills` plugins expose the Xcode-owned MCP path without bundling a separate server package.
- Added an experimental `xcode_lldb` MCP config entry for Xcode 27 beta-era `xcrun lldb-mcp` investigation while keeping the dedicated debugger workflow planned until startup validation succeeds.
- Clarified the Apple `maintain-project-repo` branch-protection contract so generated and synced repos require the `validate` Actions check context instead of the workflow-title display string.
- Completed Milestones 1 through 17 by establishing the repository, shipping the core Apple skill bundle, improving portability and customization guidance, adding bootstrap and repo-sync workflows, extracting Apple docs exploration into its own skill, and cleaning up the install surface around the top-level export model.
- Completed Milestones 19 and 20 by shipping `format-swift-sources` and `structure-swift-sources` as distinct cleanup workflows with clear boundaries.
- Completed Milestones 22 and 23 by expanding deterministic TODO/FIXME ledger normalization and finishing the customization consolidation review. See `docs/maintainers/customization-consolidation-review.md`.
- Completed Milestones 27 and 28 by validating the top-level `skills/` export story against the live repo validator and tests, and by narrowing `agent-portability-skills` usage to selective plugin and export-surface alignment while leaving broader docs standards with `productivity-skills`.
- Completed Milestones 30 through 36 by shrinking the customization surface, adding the `maintain-project-repo` integration and shared extraction work, splitting execution workflows, and preserving guidance through the refactor.
- Collapsed the older first-slice planning docs for Milestones 37, 38, and 40 plus the standalone execution guidance-preservation matrix into this roadmap history and the still-live maintainer docs once those decisions were absorbed into the shipped skills, validator rules, and synced guidance assets.
- Tightened the Swift package guidance so the explicit Swift 6 language-mode default stays in place while making it clear that `// swift-tools-version:` may be lowered from the scaffold default when real package compatibility needs it, but never below `6.0`.
