---
name: inspect-macos-persistence
description: Inspect macOS persistence and recurring execution without deleting evidence. Use for suspicious login items, background items, launch agents or daemons, system or network extensions, configuration profiles, shell startup files, scheduled tasks, browser extensions, helper tools, app registrations, or startup behavior that may survive logout, reboot, or application exit.
---

# Inspect macOS Persistence

## Overview

Inventory registered and file-backed persistence, then correlate it with loaded runtime state and installation history. Read files and official service state; never manage launchd by editing its internal state.

Read [references/macos-persistence-surfaces.md](references/macos-persistence-surfaces.md) for prioritized surfaces and evidence fields.

## Workflow

1. Record host/build, user domains, event timeline, and the suspected executable or label.
2. Inventory user-visible registrations.
   - Review Login Items and background-item state, profiles, extensions, browser add-ons, and app-managed helpers.
3. Inventory launch services.
   - Inspect user/system LaunchAgents and LaunchDaemons as files and query service state through `launchctl` read operations.
   - Record label, domain, program/arguments, working directory, environment, sockets, keep-alive/start conditions, owner/permissions, signer, and loaded PID/status.
4. Inspect adjacent persistence.
   - Review shell startup files, scheduled jobs, package receipts/scripts, privileged helpers, system/network extensions, authorization plugins, and current platform-specific surfaces justified by evidence.
5. Correlate provenance and runtime.
   - Identify parent installer/app, creation/change time, signature/notarization, executable hash, running process ancestry, files, network, and logs.
6. Classify each item.
   - Expected, suspicious, confirmed malicious, disabled/orphaned, or unresolved; explain evidence and impact.
7. Preserve before containment.
   - Record files and service state before using official `launchctl bootout` or app/uninstaller paths in the containment workflow.

## Output

Return a persistence inventory, loaded-versus-file state, provenance, runtime correlation, classification/confidence, and safe containment handoff.
