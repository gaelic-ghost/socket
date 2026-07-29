---
name: orchestrate-agent-work
description: Coordinate bounded work across in-run subagents or worker tasks. Use before spawning, resuming, steering, cancelling, or closing workers when the coordinator needs a structured launch envelope, required report-back, escalation, and synthesis contract.
---

# Orchestrate Agent Work

Use this skill at the delegation boundary. The coordinator owns the user goal,
decomposition, authority, final decision, validation, and closure; workers own
only their assigned slice.

## Workflow

1. Confirm delegation is requested or required by the active workflow. Prefer a
   single agent when the work is sequential or one small write target.
2. Split only independent work. Assign one coordinator and one owner per
   artifact, worktree, branch, validation lane, and external side effect.
3. Give every worker a launch envelope:
   - task and coordinator identity;
   - objective, bounded scope, inputs, and source-of-truth locations;
   - allowed and forbidden actions, including write authority;
   - acceptance criteria, validation owner, and output location;
   - required terminal report and escalation conditions.
4. State whether the coordinator waits for all results, consumes partial
   reports, or hands work to a durable task surface.
5. Track each worker until it is `completed`, `blocked`, `needs-decision`,
   `cancelled`, or `failed`. A worker must not silently stop.
6. Acknowledge each result: consume it, request one bounded follow-up, mark it
   superseded, or cancel it explicitly. Then synthesize and verify the result
   in the coordinator thread.

## Worker Report Contract

Require the final report to contain the terminal state, outcome, evidence or
artifacts, validation run or intentionally skipped, uncertainty, and one
recommended next action. Workers escalate rather than improvise when scope,
authority, ownership, evidence, or acceptance criteria change.

## Boundaries

- Keep user-facing decisions, final edits, merge, release, and final validation
  with the coordinator unless a user-approved disjoint ownership plan says
  otherwise.
- Default to one delegation layer. Nested orchestration needs an explicit
  reason, bounded fan-out/depth, and host support.
- Use `coordinate-external-agents` when work crosses a host, session, or
  durable ownership boundary.
- Use `coordinate-worktrees-and-threads` when workers need repository state.
