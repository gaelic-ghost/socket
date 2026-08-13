---
name: sync-xcode-workspace-guidance
description: Audit and sync guidance for one Apple product workspace with one root XcodeGen project, Apps target specs, and Packages local Swift packages.
---

# Sync Apple Product Workspace Guidance

## Purpose

Align an existing Apple product root with the canonical single-workspace model.
The runner audits the root workspace and generated project, `project.yml`,
shared YAML and `.xcconfig` layers, target specs under `Apps/`, and local
packages under `Packages/`. It adds only bounded root guidance; it does not
edit generated project data, target membership, or package manifests.

## Workflow

1. Apply the Apple documentation gate through `explore-apple-swift-docs`.
2. Run `scripts/run_workflow.py --repo-root <root>`.
3. Require exactly one root `.xcworkspace`, exactly one root `.xcodeproj`, and
   root `project.yml`.
4. Require `Apps/apps-shared.yml`, `Apps/Apps-shared.xcconfig`, at least one
   `Apps/**/target.yml`, `Packages/packages-shared.yml`, and at least one
   `Packages/**/Package.swift`.
5. Correct the owning source, run `xcodegen generate --spec project.yml`, and
   validate with the root workspace. Do not repair `.pbxproj` data directly.

## Guards And Handoffs

- Stop if the root is not the canonical product workspace shape.
- Do not route each `Apps/` directory to standalone project sync: those
  directories are target-owned portions of the one root project.
- Use `sync-swift-package-guidance` only for a deliberately standalone package
  repository, not a package below this product's `Packages/` directory.
- Hand active building, running, diagnostics, and test work to the appropriate
  Xcode workflow after this composition audit.
