# Repo Shape Detection

Treat a repo as a plain Swift package when:
- `Package.swift` exists at the chosen root
- no `.xcodeproj`, `.xcworkspace`, or `.pbxproj` markers exist at that same root

Treat a repo as mixed when:
- `Package.swift` exists
- one or more `.xcodeproj`, `.xcworkspace`, or `.pbxproj` markers also exist at the same root

For mixed roots:
- prefer `swift-package-build-run-workflow` when the request is ordinary SwiftPM build, run, manifest, dependency, plugin, resource, or Metal-distribution work
- hand off to `xcode-build-run-workflow` when the request needs Xcode session state, schemes, previews, simulator or device flows, Xcode diagnostics, or guarded Xcode-managed mutation
