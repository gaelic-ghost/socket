# Configuration Schema

Persistent customization for this skill is defined in:

- Template defaults: `config/customization.template.yaml`
- User overrides: `config/customization.yaml`

## Top-level fields

- `schemaVersion`: integer schema version (`1`).
- `isCustomized`: `true` when user overrides exist in `config/customization.yaml`.
- `profile`: short profile label (`default`, `strict-hygiene`, etc).
- `settings`: scanner behavior controls.

## `settings` fields

- `workspaceRoot`: directory scanned for repositories.
- `minMb`: minimum size threshold for findings.
- `staleDays`: age threshold for stale-artifact score bonus.
- `maxFindings`: report cap.
- `severityCutoffs`:
  - `medium`
  - `high`
  - `critical`
- `dirRuleOverrides`: map of directory name to `{ category, weight }`.
- `fileExtRuleOverrides`: map of file extension to `{ category, weight }`.

## Example user config

```yaml
schemaVersion: 1
isCustomized: true
profile: low-noise-monorepo
settings:
  workspaceRoot: ~/Workspace
  minMb: 150
  staleDays: 120
  maxFindings: 120
  severityCutoffs:
    medium: 50
    high: 75
    critical: 90
  dirRuleOverrides:
    node_modules:
      category: dependency_artifact
      weight: 10
  fileExtRuleOverrides:
    ".zip":
      category: archive
      weight: 8
```
