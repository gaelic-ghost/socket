# Layout Rules

## Swift Packages

- Prefer directories grouped by both layer and feature when the package has real feature boundaries.
- High-signal examples:
  - `API/<Feature>/<Concern>.swift`
  - `Features/<Feature>/<Concern>.swift`
  - `Models/<Feature>/<Concern>.swift`
- Do not force a feature tree when the package is truly tiny or infrastructure-only.

## Xcode App Projects

- Ensure app-facing source directories such as `Views/`, `Models/`, and `Services/`.
- Do not create or preserve a root `Controllers/` directory for ordinary app structure.
- `Sources/Views/` must contain `Shared/`, `macOS/`, and `iOS/` subdirectories.
- Keep SwiftUI views and UIKit/AppKit view surfaces in `Views/` or the appropriate platform/shared subdirectory.
- Require one SwiftUI `View` component per file, named `<Name>.swift`, with that component's Xcode SwiftUI preview in the same file.
- Do not group multiple SwiftUI view components into one file; split related child views into their own files instead.
- SwiftUI view models are always per-view, with no exceptions: the model for `<Name>.swift` must live in `<Name>+Model.swift` beside the view and must not be shared with any other SwiftUI view.
- Do not use grouped model files, shared view-model files, or view-cluster models for SwiftUI views.
- When a view needs extracted modifiers, use `<Name>+Modifier.swift`.
- UIKit and AppKit view-controller support files must live beside their matching view as `<Name>+Controller.swift`.
- Put app-wide `@Observable` state beside the app entry point: `WhateverNameApp.swift` pairs with `WhateverNameApp+ViewModel.swift`.
- `Models/` owns Core Data persistence models, SwiftData `@Model` types, app datamodels, DTOs, and shared transfer or persistence shapes.
- `Services/` owns app-wide and boundary-facing services with `Consumed/`, `Internal/`, and `Provided/` subdirectories.
- Put the main app-wide service, when present, under `Services/Internal/` as `WhateverNameAppService.swift`.
- Move files into their proper layer directory rather than leaving them flat at the project root.

## Shared Rule

- Prefer layout that makes both feature ownership and technical role easy to scan from the path.
- Do not create duplicate parallel trees for the same responsibility.
