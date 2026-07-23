# Platform Gates, Beta Evidence, and TVMLKit Migration

## Capability Record

Before recommending an Apple TV feature, record the deployment target, target
Apple TV generation, whether a physical device is required, relevant GPU-family
or controller capability, and the SDK/Xcode version. Simulator proof does not
prove remote hardware, controller, Continuity Camera, or GPU-specific behavior.

tvOS 26 design changes do not extend to Apple TV 4K (1st generation) and older
models. RealityKit and Metal capability can also vary by GPU family. Treat those
as explicit feature gates instead of one generic Apple TV claim.

The Speech framework is unavailable in the tvOS SDK. Web views and widgets are
not supported on tvOS. Choose a native TV UI or a companion-device interaction
instead of inventing an unsupported embedded-web or widget path.

## tvOS 27 Beta Contract

As checked on 2026-07-23, tvOS 27 beta adds system-wide Large Text and includes
beta changes to localized Background Assets, `AsyncImage` HTTP caching, and
button tint behavior. These claims are release-note/WWDC-beta evidence: mark
them with the checked build and revalidate at release candidate and GM.

## TVMLKit

TVMLKit is deprecated in tvOS 18 and later. For an existing client-server app,
first inventory templates, JavaScript navigation, document loading, player
behavior, server data contracts, and focus/accessibility dependencies. Then
move feature slices to SwiftUI or UIKit while retaining a testable content
contract. Do not add a new TVMLKit feature as a shortcut.

## AI Availability

Apple's current Core AI hardware requirements and Foundation Models model
version matrix do not name tvOS as a direct app runtime target. Do not promise
that Apple TV can run Core AI, `SystemLanguageModel`, or Foundation Models
inference. A genuine model-runtime question belongs to
`model-lab-skills:choose-apple-model-runtime`; it must begin from current Apple
availability evidence and supply a non-tvOS fallback where necessary.
