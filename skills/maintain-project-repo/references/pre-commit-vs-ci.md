# Pre-Commit vs CI

Use the maintainer toolkit with a local-first split:

- `scripts/repo-maintenance/validate-all.sh`
  - the full local validation command
  - the same command CI should call
- `.github/workflows/validate-repo-maintenance.yml`
  - a thin wrapper that calls the local script
  - keep workflow logic minimal
- `scripts/repo-maintenance/hooks/pre-commit.sample`
  - an opt-in sample for cheap local checks
  - do not turn it into the only validation surface

Keep expensive or repo-shaping logic in the repo-owned scripts, not in GitHub workflow YAML.
