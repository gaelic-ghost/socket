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

- Select a toolchain for one command:
  - `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild -version`
  - `DEVELOPER_DIR=/Applications/Xcode-beta.app/Contents/Developer xcodebuild -version`
  - `DEVELOPER_DIR=/Applications/Betas/Xcode-beta.app/Contents/Developer xcodebuild -version`
- Select the system-wide active developer directory only when the user explicitly wants the default CLI tools to change:
  - record the current value first with `xcode-select -p`
  - switch to stable Xcode with `sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer`
  - switch to a beta Xcode with `sudo xcode-select --switch /Applications/Xcode-beta.app/Contents/Developer` or `sudo xcode-select --switch /Applications/Betas/Xcode-beta.app/Contents/Developer`
  - verify with `xcode-select -p`, `xcodebuild -version`, and `xcrun --find swift`
  - restore the previous path with another `sudo xcode-select --switch <previous-path>` when the global beta test is finished
- Reset default command line tools path:
  - `sudo xcode-select --reset`
- Install/repair command line tools (interactive on macOS):
  - `xcode-select --install`

## Guidance

- Prefer explicit output of versions and selected developer dir before diagnosing build/test failures.
- Keep fallback commands deterministic and project-local.
- Prefer per-command `DEVELOPER_DIR` when checking a beta, reproducing a toolchain-specific issue, or avoiding changes that affect other shells, editors, CI helpers, and agents on the same Mac.
- Use `xcode-select --switch` when the task is intentionally about changing the default command-line tools selection. `xcode-select` controls tools discovered through `xcrun`, `xcodebuild`, and BSD development commands such as `cc` and `make`.
- Treat `/Applications/Xcode.app` as the usual stable Xcode path. For beta Xcode installs on Gale's MacBook, check system-wide candidates such as `/Applications/Xcode-beta.app` and `/Applications/Betas/Xcode-beta.app` instead of the older user-local `~/Applications/Betas` location.
- Do not use `xcode-select --install` as an Xcode app switch; it opens the interactive Command Line Tools installer.
- When a Swift package build appears to depend on Xcode-managed assets or components, verify the active Xcode toolchain before defaulting to `swift build`.
- `xcodebuild` may expose Apple-managed toolchain paths, including components like the Metal toolchain, that do not show up the same way through plain SwiftPM invocation.
- When Metal shader compilation or packaged `.metallib` validation matters, verify the active Xcode component state and prefer explicit `xcodebuild` validation over assuming SwiftPM alone covers the Apple-managed build path.
