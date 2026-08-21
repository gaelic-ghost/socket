---
name: author-swift-docc-docs
description: Author and review DocC content in Swift components, including symbol comments, articles, extension files, landing pages, topic groups, and light tutorial-aware review. Use when the user wants help writing or reviewing DocC content, checking DocC structure or content correctness, or deciding which execution surface owns generation and export.
---

# Author Swift DocC Docs

## Purpose

Provide the canonical DocC authoring-and-review workflow for Swift components. `scripts/run-workflow.fsx` classifies the task and, only when execution is needed, selects SwiftPM or Xcode according to the requested generation operation.

## When To Use

- Use this skill for in-source symbol documentation work that is meant to compile into DocC output.
- Use this skill for DocC article writing and review.
- Use this skill for DocC extension-file, landing-page, topic-group, and catalog-structure work.
- Use this skill when the user wants a DocC-oriented review pass for clarity, content accuracy, or DocC-specific structure quality.
- Use this skill when the user wants help deciding whether content belongs in source comments, articles, extension files, or landing pages.
- Use this skill for tutorial-aware DocC review when the user clearly wants DocC tutorial help but the task is still mainly about authoring shape and conceptual flow rather than directive-deep mechanics.
- Recommend `explore-apple-swift-docs` when the user really needs broader Apple or Swift documentation lookup, WWDC-material lookup, or directive-reference lookup instead of DocC authoring or review work.
- Recommend `swift-package-build-run-workflow` for SwiftPM DocC generation and package-oriented follow-through.
- Recommend `xcode-build-run-workflow` for `Product > Build Documentation`, `xcodebuild docbuild`, scheme, export, archive, or project-integrity follow-through.

## Single-Path Workflow

1. Classify the DocC task:
   - `symbol-docs`
   - `article`
   - `structure`
   - `review`
   - `tutorial-aware-review`
2. Run `scripts/run-workflow.fsx` so task inference, tutorial-depth boundaries, and handoff rules resolve into one JSON contract.
4. If the request is actually broad Apple-docs lookup, hand off to `explore-apple-swift-docs`.
4. If the request is DocC generation, export, hosting, archive, or project-integrity follow-through, select the execution surface required by that operation and hand off to its owner.
6. Otherwise stay local to DocC authoring and review:
   - revise or review source comments
   - revise or review articles and extension files
   - review landing-page and topic-group structure
   - explain the difference between content correctness, DocC correctness, and project correctness
6. Return one `status`, one `path_type`, one resolved task type, optional execution surface, and one next-step contract.

## Inputs

- `repo_path`: optional filesystem root to inspect for `Package.swift`, `.xcodeproj`, `.xcworkspace`, and `.docc` surfaces
- `execution_surface`: optional explicit generation override; use `swiftpm` or `xcode`
- `task_type`: optional explicit override; use `symbol-docs`, `article`, `structure`, `review`, or `tutorial-aware-review`
- `request`: optional free-text task description used for inference and handoff decisions
- `needs_generation`: optional explicit flag for generation, export, archive, hosting, or other execution-heavy DocC follow-through

## Outputs

- `status`
  - `success`: the request belongs to this DocC authoring-and-review workflow
  - `handoff`: the request belongs to another skill after DocC-aware classification
  - `blocked`: the request lacks enough task information, or a generation request lacks an execution surface
- `path_type`
  - `primary`: the DocC authoring-and-review path completed or the direct handoff decision is ready
  - `fallback`: the result depended on request-only inference because repo inspection was unavailable
- `output`
  - optional resolved `execution_surface`
  - resolved `task_type`
  - detected repo surfaces
  - tutorial support level
  - correctness model guidance
  - recommended skill when handing off
  - one concise next step

## Guards and Stop Conditions

- Do not pretend the skill has already validated DocC generation or export success unless the work hands off and those steps actually run.
- Do not silently absorb broad Apple-docs lookup that belongs in `explore-apple-swift-docs`.
- Do not silently absorb build, export, archive, hosting, or project-integrity work that belongs in the execution skills.
- Stop with `blocked` when the task type cannot be inferred, or a generation operation has no resolvable execution surface.
- Keep tutorial support phase-one light; do not imply full tutorial-directive expertise unless the deeper DocC references are consulted explicitly.

## Fallbacks and Handoffs

- Prefer explicit `execution_surface` and `task_type` when the user provides them.
- Fall back to repo inspection when `repo_path` is available.
- Fall back to request-text inference when repo inspection is missing or incomplete.
- Hand off to `explore-apple-swift-docs` when the request is primarily about finding DocC or Apple documentation rather than writing or reviewing DocC content.
- Hand off to `swift-package-build-run-workflow` when the requested generation operation is SwiftPM-owned.
- Hand off to `xcode-build-run-workflow` when the requested generation operation needs `docbuild`, a scheme, export, archive, or project-integrity follow-through.
- `scripts/run-workflow.fsx` is the top-level runtime entrypoint and converts repo inspection plus request inference into the documented JSON contract.

## Fixed Policy

- `scripts/run-workflow.fsx` uses the managed tutorial-depth policy.

## References

### Workflow References

- `references/xcode-docc-sources.md`
- `references/swift-docc-sources.md`
- `references/execution-surface-and-handoffs.md`
- `../../shared/execution-surface-routing.md`

### Contract References

- `references/automation-prompts.md`

### Support References

- `references/docc-correctness-model.md`

### Script Inventory

- `scripts/run-workflow.fsx`
