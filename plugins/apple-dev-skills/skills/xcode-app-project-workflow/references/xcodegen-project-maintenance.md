# XcodeGen Project Maintenance

## Purpose

Use this reference only to route broad existing-project requests when the repository is XcodeGen-backed.

Authoritative XcodeGen references:

- [XcodeGen Project Spec documentation](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html)
- [XcodeGen repository](https://github.com/yonaskolb/XcodeGen)

## Routing

- If the request touches generated project structure in `project.yml`, `project.yaml`, included specs, targets, schemes, settings, packages, or file membership, route to `xcode-build-run-workflow`.
- If the request is primarily about generated test targets, scheme test actions, launch arguments, environment variables, or `.xctestplan` references, route to `xcode-testing-workflow`.
- If the request asks for new-project defaults, template changes, minimum XcodeGen versions, or baseline `.xcconfig` layout, route to `bootstrap-xcode-app-project`.
- Treat XcodeGen specs as the owner for targets, resources, schemes, packages, project references, test-plan references, configuration-file wiring, generation options, and generated file membership.
- Treat Xcode 16 `syncedFolder` source roots as the preferred file-membership model for new generated app/test source directories, with broad recursive source paths plus explicit `includes` and `excludes` as the fallback.
- Treat `.xcconfig` files as the owner for nontrivial build settings, with shared, target-level, and per-configuration layers when a repo uses that layout.
- Treat external `.entitlements` files as the owner for app, extension, and capability-bearing target entitlements when `CODE_SIGN_ENTITLEMENTS` points at a checked-in plist.
- Do not assume Xcode Build Settings UI edits update `.xcconfig` files; route intentional tracked settings back into the owning config before regeneration.
- Preserve the direct `.pbxproj` warning boundary for hand-edited project files, but treat generated `.pbxproj` diffs as reviewed output when they come from `xcodegen generate`.
- Do not introduce XcodeGen into a hand-managed Xcode project unless the user explicitly asks for that migration.
