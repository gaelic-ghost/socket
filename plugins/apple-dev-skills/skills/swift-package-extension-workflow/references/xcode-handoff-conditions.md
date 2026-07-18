# Xcode Handoff Conditions

## Stay package-first when

- `Package.swift` owns the plugin, macro, trait, dependency, target, and product shape.
- `swift package`, `swift build`, or `swift test` can reproduce the behavior without Xcode workspace state.
- Generated output remains inside SwiftPM-managed build directories.

## Hand off to Xcode when

- A command plugin uses Xcode project or target context rather than only a Swift package context.
- Correctness depends on the active scheme, destination, app host, SDK, build setting, or Xcode UI invocation.
- Generated artifacts must be added to Xcode target membership or an Xcode-owned build phase.
- Macro expansion or diagnostics must be inspected in Xcode's editor/build log as the authoritative user experience.
- Package behavior differs under `xcrun swift`, `xcodebuild`, or the open Xcode workspace.

## Handoff payload

Provide the package root, extension type, plugin or macro target, selected traits, Swiftly and Xcode versions, exact CLI reproduction, permission flags, expected outputs, and the scheme/destination that must be validated.
