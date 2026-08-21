# Contributing to Socket

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

This guide is for contributors changing Socket's root marketplace, managed
documentation, repository maintenance, compatibility metadata, or the
monorepo-owned plugin payloads under [`plugins/`](./plugins/).

### Before You Start

Read [README.md](./README.md), [AGENTS.md](./AGENTS.md), and
[ROADMAP.md](./ROADMAP.md). Work in the closest owning plugin when a change is
plugin-specific. Speak Swiftly remains Git-backed and is maintained in its
standalone repository.

## Contribution Workflow

### Choosing Work

Root work includes marketplace wiring, shared exports, root documentation,
cross-plugin compatibility, FSX repository automation, and release policy.
Child implementation belongs under its owning directory in `plugins/`.

### Making Changes

Use a `<scope>/<slug>` feature branch. Keep one coherent concern per change and
update the owning source rather than an installed cache or generated copy.
Repository Skills source lives under `plugins/repository-skills`; root exports
are synchronized by `just repo-sync`.

Documentation is always maintained as one four-file transaction. The only docs
commands are:

```bash
just docs-check
just docs-apply
```

### Asking For Review

State the changed ownership surface, compatibility consequence, and exact
commands run. Do not claim a release, installation, or synchronization that was
not performed.

## Local Setup

### Runtime Config

Socket pins .NET in [`global.json`](./global.json) and exposes maintainer work
through [`justfile`](./justfile). Install a compatible .NET 10 SDK and `just`,
then inspect the recipes:

```bash
just --list
```

Do not add Python or shell maintainer scripts, direct operator-facing script
commands, nested test suites, or per-document recipes.

### Runtime Behavior

Socket has no root application. Its essential validation is integration-level:

```bash
just repo-validate
just test
```

`repo-validate` checks marketplace-to-plugin resolution, shared version
alignment, Claude compatibility references, root-only test placement, managed
repository assets, and the four canonical documents. `test` runs the installer,
docs apply/idempotence/check, Just interface, and repository validation in a
temporary Git repository. There are no unit-style or child-local test suites.

Use `just repo-sync` to refresh generated root skill exports and validate the
result. Do not edit root `skills/` by hand.

### Xcode Workspace

[`Socket.xcworkspace`](./Socket.xcworkspace) is browse-only. Do not add a root
project, scheme, target, or package solely for documentation browsing.

### Marketplace Shape

The catalog at [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
points to monorepo-owned local plugins plus the Git-backed Speak Swiftly source.
It is not an aggregate plugin. Each local entry must resolve to a matching
`.codex-plugin/plugin.json`.

## Development Expectations

### Naming Conventions

Use `skill` for a reusable workflow, `plugin` for an installable bundle, and
`subagent` for a delegated runtime worker. Keep names aligned across manifests,
skills, marketplaces, documentation, and reports.

### Accessibility Expectations

Keep commands, logs, headings, links, errors, and user-facing behavior readable
and actionable. Record product-specific accessibility requirements beside the
surface that owns them; do not create a separate root accessibility contract.

### Verification

Run the root integration surface:

```bash
just docs-check
just repo-validate
just test
```

For a requested release, author `docs/releases/vX.Y.Z.md`, then use only:

```bash
just repo-release-prepare X.Y.Z
just repo-release-inspect X.Y.Z
just repo-release-advance X.Y.Z
```

See [`docs/maintainers/release-workflow.md`](./docs/maintainers/release-workflow.md)
for release gates. Do not invoke internal FSX files directly.

## Pull Request Expectations

A pull request should state what changed, why it belongs at that ownership
layer, any generated or compatibility surfaces updated, and the integration
commands run. Preserve the current PR body when updating an existing pull
request.

## Communication

Surface ownership, packaging, compatibility, release, or destructive cleanup
consequences explicitly. Ask before widening the marketplace architecture.

## License and Contribution Terms

Contributions are licensed under [Apache License 2.0](./LICENSE). Use Developer
Certificate of Origin sign-off when the repository requires it:

```text
Signed-off-by: Your Name <you@example.com>
```
