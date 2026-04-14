# Contributing to socket

Use this guide when preparing root-level changes so the `socket` superproject stays understandable, runnable, and reviewable for the next maintainer.

## Table of Contents

- [Overview](#overview)
- [Contribution Workflow](#contribution-workflow)
- [Local Setup](#local-setup)
- [Development Expectations](#development-expectations)
- [Pull Request Expectations](#pull-request-expectations)
- [Communication](#communication)
- [License and Contribution Terms](#license-and-contribution-terms)

## Overview

### Who This Guide Is For

This guide is for contributors working on the `socket` superproject layer itself: the root marketplace, root maintainer docs, root validation scripts, and root coordination rules for the child repositories under [`plugins/`](./plugins/).

### Before You Start

Before starting work:

- read the root [README.md](./README.md) and [AGENTS.md](./AGENTS.md)
- confirm whether the task belongs in the root superproject or in a specific child repository
- if the work affects subtree-managed children, use the documented subtree workflow instead of improvising a mixed root-and-child change
- if the change affects root docs, marketplace wiring, or maintainer automation, plan to update the relevant root docs in the same pass

## Contribution Workflow

### Choosing Work

Use the root repository for work about:

- repo-root marketplace wiring in [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
- root maintainer docs under [`docs/`](./docs/)
- root policies in [README.md](./README.md), [AGENTS.md](./AGENTS.md), and [ROADMAP.md](./ROADMAP.md)
- root validation and CI such as [`scripts/validate_socket_metadata.py`](./scripts/validate_socket_metadata.py) and [`.github/workflows/validate-socket-metadata.yml`](./.github/workflows/validate-socket-metadata.yml)

If the change is really about one child repository's own skills, packaging, tests, or release flow, start in that child repository's docs and workflow instead of treating `socket` as a generic catch-all.

### Making Changes

Keep changes bounded to one coherent root concern at a time. Common safe shapes are:

- docs-only root alignment
- marketplace-path or manifest-alignment fixes
- root validation improvements
- root subtree-workflow documentation updates

For ordinary work in monorepo-owned child directories, edit the copy in `plugins/<repo>/` directly from this checkout. For `apple-dev-skills` and `python-skills`, keep subtree pull and push operations explicit and separate from unrelated edits.

### Asking For Review

A root change is ready for review when:

- the change clearly belongs at the superproject layer
- any affected root docs and automation surfaces were updated together
- verification relevant to the changed root surface has been run
- the PR or review request explains whether the change affects root docs, marketplace wiring, subtree workflow, or validation behavior

## Local Setup

### Runtime Config

The root superproject uses a small `uv` environment for maintainer tooling:

```bash
uv sync --dev
```

The root validation path does not require application secrets. If your change involves subtree sync or GitHub operations, make sure your git remotes and GitHub authentication are already configured on your machine before you start those steps.

### Runtime Behavior

`socket` does not run a root application or service. A healthy root setup means:

- the `uv` dev environment is synced
- the root marketplace file is valid JSON
- the root packaged plugin paths still point at real installable plugin surfaces
- the root validator completes successfully

You can verify that baseline with:

```bash
uv run scripts/validate_socket_metadata.py
```

## Development Expectations

### Naming Conventions

Keep root terminology aligned with the repository docs:

- `skill` means a reusable workflow-authoring unit
- `plugin` means an installable distribution bundle
- `subagent` means a delegated runtime worker with its own context and tool policy

Use the same names for the same concepts across `SKILL.md`, plugin manifests, marketplace metadata, docs, automation prompts, scripts, and validation messages.

### Accessibility Expectations

Contributors must keep root-level changes aligned with the project's accessibility contract in [ACCESSIBILITY.md](./ACCESSIBILITY.md).

If a change affects root docs, structural navigation, command readability, log clarity, workflow operability, or other root maintainer-facing surfaces, verify the affected surface against the documented accessibility expectations before asking for review.

If a root-level change introduces a new accessibility limitation, exception, or remediation path, update [ACCESSIBILITY.md](./ACCESSIBILITY.md) in the same pass unless maintainers have explicitly agreed on a different tracking path.

### Verification

Prefer grounded validation commands that match the changed root surface.

Root baseline validation:

```bash
uv sync --dev
uv run scripts/validate_socket_metadata.py
```

When editing docs, also review the rendered Markdown structure and cross-links for the files you changed.

## Pull Request Expectations

A good root PR should make the changed superproject surface obvious. Include:

- what root concern changed
- why the change belongs in `socket` instead of a child repo
- any root docs updated to keep the policy surface aligned
- the verification you ran

If a PR touches subtree-managed children, call that out explicitly so reviewers know whether they are looking at ordinary monorepo edits or subtree workflow changes.

## Communication

Surface uncertainty early when a change starts to look architectural, cross-repo, or hard to keep bounded. In particular, pause and ask for alignment if the work would:

- change the root marketplace model
- widen the superproject's ownership boundary
- add a new root abstraction or coordination layer
- blur the line between root policy and child-repo behavior

When docs and scripts disagree, fix the script or narrow the documented contract so the two surfaces match.

## License and Contribution Terms

Unless a contribution explicitly says otherwise in writing, contributions to `socket` are made under the Apache License 2.0 terms in [LICENSE](./LICENSE). The root legal-notice surface for this superproject lives in [NOTICE](./NOTICE).
