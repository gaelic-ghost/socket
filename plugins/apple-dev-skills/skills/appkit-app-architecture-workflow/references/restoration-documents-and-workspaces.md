# Restoration, Documents, And Workspaces

Use this reference when the request involves app reopening,
`NSWindowRestoration`, window restoration, document restoration, workspace
restoration, restoration identifiers, or the boundary between restored UI state
and durable model state.

## Decision Rules

- Treat restoration as a way to reopen UI around known model state, not as the
  sole durable store for domain data.
- Give restorable windows stable restoration identifiers and a controller that
  can recreate the window from a small payload.
- Keep the durable payload in documents, workspace records, files, Core Data,
  SwiftData, or another real storage surface when the user expects the state to
  survive beyond UI restoration.
- Use document architecture when the user opens, edits, saves, duplicates, or
  versions files as first-class objects.
- Use workspace architecture when the reopenable state is project, folder,
  session, or app-defined state rather than a single document file.

## Restoration Boundary

- **Restoration payload:** enough information to find or reconstruct a window.
- **Durable model state:** the content, project, workspace, or document state the
  restored window will show.
- **Transient UI state:** selection, splitter position, visible inspector, or
  focused control, when useful and cheap to restore.

## AppKit And SwiftUI

- SwiftUI `SceneStorage` and scene identity belong in the SwiftUI architecture
  workflow when SwiftUI owns the scene.
- In AppKit-owned apps, prefer AppKit restoration and window-controller
  ownership, with SwiftUI hosted content receiving the restored model as input.

## Anti-Patterns

- Do not store a full domain model only in a window restoration archive.
- Do not restore a window without checking whether its document, workspace, or
  project still exists.
- Do not conflate "which window reopens" with "what data is saved."
