<!-- socket-managed:begin workspace-packages-agents -->
# Packages guidance

This directory inherits the repository-root `AGENTS.md`.

- `ProductCore` is the product package and public façade; its feature modules
  keep domain, UI, and service responsibilities separate.
- Use SwiftPM for package builds and tests. Package targets default to
  `nonisolated`; app adaptation belongs under `Apps/`.
<!-- socket-managed:end workspace-packages-agents -->

<!-- repository-specific:begin -->
<!-- Add Packages-specific guidance below this line. -->
<!-- repository-specific:end -->
