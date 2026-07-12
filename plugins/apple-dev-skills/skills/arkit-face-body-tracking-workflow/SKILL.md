---
name: arkit-face-body-tracking-workflow
description: Guide ARKit TrueDepth face tracking, face anchors, geometry, topology, transforms, eye transforms, blend shapes, face-driven animation, world-plus-face tracking, body anchors, skeletons, joint transforms, scale estimation, privacy, and diagnostics. Use when ARKit face geometry or 3D body tracking is primary rather than Face ID authentication or Vision frame analysis.
---

# ARKit Face and Body Tracking Workflow

## Purpose

Guide ARKit face and body tracking while keeping TrueDepth geometry, body skeletons, Vision image analysis, Local Authentication, camera capture, rendering, and sensitive-data handling explicitly separate.

## When To Use

- Use for `ARFaceTrackingConfiguration`, `ARFaceAnchor`, face geometry, blend shapes, eye transforms, `ARBodyTrackingConfiguration`, `ARBodyAnchor`, `ARSkeleton3D`, joint transforms, and scale estimation.
- Recommend Local Authentication for Face ID or Touch ID authentication; ARKit never exposes enrolled biometric templates.
- Recommend Vision for face rectangles/landmarks or 2D body/hand/animal pose analysis in ordinary images and video frames.

## Single-Path Workflow

1. Classify the request:
   - face position/orientation or topology
   - blend shapes or face-driven animation
   - eye transforms or gaze-adjacent effects
   - world-plus-face tracking
   - body anchor, skeleton, joint pose, or scale
   - rendering, privacy, performance, or correctness repair
2. Apply the Apple docs gate:
   - read current ARKit face/body and Local Authentication documentation
   - state the documented behavior relied on
   - apply `../../shared/references/apple-spatial-data-privacy-contract.md`
   - check configuration support, supported video formats, maximum tracked faces, world-tracking support, automatic scale support, and physical device capability
3. Choose one tracking configuration:
   - use `ARFaceTrackingConfiguration` for supported TrueDepth face tracking and optional documented world tracking
   - use `ARBodyTrackingConfiguration` for supported 3D body tracking
   - do not imply simultaneous configurations or combine them through a generic tracking manager
4. Preserve typed tracking data:
   - keep anchor identifier, transform, geometry/topology, blend-shape coefficients, eye transforms, skeleton definition, joint names/transforms, estimated scale, timestamps, and tracking state inspectable
   - attach results to the correct frame/session generation
5. Define the consumer boundary:
   - hand rendering and animation to RealityKit, SceneKit, Metal, SwiftUI, or AppKit/UIKit as the actual UI requires
   - hand 2D image analysis to Vision and authentication to Local Authentication
6. Return documented behavior, capability evidence, configuration, coordinate/skeleton contract, privacy and retention policy, diagnostics, physical-device validation, and handoffs.

## Inputs

- `request`: ARKit face/body task or code under repair.
- `tracking_goal`: `face-transform`, `geometry`, `blend-shapes`, `eyes`, `world-face`, `body`, `skeleton`, `scale`, `animate`, or `repair`.
- `platform_context`: platform, deployment target, intended devices, and render surface.
- `privacy_context`: storage, transmission, analytics, personalization, sharing, and deletion requirements.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` for ARKit face/body tracking, `fallback` for authentication, Vision, camera, spatial sensing, rendering, or execution.
- `output`: documented behavior, capability/configuration, typed data and coordinates, privacy, diagnostics, validation, and handoffs.

## Guards and Stop Conditions

- Do not call ARKit face tracking Face ID, biometric authentication, identity recognition, or access to enrolled face data.
- Do not claim `LAContext` or Local Authentication returns face geometry; it evaluates authentication policy and returns an outcome.
- Do not use face geometry, blend shapes, eye transforms, or body skeletons for identity or sensitive inference without an explicit lawful product decision and suitable safeguards.
- Do not treat blend-shape coefficients as universal emotion labels, eye transforms as verified gaze intent, or skeleton joints as medically accurate measurements.
- Do not assume TrueDepth, multiple-face tracking, world-plus-face tracking, body tracking, or scale estimation support without current capability checks.
- Do not claim simulator or desktop-camera behavior verifies TrueDepth or body-tracking quality.
- Stop when physical device support, permission/notice, tracking state, or required privacy policy is unavailable.

## Fallbacks and Handoffs

- Recommend Local Authentication for Face ID, Touch ID, passcode, and device-owner authentication.
- Recommend `vision-image-analysis-workflow` for 2D face landmarks, body/hand/animal pose, and image/video analysis.
- Recommend `arkit-spatial-sensing-workflow` for world, planes, depth, meshes, maps, and environment understanding.
- Recommend `camera-capture-depth-workflow` for camera controls, photo/video capture, calibrated depth, and synchronized outputs.
- Recommend RealityKit or SceneKit for 3D presentation and animation, and Metal only for advanced custom rendering.
- Recommend `xcode-build-run-workflow` for privacy strings, build, run, physical-device logs, or profiling.
- Recommend `xcode-testing-workflow` for transform, coefficient, skeleton, session-generation, and device test plans.
- Recommend `explore-apple-swift-docs` for current ARKit or Local Authentication research.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/face-geometry-blend-shapes-and-authentication-boundary.md`
- `references/body-skeleton-scale-rendering-and-diagnostics.md`
- `references/customization-flow.md`
- `../../shared/references/apple-spatial-data-privacy-contract.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
