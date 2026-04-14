# SwiftLint Surfaces

Authoritative source: [SwiftLint README](https://github.com/realm/swiftlint/blob/master/README.md)

## Supported Surfaces

- CLI
- Swift Package command plugin
- Swift Package build tool plugin
- Xcode package dependency with build tool plugin
- Xcode Run Script Build Phase
- Git `pre-commit` integration through the `pre-commit` framework
- GitHub Actions through reporter support and repo-authored workflow steps

## Preferred Path Notes

- Prefer SwiftLint plugins when the project shape supports them and the config file lives inside the package or project directory.
- Prefer a checked-in root `.swiftlint.yml` file, with `parent_config` or nested config flows when repo structure needs them.
- Prefer the Run Script Build Phase when the plugin path cannot express the needed config placement or invocation shape.
- When SwiftFormat is also present, prefer SwiftLint rules that add clarity, safety, maintainability, or scoped public-API documentation signal instead of re-linting formatting choices that SwiftFormat already owns.

## Complementary Rule Guidance

- Good default buckets alongside SwiftFormat are API-safety rules such as `force_unwrapping`, `force_try`, `empty_count`, `unused_import`, and `duplicate_imports`.
- Maintainability rules such as `file_length`, `type_body_length`, and `function_body_length` are reasonable when thresholds stay loose enough to catch true outliers instead of ordinary library code.
- Documentation-oriented rules can be useful once a package is shipping DocC, but apply them selectively to clear public API surfaces instead of internal runtime machinery.
- Avoid using SwiftLint as a second formatting layer for line wrapping, indentation, commas, import ordering, or declaration reflow when SwiftFormat is already configured.

## High-Signal Caveats

- Build tool plugins cannot take arbitrary `--config` paths.
- Xcode 15+ script sandboxing can block Run Script usage unless `ENABLE_USER_SCRIPT_SANDBOXING` is disabled for that target.
- SwiftLint does not ship an Xcode source editor extension or AppleScript integration surface comparable to SwiftFormat.
