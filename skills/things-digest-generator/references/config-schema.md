# Configuration Schema

Persistent customization for this skill is defined in:

- Template defaults: `config/customization.template.yaml`
- User overrides: `config/customization.yaml`

## Top-level fields

- `schemaVersion`: integer schema version (`1`).
- `isCustomized`: `true` when user overrides exist in `config/customization.yaml`.
- `profile`: short profile label (`default`, `weekly-planner`, etc).
- `settings`: digest generation controls.

## `settings` fields

- `dueSoonDays`: due-soon horizon in days.
- `daysAhead`: planning window length.
- `topProjects`: number of project entries in digest.
- `topAreas`: number of area entries in digest.
- `maxSuggestions`: cap for suggestion bullets.
- `openCountCap`: cap used in scoring formula.
- `outputStyle`: one of `operational`, `executive`.
- `scoringWeights`:
  - `completed7d`
  - `dueSoon`
  - `overdue`
  - `openCountWeight`
  - `checklistHints`

## Example user config

```yaml
schemaVersion: 1
isCustomized: true
profile: weekly-planner
settings:
  dueSoonDays: 5
  daysAhead: 7
  topProjects: 4
  topAreas: 3
  maxSuggestions: 6
  openCountCap: 12
  outputStyle: executive
  scoringWeights:
    completed7d: 4.0
    dueSoon: 2.0
    overdue: 2.5
    openCountWeight: 0.6
    checklistHints: 1.0
```
