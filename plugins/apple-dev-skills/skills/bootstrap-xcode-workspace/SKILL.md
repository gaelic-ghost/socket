---
name: bootstrap-xcode-workspace
description: Bootstrap a modular Apple workspace with an .xcworkspace, Apps and Packages directories, XcodeGen-backed app projects, and optional server siblings. Use when starting a new multi-app Apple codebase that shares Core Swift packages across iOS, macOS, tvOS, watchOS, or visionOS apps; do not use for one standalone app project or one standalone Swift package.
---

# Bootstrap Xcode Workspace

## Purpose

Create the root composition for a modular Apple product without pretending that a
workspace, an Xcode project, an app target, and a Swift package are equivalent.
The workspace owns related Xcode projects and shared schemes. Each app project
owns its targets, build settings, and XcodeGen spec. Each package owns its
manifest and target graph.

Use `scripts/run_workflow.py` to normalize the workspace contract before
creating files. XcodeGen generates each app project; create the `.xcworkspace`
and add the generated projects through Xcode's documented workspace flow rather
than hand-writing workspace data.

## Required Shape

```text
Product/
  Product.xcworkspace/
  Apps/
    ProductiOS/
    ProductMac/
  Packages/
    ProductCore/
  Services/                  # optional
```

- `Apps/` contains one or more independently generated Xcode app projects.
- `Packages/` contains standalone SwiftPM packages, each with `Package.swift`.
- `Services/` is optional and contains a server sibling, never an app target or
  an implicit Apple build dependency.

## Workflow

1. Collect `name`, `destination`, `app_topology`, app platforms, and optional
   service selection. Run `scripts/run_workflow.py` first.
2. Apply the Apple docs gate with `explore-apple-swift-docs`. Use Xcode MCP
   `DocumentationSearch` first; use Dash's `XcodeGen : ProjectSpec` docset when
   XcodeGen detail is needed.
3. Choose topology:
   - Default to `separate-projects` for independently shipped or materially
     platform-specific apps. Create one XcodeGen project per app under `Apps/`.
   - Use `multiplatform-target` only when iOS, macOS, tvOS, or visionOS share
     app identity and lifecycle. Keep watchOS in a separate target/project.
4. Create each Core package under `Packages/` with `bootstrap-swift-package`.
   Make reusable modules package products; do not use Xcode groups as module
   boundaries.
5. Create each app project with `bootstrap-xcode-app-project`. For a workspace
   project, set XcodeGen `options.schemePathPrefix: "../"`; retain the default
   standalone value for projects that are not opened from a workspace.
6. In every consuming app's `project.yml`, declare the local package in the
   top-level `packages` map and link the required product from the app target's
   `dependencies`. A workspace does not replace that per-project declaration.
7. In Xcode, create `<Name>.xcworkspace` at the root and add each `.xcodeproj`
   at workspace root level. Open the workspace, not an individual project, for
   product-wide work.
8. Add an optional service under `Services/` only after selecting it:
   - Hummingbird: `bootstrap-hummingbird-service`.
   - Vapor: `bootstrap-vapor-service`.
   - F#: `choose-fsharp-web-framework`, then `build-fsharp-project` and the
     Azure deployment handoff.
9. Validate packages and app schemes serially. Use `xcode-build-run-workflow`
   for workspace/scheme execution and `xcode-testing-workflow` for Xcode-native
   test work.

## Dependency And Navigator Rules

- Use a local Swift package for shared Core code. Its `Package.swift` is the
  source of truth for targets and products.
- Use an Xcode cross-project reference only when one `.xcodeproj` must depend on
  a target from another `.xcodeproj`; declare it with XcodeGen
  `projectReferences` and a `ProjectName/TargetName` dependency.
- Use filesystem directories for organization. A group only organizes the
  Project navigator. A folder reference is for a bundle-preserved resource
  directory, not ordinary Swift source.
- For Xcode 16 project formats, prefer broad `syncedFolder` roots for ordinary
  app source. Use `explicitFolders` only when a child must intentionally remain
  a folder reference.
- Keep `project.yml`, `.xcconfig`, entitlements, schemes, and generated project
  diffs owned by their documented source files. Never hand-edit `.pbxproj`.

## Inputs

- `name`: required product and workspace name.
- `destination`: parent directory, default `.`.
- `app_topology`: `separate-projects` (default) or `multiplatform-target`.
- `platforms`: comma-separated app platforms; default `ios,macos`.
- `service`: `none` (default), `hummingbird`, `vapor`, or `fsharp-azure`.
- `dry_run`: emit the normalized composition contract without creating files.

## Guards And Handoffs

- Stop when the requested root already contains non-ignorable files.
- Stop when `multiplatform-target` includes watchOS; create a separate watchOS
  target/project instead.
- Do not add packages, services, or projects to the workspace merely for visual
  symmetry. Add only real dependency or navigation surfaces.
- Do not make a backend part of an Apple app's Xcode target graph.
- Hand off existing workspace guidance to `sync-xcode-workspace-guidance`.
- Hand off one existing app project to `sync-xcode-project-guidance` and one
  package to `sync-swift-package-guidance`.

## References

- `references/workspace-shape.md`
- [Apple: managing multiple projects and dependencies](https://developer.apple.com/documentation/xcode/managing-multiple-projects-and-their-dependencies)
- [Apple: organizing code with local packages](https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages)
- [XcodeGen Project Spec](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html)
