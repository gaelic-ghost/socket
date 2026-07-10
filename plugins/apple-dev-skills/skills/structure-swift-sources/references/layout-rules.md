# Layout Rules

## Project Prefix

- Choose and record one explicit three-letter uppercase prefix for every Swift app or package.
- Suggest app or package initials, or `G` plus two product initials, but require the user or agent to make the final choice.
- Prefix every project-owned Swift filename and its primary declaration. Do not silently derive a new prefix after setup.
- Exempt only `Package.swift`, externally generated Swift, and vendored third-party Swift by default.
- Retire `+` filenames completely because they weaken navigator consistency and interfere with Xcode rename and refactoring workflows.

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
- Follow `swiftui-app-architecture-workflow` for component extraction and paired `View`, `ViewModel`, and `ViewModifier` filenames.
- Use concatenated ownership names such as `GEASettingsSheetToggleCard.swift` and `GEAWhateverServiceAdapter.swift`.
- Use `GEAWhatever.swift` for the runtime/domain value, `GEAWhateverModel.swift` for persistence, and `GEAWhateverRecord.swift` or `GEAWhateverDTO.swift` only for genuinely additional representations.
- `Models/` owns Core Data persistence models, SwiftData `@Model` types, app datamodels, DTOs, and shared transfer or persistence shapes.
- `Services/` owns app-wide and boundary-facing services with `Consumed/`, `Internal/`, and `Provided/` subdirectories.
- Put the main app-wide service under `Services/Internal/` as `GEAAppService.swift`; it may manage `GEA.swift` as the application runtime/domain value while `GEAApp.swift` remains the lifecycle-entry special case.
- Move files into their proper layer directory rather than leaving them flat at the project root.

## Shared Rule

- Prefer layout that makes both feature ownership and technical role easy to scan from the path.
- Do not create duplicate parallel trees for the same responsibility.
