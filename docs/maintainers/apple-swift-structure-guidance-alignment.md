# Apple Swift Structure Guidance Alignment

This note records Gale's preferred Swift and Apple-platform project structure
across Socket's Swift-related skills.

## Current Fit

The existing guidance is already close to the preferred shape:

- `swift-lang` owns shared Swift language choices: API ergonomics, functional
  data pipelines, formatting, source organization, and modernization cleanup.
- `apple-dev-skills` owns Apple-platform structure: Xcode, SwiftUI app and
  scene ownership, AppKit app architecture, project guidance sync, and
  Apple-docs-first workflow.
- `server-side-swift` owns SwiftPM-first server work and should keep app,
  scene, preview, simulator, and Xcode-specific concerns delegated away.

The useful direction is strict Apple-app MVVM for Xcode app projects, while
keeping Swift package and server-side Swift guidance focused on their own
non-app boundaries.

## Preferred Structure

Use strict Apple-app MVVM for Xcode app projects:

- `App` declares app entry, app-wide lifecycle, and the top-level scene list.
- App-wide `@Observable` state lives beside the app entry point in
  `WhateverNameApp+ViewModel.swift`, containing
  `@Observable final class WhateverNameAppViewModel`.
- `Scene` owns per-window, per-document, or managed scene lifecycle and context.
- SwiftUI views stay component UI: render state, expose local interactions, and
  avoid becoming broad app coordinators.
- View-local state and actions stay in the view where feasible.
- View models are typed view-driving state paired with exactly one owning view
  or app entry point.
- SwiftUI view models live beside their matching view as
  `SomeKindaView+Model.swift`.
- UIKit and AppKit view-controller support lives beside the matching view as
  `SomeKindaView+Controller.swift`.
- Models preserve source-of-truth naming and raw persistence or wire shape until
  a real semantic boundary requires mapping.
- `Sources/Models/` owns Core Data persistence models, SwiftData `@Model`
  types, app datamodels, DTOs, and shared transfer or persistence shapes.
- `Sources/Services/Consumed`, `Sources/Services/Internal`, and
  `Sources/Services/Provided` own services by direction.
- The main app-wide service, when present, lives under
  `Sources/Services/Internal/` as `WhateverNameAppService.swift`.
- There is no root `Controllers/` directory in ordinary Xcode app structure.
- Data transformation should prefer small composable functions and functional
  pipelines when that keeps flow readable.

## Implemented Guidance Changes

### `apple-dev-skills:swiftui-app-architecture-workflow`

The workflow now treats strict app MVVM as the app-project source layout:

- routes app lifecycle to `App`, scene lifecycle to `Scene`, and component
  rendering to `View`
- distinguishes view-driving state from services, persistence models, and view
  controller support
- warns against environment-object dumping and hidden router state
- keeps native SwiftUI scene actions, focused values, and selection-driven
  `NavigationSplitView` as the first choices when they fit

### `apple-dev-skills:sync-xcode-project-guidance`

The reusable Xcode project guidance now names the structure directly and the
sync runtime emits a `structure_audit` payload for downstream repos:

- missing `Sources/Views/Shared`, `Sources/Views/macOS`, `Sources/Views/iOS`,
  `Sources/Models`, `Sources/Services/Consumed`, `Sources/Services/Internal`,
  or `Sources/Services/Provided`
- legacy `Sources/Controllers`
- unpaired `ViewModel.swift` files
- view model or controller support files outside `Sources/Views`
- missing app-entry view model files
- missing internal app service files when a strict app entry exists

The sync skill still owns downstream repo guidance alignment. Socket Steward and
`productivity-skills:maintain-project-docs` own umbrella Socket docs audits and
proposal reports; they should point at this sync skill when Apple app repo
guidance drift is the concrete finding.

### `apple-dev-skills:sync-swift-package-guidance`

Keep package guidance focused on SwiftPM and Swift language quality. Add only a
handoff note for app architecture when a package contains app-facing SwiftUI or
AppKit modules.

### `swift-lang`

Keep the shared Swift layer focused on source organization and functional data
flow. It should not learn Apple scene, command, or navigation ownership details.

## Validation

- Run the Apple Dev child validation added for the touched skill references.
- Run `uv run scripts/validate_socket_metadata.py` from the Socket root after
  metadata, marketplace, or exported skill descriptions change.
- Review generated or copied guidance text for consistent vocabulary:
  `strict Apple-app MVVM`, `view-driving state`, `Services/Consumed`,
  `Services/Internal`, `Services/Provided`, `Models`, `Views`, and
  `component UI`.
