# Repo Maintenance Toolkit Automation Prompts

- Install `maintain-project-repo` into `<repo_root>` and keep the GitHub workflow wrapper enabled.
- Refresh `maintain-project-repo` in `<repo_root>` without deleting repo-specific custom scripts.
- Report what `maintain-project-repo` would install into `<repo_root>` without mutating files.
- Explain when to use `scripts/repo-maintenance/validate-all.sh`, `scripts/repo-maintenance/sync-shared.sh`, and `scripts/repo-maintenance/release.sh`.
- Explain that standard release mode runs from a feature branch or worktree, opens a PR against protected `main`, watches CI, gates on PR comments, merges, fast-forwards local `main`, creates and pushes the tag from that reviewed `main`, creates the GitHub release, and cleans up merged branches.
- Explain that standard release mode may use `--remote-ci-mode defer` after full local validation for repositories with intentionally heavy GitHub CI, and that Codex should use a native thread Timer/Wakeup or heartbeat automation when available instead of leaving a shell process open just to poll remote checks.
- Explain that protected branches should require the GitHub Actions check context `validate` for the managed repo-maintenance workflow.
