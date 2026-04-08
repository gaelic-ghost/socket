---
name: xcode-build-run-workflow
description: Guide build, run, preview-adjacent, workspace-inspection, diagnostics, toolchain, and guarded mutation work in existing Xcode-managed projects and workspaces. Use when Xcode-aware execution is needed and the task is primarily about build, run, or project-integrity work rather than testing.
---

# Xcode Build Run Workflow

## Purpose

Use this skill as the primary execution workflow for non-testing work in or around Xcode-managed projects and workspaces. Keep it focused on workspace inspection, read/search diagnostics, builds, runs, previews, toolchain management, file membership, Release-versus-Debug validation, and the `.pbxproj` warning boundary. `scripts/run_workflow.py` is the runtime entrypoint for MCP-first build/run execution, official CLI fallback planning, and direct `.pbxproj` warning enforcement.

## When To Use

- Use this skill for Xcode workspace inspection, project discovery, read/search diagnostics, build, run, preview, and navigator-issue tasks.
- Use this skill for Xcode MCP operations, scheme-aware execution, and official Apple CLI fallback when the work is primarily about build/run rather than tests.
- Use this skill when direct filesystem mutation around an Xcode-managed project may be required.
- Use this skill for file-membership and target-membership verification after on-disk edits.
- Use this skill for Debug/Release build-configuration work, artifacts, archives, toolchain checks, and Metal-toolchain-aware build execution.
- Do not use this skill as the default path for Swift Testing, XCTest, XCUITest, `.xctestplan`, flaky-test diagnosis, retries, or test filtering.
- Recommend `xcode-testing-workflow` when the task is primarily about tests or test diagnosis.
- Recommend `explore-apple-swift-docs` when the user needs Apple or Swift documentation lookup rather than execution work.
- Recommend `swift-package-build-run-workflow` or `swift-package-testing-workflow` when the task is ordinary SwiftPM package work outside Xcode-managed execution.
- Recommend `sync-xcode-project-guidance` when an existing Xcode app repo needs `AGENTS.md` or workflow-guidance alignment rather than active engineering work.

## Single-Path Workflow

1. Classify the request into one operation type:
   - workspace or session inspection
   - read, search, or diagnostics
   - build or run
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
4. Run `scripts/run_workflow.py` to apply runtime configuration, `.pbxproj` warning safeguards, and CLI fallback planning.
5. Use the guidance in `references/mcp-tool-matrix.md` for agent-executed MCP operations.
6. Use `references/testing-plans-file-membership-and-configurations.md` when the task touches file membership after filesystem edits or Debug/Release validation.
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
  - `handoff`: the workflow is handing off to another skill because the request is actually test-focused
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
- Stop with `handoff` when the request is really test-focused work.
- Stop with `blocked` when the required workspace context cannot be resolved and the operation cannot safely continue.
- Stop with `blocked` when allowlist or sandbox rules prevent the official CLI fallback and no safe alternative exists.

## Fallbacks and Handoffs

- Official CLI execution is the only fallback path when the primary agent-side MCP path cannot complete.
- Use `references/mcp-failure-handoff.md` for the canonical fallback and handoff payload.
- Use `references/allowlist-guidance.md` when a safe official CLI fallback is blocked by local rules.
- Hand off to `xcode-testing-workflow` when the request becomes primarily about Swift Testing, XCTest, XCUITest, `.xctestplan`, flaky tests, test retries, or test filtering.
- Recommend `explore-apple-swift-docs` directly when the task becomes Apple or Swift docs exploration work.
- Recommend `swift-package-build-run-workflow` or `swift-package-testing-workflow` directly when the task becomes ordinary SwiftPM package work.
- Recommend `format-swift-sources` directly when the task becomes SwiftLint or SwiftFormat setup, config export, or style-tooling maintenance work.
- Recommend `structure-swift-sources` directly when the task becomes structural source cleanup work.
- Recommend `bootstrap-swift-package` directly when the task becomes new-package scaffolding.
- Recommend `sync-xcode-project-guidance` directly when the repo needs Xcode-specific guidance sync rather than execution.
- `scripts/run_workflow.py` plans fallback commands; MCP execution itself remains agent-side tool usage guided by this skill.
- When maintaining this repository itself, refresh repo-guidance consumers after substantial Xcode-policy changes and keep the top-level export-surface docs aligned. Do not tell users to rely on repo-local installer workflows; this repository does not ship them.

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
