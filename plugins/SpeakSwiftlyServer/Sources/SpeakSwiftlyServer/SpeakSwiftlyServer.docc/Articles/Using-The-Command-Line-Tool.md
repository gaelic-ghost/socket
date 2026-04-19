# Using The Command-Line Tool

## Overview

Use the standalone `SpeakSwiftlyServerTool` executable when the server should be owned by an operator workflow instead of by an app process.

This is the right lane when you need to:

- start the shared host directly from a terminal
- inspect the command surface before installing anything
- render or manage the LaunchAgent property list

Stay in the library-first docs when an app owns the process through ``EmbeddedServer``. Switch to this article when the executable itself becomes the thing you are operating.

## Start With The Help Surface

The shortest safe operator entrypoint is the tool's help command:

```bash
xcrun swift run SpeakSwiftlyServerTool help
```

That output shows the two top-level roles the executable currently serves:

- `serve` starts the shared host in the foreground
- `launch-agent` renders, installs, promotes, inspects, or removes the per-user LaunchAgent property list

Running the executable without arguments defaults to `serve`, but the help output is the clearer first stop when you are orienting yourself or checking what a staged release currently exposes.

## Know The Two Execution Modes

### Foreground Server

Use the foreground entrypoint when you want the process attached to the current shell:

```bash
xcrun swift run SpeakSwiftlyServerTool serve
```

This is the simplest path for local operator checks, debugging, and temporary runs where you do not want launchd to own the process lifecycle. The foreground executable defaults to `127.0.0.1:7338` unless environment or YAML config overrides that port.

If the foreground run should own a specific runtime persistence root, pass `--profile-root`:

```bash
xcrun swift run SpeakSwiftlyServerTool serve \
  --profile-root ./runtime/profiles
```

That flag feeds the same `SPEAKSWIFTLY_PROFILE_ROOT` startup override the LaunchAgent and embedded-app paths use, so the foreground server can point its runtime configuration, text-profile persistence, and generated artifacts at one explicit root.

### LaunchAgent Maintenance

Use the `launch-agent` subcommands when the server should become a user-owned background service:

```bash
xcrun swift run SpeakSwiftlyServerTool launch-agent print-plist
```

That subcommand renders the property list the package would install, including the staged executable path, working directory, profile-root environment, and stdout and stderr log paths. The LaunchAgent-owned runtime keeps its own default port, `127.0.0.1:7337`, so the live background service does not have to collide with an ad hoc foreground shell session by default.

For the install, promotion, status, and uninstall flow, continue with <doc:LaunchAgent-Workflow>.

## Know When To Leave DocC

This companion article is intentionally small. It explains where the executable fits, not every transport payload or maintenance edge case.

For the full operator contract:

- use <doc:Operator-Surfaces> when you need the relationship between the executable, HTTP, and MCP
- use the repository `README.md` and `API.md` when you need the route inventory, exact request and response payloads, or the fuller LaunchAgent command reference
