## Apple / Xcode Workspace Workflow

- Treat this repository root as a composition layer: the `.xcworkspace` groups
  related app projects, `Apps/` owns app projects, `Packages/` owns standalone
  Swift packages, and `Services/` is an optional independent backend boundary.
- Prefer local Swift package products for shared Core code. Each consuming app
  declares its own local package path and product dependency in its XcodeGen
  spec; workspace visibility alone is not dependency wiring.
- Use `projectReferences` only for real Xcode target dependencies across
  projects. Do not use groups, folder references, or cross-project references as
  replacements for package boundaries.
- For XcodeGen projects in this workspace, use `schemePathPrefix: "../"` when
  a scheme stores workspace-relative file paths. Treat every app `project.yml`
  as the source of truth for its generated project and never edit `.pbxproj`.
- Use `sync-xcode-project-guidance` for an app project,
  `sync-swift-package-guidance` for a package, and
  `xcode-build-run-workflow` or `xcode-testing-workflow` for active Xcode work.
