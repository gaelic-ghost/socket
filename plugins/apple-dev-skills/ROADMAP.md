# Project Roadmap

## Table of Contents

- [Vision](#vision)
- [Product Principles](#product-principles)
- [Milestone Progress](#milestone-progress)
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
- [Milestone 41: Swift Package Extension Workflow](#milestone-41-swift-package-extension-workflow)
- [Milestone 42: Safari Extension And Control Workflow](#milestone-42-safari-extension-and-control-workflow)
- [Milestone 43: Client Auth, Keychain, and App Sync Workflow](#milestone-43-client-auth-keychain-and-app-sync-workflow)
- [Milestone 44: Swift OpenAPI Client Workflow](#milestone-44-swift-openapi-client-workflow)
- [Milestone 45: Icon Composer App Icon Workflow](#milestone-45-icon-composer-app-icon-workflow)
- [Milestone 46: AppKit App Architecture Workflow](#milestone-46-appkit-app-architecture-workflow)
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
- Milestone 41: Swift Package Extension Workflow - Planned
- Milestone 42: Safari Extension And Control Workflow - Completed
- Milestone 43: Client Auth, Keychain, and App Sync Workflow - Planned
- Milestone 44: Swift OpenAPI Client Workflow - Completed
- Milestone 45: Icon Composer App Icon Workflow - Completed
- Milestone 46: AppKit App Architecture Workflow - Completed

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

## Backlog Candidates

- [ ] Record plausible future work that is not yet committed to a milestone.

## History

- Added `safari-extension-control-workflow` as the explicit owner for Safari Web Extension, Safari Web Inspector Extension, Safari App Extension, SafariServices, messaging, content blocker, authentication, and external automation decision guidance.
- Added `icon-composer-app-icon-workflow` as the explicit owner for Icon Composer app icon production, including Mac-native artwork preparation, Computer Use GUI guidance, `ictool` preview export, Xcode handoff, and future packaged-agent direction.
- Added `appkit-app-architecture-workflow` as the explicit owner for AppKit app architecture guidance, including app delegates, status items, responder-chain menus, windows, controllers, restoration, archiving, Observation, and mixed AppKit/SwiftUI composition.
- Tightened Xcode project guidance so tracked `.pbxproj` diffs produced by Xcode, XcodeGen, or other project-aware workflows are treated as critical project state that must be reviewed, staged, and committed before push, merge, release, or cleanup.
- Updated standalone install guidance so `apple-dev-skills` defaults to Codex's Git-backed marketplace add/upgrade flow without an explicit ref, documents the optional `socket` marketplace path for Gale's broader plugin set, and keeps manual local clone marketplaces as development and fallback paths.
- Tightened the Swift public API guidance across shared snippets, skill-local snippet copies, and generated `AGENTS.md` templates so public call sites default to streamlined typed APIs, optional defaulted parameters over overloads, request/options structs at four or more public parameters, and enum-backed choice modeling.
- Registered Xcode's built-in MCP bridge through the Codex plugin manifest so installed `apple-dev-skills` plugins expose the Xcode-owned MCP path without bundling a separate server package.
- Clarified the Apple `maintain-project-repo` branch-protection contract so generated and synced repos require the `validate` Actions check context instead of the workflow-title display string.
- Completed Milestones 1 through 17 by establishing the repository, shipping the core Apple skill bundle, improving portability and customization guidance, adding bootstrap and repo-sync workflows, extracting Apple docs exploration into its own skill, and cleaning up the install surface around the top-level export model.
- Completed Milestones 19 and 20 by shipping `format-swift-sources` and `structure-swift-sources` as distinct cleanup workflows with clear boundaries.
- Completed Milestones 22 and 23 by expanding deterministic TODO/FIXME ledger normalization and finishing the customization consolidation review. See `docs/maintainers/customization-consolidation-review.md`.
- Completed Milestones 27 and 28 by validating the top-level `skills/` export story against the live repo validator and tests, and by narrowing `agent-plugin-skills` usage to selective plugin and export-surface alignment while leaving broader docs standards with `productivity-skills`.
- Completed Milestones 30 through 36 by shrinking the customization surface, adding the `maintain-project-repo` integration and shared extraction work, splitting execution workflows, and preserving guidance through the refactor.
- Collapsed the older first-slice planning docs for Milestones 37, 38, and 40 plus the standalone execution guidance-preservation matrix into this roadmap history and the still-live maintainer docs once those decisions were absorbed into the shipped skills, validator rules, and synced guidance assets.
- Tightened the Swift package guidance so the explicit Swift 6 language-mode default stays in place while making it clear that `// swift-tools-version:` may be lowered from the scaffold default when real package compatibility needs it, but never below `6.0`.
