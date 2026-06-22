# MCP Bridge And External Agents

Last checked with local `xcrun mcpbridge --help` from Xcode 26.5 on 2026-06-22.

## What `xcrun mcpbridge` Does

`xcrun mcpbridge` is Xcode's STDIO bridge for Xcode MCP tools. Without a subcommand, it reads JSON-RPC 2.0 messages from stdin and forwards responses to stdout.

Use this shape when configuring an external MCP client:

```bash
codex mcp add xcode -- xcrun mcpbridge
```

The exact client command can differ by agent, but the Xcode side is the same bridge command.

## Xcode Process Selection

`mcpbridge` can auto-detect a running Xcode process. Its help describes this fallback order:

1. Use the only running Xcode process when exactly one exists.
2. If multiple Xcode processes exist, use `xcode-select` to determine which Xcode is selected.
3. If no Xcode process exists, exit with an error.

When multiple Xcode windows or versions make auto-detection ambiguous, set `MCP_XCODE_PID` intentionally:

```bash
MCP_XCODE_PID=12345 xcrun mcpbridge
```

`MCP_XCODE_SESSION_ID` can identify an Xcode tool session when a session id is already known.

## Launching Agents With Xcode Configuration

`xcrun mcpbridge run-agent <agent-name>` launches a coding agent with Xcode-provided configuration. The local help says it connects to a running Xcode to fetch the agent binary path, auth tokens, environment, and settings, then execs the agent with terminal access.

Useful inspection command:

```bash
xcrun mcpbridge run-agent --dry-run <agent-name>
```

Use `--no-xcode-tools` only when intentionally launching the agent with Xcode-provided configuration but without Xcode MCP tools in the agent config.

## Preconditions

Before expecting Xcode tools to work through an external agent:

- Xcode must be running.
- The relevant project or workspace should be open in Xcode.
- External-agent access must be enabled in Xcode's Intelligence settings.
- The agent or client must be configured to start `xcrun mcpbridge`.
- The requested tool permission must be allowed by Xcode and by the external client.

## Failure Language

Use concrete setup errors. Prefer messages like:

- "Xcode MCP setup is blocked because no Xcode process is running. Open the target project in Xcode, then retry the MCP bridge."
- "Xcode MCP setup is ambiguous because multiple Xcode processes are running. Set MCP_XCODE_PID to the intended Xcode process id before retrying."
- "External-agent Xcode access is not ready because Xcode Intelligence settings have not allowed external agents."
