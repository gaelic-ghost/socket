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

## `defaultInstallScope`

Accepted values:

- `personal`
- `global`
- `repo`
- `repo-local`

Normalization behavior:

- `personal` and `global` resolve to personal-scope Codex installs
- `repo` and `repo-local` resolve to repo-scoped Codex installs

## Example

```yaml
schemaVersion: 1
profile: personal-first
isCustomized: true
defaultInstallScope: personal
```
