---
name: structure-swift-sources
description: Organize Swift source trees and oversized Swift files by feature, layer, and declaration group; split large files, normalize `// MARK:` sections, enforce plain-language block-comment file headers, and move TODO and FIXME text into ledger files. Use after `format-swift-sources` has established a clean formatting baseline.
---

# Structure Swift Sources

## Purpose

Use this skill as the top-level workflow for structural cleanup inside existing Swift components. It governs file splitting, file moves, section grouping, plain-language file headers, and TODO or FIXME ledger extraction. `scripts/run-workflow.fsx` classifies the cleanup, loads policy, and hands off only DocC content or Xcode-owned membership operations. It is not the formatter or linter integration authority, and it is not the DocC authoring authority.

## When To Use

- Use this skill when the user wants to split oversized Swift files or move files into a clearer repo layout.
- Use this skill when the user wants high-signal `// MARK:` sections, declaration grouping, or view-modifier extraction in SwiftUI code.
- Use this skill when the user wants consistent block-comment file headers that describe a file's purpose and area of concern in plain terms.
- Use this skill when the user wants structured project-and-file banner headers with deterministic project, filename, copyright, and optional cross-reference fields.
- Use this skill when the user wants TODO or FIXME text moved out of source files into repo ledger files.
- Use this skill when a Swift package or Xcode app repo has drifted away from the intended feature-plus-layer directory shape.
- Recommend `format-swift-sources` first when formatter or linter setup is missing, unclear, or stale.
- Recommend `author-swift-docc-docs` when the task becomes symbol documentation, DocC article work, landing-page structure, topic groups, or DocC-oriented review.
- Recommend `swift-package-build-run-workflow` or `swift-package-testing-workflow` when structural cleanup turns into ordinary package execution or SwiftPM validation.
- Recommend `xcode-build-run-workflow` when structural cleanup turns into active Xcode execution, scheme validation, file-membership follow-through, or guarded project mutation work.
- Recommend `xcode-testing-workflow` when structural cleanup turns into active Xcode test validation or test-target diagnosis.
- Recommend `bootstrap-xcode-workspace --operation align` for product guidance alignment. A deliberately standalone package uses its own explicit repository-maintenance contract.

## Single-Path Workflow

## Inputs

- `cleanup_kind`: one of the request classes above
- `target_scope`: optional narrowed scope such as one file, one feature directory, or the whole repo
- `split_mode`: optional; use values such as `advisory`, `required`, or `full-pass`
- `todo_fixme_mode`: optional; use values such as `report-only`, `rewrite-ledgers`, or `normalize-existing`
- `file_header_mode`: optional; use values such as `advisory` or `required`
- `file_header_style`: optional; currently `project-banner`
- Defaults:
  - run `format-swift-sources` before and after structural mutation
  - prefer feature-plus-layer layout over flat buckets when the repo has meaningful feature boundaries
  - prefer extracted extensions before inventing new wrapper types
  - prefer `TODO.md` and `FIXME.md` as separate ledger files
  - prefer the project-and-file banner header described in `references/file-headers.md`

## Outputs

- `status`
  - `success`: a supported structure path was selected and explained
  - `handoff`: another skill should take the next step
  - `blocked`: the request lacks a safe structural path or cleanup kind
- `path_type`
  - `primary`: the documented structure path completed
  - `fallback`: a narrower safe pass was chosen
- `output`
  - `cleanup_kind`
  - `recommended_path`
  - `layout_targets`
  - `split_targets`
  - `ledger_files`
  - `header_policy`
  - `helper_scripts`
  - `caveats`
  - `verification`

## Guards and Stop Conditions

- Do not split files purely by line count when the code still represents one small, coherent concern and the real problem is formatting or comments.
- Do not invent new abstraction layers just to make a file shorter.
- Do not move files across Xcode-managed boundaries without accounting for project membership and validation.
- Do not treat file-header automation as permission to invent vague or generic purpose text. Header content must come from the actual code understanding or an explicit inventory.
- Do not make end users reverse-engineer the file-header inventory shape from prose or tests. Point them at `references/file-header-inventory.template.yaml` when `--apply --inventory` is the right path.
- Do not rewrite TODO or FIXME comments into ledger IDs unless the ledger files are updated in the same pass.
- Do not absorb symbol-doc or DocC-content work; hand that off to `author-swift-docc-docs`.
- Stop with `blocked` when the cleanup kind or target scope is too ambiguous to mutate safely.
- Stop with `handoff` when project-file mutation or Xcode membership updates need guarded execution through `xcode-build-run-workflow`.

## Fallbacks and Handoffs

- If the repo lacks a clear formatter or linter baseline, hand off to `format-swift-sources` before any structural mutation.
- If a broad repo-wide cleanup is too risky, fall back to one feature directory or one oversized file at a time.
- If the request becomes symbol-doc or DocC-content work, hand off to `author-swift-docc-docs`.
- If Xcode project integrity must be revalidated after file moves, hand off to `xcode-build-run-workflow`.
- `scripts/run-workflow.fsx` is the top-level runtime entrypoint and converts component inspection plus request inference into the documented JSON contract.
- Recommend `bootstrap-xcode-workspace --operation align` when the request is really about durable product rules.

## Fixed Policy

- `scripts/run-workflow.fsx` uses the managed header policy and fixed split thresholds.

## References

### Workflow References

- `references/glossary.md`
- `references/layout-rules.md`
- `references/source-organization-rules.md`
- `references/file-headers.md`
- `references/todo-fixme-ledgers.md`

### Contract References

- `references/automation-prompts.md`

### Support References

- Recommend `format-swift-sources` first for formatter or linter setup and again after structural edits complete.
- Recommend `references/layout-rules.md` when the user needs the package-versus-app directory contract explained.

### Script Inventory

- `scripts/run-workflow.fsx`
- `scripts/normalize-swift-structure.fsx`
- `scripts/normalize-swift-structure.fsx`
- `references/file-header-inventory.template.yaml`
