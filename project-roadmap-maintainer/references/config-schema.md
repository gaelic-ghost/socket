# Configuration Schema

Persistent customization for this skill is defined in:

- Template defaults: `config/customization.template.yaml`
- User overrides: `config/customization.yaml`

Checklist roadmap mode is canonical. Legacy table-era keys remain for backward compatibility.

## Top-level fields

- `schemaVersion`: integer schema version (`1`).
- `isCustomized`: `true` when user overrides exist in `config/customization.yaml`.
- `profile`: short profile label (`default`, `team-delivery`, `quarterly`, etc).
- `settings`: roadmap behavior controls.

## `settings` fields

### Active in checklist mode

- `statusValues`: ordered list of allowed status values used for normalization and legacy mapping.
- `planHistoryVerbosity`: one of `concise`, `standard`, `detailed`.
- `changeLogVerbosity`: one of `concise`, `standard`, `detailed`.

### Deprecated (compatibility-only)

These keys are retained for schema compatibility and legacy migrations, but are non-authoritative for checklist-standard output:

- `milestoneIdStyle`: one of `M`, `phase`, `quarter`.
- `targetStyle`: one of `semver`, `quarter`, `date`.
- `includeOwnerField`: legacy table-column behavior.
- `includeDependencyField`: legacy table-column behavior.
- `enableSubMilestones`: legacy sub-milestone model toggle.
- `subMilestoneIdStyle`: one of `hierarchical`, `letter`, `ticket`, `external`.
- `subMilestonePrefix`: legacy ticket-style prefix.
- `subMilestonePadWidth`: legacy ticket-style zero-padding width.
- `subMilestoneDelimiter`: one of `.` or `-`.
- `allowExternalTrackerIds`: legacy external ID behavior.
- `subMilestoneStatusValues`: legacy child-status vocabulary.

Runtime treatment for deprecated keys:

- `ignored` for normal checklist updates.
- `legacy-only` as hints during table-style migration.
- never used to force table/sub-milestone output in checklist-standard mode.

## Compatibility behavior

- Existing `config/customization.yaml` files remain valid at `schemaVersion: 1`.
- Missing keys continue to inherit template defaults.
- No automatic schema migration or rewrite is required.

## Example user config (checklist-standard, recommended)

```yaml
schemaVersion: 1
isCustomized: true
profile: checklist-default
settings:
  statusValues:
    - Planned
    - In Progress
    - Completed
    - Blocked
    - De-scoped
  planHistoryVerbosity: standard
  changeLogVerbosity: concise
```

## Example user config (legacy-compatible, still accepted)

```yaml
schemaVersion: 1
isCustomized: true
profile: legacy-compatible
settings:
  milestoneIdStyle: M
  targetStyle: semver
  statusValues:
    - Planned
    - In Progress
    - Blocked
    - Completed
  includeOwnerField: false
  includeDependencyField: false
  enableSubMilestones: false
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
