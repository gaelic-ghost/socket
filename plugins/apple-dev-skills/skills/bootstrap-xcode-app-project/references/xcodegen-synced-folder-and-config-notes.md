# XcodeGen Synced Folder And Config Notes

## Decision

- For new XcodeGen-backed app scaffolds that use `projectFormat: xcode16_0` or newer, prefer `syncedFolder` roots at the broad top-level directory boundary.
- Use the standard top-level Xcode app repository layout: `Sources/`, `Tests/`, `Shared/`, `Extensions/`, `Configurations/`, `Scripts/`, and `Packages/`.
- Use exactly one top-level `Sources` source entry for the app target, exactly one top-level `Shared` source entry for shared app/extension source, and exactly one top-level `Tests` source entry for the test target. Extension targets use one `Extensions/<ExtensionName>` entry per extension target.
- Use those same broad recursive paths with explicit `includes` and `excludes` as the fallback when synchronized folders do not fit a repo.
- Avoid subdirectory fragmentation and one YAML entry per ordinary source file. Use narrower source entries only for exceptional compiler flags, build-phase routing, destination filters, target membership, or other file-specific behavior that cannot be represented from the broad root.

## Template Shape

- Keep app source, resources, support files, generated `Info.plist`, checked-in entitlements, feature folders, and nested implementation folders under `Sources/` when they belong to the app target.
- Keep tests under `Tests/` when they belong to the test target.
- Keep shared app/extension source under `Shared/`, extension target roots under `Extensions/`, project-local automation under `Scripts/`, and justified local Swift packages under `Packages/`.
- Keep resources under `Sources/Resources`, including a default `Assets.xcassets` with `AppIcon` and `AccentColor` placeholders, but do not add `Sources/Resources` as a separate XcodeGen source entry when `Sources` already owns the target root.
- Set `options.defaultSourceDirectoryType: syncedFolder` and mark only the broad target roots with `type: syncedFolder` so the intended behavior is visible at the target boundary.
- Never split `Sources/App`, `Sources/Resources`, `Sources/Support`, feature folders, or `Tests/<AppName>Tests` into separate ordinary XcodeGen source entries.
- Keep `Configurations/` visible as a `fileGroups` entry so `.xcconfig` layers are easy to find in Xcode.

## App Entry Point

- Create exactly one app lifecycle entry point per app target: one `@main` app type, one `main.swift`, or the platform-equivalent single launch entry.
- Do not add alternate app entry points, second `@main` app types, duplicate `main.swift` files, target-specific app entry files, or parallel app structs for variants.
- Put platform, configuration, feature-flag, or product-variant differences inside the single entry point using Swift conditional compilation or ordinary runtime conditionals.

## Entitlements

- Prefer a checked-in external entitlement plist for every app, extension, or capability-bearing target.
- Wire the entitlement plist with `CODE_SIGN_ENTITLEMENTS` in the owning target `.xcconfig`.
- Do not generate entitlement contents from inline XcodeGen YAML when the expected workflow is to let Xcode capabilities update the entitlement plist.
- After capability changes in Xcode, review the entitlement plist diff, the generated project diff, and any config diff together.

## Build Settings

- Prefer checked-in `.xcconfig` files for nontrivial build settings, with a shared base, target-level configs, and per-configuration configs.
- Keep `SWIFT_VERSION = 6.0`, common Swift concurrency defaults, asset-symbol generation, localization analyzer settings, user-script sandboxing, and dead-code stripping in the shared config when every generated target should inherit them.
- Keep app identity, app icon name, marketing version, build number, entitlement path, app sandbox defaults, and hardened-runtime defaults in the app config.
- Keep generated `Info.plist` version keys wired to `$(MARKETING_VERSION)` and `$(CURRENT_PROJECT_VERSION)` so version bump scripts can update the config source instead of generated project state.
- Do not assume Xcode's Build Settings UI writes edited values back into `.xcconfig` files. Treat GUI-edited build settings as generated project overrides until inspected.
- When a GUI change belongs in tracked config, move the value into the owning `.xcconfig`, regenerate with XcodeGen, and confirm the generated project no longer carries an unintended override.
- Before running `xcodegen generate`, inspect existing generated project diffs and assume they are intentional user or Xcode GUI changes unless proven otherwise.
- Promote project-file diffs into their tracked owners before regeneration: XcodeGen spec for project structure and wiring, `.xcconfig` for build settings, `.entitlements` for entitlement keys, `Info.plist` for plist keys, scheme spec or `.xcscheme` for scheme behavior, and `.xctestplan` for test-plan content.

## Evidence Sources

- XcodeGen's project spec documents recursive target `sources`, `includes`, `excludes`, `defaultSourceDirectoryType`, and `type: syncedFolder`.
- XcodeGen's project spec documents `configFiles` for project and target `.xcconfig` wiring.
- The bootstrap template should be validated with a real `xcodegen generate` and `xcodebuild -list` probe after synchronized-folder or entitlement wiring changes.
