# MCP Sequence

## Mutation-safe sequence

1. `things_capabilities`
2. `things_auth_get_status`
3. `things_validate_token_config` (before update/delete)
4. `things_find_todos` (`status="open"`)
5. Optional fallback: `things_read_todos` (`status="open"`, `include_notes=true`)
6. Mutation:
   - `things_update_todo` for correction/reschedule
   - `things_add_todo` for new tasks

## Failure handling

- Missing token for update path: report blocker and stop.
- Multiple matches: ask user to disambiguate.
- Ambiguous relative date: resolve with explicit local date and confirm before mutation.
