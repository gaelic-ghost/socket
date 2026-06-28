# Layer Ownership and Animation Rules

Use this reference when deciding whether and how to use Core Animation.

## Ownership Rules

- UIKit views own their backing layer. Do not replace the layer delegate of `UIView.layer`.
- Use `UIView.layerClass` only when a view needs a different backing layer class.
- AppKit views may be layer-backed through `wantsLayer`; keep view lifecycle and layer lifecycle distinct.
- A standalone sublayer tree needs a clear owner such as a view, view controller, representable coordinator, or custom layer host.
- A custom `CALayer` subclass should expose explicit inputs and avoid reaching into unrelated view or model state.
- SwiftUI bridges should keep layer mutation behind a representable boundary and keep SwiftUI state as the source of truth.

## Animation Rules

- Use implicit animations when property changes should animate through the current transaction.
- Use explicit `CAAnimation` when the animation needs a key path, repeat behavior, timing function, additive behavior, grouped timing, or presentation continuity not covered by framework helpers.
- Disable actions when layout or data refresh should not animate.
- Update the model layer to the final value when an explicit animation visually changes a property.
- Keep animation setup on the main/UI thread unless Apple documentation for the specific layer operation says otherwise.

## Specialized Layer Routing

- Use `CAShapeLayer` for vector paths, stroked paths, masks, and animatable path-like geometry.
- Use `CAGradientLayer` for gradient fills that belong in a layer tree.
- Use `CATextLayer` only when text is genuinely part of layer rendering; use native text views for interactive or accessibility-rich text.
- Use `CAReplicatorLayer` for repeated layer instances with transform, delay, or color offsets.
- Use `CATiledLayer` for tiled large content when the framework view stack cannot handle the size efficiently.
- Consider SpriteKit, SceneKit, Metal, AVFoundation, or SwiftUI Canvas when the content is game-like, 3D, GPU-heavy, video, or SwiftUI drawing-oriented.

## Common Failure Modes

- Visual snap-back after explicit animation because the model layer still has the old value.
- Flicker or unexpected motion because implicit animations were not disabled during layout.
- Blurry contents because `contentsScale` or AppKit image layer contents are wrong.
- Missed hit tests because code uses the model layer while an animation is in flight.
- Leaked or stale animations because layers outlive their intended owner.
- Overly broad layer mutation from SwiftUI update cycles.
