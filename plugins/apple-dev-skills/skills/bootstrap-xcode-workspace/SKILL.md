---
name: bootstrap-xcode-workspace
description: Create and align one Swift product workspace with Apps, Packages, and Services components, or add a new component without converting the repository.
---

# Bootstrap Apple Product Workspace

## Purpose

Create one product repository with one root `.xcworkspace` and one root XcodeGen project
materialized as the generated root `.xcodeproj`. `Apps/` contains platform-specific targets in that project;
`Packages/` contains shared SwiftPM modules, and `Services/` contains deployable
SwiftPM executables. This is the entrypoint for app-first, service-first, and
combined products.

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
  Services/
    services-shared.yml              # XcodeGen service-package registry
    ProductAPI/
      Package.swift
  docs/  Scripts/  .github/workflows/
```

## Ownership

- `project.yml` owns project identity, configurations, file groups, and the
  included project graph.
- `Apps/apps-shared.yml` owns common target and scheme templates.
- `Apps/<Target>/target.yml` owns one target's platform, source roots,
  target-local configurations, and product dependencies.
- `Packages/packages-shared.yml` registers local packages with XcodeGen.
- `Services/services-shared.yml` registers deployable service packages with XcodeGen.
- Each `Package.swift` owns its package products, targets, and dependencies.
- Root `Configurations/` owns project-wide settings. `Apps/Apps-shared.xcconfig`
  and target-local `.xcconfig` files layer app and target settings without
  duplicating the project baseline.
- Generated `.xcodeproj` data is build-critical output. Edit its XcodeGen and
  SwiftPM sources, then regenerate; never hand-edit `.pbxproj`.

## When To Use

Use this skill to create any Swift product repository, add an app, package, or
server component to an existing product, or realign the generated workspace and
managed guidance. Use `bootstrap-swift-package` only for a deliberately
standalone published library or CLI that is not part of a product workspace.

## Single-Path Workflow

1. Apply the Apple documentation gate through `explore-apple-swift-docs`.
2. Run `scripts/run_workflow.py --name <Name> --file-prefix <ABC>`.
   The default creates iOS and macOS targets, their Swift Testing and XCUITest
   bundles, plus `<Name>Core`.
   Start package-first with `--component-kind library` or service-first with
   `--component-kind service --framework hummingbird|vapor`; both still create
   the same permanent root workspace and component roots.
3. Add components only through `--operation add-component`:
   - app: `--component-kind app --component-name <Name> --platform <platform>`
   - library: `--component-kind library --component-name <Name>`
   - service: `--component-kind service --component-name <Name> --framework hummingbird|vapor`
4. The service option delegates framework generation to
   `server-side-swift:workspace-service-component`, while this skill retains
   ownership of the root workspace and project graph.
5. Run `just setup` after initializing Git, then use `just align` to refresh
  Socket-managed guidance/hooks and regenerate with XcodeGen. Route by
  operation: use the nearest `Package.swift` for package/service work and the
  root workspace for Xcode-owned schemes, destinations, previews, and project state.
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
- `operation`: `create`, `add-component`, or `align`.
- `repo_root`: required with `add-component` and `align`.
- `component_kind`, `component_name`: required with `add-component`.
- `platform`: required for an app component.
- `framework`: required for a service component; `hummingbird` or `vapor`.

## Outputs

- One permanent root Xcode workspace and generated XcodeGen project.
- `Apps/`, `Packages/`, and `Services/` component registries.
- Operation-routed SwiftPM and Xcode validation commands.
- Native Homebrew local-service guidance and GitHub-hosted cloud workflow ownership.

## Guards and Stop Conditions

- For an existing canonical workspace, run
  `scripts/run_workflow.py --operation align --repo-root <root>` instead of
  using a separate sync skill. It preserves local documentation and Justfile
  content outside Socket-managed markers.
- Stop when a create destination product root is non-empty.
- Stop when XcodeGen is unavailable.
- Do not introduce a second project generator, manually edited project data, or
  a separate app `.xcodeproj` under `Apps/`.
- Do not classify the repository as Xcode, SwiftPM, plain, or mixed. Those files
  coexist by design; select tools from the requested operation.
- Local service dependencies use native Homebrew services. Cloud Linux builds,
  live-test deployments, and production deployments run only in GitHub Actions.
- A standalone published library or CLI remains a deliberate exception: use
  `bootstrap-swift-package` only when it is not part of an Apple product
  workspace.

## Fallbacks and Handoffs

- Hand service generation to `server-side-swift:workspace-service-component`;
  do not let the framework generator own or replace the product workspace.
- Hand repository maintenance to `repository-skills:maintain-project-repo` with
  the `xcode-workspace` profile.
- When Xcode-only state is required, use the root workspace and Xcode workflows;
  otherwise run the nearest package operation directly.

## Customization

This skill intentionally has no independent customization template. Its explicit
CLI inputs define product identity and component creation, while the generated
XcodeGen and SwiftPM source files are the durable customization surfaces. Do not
add repository-shape switches or alternate local/cloud execution modes.

## References

- `references/workspace-shape.md`
- [Apple: organizing code with local packages](https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages)
- [XcodeGen Project Spec](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html)
