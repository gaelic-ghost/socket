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

## Build And Project-Integrity Changes

- Make target membership, resource membership, build settings, schemes, Swift package declarations, project references, and generation options in the XcodeGen spec set.
- Do not hand-edit generated `.pbxproj` files to work around spec drift; fix the spec and regenerate.
- For ordinary source edits, inspect the relevant `sources` declarations to decide whether new files are already covered or whether the spec needs an explicit source/resource entry.
- After changing specs, run `xcodegen generate` from the spec root, or `xcodegen generate --spec <path>` when the repo uses a non-default spec path.
- If the spec uses environment variables, `preGenCommand`, or `postGenCommand`, preserve the required environment and call that out in the validation notes.
- Review both the spec diff and the generated project diff after regeneration.
- Validate with explicit `xcodebuild` commands for the affected scheme, destination or SDK, and configuration.

## Boundary

- Do not introduce XcodeGen into a hand-managed Xcode project unless the user explicitly asks for that migration.
- Do not treat every Xcode project as XcodeGen-backed just because XcodeGen support exists in these skills.
