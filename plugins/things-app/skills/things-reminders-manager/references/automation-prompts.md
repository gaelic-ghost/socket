# Automation Prompt Templates

## Codex App Template

Use [$things-reminders-manager](/Users/galew/Workspace/things-app/skills/things-reminders-manager/SKILL.md).

Process reminder requests for Things using one settings-driven workflow:
1. Resolve current local date/time.
2. Load effective settings (`timezone`, `defaultReminderTime`, `duplicatePolicy`, `onUpdateWithoutToken`, `requireAbsoluteDateInConfirmation`).
3. Verify Things auth status before any update path.
4. Normalize the requested schedule using the effective timezone and default reminder time when needed.
5. Search existing open tasks and apply `duplicatePolicy`.
6. If update auth is missing, apply `onUpdateWithoutToken`.
7. Return `created`, `updated`, or `blocked` with absolute date/time confirmation when required.

## Codex CLI Template

Use `$things-reminders-manager` and follow the same workflow.
Return: action taken (`created|updated|blocked`), task title, absolute schedule, and blockers if any.
