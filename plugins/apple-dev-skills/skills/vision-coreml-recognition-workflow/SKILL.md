---
name: vision-coreml-recognition-workflow
description: Guide custom Core ML image classification, object detection, semantic segmentation, and feature-output integration through Apple Vision, including model provenance, configuration, image constraints, crop-and-scale behavior, typed observations, confidence, postprocessing, compute units, evaluation, and performance repair. Use when a custom Core ML model interprets images or video frames.
---

# Vision Core ML Recognition Workflow

## Purpose

Guide custom image-model integration through Vision while keeping Core ML model execution, Vision image semantics, preprocessing, postprocessing, evaluation, and capture ownership explicit.

## When To Use

- Use for custom Core ML image classification, object detection, segmentation, feature outputs, model loading, crop-and-scale, compute, evaluation, or recognition repair.
- Recommend `vision-image-analysis-workflow` when an Apple-provided Vision request already owns the analysis.
- Recommend direct Core ML guidance only when the input is not image-oriented or Vision does not support the model contract.

## Single-Path Workflow

1. Classify the model output:
   - classification labels
   - detected objects and boxes
   - semantic or instance segmentation
   - image-to-image or pixel-buffer output
   - feature value or embedding
   - multi-output or model-specific postprocessing
2. Apply the Apple docs gate:
   - read current Vision and Core ML documentation for the model and platform
   - prefer `CoreMLRequest` and the current Swift Vision API for new code when compatible
   - preserve `VNCoreMLModel` and `VNCoreMLRequest` as explicit original-API repair inputs
   - inspect `MLModelDescription`, image constraints, metadata, and `MLModelConfiguration`
   - apply `../../shared/references/apple-vision-analysis-contract.md`
3. Establish provenance and constraints:
   - establish immutable provenance for every shipped or downloaded model
   - record model source, version, license, checksum or immutable revision, labels, expected color space, dimensions, flexible constraints, output meanings, and known evaluation limits
   - pin the shipped model and document any compilation or download boundary
4. Configure execution:
   - select compute units from actual compatibility, energy, latency, memory, and profiling requirements
   - choose crop-and-scale behavior deliberately and preserve its inverse for output coordinates
   - keep typed Vision observations or Core ML feature values until the consumer boundary
5. Interpret and evaluate:
   - define thresholds and model-specific postprocessing from validation evidence
   - separate classification confidence from calibrated probability
   - map detection boxes or masks through preprocessing and display transforms
   - run representative fixtures and a small regression or evaluation sanity check whenever model or request logic changes
6. Return documented behavior, provenance, model contract, request family, preprocessing and postprocessing, compute plan, evaluation evidence, performance findings, and handoffs.

## Inputs

- `request`: custom image-model integration or repair task.
- `recognition_goal`: `classify`, `detect`, `segment`, `image-output`, `feature-output`, `evaluate`, `profile`, or `repair`.
- `model_context`: model file, generated model class, `MLModel`, model asset, or documented remote acquisition boundary.
- `platform_context`: Apple platform, deployment target, and representative device classes.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `path_type`: `primary` for Vision-integrated custom image models, `fallback` for built-in Vision, non-image Core ML, capture, or execution.
- `output`: documented behavior, model provenance and contract, request configuration, coordinate plan, evaluation, performance, diagnostics, and handoff.

## Guards and Stop Conditions

- Do not ship an unpinned model or omit its source, version, labels, input/output meanings, and evaluation boundary.
- Do not choose `.all`, CPU, GPU, or Neural Engine policy from assumption; configure and profile representative devices.
- Do not treat confidence as calibrated probability, identity, authorization, safety, or correctness.
- Do not invent generic recognition managers or erase typed `CoreMLRequest`, `VNCoreMLRequest`, Vision observations, `MLFeatureValue`, `MLMultiArray`, or `CVPixelBuffer` results prematurely.
- Do not apply a detection box or segmentation mask without inverting crop, scale, orientation, region-of-interest, and display transforms.
- Do not claim model accuracy, fairness, robustness, real-time performance, or hardware-unit use without suitable evidence.
- Stop when model provenance, input/output contract, labels, preprocessing, or representative evaluation data is unavailable.

## Fallbacks and Handoffs

- Recommend `vision-image-analysis-workflow` for Apple-provided Vision requests, tracking, feature prints, coordinates, and sequence lifecycle.
- Recommend `core-image-processing-workflow` for pixel preprocessing or image-to-image rendering and `apple-image-representation-workflow` for decode and orientation ownership.
- Recommend `avfoundation-media-pipeline-workflow` for capture and frame delivery until the specialist camera workflow ships.
- Recommend `xcode-build-run-workflow` for model resources, generated classes, build, run, device profiling, or Instruments.
- Recommend `xcode-testing-workflow` for fixtures, evaluation harnesses, performance baselines, and regression tests.
- Recommend `explore-apple-swift-docs` for current Vision or Core ML research.

## Customization

Use `references/customization-flow.md`. This workflow defines no runtime-enforced knobs.

## References

- `references/vision-coreml-model-integration.md`
- `references/model-evaluation-performance-and-diagnostics.md`
- `references/customization-flow.md`
- `../../shared/references/apple-vision-analysis-contract.md`
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode-project policy.

## Script Inventory

- `scripts/customization_config.py`
