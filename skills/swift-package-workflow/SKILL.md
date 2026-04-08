---
name: swift-package-workflow
description: Guide development work in existing Swift Package Manager repositories, including package inspection, manifest edits, dependency changes, builds, tests, plugin flows, toolchain checks, and terminal-first editor workflows. Use for plain Swift package work when Package.swift is the source of truth and Xcode-managed execution is not the primary concern.
---

# Swift Package Workflow

## Purpose

Use this skill as the top-level execution workflow for existing Swift Package Manager repositories whose source of truth is `Package.swift`. The skill keeps ordinary package work on a SwiftPM-first path instead of routing it through Xcode-oriented execution policy. `scripts/run_workflow.py` is the runtime entrypoint for repo-shape checks, lightweight safety policy, and command planning. Keep this workflow focused on package execution, manifest work, and terminal or editor collaboration rather than stretching it into repo-guidance sync, new-repo bootstrap, or Xcode-managed execution.

## When To Use

- Use this skill for ordinary development work inside an existing Swift package repo.
- Use this skill for manifest, target, product, dependency, plugin, build-tool, and test work driven by `Package.swift`.
- Use this skill when the user is working in a terminal or in editors such as Zed, VS Code, Neovim, Sublime Text, or other non-Xcode environments.
- Use this skill for cross-platform, server-side, library, CLI-tool, and package-plugin workflows where SwiftPM is the primary control surface.
- Use this skill for package resource layout, `Bundle.module` access, `.process(...)` / `.copy(...)` / `.embedInCode(...)` choices, and package-local fixture organization.
- Use this skill for Swift Testing-first package work, package XCTest holdouts, and package-level `xcodebuild` test-plan execution when the package surface needs it.
- Do not use this skill for brand-new package bootstrap from nothing.
- Do not use this skill for repo-guidance alignment in an existing package repo.
- Do not use this skill as the default path for Xcode workspace, scheme, preview, simulator, or navigator-driven work.
- Recommend `bootstrap-swift-package` when the package repo does not exist yet.
- Recommend `sync-swift-package-guidance` when the repo guidance needs to be added, refreshed, or merged.
- Recommend `xcode-app-project-workflow` when the task depends on active Xcode workspace state, scheme-aware execution, previews, navigator diagnostics, simulator or device flows, or guarded mutation inside Xcode-managed scope.
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
   - preserve its package-appropriate logging, telemetry, and testing guidance
4. Run `scripts/run_workflow.py` to resolve repo shape, detect whether the root is a plain package repo, and plan the SwiftPM-first command path.
5. Use the guidance in `references/cli-command-matrix.md` for agent-executed SwiftPM commands and terminal-first editor workflows.
6. Use `references/package-resources-testing-and-builds.md` when the request touches package resources, Metal artifacts, Swift Testing, XCTest holdouts, test plans, or Debug/Release validation.
7. If the repo root is ambiguous because Xcode-managed markers are present at the same root, use `references/xcode-handoff-conditions.md` and hand off cleanly to `xcode-app-project-workflow`.
8. Report which parts were agent-executed, the docs relied on, the repo-shape result, and any required next step or handoff.

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
  - `handoff`: the workflow is handing off to `xcode-app-project-workflow`
  - `blocked`: prerequisites or repo-shape rules prevented completion
- `path_type`
  - `primary`: the SwiftPM-first path completed
  - `fallback`: a non-mutating planned command path was returned
- `output`
  - operation type
  - resolved repo root
  - repo-shape result
  - `planned_commands`
  - one concise next step or handoff payload

## Guards and Stop Conditions

- Stop with `blocked` when the repo root cannot be resolved.
- Stop with `blocked` when the repo does not contain `Package.swift`.
- Stop with `handoff` when the repo root is mixed and Xcode-managed behavior is the safer default.
- Stop with `handoff` when the requested work crosses into Xcode project membership, scheme, preview, simulator, or other Xcode-managed concerns.
- Stop with `blocked` when no safe SwiftPM-first command path exists for the requested operation.

## Fallbacks and Handoffs

- SwiftPM and ordinary filesystem edits are the default execution surface for this skill.
- The only current fallback is a non-mutating planned command result when the user asked for guidance rather than immediate execution.
- Hand off to `xcode-app-project-workflow` when package work depends on:
  - active Xcode workspace or scheme state
  - previews, snippet execution, simulator, or device flows
  - navigator issues or Xcode build-log inspection
  - Xcode MCP mutation tools
  - Metal shader compilation, Apple-managed Metal toolchain inspection, or package distribution that depends on Xcode-managed Apple SDK integration
  - direct changes inside `.xcodeproj`, `.xcworkspace`, or `.pbxproj` managed scope
- Recommend `sync-swift-package-guidance` when the request is really about repo guidance instead of execution.
- Recommend `bootstrap-swift-package` when the repository still needs to be created from scratch.
- When maintaining this plugin itself, refresh guidance-sync consumers after substantial package-policy changes and keep the local plugin install current; `install-plugin-to-socket` is a useful maintainer shortcut for install, update, verify, and repair work.

## Customization

- Use `references/customization.template.yaml`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` reads customization state, but the current workflow keeps a fixed SwiftPM-first policy and does not expose ordinary user-facing knobs yet.
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
