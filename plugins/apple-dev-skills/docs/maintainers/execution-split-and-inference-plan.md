# Execution Split and Inference Plan

Date: 2026-04-08

## Purpose

Record the planned split of the current execution skills into narrower build-run and testing skills, define the guidance-preservation contract for that split, and establish the companion plan for a first-class Swift and Xcode-oriented `repo-maintenance-toolkit` profile owned by this shipped Apple plugin.

## Current Problem

The package side of the split is now underway, but the overall execution surface is still broader than it should be:

- `xcode-app-project-workflow`
- `swift-package-build-run-workflow`
- `swift-package-testing-workflow`
- `swift-package-workflow` as a compatibility surface

Those skills now contain good guidance, but they still force the agent to do too much of the routing work manually, especially on the Xcode side and in broad compatibility entry points:

- classify build versus run versus testing intent before the runtime wrapper can help
- decide when testing-specific guidance, package-resource guidance, Metal handoff guidance, or Debug-vs-Release guidance matters
- bounce between neighboring skills even when the repo shape and request wording already make the likely path obvious

The plugin-first install model reduces the old pressure to minimize skill count. That means the repo can favor narrower skill boundaries and stronger inference instead of preserving monolithic workflow skills for install simplicity.

## Target Skill Matrix

Planned execution skills:

- `xcode-build-run-workflow`
  - Xcode-aware build, run, launch, preview-adjacent execution, scheme and destination inference, configuration selection, artifact validation, and `.pbxproj` safety boundaries when execution work crosses project-integrity concerns.
- `xcode-testing-workflow`
  - Swift Testing, XCTest, XCUITest, `.xctestplan`, destinations, filters, retries, diagnostics, and testing-specific fallback behavior for Xcode-managed work.
- `swift-package-build-run-workflow`
  - SwiftPM-first build and run flows, target inference, manifest-adjacent execution, package resources, `Bundle.module`, Metal library distribution guidance, and Release-vs-Debug validation for package repos.
- `swift-package-testing-workflow`
  - Swift Testing-first package testing, XCTest holdouts, async testing guidance, package-level Xcode test-plan execution when needed, and testing-specific fallback behavior for package repos.

Skills that remain separate and keep their current high-level role:

- `explore-apple-swift-docs`
- `bootstrap-swift-package`
- `bootstrap-xcode-app-project`
- `sync-swift-package-guidance`
- `sync-xcode-project-guidance`
- `format-swift-sources`
- `structure-swift-sources`

## Guidance Preservation Contract

No guidance currently carried by `xcode-app-project-workflow` or `swift-package-workflow` should be dropped during the split.

Use [workflow-guidance-preservation-matrix.md](./workflow-guidance-preservation-matrix.md) as the concrete line-by-line mapping during implementation.

The split must preserve every active guidance area in one of these forms:

1. Retained directly inside the narrower replacement skill.
2. Moved into a shared reference that the narrower skills still require.
3. Promoted into the synced or bootstrapped `AGENTS.md` baseline when it is a durable repo policy rather than an execution-only concern.

### Current guidance that must survive

- Apple docs gate before implementation guidance.
- Simplicity-first Swift guidance.
- Structured concurrency guidance, including cancellation-aware async design and sendability boundaries.
- Swift Testing, XCTest, XCUITest, and `.xctestplan` guidance.
- Package resources, `Bundle.module`, `Resource.process(...)`, `Resource.copy(...)`, and `Resource.embedInCode(...)`.
- Metal library distribution guidance and the Xcode handoff when Apple-managed Metal toolchain behavior matters.
- Debug-vs-Release validation guidance, including tagged-release expectations.
- Xcode file-membership and target-membership verification after on-disk edits.
- `.pbxproj` warning boundary.
- Plugin-install and downstream-guidance-sync recommendations for this repo's own maintenance flow.

## AGENTS Expansion Strategy

The split is a good opportunity to move more durable policy into synced and bootstrapped `AGENTS.md` output rather than leaving it only in execution-skill prose.

Good candidates for stronger `AGENTS.md` presence:

- Swift Testing default preference and XCTest/XCUITest role boundaries.
- `.xctestplan` expectations when the repo uses test plans.
- Package-resource and `Bundle.module` expectations.
- Metal distribution and Xcode handoff guidance for packages.
- File-membership verification after script-driven on-disk edits in Xcode repos.
- Debug-vs-Release validation expectations and tagged-release behavior.
- Repo-maintenance sync expectations after substantial workflow or plugin updates.

Keep execution-only mechanics out of `AGENTS.md` when they are too tied to tool behavior or a transient runtime path.

## Repo-Maintenance Toolkit Direction

The repo should treat the bundled Apple-facing `repo-maintenance-toolkit` contract in this repository as the canonical shipped surface, with Swift- and Xcode-aware profiles, instead of treating an external repo as part of the end-user install story.

Planned profile shape:

- `generic`
- `swift-package`
- `xcode-app`
- optional later `swift-mixed-root`

The Apple repo should ship that toolkit contract directly and keep any external sharing or upstreaming as maintainer-only coordination.

Current Apple-side integration status:

- the vendored installer in this repo is now profile-aware
- Apple bootstrap and guidance-sync skills explicitly install the `swift-package` or `xcode-app` profile
- installed repos now get `scripts/repo-maintenance/config/profile.env` as a concrete profile marker
- the remaining local work is keeping the Apple-local shared source authoritative and the shipped plugin self-contained

## Implementation Plan

### Phase 1: Inference-first runtime improvements

- Teach the current execution wrappers to infer likely intent from request wording.
- Keep explicit override input available when inference would be risky.
- Return the inferred intent in the runtime payload so downstream skills and tests can assert it.

### Phase 2: Execution split

- Add the four narrower execution skills.
- Convert the current two execution skills into compatibility and migration surfaces for one release cycle.
- Update docs, tests, and install surfaces to point to the new skill matrix.

Current status:

- the Swift package side is landed
- the Xcode side is landed
- both original broad execution skills now act as compatibility-routing surfaces
- the remaining work is inference strengthening plus the toolkit follow-through

### Phase 3: Guidance redistribution

- Promote durable execution-adjacent policy into synced and bootstrapped `AGENTS.md` templates where appropriate.
- Keep volatile runtime behavior in skill-local references and wrappers.
- Re-audit the guidance-preservation contract after the split lands.

### Phase 4: Toolkit promotion

- Keep the Swift and Xcode-oriented `repo-maintenance-toolkit` profile support canonical in this repository's shared toolkit source.
- Keep any future upstream sharing strictly maintainer-side so the Apple plugin remains one-and-done for end users.

## First Implementation Slice

The first implementation slice did not wait for the full skill split.

It:

- added request-driven intent inference to the current `swift-package-workflow` and `xcode-app-project-workflow` runtime wrappers before the split
- documented the planned split and preservation contract
- updated roadmap and maintainer docs so the future work is tracked explicitly

That inference work survived the later split and directly reduced current agent ceremony.
