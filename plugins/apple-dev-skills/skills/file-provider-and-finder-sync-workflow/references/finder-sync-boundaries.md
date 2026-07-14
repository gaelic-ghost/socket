# Finder Sync Boundaries

Finder Sync is a macOS Finder UI extension. It manages monitored directories with `FIFinderSyncController.directoryURLs`, badges with `setBadgeIdentifier(_:for:)`, selected-item context, targeted URLs, and menu/toolbar-facing behavior.

It does not provide a remote storage domain, placeholders, file hydration, background synchronization, remote-change reconciliation, upload/download, or conflict resolution. A Finder badge is a presentation of known state, not proof that a remote operation completed.

Keep monitored directories narrow, return quickly from UI callbacks, and route heavy work to the containing app or the real synchronization authority through a documented and user-visible action.

## Sources

- [FIFinderSyncController](https://developer.apple.com/documentation/findersync/fifindersynccontroller)
- [Finder Sync](https://developer.apple.com/documentation/findersync)
