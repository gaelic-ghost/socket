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
- `enableSubMilestones`: enable conditional sub-milestone tracking rules when `true`.
- `subMilestoneIdStyle`: one of `hierarchical`, `letter`, `ticket`, `external`.
- `subMilestonePrefix`: string prefix used for `ticket` style IDs (`T` -> `T-01`).
- `subMilestonePadWidth`: integer zero-padding width for `ticket` style numbering.
- `subMilestoneDelimiter`: one of `.` or `-`; joins generated parts for `hierarchical` and `ticket` styles.
- `allowExternalTrackerIds`: allows non-local IDs (`PROJ-123`) when `subMilestoneIdStyle` is `external`.
- `subMilestoneStatusValues`: ordered list of allowed status values for sub-milestones. If omitted in user config, mirror `statusValues`.
- `planHistoryVerbosity`: one of `concise`, `standard`, `detailed`.
- `changeLogVerbosity`: one of `concise`, `standard`, `detailed`.

## Compatibility behavior

- Existing `config/customization.yaml` files remain valid when new sub-milestone keys are absent.
- Missing sub-milestone keys are interpreted with template defaults.
- No automatic migration or rewrite is required.

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
  enableSubMilestones: true
  subMilestoneIdStyle: hierarchical
  subMilestonePrefix: T
  subMilestonePadWidth: 2
  subMilestoneDelimiter: "."
  allowExternalTrackerIds: false
  subMilestoneStatusValues:
    - Planned
    - In Progress
    - Blocked
    - Completed
  planHistoryVerbosity: standard
  changeLogVerbosity: detailed
```

## Alternative example: ticket style IDs

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
  enableSubMilestones: true
  subMilestoneIdStyle: ticket
  subMilestonePrefix: T
  subMilestonePadWidth: 2
  subMilestoneDelimiter: "-"
  allowExternalTrackerIds: false
  subMilestoneStatusValues:
    - Planned
    - In Progress
    - Blocked
    - Completed
  planHistoryVerbosity: standard
  changeLogVerbosity: detailed
```
