# Project Generator Notes

## Purpose

Describe the supported generator choices for `bootstrap-xcode-app-project`.

## Supported Generator Modes

### `xcodegen`

- Use by default for new Xcode app, framework, and workspace repositories unless the user explicitly prefers the standard Xcode project-creation flow or the repository has a concrete reason to avoid a generator dependency.
- This is the currently supported mutating implementation path in the first iteration of the skill.
- The project spec may be YAML or JSON; this skill emits YAML as `project.yml` from `templates/xcodegen/swiftui-app/project.yml.tmpl`.
- The generated scaffold should require the recent validated XcodeGen baseline declared in the template. As of this guidance, that baseline is `minimumXcodeGenVersion: 2.45.4`.
- Current project-spec concepts this skill should keep aligned include `options.minimumXcodeGenVersion`, `options.projectFormat`, `configs`, `configFiles`, targets, sources, schemes, Swift packages, project references, target templates, scheme templates, and test-plan references.
- Prefer checked-in external `.xcconfig` files for nontrivial build settings and wire them from the XcodeGen spec rather than duplicating settings inline. New app scaffolds should start with shared, target-level, and per-configuration `.xcconfig` layers.
- Keep generated templates free of secrets, local filesystem paths, personal team IDs, provisioning profiles, and private signing material. Use safe placeholders or externally supplied build settings when the value is environment-specific.
- Prefer explicit top-level schemes once generated scheme behavior matters, including build, run, test, profile, analyze, archive, and scheme-management settings.
- After generation, future project-structure edits should change the spec set and rerun `xcodegen generate` instead of hand-editing generated `.pbxproj` files.
- Reference:
  - [XcodeGen Project Spec documentation](https://yonaskolb.github.io/XcodeGen/Docs/ProjectSpec.html)
  - [XcodeGen repository](https://github.com/yonaskolb/XcodeGen)

### `xcode`

- Use when the user explicitly prefers the standard Xcode-created-project flow.
- Treat this as a guided path in the first implementation pass.
- Do not pretend the skill has a safe full GUI automation path unless that support is actually implemented and validated.
- Reference:
  - [Creating an Xcode project for an app](https://developer.apple.com/documentation/xcode/creating_an_xcode_project_for_an_app)

### `ask`

- Use only when the user or customization state intentionally wants an explicit blocking prompt instead of the default generator.
- Block with a concise next step instead of silently choosing a different generator.

## Policy

- Prefer XcodeGen for new repositories because it keeps project structure reproducible, reviewable, and easier to regenerate from text.
- Treat the standard Xcode path as a guided fallback because it reflects Apple's first-party project-creation flow and may still be the right choice when a repository should avoid a generator dependency.
