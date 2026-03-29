# Roadmap Customization Guide

## Checklist Standard

`mode=roadmap_maintenance` treats checklist-style `ROADMAP.md` as canonical:

- `Vision`
- `Product principles`
- `Milestone Progress`
- Per-milestone sections with `Scope`, `Tickets`, and `Exit criteria`

Legacy table-style roadmap formats are auto-migrated in-place when encountered in apply mode.

## Active Customization Knobs

- `statusValues`
  - Used for status vocabulary mapping, especially during legacy migration and textual status normalization.
- `planHistoryVerbosity`
  - Controls detail level when preserving or summarizing historical plan context.
- `changeLogVerbosity`
  - Controls detail level when preserving or summarizing historical change context.

## Deprecated Knobs (Compatibility-Only)

The settings below remain available for backward compatibility but are non-authoritative in checklist mode:

- `milestoneIdStyle`
- `targetStyle`
- `includeOwnerField`
- `includeDependencyField`
- `enableSubMilestones` and related sub-milestone keys

Behavior policy:

- Do not fail when deprecated keys exist.
- Treat deprecated keys as legacy-migration hints only.
- Prefer checklist section consistency over recreating legacy table/sub-milestone structures.

## Validation Checklist

- `ROADMAP.md` uses checklist-standard sections.
- `Milestone Progress` exists and reflects milestone reality.
- Every milestone has `Tickets` and `Exit criteria` checklists.
- `[P]` markers are used only for genuinely parallelizable ticket items.
- Legacy table sections are migrated or preserved only in non-conflicting historical form.
