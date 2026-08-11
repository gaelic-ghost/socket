# A2A Operations Map

## Protocol Roles

| Concern | Owner |
| --- | --- |
| Discovery | A2A server publishes an Agent Card; client verifies it |
| Authentication | Declared security scheme plus deployment-specific credential flow |
| Immediate response | Stateless `Message` |
| Long-running work | Stateful `Task` with status transitions and artifacts |
| Related exchanges | `contextId` |
| One work item | `taskId` |
| Live progress | Advertised streaming capability |
| Deferred delivery | Advertised push notifications with authenticated callback |

Canonical v1 discovery uses `/.well-known/agent-card.json`. Verify the card's
`protocolVersion`, preferred transport/binding, endpoint, capabilities,
security schemes, and skills instead of assuming that reachability proves
compatibility.

## Task Lifecycle

- Working: `submitted`, `working`
- Interrupted: `input-required`, `auth-required`
- Terminal: `completed`, `canceled`, `rejected`, `failed`

An interrupted task needs a deliberate client response. A terminal task must
not silently resume under the same `taskId`.

## Hermes 0.20 Surface

Hermes ships an A2A v1 JSON-RPC platform in both directions:

- inbound Agent Card and task server through the messaging gateway;
- outbound discovery, call, list, history, and orchestration tools through the
  optional `a2a` toolset;
- persisted conversations keyed by `contextId`;
- bearer/per-peer authentication, trusted-peer controls, audit records,
  anti-loop limits, outbound redaction, and signed push callbacks.

Use current Hermes documentation and the installed plugin help before naming
configuration keys because this surface is newer than the core A2A protocol.

## Official Sources

- https://a2a-protocol.org/latest/topics/agent-discovery/
- https://a2a-protocol.org/latest/topics/life-of-a-task/
- https://github.com/a2aproject/A2A/blob/main/docs/specification.md
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a
