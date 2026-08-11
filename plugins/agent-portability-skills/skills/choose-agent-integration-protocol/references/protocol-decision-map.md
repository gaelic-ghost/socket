# Agent Integration Protocol Decision Map

| Desired behavior | Primary boundary | Process roles |
| --- | --- | --- |
| Let independently operated agents discover and delegate to each other | A2A | One agent is the A2A client; the peer exposes an Agent Card and A2A server |
| Run Hermes, Codex, Claude, or another agent inside Zed/Xcode UI | ACP | Editor is client; agent executable is server |
| Let an external agent call Xcode build, project, preview, or runtime tools | MCP through `xcrun mcpbridge` | Agent is MCP client; Xcode provides tools |
| Give an agent external service tools | MCP | Agent is client; service is server |
| Use Zed-owned models, profiles, instructions, skills, and tools | Zed Agent | Zed owns the agent loop and configuration |
| Preserve an agent's original terminal interface | Terminal Thread | Zed hosts a terminal; CLI/TUI owns behavior |
| Drive Hermes from a custom rich client | Hermes TUI gateway | Custom host speaks Hermes JSON-RPC |
| Drive Hermes from a web or language-neutral client | Hermes API server | Client uses HTTP and streaming responses |
| Add host-only runtime behavior | Native plug-in or extension | Host owns discovery and lifecycle |

## Direction Checks

- “Hermes in Zed” normally means Zed launches `hermes acp`.
- “Hermes in Xcode” normally means Xcode adds Hermes as an ACP agent.
- “Codex uses Xcode” normally means Codex connects to `xcrun mcpbridge` as an
  MCP client unless Codex itself was launched by Xcode.
- “Program calls Hermes” requires ACP only when the program is an ACP client;
  otherwise compare the TUI gateway and API server.

## Multi-Protocol Cases

An ACP client can pass MCP server configuration to an ACP agent. This combines
an editor-to-agent ACP connection with agent-to-tool MCP connections; it does
not merge the protocols or their security boundaries.

An A2A-connected peer can internally use MCP tools or appear inside an ACP
client. Those remain three distinct trust, lifecycle, and permission boundaries.

Official references:

- https://agentclientprotocol.com/get-started/architecture
- https://a2a-protocol.org/latest/topics/what-is-a2a/
- https://agentclientprotocol.com/protocol/v1/overview
- https://developer.apple.com/documentation/xcode/setting-up-coding-intelligence
- https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode
- https://zed.dev/docs/ai/agents
- https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration
