# AGENTS.md

This file is the Cardhop App child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `cardhop-app` owns one Cardhop.app skill plus a bundled FastMCP server for contact capture and updates on macOS.
- Treat root [`skills/`](./skills/) as the source of truth for workflow-authoring behavior.
- Treat [`mcp/`](./mcp/) as the source of truth for bundled server code, tests, and server-specific docs.
- Treat [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) and [`.mcp.json`](./.mcp.json) as packaging and launch metadata only.

## Local Rules

- Keep the mixed skill-plus-server model explicit; do not collapse those surfaces into one vague plugin layer.
- Read [`mcp/README.md`](./mcp/README.md) before changing FastMCP behavior, AppleScript routing, URL-scheme dispatch, or server validation.
- Read the specific skill under [`skills/`](./skills/) before changing workflow behavior or renaming any workflow surface.
- Do not rename the shipped skill or MCP server surface casually.

## Validation

Bundled server validation:

```bash
cd mcp
uv run pytest
uv run ruff check .
uv run mypy .
```
