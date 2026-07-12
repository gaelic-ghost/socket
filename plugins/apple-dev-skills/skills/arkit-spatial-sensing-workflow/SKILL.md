---
name: arkit-spatial-sensing-workflow
description: Guide ARKit world tracking, anchors, planes, ray casting, feature points, scene depth, smoothed depth, LiDAR scene reconstruction, meshes, classification, environment texturing, world maps, relocalization, reference images and objects, geographic anchors, visionOS providers, privacy, and diagnostics. Use when Apple-platform spatial sensing or environment understanding is primary.
---

# ARKit Spatial Sensing Workflow

## Purpose

Guide ARKit environment sensing while preserving the platform-specific session model, typed spatial data, tracking quality, authorization, privacy, and rendering/scanning handoffs.

## When To Use

- Use for world tracking, planes, anchors, ray casting, scene depth, LiDAR reconstruction, meshes, environment understanding, maps, relocalization, and visionOS ARKit providers.
- Recommend `camera-capture-depth-workflow` for camera controls, photo/video capture, calibrated camera depth, or synchronized camera outputs.
- Recommend `arkit-face-body-tracking-workflow` for TrueDepth face geometry or body skeleton tracking.

## Single-Path Workflow

1. Classify the spatial task:
   - world tracking and tracking-state repair
   - plane, image, object, or geographic detection
   - ray casting, hit testing, feature points, or measurement
   - scene depth or smoothed scene depth
   - scene reconstruction, mesh geometry, or classification
   - environment texturing or probes
   - world-map persistence, sharing, or relocalization
   - visionOS authorization and provider lifecycle
2. Apply the Apple docs gate:
   - read current ARKit documentation for the selected platform and capability
   - state the documented behavior relied on
   - apply `../../shared/references/apple-spatial-data-privacy-contract.md`
   - check `supportsFrameSemantics`, `supportsSceneReconstruction`, configuration support, provider support, authorization, and device capability before configuration
3. Choose the platform shape:
   - on iOS/iPadOS, configure and own `ARSession` with the appropriate `ARConfiguration`
   - on visionOS, request the documented `ARKitSession` authorization and run only the required data providers
   - do not hide those different lifecycles behind a generic spatial session
4. Preserve spatial evidence:
   - keep anchor identifiers, transforms, timestamps, tracking state, world origin, coordinate conventions, depth confidence, mesh geometry/classification, map state, and provider events typed
   - distinguish estimated geometry from measured truth
5. Define presentation and scanning handoffs:
   - use RealityKit for entity/scene presentation and interaction when appropriate
   - use RoomPlan for documented room-capture and structured-room workflows
   - use SceneKit only for an existing SceneKit rendering surface or a documented requirement
   - use Metal for advanced rendering or compute that RealityKit/Core Image cannot express
6. Return documented behavior, capability and authorization evidence, platform session/provider plan, coordinate and data lifecycle, privacy policy, diagnostics, validation, and handoffs.

## Inputs

- `request`: spatial-sensing task or implementation under repair.
- `spatial_goal`: `world`, `planes`, `raycast`, `depth`, `mesh`, `environment`, `map`, `image`, `object`, `geo`, `visionos`, or `repair`.
- `platform_context`: platform, deployment target, intended devices, and rendering framework.
- `data_context`: persistence, sharing, server, collaboration, or local-only requirements.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` for ARKit spatial sensing, `fallback` for camera capture, face/body, RoomPlan, rendering, or execution.
- `output`: documented behavior, capability/authorization matrix, lifecycle, coordinates, data/privacy plan, diagnostics, validation, and handoffs.

## Guards and Stop Conditions

- Do not assume LiDAR, scene depth, reconstruction, classification, geo tracking, image/object detection, or provider support from a device name or OS version.
- Do not wrap iOS `ARSession` and visionOS `ARKitSession` providers in a fake common lifecycle.
- Do not treat an anchor transform, raycast, feature point, depth sample, plane extent, or reconstructed mesh as exact ground truth.
- Do not persist or transmit world maps, meshes, room geometry, images, location anchors, or bystander-derived spatial data without an explicit purpose, consent/notice, retention, and deletion policy.
- Do not claim relocalization, metric accuracy, occlusion quality, mesh classification, or device performance without physical-device evidence.
- Do not silently reset tracking or the world origin; explain what spatial continuity is lost.
- Stop when authorization, device support, tracking conditions, or required physical validation is unavailable.

## Fallbacks and Handoffs

- Recommend `arkit-face-body-tracking-workflow` for face and body anchors, geometry, blend shapes, eyes, skeletons, and scale.
- Recommend `camera-capture-depth-workflow` for camera devices, controls, photo/video, calibrated depth, and synchronized capture.
- Recommend `vision-image-analysis-workflow` for image-frame recognition and pose analysis outside ARKit tracking.
- Recommend RealityKit for scene presentation and interaction, RoomPlan for room capture, SceneKit for existing SceneKit surfaces, and Metal for advanced rendering.
- Recommend `xcode-build-run-workflow` for privacy configuration, authorization, build, run, physical-device logs, or profiling.
- Recommend `xcode-testing-workflow` for transform fixtures, provider state tests, saved-map fixtures, and device test plans.
- Recommend `explore-apple-swift-docs` for current ARKit or related framework research.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/world-tracking-depth-meshes-and-maps.md`
- `references/visionos-providers-rendering-and-diagnostics.md`
- `references/customization-flow.md`
- `../../shared/references/apple-spatial-data-privacy-contract.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
