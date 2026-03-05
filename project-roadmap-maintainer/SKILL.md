---
name: project-roadmap-maintainer
description: Create and maintain repository-root ROADMAP.md using a checklist-first canonical format. Use when bootstrapping a roadmap, accepting or completing plans, updating milestone scope/status, migrating legacy roadmap tables, or keeping milestone progress, tickets, and exit criteria synchronized.
---

# Project Roadmap Maintainer

Maintain `ROADMAP.md` in the project root as the canonical roadmap source of truth.

## Workflow

1. Load active customization config:
   - Prefer `config/customization.yaml`.
   - Fall back to `config/customization.template.yaml`.
2. Locate `<project_root>/ROADMAP.md`.
3. If missing, create `ROADMAP.md` using the checklist canonical format.
4. Detect existing format:
   - canonical checklist format, or
   - legacy `Current Milestone` / `Milestones` table format.
5. If legacy format is found, migrate in-place to checklist format.
6. Apply requested roadmap update while keeping section consistency.

## Canonical Format

Required top-level sections:

- `Vision`
- `Product principles`
- `Milestone Progress`
- Per-milestone sections with `Scope`, `Tickets`, and `Exit criteria`

Optional preserved sections:

- `Architectural decision log`
- `Risks and mitigations`
- `Backlog candidates`

## Checklist Rules

- Use markdown checkboxes only: `[ ]` and `[x]`.
- Use `[P]` marker only for parallelizable ticket items.
- Keep milestone numbering and names deterministic.
- Keep `Milestone Progress` aligned with milestone section status.
- Keep edits bounded to roadmap-relevant sections.

## Legacy Migration Rules

If legacy roadmap sections exist:

1. Build milestone sections from legacy rows/details.
2. Convert legacy status to checklist state in `Milestone Progress`.
3. Preserve useful historical text under compatible sections.
4. Remove superseded legacy sections after successful migration.
5. Do not leave duplicated conflicting state.

## Customization Workflow

When user requests customization:

1. Read `config/customization.yaml`; if missing, use `config/customization.template.yaml`.
2. Confirm behavior for:
   - `statusValues`
   - `planHistoryVerbosity`
   - `changeLogVerbosity`
3. Propose 2-4 option bundles with one recommended default.
4. Write `config/customization.yaml` with:
   - `schemaVersion: 1`
   - `isCustomized: true`
   - `profile: <selected-profile>`
5. Validate with a dry-run roadmap update and report behavior deltas.

## Automation Templates

Use `$project-roadmap-maintainer` in automation prompts.

- `references/automation-prompts.md`

## References

- `references/customization.md`
- `references/config-schema.md`
- `references/automation-prompts.md`
