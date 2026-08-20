---
name: swift-package-testing-workflow
description: Guide Swift Testing, XCTest holdouts, code coverage, xctestplan handoff conditions, async test design, semantic accessibility-test boundaries, test-fixture organization, and package test-diagnosis work in existing Swift Package Manager repositories. Use when Package.swift is the source of truth and the task is primarily about testing rather than package build or run work.
---

# Swift Package Testing Workflow

## Purpose

Use this skill as the primary execution workflow for test-focused work in existing Swift package components. Keep it focused on Swift Testing, XCTest holdouts, code coverage, `.xctestplan` handoff conditions, async-test guidance, semantic accessibility-test boundaries, performance-sensitive package workload profiling, filters, retries, fixtures, and package-level test diagnosis. `scripts/run_workflow.py` resolves the nearest package root and plans the test surface without classifying the containing repository.

## When To Use

- Use this skill for running, diagnosing, organizing, or evolving tests in an existing Swift package repo.
- Use this skill for Swift Testing-first package work, XCTest holdouts, async-test design, semantic accessibility-test boundaries, and test-fixture organization.
- Use this skill for package-level `.xctestplan` execution when the package surface needs Xcode test-plan follow-through.
- Use this skill when the request is about test selection, filtering, retries, failures, flaky tests, or test-only Debug/Release validation.
- Use this skill when the request is about package-first performance-sensitive testing, signpost placement, Release workload harnesses, or profiling-ready package test design for Audio, Metal, MLX, local AI, streaming, or other Apple silicon-sensitive workloads.
- Do not use this skill for broad manifest edits, dependency work, package resources, package-extension design, or ordinary build and run work.
- Do not use this skill for brand-new package bootstrap from nothing.
- Do not use this skill for repo-guidance alignment in an existing package repo.
- Do not use this skill as the default path for Xcode workspace, scheme, preview, simulator, or navigator-driven work.
- Recommend `swift-package-build-run-workflow` when the request is primarily about ordinary package build/run, manifest, dependency, resource, or Metal-distribution work.
- Recommend `swift-package-extension-workflow` when trait matrices, macro/plugin test shape, or generated-source validation is the primary concern.
- Recommend `bootstrap-swift-package` when the package repo does not exist yet.
- Recommend root workspace `just align` when product guidance needs to be refreshed.
- Recommend `xcode-testing-workflow` when test work depends on active Xcode workspace state, navigator diagnostics, simulator or device flows, XCUITest, runtime accessibility verification, or Xcode-native test plans and test execution.
- Recommend `apple-ui-accessibility-workflow` when the request is primarily about accessibility semantics or review rather than package-side testing strategy.
- Recommend `xcode-build-run-workflow` when package test work crosses into guarded mutation, file membership, or other Xcode-managed project-integrity work.
- Recommend `explore-apple-swift-docs` when the user needs Apple or Swift docs exploration before implementation or test changes.

## Single-Path Workflow

1. Classify the request into one operation type:
   - package inspection
   - read or search
   - test
   - mutation
2. Apply the Apple and Swift docs gate before any design, architecture, implementation, or refactor guidance:
   - use `explore-apple-swift-docs` to gather the relevant SwiftPM, Swift, or Apple documentation first
   - state the documented API behavior, testing rule, or workflow requirement being relied on before proposing changes
   - do not rely on memory as the primary source when docs exist
   - if the docs and the current code conflict, stop and report that conflict
   - if no relevant docs can be found, say that explicitly before proceeding
3. Apply the shared Swift-package policy before giving implementation guidance:
   - apply the detailed local policy in `references/snippets/apple-swift-package-core.md` when package-policy wording is needed
   - preserve its simplicity-first, shape-preserving, and anti-ceremony Swift guidance
   - preserve its explicit `swiftLanguageModes: [.v6]` package-manifest default and prefer that spelling over the legacy `swiftLanguageVersions` alias on current manifest surfaces
   - preserve its package-appropriate logging, telemetry, structured-concurrency, and Swift Testing guidance
4. Run `scripts/run_workflow.py` to resolve the nearest package root, confirm the request stays on the testing surface, and plan the package-testing command path.
5. Use `references/code-coverage.md` when the request needs SwiftPM collection, exported-JSON discovery, coverage reporting, comparison, or an explicit coverage-gate boundary.
6. Use `references/package-resources-testing-and-builds.md` when the request touches Swift Testing, XCTest, `.xctestplan`, accessibility-related semantic tests, fixtures, async test discipline, or test-related Debug/Release validation.
7. Use `references/performance-sensitive-testing-and-profiling.md` when the request touches package-first instrumentation, `OSSignposter`, `xctrace`, Time Profiler, Metal System Trace, Allocations, VM Tracker, Audio, MLX, local AI, streaming, or other performance-sensitive Apple silicon workloads.
8. Apply `../../shared/execution-surface-routing.md`; use `xcode-testing-workflow` only for `.xctestplan`, XCUITest, scheme, or destination work.
9. Report which parts were agent-executed, the docs relied on, the resolved package context, and any required next step or handoff.

## Inputs

- `operation_type`: one of the operation types listed above.
- `request`: optional short natural-language request text used to infer `operation_type` when the explicit operation is omitted.
- `repo_root`: optional absolute path for the target package repo.
- Defaults:
  - runtime entrypoint: executable `scripts/run_workflow.py`
  - `repo_root=.` when omitted
  - the runtime may infer `operation_type` from `--request` text when the request wording is clear enough
  - package testing prefers `swift test`, filtered `swift test` runs, and `xcodebuild` test-plan follow-through only when the package surface truly needs it
  - Xcode files do not change package routing

## Outputs

- `status`
  - `success`: the workflow completed on the package-testing path
  - `handoff`: the workflow is handing off to another skill because build/run or Xcode-managed behavior is the safer surface
  - `blocked`: prerequisites or package-root resolution prevented completion
- `path_type`
  - `primary`: the package-testing path completed
  - `fallback`: a non-mutating planned command path was returned
- `output`
  - operation type
  - resolved package root
  - package context
  - `planned_commands`
  - one concise next step or handoff payload

## Guards and Stop Conditions

- Stop with `blocked` when the package root cannot be resolved.
- Stop with `blocked` when the repo does not contain `Package.swift`.
- Stop with `handoff` when the request is really ordinary package build/run, manifest, dependency, resource, or Metal-distribution work.
- Stop with `handoff` only when the requested operation requires `.xctestplan`, XCUITest, scheme, simulator, or device behavior.
- Stop with `handoff` when the requested work crosses into Xcode project membership, scheme, preview, simulator, or other Xcode-managed concerns.
- Stop with `blocked` when no safe package-testing command path exists for the requested operation.

## Fallbacks and Handoffs

- SwiftPM and ordinary filesystem edits inside package-managed scope are the default execution surface for this skill.
- The only current fallback is a non-mutating planned command result when the user asked for guidance rather than immediate execution.
- Hand off to `swift-package-build-run-workflow` when the request becomes primarily about package build/run, manifest, dependencies, plugins, package resources, or Metal-distribution work.
- Hand off to `swift-package-extension-workflow` when test planning is primarily shaped by package traits, macro expansion, plugin execution, or generated output.
- Hand off to `xcode-testing-workflow` when package test work depends on:
  - active Xcode workspace or scheme state
  - previews, snippet execution, simulator, or device flows
  - navigator issues or Xcode build-log inspection
  - Xcode MCP mutation tools
  - `.xctestplan` execution or package test behavior that is more authoritative through Xcode-managed Apple SDK integration
  - direct test execution through Xcode-native destinations, UI testing, or `.xctestplan` handling inside an Xcode-managed workspace
  - Instruments UI inspection, `.trace` artifact interpretation, or `xctrace` capture that depends on Xcode-managed schemes, destinations, app hosts, or test plans
- Recommend `apple-ui-accessibility-workflow` when the user is really asking how the UI should expose semantics to assistive technologies instead of how a package-side test should be organized.
- Hand off to `xcode-build-run-workflow` when package test work instead crosses into direct changes inside `.xcodeproj`, `.xcworkspace`, or `.pbxproj` managed scope.
- Recommend root workspace `just align` when the request is really about product guidance instead of execution.
- Recommend `bootstrap-swift-package` when the repository still needs to be created from scratch.
- When maintaining this repository itself, refresh guidance-sync consumers after substantial package-testing policy changes and keep the top-level export-surface docs aligned. Do not tell users to rely on repo-local installer workflows; this repository does not ship them.

## Customization

- Use `references/customization.template.yaml`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` reads customization state, but the current workflow keeps a fixed package-testing policy and does not expose ordinary user-facing knobs yet.
- Run the Python wrapper and customization entrypoints through `uv`, because they rely on inline `PyYAML` script metadata rather than a repo-global Python environment.

## References

### Workflow References

- `references/workflow-policy.md`
- `references/code-coverage.md`
- `references/package-resources-testing-and-builds.md`
- `references/performance-sensitive-testing-and-profiling.md`
- `../../shared/execution-surface-routing.md`

### Contract References

- `references/customization.template.yaml`

### Support References

- Recommend `references/snippets/apple-swift-package-core.md` when the user needs reusable SwiftPM baseline policy wording in an end-user repo.
- `references/snippets/apple-swift-package-core.md`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/customization_config.py`
