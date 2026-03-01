# Customization Guide

## What To Customize First

- Roadmap template sections and table columns in `SKILL.md`.
- Milestone naming style (`M1` vs `Phase 1` vs quarter-based labels).
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
- Quarterly planning roadmap
  - Replace milestone IDs with quarter IDs and use quarter-based target dates.
- Compliance-heavy roadmap
  - Require dense `Change Log` entries including reason, owner, and rollout note.

## Example Prompts For Codex

- "Customize roadmap defaults for quarterly planning with `YYYY-Qn` milestones."
- "Enable owner/dependency fields and set change-log verbosity to detailed."
- "Switch status model to `Planned`, `In Progress`, `Blocked`, `Done` and keep plan history concise."

## Validation Checklist

- Confirm active config file reflects your profile and `isCustomized: true`.
- Confirm milestone ID examples follow the configured style.
- Confirm status values are applied consistently across sections.
- Confirm verbosity settings affect plan history and change-log detail as intended.
