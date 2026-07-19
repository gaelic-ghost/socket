# Helpers, Groups, And Process Boundaries

## App Groups

Use an App Group only when separately signed targets from the same developer team need a documented shared container or service. Match the group identifier in tracked project capabilities, developer-account/profile authorization when applicable, and final entitlements of every consumer. An App Group does not grant access to arbitrary external paths.

## Helpers and XPC services

- Record which executable receives the user-selected URL, creates bookmark data, stores it, resolves it, starts access, and performs I/O.
- Do not pass a path across IPC and assume authorization follows.
- Prefer the parent process perform the file operation and exchange bounded data when that keeps authority narrower.
- If another process must consume the resource, verify the documented sandbox inheritance or bookmark transfer contract for that process type and distribution channel.
- Inspect the final signed entitlements and embedded profile of the helper/XPC service, not only the app target.

## Extensions

App extensions run in separate processes with their own entitlements, containers, lifecycle, and host-mediated inputs. Use extension-provided URLs only within their documented lifetime unless a supported bookmark contract says otherwise. Route extension architecture to `app-extension-architecture-workflow`.

## Directory selection

A user-selected directory may authorize descendants under the documented sandbox extension/bookmark behavior, subject to read/write scope and other controls. Do not generalize that to siblings, symlink escapes, other volumes, TCC-protected locations, or a remote identity model.
