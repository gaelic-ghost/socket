# XcodeGen Project Maintenance

## Purpose

Use this reference when an existing Xcode-managed app repo is backed by XcodeGen rather than a hand-maintained `.xcodeproj`.

Authoritative XcodeGen references:

- [XcodeGen Project Spec documentation](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html)
- [XcodeGen repository](https://github.com/yonaskolb/XcodeGen)

## Detection

- Look for `project.yml`, `project.yaml`, or repo docs that name an XcodeGen spec path.
- Inspect `include` entries before editing; included specs merge into the root spec, and the owning file may be narrower than `project.yml`.
- Treat generated `.xcodeproj` and `.pbxproj` files as output when the spec set is present and current.

## Test Changes

- Make test target membership, test bundle settings, build configurations, scheme test actions, launch arguments, environment variables, and test-plan references in the XcodeGen spec set when those project-level surfaces are generated.
- Before running `xcodegen generate`, inspect existing generated `.xcodeproj` or `.pbxproj` diffs. Treat those diffs as intentional user or Xcode GUI changes unless proven otherwise; preserve the intent in the owning tracked source files before regeneration.
- Promote GUI-created test settings into the right owner: XcodeGen specs for target and scheme wiring, `.xcconfig` files for build settings, scheme specs or `.xcscheme` files for scheme behavior, and `.xctestplan` files for test-plan content.
- If a `.pbxproj` diff contains test settings that would be lost on regeneration and the correct tracked owner is unclear, stop and ask instead of regenerating.
- Use top-level `schemes` for generated test behavior once the repo needs explicit test actions, coverage settings, command-line arguments, environment variables, test targets, or test-plan references.
- Remember that XcodeGen references checked-in `.xctestplan` files by path; it does not create the test-plan file content for you. Create or update the `.xctestplan` through Xcode or a structured JSON-aware edit, then wire the path through the scheme spec.
- Use target-level `configFiles` for test bundles when test-only build settings, bundle identifiers, compilation conditions, or host-app settings diverge from the app target.
- For Xcode 16 or newer project formats, prefer `syncedFolder` roots at the broad top-level directory boundary so Xcode and the filesystem stay aligned for file membership.
- Do not fragment ordinary XcodeGen source roots by subdirectory. A standard app target gets one `Sources` source entry that includes all app source, resource, support, generated plist, entitlement, and nested feature folders. A standard test target gets one `Tests` source entry that includes all test subdirectories. If a project has a separate top-level logical root such as `Resources`, use one top-level `Resources` entry for that root.
- Never split `Sources/App`, `Sources/Resources`, `Sources/Support`, feature folders, or `Tests/<TargetName>Tests` into separate ordinary XcodeGen source entries. If synchronized folders are not appropriate, use the same broad top-level recursive paths with explicit `includes` and `excludes` as the fallback instead of hand-listing every ordinary test file or fragmenting by child directory.
- Prefer external `.xcconfig` files for nontrivial build settings and wire them from the XcodeGen spec instead of duplicating build settings inline.
- Keep `.xcconfig` layering explicit, with a small shared base config, target-level configs for app/test/extension identity, and per-configuration configs that include the narrower target config and override only what changes.
- Do not assume Xcode's Build Settings UI writes edited values back into `.xcconfig` files. If a GUI edit creates a generated project override, move intentional tracked test settings into the owning `.xcconfig` before regenerating.
- Do not put secrets, personal team IDs, local filesystem paths, provisioning profiles, API tokens, or private signing material in committed `.xcconfig` files.
- Keep `.xctestplan` files versioned as ordinary source files, but wire them into schemes through the spec when the scheme itself is generated.
- Do not hand-edit generated `.pbxproj` files to add test targets, test files, or test-plan references; fix the spec and regenerate.
- For app lifecycle edits uncovered during test work, preserve exactly one app entry point per app target. Do not add alternate `@main` app types, duplicate `main.swift` files, target-specific app entry files, or parallel app structs for variants; put platform, configuration, or product-variant differences inside the single entry point with Swift conditional compilation or runtime conditionals.
- After changing specs, `.xcconfig` files, or entitlement-file wiring, run `xcodegen generate` from the spec root, or `xcodegen generate --spec <path>` when the repo uses a non-default spec path.
- If the spec uses environment variables, `preGenCommand`, or `postGenCommand`, preserve the required environment and call that out in the validation notes.
- Review the spec diff, `.xcconfig` diff, and generated project diff after regeneration, especially test target membership, host-app dependencies, test-plan paths, scheme actions, and build-setting churn.
- Validate with explicit `xcodebuild test`, `xcodebuild -showTestPlans`, or focused test-plan commands for the affected scheme, destination, and configuration.

## Boundary

- Do not introduce XcodeGen into a hand-managed Xcode project unless the user explicitly asks for that migration.
- Do not treat every Xcode project as XcodeGen-backed just because XcodeGen support exists in these skills.
