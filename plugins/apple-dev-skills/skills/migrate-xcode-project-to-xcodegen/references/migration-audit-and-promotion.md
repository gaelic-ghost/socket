# Migration Audit And Promotion

Use this reference after `scripts/run_workflow.py` has produced a project audit.

## Source-State Rules

- Treat `.pbxproj` changes as intentional until reviewed. Xcode often writes GUI build-setting, signing, capability, source-membership, resource, scheme, and package state there.
- Promote durable settings into checked-in files before regenerating:
  - `project.yml` for project structure, targets, packages, source roots, resource roots, schemes, and test plans
  - `Configurations/*.xcconfig` for build settings
  - `Sources/Support/App.entitlements` for capabilities and sandbox entitlements
  - `Sources/Support/Info.plist` for Info.plist values
  - `Sources/Resources/Assets.xcassets` for assets, app icons, accent colors, and generated asset symbols
- Keep `xcodegen generate` as the last step after promotion, not the first step.

## Xcode-Managed To XcodeGen

This is the `xcode-managed-to-xcodegen` path emitted by the audit script.

1. Inventory the current project:
   - targets, product types, build configurations, schemes, packages, frameworks, source groups, resources, scripts, entitlements, Info.plist files, asset catalogs, and test plans
2. Create the external owner files:
   - shared, app, test, Debug, and Release `.xcconfig` layers
   - app entitlement plist
   - support Info.plist if the project currently generates one internally
   - resource folder with `Assets.xcassets` when missing
3. Write `project.yml` from the inventory:
   - prefer `options.defaultSourceDirectoryType: syncedFolder`
   - prefer `type: syncedFolder` for app, test, and resource roots on Xcode 16 or newer
   - use broad recursive paths with explicit includes and excludes only when synced folders are not appropriate
4. Generate and compare:
   - generate in a temp clone or reviewed branch state
   - compare key build settings, target membership, schemes, package references, entitlements, and resources
   - only replace the hand-managed project after equivalence is reviewed

## Old Or Broken XcodeGen To Current Baseline

Use this `modernize-xcodegen` path to modernize XcodeGen projects that already have `project.yml` but do not match the current baseline.

1. Audit the existing `project.yml` and generated `.pbxproj`.
2. Move inline or generated-only settings into `.xcconfig` files.
3. Add missing external entitlements, Info.plist, resource roots, and asset catalog defaults.
4. Prefer synced folders for app, test, and resource roots when the supported Xcode/XcodeGen versions allow it.
5. Regenerate and verify the generated `.pbxproj` diff is expected.

## Baseline Targets

The current baseline should include:

- XcodeGen `minimumXcodeGenVersion` on the current template baseline
- `options.defaultSourceDirectoryType: syncedFolder`
- app/test/resource roots marked with `type: syncedFolder`
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
