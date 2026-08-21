# Repo Maintenance Layout

The installer owns one fixed runtime under `scripts/repo-maintenance/`:

```text
maintain-project-docs.fsx
repo-maintenance.fsx
repo-maintenance.just
managed-assets.json
config/profile.json
docs/
validations/*.fsx
syncing/*.fsx
version-bump.fsx (optional repo-owned release hook)
```

The root `justfile` imports `repo-maintenance.just`. Operators use `just`; the
runtime discovers root-owned `.fsx` hooks lexically. Managed files refresh in
place, while files outside the manifest remain repo-owned.

The only documentation recipes are `docs-check` and `docs-apply`. Both process
all four documents. Do not add Python, shell, per-document recipes, nested
tests, configuration schemas, or duplicate workflow implementations.
