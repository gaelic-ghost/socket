# LaunchAgent Workflow

## Overview

Use the LaunchAgent workflow when the standalone server should run as a per-user background service managed by `launchd`.

In this package, that workflow is intentionally explicit:

1. render the property list you are about to install
2. either install the already-staged artifact or promote the current source checkout into the staged live artifact
3. inspect status or remove it later through the same executable surface
4. verify the live HTTP and MCP transports through one repo-owned health-check command

This article covers the shape of that workflow. It does not replace the repository operator docs, which remain the source of truth for the full command inventory and release-process details.

## Render The Property List First

Start by printing the property list:

```bash
xcrun swift run SpeakSwiftlyServerTool launch-agent print-plist
```

That gives you the exact LaunchAgent payload the package currently wants to stage, including:

- the label
- the `ProgramArguments` path and `serve` invocation
- the working directory
- the stdout and stderr log files
- the `SPEAKSWIFTLY_PROFILE_ROOT` environment override for the standalone server

That profile-root override is the LaunchAgent-owned runtime persistence root. It is the directory the installed background service uses for its persisted runtime configuration and the underlying `SpeakSwiftly` profile and artifact persistence, so operators do not have to manage those two filesystem surfaces independently.

## Install Or Refresh The Background Service

Once the property list looks right, install it with the config file you want the background service to use:

```bash
xcrun swift run SpeakSwiftlyServerTool launch-agent install \
  --config-file ./server.yaml
```

This package's LaunchAgent path is designed around the staged release artifact, not around whichever debug binary happened to run the command. That keeps the installed service pointed at the package's maintained release surface instead of at a transient local build product.

If the live service should start running the current repository checkout instead of whichever executable already lives at `.release-artifacts/current`, use the promotion path instead:

```bash
xcrun swift run SpeakSwiftlyServerTool launch-agent promote-live \
  --config-file ./server.yaml
```

That command rebuilds the release executable, stages the executable and sibling `SpeakSwiftly` metallib into `.release-artifacts/current`, refreshes the staged executable's ad-hoc code signature explicitly, and then reruns the LaunchAgent install flow. Use `install` when the staged artifact is already the intended live executable. Use `promote-live` when the intent is "make the current source checkout become the live service now."

## Inspect Or Remove The Installed Service

Use the same executable to check the installed state or remove it:

```bash
xcrun swift run SpeakSwiftlyServerTool launch-agent status
xcrun swift run SpeakSwiftlyServerTool launch-agent uninstall
```

For one explicit live-service verification pass, run:

```bash
xcrun swift run SpeakSwiftlyServerTool healthcheck
```

That command probes the HTTP health route, reads the shared runtime host snapshot, and sends a real MCP `initialize` request to the live `/mcp` endpoint so the result distinguishes "the process is up" from "both transports are actually healthy."

Treat those commands as the stable maintenance surface for the per-user service. If the install layout or staged release artifact path changes in the package, those commands should keep reflecting the package's current contract without requiring operators to re-derive launchd details by hand.

## Related Reading

- Continue with <doc:Using-The-Command-Line-Tool> if you need the broader role of the executable.
- Continue with <doc:App-Managed-Install-Layout> if an app also needs to own the filesystem surface around the installed service.
- Use the repository docs for the full command reference and the transport-level operator inventory.
