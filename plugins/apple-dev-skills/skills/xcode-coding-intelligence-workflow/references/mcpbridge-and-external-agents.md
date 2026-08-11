# MCP Bridge And External Agents

Last checked against Apple documentation and local Xcode 27.0 Beta 5 build
27A5237l on 2026-08-10.

## What `xcrun mcpbridge` Does

`xcrun mcpbridge` is Xcode's STDIO bridge for Xcode MCP tools. Without a subcommand, it reads JSON-RPC 2.0 messages from stdin and forwards responses to stdout.

Use this shape when configuring an external MCP client:

```bash
codex mcp add xcode -- xcrun mcpbridge
```

The exact client command can differ by agent, but the Xcode side is the same bridge command.

## Headless Service Versus Live Xcode

Xcode 27 Beta 5 previews `xcrun mcp-server`, a headless Xcode MCP service that
does not require an open Xcode workspace. Inspect it with:

```bash
xcrun mcp-server status
```

The selected Xcode toolchain must provide `mcp-server`; a stable toolchain may
still resolve `mcpbridge` while lacking the Beta 5 management command. Change
the selected toolchain only through the approved Xcode Settings > Locations
workflow.

Classify requests before starting anything:

- Workspace-independent: documentation and other tools that the headless
  service exposes without a project.
- Headless project: start the service and use `xcrun mcp-server open <project>`
  after the agent and folder have been approved.
- Live Xcode: editor selection, previews, active run/debug state, Intelligence
  settings, and plug-in UI.

Use `start` and `stop` for an intentional headless service lifecycle. Do not
leave a diagnostic service running when it was stopped before the check.

## Live Process Selection

When using a live Xcode process, `mcpbridge` can auto-detect it. If multiple
Xcode processes make selection ambiguous, set `MCP_XCODE_PID` intentionally:

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

## Plug-in Import Is Not A Bridge Subcommand

Use Xcode Settings > Intelligence > Plug-ins for official plug-in imports. The local Xcode 27 beta UI can import from installed Codex state, a local folder, and a remote Git URL.

Do not describe plug-in installation as an `mcpbridge` subcommand. `mcpbridge run-agent <agent-name>` launches an agent with Xcode-provided configuration; it does not install Xcode plug-ins by itself.

## Preconditions

Before expecting Xcode tools to work through an external agent:

- External-agent access must be enabled in Xcode's Intelligence settings.
- Headless mode must be enabled for no-UI operation; otherwise Xcode must be
  running.
- A project-dependent tool needs the relevant project opened by the headless
  service or live Xcode. Documentation lookup does not inherently need one.
- Xcode must approve the actual agent executable and any requested folder tree.
- The agent or client must be configured to start `xcrun mcpbridge`.
- The requested tool permission must be allowed by Xcode and by the external client.
- Plug-in import probes should use a harmless fixture or a trusted Git URL first, and should stop before importing additional plug-ins unless the user asked to mutate Xcode state.

Do not treat a non-running Xcode instance as a final blocker by itself. Inspect
headless status and requested tool scope first. If the task needs live editor,
run/debug, Intelligence settings, or plug-in UI state, open the intended app and
retry. To change the CLI toolchain, use Settings > Locations > Command Line
Tools in that app and let macOS obtain Touch ID or administrator approval;
verify with `xcode-select -p`; do not override it with `DEVELOPER_DIR`.

## Permission Identity

Headless enablement does not grant every process or folder access. Xcode can
prompt separately for the connecting executable and directory tree, with
bounded or persistent durations. Verify the displayed client name and the
recorded executable identity: a diagnostic Python process, shell, or package
runner may be authorized instead of Hermes, Codex, or Claude.

Apple documents `sudo xcrun mcp-server enable
--unsafe-always-allow-all-agents` for unattended environments only and says it
is not recommended for at-desk use. Do not recommend it as ordinary setup.

## Failure Language

Use concrete setup errors. Prefer messages like:

- "This tool needs live Xcode editor or run/debug state; the headless service alone cannot provide that context."
- "The headless service is enabled, but Xcode has not approved this agent executable or project folder."
- "Xcode MCP setup is ambiguous because multiple Xcode processes are running. Set MCP_XCODE_PID to the intended Xcode process id before retrying."
- "External-agent Xcode access is not ready because Xcode Intelligence settings have not allowed external agents."
