<!-- socket-managed:begin workspace-agents -->
# AGENTS.md

This repository is one Apple product workspace. Read `CONTRIBUTING.md` for the
command contract, setup, validation, testing, and release procedures.

## Workspace ownership

- `project.yml` and included `Apps/**/target.yml` files own Xcode project data.
- `Apps/` owns platform app and test targets; `Packages/` owns shared SwiftPM
  modules. Edit sources, specs, `.xcconfig` files, and `Package.swift`; never
  hand-edit generated `.pbxproj` data.
- Run `just align` after updating Socket-managed guidance or project sources.
- The nested `Apps/AGENTS.md` and `Packages/AGENTS.md` add scoped guidance and
  inherit this file.
<!-- socket-managed:end workspace-agents -->

<!-- repository-specific:begin -->
<!-- Add repository-specific contributor and agent guidance below this line. -->
<!-- repository-specific:end -->
