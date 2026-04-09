# Things URL Route Matrix

This matrix tracks route coverage for the local Things MCP server.

| URL command | MCP tool | Status | Key params | Auth token required | Callback expected |
| --- | --- | --- | --- | --- | --- |
| `add` | `things_add_todo` | Implemented | `title`, `notes`, `when`, `deadline`, `tags`, `list-id`, `reveal` | No | No |
| `add-project` | `things_add_project` | Implemented | `title`, `notes`, `when`, `deadline`, `tags`, `area`, `area-id`, `completed`, `canceled`, `reveal` | No | No |
| `update` (to-do scope) | `things_update_todo` | Implemented | `id` + update fields | Yes | No |
| `show` | `things_show` | Implemented | `id` or `query`, optional `filter` | No | No |
| `search` | `things_search` | Implemented | `query` | No | No |
| `version` | `things_version` | Implemented | none | No | Yes |
| `update-project` | `things_update_project` | Implemented | `id` + project update fields | Yes | No |
| `json` | `things_import_json` | Implemented | `data`, optional `auth-token`, `reveal` | Required when payload contains `update` operations | No |

Notes:

- `things_show` requires at least one of `id` or `query`.
- `things_update_todo` resolves auth token in order: explicit `auth_token`, `THINGS_AUTH_TOKEN`, keychain.
- `things_version` uses `x-success`/`x-error` callback URLs.

## AppleScript Read Tools

| MCP tool | Backend | Status | Key params | Notes |
| --- | --- | --- | --- | --- |
| `things_read_todos` | AppleScript (`osascript`) | Implemented | `list_id`, `limit`, `offset`, `status`, `project_id`, `area_id`, `deadline_before`, `deadline_after`, `completed_before`, `completed_after`, `include_notes` | Supported lists: `inbox`, `today`, `anytime`, `upcoming`, `someday`, `logbook`, `all` |
| `things_read_todo` | AppleScript (`osascript`) | Implemented | `todo_id`, `include_notes` | Fetches by Things item ID |
| `things_find_todos` | AppleScript (`osascript`) | Implemented | `query`, `limit`, `offset`, `status`, `project_id`, `area_id`, `deadline_before`, `deadline_after`, `completed_before`, `completed_after`, `include_notes` | Title text matching with filters |
| `things_read_projects` | AppleScript (`osascript`) | Implemented | `limit`, `offset`, `status`, `area_id`, `deadline_before`, `deadline_after`, `completed_before`, `completed_after`, `include_notes` | Includes project metadata and notes (optional) |
| `things_read_areas` | AppleScript (`osascript`) | Implemented | none | Returns area `id` and `title` |
| `things_read_headings` | AppleScript (`osascript`) | Implemented | `limit`, `offset`, `project_id`, `query` | Returns heading `id`, `title`, `project_id`, and `project_title` |
