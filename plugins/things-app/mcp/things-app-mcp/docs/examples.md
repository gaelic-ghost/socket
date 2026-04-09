# Things MCP Examples

These examples assume your server is running locally.

## Start server

```bash
make run-http
```

In another terminal, call tools with `make call`.

## Keychain token lifecycle

```bash
make call TOOL=things_auth_set_token ARGS_JSON='{"token":"TOKEN"}'
make call TOOL=things_auth_get_status
make call TOOL=things_auth_clear_token
```

## Add a to-do

```bash
make call TOOL=things_add_todo ARGS_JSON='{"title":"Inbox review","when":"today","tags":["work"]}'
```

## Show a built-in list

```bash
make call TOOL=things_show ARGS_JSON='{"id":"today"}'
```

## Search

```bash
make call TOOL=things_search ARGS_JSON='{"query":"vacation"}'
```

## Update a project

```bash
make call TOOL=things_update_project ARGS_JSON='{"id":"PROJECT_ID","title":"Quarter Plan","auth_token":"TOKEN"}'
```

## Update a to-do with common automation fields

```bash
make call TOOL=things_update_todo ARGS_JSON='{"id":"TODO_ID","prepend_notes":"[bot] ","add_tags":["automated"],"list_name":"Today","auth_token":"TOKEN"}'
```

## JSON import (create-only)

```bash
make call TOOL=things_import_json ARGS_JSON='{"data":[{"type":"to-do","attributes":{"title":"From JSON"}}],"reveal":true}'
```

## JSON import with update operation

When JSON data includes `"operation":"update"`, provide an auth token.

```bash
make call TOOL=things_import_json ARGS_JSON='{"data":[{"type":"to-do","operation":"update","id":"TODO_ID","attributes":{"title":"Updated title"}}],"auth_token":"TOKEN"}'
```

## End-to-end JSON smoke test (safe)

This starts the server with `THINGS_MCP_DRY_RUN=1`, then runs create and update JSON calls through MCP CLI without launching `things:///` URLs.

```bash
make smoke-json
```

## Read operations via AppleScript

Requires macOS Automation permission for Terminal/Codex to control Things.
```bash
make call TOOL=things_read_todos ARGS_JSON='{"list_id":"today","limit":20}'
make call TOOL=things_find_todos ARGS_JSON='{"query":"invoice","limit":10}'
make call TOOL=things_read_todo ARGS_JSON='{"todo_id":"TODO_ID"}'
make call TOOL=things_read_todos ARGS_JSON='{"list_id":"anytime","status":"open","project_id":"PROJECT_ID","include_notes":true,"limit":50}'
make call TOOL=things_read_todos ARGS_JSON='{"list_id":"today","deadline_before":"2026-03-31","completed_after":"2026-03-01"}'
make call TOOL=things_read_projects ARGS_JSON='{"status":"open","area_id":"AREA_ID","include_notes":true,"limit":20}'
make call TOOL=things_read_areas
make call TOOL=things_read_headings ARGS_JSON='{"project_id":"PROJECT_ID","query":"plan","limit":20}'
```

`status` filter must be one of: `open`, `completed`, `canceled`.
Date filters must be ISO-8601 (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`).

Read smoke test:

```bash
make smoke-read
```
