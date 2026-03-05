# Customization Guide

## Checklist Standard

This skill now treats checklist-style `ROADMAP.md` as canonical:

- `Vision`
- `Product principles`
- `Milestone Progress`
- Per-milestone sections with `Scope`, `Tickets`, and `Exit criteria`

Legacy table-style roadmap formats are auto-migrated in-place when encountered.

## Active Customization Knobs

These settings remain active in checklist mode:

- `statusValues`
  - Used for status vocabulary mapping, especially during legacy migration and textual status normalization.
- `planHistoryVerbosity`
  - Controls detail level when preserving or summarizing historical plan context.
- `changeLogVerbosity`
  - Controls detail level when preserving or summarizing historical change context.

## Deprecated Knobs (Compatibility-Only)

The settings below remain in schema/config for backward compatibility but are non-authoritative in checklist mode:

- `milestoneIdStyle` (legacy ID-format hint)
- `targetStyle` (legacy date/version hint)
- `includeOwnerField` (legacy table column behavior)
- `includeDependencyField` (legacy table column behavior)
- `enableSubMilestones` and related sub-milestone keys:
  - `subMilestoneIdStyle`
  - `subMilestonePrefix`
  - `subMilestonePadWidth`
  - `subMilestoneDelimiter`
  - `allowExternalTrackerIds`
  - `subMilestoneStatusValues`

Deprecated behavior policy:

- Do not fail when deprecated keys exist.
- Treat deprecated keys as legacy-migration hints only.
- Prefer checklist section consistency over recreating table/sub-milestone structures.

## Legacy Auto-Migration Behavior

When a roadmap contains `Current Milestone` and/or `Milestones` table sections:

1. Convert to checklist standard in-place.
2. Preserve useful legacy context without duplicated conflicting sections.
3. Keep milestone order deterministic.
4. Map status information into:
   - `Milestone Progress` checkbox states and notes.
   - Milestone-local checklist state where applicable.

## Example Prompts

- "Use `$project-roadmap-maintainer` to migrate this roadmap to checklist format and keep all useful history."
- "Use `$project-roadmap-maintainer` to add tickets to Milestone 2 and update exit criteria progress."
- "Use `$project-roadmap-maintainer` in check-only mode and report any missing milestone tickets/exit criteria."
- "Customize roadmap behavior to keep change logging concise while preserving checklist structure."

## Validation Checklist

- `ROADMAP.md` uses checklist-standard sections.
- `Milestone Progress` exists and reflects milestone reality.
- Every milestone has `Tickets` and `Exit criteria` checklists.
- `[P]` markers are used only for genuinely parallelizable ticket items.
- Legacy table sections are migrated or preserved only in non-conflicting historical form.
