# AGENTS.md

## Repository Expectations

- This repository is the canonical home for `things-digest-generator` and `things-reminders-manager`.
- Keep active skills under `skills/`.
- Keep the bundled FastMCP server under `mcp/things-app-mcp/`.
- Keep packaged plugin metadata under `plugins/things-app/`.
- Keep skill runtime resources self-contained inside each skill directory.

## Source Of Truth

1. Root `README.md` for the current mixed repo model and install-surface explanation.
2. Root `skills/` for canonical workflow authoring.
3. `mcp/things-app-mcp/` for the bundled server's package, tests, and server-specific docs.
4. `plugins/things-app/` plus the repo-root marketplace files for install metadata only.

## Maintainer Guidance

- Prefer `uv run pytest` for repo-level Python validation.
- Preserve the existing skill names unless a migration is explicitly requested.
- Update repo docs in the same change when the active skill inventory changes.
- Keep the repo honest about shipping three maintained surfaces: root skills, the bundled MCP server, and thin plugin packaging metadata.
- Do not let plugin manifests or marketplace files become the source of truth for workflow content or MCP-server behavior.
