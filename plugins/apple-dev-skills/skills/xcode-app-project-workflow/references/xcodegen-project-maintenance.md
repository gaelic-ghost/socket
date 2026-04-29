# XcodeGen Project Maintenance

## Purpose

Use this reference only to route broad existing-project requests when the repository is XcodeGen-backed.

Authoritative XcodeGen references:

- [XcodeGen Project Spec documentation](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html)
- [XcodeGen repository](https://github.com/yonaskolb/XcodeGen)

## Routing

- If the request touches generated project structure in `project.yml`, `project.yaml`, included specs, targets, schemes, settings, packages, or file membership, route to `xcode-build-run-workflow`.
- If the request is primarily about generated test targets, scheme test actions, launch arguments, environment variables, or `.xctestplan` references, route to `xcode-testing-workflow`.
- Preserve the direct `.pbxproj` warning boundary for hand-edited project files, but treat generated `.pbxproj` diffs as reviewed output when they come from `xcodegen generate`.
- Do not introduce XcodeGen into a hand-managed Xcode project unless the user explicitly asks for that migration.
