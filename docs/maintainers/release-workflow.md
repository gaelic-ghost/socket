# Socket Release Workflow

Socket has one release lifecycle. Every patch, minor, major, catalog-refresh,
and child-affecting release travels through the same branch-backed
`prepare` → `inspect` → `advance` entrypoint.

## Authority And Ownership

- Run release preparation from a named feature worktree.
- Treat the separate clean `main` checkout as the post-merge verification,
  tagging, and publication surface.
- Never commit or push a version bump directly on `main`.
- Use `scripts/release.sh` as the only public release command. The Python files
  under `scripts/` are internal implementation modules.
- A release request authorizes the PR, merge, annotated tag, GitHub release,
  final marketplace refresh, and safe merged-branch/worktree cleanup after all
  gates pass. It does not authorize deleting unmerged or unaccounted history.

## Before Prepare

1. Finish and commit the intended implementation on its feature branch.
2. Add reviewed release notes at `docs/releases/vX.Y.Z.md`. State actual user
   changes, breaking changes, and migration steps. Do not claim that the tag,
   GitHub release, marketplace refresh, or cleanup already happened.
3. Run focused validation while implementing. `prepare` runs the consolidated
   full profile again after applying the version.
4. For child payload changes, determine whether the child is monorepo-owned,
   an external Git-backed catalog entry, or a genuine subtree sync target.
   Socket currently has no release-time subtree target.

Inspect the current shared version when needed:

```bash
scripts/release.sh inventory
```

## Prepare

Choose the exact next semantic version. For the current release:

```bash
scripts/release.sh prepare 10.0.0
```

`prepare`:

- refuses `main`, detached HEAD, or a dirty worktree;
- requires checked-in release notes;
- aligns every maintained manifest and adjacent lockfile to the requested
  version;
- runs `uv run scripts/validate_socket.py --profile full` against that version;
- commits the version as `release: prepare Socket vX.Y.Z`;
- pushes the feature branch and verifies its exact remote commit;
- opens the release PR or preserves the existing PR body and reviewer content; and
- prints one bounded PR snapshot plus a continuation packet when GitHub state
  is not ready.

## Inspect

Never watch or poll CI, reviews, or provider state. Inspect once:

```bash
scripts/release.sh inspect 10.0.0
```

If GitHub is still pending, reuse one matching host-native continuation no
sooner than five minutes later. On wakeup, run `inspect` again before any
mutation. Failed or pending checks, requested changes, and unreviewed comments
block the release. After reviewing and resolving comments, pass
`--review-comments-addressed` to `advance`; the flag does not bypass failed or
pending checks, requested changes, or commit-identity validation.

The required GitHub `validate` job runs the same full Socket profile used by
`prepare`; release PRs do not rely on a weaker compatibility-only check.

## Advance

Only after the PR snapshot is green and comments are resolved:

```bash
scripts/release.sh advance 10.0.0
```

If a local branch remains outside `main`, classify it explicitly rather than
using a blanket override:

```bash
scripts/release.sh advance 10.0.0 \
  --branch-accounting feature/example=in-progress
```

Allowed classifications are `preserved`, `in-progress`, `archived`, `merged`,
and `safe-to-delete`.

`advance` verifies the feature branch and PR commit identities, uses GitHub
auto-merge with the repository's merge method, finds the worktree that owns
`main`, fast-forwards it from the current remote, and proves local and remote
commit equality. It then:

1. verifies the shared version and release notes on reviewed `main`;
2. completes structured branch and child-sync accounting;
3. reruns the full validation profile on reviewed `main`;
4. captures commit-bound temporary-marketplace and Dependabot evidence;
5. creates and pushes an annotated `vX.Y.Z` tag at that exact commit;
6. creates and verifies the GitHub release using checked-in notes plus only
   pre-publication evidence;
7. reports the final branch accounting; and
8. runs `codex plugin marketplace upgrade socket` as the final release action.

The marketplace refresh retains the bounded fallback for the known Codex clone
timeout, but it cannot run before the tag and GitHub release are verified.

## Child Synchronization

Child synchronization is a conditional pre-tag gate inside this one workflow,
not a separate release mode.

- Monorepo-owned plugin directories require no separate child push.
- `plugins/apple-dev-skills` is canonical in Socket; the standalone repository
  is a compatibility pointer and must not receive a subtree push.
- `speak-swiftly` is an external Git-backed catalog entry; its standalone
  release normally requires no Socket source sync.
- If a real subtree target is deliberately introduced later, register its gate
  in the release implementation and document its pull/push ownership in
  `subtree-workflow.md` before releasing it.

## Completion And Cleanup

A release is complete only when the reviewed `main` commit, annotated remote
tag, GitHub release, branch accounting, child-sync accounting, and final local
marketplace refresh are all verified.

After that verification, prune stale remote refs and remove only merged release
branches and their worktrees. Preserve or explicitly classify every unmerged
branch before deleting any branch, worktree, archive ref, or rescue ref.
