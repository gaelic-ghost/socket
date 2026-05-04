# Architecture

## Summary

This document explains the repository's product and module architecture from code evidence. Add repo-specific notes here when the layout has unusual constraints or naming.

See [SLICES.md](./SLICES.md) for provable end-to-end code paths.

## Product Map

<!-- Generated product inventory starts here. -->

- `agent-plugin-skills` (codex-plugin) uses targets: skills:plugins/agent-plugin-skills/skills.
- `apple-dev-skills` (codex-plugin) uses targets: skills:plugins/apple-dev-skills/skills, mcp:plugins/apple-dev-skills/.mcp.json.
- `cardhop-app` (codex-plugin) uses targets: skills:plugins/cardhop-app/skills, mcp:plugins/cardhop-app/.mcp.json.
- `dotnet-skills` (codex-plugin) uses targets: no targets recorded.
- `productivity-skills` (codex-plugin) uses targets: skills:plugins/productivity-skills/skills.
- `python-skills` (codex-plugin) uses targets: skills:plugins/python-skills/skills.
- `rust-skills` (codex-plugin) uses targets: no targets recorded.
- `spotify` (codex-plugin) uses targets: no targets recorded.
- `swiftasb-skills` (codex-plugin) uses targets: skills:plugins/swiftasb-skills/skills.
- `things-app` (codex-plugin) uses targets: skills:plugins/things-app/skills, mcp:plugins/things-app/.mcp.json.
- `web-dev-skills` (codex-plugin) uses targets: no targets recorded.
- `socket` (codex-plugin-marketplace) uses targets: agent-plugin-skills, apple-dev-skills, swiftasb-skills, dotnet-skills, productivity-skills, speak-swiftly, python-skills, rust-skills, cardhop-app, things-app, spotify, web-dev-skills.
- `speak-swiftly` (remote-plugin-entry) uses targets: no targets recorded.

<!-- Generated product inventory ends here. -->

## Module Architecture

<!-- Generated target inventory starts here. -->

- `skill:agent-plugin-skills/bootstrap-skills-plugin-repo` (codex-skill) at `plugins/agent-plugin-skills/skills/bootstrap-skills-plugin-repo/SKILL.md` depends on: no declared dependencies.
- `skill:agent-plugin-skills/sync-skills-repo-guidance` (codex-skill) at `plugins/agent-plugin-skills/skills/sync-skills-repo-guidance/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/apple-ui-accessibility-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/apple-ui-accessibility-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/author-swift-docc-docs` (codex-skill) at `plugins/apple-dev-skills/skills/author-swift-docc-docs/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/bootstrap-swift-package` (codex-skill) at `plugins/apple-dev-skills/skills/bootstrap-swift-package/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/bootstrap-xcode-app-project` (codex-skill) at `plugins/apple-dev-skills/skills/bootstrap-xcode-app-project/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/explore-apple-swift-docs` (codex-skill) at `plugins/apple-dev-skills/skills/explore-apple-swift-docs/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/format-swift-sources` (codex-skill) at `plugins/apple-dev-skills/skills/format-swift-sources/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/structure-swift-sources` (codex-skill) at `plugins/apple-dev-skills/skills/structure-swift-sources/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swift-package-build-run-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swift-package-build-run-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swift-package-testing-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swift-package-testing-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swift-package-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swift-package-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/swiftui-app-architecture-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/swiftui-app-architecture-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/sync-swift-package-guidance` (codex-skill) at `plugins/apple-dev-skills/skills/sync-swift-package-guidance/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/sync-xcode-project-guidance` (codex-skill) at `plugins/apple-dev-skills/skills/sync-xcode-project-guidance/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/xcode-app-project-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/xcode-app-project-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/xcode-build-run-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/xcode-build-run-workflow/SKILL.md` depends on: no declared dependencies.
- `skill:apple-dev-skills/xcode-testing-workflow` (codex-skill) at `plugins/apple-dev-skills/skills/xcode-testing-workflow/SKILL.md` depends on: no declared dependencies.
- `mcp:plugins/apple-dev-skills/.mcp.json` (mcp-config) at `plugins/apple-dev-skills/.mcp.json` depends on: no declared dependencies.
- `skill:cardhop-app/cardhop-contact-workflow` (codex-skill) at `plugins/cardhop-app/skills/cardhop-contact-workflow/SKILL.md` depends on: no declared dependencies.
- `mcp:plugins/cardhop-app/.mcp.json` (mcp-config) at `plugins/cardhop-app/.mcp.json` depends on: no declared dependencies.
- `skill:productivity-skills/explain-code-slice` (codex-skill) at `plugins/productivity-skills/skills/explain-code-slice/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-accessibility` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-accessibility/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-agents` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-agents/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-api` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-api/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-architecture` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-architecture/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-contributing` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-contributing/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-readme` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-readme/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-repo` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-repo/SKILL.md` depends on: no declared dependencies.
- `skill:productivity-skills/maintain-project-roadmap` (codex-skill) at `plugins/productivity-skills/skills/maintain-project-roadmap/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/bootstrap-python-mcp-service` (codex-skill) at `plugins/python-skills/skills/bootstrap-python-mcp-service/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/bootstrap-python-service` (codex-skill) at `plugins/python-skills/skills/bootstrap-python-service/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/bootstrap-uv-python-workspace` (codex-skill) at `plugins/python-skills/skills/bootstrap-uv-python-workspace/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/integrate-fastapi-fastmcp` (codex-skill) at `plugins/python-skills/skills/integrate-fastapi-fastmcp/SKILL.md` depends on: no declared dependencies.
- `skill:python-skills/uv-pytest-unit-testing` (codex-skill) at `plugins/python-skills/skills/uv-pytest-unit-testing/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/build-appkit-app` (codex-skill) at `plugins/swiftasb-skills/skills/build-appkit-app/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/build-swift-package` (codex-skill) at `plugins/swiftasb-skills/skills/build-swift-package/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/build-swiftui-app` (codex-skill) at `plugins/swiftasb-skills/skills/build-swiftui-app/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/choose-integration-shape` (codex-skill) at `plugins/swiftasb-skills/skills/choose-integration-shape/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/diagnose-integration` (codex-skill) at `plugins/swiftasb-skills/skills/diagnose-integration/SKILL.md` depends on: no declared dependencies.
- `skill:swiftasb-skills/explain-swiftasb` (codex-skill) at `plugins/swiftasb-skills/skills/explain-swiftasb/SKILL.md` depends on: no declared dependencies.
- `skill:things-app/things-digest-generator` (codex-skill) at `plugins/things-app/skills/things-digest-generator/SKILL.md` depends on: no declared dependencies.
- `skill:things-app/things-reminders-manager` (codex-skill) at `plugins/things-app/skills/things-reminders-manager/SKILL.md` depends on: no declared dependencies.
- `mcp:plugins/things-app/.mcp.json` (mcp-config) at `plugins/things-app/.mcp.json` depends on: no declared dependencies.

<!-- Generated target inventory ends here. -->

## Construction And Ownership

Document who creates the important runtime objects, what inputs they receive, where those inputs come from, and which module owns the responsibility. Leave unverified relationships out until they can be proven from code.

## Visual Model

The structured visual model lives in [architecture.json](./architecture.json). It is intended for a purpose-built viewer rather than generic Markdown diagrams.

## Architecture Evidence

<!-- Generated evidence starts here. -->

- `skill-manifest` evidence from `plugins/agent-plugin-skills/skills/bootstrap-skills-plugin-repo/SKILL.md`.
- `skill-manifest` evidence from `plugins/agent-plugin-skills/skills/sync-skills-repo-guidance/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/agent-plugin-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/apple-ui-accessibility-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/author-swift-docc-docs/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/bootstrap-swift-package/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/bootstrap-xcode-app-project/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/explore-apple-swift-docs/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/format-swift-sources/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/structure-swift-sources/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swift-package-build-run-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swift-package-testing-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swift-package-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/swiftui-app-architecture-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/sync-swift-package-guidance/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/sync-xcode-project-guidance/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/xcode-app-project-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/xcode-build-run-workflow/SKILL.md`.
- `skill-manifest` evidence from `plugins/apple-dev-skills/skills/xcode-testing-workflow/SKILL.md`.
- `mcp-config` evidence from `plugins/apple-dev-skills/.mcp.json`.
- `codex-plugin-manifest` evidence from `plugins/apple-dev-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/cardhop-app/skills/cardhop-contact-workflow/SKILL.md`.
- `mcp-config` evidence from `plugins/cardhop-app/.mcp.json`.
- `codex-plugin-manifest` evidence from `plugins/cardhop-app/.codex-plugin/plugin.json`.
- `codex-plugin-manifest` evidence from `plugins/dotnet-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/explain-code-slice/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-accessibility/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-agents/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-api/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-architecture/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-contributing/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-readme/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-repo/SKILL.md`.
- `skill-manifest` evidence from `plugins/productivity-skills/skills/maintain-project-roadmap/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/productivity-skills/.codex-plugin/plugin.json`.
- `skill-manifest` evidence from `plugins/python-skills/skills/bootstrap-python-mcp-service/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/bootstrap-python-service/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/bootstrap-uv-python-workspace/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/integrate-fastapi-fastmcp/SKILL.md`.
- `skill-manifest` evidence from `plugins/python-skills/skills/uv-pytest-unit-testing/SKILL.md`.
- `codex-plugin-manifest` evidence from `plugins/python-skills/.codex-plugin/plugin.json`.
- `codex-plugin-manifest` evidence from `plugins/rust-skills/.codex-plugin/plugin.json`.
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
- `codex-plugin-manifest` evidence from `plugins/web-dev-skills/.codex-plugin/plugin.json`.
- `plugin-marketplace` evidence from `.agents/plugins/marketplace.json`.

<!-- Generated evidence ends here. -->

## Staleness Checks

Refresh this document when products, targets, module boundaries, important construction paths, or recorded slices change.
