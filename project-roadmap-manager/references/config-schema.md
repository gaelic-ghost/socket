# Configuration Schema

Persistent customization for this skill is defined in:

- Template defaults: `config/customization.template.yaml`
- User overrides: `config/customization.yaml`

## Top-level fields

- `schemaVersion`: integer schema version (`1`).
- `isCustomized`: `true` when user overrides exist in `config/customization.yaml`.
- `profile`: short profile label (`default`, `team-delivery`, `quarterly`, etc).
- `settings`: roadmap behavior controls.

## `settings` fields

- `milestoneIdStyle`: one of `M`, `phase`, `quarter`.
- `targetStyle`: one of `semver`, `quarter`, `date`.
- `statusValues`: ordered list of allowed status values.
- `includeOwnerField`: include `Owner` in generated roadmap structures when `true`.
- `includeDependencyField`: include dependency tracking fields when `true`.
- `planHistoryVerbosity`: one of `concise`, `standard`, `detailed`.
- `changeLogVerbosity`: one of `concise`, `standard`, `detailed`.

## Example user config

```yaml
schemaVersion: 1
isCustomized: true
profile: team-delivery
settings:
  milestoneIdStyle: phase
  targetStyle: semver
  statusValues:
    - Planned
    - In Progress
    - Blocked
    - Completed
  includeOwnerField: true
  includeDependencyField: true
  planHistoryVerbosity: standard
  changeLogVerbosity: detailed
```
