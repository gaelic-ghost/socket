---
name: operate-acp-agent-integration
description: Install, launch, validate, and diagnose existing ACP agents across Zed, Xcode, and other clients. Use for registry discovery, custom launch commands, auth, capabilities, sessions, and logs.
metadata:
  hermes:
    category: agent-portability
    tags: [acp, zed, xcode, hermes, diagnostics]
---

# Operate ACP Agent Integration

Operate an existing ACP agent without confusing client setup, agent-native
configuration, and protocol behavior. Read `references/acp-operations-map.md`
for the current connection and failure map.

## Preflight

1. Name the ACP client and ACP agent/server process.
2. Check the current stable protocol version and the capabilities negotiated by
   the actual pair; do not infer wire compatibility from SDK package versions.
3. Check the canonical ACP Registry with
   `scripts/check_acp_registry.py <agent-id>`.
4. If the agent is missing, use its official local executable only when the
   client supports custom agents. Keep registry absence distinct from missing
   ACP support.
5. Run the agent's documented non-interactive health or version check before
   opening the client.

For Hermes, check `hermes acp --version`, `hermes acp --check`, `hermes doctor`,
and `hermes status` as needed. ACP reuses Hermes provider credentials, config,
skills, and state; it does not create a separate provider setup.

## Connect And Validate

1. Configure the client launch command and environment with the smallest
   required surface.
2. Confirm stdout is reserved for JSON-RPC and human-readable logs go to
   stderr.
3. Inspect the initialization response for protocol version, agent
   capabilities, authentication methods, and implementation identity.
4. Complete agent-owned or terminal authentication before starting a session.
5. Create a harmless session and verify working-directory binding.
6. Verify streaming messages, tool calls, file diffs, terminal rendering,
   permission requests, cancellation, and any advertised load, resume, fork,
   list, delete, mode, or config-option behavior independently.
7. Verify forwarded MCP servers separately from the agent's native MCP config.

## Host Handoffs

- For Zed registry/custom-agent settings and ACP logs, use `operate-zed-agent`.
- For Xcode's Add an Agent flow, Xcode-owned tools, and permissions, use
  `apple-dev-skills:xcode-coding-intelligence-workflow`.
- For an external agent running outside Xcode and calling Xcode tools, stop:
  that is MCP through `xcrun mcpbridge`, not an ACP-hosted Xcode agent.
- For a custom program driving Hermes, reconsider the TUI gateway or API server
  through `choose-agent-integration-protocol`.

## Diagnose By Layer

- Discovery failure: inspect the canonical registry or custom client config.
- Spawn failure: inspect executable path, arguments, environment, and stderr.
- Handshake failure: inspect protocol version and capabilities.
- Authentication failure: inspect advertised auth methods and agent-native
  provider state.
- Empty or wrong workspace: inspect session cwd and additional roots.
- Missing tool: inspect client-forwarded MCP and agent-native MCP separately.
- Missing history: inspect whether load, resume, list, or fork is advertised;
  do not assume every client exposes every optional method.

## Report

Report registry status, launch source, client and agent versions, negotiated
protocol and capabilities, auth owner, cwd, session behavior, MCP paths,
permission behavior, evidence collected, and unresolved client-specific UI
checks.
