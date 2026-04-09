# Subtree Migration Plan

This document is the working plan for moving Gale's adjacent plugin and skills repositories under `~/Workspace/gaelic-ghost/socket/` as subtree-managed directories.

## Why This Change Exists

This is a durable building-block change.

It is intended to remove two active pains:

- relying on a noisy personal plugin catalog for repos that do not all need the same plugins
- relying on submodules, which would reintroduce nested Git roots and likely undercut the single-root Codex marketplace experiment

The simpler path considered first was "keep personal-scope installs and manually enable or disable plugins per repo." That was rejected as the default because it creates too much manual state management and does not test the shared repo-root marketplace idea.

## Working Decision

Use a single Git superproject with `git subtree` imports, not submodules.

Rationale:

- subtree keeps one Git root, which is the main behavior this experiment needs for Codex repo-scoped marketplace discovery
- subtree is easier to collapse into a plain monorepo later than submodules
- subtree still preserves a path to sync with the original repositories while the experiment remains hybrid

## Target Layout

```text
~/Workspace/gaelic-ghost/socket/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── docs/
│   └── maintainers/
│       └── subtree-migration-plan.md
├── plugins/
│   ├── agent-plugin-skills/
│   ├── apple-dev-skills/
│   ├── productivity-skills/
│   ├── python-skills/
│   ├── private-skills/
│   ├── things-app/
│   └── ...
└── README.md
```

## Phase Model

### Phase 0: scaffold

- initialize the `socket` superproject
- add maintainer docs and the repo-root marketplace placeholder
- classify candidate imports by Git readiness

### Phase 1: import existing Git repos as subtrees

Immediate subtree candidates:

- `agent-plugin-skills`
- `apple-dev-skills`
- `private-skills`
- `productivity-skills`
- `python-skills`
- `things-app`

Candidates that need verification before import:

- `web-dev-skills`
  - appears to be a Git repo but did not show an `origin` remote in the initial audit

Directories blocked from subtree import until they become real Git repos or are intentionally excluded:

- `dotnet-skills`
- `rust-skills`
- `speak-to-user-skills`

### Phase 2: wire the repo-root marketplace

- add one marketplace entry per imported plugin repo that actually ships a `.codex-plugin/plugin.json`
- keep marketplace entries pointed at subtree directories under `./plugins/`
- do not list non-plugin repositories in the marketplace catalog

### Phase 3: validate Codex behavior

- launch Codex from inside imported subtree directories
- verify whether the `socket` repo root is treated as the effective project root for the marketplace experiment
- record whether the single-root model behaves acceptably in practice

### Phase 4: decide long-term direction

Possible outcomes:

1. keep subtree sync model
2. promote some or all subtree-managed directories into a plain monorepo
3. abandon the experiment and revert to personal-scope plugin installs plus narrower repo-local strategies

## Import Rules

- subtree imports go under `plugins/<repo-name>`
- preserve the imported repo name in the directory path unless there is a strong collision reason not to
- do not hand-copy files from source repos into the superproject
- use subtree history-preserving imports instead of ad hoc file moves
- commit each import in a small, named step

## Open Questions

- which imported repos actually ship Codex plugin packaging versus only skills or app code
- whether `web-dev-skills` should be normalized as a real remote-backed Git repo before import
- whether `things-app` should live beside the skills/plugin repos under `plugins/` or under a second top-level grouping later
- whether the eventual plain monorepo path should preserve subtree history or eventually stop syncing to child remotes

## First Implementation Pass

The first implementation pass should do only this:

1. scaffold the superproject
2. verify candidate repos
3. import one low-risk subtree first
4. add the initial marketplace entry only after an imported directory proves it ships a plugin root

Do not bulk-import everything in one pass.
