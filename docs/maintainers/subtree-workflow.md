# Monorepo Workflow

This document explains how `socket` is maintained after the monorepo simplification that left `apple-dev-skills` as the remaining subtree-managed child repository.

## What Socket Owns

`socket` owns the monorepo layer:

- the nested directory layout under `plugins/`
- the root Codex marketplace at `.agents/plugins/marketplace.json`
- the maintainer docs that explain the mixed monorepo experiment
- coordinated guidance passes that intentionally keep multiple child skill repositories aligned
- release tags and release notes for the superproject itself

Treat Gale's local `socket` checkout as the normal day-to-day working checkout on `main`.

Direct work on local `main` is the default for `socket`. Use a feature branch or a dedicated worktree only when a change needs extra isolation for safety, review, or overlapping parallel work.

`socket` is the source of truth for every child directory under `plugins/` except `plugins/apple-dev-skills/`.

For ordinary child-directory fixes, work in the monorepo copy under `plugins/<name>/` and commit in `socket`.

For coordinated guidance that spans multiple monorepo-owned child repositories, edit the relevant child directories directly and update the root docs only enough to explain the cross-child policy or discovery reason.

For `apple-dev-skills`, when a change should publish back to its source repository, work in `plugins/apple-dev-skills/`, commit in `socket`, and then use `git subtree push --prefix=plugins/apple-dev-skills apple-dev-skills main`.

For Speak Swiftly plugin payload work, use the standalone `SpeakSwiftlyServer` checkout. Socket users receive that payload through the Git-backed marketplace entry, so `socket` no longer imports the standalone source tree under `plugins/`.

## Child Repository Shape

Each nested directory under `plugins/` keeps its own internal layout, docs, and packaging choices.

That means there is one important packaging rule to expect:

1. A child repo exposes plugin packaging from the actual child-repo root it treats as installable.
   Examples: `plugins/agent-plugin-skills/.codex-plugin/plugin.json` and `plugins/python-skills/.codex-plugin/plugin.json`

The socket root marketplace must point at the actual packaged plugin root, not at an assumed one.

### Remote Catalog Entries

Most Socket marketplace entries point at local child directories under `./plugins/`, but a marketplace entry may intentionally point at a Git-backed plugin source when the canonical payload lives outside `socket`.

The Speak Swiftly catalog split uses this model. `SpeakSwiftlyServer` remains the canonical owner of the `speak-swiftly` plugin payload and keeps its standalone marketplace functional. The Socket marketplace exposes the same canonical plugin payload by Git-backed reference instead of installing from the local `plugins/SpeakSwiftlyServer` subtree mirror.

Use this shape when all of these are true:

1. The external repository is the real source of truth for the plugin manifest, skills, hooks, MCP config, and doctor scripts.
2. `socket` should list the plugin for catalog convenience, but should not own a second copied payload.
3. `socket` does not need to carry a local source mirror for the plugin to stay available from the Socket catalog.

When a remote catalog entry is added, update the root marketplace validator so it understands that entry type. Local entries should still verify their checked-in packaged plugin roots. Remote entries should verify the marketplace metadata shape and document which external repository owns plugin validation.

## Current Named Remotes

The superproject keeps `origin` for `socket` and a child-repository remote for `apple-dev-skills`.

Current child-repo remotes:

- `apple-dev-skills`

If a new subtree-managed child repository is introduced later, add its matching named remote first.

## Subtree Work For Apple Dev Skills

Use dedicated commits for `apple-dev-skills` subtree work.

Current subtree direction:

| Child | Prefix | Remote | Default direction |
| --- | --- | --- | --- |
| `apple-dev-skills` | `plugins/apple-dev-skills` | `apple-dev-skills` | pull and push |

Typical pull flow:

```bash
git fetch apple-dev-skills
git subtree pull --prefix=plugins/apple-dev-skills apple-dev-skills main
```

Typical push flow:

```bash
git subtree push --prefix=plugins/apple-dev-skills apple-dev-skills main
```

After subtree work:

- verify the directory shape under `plugins/apple-dev-skills/`
- update socket docs and marketplace wiring in a separate focused commit when needed
- if the subtree work is part of a coordinated release-prep pass, use [`release-modes.md`](./release-modes.md) and account for whether the child needs pull, push, or no subtree action

## Shared Version Workflow

The maintained version-bearing manifests across `socket` now stay on one shared semantic version. Use the root workflow to inspect or update those surfaces:

```bash
scripts/release.sh inventory
scripts/release.sh patch
scripts/release.sh minor
scripts/release.sh major
scripts/release.sh custom 1.2.3
```

That workflow updates the maintained `pyproject.toml` and `.codex-plugin/plugin.json` files, plus adjacent `uv.lock` package self-version entries when those lockfiles exist. It intentionally refuses `patch`, `minor`, or `major` bumps while the maintained surfaces are split across multiple versions; use `custom` once to align them first.

## Release Mode For Subtrees

Use `subtrees` mode from [`release-modes.md`](./release-modes.md) when a `socket` release also needs subtree accounting. That mode treats the umbrella repository like a standard protected-main release and adds the subtree gate before tagging:

- `apple-dev-skills`: pull or push as needed for the child state that the release owns
- all subtree sync decisions: record whether the child was pulled, pushed, intentionally deferred, or not touched

## Add A New Subtree-Managed Child Repository

Only do this when Gale explicitly wants to preserve an upstream repository as a separate sync target.

Typical flow:

```bash
git remote add <name> <source-url-or-path>
git fetch <name>
git subtree add --prefix=plugins/<name> <name> main
```

After the import:

- verify the imported directory shape under `plugins/<name>/`
- inspect whether the child repo ships `.codex-plugin/plugin.json`
- if it does, locate the real packaged plugin root before touching the socket marketplace
- re-check `.agents/plugins/marketplace.json`
- re-check the root `README.md`
- re-check `ROADMAP.md`
- remove stale duplicated packaging if the import introduced a second surviving copy of an already present child plugin

## Root Marketplace Rules

The root marketplace lives at `.agents/plugins/marketplace.json`.

Use these rules:

- list every non-private imported child plugin surface by default
- keep private child repos out of the public marketplace, and remove their entries if their directories are retired from the monorepo
- point local entries' `source.path` at the actual child surface the imported repo treats as installable
- use a Git-backed source when the actual plugin payload is canonical in another repository and `socket` is only exposing it through the Socket catalog
- do not change a marketplace path just because a child repo rearranged files internally; if the packaged plugin root is unchanged, keep the same `source.path`
- do not invent a second socket-level plugin wrapper when the child repo already has one
- do not leave stale marketplace entries behind after a packaging move or subtree removal
- keep one surviving plugin identity for each real child plugin

### Marketplace Audit Pass

Run this audit whenever a child plugin is added, removed, moved, renamed, converted from subtree-managed to monorepo-owned, or changes its packaged plugin root:

1. List every marketplace entry in `.agents/plugins/marketplace.json`.
2. For each local `source.path`, verify the directory exists under `plugins/` and exposes `.codex-plugin/plugin.json` at the packaged plugin root.
3. For each Git-backed entry, verify the source kind matches the plugin location: `url` for a repository-root plugin and `git-subdir` for a plugin in a repository subdirectory.
4. Compare the marketplace entries against the real child directories under `plugins/` and confirm every public child plugin that ships `.codex-plugin/plugin.json` is listed or intentionally exposed by Git-backed reference.
5. Open each changed child repo's `AGENTS.md`, plugin manifest, optional public README, or maintainer docs and confirm the child still treats the marketplace path as its installable plugin root.
6. Run `uv run scripts/validate_socket_metadata.py`.
7. Update `README.md`, this maintainer workflow, and `ROADMAP.md` when the audit finds a packaging-model change rather than only a metadata typo.

The audit is about the installable plugin roots that Codex can actually see. Do not rewrite marketplace paths to follow an invented uniform layout when the child repo still packages from a different root.

For the Speak Swiftly catalog split, the expected surviving plugin identity is `speak-swiftly`, displayed as `Speak Swiftly`. The doctor should treat duplicate enablement from both the Socket marketplace and the standalone SpeakSwiftlyServer marketplace as repairable configuration drift. Its repair path should prefer `speak-swiftly@socket`, then disable or remove the duplicate standalone enablement after explaining the intended change.

### Removing A Public Child Plugin

Use this checklist before removing a public child repository from `socket` or from the root marketplace:

1. Identify whether the child is monorepo-owned, subtree-managed with push-back, or pull-only.
2. Confirm the child history is preserved where it belongs before deleting the directory, marketplace entry, branch, worktree, remote branch, or archive ref.
3. Remove the child directory only when the source repo is no longer meant to be imported here, or when the child has been explicitly moved elsewhere.
4. Remove the marketplace entry in the same commit as the directory removal when the plugin is no longer installable from `socket`.
5. Update `README.md`, `ROADMAP.md`, and any maintainer docs that listed the child as active.
6. Run `uv run scripts/validate_socket_metadata.py`.
7. Account for local branches not contained by `main` before cleanup.

If the removed Socket entry points at `SpeakSwiftlyServer`, do not use this checklist as permission to delete or rewrite the standalone live-service repository. That repo's standalone release, validation, and live-refresh path stays outside ordinary `socket` cleanup.

## Release Flow

For full release sequencing, use [`release-modes.md`](./release-modes.md). In short, `standard` is the normal `socket` release mode and `subtrees` is the normal mode plus explicit subtree accounting.

For socket releases:

1. make the intended superproject commits first
2. keep the working tree clean
3. check CI and comments for any release PR before tagging
4. merge the reviewed release state to `main`
5. fast-forward local `main` from `origin/main`
6. create the release tag locally from `main`
7. push the tag
8. create the GitHub release from the existing tag
9. run `codex plugin marketplace upgrade socket`

Use `vx.x.x` tags for socket releases. When a release used `subtrees` mode, do not create the tag until every touched subtree-managed child has been pulled, pushed, deferred with a stated reason, or confirmed untouched.

## Common Failure Modes

- The socket marketplace still points at a directory that no longer exists in `plugins/`.
- A child directory vendors another plugin repo internally, leaving two plugin payloads with the same plugin name inside the monorepo.
- `apple-dev-skills` still expects subtree sync, but its named remote is missing or points nowhere useful.
- Socket docs still describe the old all-subtree model after the monorepo has already moved on.
- `apple-dev-skills` subtree work lands without a follow-up pass over root marketplace wiring and docs.
- Socket docs or marketplace entries reintroduce a local SpeakSwiftlyServer mirror even though Speak Swiftly is served from the standalone Git-backed repository.

## Practical Rule Of Thumb

If the question is “how does this child directory work?”, read the child docs.

If the question is “how does socket expose, sync, or release these child directories together?”, read and update the socket maintainer docs.
