# Repo Maintenance Layout

The managed target layout is:

```text
scripts/
  repo-maintenance/
    validate-all.sh
    sync-shared.sh
    release.sh
    lib/
      common.sh
    validations/
      10-toolkit-layout.sh
      20-agents-guidance.sh
      30-ci-wrapper.sh
    syncing/
    release/
      10-preflight.sh
      20-tag-release.sh
      30-push-release.sh
      40-github-release.sh
    config/
      validation.env
      release.env
    hooks/
      pre-commit.sample
.github/
  workflows/
    validate-repo-maintenance.yml
```

## Design Rules

- Top-level scripts are stable entrypoints.
- Ordered `validations/*.sh`, `syncing/*.sh`, and `release/*.sh` are discovered automatically.
- Managed files are safe to refresh in place.
- Repo-specific extra scripts are allowed as long as they do not reuse the managed filenames.
