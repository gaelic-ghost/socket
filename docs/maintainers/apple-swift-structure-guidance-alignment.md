# Apple Swift Structure Guidance Alignment

This note records the first alignment pass for Gale's preferred Swift and
Apple-platform project structure across Socket's Swift-related skills.

## Current Fit

The existing guidance is already close to the preferred shape:

- `swift-lang` owns shared Swift language choices: API ergonomics, functional
  data pipelines, formatting, source organization, and modernization cleanup.
- `apple-dev-skills` owns Apple-platform structure: Xcode, SwiftUI app and
  scene ownership, AppKit app architecture, project guidance sync, and
  Apple-docs-first workflow.
- `server-side-swift` owns SwiftPM-first server work and should keep app,
  scene, preview, simulator, and Xcode-specific concerns delegated away.

The useful next move is to make the preferred app structure more explicit
inside Apple app guidance, not to rename the whole stack to MVVM-C.

## Preferred Structure

Use a coordinator-shaped, MVVM-C-adjacent model only where it removes real
ownership confusion:

- `App` declares app entry, app-wide lifecycle, and the top-level scene list.
- `Scene` owns per-window, per-document, or managed scene lifecycle and context.
- Small controller or coordinator objects own navigation, presentation, command,
  focus, and workflow state for a view cluster or scene boundary.
- SwiftUI views stay component UI: render state, expose local interactions, and
  avoid becoming broad app coordinators.
- View models are typed view-driving state when they clarify a real view or
  view-cluster boundary; they are not mandatory wrappers around every model.
- Coordinators are useful for scene, command, workflow, navigation, or
  presentation ownership; they should not become a second hidden scene graph.
- Models preserve source-of-truth naming and raw persistence or wire shape until
  a real semantic boundary requires mapping.
- Data transformation should prefer small composable functions and functional
  pipelines when that keeps flow readable.

## Guidance Changes To Consider

### `apple-dev-skills:swiftui-app-architecture-workflow`

Add a focused reference or section for "coordinator-shaped SwiftUI" that:

- describes controllers/coordinators as local ownership tools, not mandatory
  architecture ceremony
- routes app lifecycle to `App`, scene lifecycle to `Scene`, and component
  rendering to `View`
- distinguishes view-driving state from navigation or workflow coordination
- warns against environment-object dumping and hidden router state
- keeps native SwiftUI scene actions, focused values, and selection-driven
  `NavigationSplitView` as the first choices when they fit

### `apple-dev-skills:sync-xcode-project-guidance`

Update the reusable Xcode project guidance snippet so downstream app repos can
name this preference directly:

- small focused controller or coordinator classes are encouraged when they own
  a real view cluster, scene, command, or workflow boundary
- broad global coordinators, mandatory view-model wrappers, and duplicate
  mapping layers remain anti-patterns

### `apple-dev-skills:sync-swift-package-guidance`

Keep package guidance focused on SwiftPM and Swift language quality. Add only a
handoff note for app architecture when a package contains app-facing SwiftUI or
AppKit modules.

### `swift-lang`

Keep the shared Swift layer focused on source organization and functional data
flow. It should not learn Apple scene, command, or navigation ownership details.

## Validation For A Future Implementation Slice

- Run the Apple Dev child validation added for the touched skill references.
- Run `uv run scripts/validate_socket_metadata.py` from the Socket root after
  metadata, marketplace, or exported skill descriptions change.
- Review generated or copied guidance text for consistent vocabulary:
  `controller`, `coordinator`, `view-driving state`, `scene`, `view cluster`,
  and `component UI`.
