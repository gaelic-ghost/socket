---
name: migrate-xcode-project-to-xcodegen
description: Migrate or modernize native Apple app projects into the current XcodeGen baseline. Use when an existing macOS, iOS, or iPadOS app has a hand-managed .xcodeproj that should become XcodeGen-managed, when an existing project.yml is stale or broken, when Xcode GUI build settings/capabilities must be promoted into .xcconfig, .entitlements, Info.plist, schemes, test plans, or resource files before regeneration, or when Codex needs a safe non-destructive audit before running xcodegen generate.
---

# Migrate Xcode Project To XcodeGen

## Purpose

Convert existing native Apple app projects to the current XcodeGen baseline without losing user-made Xcode GUI changes. This skill owns migration planning, project-state inventory, promotion of generated `.pbxproj` state into tracked source files, and validation before any generated project is replaced.

## When To Use

- Use this skill when an existing Xcode-managed app project should move to XcodeGen.
- Use this skill when an existing `project.yml` should be modernized to the current baseline: synced folders, external `.xcconfig` layers, external entitlements, default asset catalog, and current Swift/Xcode build settings.
- Use this skill before regenerating an `.xcodeproj` when the repository has tracked `.pbxproj` changes from Xcode, XcodeGen, or another project-aware tool.
- Use this skill when Xcode GUI edits need to be moved back into `project.yml`, `.xcconfig`, `.entitlements`, `Info.plist`, `.xcscheme`, `.xctestplan`, or resources.
- Do not use this skill for brand-new app bootstrap; use `bootstrap-xcode-app-project`.
- Do not use this skill for ordinary build, run, diagnostics, previews, or file edits after migration; use `xcode-build-run-workflow`.
- Do not use this skill for test diagnosis except to preserve test-plan and test-target project state during migration; use `xcode-testing-workflow` for active testing work.
- Do not use this skill for plain Swift packages.

## Single-Path Workflow

1. Collect the required inputs:
   - `repo_root`
   - optional `project_path`
   - optional `project_yml`
   - optional `mode`
   - optional `dry_run`
2. Apply the Apple docs gate before proposing migration changes:
   - read the relevant Apple documentation first
   - use Xcode MCP `DocumentationSearch` or Xcode-local documentation first for Xcode project, build setting, asset catalog, signing, entitlement, and scheme behavior
   - use Dash MCP or Dash HTTP next when installed local docsets are a better fit
   - use XcodeGen's official docs or source repository for XcodeGen-specific behavior such as synced folders, source entries, configs, schemes, packages, and generated project output
   - state the documented behavior being relied on before proposing edits
   - if no relevant Apple or XcodeGen docs can be found, say that explicitly before proceeding
3. Run `scripts/run_workflow.py` from this skill to inventory the current repo and choose the migration path.
4. Classify the migration:
   - `xcode-managed-to-xcodegen`: repo has an `.xcodeproj` or `.xcworkspace` and no meaningful `project.yml`
   - `modernize-xcodegen`: repo already has `project.yml`
   - `blocked`: repo lacks enough project evidence or the requested mode conflicts with discovered files
5. Review the audit output before writing:
   - treat tracked `.pbxproj` diffs as intentional user/project state until reviewed
   - identify build settings that need `.xcconfig` owners
   - identify entitlements that need checked-in `.entitlements` owners
   - identify Info.plist values that need checked-in plist or build-setting owners
   - identify resources and asset catalogs that must be preserved under the broad app source root or under one separate top-level resource root when the repo actually has that shape
   - identify schemes and test plans that need explicit tracked files
6. Prepare the migration branch:
   - add or update `project.yml`
   - add or update `Configurations/*.xcconfig`
   - add or preserve the standard top-level directories: `Sources/`, `Tests/`, `Shared/`, `Extensions/`, `Configurations/`, `Scripts/`, and `Packages/`
   - add or update `Sources/Support/<AppName>.entitlements`
   - add or update `Sources/Support/Info.plist`
   - add or update `Sources/Resources/Assets.xcassets`
   - keep the app target's XcodeGen source declaration collapsed to one top-level `Sources` entry, shared app/extension code collapsed to one top-level `Shared` entry, and the test target's declaration collapsed to one top-level `Tests` entry
   - preserve exactly one app lifecycle entry point; do not create alternate `@main` app types, duplicate `main.swift` files, target-specific app entry files, or parallel app structs for variants
   - preserve existing package, framework, source, resource, script phase, scheme, and test-plan state
7. Generate into a temp or reviewed branch state:
   - run `xcodegen generate` only after promoted state is represented in tracked source files
   - never treat generated `.pbxproj` deletion or replacement as cleanup until the promoted files and generated result have been reviewed
8. Validate equivalence:
   - run `xcodebuild -list`
   - run `xcodebuild -showBuildSettings` for the main app target and compare key values against the pre-migration audit
   - run a Debug build when practical
   - run tests or at least `xcodebuild test -list-tests` when the repo has test targets
9. Hand off after migration:
   - use `sync-xcode-project-guidance` to refresh repo guidance when needed
   - use `xcode-build-run-workflow` for normal build/run work
   - use `xcode-testing-workflow` for test execution and diagnosis

## Inputs

- `repo_root`: optional absolute or relative repository root; defaults to `.`
- `project_path`: optional `.xcodeproj` or `.xcworkspace` path when discovery is ambiguous
- `project_yml`: optional XcodeGen spec path; defaults to `project.yml` under `repo_root` when present
- `mode`: `auto`, `xcode-managed`, or `xcodegen-modernize`; defaults to `auto`
- `dry_run`: optional flag; the audit workflow is non-mutating by default, so this mainly documents intent
- Defaults:
  - runtime entrypoint: executable `scripts/run_workflow.py`
  - audit implementation: `scripts/migrate_xcode_project_to_xcodegen.py`
  - no files outside the audit output are changed by the script
  - migration edits are performed by Codex after reviewing audit output and user intent

## Outputs

- `status`
  - `success`: project evidence was discovered and a migration plan was produced
  - `blocked`: required project evidence was missing or inconsistent with the requested mode
  - `failed`: the audit script could not inspect the repo
- `path_type`
  - `primary`: a supported migration or modernization path was identified
  - `fallback`: a non-mutating diagnostic result was returned
- `output`
  - resolved repo root
  - discovered Xcode project/workspace/spec/config markers
  - inferred migration path
  - XcodeGen baseline gaps
  - build settings that should be promoted to `.xcconfig`
  - entitlement, Info.plist, asset catalog, scheme, and test-plan evidence
  - recommended migration phases
  - validation commands to run after generation

## Guards and Stop Conditions

- Stop with `blocked` if `repo_root` cannot be resolved.
- Stop with `blocked` if no `.xcodeproj`, `.xcworkspace`, or `project.yml` is discovered.
- Stop with `blocked` if the user asks for Xcode-managed conversion but no project file is present.
- Stop with `blocked` if the user asks for XcodeGen modernization but no `project.yml` is present.
- Stop before running `xcodegen generate` if tracked `.pbxproj` changes have not been reviewed and promoted or explicitly preserved.
- Stop before replacing an `.xcodeproj` if generated output has not been compared against the audit and build settings.
- Stop before deleting legacy project files, schemes, configs, entitlements, or resources unless the replacement owner is tracked and validated.

## Fallbacks and Handoffs

- If project discovery is ambiguous, rerun the audit with `--project-path` or `--project-yml`.
- If the repo is a new project request, hand off to `bootstrap-xcode-app-project`.
- If the repo only needs guidance refresh, hand off to `sync-xcode-project-guidance`.
- If a migration uncovers build or test failures unrelated to project generation, hand off to `xcode-build-run-workflow` or `xcode-testing-workflow`.
- If the XcodeGen baseline cannot represent a project feature cleanly, preserve the hand-managed project and report the unsupported feature instead of forcing conversion.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- The current runtime-enforced customization surface is intentionally minimal; migration should be driven by discovered project state and explicit user intent rather than persistent broad defaults.
- Run the Python wrapper and customization entrypoints through `uv` when using customization commands, because repo skill scripts may rely on inline script metadata or local dependencies.

## References

### Workflow References

- `references/migration-audit-and-promotion.md`

### Contract References

- `references/customization-flow.md`

### Support References

- Recommend `references/snippets/apple-xcode-project-core.md` when an existing Xcode repo needs the reusable baseline policy content in a human-reviewable form.
- `references/snippets/apple-xcode-project-core.md`
- `bootstrap-xcode-app-project/references/xcodegen-synced-folder-and-config-notes.md`
- `bootstrap-xcode-app-project/references/project-generators.md`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/migrate_xcode_project_to_xcodegen.py`
- `scripts/customization_config.py`
