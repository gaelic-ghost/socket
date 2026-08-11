# Hermes Gateway Surface Map

## Messaging Gateway

The messaging gateway is the long-running Hermes process that connects external messaging platforms, webhooks, and optional API surfaces to the agent runtime. It owns platform startup, authorization, inbound normalization, session routing, model/tool execution, and outbound delivery.

Use a dedicated Hermes profile when a bot identity, credential set, memory corpus, or authorization policy must be independent.

## Platform Adapter Responsibilities

A platform adapter should cover:

- configuration schema and secret handling;
- authentication and connection lifecycle;
- inbound message, command, attachment, and event normalization;
- stable session-key construction;
- authorized-user and authorized-space checks;
- outbound text, media, reply/thread, and error delivery;
- platform rate limits and retry behavior;
- startup, reconnect, and graceful shutdown;
- unit tests with fake platform clients and an opt-in live smoke test.

Use the specialized platform plugin API. A general plugin is the wrong owner for a new messaging transport.

## API And Webhook Surfaces

The Hermes API server exposes the agent loop through an OpenAI-compatible HTTP interface. It is distinct from the subscription proxy, which forwards provider requests without running the agent loop.

Webhooks accept external events that can trigger Hermes work. Authenticate senders, constrain routes, and decide whether each route may mutate systems or only create a queued prompt.

Outbound webhooks deliver Hermes events to another service. Give them a
separate signing secret, verify the receiver checks the signature before
parsing the payload, and define retry/idempotency behavior. Do not reuse an
inbound route token as proof of outbound authenticity.

The A2A platform also runs under the gateway, but it exposes peer-agent Agent
Cards and task lifecycles rather than a generic webhook contract. Use
`operate-a2a-agent-integration` for that boundary.

## Deployment Shapes

- Foreground local gateway for setup and smoke testing.
- Long-running single-profile service for one bot identity.
- Multiple profile gateways on one host, each with isolated tokens and state.
- Remote VM or container with messaging as the primary user interface.
- Hosted or serverless deployment using a supported backend and scheduler.

For public or unattended gateways, prefer isolated terminal execution, explicit allowlists, secret redaction, and service-level logs.

## Troubleshooting Evidence

Capture the profile, gateway process state, platform connection status, authorized sender identity class, session identifier, selected provider/model, toolset, and outbound delivery result. Redact tokens and message content unless the user needs it for diagnosis.

## Authoritative Sources

- [Messaging overview](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/index)
- [Gateway internals](https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals)
- [Adding a platform adapter](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters)
- [API server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server/)
- [Webhooks](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks)
- [A2A](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a)
- [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Running many gateways](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways)
- [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security/)
- [Cron internals](https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals)
