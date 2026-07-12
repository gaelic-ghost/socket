# World Tracking, Depth, Meshes, and Maps

## World Tracking

Choose `ARWorldTrackingConfiguration` only after checking support. Configure world alignment, plane detection, image/object detection, environment texturing, frame semantics, scene reconstruction, and video format from the actual feature requirement. Observe `ARCamera.TrackingState` and explain limited-state reasons; do not hide tracking loss behind stale anchors.

Use anchor identifiers and transforms as session-relative spatial state. Define world-origin changes explicitly. Use ray casting for supported surface queries and preserve query type, alignment, target, result transform, and tracking state. Treat raw feature points as sparse estimates, not a surface model.

## Scene Depth and Reconstruction

Check `supportsFrameSemantics(.sceneDepth)` or `.smoothedSceneDepth` before enabling them. Preserve depth map, confidence map, calibration/orientation relationship, timestamp, and source frame. Smoothed depth trades responsiveness/detail for stability; choose from product behavior.

Check `supportsSceneReconstruction` before selecting mesh or mesh-with-classification. Preserve `ARMeshAnchor`, `ARMeshGeometry`, vertices, normals, faces, classification, anchor transform, and update/removal lifecycle. Mesh classification is an estimate and may change as the scene is rescanned.

## Maps, Images, Objects, and Geography

Persist `ARWorldMap` only after checking mapping status and defining a versioned, protected, deletable storage boundary. Restoring a map begins relocalization; it does not guarantee immediate or successful spatial continuity. Surface relocalization state and provide a deliberate reset path.

Keep reference images and `ARReferenceObject` provenance, physical dimensions, resource lifecycle, and detection limits explicit. Route object scanning and authoring to the documented scanning workflow rather than inventing runtime reference objects from arbitrary meshes.

Treat geographic anchors as location-sensitive and capability/availability dependent. Preserve localization state, location authorization, accuracy, and fallback behavior.
