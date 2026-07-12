---
name: camera-capture-depth-workflow
description: Guide Apple camera discovery, device and format configuration, focus, exposure, white balance, zoom, torch, stabilization, rotation, photo capture, RAW, Live Photos, depth and disparity, calibration, synchronized outputs, portrait and semantic mattes, computational capture, pressure, interruptions, and diagnostics with AVFoundation. Use when sensor, camera-control, photo, depth, or device-capability behavior is primary.
---

# Camera Capture and Depth Workflow

## Purpose

Guide AVFoundation camera, photo, depth, and computational-capture work while keeping general session topology, media pipelines, sample timing, audio policy, Vision analysis, and ARKit spatial sensing with their owning workflows.

## When To Use

- Use for camera discovery, formats, controls, rotation, photo features, depth, calibration, synchronized outputs, mattes, pressure, and device-specific capture repair.
- Recommend `avfoundation-media-pipeline-workflow` when general capture-session, output queue, player, asset, reader, writer, export, or back-pressure ownership is primary.
- Recommend `vision-image-analysis-workflow` when capture is working and image interpretation is the actual task.

## Single-Path Workflow

1. Classify the request:
   - device discovery or selection
   - format, frame rate, MultiCam, or constituent device
   - focus, exposure, white balance, zoom, torch, stabilization, or low light
   - rotation, orientation, or mirroring
   - processed, RAW, bracketed, Live Photo, responsive, or deferred photo capture
   - depth, disparity, calibration, or synchronized output
   - portrait-effects, semantic, spatial, or cinematic capture
   - authorization, interruption, pressure, dropped data, or runtime repair
2. Apply the Apple docs gate:
   - read current AVFoundation documentation for every requested feature and platform
   - state the documented behavior relied on
   - apply `../../shared/references/apple-camera-capability-contract.md`
   - apply `../../shared/references/apple-media-type-ownership.md`
3. Discover before configuration:
   - use `AVCaptureDevice.DiscoverySession`, available devices, virtual-device constituents, `AVCaptureDevice.Format`, supported frame-rate ranges, depth formats, session support, output support, and connection support
   - never infer capability from a marketing device name, lens count, or OS version alone
4. Configure through one owner:
   - keep session graph mutation on the serial session owner defined by `avfoundation-media-pipeline-workflow`
   - balance `lockForConfiguration()` and `unlockForConfiguration()` and mutate only supported device properties
   - configure output, settings, connection, rotation, mirroring, and delegate lifecycle explicitly
5. Preserve typed capture data:
   - keep `AVCapturePhoto`, `AVDepthData`, `AVCameraCalibrationData`, `AVPortraitEffectsMatte`, `AVSemanticSegmentationMatte`, `CMSampleBuffer`, synchronized data, and dropped-data reasons inspectable
   - record timestamps, dimensions, orientation, pixel/depth formats, calibration, filtering, accuracy, and source identity
6. Validate honestly:
   - distinguish documented support, discovered runtime support, simulator limitations, and physically verified behavior
   - return the capability evidence, configuration, output lifecycle, pressure/error policy, diagnostics, and device validation plan

## Inputs

- `request`: camera, photo, depth, or computational-capture task.
- `capture_goal`: `discover`, `format`, `controls`, `rotation`, `photo`, `depth`, `sync`, `matte`, `spatial`, `cinematic`, or `repair`.
- `platform_context`: Apple platform, deployment target, and intended physical devices.
- `pipeline_context`: existing session owner, inputs, outputs, connections, queues, and audio-session policy.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` for camera sensor and capture-feature work, `fallback` for general pipelines, analysis, timing, audio, ARKit, or execution.
- `output`: documented behavior, capability matrix, configuration, typed output contract, lifecycle, pressure/error policy, diagnostics, validation, and handoffs.

## Guards and Stop Conditions

- Do not select or configure a camera feature before checking the actual device, format, output, connection, session, and platform support.
- Do not call `startRunning()`, stop, or reconfigure the capture session on the main thread.
- Do not mutate an `AVCaptureDevice` outside a balanced configuration lock or request unsupported controls.
- Do not conflate pixel orientation, metadata orientation, preview rotation, capture rotation, and mirroring.
- Do not treat disparity as metric depth without the documented conversion and calibration context.
- Do not discard calibration, timestamps, dropped-data reasons, matte relationships, or auxiliary image orientation.
- Do not claim camera topology, depth quality, calibration, LiDAR, TrueDepth, MultiCam, HDR, spatial, cinematic, or real-time behavior without physical-device evidence.
- Stop when authorization, device hardware, feature support, source data, or a physical validation path required by the request is unavailable.

## Fallbacks and Handoffs

- Recommend `avfoundation-media-pipeline-workflow` for session graph, output queues, capture lifecycle, assets, readers, writers, export, and general back-pressure.
- Recommend `coremedia-timing-samplebuffer-workflow` for timestamps, format descriptions, sample attachments, synchronization timing, and dropped-buffer diagnosis.
- Recommend `avfaudio-session-workflow` for microphone permission, audio category, route, interruption, and shared capture-session audio policy.
- Recommend `vision-image-analysis-workflow` or `vision-coreml-recognition-workflow` after typed frames reach the analysis boundary.
- Recommend `core-image-processing-workflow` for image effects, mattes, compositing, color, or rendering after capture.
- Recommend `arkit-spatial-sensing-workflow` for LiDAR scene reconstruction, world tracking, anchors, and environment mapping after Milestone 59 ships.
- Recommend `xcode-build-run-workflow` for privacy strings, entitlements, build, run, physical-device capture, logging, or Instruments.
- Recommend `xcode-testing-workflow` for fixtures, capability probes, deterministic transforms, and device test plans.
- Recommend `explore-apple-swift-docs` for current capture documentation.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/camera-discovery-controls-and-rotation.md`
- `references/photo-computational-capture-and-lifecycle.md`
- `references/depth-calibration-and-synchronized-capture.md`
- `references/customization-flow.md`
- `../../shared/references/apple-camera-capability-contract.md`
- `../../shared/references/apple-media-type-ownership.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
