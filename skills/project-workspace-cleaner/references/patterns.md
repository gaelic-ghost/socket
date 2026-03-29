# Workspace Cleanup Patterns

## Directory Patterns

- Build outputs: `dist`, `build`, `.next`, `.nuxt`, `.turbo`, `target`, `out`
- Dependency footprints: `node_modules`, `.venv`, `venv`, `.gradle`, `.m2`
- Tool caches: `.cache`, `.parcel-cache`, `.ruff_cache`, `.mypy_cache`, `.pytest_cache`, `__pycache__`

## File Patterns

- Large transient/log/archive files: `.log`, `.tmp`, `.temp`, `.cache`, `.zip`, `.tar`, `.tgz`, `.gz`, `.bz2`, `.xz`

## Severity Guidance

Base size thresholds (higher wins):

- >= 5 GiB: critical
- >= 2 GiB: high/critical boundary
- >= 1 GiB: high
- >= 200 MiB: medium
- < 200 MiB: low unless category weight raises score

Additional score boosts:

- Dependency footprints: higher cleanup impact
- Build outputs: moderate impact
- Stale artifacts (older than stale-days): additional priority
