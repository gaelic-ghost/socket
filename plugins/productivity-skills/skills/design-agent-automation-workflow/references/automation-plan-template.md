# Automation Plan Template

Use this template when the user wants a reusable prompt, implementation brief,
issue body, or handoff note.

````markdown
# Agent Automation Plan

## Recommendation

Chosen surface: `<codex-app-automation|codex-exec|codex-subagents|agents-sdk-service|langgraph-graph|hermes-workflow|full-auto|auto-with-escalation|no-automation-yet>`

Why this surface:
- `<one sentence tied to schedule, state, approvals, retries, observability, or runtime ownership>`

## Not Chosen

- Codex app automation: `<why not first, or "not applicable">`
- `codex exec` or Codex GitHub Action: `<why not first, or "not applicable">`
- Codex subagents: `<why not first, or "not applicable">`
- OpenAI Agents SDK service: `<why not first, or "not applicable">`
- LangGraph graph: `<why not first, or "not applicable">`
- Hermes-specific workflow: `<why not first, or "not applicable">`
- Full-auto execution: `<why yes/no, tied to validation and rollback confidence>`
- Auto-with-escalation: `<why yes/no, tied to exact escalation triggers>`
- No automation yet: `<why automation is justified, or why it is the recommendation>`

## State And Safety

- Trigger:
- Automation target:
- State that must persist:
- Read scope:
- Write scope:
- Secret or credential handling:
- Escalation or human approval gate:
- Retry policy:
- Rollback, no-op, or stop condition:

## Scaffold

First run:
- `<smallest useful run>`

Prompt, command, service outline, or graph outline:

```text
<scaffold here>
```

## Validation

- First-run check:
- Regression check:
- Artifact or report:
- Reviewer decision:

## Handoff

- Owning skill/plugin/docs:
- Files or services likely to change:
- Work that should stay out of this first pass:

## Sources

- `<official docs link>`
````
