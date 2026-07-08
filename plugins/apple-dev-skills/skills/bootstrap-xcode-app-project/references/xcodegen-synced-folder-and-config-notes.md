# XcodeGen Synced Folder And Config Notes

## Decision

- For new XcodeGen-backed app scaffolds that use `projectFormat: xcode16_0` or newer, prefer `syncedFolder` source roots for ordinary app and test source directories.
- Use broad recursive `sources` paths with explicit `includes` and `excludes` as the fallback when synchronized folders do not fit a repo.
- Avoid one YAML entry per ordinary source file. Use per-file source entries only for exceptional compiler flags, build-phase routing, destination filters, or other file-specific behavior.

## Template Shape

- Keep app source files under `Sources/App` and test files under `Tests/<AppName>Tests`.
- Set `options.defaultSourceDirectoryType: syncedFolder` and mark app/test source roots with `type: syncedFolder` so the intended behavior is visible at the target boundary.
- Keep support files such as generated `Info.plist` and checked-in entitlements outside the synced source root unless they are intentionally part of that target's buildable folder.
- Keep `Configurations/` visible as a `fileGroups` entry so `.xcconfig` layers are easy to find in Xcode.

## Entitlements

- Prefer a checked-in external entitlement plist for every app, extension, or capability-bearing target.
- Wire the entitlement plist with `CODE_SIGN_ENTITLEMENTS` in the owning target `.xcconfig`.
- Do not generate entitlement contents from inline XcodeGen YAML when the expected workflow is to let Xcode capabilities update the entitlement plist.
- After capability changes in Xcode, review the entitlement plist diff, the generated project diff, and any config diff together.

## Build Settings

- Prefer checked-in `.xcconfig` files for nontrivial build settings, with a shared base, target-level configs, and per-configuration configs.
- Keep `SWIFT_VERSION = 6.0`, common Swift concurrency defaults, asset-symbol generation, localization analyzer settings, and user-script sandboxing in the shared config when every generated target should inherit them.
- Keep app identity, marketing version, build number, entitlement path, app sandbox defaults, and hardened-runtime defaults in the app config.
- Keep generated `Info.plist` version keys wired to `$(MARKETING_VERSION)` and `$(CURRENT_PROJECT_VERSION)` so version bump scripts can update the config source instead of generated project state.
- Do not assume Xcode's Build Settings UI writes edited values back into `.xcconfig` files. Treat GUI-edited build settings as generated project overrides until inspected.
- When a GUI change belongs in tracked config, move the value into the owning `.xcconfig`, regenerate with XcodeGen, and confirm the generated project no longer carries an unintended override.
- Before running `xcodegen generate`, inspect existing generated project diffs and assume they are intentional user or Xcode GUI changes unless proven otherwise.
- Promote project-file diffs into their tracked owners before regeneration: XcodeGen spec for project structure and wiring, `.xcconfig` for build settings, `.entitlements` for entitlement keys, `Info.plist` for plist keys, scheme spec or `.xcscheme` for scheme behavior, and `.xctestplan` for test-plan content.

## Evidence Sources

- XcodeGen's project spec documents recursive target `sources`, `includes`, `excludes`, `defaultSourceDirectoryType`, and `type: syncedFolder`.
- XcodeGen's project spec documents `configFiles` for project and target `.xcconfig` wiring.
- The bootstrap template should be validated with a real `xcodegen generate` and `xcodebuild -list` probe after synchronized-folder or entitlement wiring changes.
