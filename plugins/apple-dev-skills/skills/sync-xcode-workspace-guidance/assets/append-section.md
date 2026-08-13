## Apple / Xcode Workspace Workflow

- This product has one root `.xcworkspace` and one generated root `.xcodeproj`.
  Root `project.yml` is the editable Xcode project graph; never hand-edit its
  generated `.pbxproj` data.
- `Apps/` owns Xcode targets. Keep common target and scheme templates in
  `Apps/apps-shared.yml`, shared app build settings in
  `Apps/Apps-shared.xcconfig`, and target-specific settings under the owning
  target directory.
- `Packages/` owns local SwiftPM packages. Register each package in
  `Packages/packages-shared.yml`, but keep products, targets, and dependencies
  in its own `Package.swift`.
- Regenerate with `xcodegen generate --spec project.yml`; use the root
  workspace for Xcode and `xcodebuild` operations. Use `swift` directly for
  package work.
- Use `repository-skills:maintain-project-repo` with the `xcode-workspace`
  profile for root validation, release, and CI maintenance.
