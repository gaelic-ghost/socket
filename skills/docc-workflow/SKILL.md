---
name: docc-workflow
description: Author and review DocC content for Swift package and Xcode app or framework repositories, including symbol comments, articles, extension files, landing pages, topic groups, and light tutorial-aware review. Use when the user wants help writing or reviewing DocC content, checking DocC structure or content correctness, or deciding when DocC work should hand off to Apple docs lookup or build and export workflows.
---

# DocC Workflow

## Purpose

Provide the canonical DocC authoring-and-review workflow for Swift package and Xcode app or framework repositories. `scripts/run_workflow.py` is the runtime wrapper for repo-shape detection, task classification, tutorial-depth boundaries, and clean handoffs to the Apple docs and execution skills.

## When To Use

- Use this skill for in-source symbol documentation work that is meant to compile into DocC output.
- Use this skill for DocC article writing and review.
- Use this skill for DocC extension-file, landing-page, topic-group, and catalog-structure work.
- Use this skill when the user wants a DocC-oriented review pass for clarity, content accuracy, or DocC-specific structure quality.
- Use this skill when the user wants help deciding whether content belongs in source comments, articles, extension files, or landing pages.
- Use this skill for tutorial-aware DocC review when the user clearly wants DocC tutorial help but the task is still mainly about authoring shape and conceptual flow rather than directive-deep mechanics.
- Recommend `explore-apple-swift-docs` when the user really needs broader Apple or Swift documentation lookup, WWDC-material lookup, or directive-reference lookup instead of DocC authoring or review work.
- Recommend `swift-package-build-run-workflow` when a Swift package repo needs `swift package` or build-oriented DocC follow-through such as generation, export, archive inspection, or package-shape execution work.
- Recommend `xcode-build-run-workflow` when an Xcode app or framework repo needs `Product > Build Documentation`, `xcodebuild docbuild`, export, archive, or project-integrity follow-through.

## Single-Path Workflow

1. Classify the repo shape:
   - `swift-package`
   - `xcode-app-framework`
2. Classify the DocC task:
   - `symbol-docs`
   - `article`
   - `structure`
   - `review`
   - `tutorial-aware-review`
3. Run `scripts/run_workflow.py` so the repo-shape heuristics, task inference, tutorial-depth boundary, and handoff rules resolve into one JSON contract.
4. If the request is actually broad Apple-docs lookup, hand off to `explore-apple-swift-docs`.
5. If the request is actually DocC generation, export, hosting, archive, or project-integrity follow-through, hand off to the matching build-run skill for the detected repo shape.
6. Otherwise stay local to DocC authoring and review:
   - revise or review source comments
   - revise or review articles and extension files
   - review landing-page and topic-group structure
   - explain the difference between content correctness, DocC correctness, and project correctness
7. Return one `status`, one `path_type`, one resolved repo shape, one resolved task type, and one next-step contract.

## Inputs

- `repo_path`: optional filesystem root to inspect for `Package.swift`, `.xcodeproj`, `.xcworkspace`, and `.docc` surfaces
- `repo_shape`: optional explicit override; use `swift-package` or `xcode-app-framework`
- `task_type`: optional explicit override; use `symbol-docs`, `article`, `structure`, `review`, or `tutorial-aware-review`
- `request`: optional free-text task description used for inference and handoff decisions
- `needs_generation`: optional explicit flag for generation, export, archive, hosting, or other execution-heavy DocC follow-through
- Defaults:
  - runtime entrypoint: executable `scripts/run_workflow.py`
  - tutorial handling defaults to the configured first-pass policy in `references/customization-flow.md`
  - repo-shape inference prefers an explicit override, then on-disk detection, then request wording
  - task inference prefers an explicit override, then request wording

## Outputs

- `status`
  - `success`: the request belongs to this DocC authoring-and-review workflow
  - `handoff`: the request belongs to another skill after DocC-aware classification
  - `blocked`: the request lacks enough repo-shape or task information to proceed honestly
- `path_type`
  - `primary`: the DocC authoring-and-review path completed or the direct handoff decision is ready
  - `fallback`: the result depended on request-only inference because repo inspection was unavailable
- `output`
  - resolved `repo_shape`
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
- Stop with `blocked` when neither repo shape nor task type can be inferred honestly.
- Keep tutorial support phase-one light; do not imply full tutorial-directive expertise unless the deeper DocC references are consulted explicitly.

## Fallbacks and Handoffs

- Prefer explicit `repo_shape` and `task_type` when the user provides them.
- Fall back to repo inspection when `repo_path` is available.
- Fall back to request-text inference when repo inspection is missing or incomplete.
- Hand off to `explore-apple-swift-docs` when the request is primarily about finding DocC or Apple documentation rather than writing or reviewing DocC content.
- Hand off to `swift-package-build-run-workflow` when a package repo needs generation, export, archive, or build-oriented DocC follow-through.
- Hand off to `xcode-build-run-workflow` when an Xcode repo needs generation, export, archive, `docbuild`, or project-integrity follow-through.
- `scripts/run_workflow.py` is the top-level runtime entrypoint and converts repo inspection plus request inference into the documented JSON contract.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` loads the runtime-safe tutorial-depth setting before shaping the final workflow contract.

## References

### Workflow References

- `references/xcode-docc-sources.md`
- `references/swift-docc-sources.md`
- `references/repo-shape-and-handoffs.md`

### Contract References

- `references/automation-prompts.md`
- `references/customization-flow.md`

### Support References

- `references/docc-correctness-model.md`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/customization_config.py`
