# Socket Release Workflow

Socket has one branch-backed release lifecycle: `prepare` → `inspect` →
`advance`. The managed repository-skills runtime owns every stage, and all
operator entrypoints are root Just recipes backed by FSX.

## Authority And Ownership

- Prepare from a named, clean feature branch with reviewed release notes at
  `docs/releases/vX.Y.Z.md`.
- Keep a separate clean worktree on `main` for post-merge verification,
  tagging, publication, and safe cleanup.
- Never commit a release bump directly on `main`.
- Account for every unmerged branch before cleanup. Release authorization does
  not authorize deleting unaccounted history.

## Prepare

```bash
just repo-release-prepare 10.0.0
```

Prepare verifies the branch and worktree, requires checked-in release notes,
runs canonical validation, applies the deterministic version bump, commits and
pushes it, verifies the remote commit, and creates or reuses the release pull
request. If GitHub is not ready, it emits a bounded continuation packet.

## Inspect

```bash
just repo-release-inspect 10.0.0
```

Inspect performs one bounded read of the pull request, required checks,
reviews, comments, and commit identity. Do not poll. If state is pending, use
one matching continuation no sooner than five minutes later and inspect again
before mutation.

## Advance

```bash
just repo-release-advance 10.0.0
```

Classify any unmerged branch explicitly when required:

```bash
just repo-release-advance 10.0.0 \
  --branch-accounting feature/example=in-progress
```

Allowed classifications are `preserved`, `in-progress`, `archived`, `merged`,
and `safe-to-delete`. Advance verifies the reviewed commit, enables GitHub
auto-merge, fast-forwards the clean `main` worktree, reruns canonical
validation and the root E2E test, creates the annotated tag and GitHub release,
and performs the final marketplace refresh.

## Child Synchronization

- Monorepo-owned plugins need no separate child push.
- `plugins/apple-dev-skills` is canonical in Socket; its standalone repository
  remains a compatibility pointer.
- `speak-swiftly` is an external Git-backed catalog entry and normally needs no
  Socket source synchronization.
- A future subtree target must define its ownership gate before release.

## Completion

A release is complete only after the reviewed `main` commit, remote annotated
tag, GitHub release, branch accounting, child synchronization accounting, and
final marketplace refresh are verified. Remove only merged release branches
and worktrees after that evidence exists.
