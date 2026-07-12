# visionOS Providers, Rendering, and Diagnostics

## visionOS ARKit Shape

On visionOS, use `ARKitSession` with the documented providers required by the feature, such as world tracking, plane detection, scene reconstruction, image tracking, object tracking, or hand tracking where applicable. Check provider support, request only required authorization types, inspect authorization status, run providers together only when documented, consume their update sequences, and stop work cleanly.

Do not translate an iOS `ARWorldTrackingConfiguration` mechanically into visionOS. Provider data, authorization, immersion, app lifecycle, and access differ.

## Handoffs

Use RealityKit entities, anchors, scene understanding, occlusion, physics, and rendering when it expresses presentation and interaction. Use RoomPlan's `RoomCaptureSession`, `RoomCaptureView`, `RoomBuilder`, and `CapturedRoom` for supported room scanning and structured-room output. Use SceneKit only where an existing SceneKit surface or required API justifies it. Keep advanced Metal rendering/compute separate from ARKit sensing.

## Diagnostics

Report platform, configuration or provider types, support, authorization, session/provider state, tracking state/reason, anchor/provider event, timestamp, coordinate space, mapping status, depth/mesh availability, elapsed work, and next inspection point. Avoid raw sensitive spatial payloads.

Validate transforms and lifecycle with deterministic fixtures where possible, then use physical devices and representative spaces for tracking, depth, mesh, relocalization, authorization, and performance claims.
