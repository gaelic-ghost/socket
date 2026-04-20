# cardhop-app MCP

Local macOS MCP server for Cardhop.app using documented Cardhop integration routes:

- AppleScript: `tell application "Cardhop" to parse sentence "..."`
- URL scheme: `x-cardhop://parse?s=...`

`update` is intentionally implemented as a freeform alias over `parse` and does not depend on undocumented Cardhop routes.

## Requirements

- macOS
- `uv`
- Python 3.13+

## Install dependencies

```bash
uv sync
```

## Run locally

```bash
uv run python app/server.py
```

## Packaged Codex MCP config

The parent plugin at [`../.mcp.json`](../.mcp.json) exposes this server as `cardhop_app_socket` and launches it from the plugin root with:

```json
{
  "mcpServers": {
    "cardhop_app_socket": {
      "command": "uv",
      "args": ["run", "python", "app/server.py"],
      "cwd": "../../mcp"
    }
  }
}
```

## Exposed MCP tools

- `schema`: returns the locked schema bundle (`cardhop.mcp.tools.v1`)
- `parse`: send a sentence to Cardhop (`auto|applescript|url_scheme`, optional `add_immediately`, `dry_run`)
- `add`: convenience wrapper for parse with `add_immediately=true`
- `update`: freeform update guidance over parse semantics
- `healthcheck`: local readiness status for Cardhop + transport commands

## Update guidance

For best update behavior, use freeform instructions in this form:

- `"<existing name> <changed fields>"`
- Example: `Jane Doe new email jane@acme.com mobile 555-123-4567`

## Run validation checks

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

## Project layout

- `app/server.py`: FastMCP server entrypoint
- `app/tools.py`: Cardhop schema and tool logic
- `tests/test_tools.py`: unit tests for parsing, transport, and health behavior
- `pyproject.toml`: package metadata and dependencies
