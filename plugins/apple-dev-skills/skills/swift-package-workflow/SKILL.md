---
name: swift-package-workflow
description: Compatibility workflow surface for broad or legacy Swift Package Manager execution requests. Use when older references still point at swift-package-workflow and route the request into swift-package-build-run-workflow or swift-package-testing-workflow while preserving SwiftPM-first mixed-root handoff behavior.
---

# Swift Package Workflow

## Purpose

Use this skill as a compatibility surface for older references to `swift-package-workflow` while the repo transitions to narrower package execution skills. The real long-term owners are `swift-package-build-run-workflow` for build/run and manifest work and `swift-package-testing-workflow` for testing work. `scripts/run_workflow.py` now stays intentionally thin: it performs repo-shape checks, preserves mixed-root and Xcode handoff boundaries, and returns routing context rather than trying to keep a second full execution-planning surface alive.

## When To Use

- Use this skill when older docs, prompts, or install surfaces still name `swift-package-workflow`.
- Use this skill when the request is broad and the first job is deciding between the narrower package build/run and testing skills.
- Use this skill when the user is working in a terminal or in editors such as Zed, VS Code, Neovim, Sublime Text, or other non-Xcode environments and the package-specific surface is obvious but the narrower skill has not yet been named.
- Do not use this skill for brand-new package bootstrap from nothing.
- Do not use this skill for repo-guidance alignment in an existing package repo.
- Do not use this skill as the default path for Xcode workspace, scheme, preview, simulator, or navigator-driven work.
- Recommend `swift-package-build-run-workflow` when the request is primarily about manifest, dependencies, plugins, package resources, Metal distribution, build, or run work.
- Recommend `swift-package-testing-workflow` when the request is primarily about Swift Testing, XCTest, `.xctestplan`, fixtures, flake diagnosis, or package test execution.
- Recommend `bootstrap-swift-package` when the package repo does not exist yet.
- Recommend `sync-swift-package-guidance` when the repo guidance needs to be added, refreshed, or merged.
- Recommend `xcode-build-run-workflow` when the task depends on active Xcode workspace state, scheme-aware execution, previews, navigator diagnostics, simulator or device flows, or guarded mutation inside Xcode-managed scope.
- Recommend `xcode-testing-workflow` when the task depends primarily on Xcode-native test execution, XCUITest, or `.xctestplan` handling.
- Recommend `explore-apple-swift-docs` when the user needs Apple or Swift docs exploration before implementation or package changes.

## Single-Path Workflow

1. Classify the request into one operation type:
   - package inspection
   - read or search
   - manifest or dependency changes
   - build
   - test
   - run
   - plugin
   - toolchain management
   - mutation
2. Apply the Apple and Swift docs gate before any design, architecture, implementation, or refactor guidance:
   - use `explore-apple-swift-docs` to gather the relevant SwiftPM, Swift, or Apple documentation first
   - state the documented API behavior, package rule, or workflow requirement being relied on before proposing changes
   - do not rely on memory as the primary source when docs exist
   - if the docs and the current code conflict, stop and report that conflict
   - if no relevant docs can be found, say that explicitly before proceeding
3. Apply the shared Swift-package policy before giving implementation guidance:
   - apply the detailed local policy in `references/snippets/apple-swift-package-core.md` when package-policy wording is needed
   - preserve its simplicity-first, shape-preserving, and anti-ceremony Swift guidance
   - preserve its explicit `swiftLanguageModes: [.v6]` package-manifest default and prefer that spelling over the legacy `swiftLanguageVersions` alias on current manifest surfaces
   - preserve its package-appropriate logging, telemetry, and testing guidance
4. Run `scripts/run_workflow.py` to resolve repo shape, detect whether the root is a plain package repo, and route the request toward the narrower package build/run or testing skill.
5. Use `references/cli-command-matrix.md` and `references/package-resources-testing-and-builds.md` only to explain why the narrower skill should take over; do not rebuild a second command-planning surface here.
6. If the repo root is ambiguous because Xcode-managed markers are present at the same root, use `references/xcode-handoff-conditions.md` and hand off cleanly to `xcode-build-run-workflow` or `xcode-testing-workflow` as appropriate.
7. Report the docs relied on, the repo-shape result, and the recommended narrower skill or Xcode handoff.

## Inputs

- `operation_type`: one of the operation types listed above.
- `request`: optional short natural-language request text used to infer `operation_type` when the explicit operation is omitted.
- `repo_root`: optional absolute path for the target package repo.
- `mixed_root_opt_in`: optional explicit opt-in when the user wants a SwiftPM-first plan for a mixed root even though Xcode markers are present.
- Defaults:
  - runtime entrypoint: executable `scripts/run_workflow.py`
  - `repo_root=.` when omitted
  - the runtime may infer `operation_type` from `--request` text when the request wording is clear enough
  - package execution prefers `swift package`, `swift build`, `swift test`, and `swift run`
  - mixed roots hand off by default unless `--mixed-root-opt-in` is passed

## Outputs

- `status`
  - `success`: the workflow completed on the SwiftPM-first path
  - `handoff`: the workflow is handing off to `xcode-build-run-workflow` or `xcode-testing-workflow`
  - `blocked`: prerequisites or repo-shape rules prevented completion
- `path_type`
  - `primary`: the SwiftPM-first path completed
  - `fallback`: a non-mutating planned command path was returned
- `output`
  - operation type
  - resolved repo root
  - repo-shape result
  - `routing_summary`
  - inferred context that helps the narrower skill or the caller understand why the handoff happened
  - `recommended_skill`
  - one concise next step or handoff payload

## Guards and Stop Conditions

- Stop with `blocked` when the repo root cannot be resolved.
- Stop with `blocked` when the repo does not contain `Package.swift`.
- Stop with `handoff` when the request should move into `swift-package-build-run-workflow`, `swift-package-testing-workflow`, `xcode-build-run-workflow`, or `xcode-testing-workflow`.
- Stop with `handoff` when the requested work crosses into Xcode project membership, scheme, preview, simulator, or other Xcode-managed concerns.
- Stop with `blocked` when no safe SwiftPM-first command path exists for the requested operation.

## Fallbacks and Handoffs

- The primary job of this skill now is to route to the narrower package skills while preserving the mixed-root Xcode handoff boundary.
- Do not keep a second package command matrix alive in this compatibility surface; the narrower skill should own concrete execution planning.
- The only current compatibility payload here is routing context, inferred repo shape, and one concise next step.
- Hand off to `swift-package-build-run-workflow` when the request is primarily about package build/run, manifest, dependency, plugin, resource, or Metal-distribution work.
- Hand off to `swift-package-testing-workflow` when the request is primarily about tests, test plans, fixtures, or package test diagnosis.
- Hand off to `xcode-build-run-workflow` when package work depends on:
  - active Xcode workspace or scheme state
  - previews, snippet execution, simulator, or device flows
  - navigator issues or Xcode build-log inspection
  - Xcode MCP mutation tools
  - Metal shader compilation, Apple-managed Metal toolchain inspection, or package distribution that depends on Xcode-managed Apple SDK integration
  - direct changes inside `.xcodeproj`, `.xcworkspace`, or `.pbxproj` managed scope
- Hand off to `xcode-testing-workflow` when package work depends primarily on Xcode-native test execution, XCUITest, or `.xctestplan` handling.
- Recommend `sync-swift-package-guidance` when the request is really about repo guidance instead of execution.
- Recommend `bootstrap-swift-package` when the repository still needs to be created from scratch.
- When maintaining this repository itself, refresh guidance-sync consumers after substantial package-policy changes and keep the top-level export-surface docs aligned. Do not tell users to rely on repo-local installer workflows; this repository does not ship them.

## Customization

- Use `references/customization.template.yaml`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` reads customization state, but the current workflow keeps a fixed routing policy and does not expose ordinary user-facing knobs.
- Run the Python wrapper and customization entrypoints through `uv`, because they rely on inline `PyYAML` script metadata rather than a repo-global Python environment.

## References

### Workflow References

- `references/workflow-policy.md`
- `references/repo-shape-detection.md`
- `references/cli-command-matrix.md`
- `references/package-resources-testing-and-builds.md`
- `references/xcode-handoff-conditions.md`

### Contract References

- `references/customization.template.yaml`

### Support References

- Recommend `references/snippets/apple-swift-package-core.md` when the user needs reusable SwiftPM baseline policy wording in an end-user repo.
- `references/snippets/apple-swift-package-core.md`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/customization_config.py`
