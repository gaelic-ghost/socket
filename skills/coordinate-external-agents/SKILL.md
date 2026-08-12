---
name: coordinate-external-agents
description: Coordinate independently operated external agents through durable handoffs. Use when work crosses hosts, sessions, accounts, services, queues, boards, pull requests, or human-owned task systems and cannot rely on an in-run subagent result.
---

# Coordinate External Agents

Treat an external agent as an independently operated worker, not as a magical
subagent. Starting it is not progress unless the coordinator can later discover
its state and consume its report.

## Workflow

1. Choose a durable shared surface: task record, issue, pull request, branch,
   worktree, artifact directory, shared document, queue, or host-native board.
2. Create a task record with the normal launch envelope plus access, retention,
   retry/resume, and result-delivery details.
3. Assign one owner, one coordinator, one artifact/write surface, and one final
   verification owner. Do not assume direct worker-to-worker messages exist.
4. Record status using `queued`, `running`, `blocked`, `needs-decision`,
   `completed`, `failed`, or `cancelled`; use the selected host's closest
   equivalent without hiding meaning.
5. Require a final report on the durable surface and notify the coordinator
   through the specified return route.
6. Verify the returned artifact, branch, change, or evidence before treating
   the task as complete.

## Durable Work Rule

Use a queue, board, scheduled task, CI workflow, or service for work that must
survive session closure, restart, human input, retry, multiple roles, or later
audit. Do not represent a transient child-agent call as durable work.

## Boundaries

- Keep credentials, private context, and mutation authority scoped to the
  external worker's actual access surface.
- Use host-specific adapters only for mechanics. This skill owns the universal
  handoff contract; it does not claim Codex, ChatGPT Work, Hermes, or another
  host shares one message or task API.
