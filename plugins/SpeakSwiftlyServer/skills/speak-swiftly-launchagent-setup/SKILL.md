---
name: speak-swiftly-launchagent-setup
description: Use when a user wants to install, refresh, promote, inspect, validate, troubleshoot, or remove the per-user SpeakSwiftlyServer LaunchAgent on their machine. This skill covers the supported launch-agent CLI workflow, required config-file checks, staged-artifact expectations, and end-to-end HTTP plus MCP health verification.
---

# SpeakSwiftly LaunchAgent Setup

Use this skill when the user wants the standalone `SpeakSwiftlyServer` to run as a per-user background service managed by `launchd`.

## Start Here

- Use the supported `SpeakSwiftlyServerTool launch-agent ...` commands instead of hand-editing property lists or calling `launchctl` directly.
- Read the repo operator guidance in [README.md](../../README.md) first, then [LaunchAgent-Workflow.md](../../Sources/SpeakSwiftlyServer/SpeakSwiftlyServer.docc/Articles/LaunchAgent-Workflow.md) when the user needs the full setup model.
- If the user is asking about Codex access to the running service, remember that the plugin points at [`.mcp.json`](../../.mcp.json), which expects the live MCP endpoint at `http://127.0.0.1:7337/mcp`.

## Normal Setup Flow

1. Print the property list first with `xcrun swift run SpeakSwiftlyServerTool launch-agent print-plist`.
2. Confirm the config file the service should use. The standard live-service path is `~/Library/Application Support/SpeakSwiftlyServer/server.yaml` unless the user explicitly wants another file.
3. If the staged live artifact is already the intended executable, run `xcrun swift run SpeakSwiftlyServerTool launch-agent install --config-file /absolute/path/to/server.yaml`.
4. If the user wants the current checkout to become the live service now, run `xcrun swift run SpeakSwiftlyServerTool launch-agent promote-live --config-file /absolute/path/to/server.yaml`.
5. Verify the result with `xcrun swift run SpeakSwiftlyServerTool healthcheck`.

## When To Use Each Command

- `launch-agent print-plist`:
  Use before install work or when the user wants to inspect exactly what will be staged into `~/Library/LaunchAgents`.
- `launch-agent install --config-file ...`:
  Use when the staged release artifact under `.release-artifacts/current` is already the executable the user wants `launchd` to boot.
- `launch-agent promote-live --config-file ...`:
  Use when the intent is "make this checkout become the live service now." This rebuilds and stages the release artifact first, then refreshes the LaunchAgent install.
- `launch-agent status`:
  Use when the user wants to inspect the installed state, label, plist location, or staged executable details.
- `launch-agent uninstall`:
  Use when the user explicitly wants the per-user background service removed.
- `healthcheck`:
  Use after install, promotion, config changes, or troubleshooting. It is the supported end-to-end probe for both HTTP and MCP.

## Validation And Troubleshooting

- Treat `healthcheck` as the primary verification path because it probes `GET /healthz`, reads `GET /runtime/host`, and sends a real MCP `initialize` request to `/mcp`.
- If the HTTP process is healthy but Codex still cannot use the MCP surface, check whether MCP is enabled in the server config or environment. The MCP endpoint exists only when `APP_MCP_ENABLED=true` or the config file enables MCP.
- If the user wants to understand whether the live background service is using the staged artifact or a different executable, rely on `launch-agent status`, install output, and the printed plist rather than inferring from filesystem timestamps alone.
- If the user needs queue, playback, or backend control after the service is already installed, switch to `$speak-swiftly-runtime-operator` instead of stretching this skill into runtime operations.
- If the question is about using the live MCP surface from Codex after setup, switch to `$speak-swiftly-mcp`.
