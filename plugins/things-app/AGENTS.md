# AGENTS.md

This file is the Things App child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `things-app` owns Things-oriented skills plus a bundled FastMCP server for reminders, planning digests, and structured task workflows.
- Treat root [`skills/`](./skills/) as the source of truth for workflow-authoring behavior.
- Treat [`mcp/`](./mcp/) as the source of truth for bundled server code, tests, helper commands, and server-specific docs.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and [`.mcp.json`](./.mcp.json) as packaging and launch metadata only.

## Local Rules

- Keep the mixed skills-plus-server model explicit; do not collapse those surfaces into one vague plugin layer.
- Read [`mcp/README.md`](./mcp/README.md) before changing FastMCP behavior, AppleScript routing, auth-token handling, or HTTP smoke flows.
- Read the specific skill under [`skills/`](./skills/) before changing workflow behavior or renaming any workflow surface.
- Do not rename shipped skills or the MCP server surface casually.
- Do not change the packaged MCP command contract or relative `cwd` model in [`.mcp.json`](./.mcp.json) without making that packaging change explicit.

## Validation

Repo-root skill validation:

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

Optional bundled server smoke helpers live under `mcp`:

```bash
cd mcp
make inspect
make smoke-http
make smoke-json
make smoke-read
```
