# Customization Guide

## What To Customize First

- Roadmap template sections and table columns in `SKILL.md`.
- Milestone naming style (`M1` vs `Phase 1` vs quarter-based labels).
- Optional sub-milestone model and ID style (`M2.1`, `M2a`, `M2-T01`, `PROJ-123`).
- Status vocabulary (`Planned`, `In Progress`, `Completed`, `Blocked`, `De-scoped`).
- Change log detail level and plan history verbosity.
- Target version/date conventions (semantic versions, quarters, or calendar dates).

## Personalization Points

- Template shape and required sections
  - Default: skill creates/maintains `ROADMAP.md` with `Current Milestone`, `Milestones`, `Plan History`, and `Change Log`.
  - Why customize: teams often need owners, risk tracking, dependencies, or OKR fields.
  - Where to change: `settings.includeOwnerField`, `settings.includeDependencyField`, and roadmap template rules in `SKILL.md`.
- Milestone IDs and naming
  - Default: `M1` style IDs and semantic version examples like `v0.1.0`.
  - Why customize: some teams track by quarter (`2026-Q1`) or phase (`Phase 1`).
  - Where to change: `settings.milestoneIdStyle`, `settings.targetStyle`.
- Sub-milestones
  - Default: disabled to preserve existing roadmap behavior.
  - Why customize: break milestones into smaller deliverables while preserving parent milestone ownership.
  - Where to change: `settings.enableSubMilestones` plus `settings.subMilestoneIdStyle`, `settings.subMilestonePrefix`, `settings.subMilestonePadWidth`, `settings.subMilestoneDelimiter`, `settings.allowExternalTrackerIds`, and optional `settings.subMilestoneStatusValues`.
  - Style guidance:
    - `hierarchical`: `M2.1`, `M2.2` (recommended default when enabled).
    - `letter`: `M2a`, `M2b`.
    - `ticket`: local ticket IDs such as `M2-T01`, `M2-T02`.
    - `external`: tracker-native IDs such as `PROJ-123`.
- Status model
  - Default: planned set includes `Completed`, `In Progress`, `Blocked`, `De-scoped`, `Planned`.
  - Why customize: organizations may enforce a simpler or stricter status workflow.
  - Where to change: `settings.statusValues`.
- Change tracking granularity
  - Default: every mutation gets a dated `Change Log` note and accepted plans are captured in `Plan History`.
  - Why customize: reduce noise for fast-moving projects or increase audit detail for regulated teams.
  - Where to change: `settings.planHistoryVerbosity`, `settings.changeLogVerbosity`.

## Common Customization Profiles

- Lightweight solo roadmap
  - Keep the default structure, shorten `Plan History` entries, and keep only one active + one next milestone.
- Team delivery roadmap
  - Add owner and dependency columns, require explicit acceptance criteria and risk notes.
- Team delivery with child tracking
  - Enable sub-milestones, use `hierarchical` or `ticket` IDs, and capture sub-milestone transitions in `Change Log`.
- Quarterly planning roadmap
  - Replace milestone IDs with quarter IDs and use quarter-based target dates.
- Compliance-heavy roadmap
  - Require dense `Change Log` entries including reason, owner, and rollout note.

## Example Prompts For Codex

- "Customize roadmap defaults for quarterly planning with `YYYY-Qn` milestones."
- "Enable owner/dependency fields and set change-log verbosity to detailed."
- "Enable sub-milestones with hierarchical IDs and keep sub-statuses aligned to milestone statuses."
- "Use ticket-style sub-milestone IDs (`M2-T01`) with two-digit zero padding."
- "Switch status model to `Planned`, `In Progress`, `Blocked`, `Done` and keep plan history concise."

## Validation Checklist

- Confirm active config file reflects your profile and `isCustomized: true`.
- Confirm milestone ID examples follow the configured style.
- Confirm sub-milestone IDs follow the selected style and delimiter when enabled.
- Confirm status values are applied consistently across sections.
- Confirm sub-milestone statuses follow `subMilestoneStatusValues` (or inherited `statusValues` when unspecified).
- Confirm verbosity settings affect plan history and change-log detail as intended.
