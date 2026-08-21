set shell := ["zsh", "-cu"]

repo-report repo_root="." profile="generic":
    dotnet fsi plugins/repository-skills/skills/maintain-project-repo/scripts/maintain-project-repo.fsx --repo-root {{ quote(repo_root) }} --operation report-only --profile {{ quote(profile) }}

repo-install repo_root="." profile="generic":
    dotnet fsi plugins/repository-skills/skills/maintain-project-repo/scripts/maintain-project-repo.fsx --repo-root {{ quote(repo_root) }} --operation install --profile {{ quote(profile) }}

repo-refresh repo_root="." profile="generic":
    dotnet fsi plugins/repository-skills/skills/maintain-project-repo/scripts/maintain-project-repo.fsx --repo-root {{ quote(repo_root) }} --operation refresh --profile {{ quote(profile) }}

test:
    dotnet fsi tests/repository-maintenance-e2e.fsx

# BEGIN managed repo-maintenance
import 'scripts/repo-maintenance/repo-maintenance.just'
# END managed repo-maintenance

# BEGIN managed agent-plugins
import 'scripts/agent-plugins/agent-plugins.just'
# END managed agent-plugins
