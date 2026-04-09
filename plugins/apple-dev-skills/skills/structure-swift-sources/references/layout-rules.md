# Layout Rules

## Swift Packages

- Prefer directories grouped by both layer and feature when the package has real feature boundaries.
- High-signal examples:
  - `API/<Feature>/<Concern>.swift`
  - `Features/<Feature>/<Concern>.swift`
  - `Models/<Feature>/<Concern>.swift`
- Do not force a feature tree when the package is truly tiny or infrastructure-only.

## Xcode App Projects

- Ensure app-facing source directories such as `Views/`, `Controllers/`, and `Models/`.
- Keep SwiftUI views in `Views/`.
- When a view has a paired model type, use `<Name>+Model.swift`.
- When a view needs extracted modifiers, use `<Name>+Modifier.swift`.
- Move files into their proper layer directory rather than leaving them flat at the project root.

## Shared Rule

- Prefer layout that makes both feature ownership and technical role easy to scan from the path.
- Do not create duplicate parallel trees for the same responsibility.
