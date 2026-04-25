# Repo Maintenance Toolkit Automation Prompts

- Install `maintain-project-repo` into `<repo_root>` and keep the GitHub workflow wrapper enabled.
- Refresh `maintain-project-repo` in `<repo_root>` without deleting repo-specific custom scripts.
- Report what `maintain-project-repo` would install into `<repo_root>` without mutating files.
- Explain when to use `scripts/repo-maintenance/validate-all.sh`, `scripts/repo-maintenance/sync-shared.sh`, and `scripts/repo-maintenance/release.sh`.
- Explain that protected branches should require the GitHub Actions check context `validate` for the managed repo-maintenance workflow.
