# ``SpeakSwiftlyServer``

Embed the shared SpeakSwiftly speech runtime in an app, or package the same host behind HTTP, MCP, and command-line operator surfaces.

## Overview

`SpeakSwiftlyServer` is the library layer for the standalone SpeakSwiftly server package. It owns the embedded host session, the app-facing observable state model, and the install-layout contract that a macOS app can use when it stages the LaunchAgent-backed server into a per-user home directory.

The package also ships the `SpeakSwiftlyServerTool` executable, but the executable is an operator surface built on top of this library rather than the main story of the hosted package docs. Start here when you need to:

- start the shared server inside an app process
- read the current host, queue, transport, and runtime snapshots from SwiftUI-friendly state
- reason about the filesystem layout an app should own when it installs the standalone server

When you need transport-level route inventories, request and response payload examples, or command-line usage details, use the repository operator docs in the README and API reference:

- [README](https://github.com/gaelic-ghost/SpeakSwiftlyServer/blob/main/README.md)
- [API Reference](https://github.com/gaelic-ghost/SpeakSwiftlyServer/blob/main/API.md)

## Topics

### Embedding The Shared Host

- ``EmbeddedServerSession``
- ``ServerState``
- ``HostStateSnapshot``

### App-Owned Install Surface

- ``ServerInstallLayout``
- ``ServerInstalledLogs``
- ``ServerInstalledLogsSnapshot``

### Runtime Entry

- ``ServerRuntimeEntrypoint``

### Executable Companion

- ``SpeakSwiftlyServerToolCommand``
- ``LaunchAgentCommand``

### Articles

- <doc:First-Embedded-Session>
- <doc:Embedding-The-Server>
- <doc:App-Managed-Install-Layout>
- <doc:Operator-Surfaces>
- <doc:Using-The-Command-Line-Tool>
- <doc:LaunchAgent-Workflow>
