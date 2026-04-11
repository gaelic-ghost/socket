# Roadmap Configuration Schema

Persistent roadmap customization for `maintain-project-roadmap` is defined in:

- Template defaults: `config/roadmap-customization.template.yaml`
- User overrides: `config/roadmap-customization.yaml`

Checklist roadmap mode is canonical.

## Top-level fields

- `schemaVersion`: integer schema version (`1`)
- `isCustomized`: `true` when user overrides exist in `config/roadmap-customization.yaml`
- `profile`: short profile label such as `base`, `team-delivery`, or `quarterly`
- `settings`: roadmap behavior and structure controls

## `settings` fields

- `preservePreamble`: whether to preserve preamble content beneath the title before the first H2
- `allowAdditionalSections`: whether non-canonical top-level sections are preserved after the canonical roadmap block
- `statusValues`: allowed milestone status values used for milestone `Status` subsections and milestone-progress rollups
- `requiredSections`: required non-milestone H2 sections
- `sectionOrder`: canonical roadmap order, including the milestone slot marker `__MILESTONES__`
- `requiredMilestoneSubsections`: required H3 subsections inside every milestone
- `sectionAliases`: top-level heading aliases migrated to canonical names during apply
- `milestoneSubsectionAliases`: milestone subsection aliases migrated to canonical names during apply
- `sectionTemplates`: default body scaffolding for required top-level sections
- `milestoneSubsectionTemplates`: default body scaffolding for required milestone subsections

Base interpretation notes:

- `Milestone Progress` should summarize milestone names plus statuses only.
- `Scope` should stay outcome- and boundary-oriented.
- `Tickets` should carry actionable checklist work.
- `History` should stay high-signal and record only notable roadmap changes.
