<!-- socket-managed:begin workspace-apps-agents -->
# Apps guidance

This directory inherits the repository-root `AGENTS.md`.

- Each sibling target directory owns one app, unit-test, or UI-test target and
  its target-local XcodeGen spec and configurations.
- Keep platform-specific code in its app target. Put reusable product logic,
  shared views, and clients in `Packages/`.
- Regenerate the root project with `just align`; do not edit generated project
  data in Xcode.
<!-- socket-managed:end workspace-apps-agents -->

<!-- repository-specific:begin -->
<!-- Add Apps-specific guidance below this line. -->
<!-- repository-specific:end -->
