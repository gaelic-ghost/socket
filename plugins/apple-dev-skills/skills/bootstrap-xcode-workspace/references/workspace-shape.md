# Apps And Packages Workspace Shape

Use this reference when a product has several Apple apps that share local Swift
packages.

| Surface | Owns | Does not own |
| --- | --- | --- |
| `.xcworkspace` | related Xcode projects, workspace navigation, shared scheme context | package target graph or app build settings |
| `.xcodeproj` | targets, build configurations, schemes, package declarations | the whole product's package graph |
| app target | one installable app product | reusable Core modules by default |
| `Package.swift` | package products, targets, dependencies, resources, tests | Xcode app signing and destinations |

## XcodeGen

- XcodeGen `2.46.0` is the current validated baseline.
- Generate each app project from its own spec.
- For workspace-relative scheme file paths, set `options.schemePathPrefix: "../"`.
- Set `defaultSourceDirectoryType: syncedFolder` only for Xcode 16+ project
  formats and ordinary broad app roots. Retain narrow explicit source entries
  only for genuinely exceptional build-phase or membership behavior.
- A local package entry needs a path to a directory containing `Package.swift`.
  Link its actual product through the consuming target dependency.
- `excludeFromProject` is an exception for a package deliberately visible through
  the workspace but not intended for a standalone app project.

## Platform Topology

- `separate-projects` is the default for independently shipped or heavily
  platform-specific apps.
- `multiplatform-target` is suitable only when non-watch Apple platforms share
  lifecycle and app identity.
- watchOS remains separate; do not treat it as another supported destination of
  the shared app target.
