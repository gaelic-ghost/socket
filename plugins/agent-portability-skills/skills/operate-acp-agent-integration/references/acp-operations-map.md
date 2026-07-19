# ACP Operations Map

## Connection Lifecycle

1. Client launches the agent process, normally over stdio.
2. Client sends `initialize` with protocol version and client capabilities.
3. Agent returns the negotiated version, capabilities, implementation info,
   and authentication methods.
4. Client completes authentication when required.
5. Client creates, loads, or resumes a session with cwd and MCP servers.
6. Client sends prompts; agent streams updates and tool activity.
7. Client and agent handle reverse requests such as permissions, filesystem, or
   terminal operations only when supported.
8. Client cancels or closes sessions and terminates the process cleanly.

## Evidence Layers

| Layer | Useful evidence |
| --- | --- |
| Distribution | Canonical registry JSON or official executable/package |
| Process | Exit status and stderr diagnostics |
| Handshake | Negotiated protocol, capabilities, auth methods, agent info |
| Session | cwd, ID, supported load/resume/list/fork operations |
| Rendering | streamed text, tool calls, diffs, plans, terminal output |
| Safety | permission requests, timeout behavior, cancellation |
| Tools | client-forwarded MCP versus agent-native MCP inventories |

## Hermes Today

Hermes' source repository ships `acp_registry/agent.json`, but a source manifest
is not a published registry entry. Check the live registry every time. When the
entry is absent, an official custom launch can use:

```json
{
  "agent_servers": {
    "hermes-agent": {
      "type": "custom",
      "command": "hermes",
      "args": ["acp"]
    }
  }
}
```

Official references:

- https://agentclientprotocol.com/protocol/v1/initialization
- https://agentclientprotocol.com/protocol/v1/session-setup
- https://agentclientprotocol.com/protocol/v1/authentication
- https://agentclientprotocol.com/get-started/registry
- https://hermes-agent.nousresearch.com/docs/user-guide/features/acp
- https://zed.dev/docs/ai/external-agents
