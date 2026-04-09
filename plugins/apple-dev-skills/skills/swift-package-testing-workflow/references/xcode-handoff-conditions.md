# Xcode Handoff Conditions

Hand off to `xcode-testing-workflow` when:
- the task depends on an active Xcode workspace or scheme
- previews or `ExecuteSnippet` style flows matter
- simulator or device execution matters
- navigator issues, Xcode build logs, or scheme-aware diagnostics are the best interface
- package work is being exercised through Xcode rather than through plain SwiftPM
- the requested mutation crosses into `.xcodeproj`, `.xcworkspace`, or `.pbxproj` managed scope

Do not hand off just because the package is Apple-platform-related. Plain SwiftPM testing work should stay in `swift-package-testing-workflow`, while build/run, manifest, dependency, plugin, resource, and source work should stay in `swift-package-build-run-workflow`.
