# Contributing

Practical contributor and maintainer guide for working on `SpeakSwiftlyServer`, including local setup, validation, live end-to-end coverage, pull request workflow, and release handoff.

## Table of Contents

- [Overview](#overview)
- [Contribution Workflow](#contribution-workflow)
- [Local Setup](#local-setup)
- [Development Expectations](#development-expectations)
- [Pull Request Expectations](#pull-request-expectations)
- [Communication](#communication)
- [Documentation Map](#documentation-map)
- [Monorepo and Submodule Handoff](#monorepo-and-submodule-handoff)
- [Release Workflow](#release-workflow)
- [License and Contribution Terms](#license-and-contribution-terms)

## Overview

### Who This Guide Is For

This guide is for contributors and maintainers making source, docs, test, release, or operator-surface changes in the standalone `SpeakSwiftlyServer` repository.

### Before You Start

- Treat `Package.swift` as the source of truth for package structure, dependencies, resources, and deployment targets.
- Start with [AGENTS.md](./AGENTS.md) for the repo's package, architecture, and workflow rules.
- Keep package graph changes together in one pass, including `Package.swift`, `Package.resolved`, tests, and matching docs.
- Keep transport-local shaping at the HTTP and MCP edges. If `SpeakSwiftly` or `TextForSpeech` can express a concept directly, prefer deleting server-local inference instead of adding another translation layer.
- Preserve the current standalone package baseline on macOS 15 while keeping the host and state model friendly to the near-future iOS reuse path.

## Contribution Workflow

### Choosing Work

Choose work from the current repo state rather than from stale assumptions. Use [README.md](./README.md) for the product and operator story, [ROADMAP.md](./ROADMAP.md) for planned work, and the maintainer docs under [docs/maintainers](./docs/maintainers/) when the task touches releases, source layout, or transport behavior.

For substantial changes, work on a feature branch instead of local `main`. When a task already has active release or bug-fix context on a branch, keep the follow-on work stacked on that line unless maintainers explicitly want a separate branch.

### Making Changes

Use the `xcrun` SwiftPM path intentionally in this repository:

```bash
xcrun swift build
xcrun swift test
```

This repo documents the `xcrun` form because the standalone Swiftly-selected Swift 6.3 toolchain currently reproduces a transitive `_NumericsShims` module-loading failure that does not appear when SwiftPM runs through Xcode's selected toolchain.

Keep work bounded and coherent:

- keep transport concerns at the HTTP and MCP edges
- keep host ownership narrow instead of adding new coordinator layers casually
- update docs in the same pass when HTTP, MCP, LaunchAgent, release, or source-layout behavior changes
- prefer the repo-maintenance scripts over one-off release or validation command chains when the repo already owns a workflow

### Asking For Review

Before asking for review, make sure the affected docs are in sync, the local validation path for the change has run, and any release-relevant or operator-facing behavior changes are called out plainly. For release work, use the documented branch-to-`main` split instead of trying to tag directly from a feature branch.

## Local Setup

### Runtime Config

The concrete runtime config surfaces in this repo are:

- [`server.yaml`](./server.yaml) for local config examples
- `APP_CONFIG_FILE` for YAML-backed configuration
- `SPEAKSWIFTLY_PROFILE_ROOT` for the runtime-owned profile and persistence root
- the staged release artifact under `.release-artifacts/current/` for LaunchAgent-owned runs

The shared server supports the same environment variables documented in [README.md](./README.md#configuration), including the `APP_*` transport settings and `SPEAKSWIFTLY_PROFILE_ROOT`.

### Runtime Behavior

The default local package workflow is:

```bash
xcrun swift build
xcrun swift test
```

Use the unified tool surface when you want to inspect the operator path directly:

```bash
xcrun swift run SpeakSwiftlyServerTool help
xcrun swift run SpeakSwiftlyServerTool launch-agent print-plist
xcrun swift run SpeakSwiftlyServerTool healthcheck
```

Before any live end-to-end run, stop the LaunchAgent-backed live service first:

```bash
./.release-artifacts/current/SpeakSwiftlyServerTool launch-agent uninstall
```

That matters because the live E2E harness is intentionally a one-speaking-server surface. The helper now fails fast when the LaunchAgent-backed service is still loaded or when a competing `SpeakSwiftlyServerTool serve` process is already running.

## Development Expectations

### Naming Conventions

Keep user-facing lifecycle vocabulary consistent across docs, scripts, and commands. In this repo that means preferring pairs like `install` and `uninstall`, using `promote-live` for staged-to-live promotion, and avoiding alternate verbs for the same operator action unless a compatibility surface already requires them.

Match the current boundary language in the code:

- `EmbeddedServer` is the public app-owned embedding surface
- transport-local shaping belongs at the HTTP and MCP edges
- internal host ownership should stay behind the package boundary instead of leaking new public helpers casually

### Accessibility Expectations

This repository does not currently maintain a separate top-level `ACCESSIBILITY.md`. For relevant work, treat accessibility and operator clarity as part of normal change quality: keep user-facing logs, errors, and documentation explicit, readable, and unambiguous, and call out any new user-visible limitation plainly in docs or review notes when it matters.

### Verification

The maintainer validation entrypoint is:

```bash
sh scripts/repo-maintenance/validate-all.sh
```

Direct formatter and linter commands are:

```bash
swiftformat --lint --config .swiftformat .
swiftformat --config .swiftformat .
swiftlint lint --config .swiftlint.yml
```

The full live end-to-end gate should be run one suite at a time, in separate foreground commands:

```bash
SPEAKSWIFTLYSERVER_E2E=1 xcrun swift test --filter HTTPWorkflowE2ETests
SPEAKSWIFTLYSERVER_E2E=1 xcrun swift test --filter MCPWorkflowE2ETests
SPEAKSWIFTLYSERVER_E2E=1 xcrun swift test --filter ControlE2ETests
```

Do not overlap those suites or run the full live target as one giant parallelized process. The repo's live E2E surface is intentionally a serial, one-suite-at-a-time gate.

## Pull Request Expectations

Summarize what changed, why it changed, and what reviewers should pay attention to first. For release work, make sure the branch-side candidate preparation is complete before handing it off to `main` for the final publish step.

## Communication

Raise uncertainty early when a task starts pushing on architecture, release semantics, or live-service behavior. If the clean path needs wider scope than the original request, say so before the change sprawls. If a behavior changed across docs, HTTP, MCP, LaunchAgent, or embedding surfaces, mention that explicitly instead of assuming reviewers will reconstruct it from the diff.

## Documentation Map

- [README.md](./README.md) is the product and operator-facing entrypoint.
- [API.md](./API.md) is the detailed HTTP and MCP contract reference.
- [docs/maintainers/source-layout.md](./docs/maintainers/source-layout.md) is the maintainer map for the current source split.
- [docs/maintainers/release-workflow.md](./docs/maintainers/release-workflow.md) is the branch-versus-`main` release contract.
- [docs/maintainers](./docs/maintainers/) holds release checklists, release notes, and other maintainer-facing supporting docs.

## Monorepo and Submodule Handoff

- Treat `../../speak-to-user/monorepo/packages/SpeakSwiftlyServer` as the integration submodule copy, not the primary development home.
- Treat the local `../../speak-to-user/monorepo` checkout as a clean base checkout that stays on `main` and stays clean.
- Never use that clean base checkout for feature work, experiments, release bumps, or submodule-pointer edits.
- For monorepo work, create a dedicated `git worktree`, do the work there, open a pull request, and then delete the merged worktree and branch afterward.
- When `speak-to-user` adopts a new server version, prefer updating the submodule pointer to a tagged `SpeakSwiftlyServer` release instead of an arbitrary branch tip.

## Release Workflow

Use the repo-maintenance release split intentionally:

```bash
scripts/repo-maintenance/release-prepare.sh --version vX.Y.Z
scripts/repo-maintenance/release-publish.sh --version vX.Y.Z --skip-live-service-refresh
```

Use `release-prepare.sh` from a feature branch or worktree when the job is "push this release candidate, open or update the PR, and queue auto-merge." Use `release-publish.sh` from local `main` after that PR merges when the job is "cut the actual tag and GitHub release."

For the detailed contract and edge cases, use [docs/maintainers/release-workflow.md](./docs/maintainers/release-workflow.md).

## License and Contribution Terms

This repository is licensed under [Apache License 2.0](./LICENSE). By contributing, you are contributing changes under that same project license.
