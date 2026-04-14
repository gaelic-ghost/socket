# Project Roadmap

## Vision

- Keep `apple-dev-skills` as the canonical Apple, Swift, and Xcode workflow repository, with Apple-docs-first guidance, clear top-level export boundaries, and maintainable supporting tooling.

## Product principles

- Keep root `skills/` as the canonical authored and exported surface.
- Keep Apple documentation requirements explicit and enforceable in the skill guidance.
- Keep plugin packaging thin and secondary to the workflow-authoring surface.
- Expand the repo deliberately instead of adding loosely related helper features ad hoc.

## Milestone Progress

- [ ] Milestone 18: Claude Code Plugin Extras
- [ ] Milestone 21: Swift Cleanup Automation Exploration
- [ ] Milestone 24: MCP App UI for Configuration and Customization
- [ ] Milestone 25: macOS Menu Bar Extra for Skill Controls
- [ ] Milestone 26: Dash Direct MCP and Call Library
- [ ] Milestone 27: Repo Self-Compliance and Install-Surface Audit
- [ ] Milestone 28: Use `Agent Dev Skills` plugin to align repo with skills/plugin repo standards
- [ ] Milestone 29: Swift and Xcode Testing Offload Workflow
- [ ] Milestone 37: Apple UI Accessibility Workflow
- [ ] Milestone 38: DocC Workflow
- [ ] Milestone 39: Swift Package Index Workflow

## Milestone 18: Claude Code Plugin Extras

Scope:

- [ ] Add Claude-only plugin enhancements on top of the shared Codex and Claude common denominator without making cross-ecosystem workflows depend on them.

Tickets:

- [ ] Flesh out `hooks/` for Claude-only automation where it clearly helps maintainers or end users.
- [ ] Add `bin/` helpers only for Claude-only convenience wrappers that do not become required for the shared workflow contract.
- [ ] Document which Claude-only extras are optional sugar versus canonical workflow behavior.
- [ ] Validate that Claude-only extras degrade gracefully when absent from Codex.

Exit criteria:

- [ ] Claude-only plugin extras exist as clearly separated enhancements, and the core workflow remains usable through the shared skill surface in both ecosystems.

## Milestone 21: Swift Cleanup Automation Exploration

Scope:

- [ ] Explore a larger maintainer automation flow for the `format-swift-sources` -> `structure-swift-sources` -> `format-swift-sources` choreography without overclaiming determinism for agent-driven file splits.

Tickets:

- [ ] Evaluate a `codex exec`-friendly maintainer wrapper for sequential formatting and structure passes.
- [ ] Define a structured-output contract for any `codex exec` helper so it can report findings, changed files, blocked steps, and follow-up recommendations deterministically.
- [ ] Decide whether `codex exec` should remain an on-demand maintainer tool, become a wrapper around deterministic repo helpers, or stay limited to advisory and enrichment work.
- [ ] Evaluate a Codex GUI App Automation that runs the same choreography on a schedule, preferably in a dedicated worktree.
- [ ] Document the boundary between deterministic local scripts, `codex exec` enrichment, and Codex GUI background automation.
- [ ] Keep file splitting and concern detection agent-driven unless a later design proves a safer deterministic boundary.

Exit criteria:

- [ ] The repo has a written decision and an approved implementation direction for higher-level Swift cleanup automation.

## Milestone 24: MCP App UI for Configuration and Customization

Scope:

- [ ] Add an MCP App surface for inspecting and adjusting skill configuration and customization state without hand-editing YAML.

Tickets:

- [ ] Design the MCP App scope for viewing effective customization state across skills.
- [ ] Define which edits should remain metadata-only versus which should affect runtime-enforced behavior.
- [ ] Add UI resources and tool wiring for reading templates, durable overrides, and effective merged config.
- [ ] Validate that MCP App edits preserve the same contracts as the script-based customization flow.
- [ ] Document how the MCP App surface relates to the existing script-based customization flow.

Exit criteria:

- [ ] The repo ships a documented MCP App path for viewing and editing customization state, or has an explicit bounded design ready for implementation.

## Milestone 25: macOS Menu Bar Extra for Skill Controls

Scope:

- [ ] Explore a native macOS menu bar utility for local maintainer workflows around skill installation, customization, and quick actions.

Tickets:

- [ ] Define the minimum viable menu bar feature set for local maintainer use.
- [ ] Evaluate whether the app should be a thin shell around existing scripts and MCP surfaces or a richer native controller.
- [ ] Identify which repo-local actions are safe and useful from a menu bar context.
- [ ] Document how the menu bar app would coexist with Codex plugin wiring and any future MCP App customization UI.
- [ ] Decide whether the menu bar app belongs in this repo, a sibling repo, or a plugin-bundled local-development surface.

Exit criteria:

- [ ] Maintainers have a documented plan for whether to build the menu bar app, what it should own, and where it should live.

## Milestone 26: Dash Direct MCP and Call Library

Scope:

- [ ] Remove avoidable indirection in the Dash-docsets workflow by teaching direct MCP usage first and documenting the Dash.app localhost HTTP call structure as a direct fallback surface.

Tickets:

- [ ] Audit `explore-apple-swift-docs` for places where wrapper scripts stand in for MCP usage the agent could perform directly.
- [ ] Teach the skill to prefer direct Dash MCP calls when the MCP service is available.
- [ ] Document the Dash.app localhost HTTP call structure clearly enough that the agent can use it directly when MCP is unavailable or incomplete.
- [ ] Provide a compact library of common Dash example calls and docset targets.
- [ ] Reconcile references and runtime helpers so the documented primary path and the actual preferred path match again.

Exit criteria:

- [ ] The Dash workflow teaches direct MCP usage first, documents the localhost HTTP structure as a real fallback, and ships a practical library of common example calls and docset targets.

## Milestone 27: Repo Self-Compliance and Install-Surface Audit

Scope:

- [ ] Keep this repository checked against its own skill, symlink, export-surface, and local-discovery guidance.

Tickets:

- [ ] Verify that root docs, maintainer docs, and skill docs stay aligned with the top-level export model after future refactors.
- [ ] Document any mismatch between repo docs and the actual top-level export surface so guidance reflects operational reality instead of stale packaging assumptions.

Exit criteria:

- [ ] Maintainers have a verified, reality-based local discovery and top-level export story for this repo, with docs and tooling updated to match what the repository actually ships.

## Milestone 28: Use `Agent Dev Skills` plugin to align repo with skills/plugin repo standards

Scope:

- [ ] Use the adjacent `agent-plugin-skills` maintainer workflows to audit and align this repository with the current shared skills/plugin repo standards while keeping this repo's own contract focused on top-level exports only.

Tickets:

- [ ] Keep the personal-scope `agent-plugin-skills` install current for work on this repository without reintroducing a nested packaged plugin tree here.
- [ ] Use `maintain-plugin-repo` and `sync-skills-repo-guidance` as the maintainer entrypoints for repo-wide audit and docs alignment where relevant.
- [ ] Align repo docs, export surfaces, ignores, and maintainer guidance with the current shared standards without flattening repo-specific policy.
- [ ] Remove stale nested packaging language while keeping the adjacent standards repo as the maintainer-only setup.

Exit criteria:

- [ ] The repository validates cleanly against the current shared skills/plugin repo standards.
- [ ] Repo docs, packaging metadata, marketplace wiring, and maintainer guidance describe the same live behavior.

## Milestone 29: Swift and Xcode Testing Offload Workflow

Scope:

- [ ] Design and ship a dedicated offload workflow for repetitive, noisy SwiftPM and Xcode build, test, preview, and diagnostics work so the main agent thread can stay focused on higher-signal reasoning and implementation.

Tickets:

- [ ] Audit the repetitive Swift and Xcode verification work that is currently handled inline.
- [ ] Decide which implementation surface should own the offload path.
- [ ] Define the input and output contract for the offload path so verification work can be delegated without losing decision-useful detail.
- [ ] Cover the highest-value offload cases first, including `swift build`, `swift test`, `xcodebuild`, preview refresh, diagnostics refresh, and noisy failure summarization.
- [ ] Document when the main agent should stay local versus when it should hand verification work to the offload path.
- [ ] Add validation or smoke-test coverage once the implementation surface is chosen.

Exit criteria:

- [ ] Maintainers have one documented and validated way to offload repetitive Swift and Xcode verification work from the main agent thread.
- [ ] The offload path returns concise, decision-useful results without obscuring the underlying build or test evidence.

## Milestone 37: Apple UI Accessibility Workflow

Scope:

- [ ] Add a dedicated Apple accessibility workflow skill that covers SwiftUI, UIKit, and AppKit accessibility implementation and review.
- [ ] Keep the skill grounded in current Apple accessibility APIs, platform semantics, focus behavior, VoiceOver behavior, Dynamic Type or text sizing expectations, and reduced-motion or contrast-related system settings.

Tickets:

- [ ] Define the skill boundary so it owns Apple UI accessibility implementation and review work without duplicating the broader docs-routing or generic repo-accessibility workflows.
- [ ] Gather the core Apple documentation references for SwiftUI, UIKit, AppKit, accessibility traits, labels, actions, announcements, focus, and testing surfaces.
- [ ] Ship a workflow surface that can help with both new implementation and review of existing Apple UI code.
- [ ] Cover the differences and overlap between SwiftUI accessibility modifiers, UIKit accessibility properties, and AppKit accessibility APIs.
- [ ] Document practical verification expectations, including simulator or device testing, VoiceOver checks, focus-order review, and content-scaling or motion-related checks where relevant.
- [ ] Add tests and maintainer docs once the workflow shape is stable.

Exit criteria:

- [ ] The repository ships a documented Apple accessibility workflow skill for SwiftUI, UIKit, and AppKit work.
- [ ] The workflow clearly distinguishes framework-specific guidance from shared Apple accessibility principles and verification expectations.

## Milestone 38: DocC Workflow

Scope:

- [ ] Add a dedicated DocC workflow skill for authoring, organizing, validating, and publishing Apple documentation bundles.
- [ ] Cover DocC structure, tutorials, symbol documentation, article organization, catalog layout, preview or generation paths, and integration with package or Xcode-hosted docs builds.

Tickets:

- [ ] Define the skill boundary so it owns DocC authoring and publishing workflow guidance without absorbing generic Markdown maintenance work.
- [ ] Gather the Apple documentation needed for DocC catalogs, articles, tutorials, symbol links, directives, and build or preview tooling.
- [ ] Ship a workflow surface that helps maintainers create, revise, and validate DocC content in Swift package and Xcode repository shapes.
- [ ] Cover common failure modes such as broken symbol links, bundle-structure mistakes, navigation drift, and preview or build mismatches.
- [ ] Document how the workflow should advise on DocC hosting and publishing paths when the repo is using static hosting or generated docs artifacts.
- [ ] Add tests and maintainer docs once the workflow shape is stable.

Exit criteria:

- [ ] The repository ships a documented DocC workflow skill with clear authoring, validation, and publishing guidance.
- [ ] The workflow can explain both local DocC maintenance and the main hosting or export paths without blurring them together.

## Milestone 39: Swift Package Index Workflow

Scope:

- [ ] Add a dedicated Swift Package Index workflow skill for package distribution, documentation hosting, build readiness, metadata, and submission or listing expectations.
- [ ] Cover the parts of SPI work that matter to maintainers shipping public Swift packages, including documentation hosting, build compatibility, supported platform metadata, README and package-surface expectations, and listing hygiene.

Tickets:

- [ ] Define the skill boundary so it owns SPI-specific distribution and hosting guidance without replacing the core Swift package build or testing workflows.
- [ ] Gather the relevant Swift Package Index documentation for package metadata, documentation hosting, build surfaces, listing or submission expectations, and compatibility signals.
- [ ] Ship a workflow surface that can help maintainers prepare a package for SPI, diagnose common SPI-facing build or docs issues, and understand what SPI is deriving from the repository.
- [ ] Cover the relationship between SPI docs hosting, DocC output, README quality, package metadata, and supported platform declarations.
- [ ] Document common SPI failure modes such as unsupported package structure, incomplete metadata, broken docs generation, or platform mismatch signals.
- [ ] Add tests and maintainer docs once the workflow shape is stable.

Exit criteria:

- [ ] The repository ships a documented Swift Package Index workflow skill for package distribution and SPI-facing readiness work.
- [ ] The workflow clearly explains how SPI distribution, documentation hosting, and package metadata fit together for public Swift packages.

## History

- Completed Milestones 1 through 17 by establishing the repository, shipping the core Apple skill bundle, improving portability and customization guidance, adding bootstrap and repo-sync workflows, extracting Apple docs exploration into its own skill, and cleaning up the install surface around the top-level export model.
- Completed Milestones 19 and 20 by shipping `format-swift-sources` and `structure-swift-sources` as distinct cleanup workflows with clear boundaries.
- Completed Milestones 22 and 23 by expanding deterministic TODO/FIXME ledger normalization and finishing the customization consolidation review. See `docs/maintainers/customization-consolidation-review.md`.
- Completed Milestones 30 through 36 by shrinking the customization surface, adding the repo-maintenance toolkit and shared extraction work, splitting execution workflows, and preserving guidance through the refactor.
