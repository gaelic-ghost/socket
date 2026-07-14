---
name: file-provider-and-finder-sync-workflow
description: Choose File Provider for Apple remote-storage synchronization or scoped macOS Finder Sync UI. Use when a feature needs cloud-backed files or Finder decoration without confusing Finder Sync with a sync engine.
metadata:
  hermes:
    category: apple-development
    tags: [apple, file-provider, finder-sync, macos, ios, remote-storage, synchronization]
---

# File Provider and Finder Sync Workflow

## Purpose

Choose the correct filesystem extension model. File Provider is the modern path for remote-storage synchronization: it enumerates items, materializes content, receives file operations, and reports remote changes to the system. Finder Sync is a macOS Finder UI extension for monitored-folder badges, contextual menus, and visibility; it does not implement remote synchronization itself.

This skill owns that decision, File Provider synchronization mechanics, and Finder Sync’s limited UI role. It does not own a storage backend protocol, generic networking, or unrelated app-extension architecture.

## When To Use

- Use this skill when an Apple app exposes remote storage in Files or Finder, synchronizes cloud-backed files, handles placeholders, materializes content, or reconciles remote changes.
- Use this skill when a macOS app needs Finder badges, toolbar/contextual menus, selected-item context, or monitored-folder visibility.
- Use `app-extension-architecture-workflow` when target/process, entitlement, app-group, or general extension decisions remain unresolved.
- Use `swift-openapi-client-workflow` or server-side skills when the storage service contract or transport is the main unresolved concern.
- Use `xcode-build-run-workflow`, `xcode-testing-workflow`, and `macos-distribution-workflow` for execution, testing, and release evidence.

## Single-Path Workflow

1. Classify the requested outcome:
   - choose File Provider when users need remote files to appear, hydrate, upload, rename, move, delete, remain available offline as supported, and reconcile with a remote service
   - choose Finder Sync only when the files already exist locally and the product needs Finder badges, menus, or monitored-folder UI
   - combine them only when File Provider owns sync and Finder Sync has a separately justified, narrow Finder UI role
2. State the documented behavior relied on:
   - a File Provider extension enumerates storage and implements file operations; the system asks it to materialize content and notify the system of remote changes
   - the File Provider working set drives background updates, materialized availability, and Spotlight visibility
   - Finder Sync manages `directoryURLs`, badges, selected items, and menu/visibility UI for monitored folders; it is not a sync implementation
3. Design File Provider as the synchronization authority:
   - define stable item identifiers, parent hierarchy, version/anchor handling, placeholders, materialization, upload, rename/move/delete, conflict behavior, and cancellation
   - distinguish local intent from confirmed remote state and maintain a durable retry/reconciliation plan
   - signal remote changes with the documented File Provider notification/enumerator path or supported push path; do not pollute Finder UI callbacks with sync work
   - keep backend transport behind a small, typed client boundary and avoid treating local file paths as durable remote IDs
4. Bound Finder Sync:
   - monitor only the necessary local directories
   - use badges and menus to represent known local state, explain uncertainty, and initiate explicit app actions when needed
   - do not claim Finder Sync observes all disk changes, transfers files, owns conflict resolution, or makes remote content available
5. Protect people’s files:
   - minimize metadata and content access, avoid logging file names or paths unnecessarily, and describe sync/error state honestly
   - keep user actions, destructive remote changes, conflict choices, and offline behavior visible and recoverable
6. Validate:
   - File Provider: domain/account lifecycle, enumeration, placeholders, fetch, upload, rename/move/delete, working-set changes, remote notifications, offline behavior, cancellation, conflicts, and upgrade/recovery
   - Finder Sync: extension enablement, monitored directories, badge update, menu context, selected-item behavior, disabled state, and Finder restart/relaunch behavior
   - validate target entitlements, signing, embedding, and distribution separately from service integration tests
7. Return the chosen model, documented behavior, ownership map, backend handoff, privacy policy, validation matrix, and next workflow.

## Inputs

- `request`: optional storage or Finder feature request.
- `platforms`: optional macOS, iOS, iPadOS, or mixed platform context.
- `storage_model`: optional remote authoritative store, local-only folder, existing File Provider domain, or unknown.
- `finder_ui_need`: optional badges, menus, selected-item actions, or none.
- Defaults:
  - File Provider for remote storage synchronization
  - Finder Sync only for constrained local Finder UI
  - explicit remote identity, conflict, retry, and privacy policies
  - no claim that Finder Sync performs synchronization

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `integration_plan`:
  - selected File Provider, Finder Sync, or explicitly bounded combination
  - documented behavior relied on and target ownership
  - synchronization or Finder UI state model
  - backend, privacy, conflict, and recovery boundaries
  - validation matrix and explicit next handoff

## Guards and Stop Conditions

- Do not recommend Finder Sync as the implementation of remote storage synchronization, upload/download, placeholders, conflict resolution, or offline access.
- Do not model a File Provider as a one-way downloader; it must handle the document and hierarchy operations its declared model requires.
- Do not use transient file paths as stable remote identifiers or mistake a local materialized copy for confirmed remote state.
- Do not do network synchronization, long-running reconciliation, or destructive mutation inside Finder menu/badge callbacks.
- Do not silently delete, overwrite, or resolve user-file conflicts without a documented policy and user-visible recovery path.
- Stop with `blocked` when the feature needs filesystem or host access beyond the documented extension point, or the backend cannot supply stable identity and change information needed for safe synchronization.

## Fallbacks and Handoffs

- Recommend `app-extension-architecture-workflow` for extension targets, process isolation, entitlements, App Groups, and shared containers.
- Recommend `swift-openapi-client-workflow` for generated Apple client transport integration.
- Recommend `xcode-build-run-workflow` for target configuration, capabilities, signing, embedding, install, and run work.
- Recommend `xcode-testing-workflow` for File Provider fixture tests, Finder UI checks, and repeatable Xcode test execution.
- Recommend `macos-distribution-workflow` for macOS release artifact validation.
- Recommend `explore-apple-swift-docs` for current File Provider or Finder Sync API confirmation.
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable File Provider/Finder Sync target structure guidance.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` preserves the common customization-file contract. Synchronization ownership, conflict policy, and monitored-directory scope remain product evidence, not opaque defaults.

## References

### Workflow References

- `references/file-provider-synchronization.md`
- `references/finder-sync-boundaries.md`
- `references/privacy-validation-and-recovery.md`
- `references/customization-flow.md`

### Authoritative Sources

- [Synchronizing files using file provider extensions](https://developer.apple.com/documentation/fileprovider/synchronizing-files-using-file-provider-extensions)
- [Synchronizing the File Provider Extension](https://developer.apple.com/documentation/fileprovider/synchronizing-the-file-provider-extension)
- [FIFinderSyncController](https://developer.apple.com/documentation/findersync/fifindersynccontroller)

### Support References

- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode project guidance for File Provider and Finder Sync targets.

### Script Inventory

- `scripts/customization_config.py`
