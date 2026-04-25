# AGENTS.md

Use this file for durable repo-local guidance that Codex should follow before changing code, docs, or project workflow surfaces in this repository.

## Repository Scope

### What This File Covers

- `cardhop-app` is the canonical home for Gale's Cardhop.app skill, the bundled FastMCP server, and the thin plugin packaging that exposes those surfaces to Codex.
- Use this file to coordinate the root guidance files, the authored skill surface under [`skills/`](./skills/), the bundled server package under [`mcp/`](./mcp/), and the repo-root plugin metadata.
- Treat this repository as a mixed skill-plus-server repo on purpose. Do not collapse those surfaces into one vague "plugin" layer.

### Where To Look First

- Start with [README.md](./README.md), [CONTRIBUTING.md](./CONTRIBUTING.md), and [ROADMAP.md](./ROADMAP.md) for the current repo shape and contributor expectations.
- Read [`mcp/README.md`](./mcp/README.md) before changing the bundled server package or its local validation flow.
- Read the specific skill under [`skills/`](./skills/) before changing workflow behavior or renaming any workflow surface.

## Working Rules

### Change Scope

- Keep work bounded to the surface that actually changed: root skill, bundled server, or thin packaging metadata.
- When one change crosses those boundaries, update the nearby docs in the same pass so the mixed-repo model stays explicit.
- Surface scope widening before introducing another skill, renaming a shipped workflow, or changing the packaged MCP command contract.

### Source of Truth

- Treat root [`skills/`](./skills/) as the source of truth for workflow-authoring behavior.
- Treat [`mcp/`](./mcp/) as the source of truth for bundled server code, tests, and server-specific docs.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and [`.mcp.json`](./.mcp.json) as packaging and launch metadata only.
- Keep the repo honest about the install surfaces that actually exist. Do not claim a discovery mirror or packaged surface is present unless it is checked in here.

### Dependency Provenance

- Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories that another contributor can fetch.
- Do not commit dependency declarations, lockfiles, scripts, docs, examples, generated project files, or CI config that point at machine-local paths such as `/Users/...`, `~/...`, `../...`, local worktrees, or private checkout paths.
- Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly. If local integration is needed, keep it uncommitted or convert it to a tagged release, branch, or registry dependency before sharing.

### Communication and Escalation

- Start from the root docs when the task is about the mixed repo model, contributor workflow, packaging boundaries, or root guidance alignment.
- Start from the bundled server docs when the task is really about FastMCP behavior, AppleScript routing, URL-scheme dispatch, or validation flows.
- Stop and surface the tradeoff before broadening the repo from its current single-skill scope into a larger Cardhop automation bundle or a materially different plugin packaging model.

## Commands

### Setup

Bundled server setup:

```bash
cd mcp
uv sync
```

### Validation

Bundled server validation:

```bash
cd mcp
uv run pytest
uv run ruff check .
uv run mypy .
```

## Review and Delivery

### Review Expectations

- Keep README, CONTRIBUTING, ROADMAP, and the bundled server README aligned when a shared contract changes.
- Say clearly which surface changed and which validation path you ran.
- When a change only affects one surface, avoid broad edits in unrelated packaging or server files.

### Definition of Done

- The change is grounded in the correct source-of-truth surface for the behavior you touched.
- The relevant validation commands ran for the changed surface.
- Nearby docs and packaging metadata were updated when behavior, install wiring, or contributor workflow changed.

## Safety Boundaries

### Never Do

- Do not rename the shipped skill or MCP server surface casually.
- Do not treat plugin manifests or launch metadata as the source of truth for workflow behavior.
- Do not claim install surfaces or local files exist when they are not checked in here.
- Do not skip the bundled server README and tests when changing `mcp/`.

### Ask Before

- Ask before adding another skill or another packaged host surface.
- Ask before changing the packaged MCP command contract or the relative `cwd` model in [`.mcp.json`](./.mcp.json).
- Ask before making repo-wide terminology changes that would rename user-facing workflows, tool names, or packaging concepts.
