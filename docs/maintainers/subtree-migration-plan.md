# Subtree Migration Plan

This document is the working plan for moving Gale's adjacent plugin and skills repositories under `~/Workspace/gaelic-ghost/socket/` as subtree-managed directories.

Status note: this plan is now mostly historical. `socket` has already completed the simplification step that keeps `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer` as subtrees while treating the other child directories as ordinary monorepo-owned nested directories.

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
│   ├── SpeakSwiftlyServer/
│   ├── python-skills/
│   ├── things-app/
│   └── ...
└── README.md
```

## Phase Model

### Phase 0: scaffold

- initialize the `socket` superproject
- add maintainer docs and the repo-root marketplace placeholder
- classify candidate imports by Git readiness

Status:

- completed
- scaffold commit: `3bbf8f0` `Scaffold socket superproject`

### Phase 1: import existing Git repos as subtrees

Immediate subtree candidates:

- `agent-plugin-skills`
- `apple-dev-skills`
- `productivity-skills`
- `python-skills`
- `SpeakSwiftlyServer`
- `speak-to-user-skills`
- `things-app`
- `dotnet-skills` once bootstrapped as a real Git repo
- `rust-skills` once bootstrapped as a real Git repo
- `web-dev-skills`

Directories blocked from subtree import until they become real Git repos or are intentionally excluded:

- `dotnet-skills`
- `rust-skills`
- `private-skills`

Status:

- started
- imported so far:
  - `agent-plugin-skills`
  - `apple-dev-skills`
  - `dotnet-skills`
  - `productivity-skills`
  - `python-skills`
  - `SpeakSwiftlyServer`
  - `rust-skills`
  - `speak-to-user-skills`
  - `web-dev-skills`
  - `things-app`
- initial subtree commits:
  - `c884399` `agent-plugin-skills`
  - `38b095f` `apple-dev-skills`
  - `5eabafe` `dotnet-skills`
  - `57698b8` `productivity-skills`
  - `516f256` `python-skills`
  - `adbc78b` `SpeakSwiftlyServer`
  - `fd77a92` `rust-skills`
  - `6f63d61` `speak-to-user-skills` remake
  - `f8cb4bd` `web-dev-skills`
  - `06ce077` `things-app`

### Phase 2: wire the repo-root marketplace

- add one marketplace entry per imported non-private child plugin surface
- point marketplace entries at the actual installable child surface under `./plugins/`, even when that surface is a nested packaged plugin root or a root `skills/` directory the child repo intentionally exposes through thin marketplace metadata
- keep private child repos out of the public superproject marketplace catalog

Current state:

- `agent-plugin-skills`, `apple-dev-skills`, `dotnet-skills`, `productivity-skills`, `rust-skills`, `things-app`, `web-dev-skills`, and `SpeakSwiftlyServer` ship top-level `.codex-plugin/plugin.json` roots, so their socket marketplace entries point directly at the child-repo root directories
- `python-skills` ships its packaged plugin root inside `./plugins/python-skills/plugins/python-skills`, so the socket marketplace points there instead of the subtree root
- `private-skills` remains intentionally excluded from this public superproject and from the root marketplace

### Phase 3: validate Codex behavior

- launch Codex from inside imported subtree directories
- verify whether the `socket` repo root is treated as the effective project root for the marketplace experiment
- record whether the single-root model behaves acceptably in practice

### Phase 4: decide long-term direction

Possible outcomes:

1. keep subtree sync model
2. promote some or all subtree-managed directories into a plain monorepo
3. abandon the experiment and revert to personal-scope plugin installs plus narrower repo-local strategies

Outcome reached:

- `apple-dev-skills` remains subtree-managed
- `python-skills` remains subtree-managed
- `SpeakSwiftlyServer` is now subtree-managed
- the other child directories under `plugins/` are now monorepo-owned nested directories
- `speak-to-user-skills` has already been retired from the working tree and from the root marketplace
- their child remotes are no longer part of the intended steady-state model

## Import Rules

- subtree imports go under `plugins/<repo-name>`
- preserve the imported repo name in the directory path unless there is a strong collision reason not to
- do not hand-copy files from source repos into the superproject
- use subtree history-preserving imports instead of ad hoc file moves
- commit each import in a small, named step

## Open Questions

- which imported repos actually ship Codex plugin packaging versus only skills or app code
- whether `things-app` should live beside the skills/plugin repos under `plugins/` or under a second top-level grouping later
- whether the eventual plain monorepo path should preserve `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer` subtree history or eventually stop syncing those last child remotes too

## First Implementation Pass

The first implementation pass should do only this:

1. scaffold the superproject
2. verify candidate repos
3. import one low-risk subtree first
4. add the initial marketplace entry only after an imported directory proves it ships a plugin root

Do not bulk-import everything in one pass.

## Implementation Notes

- the first subtree import proved the Git shape works for the superproject
- the later simplification step proved most child repos did not need to stay real and syncable as separate public remotes
- plugin packaging remains a separate track from subtree import
- the marketplace now lists every non-private child plugin surface the superproject intentionally exposes and should continue excluding private repos
