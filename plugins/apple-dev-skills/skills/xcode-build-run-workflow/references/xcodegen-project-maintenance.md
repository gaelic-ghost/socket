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

- Make target membership, resource membership, build settings, build configurations, schemes, Swift package declarations, project references, and generation options in the XcodeGen spec set.
- Use top-level `configs` and `configFiles` when the whole project has shared configuration behavior, and target-level `configFiles` when app, test, extension, or framework targets need separate setting layers.
- Keep top-level `schemes` explicit when build, run, archive, profile, analyze, command-line arguments, environment variables, or test-plan behavior matters. Do not rely on generated scheme defaults after the repo has explicit scheme policy.
- Declare Swift packages in the spec-level `packages` map and link them through target `dependencies`; do not add package references by hand in the generated project.
- Use `projectReferences`, `targetTemplates`, and `schemeTemplates` when they remove real repetition across generated modules, not as ceremony for a tiny one-target project.
- Prefer external `.xcconfig` files for nontrivial build settings and wire them from the XcodeGen spec instead of duplicating build settings inline.
- Keep `.xcconfig` layering explicit, with a small shared base config, target-level configs for app/test/extension identity, and per-configuration configs that include the narrower target config and override only what changes.
- Do not put secrets, personal team IDs, local filesystem paths, provisioning profiles, API tokens, or private signing material in committed `.xcconfig` files.
- Do not hand-edit generated `.pbxproj` files to work around spec drift; fix the spec and regenerate.
- For ordinary source edits, inspect the relevant `sources` declarations to decide whether new files are already covered or whether the spec needs an explicit source/resource entry.
- After changing specs or `.xcconfig` files, run `xcodegen generate` from the spec root, or `xcodegen generate --spec <path>` when the repo uses a non-default spec path.
- If the spec uses environment variables, `preGenCommand`, or `postGenCommand`, preserve the required environment and call that out in the validation notes.
- Review the spec diff, `.xcconfig` diff, and generated project diff after regeneration, especially target membership, package references, signing settings, scheme actions, and build-setting churn.
- Validate with explicit `xcodebuild` commands for the affected scheme, destination or SDK, and configuration.

## Boundary

- Do not introduce XcodeGen into a hand-managed Xcode project unless the user explicitly asks for that migration.
- Do not treat every Xcode project as XcodeGen-backed just because XcodeGen support exists in these skills.
