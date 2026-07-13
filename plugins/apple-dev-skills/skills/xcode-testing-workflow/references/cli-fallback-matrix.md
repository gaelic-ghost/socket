# CLI Fallback Matrix

## Build and test

- Xcode project/workspace build:
  - `xcodebuild -project <proj.xcodeproj> -scheme <scheme> build`
  - `xcodebuild -workspace <ws.xcworkspace> -scheme <scheme> build`
- Xcode tests:
  - `xcodebuild test -project <proj.xcodeproj> -scheme <scheme> -destination '<dest>'`
  - Coverage: `xcodebuild test -project <proj.xcodeproj> -scheme <scheme> -destination '<dest>' -enableCodeCoverage YES -resultBundlePath <artifacts>/<run>.xcresult`
  - Coverage report: `xcrun xccov view --report --json <artifacts>/<run>.xcresult`

## Runtime and tooling

- Tool lookup:
  - `xcrun --find swift`
  - `xcrun --find xcodebuild`
  - `xcrun --find xctrace`
- Instruments:
  - `xcrun xctrace version`
  - `xcrun xctrace list templates`
  - `xcrun xctrace record --template 'Time Profiler' --time-limit 30s --output traces/<name>.trace --launch -- <command> <args>`
  - `xcrun xctrace record --template 'Metal System Trace' --time-limit 30s --output traces/<name>.trace --launch -- <command> <args>`
  - `xcrun xctrace record --template 'Allocations' --output traces/<name>.trace --launch -- <command> <args>`
  - `xcrun xctrace record --template 'Time Profiler' --time-limit 30s --output traces/<name>.trace --attach <pid-or-process-name>`
- Simulator-related tools:
  - `xcrun simctl list`

## SwiftPM

- Build:
  - `swift build`
- Test:
  - `swift test`
  - Coverage: `swift test --enable-code-coverage`
  - Coverage report location: `swift test --show-codecov-path`
- Run executable target:
  - `swift run <target>`
- Package commands:
  - `swift package describe`
  - `swift package resolve`
  - `swift package update`
  - `swift package test` (alias behavior varies by toolchain; prefer `swift test` for test execution)
- Xcode-managed package fallback when the package needs Xcode SDK or toolchain behavior:
  - confirm package scheme discovery first with `xcodebuild -list -json`
  - build with `xcodebuild -scheme <PackageName> -destination 'generic/platform=macOS' build`
  - test with `xcodebuild -scheme <PackageName> -destination 'platform=macOS' test`
  - use this path when plain SwiftPM invocation is insufficient for Apple-managed toolchain components or build assets surfaced through Xcode
