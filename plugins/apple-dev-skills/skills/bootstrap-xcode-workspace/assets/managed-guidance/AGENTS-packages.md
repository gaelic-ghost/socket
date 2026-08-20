<!-- socket-managed:begin workspace-packages-agents -->
# Packages guidance

This directory inherits the repository-root `AGENTS.md`.

- `ProductCore` is the product package and public façade; its feature modules
  keep domain, UI, and service responsibilities separate.
- Use SwiftPM for package builds and tests. Package targets default to
  `nonisolated`; app adaptation belongs under `Apps/`.
- Use `swift-package-build-run-workflow` for manifest, dependency, resource,
  build, and executable work; use `swift-package-testing-workflow` for package
  tests; use `swift-package-extension-workflow` for plugins, macros, traits,
  generated sources, and permission-sensitive package extensions.
- Keep SwiftPM resources explicit: choose `Resource.process(...)`,
  `Resource.copy(...)`, or `Resource.embedInCode(...)` deliberately and access
  target resources through `Bundle.module`.
- Keep Xcode-owned `.xctestplan`, scheme, destination, and UI-test state in the
  root workspace. Validate material package behavior in both Debug and Release.
<!-- socket-managed:end workspace-packages-agents -->

<!-- repository-specific:begin -->
<!-- Add Packages-specific guidance below this line. -->
<!-- repository-specific:end -->
