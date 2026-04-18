---
name: structure-swift-sources
description: Organize Swift source trees and oversized Swift files by feature, layer, and declaration group; split large files, normalize `// MARK:` sections, enforce plain-language block-comment file headers, and move TODO and FIXME text into ledger files. Use after `format-swift-sources` has established a clean formatting baseline.
---

# Structure Swift Sources

## Purpose

Use this skill as the top-level workflow for structural cleanup inside existing Swift repositories. It governs file splitting, file moves, section grouping, plain-language file headers, and TODO or FIXME ledger extraction. `scripts/run_workflow.py` is the runtime wrapper for repo-shape detection, cleanup-kind classification, header-policy loading, split-threshold loading, and clean handoffs to DocC or Xcode execution workflows. It is not the formatter or linter integration authority, and it is not the DocC authoring authority. Use `format-swift-sources` before this skill starts mutating source layout, use `author-swift-docc-docs` when the request becomes symbol-doc or DocC-content work, and run `format-swift-sources` again after this skill finishes.

## When To Use

- Use this skill when the user wants to split oversized Swift files or move files into a clearer repo layout.
- Use this skill when the user wants high-signal `// MARK:` sections, declaration grouping, or view-modifier extraction in SwiftUI code.
- Use this skill when the user wants consistent block-comment file headers that describe a file's purpose and area of concern in plain terms.
- Use this skill when the user wants structured project-and-file banner headers with deterministic project, filename, copyright, and optional cross-reference fields.
- Use this skill when the user wants TODO or FIXME text moved out of source files into repo ledger files.
- Use this skill when a Swift package or Xcode app repo has drifted away from the intended feature-plus-layer directory shape.
- Recommend `format-swift-sources` first when formatter or linter setup is missing, unclear, or stale.
- Recommend `author-swift-docc-docs` when the task becomes symbol documentation, DocC article work, landing-page structure, topic groups, or DocC-oriented review.
- Recommend `swift-package-build-run-workflow` or `swift-package-testing-workflow` when structural cleanup in a plain package repo turns into ordinary package execution or SwiftPM validation.
- Recommend `xcode-build-run-workflow` when structural cleanup turns into active Xcode execution, scheme validation, file-membership follow-through, or guarded project mutation work.
- Recommend `xcode-testing-workflow` when structural cleanup turns into active Xcode test validation or test-target diagnosis.
- Recommend `sync-xcode-project-guidance` or `sync-swift-package-guidance` when the real need is repo-level `AGENTS.md` alignment rather than source-structure cleanup.

## Single-Path Workflow

1. Classify the request:
   - repo layout cleanup
   - large-file split
   - section and MARK normalization
   - file-header normalization
   - TODO or FIXME ledger extraction
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
   - `references/file-headers.md`
   - `references/todo-fixme-ledgers.md`
   - `references/automation-prompts.md`
   - `references/customization-flow.md`
5. Apply the structure rules:
   - strongly consider splitting a file once it exceeds the configured soft split threshold and clearly holds `2` or more separate concerns
   - always split a file once it exceeds the configured hard split threshold
   - when the underlying type is still one coherent type, extract grouped concerns into extension files such as `<Original>+Models.swift` or `<Original>+<Concern>.swift`
   - add `// MARK:` groups only when a file is large enough or varied enough that the grouping materially improves navigation, concern ownership, or declaration discovery
   - skip `// MARK:` groups entirely when a short file or an already-obvious declaration run does not present meaningful navigation ambiguity
   - when groups are warranted, use explicit `// MARK: - <Heading>` sections that name a real responsibility boundary instead of restating declaration kinds or symbol names in slightly different words
   - add a secondary `// MARK: <Comment>` line only when it answers a useful navigation question such as why this section exists, what job it serves, or how it differs from nearby sections
   - never use headings or secondary comments that just restate an obvious type, symbol, or method name, narrate intuitive code in a small file, or pad the file with redundant structure
   - require or recommend the documented project-and-file banner header according to the effective header policy
   - keep `Concern` and `Purpose` text in plain terms that explain what the file owns and what job it does, instead of repeating the filename or symbol names as jargon
   - treat `Key Types` and `See Also` as optional high-signal fields rather than mandatory filler
   - move TODO and FIXME text into `TODO.md` and `FIXME.md`, keeping only ticket IDs in source comments
   - when the task is TODO or FIXME normalization, use `scripts/normalize_todo_fixme_ledgers.py` for the deterministic ledger rewrite pass across supported Swift and Objective-C source forms
   - when the task is file-header normalization or a full cleanup pass that includes headers, use `scripts/normalize_swift_file_headers.py` to audit or apply the documented header shape
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
- Stop with `blocked` when the repo shape is too ambiguous to choose feature-first versus layer-first layout safely.
- Stop with `handoff` when project-file mutation or Xcode membership updates need guarded execution through `xcode-build-run-workflow`.

## Fallbacks and Handoffs

- If the repo lacks a clear formatter or linter baseline, hand off to `format-swift-sources` before any structural mutation.
- If a broad repo-wide cleanup is too risky, fall back to one feature directory or one oversized file at a time.
- If the request becomes symbol-doc or DocC-content work, hand off to `author-swift-docc-docs`.
- If Xcode project integrity must be revalidated after file moves, hand off to `xcode-build-run-workflow`.
- `scripts/run_workflow.py` is the top-level runtime entrypoint and converts repo inspection plus request inference into the documented JSON contract.
- Recommend `sync-xcode-project-guidance` or `sync-swift-package-guidance` when the request is really about durable repo rules rather than current-file cleanup.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` loads the runtime-enforced header policy and split thresholds before shaping the final workflow contract.

## References

### Workflow References

- `references/glossary.md`
- `references/layout-rules.md`
- `references/source-organization-rules.md`
- `references/file-headers.md`
- `references/todo-fixme-ledgers.md`

### Contract References

- `references/automation-prompts.md`
- `references/customization-flow.md`

### Support References

- Recommend `format-swift-sources` first for formatter or linter setup and again after structural edits complete.
- Recommend `references/layout-rules.md` when the user needs the package-versus-app directory contract explained.

### Script Inventory

- `scripts/customization_config.py`
- `scripts/run_workflow.py`
- `scripts/normalize_todo_fixme_ledgers.py`
- `scripts/normalize_swift_file_headers.py`
- `references/file-header-inventory.template.yaml`
