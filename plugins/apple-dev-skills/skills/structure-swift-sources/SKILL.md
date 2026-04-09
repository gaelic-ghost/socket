---
name: structure-swift-sources
description: Organize Swift source trees and oversized Swift files by feature, layer, and declaration group; split large files, normalize `// MARK:` sections, move TODO and FIXME text into ledger files, and add DocC comments. Use after `format-swift-sources` has established a clean formatting baseline.
---

# Structure Swift Sources

## Purpose

Use this skill as the top-level workflow for structural cleanup inside existing Swift repositories. It governs file splitting, file moves, section grouping, DocC coverage, and TODO or FIXME ledger extraction. It is not the formatter or linter integration authority; use `format-swift-sources` before this skill starts mutating source layout, and run `format-swift-sources` again after this skill finishes.

## When To Use

- Use this skill when the user wants to split oversized Swift files or move files into a clearer repo layout.
- Use this skill when the user wants consistent `// MARK:` sections, declaration grouping, or view-modifier extraction in SwiftUI code.
- Use this skill when the user wants TODO or FIXME text moved out of source files into repo ledger files.
- Use this skill when the user wants DocC comments added across Swift symbols as part of a structure or hygiene pass.
- Use this skill when a Swift package or Xcode app repo has drifted away from the intended feature-plus-layer directory shape.
- Recommend `format-swift-sources` first when formatter or linter setup is missing, unclear, or stale.
- Recommend `swift-package-build-run-workflow` or `swift-package-testing-workflow` when structural cleanup in a plain package repo turns into ordinary package execution or SwiftPM validation.
- Recommend `xcode-build-run-workflow` when structural cleanup turns into active Xcode execution, scheme validation, file-membership follow-through, or guarded project mutation work.
- Recommend `xcode-testing-workflow` when structural cleanup turns into active Xcode test validation or test-target diagnosis.
- Recommend `sync-xcode-project-guidance` or `sync-swift-package-guidance` when the real need is repo-level `AGENTS.md` alignment rather than source-structure cleanup.

## Single-Path Workflow

1. Classify the request:
   - repo layout cleanup
   - large-file split
   - section and MARK normalization
   - TODO or FIXME ledger extraction
   - DocC coverage pass
   - combined source-hygiene pass
2. Run or confirm `format-swift-sources` first:
   - use it to establish a clean baseline before file moves or file splits
   - if the repo does not have a clear formatter or linter path yet, stop and set that up first
3. Resolve the repo shape:
   - `swift-package`
   - `xcode-app-project`
   - `mixed`
4. Read the relevant references:
   - `references/glossary.md`
   - `references/layout-rules.md`
   - `references/source-organization-rules.md`
   - `references/todo-fixme-ledgers.md`
   - `references/automation-prompts.md`
5. Apply the structure rules:
   - strongly consider splitting a file once it exceeds `400` lines and clearly holds `2` or more separate concerns
   - always split a file once it exceeds `800` lines
   - when the underlying type is still one coherent type, extract grouped concerns into extension files such as `<Original>+Models.swift` or `<Original>+<Concern>.swift`
   - group declarations into explicit `// MARK: - <Heading>` sections, then place a descriptive secondary `// MARK: <Comment>` line directly below each heading
   - ensure every symbol declaration has DocC-compliant documentation comments
   - move TODO and FIXME text into `TODO.md` and `FIXME.md`, keeping only ticket IDs in source comments
  - when the task is TODO or FIXME normalization, use `scripts/normalize_todo_fixme_ledgers.py` for the deterministic ledger rewrite pass across supported Swift and Objective-C source forms
6. Apply repo-shape rules:
   - for Swift packages, prefer directories grouped by layer and feature, such as `API/<Feature>/<Concern>.swift` and `Features/<Feature>/<Concern>.swift`
   - for Xcode app projects, ensure important app-facing source directories such as `Views/`, `Controllers/`, and `Models/`
   - for SwiftUI views, keep view files in `Views/` and pair them with `<Name>+Model.swift` and `<Name>+Modifier.swift` files when those concerns exist
7. Finish with `format-swift-sources` again so the moved or split files end in a normalized state.

## Inputs

- `cleanup_kind`: one of the request classes above
- `repository_kind`: `swift-package`, `xcode-app-project`, or `mixed`
- `target_scope`: optional narrowed scope such as one file, one feature directory, or the whole repo
- `split_mode`: optional; use values such as `advisory`, `required`, or `full-pass`
- `docc_scope`: optional; use values such as `public-only`, `all-symbols`, or `changed-symbols`
- `todo_fixme_mode`: optional; use values such as `report-only`, `rewrite-ledgers`, or `normalize-existing`
- Defaults:
  - run `format-swift-sources` before and after structural mutation
  - prefer feature-plus-layer layout over flat buckets when the repo has meaningful feature boundaries
  - prefer extracted extensions before inventing new wrapper types
  - prefer `TODO.md` and `FIXME.md` as separate ledger files
  - prefer symbol-level DocC coverage during a full cleanup pass

## Outputs

- `status`
  - `success`: a supported structure path was selected and explained
  - `handoff`: another skill should take the next step
  - `blocked`: the request lacks a safe structural path or the repo shape is too unclear
- `path_type`
  - `primary`: the documented structure path completed
  - `fallback`: a narrower safe pass was chosen
- `output`
  - `cleanup_kind`
  - `repository_kind`
  - `recommended_path`
  - `layout_targets`
  - `split_targets`
  - `ledger_files`
  - `caveats`
  - `verification`

## Guards and Stop Conditions

- Do not split files purely by line count when the code still represents one small, coherent concern and the real problem is formatting or comments.
- Do not invent new abstraction layers just to make a file shorter.
- Do not move files across Xcode-managed boundaries without accounting for project membership and validation.
- Do not rewrite TODO or FIXME comments into ledger IDs unless the ledger files are updated in the same pass.
- Stop with `blocked` when the repo shape is too ambiguous to choose feature-first versus layer-first layout safely.
- Stop with `handoff` when project-file mutation or Xcode membership updates need guarded execution through `xcode-build-run-workflow`.

## Fallbacks and Handoffs

- If the repo lacks a clear formatter or linter baseline, hand off to `format-swift-sources` before any structural mutation.
- If a broad repo-wide cleanup is too risky, fall back to one feature directory or one oversized file at a time.
- If Xcode project integrity must be revalidated after file moves, hand off to `xcode-build-run-workflow`.
- Recommend `sync-xcode-project-guidance` or `sync-swift-package-guidance` when the request is really about durable repo rules rather than current-file cleanup.

## Customization

- This skill currently has no durable customization surface.
- Keep split thresholds, ledger names, and MARK conventions as workflow policy unless a real repeat customization need appears.

## References

### Workflow References

- `references/glossary.md`
- `references/layout-rules.md`
- `references/source-organization-rules.md`
- `references/todo-fixme-ledgers.md`

### Contract References

- `references/automation-prompts.md`

### Support References

- Recommend `format-swift-sources` first for formatter or linter setup and again after structural edits complete.
- Recommend `references/layout-rules.md` when the user needs the package-versus-app directory contract explained.

### Script Inventory

- `scripts/normalize_todo_fixme_ledgers.py`
