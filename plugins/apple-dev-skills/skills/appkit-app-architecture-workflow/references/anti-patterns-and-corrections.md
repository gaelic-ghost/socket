# Anti-Patterns And Corrections

Use this reference before finalizing AppKit architecture guidance.

## SwiftUI-Only Steering

Symptom: A menu bar app, window-controller app, responder-chain command, or
restoration problem is pushed into SwiftUI scene structure because SwiftUI is
newer or more familiar.

Correction: name the AppKit owner first. Hand off to SwiftUI only when SwiftUI
actually owns the app, scene, focus, environment, command, or view-composition
behavior.

## Catch-All App Delegate

Symptom: launch, menu setup, status item, persistence, window construction,
networking, and model mutation all live directly in the app delegate.

Correction: keep lifecycle callbacks in the delegate, then call explicit app
models, status-item controllers, window controllers, or persistence helpers.

## Controller Dumping Ground

Symptom: a view controller owns app-wide services, window restoration, menu
validation, persistence migrations, background work, and local view state.

Correction: split by lifetime. Move app-wide behavior up, durable model state
into models, window behavior into window controllers, and local UI behavior into
view controllers.

## Hidden Command Bus

Symptom: target/action and responder-chain behavior are replaced with a broad
command router even though AppKit already names the active owner.

Correction: use AppKit actions and validation until multiple surfaces genuinely
need a shared command model.

## Restoration As Storage

Symptom: window restoration archives become the only durable copy of user data.

Correction: keep restoration payloads small and point them at documents,
workspaces, files, or persistent models that own durable state.

## Unsafe Or Unmigrated Archives

Symptom: archived object graphs are restored without secure-coding expectations,
class validation, versioning, or migration.

Correction: prefer narrow secure coding where archives are required, and name
the migration path before persisted data ships.

## Observation As Automatic AppKit Binding

Symptom: an `@Observable` model is expected to refresh arbitrary AppKit controls
without a bridge.

Correction: name the bridge: hosted SwiftUI, controller refresh, target/action,
delegate, binding, notification, or another explicit app-owned update path.

## Split Ownership Across Frameworks

Symptom: AppKit and SwiftUI both own and mutate the same model state.

Correction: pick one model owner and pass state or commands across the hosting
boundary explicitly.
