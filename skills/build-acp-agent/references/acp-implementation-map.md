# ACP Implementation Map

## Stable Baseline

- Current stable wire protocol: ACP v1
- Required connection phase: `initialize`
- Required session behavior: new, prompt, cancel, and streamed update
- Optional behavior must be advertised through capabilities before use
- Default transport: JSON-RPC over process stdin/stdout
- Human diagnostics belong on stderr

## Official SDK Choices

- Rust: higher-level `agent-client-protocol` runtime crate
- Python: official ACP Python SDK
- TypeScript: official ACP TypeScript SDK
- Kotlin and Java: official ACP JVM libraries

Select by the agent's existing implementation language and deployment model.
Do not add another runtime solely to obtain a preferred SDK.

## Required Test Families

- protocol negotiation and unsupported versions
- capability omission and optional-method gating
- authentication discovery, success, failure, and logout when advertised
- new session, prompt, streaming updates, and cancellation
- cwd and additional-root isolation
- permission requests and fail-closed timeouts
- file diff, terminal, tool-call, and plan rendering
- process shutdown, malformed messages, and stderr/stdout separation
- published package launch on every declared platform
- custom-client development path and canonical registry path

## Publication States

1. ACP implemented in source
2. Fetchable package or binary published
3. Source-owned registry manifest updated to the same version
4. Canonical registry PR accepted
5. Live registry feed contains the entry
6. Representative clients install and run the published entry

Only states 5 and 6 support a claim that users can install the agent from the
registry.

Official references:

- https://agentclientprotocol.com/get-started/architecture
- https://agentclientprotocol.com/protocol/v1/initialization
- https://agentclientprotocol.com/protocol/v1/session-setup
- https://agentclientprotocol.com/protocol/v1/tool-calls
- https://agentclientprotocol.com/protocol/v1/terminals
- https://agentclientprotocol.com/libraries/python
- https://agentclientprotocol.com/libraries/typescript
- https://agentclientprotocol.com/libraries/rust
- https://agentclientprotocol.com/get-started/registry
