# Roadmap Customization Guide

## Canonical Base Contract

`maintain-project-roadmap` treats checklist-style `ROADMAP.md` as canonical.

The default shared roadmap structure is defined in:

- `config/roadmap-customization.template.yaml`
- `assets/ROADMAP.template.md`

That base contract requires:

- a top-level `# ...` title
- `## Table of Contents`
- `## Vision`
- `## Product Principles`
- `## Milestone Progress`
- one or more milestone sections named `## Milestone N: Name`
- `## Backlog Candidates`
- `## History`

Each milestone must include:

- `### Status`
- `### Scope`
- `### Tickets`
- `### Exit Criteria`

Interpretation guidance:

- `Vision` is for the long-term outcome, not a project description.
- `Product Principles` is for roadmap decision rules, not general product philosophy.
- `Milestone Progress` is a status rollup, not a second checklist surface.
- `Status` is one allowed value only.
- `Scope` defines the milestone boundary and intended outcome, not the implementation task inventory.
- `Tickets` is the actionable checklist surface.
- `Exit Criteria` defines what must be true for completion.
- `Backlog Candidates` is for uncommitted future work.
- `History` is for notable roadmap changes, not every minor edit.

## Customization Model

Downstream plugins may customize roadmap structure through `config/roadmap-customization.yaml`.

The intended customization surface is structural and explicit:

- required top-level sections
- top-level section order
- required milestone subsections
- heading aliases for migration
- section and milestone-subsection scaffolding
- whether additional non-canonical sections are preserved

## Legacy Migration

Legacy roadmap layouts such as `Current Milestone` sections or milestone tables are not canonical output modes.

Runtime policy:

- in `check-only`, report legacy format as a migration finding
- in `apply`, migrate legacy layout into checklist-roadmap structure
- preserve useful milestone identity where possible
- use canonical template scaffolding when legacy content is incomplete
