# App-Managed Install Layout

## Overview

Use ``ServerInstallLayout`` when an app needs one stable answer for where the standalone `SpeakSwiftlyServer` install should live in a user account.

The layout type exists so an app can stage the LaunchAgent-backed server into an owned filesystem surface without guessing at paths for:

- application support files
- cache and log files
- LaunchAgent property lists
- runtime profile and configuration storage

## Core Types

### ``ServerInstallLayout``

``ServerInstallLayout`` is the path contract. It describes the working directory, support and cache roots, LaunchAgents directory, config files, runtime storage, and stdout and stderr log files for one user install.

Use ``ServerInstallLayout/defaultForCurrentUser(fileManager:homeDirectoryURL:launchAgentLabel:)`` when the app wants the package’s default per-user layout. If the app needs a custom label or a redirected home directory during tests, provide those values explicitly.

### Installed Log Snapshots

Use ``ServerInstalledLogs/read(layout:maximumLineCount:)`` to read the retained stdout and stderr files for an installed server.

The read path returns ``ServerInstalledLogsSnapshot``, which contains:

- the layout the read used
- a ``ServerInstalledLogFileSnapshot`` for stdout
- a ``ServerInstalledLogFileSnapshot`` for stderr

`ServerInstalledLogFileSnapshot` keeps the retained text, split lines, detected JSON line texts, and truncation counts together so app code can build operator views without re-parsing the files each time.

## Ownership Guidance

Treat this install layout as the app-owned staging surface for the standalone server. If the package later grows new runtime files, extend the layout type instead of teaching each caller to synthesize new ad hoc path rules.
