docs-check:
    dotnet fsi scripts/repo-maintenance/maintain-project-docs.fsx --project-root . --run-mode check-only --format markdown --fail-on-issues

docs-apply:
    dotnet fsi scripts/repo-maintenance/maintain-project-docs.fsx --project-root . --run-mode apply --format markdown --fail-on-issues

repo-validate:
    dotnet fsi scripts/repo-maintenance/repo-maintenance.fsx validate

repo-sync:
    dotnet fsi scripts/repo-maintenance/repo-maintenance.fsx sync

repo-release-prepare version *args:
    dotnet fsi scripts/repo-maintenance/repo-maintenance.fsx release prepare --version {{ quote(version) }} {{ args }}

repo-release-inspect version:
    dotnet fsi scripts/repo-maintenance/repo-maintenance.fsx release inspect --version {{ quote(version) }}

repo-release-advance version *args:
    dotnet fsi scripts/repo-maintenance/repo-maintenance.fsx release advance --version {{ quote(version) }} {{ args }}
