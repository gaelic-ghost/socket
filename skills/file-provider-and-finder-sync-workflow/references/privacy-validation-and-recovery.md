# Privacy, Validation, and Recovery

## Privacy

File names, paths, hierarchy, metadata, and content can reveal sensitive information. Record only data needed for synchronization, avoid logs that expose paths or content, and make remote uploads, deletions, conflicts, and offline state understandable to the person using the app.

## Validation

Use a disposable remote account and fixture tree. Exercise first connection, domain creation/removal, placeholder enumeration, materialization, changes from both sides, cancellation, network loss, retries, conflict policy, stale-anchor/identifier recovery, and upgrade. Separately prove Finder Sync enablement, folder filtering, badges, menu context, and Finder relaunch behavior.

## Recovery

When state is no longer trustworthy, use File Provider’s documented synchronization-loss and reimport mechanisms. Do not silently reset local data or make irreversible remote changes merely to restore apparent consistency.

## Sources

- [NSFileProviderManager.signalEnumerator(for:completionHandler:)](https://developer.apple.com/documentation/fileprovider/nsfileprovidermanager/signalenumerator(for:completionhandler:))
- [NSFileProviderManager.reimportItems(below:completionHandler:)](https://developer.apple.com/documentation/fileprovider/nsfileprovidermanager/reimportitems(below:completionhandler:))
