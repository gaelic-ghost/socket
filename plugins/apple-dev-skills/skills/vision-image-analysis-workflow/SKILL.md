---
name: vision-image-analysis-workflow
description: Guide Apple Vision implementation and repair for text, barcode, face, landmark, rectangle, contour, saliency, trajectory, pose, segmentation, tracking, feature-print, and image-location analysis across still images and video. Use when Apple-provided Vision requests, observations, orientation, normalized coordinates, request revisions, sequence state, cancellation, or live-frame scheduling are primary.
---

# Vision Image Analysis Workflow

## Purpose

Guide Apple-provided image and video analysis while keeping Vision request ownership separate from image processing, custom Core ML model execution, capture, and biometric authentication.

## When To Use

- Use for built-in Vision detection, recognition, segmentation, tracking, pose, feature-print, request, observation, coordinate, and live-frame problems.
- Recommend `vision-coreml-recognition-workflow` when a custom Core ML model supplies classification, detection, or segmentation.
- Recommend `core-image-processing-workflow` when the primary job changes pixels rather than interpreting them.

## Single-Path Workflow

1. Classify the analysis:
   - text or document
   - barcode or machine-readable code
   - face rectangle or landmark
   - shape, contour, horizon, rectangle, saliency, or trajectory
   - human, hand, or animal pose
   - person, foreground, or instance segmentation
   - object tracking or sequence analysis
   - feature prints or similarity
   - coordinate, revision, performance, or correctness repair
2. Apply the Apple docs gate:
   - read the current Vision documentation for the selected request and platform
   - choose the current Swift request API for new code when it supports the task
   - recognize the original `VN*` API explicitly when repairing existing code or when the current documented task requires it
   - state the documented behavior relied on
   - apply `../../shared/references/apple-vision-analysis-contract.md`
3. Define the input contract:
   - source type, dimensions, orientation, color/pixel format, region of interest, and frame identity
   - still-image versus sequence state
   - request revision or current Swift request availability
4. Execute and interpret:
   - use `ImageRequestHandler` or the documented current request execution surface for new code
   - use `VNImageRequestHandler` for independent original-API images and `VNSequenceRequestHandler` when original-API requests need temporal state
   - keep observation types, normalized locations, confidence, labels, landmarks, and masks typed
   - convert coordinates through the full orientation, crop, region-of-interest, and display transform
5. Control live work:
   - serialize stateful sequence requests
   - bound in-flight frames, cancel obsolete work where supported, and drop stale frames deliberately
   - publish results with the source frame identity so old observations cannot overwrite newer UI
6. Return documented behavior, request family, input contract, coordinate transform, lifecycle plan, observations, diagnostics, validation, and handoffs.

## Inputs

- `request`: Vision task or code under repair.
- `analysis_goal`: `text`, `barcode`, `face`, `shape`, `pose`, `segmentation`, `tracking`, `feature-print`, `coordinates`, or `repair`.
- `media_context`: `still-image`, `video-frame`, `camera-stream`, `file-video`, or `mixed`.
- `platform_context`: Apple platform and minimum deployment target.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` for Apple-provided Vision analysis, `fallback` for custom models, processing, capture, or execution.
- `output`: documented behavior, API family, request lifecycle, coordinate and confidence contract, diagnostics, evidence, and handoff.

## Guards and Stop Conditions

- Do not mix current Swift Vision requests and original `VN*` requests into parallel app codepaths without a documented compatibility need.
- Do not reuse a stateful sequence handler concurrently or silently reset tracking state between related frames.
- Do not map a normalized bounding box directly into a view without accounting for orientation, crop, region of interest, aspect fill/fit, mirroring, and view coordinates.
- Do not treat confidence as probability, identity, authorization, safety, or verified correctness.
- Do not call face detection, landmarks, or tracking Face ID; Local Authentication owns Face ID authentication.
- Do not process every live frame when analysis cannot keep pace; bound work and make stale-frame policy explicit.
- Do not claim request availability, device performance, Neural Engine use, or real-time behavior without current documentation and runtime evidence.

## Fallbacks and Handoffs

- Recommend `vision-coreml-recognition-workflow` for custom Core ML image models.
- Recommend `core-image-processing-workflow` and `apple-image-representation-workflow` for processing, decode, metadata, orientation normalization, or representation ownership.
- Recommend `avfoundation-media-pipeline-workflow` for capture and frame delivery until `camera-capture-depth-workflow` ships.
- Recommend `arkit-face-body-tracking-workflow` for TrueDepth face geometry or AR body tracking after Milestone 59 ships.
- Recommend `xcode-build-run-workflow` for app integration, physical-device execution, signing, permissions, or profiling.
- Recommend `xcode-testing-workflow` for fixtures, coordinate tests, sequence regressions, and performance baselines.
- Recommend `explore-apple-swift-docs` for documentation research.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/vision-requests-observations-and-sequences.md`
- `references/vision-coordinates-live-frames-and-diagnostics.md`
- `references/customization-flow.md`
- `../../shared/references/apple-vision-analysis-contract.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
