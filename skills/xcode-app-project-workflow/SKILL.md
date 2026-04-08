---
name: xcode-app-project-workflow
description: Guide development work in or around existing Xcode-managed projects and workspaces, including workspace inspection, diagnostics, builds, tests, runs, previews, navigator issues, Xcode MCP operations, and guarded mutation in Xcode-managed scope. Use when Xcode-aware execution is needed.
---

# Xcode App Project Workflow

## Purpose

Use this skill as the top-level entry point for execution work in or around Xcode-managed projects and workspaces. The skill guides agent-side tool use and applies the shared simplicity-first Swift policy, while `scripts/run_workflow.py` enforces local policy, `.pbxproj` edit safeguards, and structured fallback planning. Keep this workflow focused on Xcode-aware execution instead of stretching it into docs-management, package-first execution, or repo-sync responsibilities. Codex Plugin and Claude Code Plugin installs for the bundled Apple skill set are now the preferred install path going forward.

## When To Use

- Use this skill for Xcode workspace inspection, read or search, diagnostics, build, test, run, preview, and navigator-issue tasks.
- Use this skill for Xcode MCP operations, scheme-aware execution, and official Apple CLI fallback.
- Use this skill when direct filesystem mutation around an Xcode-managed project may be required.
- Use this skill for Swift Testing, XCTest, XCUITest, `.xctestplan`, Debug/Release build-configuration work, and file-membership verification after on-disk edits.
- Use this skill when Metal toolchain state, Apple-managed SDK components, or package-in-Xcode validation make `xcodebuild` more authoritative than plain SwiftPM.
- Use this skill after Apple or Swift docs have already been gathered through `explore-apple-swift-docs` and the work has shifted into Xcode-aware execution or implementation.
- Do not use this skill as the default path for ordinary Swift package development when `Package.swift` is the source of truth and Xcode-managed behavior is not the main concern.
- Recommend `explore-apple-swift-docs` when the user needs Apple or Swift documentation lookup, source selection, Dash compatibility, or docs install follow-up rather than execution work.
- Recommend `format-swift-sources` when the user needs to integrate or maintain SwiftLint or SwiftFormat across CLI, Xcode, SwiftPM, Git hooks, GitHub Actions, or SwiftFormat config export rather than active Xcode execution work.
- Recommend `structure-swift-sources` when the user needs file splitting, source-tree cleanup, DocC coverage, or TODO/FIXME ledger normalization rather than active Xcode execution work.
- Recommend `bootstrap-swift-package` when the user needs to create a brand new Swift package rather than work inside an existing Xcode or Swift project.
- Recommend `swift-package-workflow` when the task is ordinary SwiftPM package development, manifest work, dependency work, build, test, run, plugin, or terminal-first editor collaboration.
- Recommend `sync-xcode-project-guidance` when an existing Xcode app repo needs `AGENTS.md` or workflow-guidance alignment rather than active engineering work.
- Mention that older references to `apple-xcode-workflow` now map to `xcode-app-project-workflow`.
- Mention that Codex Plugin or Claude Code Plugin installs are the preferred install path going forward.

## Single-Path Workflow

1. Classify the request into one operation type:
   - workspace or session inspection
   - read, search, or diagnostics
   - build, test, or run
   - package or toolchain management
   - mutation
2. Apply the Apple docs gate before any Apple design, architecture, implementation, or refactor guidance:
   - use `explore-apple-swift-docs` to gather the relevant Apple documentation first
   - state the documented API behavior, lifecycle rule, or workflow requirement being relied on before proposing changes
   - do not rely on memory as the primary source when Apple docs exist
   - if the docs and the current code conflict, stop and report that conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
3. Apply the shared Swift policy before giving implementation guidance:
   - apply the detailed local policy in `references/snippets/apple-xcode-project-core.md`
   - preserve its simplicity-first, shape-preserving, and anti-ceremony Swift guidance
   - preserve its project-appropriate logging, telemetry, and SwiftUI architecture guidance
4. Run `scripts/run_workflow.py` to apply runtime configuration, `.pbxproj` edit safeguards, and CLI fallback planning.
5. Use the guidance in `references/mcp-tool-matrix.md` for agent-executed MCP operations.
6. Use `references/testing-plans-file-membership-and-configurations.md` when the task touches Swift Testing, XCTest, XCUITest, `.xctestplan`, file membership after filesystem edits, or Debug/Release validation.
7. If MCP fails, use the structured fallback output from `scripts/run_workflow.py` together with `references/cli-fallback-matrix.md`.
8. Report which parts were agent-executed, which parts were locally enforced by script, the Apple docs relied on, and any required next step.

## Inputs

- `operation_type`: one of the operation types listed above.
- `request`: optional short natural-language request text used to infer `operation_type` when the explicit operation is omitted.
- `workspace_path`: optional absolute path for the target Xcode or Swift workspace.
- `tab_identifier`: optional MCP tab identifier when already known.
- `mcp_failure_reason`: optional input when continuing from an earlier MCP failure.
- `direct_pbxproj_edit`: optional flag when the requested mutation would directly edit a `.pbxproj` file.
- `direct_pbxproj_edit_opt_in`: optional explicit opt-in after the user has been warned about direct `.pbxproj` edit risks.
- Defaults:
  - runtime entrypoint: executable `scripts/run_workflow.py`
  - the runtime may infer `operation_type` from `--request` text when the request wording is clear enough
  - agent-side MCP retries once for transient failures
  - direct edits are allowed by default when they do not directly edit `.pbxproj`

## Outputs

- `status`
  - `success`: the workflow completed on its primary or fallback path
  - `blocked`: prerequisites, policy, or mutation safeguards prevented completion
- `path_type`
  - `primary`: the guided agent-side MCP path completed successfully
  - `fallback`: the official CLI fallback path completed successfully
- `output`
  - operation type
  - `guard_result`
  - `fallback_commands`
  - one next step payload when needed

## Guards and Stop Conditions

- Apply the mutation safeguard from `references/mutation-risk-policy.md` only when the operation type is `mutation`.
- Do not skip the explicit warning path for direct `.pbxproj` edits.
- Stop with `blocked` when the required workspace context cannot be resolved and the operation cannot safely continue.
- Stop with `blocked` when allowlist or sandbox rules prevent the official CLI fallback and no safe alternative exists.

## Fallbacks and Handoffs

- Official CLI execution is the only fallback path when the primary agent-side MCP path cannot complete.
- Use `references/mcp-failure-handoff.md` for the canonical fallback and handoff payload.
- Use `references/allowlist-guidance.md` when a safe official CLI fallback is blocked by local rules.
- Recommend `explore-apple-swift-docs` directly when the task becomes Apple or Swift docs exploration work.
- Recommend `swift-package-workflow` directly when the task becomes ordinary SwiftPM package execution or manifest work.
- Recommend `format-swift-sources` directly when the task becomes SwiftLint or SwiftFormat setup, config export, or style-tooling maintenance work.
- Recommend `structure-swift-sources` directly when the task becomes structural source cleanup work.
- Recommend `bootstrap-swift-package` directly when the task becomes new-package scaffolding.
- Recommend `sync-xcode-project-guidance` directly when the repo needs Xcode-specific guidance sync rather than execution.
- `scripts/run_workflow.py` plans fallback commands; MCP execution itself remains agent-side tool usage guided by this skill.
- When maintaining this plugin itself, refresh repo-guidance consumers after substantial Xcode-policy changes and keep the local plugin install current; `install-plugin-to-socket` is a useful maintainer shortcut for install, update, verify, and repair work.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` reads customization state for the remaining user-facing execution knobs.
- MCP tool execution itself remains agent-side and is not performed by the local runtime entrypoint or by the skill as a direct runtime.

## References

### Workflow References

- `references/workflow-policy.md`
- `references/mcp-tool-matrix.md`
- `references/cli-fallback-matrix.md`
- `references/toolchain-management.md`
- `references/testing-plans-file-membership-and-configurations.md`
- `references/mutation-risk-policy.md`
- `references/mutation-via-mcp.md`

### Contract References

- `references/mcp-failure-handoff.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs Apple or Swift docs exploration or Dash-compatible docs access.
- Recommend `format-swift-sources` when the user needs SwiftLint or SwiftFormat setup rather than active Xcode execution.
- Recommend `structure-swift-sources` when the user needs structural Swift source cleanup rather than active Xcode execution.
- Recommend `sync-xcode-project-guidance` when the user needs repo guidance aligned inside an existing Xcode app repo.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs to add or merge the shared Xcode-project guidance into an end-user repo.
- `references/allowlist-guidance.md`
- `references/skills-installation.md`
- `references/skills-discovery.md`
- `references/snippets/apple-xcode-project-core.md`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/detect_xcode_managed_scope.sh`
- `scripts/customization_config.py`
