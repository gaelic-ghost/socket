---
name: choose-agent-integration-protocol
description: Choose ACP, MCP, a native host integration, a terminal thread, or a Hermes programmatic interface. Use when the direction of agent, editor, tool, or host control is unclear.
metadata:
  hermes:
    category: agent-portability
    tags: [acp, mcp, zed, xcode, hermes]
---

# Choose Agent Integration Protocol

Name the processes and the direction of control before selecting a protocol.
Do not use “connect the agents” or “hook into Xcode” as an architecture.

## Decision Workflow

1. Identify the process that owns the conversation UI.
2. Identify the process that owns the agent loop, model, credentials, tools, and
   persistent sessions.
3. Identify whether the other endpoint is an editor, a tool provider, another
   agent, a terminal, or a custom application.
4. Select one primary boundary:
   - Use ACP when an editor or compatible client launches and renders an
     external coding agent.
   - Use MCP when an agent calls tools or resources supplied by another
     process. An externally running agent uses Xcode through `xcrun mcpbridge`.
   - Use a native host agent when the host should own the model, instructions,
     skills, permissions, and tools.
   - Use a terminal thread when the original CLI or TUI experience is the
     requirement and editor-native diffs or approvals are unnecessary.
   - Use the Hermes TUI gateway or API server when a custom program drives
     Hermes directly and no ACP client owns the interaction.
   - Use a host plug-in only for capabilities that the host's documented
     skills, MCP, ACP, or configuration surfaces cannot provide.
5. Record authentication, working-directory, permission, session, and
   lifecycle ownership separately. A transport choice does not make those
   boundaries identical.

Read `references/protocol-decision-map.md` when the request spans more than one
host or appears to require multiple transports.

## Required Distinctions

- ACP makes an agent editor-native; it is not a general tool protocol.
- MCP gives an agent callable tools; it does not provide an editor conversation
  or review UI.
- Hermes running `hermes acp` is the ACP agent/server. Zed or Xcode is the ACP
  client that launches or connects to it.
- A Hermes provider that internally launches another ACP program is a
  provider-specific integration, not proof that Hermes is a universal ACP
  client or agent orchestrator.
- Xcode-hosted ACP and an external agent using Xcode MCP are different paths.

## Handoffs

- Hand existing ACP installation and diagnosis to
  `operate-acp-agent-integration`.
- Hand ACP server implementation and registry packaging to `build-acp-agent`.
- Hand Zed-native, Zed External Agent, and Terminal Thread choices to
  `operate-zed-agent`.
- Hand Xcode client setup and Xcode-owned permissions to
  `apple-dev-skills:xcode-coding-intelligence-workflow`.
- Hand Hermes-specific external-program implementation to
  `build-hermes-agent-extensions` after selecting ACP, TUI gateway, or API.

## Report

Return the chosen boundary, process roles, authentication owner, configuration
owner, permission owner, session owner, validation path, and any secondary
transport. State unresolved host support instead of inventing parity.
