---
name: things-reminders-manager
description: Manage Things reminders and todo create/update requests with a deterministic MCP workflow that prevents duplicate tasks and date mistakes. Use when users ask to add, reschedule, or correct Things reminders, especially with relative dates or potential update-vs-create ambiguity.
---

# Things Reminders Manager

Use an update-first workflow for Things reminder requests.

## Workflow

1. Resolve the local date anchor first.
   - Run `date '+%Y-%m-%d %H:%M:%S %Z %z'`.
   - Default to `America/New_York` unless user specifies a different timezone.
2. Check Things MCP readiness.
   - Run `things_capabilities`.
   - Run `things_auth_get_status`.
   - If updates are likely, run `things_validate_token_config`.
3. Normalize relative scheduling terms into absolute dates.
4. Search for matching open tasks before creating new ones.
   - Prefer `things_find_todos` with focused query.
   - Fall back to `things_read_todos` when needed.
5. Choose mutation path with duplicate protection.
   - Single clear match and correction intent: update.
   - No match: create.
   - Multiple likely matches: ask user to disambiguate.
6. Enforce auth safety.
   - If update requires token and token is unavailable, stop and report exact blocker.
7. Execute mutation.
   - Create: `things_add_todo`
   - Update: `things_update_todo`
8. Report deterministic result.
   - action (`created` or `updated`)
   - task title
   - normalized absolute schedule

## Guardrails

- Never assume relative dates without resolving current local date.
- Never claim updates succeeded without tool confirmation.
- Never silently create duplicates when update intent is clear.
- Never hide auth source/status details.

## Customization Workflow

1. Read `config/customization.yaml`; if missing, read `config/customization.template.yaml`.
2. Confirm:
   - timezone
   - default reminder time
   - duplicate policy
   - token-missing behavior
3. Propose 2-3 option bundles with one recommended default.
4. Write `config/customization.yaml` with `schemaVersion: 1`, `isCustomized: true`, and profile.
5. Validate with one simulated create flow and one update flow.

## Automation Templates

Use `$things-reminders-manager` in automation prompts.

- `references/automation-prompts.md`

## References

- `references/mcp-sequence.md`
- `references/customization.md`
- `references/config-schema.md`
- `references/automation-prompts.md`
