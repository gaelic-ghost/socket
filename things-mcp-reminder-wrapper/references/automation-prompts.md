# Automation Prompt Templates

## Codex App Template

Use [$things-mcp-reminder-wrapper](/Users/galew/Workspace/productivity-skills/things-mcp-reminder-wrapper/SKILL.md).

Process reminder requests for Things using update-first behavior:
1. Resolve local date/time in America/New_York.
2. Verify Things auth status before any update path.
3. Search existing open tasks and avoid duplicates.
4. Update existing task when intent is correction/reschedule.
5. Create new task only when no suitable match exists.
6. Return absolute date/time confirmations.

## Codex CLI Template

Use `$things-mcp-reminder-wrapper` and follow the same workflow.
Return: action taken (`created|updated|blocked`), task title, absolute schedule, and blockers if any.
