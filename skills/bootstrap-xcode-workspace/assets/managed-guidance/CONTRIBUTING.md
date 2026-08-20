<!-- socket-managed:begin workspace-contributing -->
# Contributing

## Setup

Run `just setup` after cloning. It verifies the local toolchain and activates
the checked-in Git hooks for this repository.

## Daily commands

- `just align` refreshes Socket-managed guidance and hooks, then regenerates
  the root Xcode project.
- `just validate` runs formatting, lint, package, and workspace validation.
- `just test <AppTarget>` runs the app's unit tests; use Xcode's shared test
  schemes for unit, UI, or combined test runs.
- Use `swift test` from the owning directory under `Packages/` or `Services/`.
- Run local service dependencies through Homebrew services. Linux artifacts and
  test or production deployments run only in GitHub Actions.

## Project changes

Edit XcodeGen specs, checked-in `.xcconfig` files, package manifests, and
source files. Regenerate with `just align`; never hand-edit generated project
files. App release commands use the named Staging, App Store, AltStore, and
Direct Distribution schemes.
<!-- socket-managed:end workspace-contributing -->

<!-- repository-specific:begin -->
<!-- Add repository-specific contribution policy below this line. -->
<!-- repository-specific:end -->
