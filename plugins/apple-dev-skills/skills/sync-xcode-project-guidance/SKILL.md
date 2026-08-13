---
name: sync-xcode-project-guidance
description: Compatibility handoff for legacy standalone Xcode project guidance. Product work uses sync-xcode-workspace-guidance.
---

# Sync Xcode Project Guidance

## Purpose

Recognize a legacy standalone project and plan its migration to the canonical
root workspace without perpetuating a second new-product path.

## Status

For an Apple product repository, use `sync-xcode-workspace-guidance`. Its root
`project.yml` is the project authority; `Apps/` directories are target-owned
fragments, not standalone app-project roots.

Use this skill only to identify a genuinely legacy standalone project and plan
its migration to the canonical workspace. Do not add guidance that preserves a
new standalone-app bootstrap path.

## When To Use

Use only to identify and migrate a legacy standalone Xcode project. Product
workspace guidance belongs to `sync-xcode-workspace-guidance`.

## Single-Path Workflow

1. Audit the existing project without hand-editing `.pbxproj` data.
2. Create the canonical root workspace through `bootstrap-xcode-workspace`.
3. Move target-owned source, resource, entitlement, and configuration files
   into `Apps/<Target>/`.
4. Express target graph and build settings through root XcodeGen sources, then
   validate from the root workspace.

Hand GitHub repository features, settings, branch protection, rulesets, and security automation to
`repository-skills:maintain-github-repository`.

## Inputs

Provide the legacy project root and the intended canonical product workspace
root.

## Outputs

The result is a migration handoff, not a second project-guidance baseline.

## Guards and Stop Conditions

- Do not sync target guidance as though `Apps/` contained child projects.
- Do not hand-edit generated project data.

## Fallbacks and Handoffs

Use `sync-xcode-workspace-guidance` once the canonical root exists.

## Companion Plugin Requirement

Workspace maintenance is supplied by `repository-skills:maintain-project-repo`.
Install both plugins from the Socket marketplace:
<https://github.com/gaelic-ghost/socket>.

## Customization

Place durable product customization in root and target-owned canonical source
files, not in a legacy standalone guidance profile.

## References

- `sync-xcode-workspace-guidance`
- `references/snippets/apple-xcode-project-core.md`

Recommend `references/snippets/apple-xcode-project-core.md` when auditing the
legacy project's source-of-truth boundaries.
