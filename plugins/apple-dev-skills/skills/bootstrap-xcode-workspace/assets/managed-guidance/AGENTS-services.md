<!-- socket-managed:begin workspace-services-agents -->
# Services guidance

This directory inherits the repository-root `AGENTS.md`.

- Each child is a deployable SwiftPM executable package and appears in the root workspace.
- Build and test services natively on macOS. Use Homebrew services for local dependencies; do not start a Linux VM or local container runtime.
- Linux release artifacts, live-test deployments, and production deployments are GitHub Actions responsibilities.
- Framework-specific service creation and alignment belong to the server-side Swift component adapter invoked through the workspace entrypoint.
<!-- socket-managed:end workspace-services-agents -->

<!-- repository-specific:begin -->
<!-- Add Services-specific guidance below this line. -->
<!-- repository-specific:end -->
