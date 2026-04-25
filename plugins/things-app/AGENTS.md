# AGENTS.md

Use this file for durable repo-local guidance that Codex should follow before changing code, docs, or project workflow surfaces in this repository.

## Repository Scope

### What This File Covers

- `things-app` is the canonical home for Gale's Things-oriented skills, the bundled FastMCP server, and the thin plugin packaging that exposes those surfaces to Codex and Claude.
- Use this file to coordinate the root guidance files, the authored skill surfaces under [`skills/`](./skills/), the bundled server package under [`mcp/`](./mcp/), and the repo-root plugin metadata.
- Treat this repository as a mixed skills-plus-server repo on purpose. Do not collapse those surfaces into one vague "plugin" layer.

### Where To Look First

- Start with [README.md](./README.md), [CONTRIBUTING.md](./CONTRIBUTING.md), and [ROADMAP.md](./ROADMAP.md) for the current repo shape and contributor expectations.
- Read [`mcp/README.md`](./mcp/README.md) before changing the bundled server package or its local validation flow.
- Read the specific skill under [`skills/`](./skills/) before changing workflow behavior or renaming any workflow surface.

## Working Rules

### Change Scope

- Keep work bounded to the surface that actually changed: root skills, bundled server, or thin packaging metadata.
- When one change crosses those boundaries, update the nearby docs in the same pass so the mixed-repo model stays explicit.
- Surface scope widening before introducing a new skill, renaming a shipped workflow, changing the packaged MCP command contract, or adding another install/discovery surface.

### Source of Truth

- Treat root [`skills/`](./skills/) as the source of truth for workflow-authoring behavior.
- Treat [`mcp/`](./mcp/) as the source of truth for bundled server code, tests, helper commands, and server-specific docs.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json), [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json), and [`.mcp.json`](./.mcp.json) as packaging and launch metadata only.
- Keep the repo honest about the install surfaces that actually exist. Do not claim a discovery mirror, license file, or packaged surface is present unless it is checked in here.

### Dependency Provenance

- Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch.
- Do not commit dependency declarations, lockfiles, scripts, docs, examples, generated project files, or CI config that point at machine-local paths such as `/Users/...`, `~/...`, `../...`, local worktrees, or private checkout paths.
- Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly. If local integration is needed, keep it uncommitted or convert it to a tagged release, branch, or registry dependency before sharing.

### Communication and Escalation

- Start from the root docs when the task is about the mixed repo model, contributor workflow, packaging boundaries, or root guidance alignment.
- Start from the bundled server docs when the task is really about FastMCP behavior, AppleScript routing, auth-token handling, or HTTP smoke flows.
- Stop and surface the tradeoff before broadening the repo from its current two-skill scope into a larger Things automation bundle or a materially different plugin packaging model.

### Sync And Branch Accounting Gates

- Treat repo-sync verification and local-branch accounting as hard gates before cleanup or "done" claims.
- When work in this repository is performed from the `socket` superproject or is expected to ship back through `socket`, verify whether `socket` now needs an explicit sync step and either complete it or say plainly why no sync is required.
- Before saying work is merged, preserved, or safe to delete, verify the exact commit reachability in the repo and remote being discussed.
- Before deleting local branches, remote branches, worktrees, or rescue refs, enumerate every local branch not contained by `main` and account for each one explicitly as preserved elsewhere, intentionally in progress, newly archived, newly merged, or safe to delete.
- Do not treat branch cleanup as routine hygiene that can happen before that accounting pass.

## Commands

### Setup

Repo-root setup:

```bash
uv sync --dev
```

Bundled server setup:

```bash
cd mcp
uv sync
```

### Validation

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

### Optional Project Commands

Bundled server smoke and helper commands live under `mcp`:

```bash
cd mcp
make inspect
make smoke-http
make smoke-json
make smoke-read
```

## Review and Delivery

### Review Expectations

- Keep README, CONTRIBUTING, ROADMAP, AGENTS, and the bundled server README aligned when a shared contract changes.
- Say clearly which surface changed and which validation path you ran.
- When a change only affects one surface, avoid broad edits in unrelated packaging or server files.

### Definition of Done

- The change is grounded in the correct source-of-truth surface for the behavior you touched.
- The relevant validation commands ran for the changed surface.
- Nearby docs and packaging metadata were updated when behavior, install wiring, or contributor workflow changed.
- Any required superproject or nested-repo sync has been completed or surfaced explicitly before cleanup.
- Local branches not contained by `main` have been accounted for explicitly before deleting anything.

## Safety Boundaries

### Never Do

- Do not rename the shipped skills or MCP server surface casually.
- Do not treat plugin manifests or launch metadata as the source of truth for workflow behavior.
- Do not claim install surfaces or local files exist when they are not checked in here.
- Do not skip the bundled server README and tests when changing `mcp/`.

### Ask Before

- Ask before adding another skill, another packaged host surface, or another bundled service.
- Ask before changing the packaged MCP command contract or the relative `cwd` model in [`.mcp.json`](./.mcp.json).
- Ask before making repo-wide terminology changes that would rename user-facing workflows, tool names, or packaging concepts.

## Local Overrides

- There are currently no deeper `AGENTS.md` files below this repo root.
- Use the specific skill docs under `skills/` and the bundled server docs under `mcp/` as narrower workflow guidance when work happens there.
