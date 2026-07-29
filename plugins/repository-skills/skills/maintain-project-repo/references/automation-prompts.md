# Repo Maintenance Toolkit Automation Prompts

- Install `maintain-project-repo` into `<repo_root>` and keep the GitHub workflow wrapper enabled.
- Refresh `maintain-project-repo` in `<repo_root>` without deleting repo-specific custom scripts.
- Report what `maintain-project-repo` would install into `<repo_root>` without mutating files.
- Explain when to use `scripts/repo-maintenance/validate-all.sh`, `scripts/repo-maintenance/sync-shared.sh`, and `scripts/repo-maintenance/release.sh`.
- Explain that standard release mode runs from a feature branch or worktree, opens a PR against protected `main`, watches CI, gates on PR comments, merges, fast-forwards local `main`, creates and pushes the tag from that reviewed `main`, creates the GitHub release, accounts for every local branch not contained by `main`, and only then cleans up branches that are proven safe to delete.
- Explain that branch cleanup is gated by commit reachability: do not call work on `main`, merged, recovered, preserved, or safe to clean up until the exact local repository and remote prove it, and do not delete local branches, remote branches, worktrees, archive refs, or temporary rescue refs until any non-base history is merged or explicitly archived.
- Explain that standard release mode may use `--remote-ci-mode defer` after full local validation for repositories with intentionally heavy GitHub CI or slow review-bot status contexts, and that Codex should create a same-thread heartbeat automation when available instead of leaving a shell process open just to poll remote checks.
- Explain that pending review-bot contexts such as CodeRabbit are not a clean merge signal. Codex should wake, inspect the review and comments, address valid findings, and only merge after the review/comment gate is clear.
- Explain that protected branches should require the GitHub Actions check context `validate` for the managed repo-maintenance workflow.
