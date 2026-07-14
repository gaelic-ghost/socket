# App Extension Workflows Plan

## Decision

Apple Dev Skills owns reusable Apple app-extension mechanics plus the specific macOS MailKit and File Provider/Finder Sync workflows. This is a durable building-block change: it removes the gap between app-level architecture skills and extension-specific framework work without adding a generic extension framework or absorbing product policy.

## Owned Workflows

- `app-extension-architecture-workflow` routes extension points, targets, separate processes, lifecycle, activation, entitlement minimization, App Groups/shared containers, typed data flow, privacy, testing, signing, distribution, and focused handoffs.
- `mailkit-workflow` owns macOS MailKit content blockers, message actions, compose sessions, message security, capability declarations, privacy, and handler validation.
- `file-provider-and-finder-sync-workflow` owns remote storage synchronization through File Provider and constrains Finder Sync to monitored-folder badges, menus, selected-item context, and visibility.

## Explicit Non-Goals

- Do not turn this slice into a catch-all guide for every extension point.
- Do not place Messages/iMessage collaboration, communication-notification policy, VoIP, or Push to Talk behavior here; Messaging Collaboration Skills owns those product workflows.
- Do not make Finder Sync a sync engine. File Provider owns remote storage enumeration, materialization, document operations, remote change signaling, and recovery.
- Do not move server transport, storage protocol, or backend persistence ownership into Apple Dev Skills.

## Documentation Evidence

The shipped workflows cite Apple documentation for the separate-process app-extension model, MailKit handler capabilities, File Provider synchronization and working sets, Finder Sync controller UI, App Groups, and per-target signing/distribution boundaries. A current Xcode documentation search is required before future platform-behavior changes.

## Delivery Checklist

- [x] Add the three bounded skills with interface metadata, customization contract, shared Xcode policy reference, and authoritative Apple source links.
- [x] Add targeted tests and update the active inventory, plugin manifest, README, AGENTS guidance, docs validator, and customization review.
- [x] Export the portable instruction-only skills through the checked-in Hermes skill tap, group them, and validate the export.
- [x] Keep MailKit/File Provider/Finder Sync as product-specific handoffs from reusable extension mechanics.
- [ ] Validate a real app target for each framework only when a consumer app supplies the concrete project, signing identity, and service/backend context.
