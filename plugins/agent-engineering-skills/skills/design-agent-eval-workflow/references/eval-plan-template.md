# Agent Eval Plan Template

Use this template when the user wants a reusable prompt, issue body, project
note, or implementation brief.

````markdown
# Agent Eval Plan

## Recommendation

Eval surface: `<local-script|pytest|codex-exec|codex-github-action|agents-sdk-eval|langgraph-eval|stack-owned-runner>`

Automation target: `<full-auto|auto-with-escalation|human-review|manual-only-for-now>`

Why this shape:
- `<one sentence tied to risk, validation confidence, state, traceability, or runtime ownership>`

## Behavior Under Test

- Workflow:
- Real decision this eval supports:
- Surfaces touched:
- Known failure modes:

## Case Set

- Happy path:
- Messy realistic input:
- Past regression:
- Boundary or refusal case:
- Tool/filesystem/network/credential case:
- Full-auto eligibility case:

## Graders

- Deterministic assertions:
- Model-graded rubric:
- Snapshot checks:
- Trace or event checks:
- Human audit sample:

## Safety Gates

- Full-auto pass criteria:
- Escalation triggers:
- Stop condition:
- Rollback or no-op behavior:
- Secret and private-data handling:

## Run Cadence

- Local:
- CI or release:
- Scheduled:
- Post-change:

## Scaffold

Case schema:

```json
{
  "id": "<stable-case-id>",
  "prompt": "<input>",
  "expected_behavior": "<observable outcome>",
  "forbidden_behavior": ["<unsafe or incorrect behavior>"],
  "grader": "<deterministic|model|snapshot|trace>",
  "automation_target": "<full-auto|auto-with-escalation|human-review|manual-only-for-now>"
}
```

Runner outline:

```text
<runner, command, or service outline here>
```

## Handoff

- Owning skill/plugin/docs:
- Files or services likely to change:
- Work that should stay out of this first pass:

## Sources

- `<official docs link>`
````
