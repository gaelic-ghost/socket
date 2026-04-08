# Install Plugin To Socket Customization

Persistent customization for `install-plugin-to-socket` can live in either of these files:

- Repo profile: `.codex/profiles/install-plugin-to-socket/customization.yaml`
- Global profile: `~/.config/gaelic-ghost/agent-plugin-skills/install-plugin-to-socket/customization.yaml`

Resolution order:

1. `--scope` CLI flag
2. Explicit `--config <path>` override
3. Repo profile
4. Global profile
5. Built-in default: `personal`

If `--config` is provided explicitly and the file does not exist, the helper should fail instead of silently falling back.

## Supported fields

- `schemaVersion`: integer schema version, currently `1`
- `profile`: short human label for the customization profile
- `isCustomized`: optional boolean marker for maintainers
- `defaultInstallScope`: preferred default install target
- `repoInstallTracking`: preferred repo-scope tracking policy when `defaultInstallScope` resolves to repo scope or the maintainer passes `--scope repo`

## `defaultInstallScope`

Accepted values:

- `personal`
- `global`
- `repo`
- `repo-local`

Normalization behavior:

- `personal` and `global` resolve to personal-scope Codex installs
- `repo` and `repo-local` resolve to repo-scoped Codex installs

## `repoInstallTracking`

Accepted values:

- `tracked`
- `local-only`

Normalization behavior:

- `tracked` means repo-scoped staged plugin trees and marketplace changes are intentional shared repo state that may be committed and synced
- `local-only` means the same documented repo-scoped paths are used, but the resulting working-tree changes are local dev wiring unless the repo explicitly chooses to share them
- the built-in default is `local-only`

## Example

```yaml
schemaVersion: 1
profile: personal-first
isCustomized: true
defaultInstallScope: personal
repoInstallTracking: local-only
```
