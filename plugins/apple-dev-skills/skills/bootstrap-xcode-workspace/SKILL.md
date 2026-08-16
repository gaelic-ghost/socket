---
name: bootstrap-xcode-workspace
description: Bootstrap one Apple product workspace with one root XcodeGen project, Apps target directories, and Packages local Swift packages. Use for all new Apple product repositories.
---

# Bootstrap Apple Product Workspace

## Purpose

Create one product repository with one root `.xcworkspace` and one generated
root `.xcodeproj`. `Apps/` contains platform-specific targets in that project;
`Packages/` contains the SwiftPM modules that support those targets. Do not
bootstrap new Apple products as independent app projects.

Run `scripts/run_workflow.py` before creating files. It generates the root
XcodeGen project, creates the workspace wrapper, initializes the first local
Swift package with SwiftPM, and installs the `xcode-workspace` maintenance
profile through `repository-skills`.

## Required Shape

```text
Product/
  Product.xcworkspace/
  Product.xcodeproj/                 # generated from project.yml
  project.yml                        # root project graph
  Configurations/                    # Debug, Staging, Release, AppStore, DirectDistribution, AltStore
  AGENTS.md  CONTRIBUTING.md  Justfile
  Apps/
    apps-shared.yml                  # target and scheme templates
    Apps-shared.xcconfig             # shared app build settings
    ProductiOS/
      target.yml
      Configurations/
      Sources/ Resources/ Configurations/ target.yml
    ProductiOSTests/  ProductiOSUITests/
    ProductmacOS/
      target.yml
      Configurations/
      Sources/ Resources/ Tests/
  Packages/
    packages-shared.yml              # XcodeGen local-package registry
    ProductCore/
      Package.swift
  docs/
```

## Ownership

- `project.yml` owns project identity, configurations, file groups, and the
  included project graph.
- `Apps/apps-shared.yml` owns common target and scheme templates.
- `Apps/<Target>/target.yml` owns one target's platform, source roots,
  target-local configurations, and product dependencies.
- `Packages/packages-shared.yml` registers local packages with XcodeGen.
- Each `Package.swift` owns its package products, targets, and dependencies.
- Root `Configurations/` owns project-wide settings. `Apps/Apps-shared.xcconfig`
  and target-local `.xcconfig` files layer app and target settings without
  duplicating the project baseline.
- Generated `.xcodeproj` data is build-critical output. Edit its XcodeGen and
  SwiftPM sources, then regenerate; never hand-edit `.pbxproj`.

## Workflow

1. Apply the Apple documentation gate through `explore-apple-swift-docs`.
2. Run `scripts/run_workflow.py --name <Name> --file-prefix <ABC>`.
   The default creates iOS and macOS targets, their Swift Testing and XCUITest
   bundles, plus `<Name>Core`.
3. Add platform-specific targets by adding a target directory and include in
   root `project.yml`; use `Apps/apps-shared.yml` templates instead of copying
   project settings.
4. Add a local package under `Packages/`, register it in
   `Packages/packages-shared.yml`, then declare only the consumed product in
   the relevant target's dependencies.
5. Run `just setup` after initializing Git, then use `just align` to refresh
   Socket-managed guidance/hooks and regenerate with XcodeGen. Use Xcode for
   app work and `swift` for package work.
6. Use Xcode MCP (`xcrun mcpbridge`) for agent-assisted project inspection and
   debugging when Xcode is open. It augments these deterministic commands; it
   is not a bootstrap prerequisite.

## Inputs

- `name`: required product name and root project/workspace stem.
- `file_prefix`: three uppercase letters; default `APP`.
- `destination`: parent directory; default `.`.
- `platforms`: `ios`, `macos`, `tvos`, `watchos`, and/or `visionos`; default
  `ios,macos`.
- `org_identifier`: bundle identifier prefix; default `com.galewilliams`.
- `development_team`: code-signing team; default `BC73766F69`.
- `dry_run`: report the normalized scaffold without writing files.
- `operation`: `create` (default) creates a new product; `align` initializes
  the managed alignment contract in an existing canonical workspace.
- `repo_root`: required with `--operation align`; the existing workspace root.

## Guards And Handoffs

- For an existing canonical workspace, run
  `scripts/run_workflow.py --operation align --repo-root <root>` instead of
  using a separate sync skill. It preserves local documentation and Justfile
  content outside Socket-managed markers.
- Stop when a create destination product root is non-empty.
- Stop when XcodeGen is unavailable.
- Do not introduce a second project generator, manually edited project data, or
  a separate app `.xcodeproj` under `Apps/`.
- A standalone published library or CLI remains a deliberate exception: use
  `bootstrap-swift-package` only when it is not part of an Apple product
  workspace.

## References

- `references/workspace-shape.md`
- [Apple: organizing code with local packages](https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages)
- [XcodeGen Project Spec](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html)
