---
name: sync-xcode-workspace-guidance
description: Sync guidance for an existing modular Apple workspace that has an .xcworkspace plus Apps and Packages directories. Use when auditing or aligning workspace-root AGENTS.md guidance, app-project membership, local Swift package wiring, XcodeGen workspace settings, and optional service boundaries; do not use for one standalone .xcodeproj or Package.swift repository.
---

# Sync Xcode Workspace Guidance

## Purpose

Align the root guidance for a modular Apple workspace while preserving the
separate owners of each app project and Swift package. `scripts/run_workflow.py`
detects the shape, audits its composition, and adds the bounded workspace
guidance section when needed.

## Workflow

1. Use `explore-apple-swift-docs` before changing workflow policy. Prefer Xcode
   MCP, then Dash's usable `XcodeGen : ProjectSpec` archive.
2. Run `scripts/run_workflow.py --repo-root <root>` to inspect workspace,
   projects, packages, and optional services.
3. Confirm that the root contains one `.xcworkspace`, `Apps/`, and `Packages/`.
   Report missing or misplaced projects and packages; do not repair project
   membership by editing workspace or `.pbxproj` data directly.
4. Check each app's `project.yml` for a local `packages` declaration before
   claiming it consumes a Core package. Check the package's `Package.swift` for
   its real target and product graph.
5. For generated workspace projects, verify `schemePathPrefix: "../"` where
   workspace-relative scheme paths are used. Keep XcodeGen per-project: it does
   not become the workspace source of truth.
6. Route app-specific guidance to `sync-xcode-project-guidance`, package-specific
   guidance to `sync-swift-package-guidance`, and active execution to
   `xcode-build-run-workflow` or `xcode-testing-workflow`.
7. Keep optional services under `Services/` as their own deployment and runtime
   boundary. Use the selected server skill for service-local policy.

## Audit Contract

The runtime reports:

- workspace and app-project paths;
- package paths containing `Package.swift`;
- `project.yml` paths;
- optional service roots;
- missing workspace, app-project, package, or marker-directory findings;
- the root `AGENTS.md` action taken or planned.

It does not parse XcodeGen package declarations, classify topology, or change
workspace membership, app target dependencies, package manifests, generated
projects, or service code.

## Guards And Handoffs

- Stop when the root has no `.xcworkspace`, `Apps/`, or `Packages/` marker.
- Stop when the root is a single app project or package; use the narrower sync
  skill instead.
- Do not mistake a navigator group, folder reference, or directory for a Swift
  package target.
- Do not use cross-project references to replace local package products.
- Do not hand-edit `.pbxproj` or workspace data. Make Xcode/XcodeGen-aware
  changes through the owner skill.

## References

- `references/workspace-shape.md`
- `assets/append-section.md`
