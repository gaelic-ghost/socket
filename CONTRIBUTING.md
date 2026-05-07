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

Read the root [README.md](./README.md) and [AGENTS.md](./AGENTS.md), confirm whether the task belongs in the root superproject or in a specific child repository, and if the work affects subtree-managed children use the documented subtree workflow instead of improvising a mixed root-and-child change. If the change affects root docs, marketplace wiring, or maintainer automation, plan to update the relevant root docs in the same pass.

## Contribution Workflow

### Choosing Work

Use the root repository for work about:

- repo-root marketplace wiring in [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
- root maintainer docs under [`docs/`](./docs/)
- root policies in [README.md](./README.md), [AGENTS.md](./AGENTS.md), and [ROADMAP.md](./ROADMAP.md)
- root validation and CI such as [`scripts/validate_socket_metadata.py`](./scripts/validate_socket_metadata.py) and [`.github/workflows/validate-socket-metadata.yml`](./.github/workflows/validate-socket-metadata.yml)
- coordinated child-skill guidance that needs one consistent policy across multiple monorepo-owned plugin or skills repositories

If the change is really about one child repository's own skills, packaging, tests, or release flow, start in that child repository's docs and workflow instead of treating `socket` as a generic catch-all.

### Making Changes

Keep changes bounded to one coherent root concern at a time, such as docs-only root alignment, marketplace-path or manifest-alignment fixes, root validation improvements, or root subtree-workflow documentation updates. For ordinary work in monorepo-owned child directories, edit the copy in the relevant directory under `plugins/` directly from this checkout. For `apple-dev-skills`, keep subtree pull and push operations explicit and separate from unrelated edits. For Speak Swiftly plugin payload changes, work in the standalone `SpeakSwiftlyServer` checkout; `socket` lists that payload by Git-backed marketplace reference. Treat `plugins/SpeakSwiftlyServer` as a pull-only source mirror, and refresh it only when the superproject intentionally needs the standalone source state.

When changing user-facing plugin install or update docs, make the Git-backed marketplace path the default. Use commands shaped like `codex plugin marketplace add owner/repo` for install setup and `codex plugin marketplace upgrade marketplace-name` for updates; keep explicit refs such as `owner/repo@vX.Y.Z` scoped to pinned reproducible installs, and keep manual local marketplace roots scoped to development, unpublished testing, or fallback instructions.

For coordinated child-skill guidance, keep the root explanation small and put detailed behavior in the child repo that owns the skill surface. The root docs should explain why the pass is coordinated; the child docs should explain the actual skill contract.

When adding root screenshots or other documentation media, place them under [`docs/media/`](./docs/media/), use portable descriptive filenames, and add nearby text that explains what the artifact proves or demonstrates. Do not rely on image content alone to explain a workflow.

When updating root docs, keep [README.md](./README.md) short, nontechnical, and focused on people or agents installing and using the Socket marketplace. Put contributor workflow, maintainer commands, release process, subtree accounting, marketplace source-shape details, and root validation expectations in this file or the maintainer docs under [`docs/maintainers/`](./docs/maintainers/). Put durable agent-facing operating rules in [AGENTS.md](./AGENTS.md).

Do not add `README.md` files to monorepo-owned child plugin roots by default. The root Socket docs, plugin manifests, skill metadata, child `AGENTS.md`, and root planning docs are the normal documentation surfaces for those children. Keep child root READMEs only for standalone public surfaces such as `apple-dev-skills`; keep server-specific README files under bundled server directories such as `mcp/`.

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

If a root or child-repo workflow depends on Python quality tooling, declare that tooling in the relevant repo's `pyproject.toml` dev dependencies rather than assuming a machine-global install. Treat `pytest`, `ruff`, and `mypy` as the normal Python maintainer baseline when the repo's shipped validation surface uses them.

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

### Marketplace Shape

The repo-root marketplace lives at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json). It is a catalog, not a root aggregate plugin.

The installable local child entries currently point at:

- `./plugins/agent-plugin-skills`
- `./plugins/apple-dev-skills`
- `./plugins/cardhop-app`
- `./plugins/productivity-skills`
- `./plugins/python-skills`
- `./plugins/swiftasb-skills`
- `./plugins/things-app`

The Speak Swiftly entry points at the canonical Git-backed `gaelic-ghost/SpeakSwiftlyServer` plugin source as `speak-swiftly`, with the display name `Speak Swiftly`.

Placeholder entries may stay visible with `policy.installation: NOT_AVAILABLE` until they ship real plugin content. Current placeholder entries are `dotnet-skills`, `rust-skills`, `spotify`, and `web-dev-skills`.

For the detailed packaging stance, use [`docs/maintainers/plugin-packaging-strategy.md`](./docs/maintainers/plugin-packaging-strategy.md). For isolated install testing that leaves personal production installs alone, use [`docs/maintainers/plugin-install-testing.md`](./docs/maintainers/plugin-install-testing.md).

### Legacy Install Cleanup

If a contributor is cleaning up an older copied-plugin or local-personal-marketplace setup after confirming the Git-backed Socket marketplace works, use the repo-owned cleanup helper:

```bash
uv run scripts/cleanup_legacy_socket_installs.py
uv run scripts/cleanup_legacy_socket_installs.py --apply
```

The first command is a dry run. The `--apply` command backs up known legacy Socket install artifacts before removing them.

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

When the change intentionally bumps released version numbers across the superproject, inventory or update the maintained manifest surfaces with:

```bash
scripts/release.sh inventory
scripts/release.sh patch
scripts/release.sh minor
scripts/release.sh major
scripts/release.sh custom 1.2.3
```

Use the release modes in [`docs/maintainers/release-modes.md`](./docs/maintainers/release-modes.md) when preparing the actual release. Use `standard` for root-only releases and `subtrees` when a release also needs subtree pull/push accounting.

If the changed surface also introduces or expands Python-backed repo checks, add the required tools to the repo-local `uv` dev group and document the corresponding `uv run pytest`, `uv run ruff check .`, and `uv run mypy .` commands where that repo's contributors will actually look.

When editing docs, also review the rendered Markdown structure and cross-links for the files you changed.

When editing docs that include media, also review the image path, alt text, and adjacent explanatory prose.

### Release and Subtree Accounting

Use [`docs/maintainers/release-modes.md`](./docs/maintainers/release-modes.md) for release sequencing. Use `standard` for root-only releases and `subtrees` when a release also needs explicit subtree pull or push accounting.

Use the root release-version script when the task is to inventory or bump the maintained semantic-version surfaces across the superproject:

```bash
scripts/release.sh inventory
scripts/release.sh patch
scripts/release.sh minor
scripts/release.sh major
scripts/release.sh custom 1.2.3
```

`patch`, `minor`, and `major` assume every maintained version surface already shares one common semantic version. If versions are split, align them first with a `custom X.Y.Z` version.

Sometimes `socket` needs a patch-only release even when the visible root catalog shape did not otherwise change. This is the current maintainer workaround for refreshing Git-backed plugin entries that Codex resolves through the Socket marketplace, including `speak-swiftly` from `gaelic-ghost/SpeakSwiftlyServer`. Treat those bumps as real releases: run the shared version bump, validate the marketplace metadata, follow the release-ready gate, complete any required subtree accounting, tag the Socket release, create the GitHub release, and run `codex plugin marketplace upgrade socket` last.

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
