---
name: sync-xcode-project-guidance
description: Sync repo guidance for an existing native Apple app repository managed through Xcode when the user wants to add, merge, refresh, or align AGENTS.md and project workflow guidance. Use for existing macOS, iOS, or iPadOS app repos with an .xcodeproj or .xcworkspace. Do not use for brand-new app bootstrap or plain Swift packages.
---

# Sync Xcode Project Guidance

## Purpose

Bring an existing Xcode app repository up to the expected guidance baseline without overloading the main Xcode execution skill. This skill owns repo-guidance alignment for existing Apple app repos, including deterministic `AGENTS.md` creation or bounded section append behavior, and runs `maintain-project-repo` with the `xcode-app` profile alongside that guidance. `scripts/run_workflow.py` is the runtime entrypoint, and `scripts/sync_xcode_project_guidance.py` applies the current sync behavior.

## Companion Plugin Requirement

This skill can be discovered from a standalone `apple-dev-skills` install, but its mutating guidance-sync path refreshes repo-maintenance files through the companion [`productivity-skills`](https://github.com/gaelic-ghost/productivity-skills) plugin. Before giving filesystem-level fallback instructions, first check the skills exposed in the current Codex session and use the harness-discovered `productivity-skills:maintain-project-repo` workflow when it is available. If the companion skill is not exposed, tell the user to add the [`socket`](https://github.com/gaelic-ghost/socket) marketplace with `codex plugin marketplace add gaelic-ghost/socket`, then install the relevant plugins from Codex's plugin directory so future sessions expose both `apple-dev-skills` and `productivity-skills`.

## When To Use

- Use this skill when an existing macOS, iOS, or iPadOS app repo needs `AGENTS.md` added, refreshed, or merged with the current Xcode workflow baseline.
- Use this skill when the repository already has an `.xcodeproj` or `.xcworkspace` and the user wants project guidance, onboarding rules, or workflow policy brought up to date.
- Use this skill when the user wants the repo guidance for the current narrower Xcode execution skills to be made explicit in the repo itself.
- Do not use this skill for new-project creation from nothing.
- Do not use this skill for ordinary build, test, run, diagnostics, docs lookup, or mutation work inside an existing Xcode project.
- Do not use this skill for plain Swift packages, libraries, or tools that are not native Apple apps.
- Recommend `bootstrap-xcode-app-project` when the repo does not exist yet.
- Recommend `xcode-build-run-workflow` when the task is active Xcode execution, diagnostics, docs lookup, previews, file-membership follow-through, or mutation work inside an existing Xcode project.
- Recommend `xcode-testing-workflow` when the task is primarily about Swift Testing, XCTest, XCUITest, `.xctestplan`, or test diagnosis inside an existing Xcode project.
- Recommend `sync-swift-package-guidance` when the repo is a plain Swift package instead of an Xcode app project.
- After updating this plugin's Xcode-policy surfaces, recommend rerunning `sync-xcode-project-guidance` in downstream repos so their `AGENTS.md` and `maintain-project-repo` output stay aligned.
- For maintainer notes about this repository itself, say plainly that the repo exports from top-level `skills/` today and does not ship repo-local installer workflows.

## Single-Path Workflow

1. Collect the required inputs:
   - `repo_root`
   - optional `workspace_path`
   - optional `skip_validation`
   - optional `dry_run`
2. Classify the request as existing Xcode app-repo guidance sync before continuing:
   - continue only when the repo already contains an `.xcodeproj` or `.xcworkspace`
   - stop if the request is really new-project bootstrap or SwiftPM-only guidance sync
3. Apply the Apple docs gate before shaping workflow guidance:
   - read the relevant Apple documentation first
   - use Xcode MCP `DocumentationSearch` first for Apple-owned SDK, framework, lifecycle, and Xcode project behavior
   - use the Dash.app MCP second when its installed docsets cover the question; use Dash HTTP only when that MCP is unavailable or incomplete
   - use checked-out source, generated DocC, GitHub/source repositories, release notes, and readable online documentation only after those local MCP paths; generic no-JS web search/open results, snippets, metadata shells, or bare URLs are not enough
   - state the documented workflow boundary being relied on before proposing repo guidance changes
   - current documented anchors for this workflow include:
     - Apple's Xcode project-creation guidance: [Creating an Xcode project for an app](https://developer.apple.com/documentation/xcode/creating_an_xcode_project_for_an_app)
     - SwiftUI app lifecycle guidance through the `App` protocol: [App](https://developer.apple.com/documentation/swiftui/app)
     - scene composition guidance through `Scene` and `WindowGroup`: [Scene](https://developer.apple.com/documentation/swiftui/scene) and [WindowGroup](https://developer.apple.com/documentation/swiftui/windowgroup)
   - if the docs and the current guidance template conflict, stop and report that conflict
   - if no relevant Apple docs can be found, say that explicitly before proceeding
4. Apply the shared Xcode-project policy before making repo-guidance changes:
   - apply the detailed local policy in `references/snippets/apple-xcode-project-core.md`
   - preserve its simplicity-first Swift, SwiftUI, Xcode-managed project, XcodeGen-backed project, test-plan, file-membership, tracked `.pbxproj` commit, and Debug/Release guidance
   - require one default `Localizable.xcstrings` String Catalog per app target; use `Sources/Resources/Localizable.xcstrings` for the standard XcodeGen layout and record another target-owned location explicitly when a project has a justified different resource root
5. Run `scripts/run_workflow.py` to normalize inputs, detect whether the repo is really Xcode-managed, shape the sync plan, and report strict Xcode app structure drift:
   - missing `Sources/Views/Shared`, `Sources/Views/macOS`, `Sources/Views/iOS`, or `Sources/Models`
   - legacy `Sources/Controllers`
   - legacy external SwiftUI ViewModel files
   - project-owned Swift files missing the selected three-letter prefix
   - any project-owned `+` filename
   - umbrella app-service containers and forwarding service layers when actual source evidence shows them
   - a missing default String Catalog; report the exact catalog path and hand target membership or XcodeGen regeneration to `xcode-build-run-workflow` instead of hand-editing `.pbxproj`
6. Apply the sync path:
   - if `AGENTS.md` is missing, copy `assets/AGENTS.md`
   - if `AGENTS.md` exists and already contains the managed section, keep the file unchanged
   - if `AGENTS.md` exists but lacks the managed section, append `assets/append-section.md` as a bounded section
7. Validate the synced repo guidance:
   - verify `AGENTS.md` exists
   - verify the synced file mentions `xcode-build-run-workflow` and `xcode-testing-workflow`
   - verify the synced file preserves the no-direct-`.pbxproj` rule and the tracked `.pbxproj` stage-and-commit rule
   - verify the synced file preserves the XcodeGen source-of-truth rule for repos that use generated projects
   - verify the sync audit records whether the default String Catalog exists; a guidance sync does not claim a file is in an Xcode target until project-aware Xcode or XcodeGen evidence confirms membership
8. Refresh `maintain-project-repo`:
   - refresh `Scripts/repo-maintenance/`
   - refresh `.github/workflows/validate-repo-maintenance.yml`
   - preserve repo-specific extra scripts that are not part of the managed file set
9. Verify the synced maintenance guidance still points at the expected maintainer files:
   - `.swiftformat`
   - `Scripts/repo-maintenance/hooks/pre-commit.sample`
   - `Scripts/repo-maintenance/validate-all.sh`
   - `Scripts/repo-maintenance/sync-shared.sh`
   - `Scripts/repo-maintenance/release.sh`
   - protected branches, when configured, require the GitHub Actions check context `validate` rather than `Validate Repo Maintenance / validate`
   - when a GitHub remote exists, route repository settings audit or mutation
     through `productivity-skills:maintain-github-repository`
10. Hand off ongoing engineering work cleanly:
   - recommend `xcode-build-run-workflow` or `xcode-testing-workflow` for active Xcode collaboration after the repo guidance is aligned
   - recommend `bootstrap-xcode-app-project` only when the user actually needs a fresh repo instead of guidance sync

## Inputs

- `repo_root`: optional absolute or relative path to the repository root; defaults to `.`
- `workspace_path`: optional path used only to improve Xcode-project discovery when repo-root detection is ambiguous
- `skip_validation`: optional flag to skip post-sync file validation
- `dry_run`: optional flag to emit the planned contract without writing files
- Defaults:
  - runtime entrypoint: executable `scripts/run_workflow.py`
  - `repo_root=.` when omitted
  - `writeMode=sync-if-needed`
  - validation runs unless `--skip-validation` is passed
  - successful mutating runs install `.codex/environments/xcode-project.toml` from `templates/codex-local-environments/xcode-project.toml` when missing, replace `SCHEME_NAME` with the workspace or project stem, leave matching files unchanged, and preserve customized existing files
  - successful mutating runs refresh `maintain-project-repo` output in place

## Outputs

- `status`
  - `success`: guidance sync completed or was already satisfied
  - `blocked`: prerequisites, repo classification, or sync policy prevented completion
  - `failed`: the sync path started but did not complete successfully
- `path_type`
  - `primary`: the documented sync path completed
  - `fallback`: a non-mutating guided result was returned
- `output`
  - resolved repo root
  - detected workspace or project markers
  - `AGENTS.md` path
  - actions applied or planned
  - installed or preserved `.codex/environments/xcode-project.toml`
  - refreshed `maintain-project-repo` paths
  - validation result
  - strict app-structure audit result and findings
  - default String Catalog audit result and required project-aware follow-up
  - one concise next step or handoff

## Guards and Stop Conditions

- Stop with `blocked` if the repo root cannot be resolved.
- Stop with `blocked` if the repo does not contain an `.xcodeproj` or `.xcworkspace`.
- Stop with `blocked` if the repo appears to be a SwiftPM-only package without Xcode-managed app markers.
- Stop with `blocked` if the chosen `writeMode` does not allow the mutation the repo still needs, such as creating a missing `AGENTS.md` or appending the bounded Xcode guidance section.
- Stop with `blocked` if the target `AGENTS.md` path exists but is not a regular file.
- Fail with a clear message if the Codex local environment template is missing or the target `.codex/environments/xcode-project.toml` path exists but is not a regular file.

## Fallbacks and Handoffs

- The only current fallback is a non-mutating dry-run or guided result that explains what the sync would do.
- After a successful sync, hand off ongoing build, run, diagnostics, preview, and mutation work to `xcode-build-run-workflow`.
- After a successful sync, hand off ongoing test execution and test diagnosis work to `xcode-testing-workflow`.
- After a successful sync that reports a missing catalog, hand off to `xcode-build-run-workflow` to add `Localizable.xcstrings` through Xcode or the owning XcodeGen spec, confirm target membership, and build to populate it.
- After a successful sync, use `Scripts/repo-maintenance/validate-all.sh` for local maintainer validation and `Scripts/repo-maintenance/release.sh --mode standard --version vX.Y.Z` from a feature branch or worktree for protected-main releases.
- After a successful sync, configure protected branches to require `validate` for the managed repo-maintenance workflow; GitHub exposes that job check context directly rather than the workflow title plus job string.
- When a GitHub remote exists, use `productivity-skills:maintain-github-repository`
  to audit repository features, merge modes, security automation, sign-off
  policy, and branch protection without changing visibility implicitly.
- Recommend `bootstrap-xcode-app-project` when the repository still needs to be created from scratch.
- Recommend `sync-swift-package-guidance` when the repo is a plain Swift package rather than an Xcode app project.

## Codex Subagent Fit

When the user explicitly asks for subagents, `swift-steward`, review-packet planning, or asks to keep working while broad Xcode repo-maintenance discovery happens in parallel, use the `swift-steward` custom-agent role for read-heavy discovery before this skill applies guidance sync.

Good `swift-steward` jobs for this skill:

- classify the project shape and flag ambiguous SwiftPM/Xcode boundaries
- inspect `AGENTS.md`, README, CONTRIBUTING, ROADMAP, Xcode project/workspace markers, `.swiftformat`, `.swiftlint.yml`, and `Scripts/repo-maintenance/`
- compare current repo guidance against this skill's current Xcode baseline
- return a review packet with proposed patch set, validation handoff, affected files, and blockers

Keep apply-mode edits in the main thread. The steward may return proposed patch-set entries, but the main agent should review them with the user before saving, editing, or applying any edits.

## Customization

- Use `references/customization-flow.md`.
- `scripts/customization_config.py` stores and reports customization state.
- `scripts/run_workflow.py` loads runtime-safe defaults from customization state before invoking the supported sync path.
- The current runtime-enforced customization surface is one `writeMode` knob that controls whether the workflow may create missing `AGENTS.md`, append the bounded Xcode section, or stay report-only.
- Run the Python wrapper and customization entrypoints through `uv`, because they rely on inline `PyYAML` script metadata rather than a repo-global Python environment.
- In consuming repos, the supported path is `uv run scripts/run_workflow.py ...` and `uv run scripts/customization_config.py ...`; do not assume plain `python` or `python3` will have the needed YAML dependency installed.

## References

### Workflow References

- `references/project-detection.md`

### Contract References

- `references/automation-prompts.md`
- `references/customization-flow.md`

### Support References

- `assets/AGENTS.md`
- `assets/append-section.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when an existing Xcode repo needs the reusable baseline policy content in a human-reviewable form.
- `references/snippets/apple-xcode-project-core.md`
- `templates/codex-local-environments/xcode-project.toml`

### Script Inventory

- `scripts/run_workflow.py`
- `scripts/sync_xcode_project_guidance.py`
- `scripts/customization_config.py`
