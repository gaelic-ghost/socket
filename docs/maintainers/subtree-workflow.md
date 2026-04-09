# Subtree Workflow

This document explains how `socket` is maintained as a subtree-based superproject after the first migration pass.

## What Socket Owns

`socket` owns the superproject layer:

- the imported child repository layout under `plugins/`
- the root Codex marketplace at `.agents/plugins/marketplace.json`
- the maintainer docs that explain the monorepo experiment
- release tags and release notes for the superproject itself

`socket` does not replace the imported child repositories as their own source of truth.

## Child Repository Shape

Each imported child repository remains a real repository with its own internal layout, docs, and packaging choices.

That means there are two important patterns to expect:

1. A child repo may expose plugin packaging at the subtree root.
   Example: `plugins/agent-plugin-skills/.codex-plugin/plugin.json`
2. A child repo may keep plugin packaging inside its own nested `plugins/<plugin-name>/` directory.
   Example: `plugins/python-skills/plugins/python-skills/.codex-plugin/plugin.json`

The socket root marketplace must point at the actual packaged plugin root, not at an assumed one.

## Current Named Remotes

The superproject keeps one named git remote per imported child repository plus `origin` for the public socket repository.

Current child-repo remotes:

- `agent-plugin-skills`
- `apple-dev-skills`
- `dotnet-skills`
- `private-skills`
- `productivity-skills`
- `python-skills`
- `rust-skills`
- `speak-to-user-skills`
- `things-app`
- `web-dev-skills`

If a new child repository is imported later, add its matching named remote first.

The rebuilt minimal subtree source repos now also have public GitHub homes:

- [`gaelic-ghost/speak-to-user-skills`](https://github.com/gaelic-ghost/speak-to-user-skills)
- [`gaelic-ghost/web-dev-skills`](https://github.com/gaelic-ghost/web-dev-skills)

## Import A New Child Repository

Use a dedicated commit for each new subtree import.

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
- update socket docs and marketplace wiring in a separate focused commit when needed

## Sync An Existing Child Repository

Use a dedicated commit for each subtree sync.

Typical flow:

```bash
git fetch <name>
git subtree pull --prefix=plugins/<name> <name> main
```

After the sync:

- review whether the child repo moved or added plugin packaging
- re-check `.agents/plugins/marketplace.json`
- re-check `README.md`
- re-check `docs/maintainers/subtree-migration-plan.md`
- remove stale duplicated packaging if the sync introduced a second surviving copy of an already imported child plugin

## Root Marketplace Rules

The root marketplace lives at `.agents/plugins/marketplace.json`.

Use these rules:

- list only child repositories that already ship real Codex plugin packaging
- point `source.path` at the actual packaged plugin root
- do not invent a second socket-level plugin wrapper when the child repo already has one
- do not leave stale marketplace entries behind after a packaging move or subtree removal
- keep one surviving plugin identity for each real child plugin

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

- A child repo is imported correctly, but the socket marketplace still points at the subtree root even though the real plugin root is nested.
- A child repo vendors another plugin repo internally, leaving two plugin payloads with the same plugin name inside the monorepo.
- A child subtree exists in `socket`, but its matching named source remote is missing or points nowhere useful, which blocks future subtree pulls.
- Socket docs describe an earlier migration assumption after the imported child repo has already changed packaging shape.
- A subtree sync lands without a follow-up pass over root marketplace wiring and docs.

## Practical Rule Of Thumb

If the question is “how does this child repository work?”, read the child repo docs.

If the question is “how does socket expose, import, sync, or release these child repositories together?”, read and update the socket maintainer docs.
