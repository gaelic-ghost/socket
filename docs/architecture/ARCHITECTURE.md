# Architecture

## Summary

This document explains the repository's product and module architecture from code evidence. Add repo-specific notes here when the layout has unusual constraints or naming.

See [SLICES.md](./SLICES.md) for provable end-to-end code paths.

## Product Map

<!-- Generated product inventory starts here. -->

- `agent-portability-skills` (codex-plugin) uses targets: skills:plugins/agent-portability-skills/skills.
- `android-dev-skills` (codex-plugin) uses targets: no targets recorded.
- `apple-dev-skills` (codex-plugin) uses targets: skills:plugins/apple-dev-skills/skills, mcp:plugins/apple-dev-skills/.mcp.json.
- `cardhop-app` (codex-plugin) uses targets: skills:plugins/cardhop-app/skills, mcp:plugins/cardhop-app/.mcp.json.
- `agentdeck` (codex-plugin) uses targets: no targets recorded.
- `dotnet-skills` (codex-plugin) uses targets: skills:plugins/dotnet-skills/skills.
- `productivity-skills` (codex-plugin) uses targets: skills:plugins/productivity-skills/skills, mcp:plugins/productivity-skills/.mcp.json.
- `python-skills` (codex-plugin) uses targets: skills:plugins/python-skills/skills.
- `reverse-engineering-skills` (codex-plugin) uses targets: skills:plugins/reverse-engineering-skills/skills.
- `rust-skills` (codex-plugin) uses targets: skills:plugins/rust-skills/skills.
- `server-side-jvm` (codex-plugin) uses targets: skills:plugins/server-side-jvm/skills.
- `server-side-swift` (codex-plugin) uses targets: skills:plugins/server-side-swift/skills.
- `spotify` (codex-plugin) uses targets: no targets recorded.
- `swiftasb-skills` (codex-plugin) uses targets: skills:plugins/swiftasb-skills/skills.
- `things-app` (codex-plugin) uses targets: skills:plugins/things-app/skills, mcp:plugins/things-app/.mcp.json.
- `web-dev-skills` (codex-plugin) uses targets: skills:plugins/web-dev-skills/skills.
- `socket` (codex-plugin-marketplace) uses targets: agent-portability-skills, android-dev-skills, apple-dev-skills, cardhop-app, dotnet-skills, productivity-skills, python-skills, server-side-swift, server-side-jvm, rust-skills, speak-swiftly, swiftasb-skills, things-app, spotify, web-dev-skills, reverse-engineering-skills, agentdeck.
- `speak-swiftly` (remote-plugin-entry) uses targets: no targets recorded.

<!-- Generated product inventory ends here. -->

## Module Architecture

<!-- Generated target inventory starts here. -->

- `skill:agent-portability-skills/bootstrap-skills-plugin-repo` (codex-skill) at `plugins/agent-portability-skills/skills/bootstrap-skills-plugin-repo/SKILL.md` depends on: no declared dependencies.
- `skill:agent-portability-skills/sync-skills-repo-guidance` (codex-skill) at `plugins/agent-portability-skills/skills/sync-skills-repo-guidance/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/appkit-app-architecture-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/appkit-app-architecture-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/apple-ui-accessibility-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/apple-ui-accessibility-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/author-swift-docc-docs` (codex-skill) at `plugins/apple-dev-skills/skills/author-swift-docc-docs/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/bootstrap-swift-package` (codex-skill) at `plugins/apple-dev-skills/skills/bootstrap-swift-package/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/bootstrap-xcode-app-project` (codex-skill) at `plugins/apple-dev-skills/skills/bootstrap-xcode-app-project/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/explore-apple-swift-docs` (codex-skill) at `plugins/apple-dev-skills/skills/explore-apple-swift-docs/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/format-swift-sources` (codex-skill) at `plugins/apple-dev-skills/skills/format-swift-sources/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/icon-composer-app-icon-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/icon-composer-app-icon-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/safari-extension-control-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/safari-extension-control-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/structure-swift-sources` (codex-skill) at `plugins/apple-dev-skills/skills/structure-swift-sources/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swift-openapi-client-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swift-openapi-client-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swift-package-build-run-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swift-package-build-run-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swift-package-testing-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swift-package-testing-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swift-package-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swift-package-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swiftui-app-architecture-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swiftui-app-architecture-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/sync-swift-package-guidance` (codex-skill) at `plugins/apple-dev-skills/skills/sync-swift-package-guidance/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/sync-xcode-project-guidance` (codex-skill) at `plugins/apple-dev-skills/skills/sync-xcode-project-guidance/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/xcode-app-project-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/xcode-app-project-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/xcode-build-run-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/xcode-build-run-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/xcode-coding-intelligence-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/xcode-coding-intelligence-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/xcode-testing-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/xcode-testing-workflow/SKILL.md` depends on: no declared dependencies.
- `mcp:plugins/apple-dev-skills/.mcp.json` (mcp-config) at `plugins/apple-dev-skills/.mcp.json` depends on: no declared dependencies.
- `skill:cardhop-app/cardhop-contact-workflow` (codex-skill) at `plugins/cardhop-app/skills/cardhop-contact-workflow/SKILL.md` depends on: no declared dependencies.
- `mcp:plugins/cardhop-app/.mcp.json` (mcp-config) at `plugins/cardhop-app/.mcp.json` depends on: no declared dependencies.
- `skill:dotnet-skills/aspnet-core-service-workflow` (codex-skill) at `plugins/dotnet-skills/skills/aspnet-core-service-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/bootstrap-solution` (codex-skill) at `plugins/dotnet-skills/skills/bootstrap-solution/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/build-csharp-project` (codex-skill) at `plugins/dotnet-skills/skills/build-csharp-project/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/build-fsharp-project` (codex-skill) at `plugins/dotnet-skills/skills/build-fsharp-project/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/choose-project-shape` (codex-skill) at `plugins/dotnet-skills/skills/choose-project-shape/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/ci-workflow` (codex-skill) at `plugins/dotnet-skills/skills/ci-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/diagnose-project` (codex-skill) at `plugins/dotnet-skills/skills/diagnose-project/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/fsharp-csharp-interop` (codex-skill) at `plugins/dotnet-skills/skills/fsharp-csharp-interop/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/package-workflow` (codex-skill) at `plugins/dotnet-skills/skills/package-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/testing-workflow` (codex-skill) at `plugins/dotnet-skills/skills/testing-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/tooling-style-workflow` (codex-skill) at `plugins/dotnet-skills/skills/tooling-style-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:dotnet-skills/upgrade-workflow` (codex-skill) at `plugins/dotnet-skills/skills/upgrade-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/codex-gui-worktree-workflow` (codex-skill) at `plugins/productivity-skills/skills/codex-gui-worktree-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/design-agent-automation-workflow` (codex-skill) at `plugins/productivity-skills/skills/design-agent-automation-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/design-agent-eval-workflow` (codex-skill) at `plugins/productivity-skills/skills/design-agent-eval-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/dice-job-search-workflow` (codex-skill) at `plugins/productivity-skills/skills/dice-job-search-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/explain-code-slice` (codex-skill) at `plugins/productivity-skills/skills/explain-code-slice/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-github-repository` (codex-skill) at `plugins/productivity-skills/skills/maintain-github-repository/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-accessibility` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-accessibility/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-agents` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-agents/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-api` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-api/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-architecture` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-architecture/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-contributing` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-contributing/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-docs` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-docs/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-readme` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-readme/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-repo` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-repo/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-roadmap` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-roadmap/SKILL.md` depends on: no declared dependencies.
- `mcp:plugins/productivity-skills/.mcp.json` (mcp-config) at `plugins/productivity-skills/.mcp.json` depends on: no declared dependencies.
- `skill:python-skills/bootstrap-python-mcp-service` (codex-skill) at `plugins/python-skills/skills/bootstrap-python-mcp-service/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/bootstrap-python-service` (codex-skill) at `plugins/python-skills/skills/bootstrap-python-service/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/bootstrap-uv-python-workspace` (codex-skill) at `plugins/python-skills/skills/bootstrap-uv-python-workspace/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/build-python-project` (codex-skill) at `plugins/python-skills/skills/build-python-project/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/choose-python-project-shape` (codex-skill) at `plugins/python-skills/skills/choose-python-project-shape/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/diagnose-python-project` (codex-skill) at `plugins/python-skills/skills/diagnose-python-project/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/integrate-fastapi-fastmcp` (codex-skill) at `plugins/python-skills/skills/integrate-fastapi-fastmcp/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/python-ci-workflow` (codex-skill) at `plugins/python-skills/skills/python-ci-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/python-package-workflow` (codex-skill) at `plugins/python-skills/skills/python-package-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/python-tooling-style-workflow` (codex-skill) at `plugins/python-skills/skills/python-tooling-style-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/python-upgrade-workflow` (codex-skill) at `plugins/python-skills/skills/python-upgrade-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/uv-pytest-unit-testing` (codex-skill) at `plugins/python-skills/skills/uv-pytest-unit-testing/SKILL.md` depends on: no declared dependencies.
- `skill:reverse-engineering-skills/evidence-notes-workflow` (codex-skill) at `plugins/reverse-engineering-skills/skills/evidence-notes-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:reverse-engineering-skills/triage-artifact` (codex-skill) at `plugins/reverse-engineering-skills/skills/triage-artifact/SKILL.md` depends on: no declared dependencies.
- `skill:rust-skills/bootstrap-cargo-project` (codex-skill) at `plugins/rust-skills/skills/bootstrap-cargo-project/SKILL.md` depends on: no declared dependencies.
- `skill:rust-skills/build-cli-project` (codex-skill) at `plugins/rust-skills/skills/build-cli-project/SKILL.md` depends on: no declared dependencies.
- `skill:rust-skills/build-library-crate` (codex-skill) at `plugins/rust-skills/skills/build-library-crate/SKILL.md` depends on: no declared dependencies.
- `skill:rust-skills/choose-project-shape` (codex-skill) at `plugins/rust-skills/skills/choose-project-shape/SKILL.md` depends on: no declared dependencies.
- `skill:rust-skills/ci-workflow` (codex-skill) at `plugins/rust-skills/skills/ci-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:rust-skills/package-workflow` (codex-skill) at `plugins/rust-skills/skills/package-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:rust-skills/testing-workflow` (codex-skill) at `plugins/rust-skills/skills/testing-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:rust-skills/tooling-style-workflow` (codex-skill) at `plugins/rust-skills/skills/tooling-style-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-jvm/build-java-service` (codex-skill) at `plugins/server-side-jvm/skills/build-java-service/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-jvm/build-scala-service` (codex-skill) at `plugins/server-side-jvm/skills/build-scala-service/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-jvm/build-tooling-workflow` (codex-skill) at `plugins/server-side-jvm/skills/build-tooling-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-jvm/choose-service-shape` (codex-skill) at `plugins/server-side-jvm/skills/choose-service-shape/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-jvm/testing-workflow` (codex-skill) at `plugins/server-side-jvm/skills/testing-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/app-sync-workflow` (codex-skill) at `plugins/server-side-swift/skills/app-sync-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/apple-containerization-workflow` (codex-skill) at `plugins/server-side-swift/skills/apple-containerization-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/auth-authorization-workflow` (codex-skill) at `plugins/server-side-swift/skills/auth-authorization-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/bootstrap-hummingbird-service` (codex-skill) at `plugins/server-side-swift/skills/bootstrap-hummingbird-service/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/bootstrap-vapor-service` (codex-skill) at `plugins/server-side-swift/skills/bootstrap-vapor-service/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/docker-workflow` (codex-skill) at `plugins/server-side-swift/skills/docker-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/fly-io-deployment-workflow` (codex-skill) at `plugins/server-side-swift/skills/fly-io-deployment-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/hummingbird-server-workflow` (codex-skill) at `plugins/server-side-swift/skills/hummingbird-server-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/observability-tracing-workflow` (codex-skill) at `plugins/server-side-swift/skills/observability-tracing-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/openapi-rpc-workflow` (codex-skill) at `plugins/server-side-swift/skills/openapi-rpc-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/persistence-workflow` (codex-skill) at `plugins/server-side-swift/skills/persistence-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/sync-hummingbird-service-guidance` (codex-skill) at `plugins/server-side-swift/skills/sync-hummingbird-service-guidance/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/swiftnio-workflow` (codex-skill) at `plugins/server-side-swift/skills/swiftnio-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:server-side-swift/vapor-server-workflow` (codex-skill) at `plugins/server-side-swift/skills/vapor-server-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/build-appkit-app` (codex-skill) at `plugins/swiftasb-skills/skills/build-appkit-app/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/build-swift-package` (codex-skill) at `plugins/swiftasb-skills/skills/build-swift-package/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/build-swiftui-app` (codex-skill) at `plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/choose-integration-shape` (codex-skill) at `plugins/swiftasb-skills/skills/choose-integration-shape/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/diagnose-integration` (codex-skill) at `plugins/swiftasb-skills/skills/diagnose-integration/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/explain-swiftasb` (codex-skill) at `plugins/swiftasb-skills/skills/explain-swiftasb/SKILL.md` depends on: no declared dependencies.
- `skill:things-app/things-digest-generator` (codex-skill) at `plugins/things-app/skills/things-digest-generator/SKILL.md` depends on: no declared dependencies.
- `skill:things-app/things-reminders-manager` (codex-skill) at `plugins/things-app/skills/things-reminders-manager/SKILL.md` depends on: no declared dependencies.
- `mcp:plugins/things-app/.mcp.json` (mcp-config) at `plugins/things-app/.mcp.json` depends on: no declared dependencies.
- `skill:web-dev-skills/expo-inline-native-modules-workflow` (codex-skill) at `plugins/web-dev-skills/skills/expo-inline-native-modules-workflow/SKILL.md` depends on: no declared dependencies.

<!-- Generated target inventory ends here. -->

## Construction And Ownership

Document who creates the important runtime objects, what inputs they receive, where those inputs come from, and which module owns the responsibility. Leave unverified relationships out until they can be proven from code.

## Visual Model

The structured visual model lives in [architecture.json](./architecture.json). It is intended for a purpose-built viewer rather than generic Markdown diagrams.

## Architecture Evidence

<!-- Generated evidence starts here. -->

- `skill-manifest` evidence from `plugins/agent-portability-skills/skills/bootstrap-skills-plugin-repo/SKILL.md`.
- `skill-manifest` evidence from `plugins/agent-portability-skills/skills/sync-skills-repo-guidance/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/agent-portability-skills/.codex-plugin/plugin.json`.
- `codex-plugin-manifest` evidence from `plugins/android-dev-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/appkit-app-architecture-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/apple-ui-accessibility-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/author-swift-docc-docs/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/bootstrap-swift-package/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/bootstrap-xcode-app-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/explore-apple-swift-docs/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/format-swift-sources/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/icon-composer-app-icon-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/safari-extension-control-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/structure-swift-sources/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swift-openapi-client-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swift-package-build-run-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swift-package-testing-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swift-package-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swiftui-app-architecture-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/sync-swift-package-guidance/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/sync-xcode-project-guidance/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/xcode-app-project-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/xcode-build-run-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/xcode-coding-intelligence-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/xcode-testing-workflow/SKILL.md`.
- `mcp-config` evidence from `plugins/apple-dev-skills/.mcp.json`.
- `codex-plugin-manifest` evidence from `plugins/apple-dev-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/cardhop-app/skills/cardhop-contact-workflow/SKILL.md`.
- `mcp-config` evidence from `plugins/cardhop-app/.mcp.json`.
- `codex-plugin-manifest` evidence from `plugins/cardhop-app/.codex-plugin/plugin.json`.
- `codex-plugin-manifest` evidence from `plugins/agentdeck/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/aspnet-core-service-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/bootstrap-solution/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/build-csharp-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/build-fsharp-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/choose-project-shape/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/ci-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/diagnose-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/fsharp-csharp-interop/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/package-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/testing-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/tooling-style-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/dotnet-skills/skills/upgrade-workflow/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/dotnet-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/codex-gui-worktree-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/design-agent-automation-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/design-agent-eval-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/dice-job-search-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/explain-code-slice/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-github-repository/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-accessibility/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-agents/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-api/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-architecture/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-contributing/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-docs/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-readme/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-repo/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-roadmap/SKILL.md`.
- `mcp-config` evidence from `plugins/productivity-skills/.mcp.json`.
- `codex-plugin-manifest` evidence from `plugins/productivity-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/python-skills/skills/bootstrap-python-mcp-service/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/bootstrap-python-service/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/bootstrap-uv-python-workspace/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/build-python-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/choose-python-project-shape/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/diagnose-python-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/integrate-fastapi-fastmcp/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/python-ci-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/python-package-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/python-tooling-style-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/python-upgrade-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/uv-pytest-unit-testing/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/python-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/reverse-engineering-skills/skills/evidence-notes-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/reverse-engineering-skills/skills/triage-artifact/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/reverse-engineering-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/rust-skills/skills/bootstrap-cargo-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/rust-skills/skills/build-cli-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/rust-skills/skills/build-library-crate/SKILL.md`.
- `skill-manifest` evidence from `plugins/rust-skills/skills/choose-project-shape/SKILL.md`.
- `skill-manifest` evidence from `plugins/rust-skills/skills/ci-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/rust-skills/skills/package-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/rust-skills/skills/testing-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/rust-skills/skills/tooling-style-workflow/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/rust-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/server-side-jvm/skills/build-java-service/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-jvm/skills/build-scala-service/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-jvm/skills/build-tooling-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-jvm/skills/choose-service-shape/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-jvm/skills/testing-workflow/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/server-side-jvm/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/app-sync-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/apple-containerization-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/auth-authorization-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/bootstrap-hummingbird-service/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/bootstrap-vapor-service/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/docker-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/fly-io-deployment-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/hummingbird-server-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/observability-tracing-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/openapi-rpc-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/persistence-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/sync-hummingbird-service-guidance/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/swiftnio-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/server-side-swift/skills/vapor-server-workflow/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/server-side-swift/.codex-plugin/plugin.json`.
- `codex-plugin-manifest` evidence from `plugins/spotify/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/swiftasb-skills/skills/build-appkit-app/SKILL.md`.
- `skill-manifest` evidence from `plugins/swiftasb-skills/skills/build-swift-package/SKILL.md`.
- `skill-manifest` evidence from `plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md`.
- `skill-manifest` evidence from `plugins/swiftasb-skills/skills/choose-integration-shape/SKILL.md`.
- `skill-manifest` evidence from `plugins/swiftasb-skills/skills/diagnose-integration/SKILL.md`.
- `skill-manifest` evidence from `plugins/swiftasb-skills/skills/explain-swiftasb/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/swiftasb-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/things-app/skills/things-digest-generator/SKILL.md`.
- `skill-manifest` evidence from `plugins/things-app/skills/things-reminders-manager/SKILL.md`.
- `mcp-config` evidence from `plugins/things-app/.mcp.json`.
- `codex-plugin-manifest` evidence from `plugins/things-app/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/web-dev-skills/skills/expo-inline-native-modules-workflow/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/web-dev-skills/.codex-plugin/plugin.json`.
- `plugin-marketplace` evidence from `.agents/plugins/marketplace.json`.

<!-- Generated evidence ends here. -->

## Staleness Checks

Refresh this document when products, targets, module boundaries, important construction paths, or recorded slices change.
