---
name: xcode-app-project-workflow
description: Compatibility workflow surface for broad or legacy Xcode execution requests. Use when older references still point at xcode-app-project-workflow and route the request into xcode-build-run-workflow or xcode-testing-workflow while preserving the direct .pbxproj warning boundary.
---

# Xcode App Project Workflow

## Purpose

Use this skill as a compatibility surface for older references to `xcode-app-project-workflow` while the repo transitions to narrower Xcode execution skills. The real long-term owners are `xcode-build-run-workflow` for build, run, diagnostics, toolchain, and guarded mutation work and `xcode-testing-workflow` for Swift Testing, XCTest, XCUITest, and `.xctestplan` work. `scripts/run_workflow.py` is intentionally routing-only now: it infers enough workspace context to choose the real owner and preserves the direct `.pbxproj` warning boundary so older flows continue to work during the migration window.

## When To Use

- Use this skill when older docs, prompts, or install surfaces still name `xcode-app-project-workflow`.
- Use this skill when the request is broad and the first job is deciding between the narrower Xcode build/run and testing skills.
- Use this skill after Apple or Swift docs have already been gathered through `explore-apple-swift-docs` and the work has shifted into Xcode-aware execution or implementation.
- Do not use this skill as the default path for ordinary Xcode build/run work or ordinary Xcode testing work now that narrower skills exist.
- Do not use this skill as the default path for ordinary Swift package development when `Package.swift` is the source of truth and Xcode-managed behavior is not the main concern.
- Recommend `xcode-build-run-workflow` when the task is primarily about workspace inspection, diagnostics, build, run, previews, toolchain work, file membership, Metal-toolchain-aware execution, or guarded mutation.
- Recommend `xcode-testing-workflow` when the task is primarily about Swift Testing, XCTest, XCUITest, `.xctestplan`, test filtering, retries, or test diagnosis.
- Recommend `explore-apple-swift-docs` when the user needs Apple or Swift documentation lookup, source selection, Dash compatibility, or docs install follow-up rather than execution work.
- Recommend `format-swift-sources` when the user needs to integrate or maintain SwiftLint or SwiftFormat across CLI, Xcode, SwiftPM, Git hooks, GitHub Actions, or SwiftFormat config export rather than active Xcode execution work.
- Recommend `structure-swift-sources` when the user needs file splitting, source-tree cleanup, DocC coverage, or TODO/FIXME ledger normalization rather than active Xcode execution work.
- Recommend `bootstrap-swift-package` when the user needs to create a brand new Swift package rather than work inside an existing Xcode or Swift project.
- Recommend `swift-package-build-run-workflow` or `swift-package-testing-workflow` when the task is ordinary SwiftPM package development outside Xcode-managed execution.
- Recommend `sync-xcode-project-guidance` when an existing Xcode app repo needs `AGENTS.md` or workflow-guidance alignment rather than active engineering work.
- Mention that older references to `apple-xcode-workflow` now map through this compatibility surface.

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
4. Run `scripts/run_workflow.py` to preserve the direct `.pbxproj` warning safeguard and route the request toward the narrower Xcode build/run or testing skill.
5. Use `references/mcp-tool-matrix.md`, `references/cli-fallback-matrix.md`, and `references/testing-plans-file-membership-and-configurations.md` only to explain why the narrower skill should take over; do not rebuild a second Xcode execution-planning surface here.
6. Report the Apple docs relied on, the direct `.pbxproj` warning result when relevant, and the recommended narrower skill.

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
  - direct edits are allowed by default when they do not directly edit `.pbxproj`

## Outputs

- `status`
  - `handoff`: the workflow is routing the request into the narrower Xcode build/run or testing skill
  - `blocked`: prerequisites, policy, or mutation safeguards prevented completion
- `path_type`
  - `primary`: the compatibility-routing path completed successfully
- `output`
  - operation type
  - `guard_result`
  - `recommended_skill`
  - one next step payload when needed

## Guards and Stop Conditions

- Apply the mutation safeguard from `references/mutation-risk-policy.md` only when the operation type is `mutation`.
- Do not skip the explicit warning path for direct `.pbxproj` edits.
- Stop with `handoff` when the request should move into `xcode-build-run-workflow` or `xcode-testing-workflow`.
- Stop with `blocked` when the required workspace context cannot be resolved and the operation cannot safely continue.

## Fallbacks and Handoffs

- This skill now routes to the narrower Xcode execution skills rather than acting as the primary execution owner itself.
- Do not let this compatibility surface regrow concrete Xcode command-planning logic; keep it limited to routing context, the `.pbxproj` safeguard, and one concise next step.
- Hand off to `xcode-build-run-workflow` when the request is primarily about workspace inspection, diagnostics, build, run, previews, file membership, toolchains, Metal-aware execution, or guarded mutation.
- Hand off to `xcode-testing-workflow` when the request is primarily about Swift Testing, XCTest, XCUITest, `.xctestplan`, flaky tests, retries, or test filtering.
- Recommend `explore-apple-swift-docs` directly when the task becomes Apple or Swift docs exploration work.
- Recommend `swift-package-build-run-workflow` or `swift-package-testing-workflow` directly when the task becomes ordinary SwiftPM package execution outside Xcode-managed work.
- Recommend `format-swift-sources` directly when the task becomes SwiftLint or SwiftFormat setup, config export, or style-tooling maintenance work.
- Recommend `structure-swift-sources` directly when the task becomes structural source cleanup work.
- Recommend `bootstrap-swift-package` directly when the task becomes new-package scaffolding.
- Recommend `sync-xcode-project-guidance` directly when the repo needs Xcode-specific guidance sync rather than execution.
- `scripts/run_workflow.py` preserves the direct `.pbxproj` warning path while routing toward the narrower skill that should really own the work.
- When maintaining this plugin itself, refresh repo-guidance consumers after substantial Xcode-policy changes and keep the local plugin install current; `install-plugin-to-socket` is a useful maintainer shortcut for install, update, verify, and repair work.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` reads customization state, but the current compatibility router keeps a fixed routing policy and does not expose ordinary user-facing knobs.
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
