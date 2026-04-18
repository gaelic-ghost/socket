# Contributing to things-app

Use this guide when preparing changes so the repo stays understandable, runnable, and reviewable across its three active surfaces: root skills, the bundled MCP server, and thin plugin packaging metadata.

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

Use this guide when contributing to the root Things skills, the bundled FastMCP server under `mcp/`, or the repo-root plugin packaging and guidance files that tie those surfaces together.

### Before You Start

- Read [README.md](./README.md) for the mixed repo model and install-surface overview.
- Read [AGENTS.md](./AGENTS.md) for durable maintainer boundaries.
- Read [`mcp/README.md`](./mcp/README.md) before changing the bundled server package.
- Confirm which surface actually owns the behavior you want to change before editing files.

## Contribution Workflow

### Choosing Work

Choose work by identifying the owning surface first:

- `skills/` for workflow-authoring behavior
- `mcp/` for server implementation and FastMCP tooling
- repo-root packaging files and docs for installation, discovery, and contributor guidance

If the change needs to cross those boundaries, keep the scope explicit and update the nearby docs in the same pass.

### Making Changes

Keep edits bounded and coherent. Change the authored surface first, then update packaging metadata or root docs only when the shipped contract actually changed. Avoid letting launch metadata drift into the role of behavioral source of truth.

For server changes, prefer editing and validating inside `mcp/` rather than patching around behavior from root docs or plugin files.

### Asking For Review

Ask for review when the owning surface is clear, the relevant checks have run, and the docs affected by that change are aligned. Call out whether the change touched root skills, the bundled server, packaging metadata, or more than one of those surfaces.

## Local Setup

### Runtime Config

Root skill-maintainer setup:

```bash
uv sync --dev
```

Bundled server setup:

```bash
cd mcp
uv sync
```

Server update flows may require a Things auth token. The bundled server supports:

- explicit `auth_token` arguments to update tools
- `THINGS_AUTH_TOKEN` in the environment
- keychain-backed token storage through the bundled auth tools

Read and update flows also assume macOS with Things.app installed.

### Runtime Behavior

Nothing needs to run continuously for repo-root skill work. The root `pyproject.toml` currently supports a narrow pytest surface for the digest skill tests.

For bundled server work:

- Codex packaging uses stdio launch through [`.mcp.json`](./.mcp.json)
- local smoke flows use the HTTP helper commands inside `mcp`
- read tools depend on macOS Automation permission for the host app controlling Things

If read calls fail locally, verify Automation permissions before assuming the server code is broken.

## Development Expectations

### Naming Conventions

- Keep the existing skill names stable unless a migration is explicitly intended.
- Use `skill`, `bundled MCP server`, and `plugin packaging` consistently so the repo shape stays understandable.
- Match existing tool names and avoid introducing alternate names for the same user-facing workflow unless the change intentionally includes a migration.

### Accessibility Expectations

This repository is mostly documentation, workflow-authoring, and local automation surfaces rather than end-user UI. Accessibility work here mainly means keeping contributor docs readable, install instructions explicit, and tool descriptions clear enough to use without guessing.

When a change affects user-facing examples, commands, or workflow guidance, keep the language plain and the step order easy to follow in ordinary Markdown readers.

### Verification

Run the checks that match the surface you changed.

Repo-root validation:

```bash
uv run pytest
```

Bundled server validation:

```bash
cd mcp
uv run pytest
uv run ruff check .
uv run mypy .
```

Useful bundled-server smoke commands:

```bash
cd mcp
make smoke-http
make smoke-json
make smoke-read
```

## Pull Request Expectations

Summarize what changed, why it changed, and which repo surface owns the behavior. Point reviewers to the most relevant docs or server files first, and include the exact validation commands you ran.

If packaging metadata changed, call out whether the launch command, relative `cwd`, or shipped discovery surfaces changed with it.

## Communication

Surface questions early when a change starts widening from one repo surface into another, especially if it would rename a shipped workflow, add another packaging surface, or change the bundled MCP contract.

When in doubt, ask whether the work should stay in root skills, move into `mcp/`, or remain thin packaging-only maintenance.

## License and Contribution Terms

Keep contributor-facing license language aligned with the repository's checked-in license terms. If a local `LICENSE` file is added or changed, update this guide and [README.md](./README.md) in the same pass.
