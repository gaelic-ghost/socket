# Monorepo Workflow

This document explains how `socket` is maintained after the monorepo simplification that left `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer` as the remaining subtree-managed child repositories.

## What Socket Owns

`socket` owns the monorepo layer:

- the nested directory layout under `plugins/`
- the root Codex marketplace at `.agents/plugins/marketplace.json`
- the maintainer docs that explain the mixed monorepo experiment
- release tags and release notes for the superproject itself

Treat Gale's local `socket` checkout as the normal day-to-day working checkout on `main`.

Direct work on local `main` is the default for `socket`. Use a feature branch or a dedicated worktree only when a change needs extra isolation for safety, review, or overlapping parallel work.

`socket` is the source of truth for every child directory under `plugins/` except `plugins/apple-dev-skills/`, `plugins/python-skills/`, and `plugins/SpeakSwiftlyServer/`.

For ordinary child-directory fixes, work in the monorepo copy under `plugins/<name>/` and commit in `socket`.

For `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer`, when a change should publish back to their source repositories, work in `plugins/<repo-name>/`, commit in `socket`, and then use `git subtree push --prefix=plugins/<repo-name> <remote> <branch>`.

## Child Repository Shape

Each nested directory under `plugins/` keeps its own internal layout, docs, and packaging choices.

That means there is one important packaging rule to expect:

1. A child repo exposes plugin packaging from the actual subtree root it treats as installable.
   Examples: `plugins/agent-plugin-skills/.codex-plugin/plugin.json` and `plugins/python-skills/.codex-plugin/plugin.json`

The socket root marketplace must point at the actual packaged plugin root, not at an assumed one.

## Current Named Remotes

The superproject keeps `origin` for `socket` and child-repository remotes for `apple-dev-skills`, `python-skills`, and `speak-swiftly-server`.

Current child-repo remotes:

- `apple-dev-skills`
- `python-skills`
- `speak-swiftly-server`

If a new subtree-managed child repository is introduced later, add its matching named remote first.

## Subtree Work For Apple Dev Skills, Python Skills, And SpeakSwiftlyServer

Use dedicated commits for `apple-dev-skills`, `python-skills`, and `SpeakSwiftlyServer` subtree work.

Typical pull flow:

```bash
git fetch apple-dev-skills
git subtree pull --prefix=plugins/apple-dev-skills apple-dev-skills main

git fetch python-skills
git subtree pull --prefix=plugins/python-skills python-skills main

git fetch speak-swiftly-server
git subtree pull --prefix=plugins/SpeakSwiftlyServer speak-swiftly-server main
```

Typical push flow:

```bash
git subtree push --prefix=plugins/apple-dev-skills apple-dev-skills main
git subtree push --prefix=plugins/python-skills python-skills main
git subtree push --prefix=plugins/SpeakSwiftlyServer speak-swiftly-server main
```

After subtree work:

- verify the directory shape under `plugins/apple-dev-skills/`, `plugins/python-skills/`, or `plugins/SpeakSwiftlyServer/`
- update socket docs and marketplace wiring in a separate focused commit when needed
- if the subtree work is part of a coordinated release-prep pass, keep the child repo version metadata and child docs aligned before pushing the subtree back out

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
- re-check `README.md`
- re-check `ROADMAP.md`
- remove stale duplicated packaging if the import introduced a second surviving copy of an already present child plugin

## Root Marketplace Rules

The root marketplace lives at `.agents/plugins/marketplace.json`.

Use these rules:

- list every non-private imported child plugin surface by default
- keep private child repos out of the public marketplace, and remove their entries if their directories are retired from the monorepo
- point `source.path` at the actual child surface the imported repo treats as installable
- do not change a marketplace path just because a child repo rearranged files internally; if the packaged plugin root is unchanged, keep the same `source.path`
- do not invent a second socket-level plugin wrapper when the child repo already has one
- do not leave stale marketplace entries behind after a packaging move or subtree removal
- keep one surviving plugin identity for each real child plugin

Recent example: `things-app` moved its bundled MCP server from `mcp/things-app-mcp/` to top-level `mcp/` inside the child repo, but the root marketplace entry stayed `./plugins/things-app` because the installable plugin root did not move.

## Release Flow

For socket releases:

1. make the intended superproject commits first
2. keep the working tree clean
3. push `main` to `origin`
4. create the release tag locally
5. push the tag
6. create the GitHub release from the existing tag

Use `vx.x.x` tags for socket releases.

## Common Failure Modes

- The socket marketplace still points at a directory that no longer exists in `plugins/`.
- A child directory vendors another plugin repo internally, leaving two plugin payloads with the same plugin name inside the monorepo.
- `apple-dev-skills`, `python-skills`, or `SpeakSwiftlyServer` still expects subtree sync, but its named remote is missing or points nowhere useful.
- Socket docs still describe the old all-subtree model after the monorepo has already moved on.
- `apple-dev-skills`, `python-skills`, or `SpeakSwiftlyServer` subtree work lands without a follow-up pass over root marketplace wiring and docs.

## Practical Rule Of Thumb

If the question is “how does this child directory work?”, read the child docs.

If the question is “how does socket expose, sync, or release these child directories together?”, read and update the socket maintainer docs.
