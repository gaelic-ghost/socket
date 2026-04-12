# AGENTS.md

## Repository Role

- This repository is the canonical home for `things-digest-generator` and `things-reminders-manager`.
- Keep active skills under [`skills/`](./skills/).
- Keep the bundled FastMCP server under [`mcp/things-app-mcp/`](./mcp/things-app-mcp/).
- Keep root plugin metadata thin and explicit.

## Source Of Truth

1. root [README.md](./README.md) for the mixed repo model and install-surface explanation
2. root [`skills/`](./skills/) for canonical workflow authoring
3. [`mcp/things-app-mcp/`](./mcp/things-app-mcp/) for the bundled server package, tests, and server-specific docs
4. root plugin manifests and marketplace files for install metadata only

## Repo-specific Rules

- Preserve the existing skill names unless a migration is explicitly requested.
- Update repo docs in the same change when the active skill inventory changes.
- Keep the repo honest about shipping three maintained surfaces: root skills, the bundled MCP server, and thin plugin packaging metadata.
- Do not let plugin manifests or marketplace files become the source of truth for workflow content or MCP-server behavior.
