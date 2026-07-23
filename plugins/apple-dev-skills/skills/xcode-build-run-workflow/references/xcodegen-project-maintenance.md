# XcodeGen Project Maintenance

## Purpose

Use this reference when an existing Xcode-managed app repo is backed by XcodeGen rather than a hand-maintained `.xcodeproj`.

Authoritative XcodeGen references:

- [XcodeGen Project Spec documentation](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html)
- [XcodeGen repository](https://github.com/yonaskolb/XcodeGen)

Current validated baseline: XcodeGen `2.46.0`.

## Detection

- Look for `project.yml`, `project.yaml`, or repo docs that name an XcodeGen spec path.
- Inspect `include` entries before editing; included specs merge into the root spec, and the owning file may be narrower than `project.yml`.
- Treat generated `.xcodeproj` and `.pbxproj` files as output when the spec set is present and current.

## Build And Project-Integrity Changes

- Make target membership, resource membership, build settings, build configurations, schemes, Swift package declarations, project references, and generation options in the XcodeGen spec set.
- Before running `xcodegen generate`, inspect existing generated `.xcodeproj` or `.pbxproj` diffs. Treat those diffs as intentional user or Xcode GUI changes unless proven otherwise; preserve the intent in the owning tracked source files before regeneration.
- Promote GUI-created project settings into the right owner: XcodeGen specs for structure and wiring, `.xcconfig` files for build settings, `.entitlements` files for entitlement keys, `Info.plist` for plist keys, scheme specs or `.xcscheme` files for scheme behavior, and `.xctestplan` files for test-plan content.
- If a `.pbxproj` diff contains settings that would be lost on regeneration and the correct tracked owner is unclear, stop and ask instead of regenerating.
- Use top-level `configs` and `configFiles` when the whole project has shared configuration behavior, and target-level `configFiles` when app, test, extension, or framework targets need separate setting layers.
- Keep top-level `schemes` explicit when build, run, archive, profile, analyze, command-line arguments, environment variables, or test-plan behavior matters. Do not rely on generated scheme defaults after the repo has explicit scheme policy.
- Declare Swift packages in the spec-level `packages` map and link them through target `dependencies`; do not add package references by hand in the generated project.
- Use `projectReferences`, `targetTemplates`, and `schemeTemplates` when they remove real repetition across generated modules, not as ceremony for a tiny one-target project.
- Treat XcodeGen as per-project generation. In an Apps/Packages workspace, each app project declares its own local Swift packages; a workspace makes projects convenient to open together but does not replace target dependency wiring.
- Set `schemePathPrefix: "../"` when a generated project lives in an `.xcworkspace` and scheme file paths must resolve from the workspace. Retain XcodeGen's default standalone prefix otherwise.
- Use a local Swift package product for shared Core code. Use a `projectReferences` target dependency only for a real dependency on another `.xcodeproj` target.
- Use `defaultSourceDirectoryType: syncedFolder` for broad ordinary roots in Xcode 16+ project formats. Use `explicitFolders` only when a child must be a bundle-style folder reference.
- Preserve the standard top-level Xcode app layout when adding or moving generated targets: `Sources/`, `Tests/`, `Shared/`, `Extensions/`, `Configurations/`, `Scripts/`, and `Packages/`.
- For Xcode 16 or newer project formats, prefer `syncedFolder` roots at the broad top-level directory boundary so Xcode and the filesystem stay aligned for file membership.
- Do not fragment ordinary XcodeGen source roots by subdirectory. A standard app target gets one `Sources` source entry that includes all app source, resource, support, generated plist, entitlement, and nested feature folders, plus one `Shared` source entry when shared app/extension code exists. A standard test target gets one `Tests` source entry that includes all test subdirectories. Extension targets use one `Extensions/<ExtensionName>` source entry per extension target.
- Never split `Sources/App`, `Sources/Resources`, `Sources/Support`, feature folders, or `Tests/<TargetName>Tests` into separate ordinary XcodeGen source entries. If synchronized folders are not appropriate, use the same broad top-level recursive paths with explicit `includes` and `excludes` as the fallback instead of hand-listing every ordinary source file or fragmenting by child directory.
- Prefer external `.xcconfig` files for nontrivial build settings and wire them from the XcodeGen spec instead of duplicating build settings inline.
- Keep `.xcconfig` layering explicit, with a small shared base config, target-level configs for app/test/extension identity, and per-configuration configs that include the narrower target config and override only what changes.
- Prefer external `.entitlements` files for app, extension, and other capability-bearing targets. Wire them through `CODE_SIGN_ENTITLEMENTS` in the owning `.xcconfig`; let Xcode capabilities update the entitlement plist when possible, then review and commit the plist diff.
- Do not assume Xcode's Build Settings UI writes edited values back into `.xcconfig` files. If a GUI edit creates a generated project override, move intentional tracked settings into the owning `.xcconfig` before regenerating.
- Do not put secrets, personal team IDs, local filesystem paths, provisioning profiles, API tokens, or private signing material in committed `.xcconfig` files.
- Do not hand-edit generated `.pbxproj` files to work around spec drift; fix the spec and regenerate.
- For ordinary source edits, inspect the relevant `sources` declarations to decide whether new files are already covered or whether the spec needs an explicit source/resource entry.
- For app lifecycle edits, preserve exactly one app entry point per app target. Do not add alternate `@main` app types, duplicate `main.swift` files, target-specific app entry files, or parallel app structs for variants; put platform, configuration, or product-variant differences inside the single entry point with Swift conditional compilation or runtime conditionals.
- After changing specs, `.xcconfig` files, or entitlement-file wiring, run `xcodegen generate` from the spec root, or `xcodegen generate --spec <path>` when the repo uses a non-default spec path.
- If the spec uses environment variables, `preGenCommand`, or `postGenCommand`, preserve the required environment and call that out in the validation notes.
- Review the spec diff, `.xcconfig` diff, and generated project diff after regeneration, especially target membership, package references, signing settings, scheme actions, and build-setting churn.
- Validate with explicit `xcodebuild` commands for the affected scheme, destination or SDK, and configuration.

## Boundary

- Do not introduce XcodeGen into a hand-managed Xcode project unless the user explicitly asks for that migration.
- Do not treat every Xcode project as XcodeGen-backed just because XcodeGen support exists in these skills.
