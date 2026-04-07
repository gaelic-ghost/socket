# Customization Consolidation Review

Date: 2026-04-04

## Purpose

Record the Milestone 20 audit of the current customization system, decide whether to keep or shrink it, and define the follow-up plan before any MCP App or other UI work is built on top of it.

## Current State Summary

- The active skill surface ships `8` separate `references/customization.template.yaml` files.
- The active skill surface ships `8` separate `scripts/customization_config.py` entrypoints.
- Those `customization_config.py` files are functionally identical and exist only because installed skills are expected to keep runtime resources inside the skill directory.
- The current templates expose `13` knobs total:
  - `12` are documented as `runtime-enforced`
  - `1` is documented as `policy-only`
- The current surface mixes together four different categories that should not all be presented as the same kind of user customization:
  - durable user preference
  - inference candidate
  - maintainer tuning
  - safety or invariants that should not be softened through ordinary customization

## Original Audit Baseline

Milestone 20 audited a larger surface before the implementation pass landed.

- The original Milestone 20 audit counted `35` knobs total:
  - `30` documented as `runtime-enforced`
  - `5` documented as `policy-only`
- Milestone 27 applied the approved reduction so the live surface now reflects the smaller counts in the current-state summary above.

## Decision

Milestone 20 concludes that the repo should shrink the customization surface rather than expand it.

The decision is:

1. Keep the current per-skill file locations and CLI shape for now.
   - `references/customization.template.yaml`
   - `scripts/customization_config.py`
   - commands `path`, `effective`, `apply`, and `reset`
2. Do not centralize the runtime helper into a shared imported module at repo root.
   - Installed skills are meant to keep runtime resources inside the skill directory.
   - A shared runtime import would make the shipped skill depend on repository structure outside the skill.
3. Treat the duplicated helper plumbing as an authoring and maintenance problem, not as a user-facing architecture problem.
   - If the duplication is still worth reducing after the surface shrinks, use maintainer-time generation or sync into local per-skill copies.
4. Move toward an inference-first model for defaults that can be derived from the request, repo shape, tool availability, or current environment.
5. Remove safety invariants and low-value maintainer tuning from the ordinary user-facing customization surface.

## Knob Classification

### Implemented User-Meaningful Customization

- `bootstrap-swift-package`
  - `defaultVersionProfile`
  - `defaultTestingMode`
  - `initializeGit`
  - `copyAgentsMd`
- `bootstrap-xcode-app-project`
  - `defaultPlatform`
  - `defaultOrgIdentifier`
  - `copyAgentsMd`
- `explore-apple-swift-docs`
  - `defaultSourceOrder`
- `format-swift-sources`
  - `defaultToolSelection`
- `sync-xcode-project-guidance`
  - `writeMode`
- `sync-swift-package-guidance`
  - `writeMode`
These are the knobs most likely to reflect real user preference instead of hidden implementation detail.

### Implemented As Inference, Fixed Workflow Defaults, Or Explicit Invocation Inputs

- `bootstrap-swift-package`
  - `defaultPackageType`
  - `defaultPlatformPreset`
- `bootstrap-xcode-app-project`
  - `defaultProjectGenerator`
- `explore-apple-swift-docs`
  - `troubleshootingPreference`
- `format-swift-sources`
  - `defaultSurface`
  - `preferSwiftLintPlugins`
  - `preferSwiftFormatHostAppExport`
- `swift-package-workflow`
  - no ordinary user-facing knobs

These are now better derived from request wording, available tools, repo shape, explicit CLI input, or fixed workflow defaults than held as broad durable user state.

### Removed From Ordinary User Customization

- `bootstrap-xcode-app-project`
  - `defaultProjectKind`
  - `defaultUIStack`
  - `validationMode`
- `explore-apple-swift-docs`
  - `defaultMaxResults`
  - `defaultSearchSnippets`
  - `dashInstallSourcePriority`
  - `requireExplicitApprovalForDashInstallYes`
  - `dashGenerationPolicy`
- `format-swift-sources`
  - `preferProjectRootConfigFiles`
- `sync-xcode-project-guidance`
  - `validationMode`
- `sync-swift-package-guidance`
  - `validationMode`

These are either safety policy, implementation tuning, or maintainer defaults that should not be presented as if they were equally meaningful end-user preference.

### Reintroduced Runtime Tuning Where It Changes Real Behavior

- `xcode-app-project-workflow`
  - `mcpRetryCount`
  - `fallbackCommandMappingProfile`

These remain because they now change actual runtime behavior without weakening the workflow's hard `.pbxproj` safety boundary.

## Sync Skill Simplification Decision

The two guidance-sync skills currently expose:

- `copyAgentsTemplateWhenMissing`
- `appendSectionWhenAgentsExists`
- `validationMode`

This should collapse into one smaller write model:

- implemented replacement: `writeMode`
- target values:
  - `sync-if-needed`
  - `create-missing-only`
  - `append-existing-only`
  - `report-only`

`validationMode` should stop being ordinary user-facing customization and become a maintainer or implementation detail unless a real user need appears.

## Shared Helper Decision

The duplicated `customization_config.py` scripts should not be consolidated into a shared runtime import.

Reason:

- the repository guidance says skill runtime resources should stay inside the skill directory
- installed skills should not depend on repo-root Python modules that are not shipped as part of the skill
- the current duplication is noisy, but it is operationally safe

If the repo still wants less duplication after the surface shrinks, the approved direction is:

- keep one canonical maintainer source template
- generate or sync local per-skill `customization_config.py` copies during maintainer work
- keep the installed skill self-contained

## Post-Extraction Note

The shared `repo-maintenance-toolkit` skill was later extracted into `../productivity-skills` because it is globally useful rather than Apple-specific.

- `apple-dev-skills` no longer counts that skill in its active customization surface
- this repo still vendors the managed toolkit snapshot under `shared/repo-maintenance-toolkit/` so the Apple bootstrap and guidance-sync skills can stay independently usable

## Follow-Up Plan

### Phase 1: Surface Reduction

Status: complete

- shrink each customization template to the user-meaningful knobs listed above
- reclassify or remove maintainer-only and invariant knobs
- update `references/customization-flow.md` files so their `Status` labels match the reduced model

### Phase 2: Inference Pass

Status: complete for the current approved scope

- teach the relevant workflow docs and runtime wrappers to infer the approved inference-first defaults
- keep escape hatches only where inference is likely to be wrong often enough to matter

### Phase 3: Helper Plumbing Review

Status: deferred on purpose

- after the surface is smaller, re-evaluate whether duplicated `customization_config.py` maintenance is still painful
- if yes, add maintainer-time generation or sync while preserving local per-skill shipped copies

### Phase 4: UI Follow-On

Status: not started

- only after the smaller customization model is in place should the repo build MCP App or other UI surfaces on top of it

## Outcome

Milestone 20 is complete once the roadmap reflects this review and the repository treats this document as the source of truth for the next implementation pass.

Milestone 27 is complete once the live customization templates, flow docs, runtime wrappers, tests, and roadmap all match the reduced surface described here. That implementation pass is now in place, with the current Xcode workflow keeping only the retry-count and fallback-profile runtime knobs plus the hard `.pbxproj` warning boundary.
