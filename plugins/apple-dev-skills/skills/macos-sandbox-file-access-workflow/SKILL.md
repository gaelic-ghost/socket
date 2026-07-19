---
name: macos-sandbox-file-access-workflow
description: Design, implement, and diagnose the narrowest documented filesystem access path for a macOS app, helper, XPC service, or extension. Use for App Sandbox containers, App Groups, open/save panels, drag and drop, user-selected file entitlements, security-scoped bookmarks, persistent access across relaunches, stale bookmark repair, helper boundaries, Files and Folders or Full Disk Access overlap, and denials that may instead come from POSIX permissions, ACLs, symlinks, mounts, Data Vaults, or SIP.
---

# macOS Sandbox File Access Workflow

## Purpose

Preserve user intent and access lifetime while selecting the smallest supported file-access mechanism. Treat a URL or path as resource identity, not durable authorization, and keep App Sandbox, TCC, POSIX, and mandatory controls distinct.

## When To Use

- Use when a sandboxed Mac app must open, save, import, export, drag, share, or persist access to files or directories.
- Use when access succeeds during selection but fails after relaunch, in a helper, or after a move/rename.
- Use to identify whether a remaining denial is sandbox, TCC, filesystem, volume, coordination, Data Vault, or SIP policy.

## Single-Path Workflow

1. Record the data owner, exact operation, resource type, read/write/execute need, persistence duration, process boundary, distribution channel, macOS build, and exact error.
2. Read `references/sandbox-and-filesystem-control-map.md` and identify every applicable control layer before choosing a capability.
3. Use the app container or a standard supported container-relative directory when it satisfies the feature. Use an App Group only for a real same-team shared-container requirement.
4. Prefer direct user selection through the appropriate open/save panel, document URL, drag/drop, or Photos/File Provider selection surface for external data.
5. Request only the user-selected read-only, read-write, or executable entitlement that the feature actually needs. Do not replace a narrow selection with Full Disk Access.
6. Create a security-scoped bookmark only when access must survive the current interaction or process lifetime. Follow every step in `references/security-scoped-bookmark-lifecycle.md`.
7. For helpers, XPC services, app extensions, or shared containers, use `references/helpers-groups-and-process-boundaries.md`; verify which process resolves and consumes authorization rather than passing a path and assuming authority follows.
8. Perform the narrow operation and balance every successful `startAccessingSecurityScopedResource()` with `stopAccessingSecurityScopedResource()`. Do not retain access indefinitely for convenience.
9. If access still fails, classify the exact denying layer: path resolution/symlink, ownership/mode/ACL, sandbox, TCC Files and Folders/Full Disk Access, mount/volume state, coordination, Data Vault, SIP, or service policy.
10. Validate relaunch, moved/renamed/removed resources, read-only enforcement, helper/extension behavior, revoked/inaccessible access, stale and malformed bookmark recovery, and privacy-safe logging using `references/validation-fixtures.md`.

## Inputs

- resource owner, selection path, operation, persistence need, and distribution channel
- app/helper/extension identities, sandbox entitlements, App Group, and signed artifacts
- bookmark creation/storage/resolution code and exact errors
- macOS build, volume/mount, POSIX/ACL, TCC, Data Vault, and SIP context

## Outputs

- selected access mechanism and least-privilege entitlement set
- bookmark ownership, storage, resolution, lifetime, and repair contract
- process-boundary authorization design
- exact denying layer, reproduced result, privacy-safe evidence, and unresolved gaps

## Guards and Stop Conditions

- Do not treat a path, URL, alias, file ID, or remote identifier as a durable authorization token.
- Do not store only a security-scoped URL or retain access indefinitely.
- Do not claim a bookmark bypasses TCC, Full Disk Access, Data Vaults, SIP, POSIX permissions, ACLs, mounts, or service policy.
- Do not log bookmark bytes or sensitive full paths without a specific privacy-reviewed diagnostic need.
- Do not use Finder Sync as a synchronization engine or access-grant mechanism.
- Stop when the resource owner, operation, persistence duration, or consuming process is unknown.

## Fallbacks and Handoffs

- Use `macos-privacy-permissions-workflow` for Files and Folders, Full Disk Access, or another TCC decision.
- Use `diagnose-apple-entitlements` when source, profile, or final signed sandbox/App Group entitlements disagree.
- Use `file-provider-and-finder-sync-workflow` for remote storage, File Provider domains, or Finder UI decoration.
- Use `app-extension-architecture-workflow` for extension lifecycle/IPC design and Xcode workflows for project edits.
- Use `research-macos-security-control` for private sandbox profiles, extensions, or exact-build Seatbelt behavior.

## Customization

Use `references/customization-flow.md`. The workflow has no runtime knobs; access scope must follow the recorded feature, process, resource, and lifetime.

## References

- `references/sandbox-and-filesystem-control-map.md`
- `references/security-scoped-bookmark-lifecycle.md`
- `references/helpers-groups-and-process-boundaries.md`
- `references/validation-fixtures.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when implementing target entitlements or helper membership.
- [Protecting user data with App Sandbox](https://developer.apple.com/documentation/security/protecting-user-data-with-app-sandbox)
- [Accessing files from the macOS App Sandbox](https://developer.apple.com/documentation/security/accessing-files-from-the-macos-app-sandbox)
