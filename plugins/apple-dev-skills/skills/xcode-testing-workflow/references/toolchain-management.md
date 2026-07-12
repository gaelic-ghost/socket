# Toolchain Management

## Preferred path

1. If `swiftly` exists, prefer it for selecting and managing Swift toolchains.
2. If `swiftly` is unavailable, use official Xcode/CLT paths.

## Quickly check toolchain state

- `swift --version`
- `xcodebuild -version`
- `xcode-select -p`
- `xcrun --find swift`
- `xcrun --find xcodebuild`
- `xcodebuild -showComponent metalToolchain`

## Official Xcode and CLT actions

- Use the developer directory currently selected by `xcode-select` for every Xcode CLI command. Do not override it per command.
- Change the active developer directory through the already-open Xcode app, or open the intended app first: choose Xcode > Settings > Locations, select the intended app from Command Line Tools, accept the macOS Touch ID or administrator prompt, then verify with `xcode-select -p`, `xcodebuild -version`, and `xcrun --find swift`.
  - leave the selected path at the user-requested value; restore a previous path only when the user asked for a temporary switch
- Reset default command line tools path:
  - `sudo xcode-select --reset`
- Install/repair command line tools (interactive on macOS):
  - `xcode-select --install`

## Guidance

- Prefer explicit output of versions and selected developer dir before diagnosing build/test failures.
- Keep fallback commands deterministic and project-local.
- Treat Xcode's Settings > Locations > Command Line Tools dropdown as the default toolchain selector; use `xcode-select -p` only to verify the result for `xcrun`, `xcodebuild`, and related commands.
- Never set `DEVELOPER_DIR` by default. Use it only if it is genuinely the sole way to accomplish a task, explain why `xcode-select` cannot work, and obtain Gale's explicit permission first.
- Treat `/Applications/Xcode.app` as the usual stable Xcode path. For beta Xcode installs on Gale's MacBook, check system-wide candidates such as `/Applications/Xcode-beta.app` and `/Applications/Betas/Xcode-beta.app` instead of the older user-local `~/Applications/Betas` location.
- Do not use `xcode-select --install` as an Xcode app switch; it opens the interactive Command Line Tools installer.
- When a Swift package build appears to depend on Xcode-managed assets or components, verify the active Xcode toolchain before defaulting to `swift build`.
- `xcodebuild` may expose Apple-managed toolchain paths, including components like the Metal toolchain, that do not show up the same way through plain SwiftPM invocation.
- When Metal shader compilation or packaged `.metallib` validation matters, verify the active Xcode component state and prefer explicit `xcodebuild` validation over assuming SwiftPM alone covers the Apple-managed build path.
