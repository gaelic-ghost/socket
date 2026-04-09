# Workflow Guidance Preservation Matrix

Date: 2026-04-08

## Purpose

Track where guidance currently carried by the monolithic execution skills moves as narrower execution skills land, so the split does not silently drop policy, handoff rules, or implementation guidance.

## Swift Package Guidance

| Guidance Area | Current Home | Future Primary Home | AGENTS.md Promotion | Notes |
| --- | --- | --- | --- | --- |
| Apple and Swift docs gate | `swift-package-workflow/SKILL.md` | `swift-package-build-run-workflow/SKILL.md` and `swift-package-testing-workflow/SKILL.md` | existing package `AGENTS.md` baseline should keep the durable docs-first rule | Execution skills still restate the gate because it affects every operation path. |
| Simplicity-first Swift and shape-preserving policy | `references/snippets/apple-swift-package-core.md` | shared snippet plus both narrower package skills | yes, via bootstrap and sync guidance assets | Durable repo policy belongs in synced and bootstrapped `AGENTS.md`, with the skills still recommending the snippet. |
| Structured concurrency, cancellation, sendability, and async test discipline | `references/snippets/apple-swift-package-core.md` and `references/package-resources-testing-and-builds.md` | shared snippet plus `swift-package-testing-workflow` | yes | Test-specific concurrency reminders stay closest to the testing skill. |
| Manifest edits, dependency changes, targets, products, and plugins | `swift-package-workflow/SKILL.md` and `references/cli-command-matrix.md` | `swift-package-build-run-workflow` | no | Build/run owns these because they are package-shape and execution-surface concerns rather than durable repo policy. |
| Package resources, `Bundle.module`, `.process(...)`, `.copy(...)`, `.embedInCode(...)` | `references/package-resources-testing-and-builds.md` | `swift-package-build-run-workflow` | yes | The durable “how this repo expects package resources to be organized” guidance should move into synced package `AGENTS.md` output. |
| Metal library packaging, distribution, and Xcode handoff | `references/package-resources-testing-and-builds.md` | `swift-package-build-run-workflow` | yes | Keep the operational handoff logic in the skill, but promote the durable package-layout expectations into package `AGENTS.md`. |
| Swift Testing, XCTest holdouts, test fixtures, and `.xctestplan` usage | `references/package-resources-testing-and-builds.md` | `swift-package-testing-workflow` | yes | Testing policy belongs in both the testing skill and package `AGENTS.md` output. |
| Debug versus Release validation and tagged-release expectations | `references/package-resources-testing-and-builds.md` | `swift-package-build-run-workflow` and `swift-package-testing-workflow` | yes | Release expectations are durable enough to belong in package `AGENTS.md` templates. |
| Mixed-root detection and Xcode handoff | `references/xcode-handoff-conditions.md` | both narrower package skills | no | This remains an execution-time routing concern. |
| Plugin update, downstream-guidance sync, and local install refresh | `swift-package-workflow/SKILL.md` | both narrower package skills | yes | Repo-maintenance recommendations should also be reflected in synced maintainer guidance where appropriate. |
| Repo-maintenance toolkit profile identity | bootstrap and sync installer calls plus vendored toolkit snapshot | shared `repo-maintenance-toolkit` installer contract and synced package `AGENTS.md` output | yes | Package repos should install and validate the `swift-package` profile explicitly rather than relying on an unnamed toolkit snapshot. |

## Xcode Guidance

| Guidance Area | Current Home | Future Primary Home | AGENTS.md Promotion | Notes |
| --- | --- | --- | --- | --- |
| Apple docs gate | `xcode-app-project-workflow/SKILL.md` | `xcode-build-run-workflow` and `xcode-testing-workflow` | existing Xcode `AGENTS.md` baseline should keep the durable docs-first rule | Same rule as the package side: keep the gate both durable and local to execution skills. |
| Simplicity-first Swift, SwiftUI architecture, logging, and telemetry guidance | `references/snippets/apple-xcode-project-core.md` | shared snippet plus both narrower Xcode skills | yes | Durable repo standards belong in synced Xcode `AGENTS.md` output. |
| Xcode workspace inspection, diagnostics, schemes, destinations, and build or run flows | `xcode-app-project-workflow/SKILL.md` and `references/mcp-tool-matrix.md` | `xcode-build-run-workflow` | no | Operational execution guidance stays in the build/run skill. |
| Swift Testing, XCTest, XCUITest, destinations, filters, retries, and `.xctestplan` usage | `references/testing-plans-file-membership-and-configurations.md` | `xcode-testing-workflow` | yes | Durable repo expectations for test plans should move into synced Xcode `AGENTS.md` where relevant. |
| File-membership and target-membership verification after on-disk edits | `references/testing-plans-file-membership-and-configurations.md` | `xcode-build-run-workflow` | yes | This is exactly the kind of durable repo policy that should show up in synced Xcode `AGENTS.md`. |
| Debug versus Release configuration guidance | `references/testing-plans-file-membership-and-configurations.md` | both narrower Xcode skills | yes | Build and test skills both need it, and repo policy should reinforce it. |
| `.pbxproj` direct-edit warning boundary | `references/mutation-risk-policy.md` | `xcode-build-run-workflow` | yes | The runtime warning behavior stays in the skill; the baseline repo rule belongs in `AGENTS.md`. |
| MCP-first execution and official CLI fallback shape | `references/workflow-policy.md` and `references/cli-fallback-matrix.md` | both narrower Xcode skills | no | This is execution behavior, not durable repo policy. |
| Plugin update, downstream-guidance sync, and local install refresh | `xcode-app-project-workflow/SKILL.md` | both narrower Xcode skills | yes | Maintainer-facing reminders can also live in synced guidance. |
| Repo-maintenance toolkit profile identity | bootstrap and sync installer calls plus vendored toolkit snapshot | shared `repo-maintenance-toolkit` installer contract and synced Xcode `AGENTS.md` output | yes | Xcode repos should install and validate the `xcode-app` profile explicitly rather than relying on an unnamed toolkit snapshot. |

## Split Readiness Checklist

- [x] The matrix exists in-repo before the first real execution split lands.
- [x] Every row above is mapped to a concrete destination when each narrower skill is added.
- [x] Bootstrap and sync `AGENTS.md` assets absorb the durable rows marked for promotion.
- [ ] The old monolithic skills stop being primary guidance owners once all rows have a maintained destination.
