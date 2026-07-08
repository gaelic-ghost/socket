# Migration Audit And Promotion

Use this reference after `scripts/run_workflow.py` has produced a project audit.

## Source-State Rules

- Treat `.pbxproj` changes as intentional until reviewed. Xcode often writes GUI build-setting, signing, capability, source-membership, resource, scheme, and package state there.
- Promote durable settings into checked-in files before regenerating:
  - `project.yml` for project structure, targets, packages, broad source roots, broad resource roots, schemes, and test plans
  - `Configurations/*.xcconfig` for build settings
  - `Sources/Support/<AppName>.entitlements` for capabilities and sandbox entitlements
  - `Sources/Support/Info.plist` for Info.plist values
  - `Sources/Resources/Assets.xcassets` for assets, app icons, accent colors, and generated asset symbols
- Preserve exactly one app lifecycle entry point per app target. If migration reveals multiple `@main` app types, duplicate `main.swift` files, target-specific app entry files, or parallel app structs, collapse the launch behavior back into one entry point and use Swift conditional compilation or runtime conditionals inside that boundary.
- Keep `xcodegen generate` as the last step after promotion, not the first step.

## Xcode-Managed To XcodeGen

This is the `xcode-managed-to-xcodegen` path emitted by the audit script.

1. Inventory the current project:
   - targets, product types, build configurations, schemes, packages, frameworks, source groups, resources, scripts, entitlements, Info.plist files, asset catalogs, and test plans
2. Create the external owner files:
   - shared, app, test, Debug, and Release `.xcconfig` layers
   - standard top-level directories: `Sources/`, `Tests/`, `Shared/`, `Extensions/`, `Configurations/`, `Scripts/`, and `Packages/`
   - app entitlement plist
   - support Info.plist if the project currently generates one internally
   - resource folder with `Assets.xcassets` when missing
3. Write `project.yml` from the inventory:
   - prefer `options.defaultSourceDirectoryType: syncedFolder`
   - prefer `type: syncedFolder` for broad top-level roots on Xcode 16 or newer
   - use exactly one `Sources` entry for the app target, one `Shared` entry for shared app/extension source, and exactly one `Tests` entry for the test target
   - use one `Extensions/<ExtensionName>` entry per extension target
   - never split ordinary paths such as `Sources/App`, `Sources/Resources`, `Sources/Support`, feature subfolders, or `Tests/<TargetName>Tests` into separate XcodeGen source entries
   - use the same broad recursive paths with explicit includes and excludes only when synced folders are not appropriate
4. Generate and compare:
   - generate in a temp clone or reviewed branch state
   - compare key build settings, target membership, schemes, package references, entitlements, and resources
   - only replace the hand-managed project after equivalence is reviewed

## Old Or Broken XcodeGen To Current Baseline

Use this `modernize-xcodegen` path to modernize XcodeGen projects that already have `project.yml` but do not match the current baseline.

1. Audit the existing `project.yml` and generated `.pbxproj`.
2. Move inline or generated-only settings into `.xcconfig` files.
3. Add missing external entitlements, Info.plist, resource folders, and asset catalog defaults under the broad owning root.
4. Prefer synced folders for broad app, test, and top-level resource roots when the supported Xcode/XcodeGen versions allow it.
5. Collapse any ordinary source-root fragmentation back to one `Sources` entry, one `Shared` entry, one `Tests` entry, and one `Extensions/<ExtensionName>` entry per extension target.
6. Regenerate and verify the generated `.pbxproj` diff is expected.

## Baseline Targets

The current baseline should include:

- XcodeGen `minimumXcodeGenVersion` on the current template baseline
- `options.defaultSourceDirectoryType: syncedFolder`
- app target source membership declared as one broad `Sources` entry marked with `type: syncedFolder`
- shared app/extension source membership declared as one broad `Shared` entry marked with `type: syncedFolder`
- test target source membership declared as one broad `Tests` entry marked with `type: syncedFolder`
- no ordinary fragmentation into `Sources/App`, `Sources/Resources`, `Sources/Support`, feature subfolders, or `Tests/<TargetName>Tests` source entries
- standard top-level directories present: `Sources/`, `Tests/`, `Shared/`, `Extensions/`, `Configurations/`, `Scripts/`, and `Packages/`
- exactly one app lifecycle entry point per app target
- shared, app, test, Debug, and Release `.xcconfig` layers
- `SWIFT_VERSION = 6.0`
- Swift concurrency defaults
- Swift asset symbol generation
- `ENABLE_USER_SCRIPT_SANDBOXING = YES`
- `DEAD_CODE_STRIPPING = YES`
- app marketing version `0.0.1` and build number `1`
- app sandbox and hardened runtime defaults present but off for macOS
- checked-in app entitlements file
- default `Assets.xcassets` with `AppIcon` and `AccentColor`

## Validation

Run validation after generation:

```bash
xcodegen generate
xcodebuild -list
xcodebuild -scheme <Scheme> -showBuildSettings
xcodebuild -scheme <Scheme> -configuration Debug build
```

When tests exist, also run the repo's normal test command or the relevant `xcodebuild test` invocation.
