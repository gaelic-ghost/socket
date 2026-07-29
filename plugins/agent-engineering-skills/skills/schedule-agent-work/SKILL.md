---
name: schedule-agent-work
description: Choose and design one-shot, recurring, event-triggered, monitored, CI, background, queue, or board-based agent work. Use when agent work must run later, repeat, survive the current thread, or deliver results through an explicit route.
---

# Schedule Agent Work

Choose scheduling only after the work has a bounded input, write scope,
validation, escalation boundary, and result-delivery route.

## Choose The Smallest Durable Shape

- Use an in-run worker for a short dependency-free result the coordinator needs
  before continuing.
- Use a native scheduled task for periodic or trigger-based work where the host
  can show status and deliver a result to Gale.
- Use CI or `codex exec` for deterministic repository jobs with structured
  output and explicit sandboxing.
- Use a queue or board for retries, dependencies, multiple roles, durable
  comments, artifacts, or human decisions.
- Use an application service only when application code must own state, tools,
  approvals, tracing, and deployment.

## Required Schedule Contract

Define the trigger/cadence, owner, input snapshot, write authority, idempotency
or duplicate policy, timeout/retry limit, no-op/rollback behavior, escalation
trigger, status surface, artifact retention, and route that delivers the final
report to Gale and the coordinator.

## Guardrails

- Do not schedule unattended mutation without validation, recovery, and an
  exact escalation boundary.
- Do not use a timer or background process as a substitute for durable task
  state when a run must survive restarts or be picked up by another agent.
- Use `coordinate-external-agents` for cross-host work and
  `orchestrate-agent-work` for the coordinator/worker report contract.
