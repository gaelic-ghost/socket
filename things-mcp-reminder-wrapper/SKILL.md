---
name: things-mcp-reminder-wrapper
description: Manage Things reminders and todo creation/update with a deterministic MCP workflow that prevents duplicate tasks and date mistakes. Use when a user asks to add, reschedule, or correct a Things task/reminder, especially when requests include relative dates like "tomorrow" or when an existing task might need to be updated instead of duplicated.
---

# Things MCP Reminder Wrapper

## Overview

Use a strict update-first workflow for Things reminder requests. Resolve relative dates in the user's local timezone, check auth/token state before updates, and avoid creating duplicates unless the user explicitly asks for duplicates.

## Workflow

1. Resolve local date anchor first.
   - Run `date '+%Y-%m-%d %H:%M:%S %Z %z'`.
   - Use `America/New_York` unless the user provides a different timezone.
2. Check Things MCP readiness before mutations.
   - Run `things_capabilities`.
   - Run `things_auth_get_status`.
   - If update/delete may be needed, run `things_validate_token_config`.
3. Normalize scheduling terms to explicit dates.
   - Convert relative terms like `today`, `tomorrow`, `next Monday` into absolute dates.
   - Always confirm with absolute wording in the final output, for example: `Monday, March 2, 2026 at 9:30 AM (America/New_York)`.
4. Search for existing matching tasks before creating new ones.
   - Run `things_find_todos` with `status="open"` and a focused query.
   - If search is insufficient, run `things_read_todos` (`status="open"`, `include_notes=true`) and match title/notes.
5. Choose mutation path with duplicate protection.
   - If clear single match and user intent is correction/reschedule: update existing task.
   - If no match: create a new task.
   - If multiple likely matches: ask which task to update; do not guess.
6. Enforce auth safety rules.
   - If update is required but token is unavailable, stop and report the exact missing auth state.
   - Do not create a replacement duplicate as fallback unless the user explicitly requests that behavior.
7. Execute mutation.
   - Create: `things_add_todo`.
   - Update: `things_update_todo`.
8. Report deterministic result.
   - State whether the action was `created` or `updated`.
   - Include task title and normalized schedule in absolute form.
   - If blocked, provide exact blocker and next action.

## Guardrails

- Never assume relative dates without resolving current local date first.
- Never claim an update succeeded without tool confirmation.
- Never silently create duplicates when update intent is clear.
- Never hide auth errors; surface them with source (`env` vs `keychain` vs none).

## Customization Workflow

When asked to customize behavior:

1. Read `config/customization.yaml`; if missing, read `config/customization.template.yaml`.
2. Confirm preferences for:
   - timezone
   - default reminder time
   - duplicate policy
   - token-missing behavior for update requests
3. Propose 2-3 option bundles with one recommended default.
4. Write `config/customization.yaml` with `schemaVersion: 1`, `isCustomized: true`, and selected profile.
5. Validate by simulating one create flow and one update flow, then summarize behavior deltas.

## Customization Reference

- Schema and allowed values: `references/config-schema.md`
- Behavior knobs and examples: `references/customization.md`

## Automation Templates

Use `$things-mcp-reminder-wrapper` in automation prompts for reliable reminder handling behavior.

For Codex App and Codex CLI templates, use:
- `references/automation-prompts.md`

## References

- MCP sequence and failure handling: `references/mcp-sequence.md`
- Automation prompt templates: `references/automation-prompts.md`
- Customization guide: `references/customization.md`
- Customization schema: `references/config-schema.md`
