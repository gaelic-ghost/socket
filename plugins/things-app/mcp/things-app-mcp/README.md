# things-mcp

Local Python MCP server for Things.app on macOS. The server executes Things actions through the official `things:///` URL scheme.

## Requirements

- macOS
- Things.app installed
- `uv`
- Python 3.13+

## Install dependencies

```bash
uv sync
```

## Configure auth token for update commands

Updates in the Things URL scheme require an auth token.

```bash
export THINGS_AUTH_TOKEN="<your-things-auth-token>"
```

You can also pass `auth_token` directly to update tools, or store a token in macOS keychain:

```bash
make call TOOL=things_auth_set_token ARGS_JSON='{"token":"YOUR_TOKEN"}'
make call TOOL=things_auth_get_status
make call TOOL=things_auth_clear_token
```

Token resolution order for update operations:

1. explicit `auth_token` argument
2. `THINGS_AUTH_TOKEN` environment variable
3. keychain token (`things_auth_set_token`)

## FastMCP local run and test workflow

These commands use the FastMCP CLI patterns from the FastMCP docs (`inspect`, `run`, `list`, `call`) and are wrapped in this repo's helper targets.

## Transport and Codex compatibility

- Default server entrypoint (`python app/server.py` or `mcp.run()`) uses FastMCP's standard stdio transport, which is the transport Codex MCP integrations expect.
- Local development smoke tests in this repo use HTTP transport (`fastmcp run --transport http`) so `fastmcp list/call` can run from a second terminal.
- No transport changes are required for Codex use as long as your Codex MCP config launches this server command over stdio.

### Make targets

```bash
make inspect
make run-http
make list-http
make call-health
make call TOOL=things_capabilities
make call TOOL=things_add_todo ARGS_JSON='{"title":"Example task","notes":"From FastMCP CLI"}'
make call TOOL=things_update_project ARGS_JSON='{"id":"PROJECT_ID","title":"New title","auth_token":"TOKEN"}'
make call TOOL=things_import_json ARGS_JSON='{"data":[{"type":"to-do","attributes":{"title":"From JSON"}}]}'
make test
make lint
make typecheck
make check
make smoke-http
make smoke-json
make smoke-read
```

### Script equivalents

```bash
./scripts/local_fastmcp.sh inspect
./scripts/local_fastmcp.sh run-http
./scripts/local_fastmcp.sh list-http
./scripts/local_fastmcp.sh call-health
./scripts/local_fastmcp.sh call things_capabilities
./scripts/local_fastmcp.sh call things_add_todo '{"title":"Example task","notes":"From FastMCP CLI"}'
./scripts/local_fastmcp.sh call things_update_project '{"id":"PROJECT_ID","title":"New title","auth_token":"TOKEN"}'
./scripts/local_fastmcp.sh call things_import_json '{"data":[{"type":"to-do","attributes":{"title":"From JSON"}}]}'
./scripts/local_fastmcp.sh test
./scripts/local_fastmcp.sh smoke-http
./scripts/local_fastmcp.sh smoke-json
./scripts/local_fastmcp.sh smoke-read
```

Defaults:

- `HOST=127.0.0.1`
- `PORT=8123`
- `MCP_URL=http://127.0.0.1:8123/mcp`
- `SERVER_SPEC=app/server.py`

Override example:

```bash
make run-http PORT=9000
make list-http MCP_URL=http://127.0.0.1:9000/mcp
```

Generic tool calling:

- `TOOL` selects any MCP tool exposed by this server.
- `ARGS_JSON` is optional JSON passed to `--input-json`.
- `make call` expects a running server at `MCP_URL` (for example, run `make run-http` in another terminal).

Examples:

```bash
make call TOOL=health
make call TOOL=things_capabilities
make call TOOL=things_add_todo ARGS_JSON='{"title":"Inbox review","when":"today"}'
make call TOOL=things_update_project ARGS_JSON='{"id":"PROJECT_ID","deadline":"2026-03-01","auth_token":"TOKEN"}'
make call TOOL=things_update_todo ARGS_JSON='{"id":"TODO_ID","prepend_notes":"[bot] ","add_tags":["automated"],"list_name":"Today","auth_token":"TOKEN"}'
make call TOOL=things_import_json ARGS_JSON='{"data":[{"type":"to-do","attributes":{"title":"Batch item"}}]}'
make call TOOL=things_read_todos ARGS_JSON='{"list_id":"today","limit":20}'
make call TOOL=things_find_todos ARGS_JSON='{"query":"invoice","limit":10}'
make call TOOL=things_read_todos ARGS_JSON='{"list_id":"anytime","status":"open","project_id":"PROJECT_ID","include_notes":true,"limit":50}'
make call TOOL=things_read_projects ARGS_JSON='{"status":"open","area_id":"AREA_ID","limit":20}'
make call TOOL=things_read_areas
make call TOOL=things_read_headings ARGS_JSON='{"project_id":"PROJECT_ID","query":"plan","limit":20}'
```

## Implemented MCP tools

- `health`: basic service heartbeat.
- `things_add_todo`: create a to-do via `things:///add`.
- `things_add_project`: create a project via `things:///add-project`.
- `things_update_todo`: update an existing to-do via `things:///update` (requires auth token).
  - includes common automation params: `prepend_notes`, `append_notes`, `add_tags`, checklist variants, list/heading moves, `duplicate`.
- `things_show`: navigate/show a list or item via `things:///show`.
- `things_search`: open Things search with optional query via `things:///search`.
- `things_update_project`: update an existing project via `things:///update-project` (requires auth token).
  - includes common automation params: `prepend_notes`, `append_notes`, `add_tags`, `duplicate`.
- `things_import_json`: create/update Things items in batch via `things:///json` (auth token required when JSON includes `update` operations).
- `things_read_todos`: read to-dos by list via AppleScript (`osascript`), with filters (`status`, `project_id`, `area_id`) and pagination (`offset`, `limit`).
  - supports date filters: `deadline_before`, `deadline_after`, `completed_before`, `completed_after` (ISO-8601).
  - status is normalized to `open`, `completed`, or `canceled` and original value is preserved as `status_raw`.
- `things_read_todo`: read a single to-do by ID via AppleScript (`include_notes` supported).
- `things_find_todos`: search to-do titles via AppleScript with filters/pagination and date filters.
- `things_read_projects`: read projects via AppleScript with status/area/date filters.
- `things_read_areas`: read area IDs and titles via AppleScript.
- `things_read_headings`: read headings across projects via AppleScript with optional `project_id` and title `query` filters.
- `things_auth_set_token`: store token in keychain.
- `things_auth_get_status`: check token source availability.
- `things_auth_clear_token`: clear keychain token.
- `things_version`: fetch Things version/build through `things:///version` with x-callback.
- `things_validate_token_config`: verify update-token configuration state.
- `things_capabilities`: list currently implemented capabilities.

See route coverage matrix: [docs/things-route-matrix.md](docs/things-route-matrix.md)
Practical command examples: [docs/examples.md](docs/examples.md)

`things_import_json` includes lightweight shape validation before dispatch:

- `operation` must be `create` or `update`.
- `id` is required for `update` operations.
- `attributes` must be an object when present.
- nested `to-dos`/`headings`/`items` must be arrays of objects.

For safe end-to-end CLI smoke checks without modifying real Things data, use `make smoke-json`. It runs the server with `THINGS_MCP_DRY_RUN=1`, which skips launching `things:///` URLs.

Sensitive URL params are redacted in tool responses (for example `auth-token`) so returned URLs are safe to log.

## macOS Permissions Caveat

Read tools use AppleScript and require macOS Automation permission for the app running Codex/Terminal to control Things. If read calls fail with permission errors:

1. Open `System Settings > Privacy & Security > Automation`.
2. Allow the terminal/Codex app to control `Things3`.
3. Re-run `make smoke-read`.

## Error Codes

Common normalized error codes:

- `THINGS_AUTH_MISSING`: no auth token in arg/env/keychain for update operations.
- `THINGS_AUTH_KEYCHAIN_WRITE_FAILED` / `THINGS_AUTH_KEYCHAIN_READ_FAILED` / `THINGS_AUTH_KEYCHAIN_CLEAR_FAILED`: keychain operation failed.
- `THINGS_AUTOMATION_DENIED`: macOS Automation permission blocked AppleScript access to Things3.
- `THINGS_APP_UNAVAILABLE`: Things3 is not running or not reachable via AppleScript.
- `THINGS_SCRIPT_FAILED`: generic AppleScript execution failure.
- `THINGS_INVALID_STATUS`: unsupported `status` filter (must be `open`, `completed`, or `canceled`).
- `THINGS_INVALID_DATE_FILTER`: invalid date filter format (must be ISO-8601 date/datetime).

## Project layout

- `app/server.py`: FastMCP server entrypoint and tool registration.
- `app/tools.py`: tool payload builders and validation.
- `app/things_client.py`: URL builder, launcher, and callback listener.
- `scripts/local_fastmcp.sh`: local FastMCP CLI helper.
- `tests/test_tools.py`: payload and validation tests.
- `tests/test_things_client.py`: URL encoding and callback client tests.
- `docs/things-route-matrix.md`: route coverage and next implementation targets.
- `docs/examples.md`: copy-paste local CLI examples for each major tool.

## Development Quickstart

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy .
```
