# Gale Git Baseline

Gale-managed development machines normally provide these global Git defaults:

```text
fetch.prune = true
pull.ff = only
branch.autoSetupRebase = always
```

They mean that ordinary fetches remove stale remote-tracking refs, ordinary
pulls refuse to create merge commits, and newly created tracking branches use
rebase when pulled. They are machine policy, not repository content.

## Workflow Contract

1. Before relying on the baseline, inspect effective values and their origins:

   ```bash
   git config --show-origin --get-regexp '^(fetch\.prune|pull\.ff|branch\.autoSetupRebase)$'
   ```

2. Treat a repository-local, worktree-local, command-line, or environment
   override as an explicit repository policy. Report it before an operation
   would behave differently from this baseline; do not silently remove it.
3. Keep explicit safety commands when their behavior must be invariant. For
   example, a protected-main release may use `git pull --ff-only` even when the
   global default already has that value.
4. Do not write these preferences with `git config --local` in bootstrap,
   sync, or repository-maintenance templates. A generated repository must work
   for contributors whose machine policy differs.

## Scope

This contract guides everyday Git work, worktree planning, repository
maintenance, and Git-initializing bootstrap workflows. It does not change a
repository's merge strategy, branch protection, remote permissions, or release
authority.
