---
name: apple-swift-package-bootstrap
description: Bootstrap new Swift Package Manager projects with consistent defaults and fast setup. Use when creating a new Swift package (library, executable, or tool), scaffolding package structure, applying standard platform/version defaults, initializing git, running first-step validation, or when the user asks to customize bootstrap defaults in this skill.
---

# Apple Swift Package Bootstrap

## Purpose

Create a new Swift package repository with one top-level entry point, one deterministic scaffold path, explicit defaults, and verification grounded in the bundled bootstrap script.

## When To Use

- Use this skill for new Swift package scaffolding.
- Use this skill when the user wants consistent package defaults, `AGENTS.md` generation, and immediate validation.
- Use this skill when the user wants to customize the documented bootstrap defaults for future runs.
- Do not use this skill as the default path for normal Xcode app collaboration work.
- Recommend `apple-xcode-workflow` when the user is working in an existing Xcode project or needs Apple-platform execution after bootstrap.
- Recommend `apple-dash-docsets` when the user needs Dash docset search, install, or generation work.

## Single-Path Workflow

1. Collect the required inputs:
   - `name`
   - `type`
   - `destination`
   - `platform`
   - `version_profile`
   - optional `skip_validation`
2. Normalize aliases exactly as `scripts/bootstrap_swift_package.sh` does:
   - `macos -> mac`
   - `ios -> mobile`
   - `both -> multiplatform`
   - `latest -> latest-major`
   - `minus-one -> current-minus-one`
   - `minus-two -> current-minus-two`
3. Run the bundled script:
   ```bash
   scripts/bootstrap_swift_package.sh --name <Name> --type <library|executable|tool> --destination <dir> --platform <mac|macos|mobile|ios|multiplatform|both> --version-profile <latest-major|current-minus-one|current-minus-two|latest|minus-one|minus-two>
   ```
4. Verify the generated repository:
   - `Package.swift`
   - `.git`
   - `AGENTS.md`
   - `Tests/`
   - `swift build` and `swift test` unless `--skip-validation` was requested
5. Return one execution summary with the created path, normalized options, and validation result.

## Inputs

- `name`: required; must start with a letter and contain only letters, numbers, `_`, or `-`.
- `type`: `library`, `executable`, or advanced explicit `tool`.
- `destination`: parent directory for the new package.
- `platform`: `mac`, `mobile`, or `multiplatform`, with aliases normalized by the script.
- `version_profile`: `latest-major`, `current-minus-one`, or `current-minus-two`, with aliases normalized by the script.
- `skip_validation`: optional flag to skip `swift build` and `swift test`.
- Defaults:
  - `type` defaults to `library`
  - `destination` defaults to `.`
  - `platform` defaults to `multiplatform`
  - `version_profile` defaults to `current-minus-one`
  - validation runs unless `--skip-validation` is passed

## Outputs

- `status`
  - `success`: the package was created and verification succeeded
  - `blocked`: prerequisites or target-directory constraints prevented the run
  - `failed`: the script started but did not complete successfully
- `path_type`
  - `primary`: the bundled script completed successfully
  - `fallback`: manual scaffold guidance is being used instead of the bundled script
- `output`
  - resolved package path
  - normalized `type`, `platform`, and `version_profile`
  - validation result
  - one concise next step

## Guards and Stop Conditions

- Stop with `blocked` if `swift` is missing.
- Stop with `blocked` if `git` is missing.
- Stop with `blocked` if `assets/AGENTS.md` is missing.
- Stop with `blocked` if the target exists and contains non-ignorable files.
- Do not claim that customization metadata changes the bootstrap script at runtime; it does not today.

## Fallbacks and Handoffs

- Preferred path is always `scripts/bootstrap_swift_package.sh`.
- Use manual `swift package init` guidance only when the script is unavailable or the user explicitly asks for the manual path.
- `tool` is an advanced explicit passthrough, not a default branch of the workflow.
- After a successful scaffold, hand off build, test, or Apple-platform execution tasks to `apple-xcode-workflow`.
- Recommend `apple-dash-docsets` directly when the user’s next step is Dash docset or cheatsheet management.

## Customization

- Use `references/customization-flow.md`.
- All documented customization knobs for this skill are `policy-only`.
- `scripts/customization_config.py` stores and reports customization state, but `scripts/bootstrap_swift_package.sh` does not auto-load those settings today.

## References

### Workflow References

- `references/package-types.md`

### Contract References

- `references/automation-prompts.md`
- `references/customization-flow.md`

### Support References

- Recommend `references/snippets/apple-swift-core.md` when the new package repo should start with reusable Apple and Swift baseline policy content next to the generated `AGENTS.md`.
- `assets/AGENTS.md`
- `references/snippets/apple-swift-core.md`

### Script Inventory

- `scripts/bootstrap_swift_package.sh`
- `scripts/customization_config.py`
