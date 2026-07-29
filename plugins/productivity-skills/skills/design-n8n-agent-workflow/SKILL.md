---
name: design-n8n-agent-workflow
description: Design safe n8n workflows with deterministic routing, credentials, idempotency, recovery, local-model checks, drafts, and exact approval gates.
---

# Design n8n Agent Workflow

Use this skill when n8n is the right visual, trigger-driven integration surface.
It does not turn n8n into a default durable multi-agent runtime.

## Source Check

- n8n hosting: <https://docs.n8n.io/hosting/>
- n8n and Ollama: <https://n8n.io/integrations/ollama/>
- Ollama: <https://ollama.com/>

## Workflow

1. Map trigger, deterministic transforms/routes, external reads, model step,
   draft output, and any external write separately.
2. Select credentials/storage ownership, webhook exposure, retry policy,
   idempotency key, concurrency limit, and failed-run record before connecting
   an AI node.
3. Treat the local model as one bounded node: prove structured output, tool
   compatibility when used, no-call behavior, malformed result recovery, and
   the exact model/server combination before exposing a write node.
4. Keep source data minimised and trace/log retention explicit. Do not put
   secrets in workflow exports or prompts.
5. Leave write nodes disabled or draft-only until `auto-with-escalation` names
   the recipient, action, payload evidence, and approval event.
6. Export a testable workflow fixture and verify happy path, duplicate event,
   failed model response, credential failure, rejected approval, and recovery.

## Output Shape

Return trigger, node graph, credentials, idempotency/retry behavior, model
contract, draft artifact, approval event, and recovery evidence.

## Guardrails

- Prefer deterministic n8n nodes over agent planning whenever the route is
  known.
- Do not expose a self-hosted instance publicly without an explicit deployment
  and authentication decision.
- Do not claim a local model is reliable for tool use without a capability gate.
