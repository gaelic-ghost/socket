---
name: bootstrap-xcode-app-project
description: Compatibility handoff for legacy requests to bootstrap one Xcode app project. New Apple product work uses bootstrap-xcode-workspace.
---

# Bootstrap Xcode App Project

## Purpose

Recognize legacy standalone-app requests and move new product work to the one
root-workspace bootstrap contract.

## Status

New Apple products do not begin as standalone app projects. Use
`bootstrap-xcode-workspace`: it creates one root workspace, one root XcodeGen
project, `Apps/` target directories, and local Swift packages under `Packages/`.

This retained skill exists only to recognize an older request and redirect it
without reviving the hand-managed Xcode project path. Its XcodeGen scaffold
helpers remain internal template implementation details during migration.

## When To Use

Use only to recognize a legacy standalone-app request. For all new product work,
use `bootstrap-xcode-workspace`.

## Single-Path Workflow

1. Collect the product name, file prefix, product platforms, and organization
   identifier.
2. Run `bootstrap-xcode-workspace` with those values.
3. Add the requested platform as a target under `Apps/`; do not create an app
   `.xcodeproj` below `Apps/`.
4. Edit root `project.yml`, included target specs, `.xcconfig` layers, and
   local package manifests; regenerate with XcodeGen.

## Inputs

Carry the legacy request's product name, file prefix, platform list, and
organization identifier into `bootstrap-xcode-workspace`.

## Outputs

The canonical workspace bootstrap is the output; this compatibility handoff
does not create a standalone project.

## Guards and Stop Conditions

## Guard

- Do not choose `xcode`, a manually authored `.pbxproj`, or another project
  generator. XcodeGen is the only authoring path for new Apple product project
  data.
- Hand GitHub repository features, settings, branch protection, rulesets, and security automation to
  `repository-skills:maintain-github-repository`.

## Fallbacks and Handoffs

For a truly independent reusable package, use `bootstrap-swift-package`.

## Companion Plugin Requirement

The canonical bootstrap installs repository maintenance through
`repository-skills:maintain-project-repo`. Install both plugins from the Socket
marketplace: <https://github.com/gaelic-ghost/socket>.

## Customization

Configure project details in the canonical workspace bootstrap; do not restore
a standalone Xcode project generator setting.

## References

- `bootstrap-xcode-workspace`
- `references/snippets/apple-swift-core.md`
- `references/snippets/apple-xcode-project-core.md`

Recommend `references/snippets/apple-xcode-project-core.md` when the migration
needs the shared Xcode project-integrity baseline.
