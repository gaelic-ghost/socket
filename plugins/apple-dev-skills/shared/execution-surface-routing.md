# Swift Execution Surface Routing

Do not classify a repository as Xcode, SwiftPM, plain, or mixed. Gale-owned Swift product repositories intentionally combine a root Xcode workspace with Swift packages.

Route each operation by the component and capability it needs:

- Resolve the nearest `Package.swift` for manifest, dependency, source, resource, plugin, macro, build, run, and package-test work.
- Use the root `.xcworkspace` only for an Xcode scheme, simulator or device destination, preview, target membership, build phase, app bundle integration, `.xctestplan`, XCUITest, signing, or other Xcode-owned state.
- The presence of `.xcworkspace`, `.xcodeproj`, or `Package.swift` files is context, never a repository identity or a reason to hand off.
- Never require a mixed-root opt-in. There is no alternate plain-package path to preserve for a product repository.
- A deliberately standalone published library or CLI may omit a workspace, but that is an explicit repository contract, not something inferred from file markers.

When a request crosses surfaces, keep package work at the nearest package root and hand only the Xcode-owned operation to the appropriate Xcode workflow.
