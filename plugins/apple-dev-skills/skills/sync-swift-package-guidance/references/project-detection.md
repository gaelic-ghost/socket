# Swift Package Detection Notes

## Detection Rules

- Treat `Package.swift` at the requested repo root as the primary package marker.
- Treat `.xcodeproj` or `.xcworkspace` markers at the same repo root as an ambiguity signal, not as a package-sync success condition.
- Prefer an explicit package-root path when a larger mono-repo contains both app and package surfaces.

## Boundaries

- Use `sync-swift-package-guidance` for plain SwiftPM repos whose source of truth is `Package.swift`.
- Use `bootstrap-xcode-workspace --operation align` for native Apple product workspaces.
- Use `bootstrap-swift-package` when the package repo does not exist yet.
