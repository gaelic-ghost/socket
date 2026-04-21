# SwiftFormat Surfaces

Authoritative source: [SwiftFormat README](https://github.com/nicklockwood/SwiftFormat/blob/main/README.md)

## Supported Surfaces

- CLI
- Xcode source editor extension through the `SwiftFormat for Xcode` host app
- Xcode Run Script Build Phase
- Swift Package Manager command plugin
- AppleScript
- Git pre-commit hook
- GitHub Actions

## Preferred Path Notes

- Prefer a checked-in `.swiftformat` file at the project root for shared repos.
- Prefer a Git pre-commit hook as the default shared-repo enforcement surface so Swift sources are formatted before commit and then verified with `swiftformat --lint`.
- Prefer a checked-in `.swift-version` file when the repository wants version-sensitive SwiftFormat rules to follow the project's actual minimum Swift version without repeating that value across commands.
- Prefer pinned package-managed or project-managed installs over purely developer-local CLI installs when the output is committed.
- When SwiftLint is also present, keep SwiftFormat as the primary authority for formatting shape instead of splitting line wrapping, indentation, comma, import-order, or declaration-layout responsibility across both tools.
- The Xcode extension is convenient for interactive formatting but does not give true per-project config auto-discovery. Import the config into the host app and re-import after project config changes.

## High-Signal Caveats

- SwiftFormat supports `.swift-version` as a plain text file in the project directory hierarchy, and that file takes precedence over an explicit `--swift-version` argument.
- Both `.swift-version` and `--swift-version` entries inside `.swiftformat` apply hierarchically, so subdirectories can intentionally override the parent Swift version when a repo has mixed-version surfaces.
- For Xcode build phases, SwiftFormat documents that `ENABLE_USER_SCRIPT_SANDBOXING` must be `NO` on newer Xcode versions for the script path to work correctly.
- The host app can import and export config files, which is the preferred supported path for turning extension settings into a shared config.
- The scriptable export path should be described as a deterministic fallback, not as the primary supported upstream workflow.
